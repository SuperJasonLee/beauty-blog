"""Crawler module: uses opencli to search and extract plastic surgery subspecialties news.

Subspecialties covered: 眼部 / 鼻部 / 唇部 / 隆胸 / 减肥 / 瘦脸 / 私密部位 / 畸形矫正
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

OPENCLI = os.environ.get("OPENCLI", r"C:\Users\Administrator\AppData\Roaming\npm\opencli.cmd")

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "plastic-surgery-subfields-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    # ── 眼部 ──────────────────────────────────────────────────────────────────
    {
        "name": "pubmed_blepharoplasty",
        "command": [
            OPENCLI, "pubmed", "search",
            "blepharoplasty double eyelid surgery upper lower aesthetic outcomes complication 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_blepharoplasty_aging",
        "command": [
            OPENCLI, "pubmed", "search",
            "periorbital aging rejuvenation blepharoplasty fat repositioning ptosis correction 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 鼻部 ──────────────────────────────────────────────────────────────────
    {
        "name": "pubmed_rhinoplasty",
        "command": [
            OPENCLI, "pubmed", "search",
            "rhinoplasty nasal aesthetic open closed technique complication revision 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_rhinoplasty_complication",
        "command": [
            OPENCLI, "pubmed", "search",
            "rhinoplasty septal perforation collapse asymmetry cartilage graft tip projection 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 唇部 ──────────────────────────────────────────────────────────────────
    {
        "name": "pubmed_lip_augmentation",
        "command": [
            OPENCLI, "pubmed", "search",
            "lip augmentation filler injection HA collagen fat transfer aesthetic outcome 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_lip_correction",
        "command": [
            OPENCLI, "pubmed", "search",
            "lip asymmetry correction vermilion advancement technique facial aesthetics 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 隆胸 ──────────────────────────────────────────────────────────────────
    {
        "name": "pubmed_breast_augmentation",
        "command": [
            OPENCLI, "pubmed", "search",
            "breast augmentation implant complication revision aesthetic surgery 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_breast_safety",
        "command": [
            OPENCLI, "pubmed", "search",
            "breast implant safety BIA-ALCL anaplastic large cell lymphoma capsular contracture 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 减肥 / 体重管理 ─────────────────────────────────────────────────────────
    {
        "name": "pubmed_cryolipolysis",
        "command": [
            OPENCLI, "pubmed", "search",
            "cryolipolysis coolsculpting body contouring fat reduction non-invasive lipolysis 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_liposuction",
        "command": [
            OPENCLI, "pubmed", "search",
            "liposuction body contouring tumescent technique complication skin retraction 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 瘦脸 / 面部轮廓 ─────────────────────────────────────────────────────────
    {
        "name": "pubmed_masseter_botox",
        "command": [
            OPENCLI, "pubmed", "search",
            "masseter botulinum toxin injection facial contouring slim face aesthetic 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_mandible_angle",
        "command": [
            OPENCLI, "pubmed", "search",
            "mandible angle osteotomy facial contouring malarplasty Asian aesthetic surgery 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 私密部位 ───────────────────────────────────────────────────────────────
    {
        "name": "pubmed_intimate_aesthetics",
        "command": [
            OPENCLI, "pubmed", "search",
            "labiaplasty vaginoplasty intimate aesthetic surgery patient satisfaction outcome 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_intimate_safety",
        "command": [
            OPENCLI, "pubmed", "search",
            "intimate aesthetic surgery complication nerve injury sensation sexual function 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 畸形矫正 ───────────────────────────────────────────────────────────────
    {
        "name": "pubmed_craniofacial",
        "command": [
            OPENCLI, "pubmed", "search",
            "craniofacial reconstruction cleft lip palate deformity correction aesthetic 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_reconstructive",
        "command": [
            OPENCLI, "pubmed", "search",
            "reconstructive plastic surgery microsurgery flap reconstruction deformity congenital 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── 中文社区 ───────────────────────────────────────────────────────────────
    {
        "name": "zhihu_subspecialties",
        "command": [
            OPENCLI, "zhihu", "search",
            "整形 医美 八大 细分 眼综合 鼻综合 唇部 隆胸 减肥 瘦脸 私密 畸形矫正 2026",
            "--limit", "15", "-f", "json",
        ],
    },
    {
        "name": "zhihu_blepharoplasty_zh",
        "command": [
            OPENCLI, "zhihu", "search",
            "双眼皮手术 开眼角 眼部整形 失败 修复 恢复 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu_rhinoplasty_zh",
        "command": [
            OPENCLI, "zhihu", "search",
            "隆鼻 鼻综合 鼻修复 耳软骨 肋软骨 假体 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu_lip_zh",
        "command": [
            OPENCLI, "zhihu", "search",
            "唇部整形 唇珠 玻尿酸 嘟嘟唇 唇形 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    # ── Google 新闻 ────────────────────────────────────────────────────────────
    {
        "name": "google_plastic_surgery_trends",
        "command": [
            OPENCLI, "web", "read",
            "--url", "https://www.google.com/search?q=plastic+surgery+trends+2026+FDA+ASPS+news&num=10",
            "-f", "json",
        ],
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def load_crawled_urls() -> set:
    if DEDUP_FILE.exists():
        return set(json.loads(DEDUP_FILE.read_text()))
    return set()


def save_crawled_urls(urls: set):
    DEDUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEDUP_FILE.write_text(json.dumps(sorted(urls), ensure_ascii=False, indent=2))


def run_opencli(cmd: list[str], timeout: int = 60) -> Optional[object]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            logger.warning(f"opencli returned non-zero: {result.stderr[:200]}")
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout running: {' '.join(cmd)}")
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON from: {' '.join(cmd)}")
    except Exception as e:
        logger.warning(f"Error running opencli: {e}")
    return None


def extract_pubmed_articles(data) -> list[dict]:
    articles = []
    for item in data or []:
        articles.append({
            "source_url": item.get("url", ""),
            "source_name": "PubMed",
            "title": item.get("title", ""),
            "date": item.get("year", ""),
            "content_markdown": (
                f"**Authors:** {item.get('authors', '')}\n"
                f"**Journal:** {item.get('journal', '')}\n"
                f"**Article type:** {item.get('article_type', '')}\n"
                f"**DOI:** {item.get('doi', '')}"
            ),
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def extract_web_articles(data) -> list[dict]:
    articles = []
    for item in data or []:
        title = item.get("title", "") or item.get("headline", "")
        url = item.get("url", "") or item.get("link", "")
        if not title or not url:
            continue
        articles.append({
            "source_url": url,
            "source_name": item.get("source", "Google Search"),
            "title": title,
            "date": item.get("date", "") or item.get("published", ""),
            "content_markdown": item.get("snippet", "") or item.get("description", ""),
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def crawl_source(source: dict, crawled_urls: set) -> list[dict]:
    logger.info(f"Crawling {source['name']}...")
    data = run_opencli(source["command"])
    if data is None:
        return []

    if "pubmed" in source["name"]:
        articles = extract_pubmed_articles(data)
    else:
        articles = extract_web_articles(data)

    new_articles = []
    for a in articles:
        url = a["source_url"]
        if not url:
            continue
        if url in crawled_urls:
            logger.info(f"Skipping duplicate: {url}")
            continue
        crawled_urls.add(url)
        new_articles.append(a)

    logger.info(f"  {source['name']}: {len(new_articles)} new articles")
    return new_articles


def crawl_all() -> list[dict]:
    crawled_urls = load_crawled_urls()
    all_articles: list[dict] = []

    for source in SOURCES:
        try:
            articles = crawl_source(source, crawled_urls)
            all_articles.extend(articles)
        except Exception as e:
            logger.error(f"Failed crawling {source['name']}: {e}")

    save_crawled_urls(crawled_urls)
    return all_articles


def save_results(articles: list[dict]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = DATA_DIR / f"plastic_surgery_subfields_news_{ts}.json"
    out_file.write_text(json.dumps(articles, ensure_ascii=False, indent=2))
    logger.info(f"Saved {len(articles)} articles to {out_file}")
    return out_file


def main():
    articles = crawl_all()
    if not articles:
        logger.warning("No articles crawled. Check opencli connectivity.")
        return None
    return save_results(articles)


if __name__ == "__main__":
    main()
