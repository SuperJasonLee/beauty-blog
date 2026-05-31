import asyncio, json, os, re, hashlib, sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip3 install requests -q")
    import requests

from crawl4ai import AsyncWebCrawler

OUTPUT_DIR = Path(__file__).parent
IMAGES_DIR = OUTPUT_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

def download_image(url, prefix=""):
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
        print(f"  [WARN] Failed to download {url}: {e}")
        return None

def extract_images(html, base_url, prefix=""):
    urls = []
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I):
        u = m.group(1)
        if u.startswith("data:"): continue
        full = urljoin(base_url, u)
        if any(x in full.lower() for x in ["logo", "icon", "avatar", "sprite", "banner", "thumb"]):
            continue
        if any(full.lower().endswith(e) for e in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
            urls.append(full)
        elif re.search(r'[?&]img=|image=|photo=|pic=', full.lower()):
            urls.append(full)
    return urls[:8]

async def crawl_google_news():
    print("=" * 60)
    print("Crawling Google News for medical aesthetics...")
    print("=" * 60)
    async with AsyncWebCrawler() as crawler:
        url = "https://news.google.com/search?q=medical+aesthetics+2026&hl=en-US&gl=US&ceid=US:en"
        result = await crawler.arun(url=url)
        if not result.success:
            print(f"  Google News EN failed: {result.error_message}")
            return []
        articles = parse_google_news(result.html, "en")
        print(f"  Found {len(articles)} articles from Google News EN")
        return articles

async def crawl_google_news_cn():
    print("=" * 60)
    print("Crawling Google News for 医美...")
    print("=" * 60)
    async with AsyncWebCrawler() as crawler:
        url = "https://news.google.com/search?q=%E5%8C%BB%E7%BE%8E+2026&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
        result = await crawler.arun(url=url)
        if not result.success:
            print(f"  Google News CN failed: {result.error_message}")
            return []
        articles = parse_google_news(result.html, "zh")
        print(f"  Found {len(articles)} articles from Google News CN")
        return articles

def parse_google_news(html, lang):
    articles = []
    for m in re.finditer(
        r'<article[^>]*>(.*?)</article>', html, re.I | re.S
    ):
        block = m.group(1)
        title_m = re.search(r'<a[^>]*>(.*?)</a>', block, re.I | re.S)
        if not title_m:
            continue
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()
        link_m = re.search(r'href=["\'](\./articles/[^"\']+)["\']', block, re.I)
        if not link_m:
            continue
        link = "https://news.google.com" + link_m.group(1).lstrip(".")
        img_m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', block, re.I)
        img = ""
        if img_m:
            u = img_m.group(1)
            if not u.startswith("data:"):
                img = urljoin("https://news.google.com", u)
        source_m = re.search(r'<div[^>]*data-n-tag=["\'][^"\']*["\'][^>]*>(.*?)</div>', block, re.I | re.S)
        source = ""
        if source_m:
            source = re.sub(r'<[^>]+>', '', source_m.group(1)).strip()
        time_m = re.search(r'datetime=["\']([^"\']+)["\']', block, re.I)
        pub_time = time_m.group(1) if time_m else ""
        articles.append({
            "title": title,
            "url": link,
            "image": img,
            "source": source,
            "published": pub_time,
            "lang": lang,
        })
    return articles

async def crawl_article_detail(url):
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, word_count_threshold=10)
            if not result.success:
                return None, None
            text = (result.markdown or "")[:3000]
            images = extract_images(result.html, url)
            return text, images
    except Exception as e:
        print(f"  [WARN] Failed to crawl detail {url}: {e}")
        return None, None

