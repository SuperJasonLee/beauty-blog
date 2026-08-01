"""Download 5 curated eye-surgery images from Pexels, resize to budget, update CREDITS."""
import httpx
import re
from datetime import date
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(r"E:\git_local\beauty-blog")
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "eye-surgery-aesthetics-2026-08"
CREDITS_FILE = REPO_ROOT / "static" / "images" / "CREDITS.md"

MAX_EDGE = 1600
MAX_BYTES = 300 * 1024

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 5 curated images from Pexels blepharoplasty search — diverse themes
CANDIDATES = [
    {
        "url": "https://images.pexels.com/photos/7585317/pexels-photo-7585317.jpeg?cs=srgb&dl=pexels-cottonbro-7585317.jpg&fm=jpg",
        "page": "https://www.pexels.com/photo/a-woman-with-markings-on-her-eyelid-7585317/",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Asian woman with eyelid markings preparing for blepharoplasty",
    },
    {
        "url": "https://images.pexels.com/photos/7585310/pexels-photo-7585310.jpeg?cs=srgb&dl=pexels-cottonbro-7585310.jpg&fm=jpg",
        "page": "https://www.pexels.com/photo/a-plastic-surgeon-measuring-the-patient-s-eyelids-by-using-a-caliper-7585310/",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Surgeon measuring patient eyelids with calipers pre-op",
    },
    {
        "url": "https://images.pexels.com/photos/7298683/pexels-photo-7298683.jpeg?cs=srgb&dl=pexels-kindelmedia-7298683.jpg&fm=jpg",
        "page": "https://www.pexels.com/photo/extreme-close-up-photo-of-woman-s-eyes-7298683/",
        "author": "Kindel Media",
        "author_url": "https://www.pexels.com/@kindelmedia/",
        "theme": "Extreme close-up of woman eyes — double eyelid beauty standard",
    },
    {
        "url": "https://images.pexels.com/photos/7585314/pexels-photo-7585314.jpeg?cs=srgb&dl=pexels-cottonbro-7585314.jpg&fm=jpg",
        "page": "https://www.pexels.com/photo/hands-woman-face-professional-7585314/",
        "author": "cottonbro studio",
        "author_url": "https://www.pexels.com/@cottonbro/",
        "theme": "Surgeon preparing for blepharoplasty — pre-op clinical setting",
    },
    {
        "url": "https://images.pexels.com/photos/33857825/pexels-photo-33857825.jpeg?cs=srgb&dl=pexels-fernando-capetillo-94107723-33857825.jpg&fm=jpg",
        "page": "https://www.pexels.com/photo/eye-surgery-preparation-in-medical-facility-33857825/",
        "author": "Fernando Capetillo",
        "author_url": "https://www.pexels.com/@fernando-capetillo/",
        "theme": "Patient eye surgery preparation in medical facility",
    },
]

headers = {"User-Agent": "Mozilla/5.0 (BeautyBlog/1.0)"}
today = date.today().isoformat()

def download_and_resize(url: str, out_path: Path) -> int:
    resp = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
    resp.raise_for_status()
    tmp = out_path.with_suffix(".tmp.jpg")
    tmp.write_bytes(resp.content)
    img = Image.open(tmp).convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_EDGE:
        scale = MAX_EDGE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    quality = 85
    while True:
        img.save(out_path, format="JPEG", quality=quality, optimize=True)
        sz = out_path.stat().st_size
        if sz <= MAX_BYTES or quality <= 40:
            tmp.unlink(missing_ok=True)
            return sz
        quality -= 5

downloaded = []
for i, c in enumerate(CANDIDATES, 1):
    fname = f"image-{i}.jpg"
    fpath = IMAGES_DIR / fname
    try:
        sz = download_and_resize(c["url"], fpath)
        downloaded.append({"file": fname, "path": str(fpath), "size": sz, **c})
        print(f"[OK] {fname}  ({sz//1024} KB)")
    except Exception as e:
        print(f"[FAIL] {fname}: {e}")

# Update CREDITS.md
if CREDITS_FILE.exists():
    header = CREDITS_FILE.read_text(encoding="utf-8")
else:
    header = "# Image Credits\n\n| File | Source URL | License | Author | Author URL | Date added |\n| --- | --- | --- | --- | --- | --- |\n"

lines = header.splitlines(keepends=True)
new_rows = []
for d in downloaded:
    new_rows.append(
        f"| {d['file']} | {d['page']} | Pexels License | [{d['author']}]({d['author_url']}) | {d['author_url']} | {today} |\n"
    )

# Insert new rows after header (skip the table header rows and blank line)
insert_idx = 0
for idx, line in enumerate(lines):
    if line.strip().startswith("| ---") and idx + 2 < len(lines):
        insert_idx = idx + 2
        break

if insert_idx:
    lines = lines[:insert_idx] + new_rows + lines[insert_idx:]
else:
    lines.extend(new_rows)

CREDITS_FILE.write_text("".join(lines), encoding="utf-8")
print(f"\nCREDITS.md updated with {len(downloaded)} entries.")
print(f"Images saved to: {IMAGES_DIR}")
print(f"Files: {[d['file'] for d in downloaded]}")
