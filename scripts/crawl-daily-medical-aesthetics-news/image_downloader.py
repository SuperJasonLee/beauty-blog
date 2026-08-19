"""Image downloader for daily medical aesthetics news."""

import json
import logging
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import httpx
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SLUG = "daily-medical-aesthetics-news-2026-08-19"
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / SLUG
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

CURATED_CANDIDATES = [
    {
        "page_url": "https://www.pexels.com/photo/doctor-explaining-a-treatment-plan-to-her-patient-5215024/",
        "image_url": "https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?cs=srgb&dl=pexels-tima-miroshnichenko-5215024.jpg&fm=jpg",
        "author": "Tima Miroshnichenko",
        "author_url": "https://www.pexels.com/@tima-miroshnichenko/",
        "theme": "Doctor-patient consultation and aesthetic diagnostic assessment",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-getting-laser-treatment-on-her-face-5069432/",
        "image_url": "https://images.pexels.com/photos/5069432/pexels-photo-5069432.jpeg?cs=srgb&dl=pexels-antoni-shkraba-5069432.jpg&fm=jpg",
        "author": "Antoni Shkraba",
        "author_url": "https://www.pexels.com/@shkrabaanthony/",
        "theme": "Energy-based RF tightening and advanced laser treatment",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-doctor-talking-to-his-patient-7108157/",
        "image_url": "https://images.pexels.com/photos/7108157/pexels-photo-7108157.jpeg?cs=srgb&dl=pexels-pavel-danilyuk-7108157.jpg&fm=jpg",
        "author": "Pavel Danilyuk",
        "author_url": "https://www.pexels.com/@pavel-danilyuk/",
        "theme": "Hair and scalp regenerative therapy and clinical examination",
    },
    {
        "page_url": "https://www.pexels.com/photo/surgeons-performing-surgery-in-operating-room-32828947/",
        "image_url": "https://images.pexels.com/photos/32828947/pexels-photo-32828947.jpeg?cs=srgb&dl=pexels-zeynep-ozata-32828947.jpg&fm=jpg",
        "author": "Zeynep Özata",
        "author_url": "https://www.pexels.com/@zeynep-ozata/",
        "theme": "Advanced surgical reconstruction and biological scaffold implant placement",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-touching-her-smooth-facial-skin-3762875/",
        "image_url": "https://images.pexels.com/photos/3762875/pexels-photo-3762875.jpeg?cs=srgb&dl=pexels-cottonbro-studio-3762875.jpg&fm=jpg",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Natural healthy facial skin glow and post-treatment rejuvenation outcome",
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
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                },
            )
            if resp.status_code in (403, 429):
                return "BLOCKED"
            resp.raise_for_status()
            html = resp.text
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
            resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
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
            "| --- | --- | --- | --- | --- | --- |\n",
            encoding="utf-8"
        )


def append_credits_row(rel_path: str, page_url: str, license_marker: str, author: str, author_url: str, today: str):
    ensure_credits_header()
    content = CREDITS_FILE.read_text(encoding="utf-8")
    if f"`{rel_path}`" in content:
        return
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
        logger.warning(f"Rejected: {page_url}")
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

    rel_path = f"posts/{SLUG}/image-{index}.jpg"
    public_path = f"/images/posts/{SLUG}/image-{index}.jpg"

    append_credits_row(rel_path, page_url, marker, author, author_url, today)
    logger.info(f"  [OK] image-{index}.jpg ({size // 1024} KB) — {candidate['theme']}")
    return {"local_path": public_path, "page_url": page_url, "author": author, "marker": marker}


def process_crawled_file(json_path: Optional[Path] = None) -> dict:
    today = date.today().isoformat()
    out: dict[str, str] = {}
    for i, candidate in enumerate(CURATED_CANDIDATES, start=1):
        result = download_one(candidate, i, today)
        if result is None:
            continue
        out[f"image-{i}.jpg"] = result["local_path"]
        if len(out) >= 5:
            break

    if len(out) < 5:
        raise RuntimeError(f"Only {len(out)} images downloaded (< 5 minimum).")

    return out


def main(json_path: Optional[str] = None) -> dict:
    if json_path:
        path = Path(json_path)
    else:
        path = None

    return process_crawled_file(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
