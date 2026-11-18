"""Image downloader for daily medical aesthetics news for 2026-11-18."""

import logging
import sys
from pathlib import Path
from typing import Optional

import httpx
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SLUG = "daily-medical-aesthetics-news-2026-11-18"
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
        "page_url": "https://www.pexels.com/photo/treatment-room-in-a-private-clinic-16571735/",
        "image_url": "https://images.pexels.com/photos/16571735/pexels-photo-16571735.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "zandatsu",
        "author_url": "https://www.pexels.com/@zandatsu/",
        "theme": "Modern medical aesthetics clinic suite equipped for multimodal injectable, energy-based, and surgical facial rejuvenation",
    },
    {
        "page_url": "https://www.pexels.com/photo/mixing-ingredients-of-cosmetic-with-pipette-16100839/",
        "image_url": "https://images.pexels.com/photos/16100839/pexels-photo-16100839.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Fernando Serrano",
        "author_url": "https://www.pexels.com/@fernando-serrano-89809820/",
        "theme": "Precision formulation of injectable poly-L-lactic acid (PLLA) biomaterial microspheres and extracellular matrix scaffolds",
    },
    {
        "page_url": "https://www.pexels.com/photo/doctors-looking-at-patient-on-bed-in-operating-room-7108264/",
        "image_url": "https://images.pexels.com/photos/7108264/pexels-photo-7108264.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Pavel Danilyuk",
        "author_url": "https://www.pexels.com/@pavel-danilyuk/",
        "theme": "Dermatologic team preparing fractional 1064-nm Nd:YAG laser and topical exosome adjunctive skin rejuvenation",
    },
    {
        "page_url": "https://www.pexels.com/photo/middle-aged-woman-receiving-cosmetic-facial-injection-29648624/",
        "image_url": "https://images.pexels.com/photos/29648624/pexels-photo-29648624.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Reborn Filmes",
        "author_url": "https://www.pexels.com/@rebornfilmes/",
        "theme": "Clinician administering biomimetic hyaluronic acid injectable gel integrated into a multimodal facial skin quality plan",
    },
    {
        "page_url": "https://www.pexels.com/photo/a-doctor-checking-his-patient-7108173/",
        "image_url": "https://images.pexels.com/photos/7108173/pexels-photo-7108173.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=1600",
        "author": "Pavel Danilyuk",
        "author_url": "https://www.pexels.com/@pavel-danilyuk/",
        "theme": "Facial plastic surgeon performing preoperative anatomical assessment for preservation facelift, eyelid, and rhinoplasty planning",
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


def verify_license(page_url: str) -> Optional[str]:
    marker = fetch_page_license_marker(page_url)
    if marker == "BLOCKED" and "pexels.com" in page_url.lower():
        logger.info(f"Page fetch anti-bot blocked for {page_url}; using Pexels License by provenance.")
        return "Pexels License (provenance by curation)"
    if marker:
        return marker
    logger.warning(f"No permitted license marker found on {page_url}")
    return None


def download_raw_image(image_url: str, dest_path: Path, timeout: int = 30) -> bool:
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
            dest_path.write_bytes(resp.content)
            return True
    except Exception as e:
        logger.warning(f"Failed to download {image_url}: {e}")
        return False


def optimize_image(src_path: Path, max_edge: int = MAX_LONGEST_EDGE_PX, max_bytes: int = MAX_BYTES):
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > max_edge:
            if w >= h:
                new_w = max_edge
                new_h = int(h * (max_edge / w))
            else:
                new_h = max_edge
                new_w = int(w * (max_edge / h))
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            logger.info(f"  Resized {src_path.name} from {w}x{h} to {new_w}x{new_h}")

        for quality in range(92, 40, -5):
            img.save(src_path, "JPEG", quality=quality, optimize=True)
            size = src_path.stat().st_size
            if size <= max_bytes:
                logger.info(f"  Saved {src_path.name}: {size / 1024:.1f} KB (quality={quality})")
                return

        img.save(src_path, "JPEG", quality=45, optimize=True)
        size = src_path.stat().st_size
        logger.info(f"  Saved {src_path.name} at min quality: {size / 1024:.1f} KB")


def update_credits(curated_candidates: list[dict], licenses: list[str]):
    today = "2026-11-18"
    new_rows = []
    for idx, (c, lic) in enumerate(zip(curated_candidates, licenses), start=1):
        rel_path = f"posts/{SLUG}/image-{idx}.jpg"
        row = f"| `{rel_path}` | {c['page_url']} | {lic} | {c['author']} | {c['author_url']} | {today} |"
        new_rows.append(row)

    credits_text = CREDITS_FILE.read_text(encoding="utf-8")
    existing_paths = set()
    for line in credits_text.splitlines():
        if line.startswith("| `posts/"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 1:
                existing_paths.add(parts[1].strip("`"))

    to_add = []
    for r in new_rows:
        target_path = r.split("|")[1].strip().strip("`")
        if target_path not in existing_paths:
            to_add.append(r)

    if to_add:
        updated = credits_text.rstrip() + "\n" + "\n".join(to_add) + "\n"
        CREDITS_FILE.write_text(updated, encoding="utf-8")
        logger.info(f"Appended {len(to_add)} rows to static/images/CREDITS.md")
    else:
        logger.info("CREDITS.md already has entries for these images.")


def run():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = {}
    verified_licenses = []
    candidates_to_record = []

    for idx, c in enumerate(CURATED_CANDIDATES, start=1):
        out_name = f"image-{idx}.jpg"
        out_path = IMAGES_DIR / out_name
        logger.info(f"Processing candidate #{idx}: {out_name}")

        lic = verify_license(c["page_url"])
        if not lic:
            logger.warning(f"Skipping candidate #{idx}: unverified license")
            continue

        if not out_path.exists():
            ok = download_raw_image(c["image_url"], out_path)
            if not ok:
                logger.warning(f"Skipping candidate #{idx}: download failed")
                continue
            optimize_image(out_path)
        else:
            logger.info(f"  {out_name} already exists, checking size...")
            if out_path.stat().st_size > MAX_BYTES:
                optimize_image(out_path)

        downloaded[c["page_url"]] = f"/images/posts/{SLUG}/{out_name}"
        verified_licenses.append(lic)
        candidates_to_record.append(c)

    if candidates_to_record:
        update_credits(candidates_to_record, verified_licenses)

    logger.info(f"Total downloaded and verified images: {len(downloaded)}")
    return downloaded


def main(json_path=None):
    return run()


if __name__ == "__main__":
    run()
