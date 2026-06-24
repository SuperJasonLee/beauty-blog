"""Crawler module: uses opencli to search and extract rhinoplasty / nasal surgery news."""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "rhinoplasty-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    {
        "name": "pubmed",
        "command": ["opencli", "pubmed", "search", "rhinoplasty OR nasal surgery OR nose augmentation OR nasal reconstruction 2026", "--limit", "10", "-f", "json"],
    },
    {
        "name": "zhihu",
        "command": ["opencli", "zhihu", "search", "鼻部整形 隆鼻 2026", "--limit", "10", "-f", "json"],
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def load_crawled_urls() -> set:
    if DEDUP_FILE.exists():
        return set(json.loads(DEDUP_FILE.read_text(encoding="utf-8")))
    return set()


def save_crawled_urls(urls: set):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DEDUP_FILE.write_text(json.dumps(sorted(urls), ensure_ascii=False, indent=2), encoding="utf-8")


def run_opencli(cmd: list[str], timeout: int = 60) -> Optional[dict]:
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=timeout, shell=True)
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        if result.returncode != 0:
            logger.warning(f"opencli returned non-zero: {stderr[:200]}")
            return None
        return json.loads(stdout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout running: {' '.join(cmd)}")
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON from: {' '.join(cmd)}")
    except Exception as e:
        logger.warning(f"Error running opencli: {e}")
    return None


def extract_pubmed_articles(data: list[dict]) -> list[dict]:
    articles = []
    for item in data:
        articles.append({
            "source_url": item.get("url", ""),
            "source_name": "PubMed",
            "title": item.get("title", ""),
            "date": item.get("year", ""),
            "content_markdown": f"**Authors:** {item.get('authors', '')}\n**Journal:** {item.get('journal', '')}\n**DOI:** {item.get('doi', '')}",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def extract_zhihu_articles(data: list[dict]) -> list[dict]:
    articles = []
    for item in data:
        articles.append({
            "source_url": item.get("url", ""),
            "source_name": "知乎",
            "title": item.get("title", ""),
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "content_markdown": f"**Author:** {item.get('author', '')}\n**Votes:** {item.get('votes', 0)}",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def crawl_source(source: dict, crawled_urls: set) -> list[dict]:
    logger.info(f"Crawling {source['name']}...")
    data = run_opencli(source["command"])
    if data is None:
        return []

    if source["name"] == "pubmed":
        articles = extract_pubmed_articles(data)
    elif source["name"] == "zhihu":
        articles = extract_zhihu_articles(data)
    else:
        return []

    new_articles = []
    for a in articles:
        url = a["source_url"]
        if url in crawled_urls:
            logger.info(f"Skipping duplicate: {url}")
            continue
        crawled_urls.add(url)
        new_articles.append(a)

    logger.info(f"  {source['name']}: {len(new_articles)} new articles")
    return new_articles


def crawl_all() -> list[dict]:
    crawled_urls = load_crawled_urls()
    all_articles = []

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
    out_file = DATA_DIR / f"rhinoplasty_news_{ts}.json"
    out_file.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
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
