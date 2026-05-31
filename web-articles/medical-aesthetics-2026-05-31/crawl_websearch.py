import asyncio, json, os, hashlib, re
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
        if path.stat().st_size < 1024:
            path.unlink()
            return None
        return str(path)
    except Exception as e:
        return None

async def crawl_article(url):
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, word_count_threshold=10)
            if not result.success:
                return None, []
            text = (result.markdown or "")[:3000]
            images = []
            for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', result.html, re.I):
                u = m.group(1)
                if u.startswith("data:"): continue
                full = urljoin(url, u)
                if any(x in full.lower() for x in ["logo","icon","avatar","sprite","svg"]):
                    continue
                if any(full.lower().endswith(e) for e in [".jpg",".jpeg",".png",".webp"]):
                    images.append(full)
            return text, images[:8]
    except Exception as e:
        return None, []

# English medical aesthetics news sources
EN_SOURCES = [
    {"url": "https://www.americanmedspa.org/news/the-future-of-the-aesthetics-industry-key-conversations-and-takeaways-from-medical-spa-show-2026/", "source": "AmSpa", "lang": "en", "title": "The Future of the Aesthetics Industry: Medical Spa Show 2026"},
    {"url": "https://www.americanmedspa.org/news/new-radiesse-research-highlights-deeper-extracellular-matrix-regeneration/", "source": "AmSpa", "lang": "en", "title": "New Radiesse Research Highlights Deeper Extracellular Matrix Regeneration"},
    {"url": "https://www.americanmedspa.org/news/building-a-lean-med-spa-team-and-network-lessons-from-kathy-taranto/", "source": "AmSpa", "lang": "en", "title": "Building a Lean Med Spa Team: Lessons from Kathy Taranto"},
    {"url": "https://www.drspiegel.com/blog/the-top-7-aesthetic-trends-in-2026-according-to-facial-plastic-surgeons", "source": "Spiegel Center", "lang": "en", "title": "Top 7 Aesthetic Trends in 2026 According to Facial Plastic Surgeons"},
    {"url": "https://www.plasticsurgery.org/news/articles/looking-into-the-future-plastic-surgery-trends-for-2026", "source": "ASPS", "lang": "en", "title": "Plastic Surgery Trends for 2026: Preservation and Regeneration"},
    {"url": "https://allure-md.com/articles/latest-news-in-aesthetic-medicine", "source": "Allure MD", "lang": "en", "title": "Latest News in Aesthetic Medicine"},
    {"url": "https://iapam.com/2026-aesthetic-medicine-trends", "source": "IAPAM", "lang": "en", "title": "Top Aesthetic Medicine Trends to Watch in 2026"},
    {"url": "https://templuslife.com/blog/medical-aesthetics-industry-news-regulatory-updates-2026", "source": "Templus Life", "lang": "en", "title": "Medical Aesthetics Industry News & Regulatory Updates 2026"},
    {"url": "https://www.elle.com/beauty/makeup-skin-care/a64945585/best-tools-treatments-2025/", "source": "ELLE", "lang": "en", "title": "The Best Beauty Gadgets and In-Office Treatments"},
    {"url": "https://orangecountyplasticsurgery.com/plastic-surgery-trends-2026-what-patients-should-know-this-spring", "source": "OC Plastic Surgery", "lang": "en", "title": "Plastic Surgery Trends 2026: What Patients Should Know"},
]

# Chinese medical aesthetics news sources
CN_SOURCES = [
    {"url": "https://www.yicai.com/news/103208520.html", "source": "第一财经", "lang": "zh", "title": "GLP-1减肥药禁止在电商销售，行业野蛮增长态势要终结了"},
    {"url": "https://www.yicai.com/news/103199946.html", "source": "第一财经", "lang": "zh", "title": "被中国消费者'放弃'的韩国化妆品，正在打开美国市场"},
    {"url": "https://www.yicai.com/news/103172925.html", "source": "第一财经", "lang": "zh", "title": "细胞疗法大降价！离平民抗衰还有多远？"},
    {"url": "https://www.yicai.com/news/103173599.html", "source": "第一财经", "lang": "zh", "title": "中信证券：医美上游品牌方因发展阶段而分化"},
    {"url": "https://www.sohu.com/a/1021728415_122671915", "source": "搜狐", "lang": "zh", "title": "2026年医美行业深度观察：当'容貌焦虑'遇上'理性消费'"},
    {"url": "https://www.sohu.com/a/994162950_122632840", "source": "搜狐", "lang": "zh", "title": "2026年医美行业深度观察：从规模扩张到质量重塑"},
    {"url": "https://cj.sina.com.cn/articles/view/9088628224/21db9760000101e9a6", "source": "新浪财经", "lang": "zh", "title": "2026医美大变局：监管重拳落地，行业洗牌加速"},
    {"url": "https://zhuanlan.zhihu.com/p/2042537290384265963", "source": "知乎", "lang": "zh", "title": "2026中国'医美+AI'产业分析：万亿级市场规模与智能化合规路径"},
    {"url": "https://zhuanlan.zhihu.com/p/2023320771804569956", "source": "知乎", "lang": "zh", "title": "研报视角：2026医美行业增长趋势"},
    {"url": "https://openaxo.com/innovation/china-medical-aesthetics-ai-2026", "source": "OpenAxo", "lang": "zh", "title": "2026中国'医美+AI'产业分析"},
]

