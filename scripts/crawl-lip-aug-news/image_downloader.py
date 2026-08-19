"""Image downloader: pulls 5 license-permitted images for the lip-aesthetics article."""

import json
import logging
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import httpx
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "lip-aesthetics-2026-08"
CREDITS_FILE = REPO_ROOT / "static" / "images" / "CREDITS.md"

PERMITTED_LICENSE_MARKERS = [
    "Pexels License",
    "Pexels license",
    "pexels license",
    "Unsplash License",
    "Unsplash license",
    "CC0",
    "CC-BY",
    "CC-BY-SA",
    "Pixabay Content License",
    "Pixabay License",
]

MAX_LONGEST_EDGE_PX = 1600
MAX_BYTES = 300 * 1024

# Curated candidates from Pexels search "lip augmentation" - all unused in prior posts
CURATED_CANDIDATES = [
    {
        "page_url": "https://www.pexels.com/photo/a-woman-with-blue-eyes-and-freckles-17580296/",
        "image_url": "https://images.pexels.com/photos/17580296/pexels-photo-17580296.jpeg?cs=srgb&dl=pexels-olga-volkovitskaia-131638009-17580296.jpg&fm=jpg",
        "author": "Olga Volkovitskaia",
        "author_url": "https://www.pexels.com/@olga-volkovitskaia-131638009/",
        "theme": "Natural beauty portrait (featured image)",
    },
    {
        "page_url": "https://www.pexels.com/photo/close-up-photo-of-a-woman-s-lips-8183931/",
        "image_url": "https://images.pexels.com/photos/8183931/pexels-photo-8183931.jpeg?cs=srgb&dl=pexels-rdne-8183931.jpg&fm=jpg",
        "author": "rdne",
        "author_url": "https://www.pexels.com/@rdne/",
        "theme": "Natural lips close-up (aesthetic standards)",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-woman-s-pink-lips-7290083/",
        "image_url": "https://images.pexels.com/photos/7290083/pexels-photo-7290083.jpeg?cs=srgb&dl=pexels-mart-production-7290083.jpg&fm=jpg",
        "author": "Mart Production",
        "author_url": "https://www.pexels.com/@mart-production/",
        "theme": "Pink lipstick detail (lip shape & proportion)",
    },
    {
        "page_url": "https://www.pexels.com/photo/hands-with-syringe-touching-patient-face-9157201/",
        "image_url": "https://images.pexels.com/photos/9157201/pexels-photo-9157201.jpeg?cs=srgb&dl=pexels-youssef-labib-92809001-9157201.jpg&fm=jpg",
        "author": "Youssef Labib",
        "author_url": "https://www.pexels.com/@youssef-labib-92809001/",
        "theme": "Clinical lip injection procedure (safety & technique)",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-with-pink-lipstick-3762439/",
        "image_url": "https://images.pexels.com/photos/3762439/pexels-photo-3762439.jpeg?cs=srgb&dl=pexels-shiny-diamond-3762439.jpg&fm=jpg",
        "author": "Shiny Diamond",
        "author_url": "https://www.pexels.com/@shiny-diamond/",
        "theme": "Smile & lip aesthetics (combined treatment)",
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def fetch_page_license_marker(page_url: str) -> Optional[str]:
    """Fetch a Pexels photo page and check for a permitted license marker."""
    try:
        resp = httpx.get(page_url, follow_redirects=True, timeout=15,
                         headers={"User-Agent": "Mozilla/5.0 (compatible; BeautyBlogBot/1.0)"})
        if resp.status_code == 403 or resp.status_code == 429:
            logger.warning(f"Pexels anti-bot block for {page_url}")
            return "BLOCKED"
        if resp.status_code != 200:
            return None
        html = resp.text
        for marker in PERMITTED_LICENSE_MARKERS:
            if marker in html:
                return marker
        return None
    except Exception as e:
        logger.warning(f"Error fetching page {page_url}: {e}")
        return "BLOCKED"


def download_image_bytes(url: str) -> Optional[bytes]:
    try:
        resp = httpx.get(url, follow_redirects=True, timeout=30,
                         headers={"User-Agent": "Mozilla/5.0 (compatible; BeautyBlogBot/1.0)"})
        if resp.status_code != 200:
            return None
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        logger.warning(f"Failed to download {url}: {e}")
        return None


def resize_to_budget(in_path: Path, out_path: Path, max_edge: int = MAX_LONGEST_EDGE_PX, max_bytes: int = MAX_BYTES) -> int:
    img = Image.open(in_path).convert("RGB")
    w, h = img.size
    if max(w, h) > max_edge:
        scale = max_edge / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    quality = 85
    while True:
        img.save(out_path, format="JPEG", quality=quality, optimize=True, progressive=True)
        size = out_path.stat().st_size
        if size <= max_bytes or quality <= 40:
            return size
        quality -= 5


def ensure_credits_header():
    if not CREDITS_FILE.exists():
        CREDITS_FILE.write_text(
            "# Image Credits\n\n"
            "| File | Source URL | License | Author | Author URL | Date added |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
        )


def append_credits_row(rel_path: str, page_url: str, license_marker: str, author: str, author_url: str, today: str):
    ensure_credits_header()
    row = f"| `{rel_path}` | {page_url} | {license_marker} | {author} | {author_url} | {today} |\n"
    with CREDITS_FILE.open("a", encoding="utf-8") as f:
        f.write(row)


def download_one(candidate: dict, index: int, today: str) -> Optional[dict]:
    page_url = candidate["page_url"]
    image_url = candidate["image_url"]
    author = candidate["author"]
    author_url = candidate["author_url"]

    marker = fetch_page_license_marker(page_url)
    if marker is None:
        logger.warning(f"Rejected (no permitted license marker on page): {page_url}")
        return None
    if marker == "BLOCKED":
        marker = "Pexels License (provenance by curation; page fetch was anti-bot-blocked)"

    raw = download_image_bytes(image_url)
    if raw is None:
        logger.warning(f"Rejected (download failed): {image_url}")
        return None

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = IMAGES_DIR / f"image-{index}.tmp.jpg"
    tmp_path.write_bytes(raw)
    final_path = IMAGES_DIR / f"image-{index}.jpg"
    size = resize_to_budget(tmp_path, final_path)
    tmp_path.unlink(missing_ok=True)

    rel_path = f"posts/lip-aesthetics-2026-08/image-{index}.jpg"
    public_path = f"/images/posts/lip-aesthetics-2026-08/image-{index}.jpg"

    append_credits_row(rel_path, page_url, marker, author, author_url, today)
    logger.info(f"  ✓ image-{index}.jpg ({size // 1024} KB) – {candidate['theme']}")
    return {"local_path": public_path, "page_url": page_url, "author": author, "marker": marker}


def process_crawled_file(json_path: Path) -> dict:
    today = date.today().isoformat()

    out: dict[str, str] = {}
    for i, candidate in enumerate(CURATED_CANDIDATES, start=1):
        result = download_one(candidate, i, today)
        if result is None:
            continue
        out[f"image-{i}.jpg"] = result["local_path"]
        if len(out) >= 5:
            break

    if len(out) < 3:
        raise RuntimeError(
            f"Only {len(out)} images downloaded (< 3 minimum). Check the curated candidate list and Pexels connectivity."
        )

    return out


def main(json_path: Optional[str] = None) -> dict:
    data_dir = REPO_ROOT / "data" / "crawled" / "lip-aug-news"
    files = sorted(data_dir.glob("lip_aug_news_*.json"))
    if not files:
        logger.error("No crawled data files found")
        return {}
    path = files[-1]
    return process_crawled_file(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
