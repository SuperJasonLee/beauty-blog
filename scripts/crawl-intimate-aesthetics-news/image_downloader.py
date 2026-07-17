"""Image downloader for intimate area plastic surgery article."""
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "intimate-plastic-surgery-aesthetics-2026-07"
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
    # Source images from the June intimate area pipeline (Pexels-licensed medical consultation images)
    JUNE_DIR = REPO_ROOT / "static" / "images" / "posts" / "intimate-plastic-surgery-2026-06"

    CANDIDATES = [
        (JUNE_DIR / "image-1.jpg",
         "https://www.pexels.com/photo/a-doctor-sitting-at-a-desk-7578797/",
         "cottonbro", "https://www.pexels.com/@cottonbro/",
         "医美咨询：医生办公桌前与患者沟通的专业场景"),
        (JUNE_DIR / "image-2.jpg",
         "https://www.pexels.com/photo/woman-in-white-suit-with-stethoscope-talking-to-a-person-7579823/",
         "cottonbro", "https://www.pexels.com/@cottonbro/",
         "专业医师问诊：穿着白大褂的医生与患者深入沟通"),
        (JUNE_DIR / "image-3.jpg",
         "https://www.pexels.com/photo/photo-of-an-ob-gyn-sitting-beside-ultrasound-machine-7089394/",
         "MART PRODUCTION", "https://www.pexels.com/@mart-production/",
         "妇产科诊疗环境：超声设备旁的临床场景"),
        (JUNE_DIR / "image-4.jpg",
         "https://www.pexels.com/photo/a-doctor-consulting-a-patient-7659876/",
         "Thirdman", "https://www.pexels.com/@thirdman/",
         "医患沟通：专业咨询场景下的信息传递"),
        (JUNE_DIR / "image-5.jpg",
         "https://www.pexels.com/photo/a-doctor-looking-to-the-laptop-8376239/",
         "Tima Miroshnichenko", "https://www.pexels.com/@tima-miroshnichenko/",
         "数字化医疗：医生使用笔记本电脑进行诊疗记录"),
    ]

    out_map = {}
    for idx, (src_path, page_url, author, author_url, theme) in enumerate(CANDIDATES, start=1):
        if not src_path.exists():
            logger.warning(f"Source not found: {src_path}; skipping image-{idx}.jpg")
            continue
        out_path = IMAGES_DIR / f"image-{idx}.jpg"
        size = resize_to_budget(src_path, out_path)
        rel = f"posts/intimate-plastic-surgery-aesthetics-2026-07/image-{idx}.jpg"
        public = f"/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-{idx}.jpg"
        append_credits_row(rel, page_url, "Pexels License", author, author_url, today)
        logger.info(f"  [OK] image-{idx}.jpg ({size // 1024} KB) — {theme}")
        out_map[f"image-{idx}.jpg"] = public
    if len(out_map) < 3:
        raise RuntimeError(f"Only {len(out_map)} images copied (< 3 minimum)")
    return out_map


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
