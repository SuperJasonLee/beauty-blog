import asyncio, json, os, re, hashlib
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests

from crawl4ai import AsyncWebCrawler

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

def download_image(url, prefix=""):
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return None
        ext = "jpg"
        ct = resp.headers.get("content-type", "")
        if "png" in ct: ext = "png"
        elif "webp" in ct: ext = "webp"
        elif "jpeg" in ct or "jpg" in ct: ext = "jpg"
        elif "gif" in ct: ext = "gif"
        name = f"{prefix}{hashlib.md5(url.encode()).hexdigest()[:10]}.{ext}"
        path = IMAGES_DIR / name
        path.write_bytes(resp.content)
        return str(path)
    except Exception as e:
        print(f"  [WARN] Failed: {url[:80]}: {e}")
        return None

async def crawl_for_images(url):
    """Crawl an article page specifically to find images."""
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            if not result.success:
                return []
            urls = set()
            for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', result.html, re.I):
                u = m.group(1)
                if u.startswith("data:"): continue
                full = urljoin(url, u)
                if any(x in full.lower() for x in ["logo","icon","avatar","sprite"]):
                    continue
                if any(full.lower().endswith(e) for e in [".jpg",".jpeg",".png",".webp"]):
                    urls.add(full)
            return list(urls)[:5]
    except Exception as e:
        print(f"  [WARN] Crawl failed for {url}: {e}")
        return []

def generate_cn_post(articles, image_map):
    lines = []
    lines.append(f"🗓️ 今日医美资讯速览 — 2026年5月31日\n")
    for i, art in enumerate(articles[:8]):
        lines.append(f"#{i+1} {art['title']}")
        lines.append(f"   📰 来源：{art.get('source', '网络')}")
        imgs = image_map.get(art.get("url",""), [])
        if imgs:
            lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art.get("summary"):
            s = art["summary"][:300].replace("\n", " ")
            lines.append(f"   💡 {s[:200]}")
        lines.append(f"   🔗 {art['url']}")
        lines.append("")
    lines.append("---")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 数据来源：crawl4ai 全网搜索")
    return "\n".join(lines)

def generate_en_post(articles, image_map):
    lines = []
    lines.append(f"🗓️ Medical Aesthetics News Roundup — May 31, 2026\n")
    for i, art in enumerate(articles[:6]):
        lines.append(f"#{i+1} {art['title']}")
        lines.append(f"   📰 {art.get('source', 'Source')}")
        imgs = image_map.get(art.get("url",""), [])
        if imgs:
            lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art.get("summary"):
            s = art["summary"][:300].replace("\n", " ")
            lines.append(f"   💡 {s[:200]}")
        lines.append(f"   🔗 {art['url']}")
        lines.append("")
    lines.append("---")
    lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} via crawl4ai")
    return "\n".join(lines)

async def main():
    json_path = BASE_DIR / "articles.json"
    if not json_path.exists():
        print("articles.json not found! Run crawl_news.py first.")
        return
    
    data = json.loads(json_path.read_text(encoding="utf-8"))
    articles = data.get("articles", [])
    print(f"Loaded {len(articles)} articles from articles.json")
    
    print("\n--- Crawling article pages for images ---")
    for i, art in enumerate(articles):
        url = art.get("url", "")
        if not url:
            continue
        existing = art.get("detail_images", []) or []
        if existing:
            print(f"  [{i+1}] Already has {len(existing)} images, skipping crawl")
            continue
        print(f"  [{i+1}] Crawling: {art['title'][:50]}...")
        imgs = await crawl_for_images(url)
        art["detail_images"] = imgs
        print(f"       Found {len(imgs)} images")
    
    print("\n--- Downloading images ---")
    image_map = {}
    for i, art in enumerate(articles):
        all_img_urls = []
        if art.get("image"):
            all_img_urls.append(art["image"])
        all_img_urls.extend(art.get("detail_images", []) or [])
        
        downloaded = []
        for j, img_url in enumerate(all_img_urls[:4]):
            if len(downloaded) >= 3:
                break
            path = download_image(img_url, f"art{i}_img{j}_")
            if path:
                downloaded.append(path)
                print(f"  [{i+1}] Downloaded: {os.path.basename(path)}")
        if downloaded:
            image_map[art.get("url", "")] = downloaded
    
    cn_articles = [a for a in articles if a.get("lang") == "zh"]
    en_articles = [a for a in articles if a.get("lang") == "en"]
    
    print("\n--- Generating bilingual post ---")
    cn_post = generate_cn_post(cn_articles, image_map)
    en_post = generate_en_post(en_articles if en_articles else cn_articles[:4], image_map)
    
    all_images = list(set(p for imgs in image_map.values() for p in imgs))
    
    post = {
        "date": "2026-05-31",
        "title_cn": "📋 今日医美资讯速览",
        "title_en": "📋 Today's Medical Aesthetics Roundup",
        "cn": cn_post,
        "en": en_post,
        "images": all_images,
    }
    
    post_path = BASE_DIR / "post.json"
    post_path.write_text(json.dumps(post, ensure_ascii=False, indent=2))
    
    md_path = BASE_DIR / "post.md"
    md_lines = []
    md_lines.append("---")
    md_lines.append(f"title: '📋 今日医美资讯速览 | Medical Aesthetics Roundup'")
    md_lines.append(f"date: 2026-05-31")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("# 📋 今日医美资讯速览")
    md_lines.append("")
    md_lines.append("## 🇨🇳 中文版")
    md_lines.append("")
    md_lines.append(cn_post)
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 🇬🇧 English Version")
    md_lines.append("")
    md_lines.append(en_post)
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 🖼️ 配图 / Images")
    md_lines.append("")
    for art in articles[:10]:
        imgs = image_map.get(art.get("url", ""), [])
        if imgs:
            md_lines.append(f"### {art['title']}")
            for img_path in imgs:
                rel = os.path.relpath(img_path, BASE_DIR)
                md_lines.append(f"  ![配图]({rel})")
            md_lines.append("")
    
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    
    print(f"\n{'=' * 60}")
    print(f"✅ 完成！输出保存至：")
    print(f"  📄 post.json — 结构化数据")
    print(f"  📄 post.md — 完整图文 Markdown")
    print(f"  🖼️  images/ — {len(all_images)} 张配图")
    print(f"{'=' * 60}")
    
    print("\n" + "=" * 60)
    print("📋 中文版预览")
    print("=" * 60)
    print(cn_post[:1000])
    print("\n" + "=" * 60)
    print("📋 English Preview")
    print("=" * 60)
    print(en_post[:800])

if __name__ == "__main__":
    asyncio.run(main())