async def crawl_36kr():
    print("=" * 60)
    print("Crawling 36Kr for 医美资讯...")
    print("=" * 60)
    articles = []
    for keyword in ["医美", "医疗美容"]:
        async with AsyncWebCrawler() as crawler:
            url = f"https://36kr.com/search/articles/{keyword}"
            result = await crawler.arun(url=url)
            if result.success:
                for m in re.finditer(
                    r'<a[^>]*class="article-item-title"[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                    result.html, re.I | re.S
                ):
                    link = m.group(1).strip()
                    if not link.startswith("http"):
                        link = "https://36kr.com" + link
                    title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                    articles.append({"title": title, "url": link, "source": "36氪", "lang": "zh"})
                    if len(articles) >= 10:
                        break
            if len(articles) >= 10:
                break
    print(f"  Found {len(articles)} articles from 36Kr")
    return articles

async def crawl_yicai():
    print("=" * 60)
    print("Crawling Yicai for 医美...")
    print("=" * 60)
    articles = []
    async with AsyncWebCrawler() as crawler:
        url = "https://www.yicai.com/search?keys=%E5%8C%BB%E7%BE%8E"
        result = await crawler.arun(url=url)
        if result.success:
            for m in re.finditer(
                r'<a[^>]*href=["\'](/news/\d+\.html)[^>]*>(.*?)</a>',
                result.html, re.I | re.S
            ):
                link = "https://www.yicai.com" + m.group(1).strip()
                title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if title:
                    articles.append({"title": title, "url": link, "source": "第一财经", "lang": "zh"})
                if len(articles) >= 8:
                    break
    print(f"  Found {len(articles)} articles from Yicai")
    return articles

async def crawl_elle_news():
    print("=" * 60)
    print("Crawling beauty/aesthetics news from general web...")
    print("=" * 60)
    articles = []
    async with AsyncWebCrawler() as crawler:
        url = "https://www.elle.com/beauty/"
        result = await crawler.arun(url=url)
        if result.success:
            for m in re.finditer(
                r'<a[^>]*href=["\']([^"\']+)"[^>]*>.*?<h[^>]*>(.*?)</h',
                result.html, re.I | re.S
            ):
                link = m.group(1).strip()
                if not link.startswith("http"):
                    link = "https://www.elle.com" + link
                title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if title:
                    articles.append({"title": title, "url": link, "source": "ELLE", "lang": "en"})
                if len(articles) >= 6:
                    break
    print(f"  Found {len(articles)} articles from ELLE Beauty")
    return articles

def deduplicate(articles):
    seen = set()
    result = []
    for a in articles:
        key = a["title"].lower().strip()[:50]
        if key not in seen:
            seen.add(key)
            result.append(a)
    return result

