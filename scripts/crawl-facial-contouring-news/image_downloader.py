"""Image downloader for facial-contouring article."""
import logging
import shutil
from datetime import date
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WEB_ARTICLES = REPO_ROOT / "web-articles"
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "facial-contouring-aesthetics-2026-07"
CREDITS_FILE = REPO_ROOT / "static" / "images" / "CREDITS.md"
MAX_LONGEST_EDGE_PX = 1600
MAX_BYTES = 300 * 1024

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


def resize_to_budget(in_path: Path, out_path: Path, max_edge: int = MAX_LONGEST_EDGE_PX, max_bytes: int = MAX_BYTES) -> int:
    if Image is None:
        shutil.copy2(in_path, out_path)
        return out_path.stat().st_size
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
        CREDITS_FILE.write_text("# Image Credits\n\n| File | Source URL | License | Author | Author URL | Date added |\n| --- | --- | --- | --- | --- | --- |\n")


def append_credits_row(rel_path: str, page_url: str, license_marker: str, author: str, author_url: str, today: str):
    ensure_credits_header()
    row = f"| `{rel_path}` | {page_url} | {license_marker} | {author} | {author_url} | {today} |\n"
    with CREDITS_FILE.open("a", encoding="utf-8") as f:
        f.write(row)


def main(json_path=None):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    CANDIDATES = [
        ("Best_Facial+contouring+botox+jawline_Photos", "img_001.jpeg",
         "https://www.pexels.com/photo/close-up-photo-of-injecting-botox-on-forehead-7581590/",
         "cottonbro", "https://www.pexels.com/@cottonbro/", "肉毒素额头注射特写"),
        ("Best_Facial+contouring+botox+jawline_Photos", "img_002.jpeg",
         "https://www.pexels.com/photo/professional-cosmetic-injection-procedure-in-spa-34220536/",
         "prolificpeople", "https://www.pexels.com/@prolificpeople/", "SPA 环境肉毒素专业注射"),
        ("Best_Facial+contouring+botox+jawline_Photos", "img_011.jpeg",
         "https://www.pexels.com/photo/woman-getting-lip-injection-7446681/",
         "Gustavo Fring", "https://www.pexels.com/@gustavo-fring/", "面部注射治疗（唇部注射）"),
        ("Best_Woman+face+side+profile+jawline_Photos", "img_004.jpeg",
         "https://www.pexels.com/photo/close-up-photo-of-person-s-side-profile-7298654/",
         "Kindel Media", "https://www.pexels.com/@kindelmedia/", "面部侧颜/下颌线轮廓"),
        ("Best_Facial+contouring+botox+jawline_Photos", "img_014.jpeg",
         "https://www.pexels.com/photo/professional-aesthetic-nurse-performing-cosmetic-treatment-34220533/",
         "prolificpeople", "https://www.pexels.com/@prolificpeople/", "医美护士规范注射治疗"),
    ]
    out_map = {}
    for idx, (src_dir, src_file, page_url, author, author_url, theme) in enumerate(CANDIDATES, start=1):
        src_path = WEB_ARTICLES / src_dir / "images" / src_file
        if not src_path.exists():
            logger.warning(f"Source not found: {src_path}; skipping image-{idx}.jpg")
            continue
        out_path = IMAGES_DIR / f"image-{idx}.jpg"
        size = resize_to_budget(src_path, out_path)
        rel = f"posts/facial-contouring-aesthetics-2026-07/image-{idx}.jpg"
        public = f"/images/posts/facial-contouring-aesthetics-2026-07/image-{idx}.jpg"
        append_credits_row(rel, page_url, "Pexels License", author, author_url, today)
        logger.info(f"  ✓ image-{idx}.jpg ({size // 1024} KB) — {theme}")
        out_map[f"image-{idx}.jpg"] = public
    if len(out_map) < 3:
        raise RuntimeError(f"Only {len(out_map)} images copied (< 3 minimum)")
    return out_map


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
