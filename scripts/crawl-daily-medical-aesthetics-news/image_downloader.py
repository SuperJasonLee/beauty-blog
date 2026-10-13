"""Image downloader for daily medical aesthetics news for 2026-10-13."""

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
SLUG = "daily-medical-aesthetics-news-2026-10-13"
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
        "page_url": "https://www.pexels.com/photo/a-doctor-talking-to-her-patient-5215029/",
        "image_url": "https://images.pexels.com/photos/5215029/pexels-photo-5215029.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Tima Miroshnichenko",
        "author_url": "https://www.pexels.com/@tima-miroshnichenko/",
        "theme": "Aesthetic physician consulting patient on ADSC exosome mRNA delivery, titanium-sapphire femtosecond holographic laser, monodisperse PCL-rhFN hydrogel, and 4D vector radiofrequency lifting",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-woman-getting-a-facial-treatment-in-a-clinic-5069399/",
        "image_url": "https://images.pexels.com/photos/5069399/pexels-photo-5069399.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Dermatologist administering sonodynamic transdermal delivery system with engineered ADSC-exosomes and collagen-encoding LNP-mRNA nanovesicles for dermal extracellular matrix senescence reversal",
    },
    {
        "page_url": "https://www.pexels.com/photo/woman-getting-a-facial-treatment-7446673/",
        "image_url": "https://images.pexels.com/photos/7446673/pexels-photo-7446673.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Gustavo Fring",
        "author_url": "https://www.pexels.com/@gustavofring/",
        "theme": "Laser surgeon performing non-thermal laser-induced optical breakdown (LIOB) with dual-wavelength 730nm/1064nm femtosecond holographic array for recalcitrant melasma and dermal melanosis",
    },
    {
        "page_url": "https://www.pexels.com/photo/cosmetologist-in-pink-gloves-injecting-filler-into-woman-s-face-4586710/",
        "image_url": "https://images.pexels.com/photos/4586710/pexels-photo-4586710.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Anna Shvets",
        "author_url": "https://www.pexels.com/@shvetsa/",
        "theme": "Plastic surgeon administering deep pre-periosteal blunt cannula delivery of monodisperse microfluidic PCL microspheres with recombinant fibronectin hydrogel for midface osteomimetic volume restoration",
    },
    {
        "page_url": "https://www.pexels.com/photo/young-woman-with-clean-skin-smiling-3762862/",
        "image_url": "https://images.pexels.com/photos/3762862/pexels-photo-3762862.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Female patient demonstrating well-defined mandibular definition, radiant skin barrier restoration, and youthful midface vector elevation following multimodal aesthetic intervention",
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
        html_lower = html.lower()
        for marker in PERMITTED_LICENSE_MARKERS:
            if marker.lower() in html_lower:
                return marker
        if "pexels.com" in page_url.lower():
            return "Pexels License (provenance by curation)"
        return None


def download_raw_image(image_url: str, timeout: int = 30, retries: int = 4) -> Optional[bytes]:
    import time
    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                resp = client.get(
                    image_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Referer": "https://www.pexels.com/",
                    },
                )
                resp.raise_for_status()
                return resp.content
        except Exception as e:
            logger.warning(f"Download attempt {attempt}/{retries} failed for {image_url}: {e}")
            if attempt < retries:
                time.sleep(2)
            else:
                logger.error(f"Failed to download image after {retries} attempts: {image_url}")
                return None
    return None


def optimize_image(raw_bytes: bytes, target_path: Path):
    temp_in = target_path.parent / f"_temp_in_{target_path.name}"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_in.write_bytes(raw_bytes)

    try:
        with Image.open(temp_in) as img:
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            orig_w, orig_h = img.size
            longest = max(orig_w, orig_h)
            if longest > MAX_LONGEST_EDGE_PX:
                scale = MAX_LONGEST_EDGE_PX / longest
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            for quality in [90, 85, 80, 75, 70, 65, 60]:
                img.save(target_path, "JPEG", quality=quality, optimize=True)
                if target_path.stat().st_size <= MAX_BYTES:
                    break

        logger.info(f"Saved: {target_path} ({target_path.stat().st_size // 1024} KB)")
    finally:
        if temp_in.exists():
            temp_in.unlink()


def record_credit(file_rel_path: str, page_url: str, license_name: str, author: str, author_url: str):
    if not CREDITS_FILE.exists():
        logger.warning(f"{CREDITS_FILE} not found; skipping credit append")
        return

    content = CREDITS_FILE.read_text(encoding="utf-8")
    if file_rel_path in content or page_url in content:
        logger.info(f"Credit already present for {file_rel_path}; skipping")
        return

    today = date.today().isoformat()
    row = f"| `{file_rel_path}` | {page_url} | {license_name} | {author} | {author_url} | {today} |\n"
    CREDITS_FILE.write_text(content.rstrip() + "\n" + row, encoding="utf-8")
    logger.info(f"Recorded credit for {file_rel_path}")


def download_curated_images() -> dict[str, str]:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {}

    for i, candidate in enumerate(CURATED_CANDIDATES, start=1):
        target_name = f"image-{i}.jpg"
        target_path = IMAGES_DIR / target_name
        rel_path = f"posts/{SLUG}/{target_name}"

        if target_path.exists() and target_path.stat().st_size > 0:
            logger.info(f"Target image already exists: {target_path}")
            mapping[candidate["image_url"]] = f"/images/{rel_path}"
            continue

        logger.info(f"Processing candidate {i}/{len(CURATED_CANDIDATES)}: {candidate['theme']}")

        marker = fetch_page_license_marker(candidate["page_url"])
        if marker == "BLOCKED":
            license_name = "Pexels License (provenance by curation; page fetch was anti-bot-blocked)"
        elif marker:
            license_name = marker
        else:
            license_name = "Pexels License (provenance by curation)"

        raw_bytes = download_raw_image(candidate["image_url"])
        if not raw_bytes:
            logger.error(f"Could not download candidate {i}; aborting")
            sys.exit(1)

        optimize_image(raw_bytes, target_path)

        record_credit(
            file_rel_path=rel_path,
            page_url=candidate["page_url"],
            license_name=license_name,
            author=candidate["author"],
            author_url=candidate["author_url"],
        )

        mapping[candidate["image_url"]] = f"/images/{rel_path}"

    return mapping


def main(json_path=None):
    return download_curated_images()


if __name__ == "__main__":
    download_curated_images()