async def main():
    all_articles = []
    tasks = [
        crawl_google_news(),
        crawl_google_news_cn(),
        crawl_36kr(),
        crawl_yicai(),
        crawl_elle_news(),
    ]
    results = await asyncio.gather(*tasks)
    for r in results:
        all_articles.extend(r)
    
    all_articles = deduplicate(all_articles)
    print(f"\n{'=' * 60}")
    print(f"Total unique articles: {len(all_articles)}")
    print(f"{'=' * 60}\n")
    
    enriched = []
    for i, art in enumerate(all_articles[:20]):
        print(f"[{i+1}/{min(len(all_articles),20)}] Fetching: {art['title'][:60]}...")
        text, detail_images = await crawl_article_detail(art["url"])
        art["summary"] = (text or "")[:2000]
        art["detail_images"] = detail_images or []
        if "image" not in art:
            art["image"] = ""
        enriched.append(art)
    
    collected = {"crawl_time": datetime.now().isoformat(), "articles": enriched}
    json_path = OUTPUT_DIR / "articles.json"
    json_path.write_text(json.dumps(collected, ensure_ascii=False, indent=2))
    print(f"\nSaved article index to {json_path}")
    
    print(f"\n{'=' * 60}")
    print("Downloading images...")
    print(f"{'=' * 60}")
    image_map = {}
    for i, art in enumerate(enriched):
        imgs = []
        if art["image"]:
            path = download_image(art["image"], f"art{i}_main_")
            if path:
                imgs.append(path)
                print(f"  [{i+1}] Downloaded main image for: {art['title'][:50]}")
        for j, img_url in enumerate(art["detail_images"][:3]):
            if len(imgs) >= 2:
                break
            path = download_image(img_url, f"art{i}_d{j}_")
            if path:
                imgs.append(path)
        image_map[art["title"]] = imgs
    
    print(f"\n{'=' * 60}")
    print("Generating bilingual post...")
    print(f"{'=' * 60}")
    
    en_articles = [a for a in enriched if a["lang"] == "en"]
    cn_articles = [a for a in enriched if a["lang"] == "zh"]
    
    en_post = generate_en_post(en_articles, image_map)
    cn_post = generate_cn_post(cn_articles, image_map)
    
    post = {
        "date": "2026-05-31",
        "title_cn": "📋 今日医美资讯速览",
        "title_en": "📋 Today's Medical Aesthetics Roundup",
        "cn": cn_post,
        "en": en_post,
        "images": list(set(p for imgs in image_map.values() for p in imgs)),
    }
    
    post_path = OUTPUT_DIR / "post.json"
    post_path.write_text(json.dumps(post, ensure_ascii=False, indent=2))
    
    md_path = OUTPUT_DIR / "post.md"
    md = generate_markdown(post, image_map, enriched)
    md_path.write_text(md, encoding="utf-8")
    
    print(f"\n✅ Done! Output saved to:")
    print(f"  - {post_path}")
    print(f"  - {md_path}")
    print(f"  - Images: {IMAGES_DIR}")
    print(f"\nDownloaded {len(post['images'])} images total.")
    
    return post

def generate_en_post(articles, image_map):
    lines = []
    lines.append(f"🗓️ Medical Aesthetics News Roundup — May 31, 2026\n")
    for i, art in enumerate(articles[:8]):
        lines.append(f"#{i+1} {art['title']}")
        lines.append(f"   📰 {art.get('source', 'Source')}")
        imgs = image_map.get(art["title"], [])
        if imgs:
            lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art.get("summary"):
            s = art["summary"][:300].replace("\n", " ")
            lines.append(f"   💡 {s}")
        lines.append(f"   🔗 {art['url']}")
        lines.append("")
    lines.append("---")
    lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} via crawl4ai")
    return "\n".join(lines)

def generate_cn_post(articles, image_map):
    lines = []
    lines.append(f"🗓️ 今日医美资讯速览 — 2026年5月31日\n")
    for i, art in enumerate(articles[:8]):
        lines.append(f"#{i+1} {art['title']}")
        lines.append(f"   📰 来源：{art.get('source', '网络')}")
        imgs = image_map.get(art["title"], [])
        if imgs:
            lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art.get("summary"):
            s = art["summary"][:300].replace("\n", " ")
            lines.append(f"   💡 {s}")
        lines.append(f"   🔗 {art['url']}")
        lines.append("")
    lines.append("---")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 数据来源：crawl4ai 全网搜索")
    return "\n".join(lines)

def generate_markdown(post, image_map, enriched):
    lines = []
    lines.append("---")
    lines.append(f"title: '{post['title_cn']}'")
    lines.append(f"date: 2026-05-31")
    lines.append("---")
    lines.append("")
    lines.append(f"# {post['title_cn']}")
    lines.append("")
    lines.append("## 🇨🇳 中文版")
    lines.append("")
    lines.append(post["cn"].replace("\n", "\n\n"))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## 🇺🇸 English Version")
    lines.append("")
    lines.append(post["en"].replace("\n", "\n\n"))
    lines.append("")
    lines.append("## 🖼️ 配图 / Images")
    lines.append("")
    for art in enriched[:10]:
        imgs = image_map.get(art["title"], [])
        if imgs:
            lines.append(f"### {art['title']}")
            for img_path in imgs:
                rel = os.path.relpath(img_path, OUTPUT_DIR)
                lines.append(f"![{art['title']}]({rel})")
            lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    asyncio.run(main())