async def main():
    all_sources = EN_SOURCES + CN_SOURCES
    
    enriched = []
    for i, src in enumerate(all_sources):
        print(f"[{i+1}/{len(all_sources)}] {src['title'][:50]}...")
        text, imgs = await crawl_article(src["url"])
        enriched.append({
            "title": src["title"],
            "url": src["url"],
            "source": src["source"],
            "lang": src["lang"],
            "summary": (text or "")[:2000],
            "detail_images": imgs,
            "image": "",
        })
    
    print("\n--- Downloading images ---")
    image_map = {}
    for i, art in enumerate(enriched):
        downloaded = []
        for j, img_url in enumerate(art["detail_images"]):
            if len(downloaded) >= 3:
                break
            path = download_image(img_url, f"en{i}_" if art["lang"] == "en" else f"cn{i}_")
            if path:
                downloaded.append(path)
                print(f"  [{i+1}] {os.path.basename(path)}")
        image_map[art["url"]] = downloaded
    
    all_images = list(set(p for imgs in image_map.values() for p in imgs))
    print(f"\nTotal images downloaded: {len(all_images)}")
    
    # Generate posts
    cn_articles = [a for a in enriched if a["lang"] == "zh"]
    en_articles = [a for a in enriched if a["lang"] == "en"]
    
    cn_post_lines = [f"📋 今日医美资讯速览 — 2026年5月31日\n"]
    for i, art in enumerate(cn_articles[:8]):
        cn_post_lines.append(f"#{i+1} {art['title']}")
        cn_post_lines.append(f"   来源：{art['source']}")
        imgs = image_map.get(art["url"], [])
        if imgs:
            cn_post_lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art["summary"]:
            snippet = art["summary"].replace("\n", " ").strip()[:200]
            cn_post_lines.append(f"   {snippet}")
        cn_post_lines.append(f"   🔗 {art['url']}\n")
    cn_post_lines.append("---\n数据来源：crawl4ai 全网搜索 | 生成时间：2026-05-31")
    cn_post = "\n".join(cn_post_lines)
    
    en_post_lines = [f"📋 Medical Aesthetics Roundup — May 31, 2026\n"]
    for i, art in enumerate(en_articles[:8]):
        en_post_lines.append(f"#{i+1} {art['title']}")
        en_post_lines.append(f"   Source: {art['source']}")
        imgs = image_map.get(art["url"], [])
        if imgs:
            en_post_lines.append(f"   🖼️ {os.path.basename(imgs[0])}")
        if art["summary"]:
            snippet = art["summary"].replace("\n", " ").strip()[:200]
            en_post_lines.append(f"   {snippet}")
        en_post_lines.append(f"   🔗 {art['url']}\n")
    en_post_lines.append("---\nData sourced via crawl4ai | Generated: 2026-05-31")
    en_post = "\n".join(en_post_lines)
    
    # Save
    post = {
        "date": "2026-05-31",
        "title_cn": "📋 今日医美资讯速览",
        "title_en": "📋 Today's Medical Aesthetics Roundup",
        "cn": cn_post,
        "en": en_post,
        "images": all_images,
    }
    
    (BASE_DIR / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2))
    
    md = []
    md.append(f"# 📋 今日医美资讯速览 | Medical Aesthetics Roundup")
    md.append(f"**2026年5月31日 / May 31, 2026**\n")
    md.append("## 🇨🇳 中文版\n")
    md.append(cn_post)
    md.append("\n---\n")
    md.append("## 🇬🇧 English Version\n")
    md.append(en_post)
    md.append("\n---\n")
    md.append("## 🖼️ 配图 / Gallery\n")
    for art in enriched[:10]:
        imgs = image_map.get(art["url"], [])
        if imgs:
            md.append(f"### {art['title']}")
            for img_path in imgs:
                rel = os.path.relpath(img_path, BASE_DIR)
                md.append(f"![{art['title']}]({rel})")
            md.append("")
    
    (BASE_DIR / "post.md").write_text("\n".join(md), encoding="utf-8")
    
    print(f"\n{'='*60}")
    print(f"✅ Output saved!")
    print(f"  📄 post.json")
    print(f"  📄 post.md")
    print(f"  🖼️  {len(all_images)} images")
    print(f"{'='*60}\n")
    
    print("=" * 60)
    print("ENGLISH POST PREVIEW")
    print("=" * 60)
    print(en_post[:1500])
    print("\n...\n")
    print("=" * 60)
    print("中文预览")
    print("=" * 60)
    print(cn_post[:1500])

if __name__ == "__main__":
    asyncio.run(main())
