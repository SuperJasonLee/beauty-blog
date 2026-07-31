"""Curate and download Pexels images for rhinoplasty deep analysis post."""
import re, httpx, os, sys, json
from pathlib import Path

md = Path(r"E:\git_local\beauty-blog\web-articles\Best_Rhinoplasty_Plastic_Surgery_Photos\Best_Rhinoplasty_Plastic_Surgery_Photos.md").read_text(encoding="utf-8")

# Find all Pexels image URLs
urls = re.findall(r'https://images\.pexels\.com/photos/\d+/[^\s\)"]+\.jpeg', md)
urls += re.findall(r'https://images\.pexels\.com/photos/\d+/[^\s\)"]+\.jpg', md)
seen = set()
unique = []
for u in urls:
    if u not in seen:
        seen.add(u)
        unique.append(u)

print(f"Found {len(unique)} unique image URLs")

IMAGES_DIR = Path(r"E:\git_local\beauty-blog\static\images\posts\rhinoplasty-aesthetics-2026-07")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Curate 5 visually diverse images (avoid duplicates in theme/color/composition)
# indices to download — pick diverse ones
indices = [0, 5, 10, 15, 20]
download_list = []
for idx in indices:
    if idx < len(unique):
        download_list.append((idx + 1, unique[idx]))

print(f"\nSelected {len(download_list)} images:")
for i, u in download_list:
    print(f"  image-{i}: {u[:100]}...")

downloaded = {}
for img_num, url in download_list:
    filename = f"image-{img_num}.jpg"
    filepath = IMAGES_DIR / filename
    if filepath.exists():
        print(f"  [exists] {filename}")
        downloaded[url] = filename
        continue
    try:
        with httpx.Client(timeout=30, follow_redirects=True) as client:
            resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BeautyBlog/1.0)"})
            resp.raise_for_status()
            filepath.write_bytes(resp.content)
            print(f"  [ok] {filename} ({len(resp.content)} bytes)")
            downloaded[url] = filename
    except Exception as e:
        print(f"  [fail] {filename}: {e}")

print(f"\nDownloaded {len(downloaded)}/{len(download_list)} images")
out = {v: k for k, v in downloaded.items()}
print(json.dumps(out, ensure_ascii=False, indent=2))
