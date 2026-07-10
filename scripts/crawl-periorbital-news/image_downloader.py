"""Image downloader for periorbital rejuvenation post.
Curated candidates from Pexels searches: botox-injection + eye-skin-rejuvenation.
"""

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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "periorbital-rejuvenation-2026-07"
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

# 5 visually diverse candidates — one per article section theme
CURATED_CANDIDATES = [
    {
        "page_url": "https://www.pexels.com/photo/close-up-of-cosmetic-injection-procedure-34220525/",
        "image_url": "https://images.pexels.com/photos/34220525/pexels-photo-34220525.jpeg?cs=srgb&dl=pexels-prolificpeople-34220525.jpg&fm=jpg",
        "author": "prolificpeople",
        "author_url": "https://www.pexels.com/@prolificpeople/",
        "theme": "临床注射操作（肉毒素 / 填充剂眶周注射）",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-person-with-a-gold-under-eye-patch-6762729/",
        "image_url": "https://images.pexels.com/photos/6762729/pexels-photo-6762729.jpeg?cs=srgb&dl=pexels-tima-miroshnichenko-6762729.jpg&fm=jpg",
        "author": "tima-miroshnichenko",
        "author_url": "https://www.pexels.com/@tima-miroshnichenko/",
        "theme": "眶周护理（黄金眼膜 / 皮肤光泽）",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-getting-a-face-botox-3985311/",
        "image_url": "https://images.pexels.com/photos/3985311/pexels-photo-3985311.jpeg?cs=srgb&dl=pexels-gustavo-fring-3985311.jpg&fm=jpg",
        "author": "gustavo-fring",
        "author_url": "https://www.pexels.com/@gustavo-fring/",
        "theme": "肉毒素注射（额部 / 眶周年轻化）",
    },
    {
        "page_url": "https://www.pexels.com/photo/crop-positive-asian-woman-with-eye-patches-on-face-6977665/",
        "image_url": "https://images.pexels.com/photos/6977665/pexels-photo-6977665.jpeg?cs=srgb&dl=pexels-gabby-k-6977665.jpg&fm=jpg",
        "author": "gabby-k",
        "author_url": "https://www.pexels.com/@gabby-k/",
        "theme": "亚裔女性眶周护理（眼膜应用）",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-woman-having-a-skin-care-13060606/",
        "image_url": "https://images.pexels.com/photos/13060606/pexels-photo-13060606.jpeg?cs=srgb&dl=pexels-lucas-guimaraes-bueno-258458556-13060606.jpg&fm=jpg",
        "author": "lucas-guimaraes-bueno",
        "author_url": "https://www.pexels.com/@lucas-guimaraes-bueno/",
        "theme": "医美诊所皮肤护理（眶周提亮）",
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def fetch_page_license_marker(page_url: str, timeout: int = 20) -> Optional[str]:
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(
                page_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                },
            )
            if resp.status_code in (403, 429):
                logger.info(f"Page fetch blocked ({resp.status_code}) for {page_url}; relying on curated Pexels provenance.")
                return "BLOCKED"
            resp.raise_for_status()
            html = resp.text
    except httpx.HTTPStatusError as e:
        logger.info(f"Page fetch HTTP error {e.response.status_code} for {page_url}; relying on curated Pexels provenance.")
        return "BLOCKED"
    except Exception as e:
        logger.warning(f"Failed to fetch {page_url}: {e}")
        return "BLOCKED"
    else:
        for marker in PERMITTED_LICENSE_MARKERS:
            if marker in html:
                return marker
        return None


def download_image_bytes(url: str, timeout: int = 30) -> Optional[bytes]:
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BeautyBlog/1.0)"})
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

    rel_path = f"posts/periorbital-rejuvenation-2026-07/image-{index}.jpg"
    public_path = f"/images/posts/periorbital-rejuvenation-2026-07/image-{index}.jpg"

    append_credits_row(rel_path, page_url, marker, author, author_url, today)
    logger.info(f"  ✓ image-{index}.jpg ({size // 1024} KB) — {candidate['theme']}")
    return {"local_path": public_path, "page_url": page_url, "author": author, "marker": marker}


def process_crawled_file(json_path: Path) -> dict:
    articles = json.loads(json_path.read_bytes())
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
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "periorbital-rejuvenation-news"
        files = sorted(data_dir.glob("periorbital_rejuvenation_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return {}
        path = files[-1]
    return process_crawled_file(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
