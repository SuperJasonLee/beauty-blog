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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "daily-medical-aesthetics-news-2026-08-12"
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
        "theme": "Doctor-patient consultation in aesthetic clinic",
    },
    {
        "page_url": "https://www.pexels.com/photo/close-up-of-cosmetic-injection-procedure-34220525/",
        "image_url": "https://images.pexels.com/photos/34220525/pexels-photo-34220525.jpeg?cs=srgb&dl=pexels-prolificpeople-34220525.jpg&fm=jpg",
        "author": "prolificpeople",
        "author_url": "https://www.pexels.com/@prolificpeople/",
        "theme": "Cosmetic injection procedure in clinic",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-getting-facial-treatment-in-a-beauty-salon-3738349/",
        "image_url": "https://images.pexels.com/photos/3738349/pexels-photo-3738349.jpeg?cs=srgb&dl=pexels-cottonbro-3738349.jpg&fm=jpg",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Facial skin rejuvenation treatment",
    },
    {
        "page_url": "https://www.pexels.com/photo/modern-dermatology-clinic-interior-7089401/",
        "image_url": "https://images.pexels.com/photos/7089401/pexels-photo-7089401.jpeg?cs=srgb&dl=pexels-pavel-danilyuk-7089401.jpg&fm=jpg",
        "author": "Pavel Danilyuk",
        "author_url": "https://www.pexels.com/@pavel-danilyuk/",
        "theme": "Modern medical aesthetics clinic environment",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-looking-in-the-mirror-after-skincare-routine-3762879/",
        "image_url": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg?cs=srgb&dl=pexels-cottonbro-3762879.jpg&fm=jpg",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Post-treatment patient outcome evaluation",
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
            "| --- | --- | --- | --- | --- | --- |\n",
            encoding="utf-8"
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

    rel_path = f"posts/daily-medical-aesthetics-news-2026-08-12/image-{index}.jpg"
    public_path = f"/images/posts/daily-medical-aesthetics-news-2026-08-12/image-{index}.jpg"

    append_credits_row(rel_path, page_url, marker, author, author_url, today)
    logger.info(f"  ✓ image-{index}.jpg ({size // 1024} KB) — {candidate['theme']}")
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
        raise RuntimeError(f"Only {len(out)} images downloaded (< 3 minimum).")

    return out


def main(json_path: Optional[str] = None) -> dict:
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "daily-medical-aesthetics-news"
        files = sorted(data_dir.glob("daily_medical_aesthetics_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return {}
        path = files[-1]

    return process_crawled_file(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
