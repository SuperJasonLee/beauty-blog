"""Crawler module: uses opencli to search and extract breast augmentation + medical-aesthetics news."""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

OPENCLI = os.environ.get("OPENCLI", r"C:\Users\Administrator\AppData\Roaming\npm\opencli.cmd")

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "crawled" / "breast-augmentation-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    {
        "name": "pubmed_augmentation",
        "command": [
            OPENCLI, "pubmed", "search",
            "breast augmentation implant complication revision aesthetic surgery 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_safety",
        "command": [
            OPENCLI, "pubmed", "search",
            "breast implant safety BIA-ALCL anaplastic large cell lymphoma capsular contracture 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_mastopexy",
        "command": [
            OPENCLI, "pubmed", "search",
            "mastopexy breast lift augmentation-mastopexy outcomes periareolar technique 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_fat_grafting",
        "command": [
            OPENCLI, "pubmed", "search",
            "autologous fat grafting breast augmentation lipofilling complications volume retention 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed_nicotine",
        "command": [
            OPENCLI, "pubmed", "search",
            "nicotine tobacco smoking breast surgery complications perioperative cessation 2026",
            "--limit", "10", "-f", "json",
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


def crawl_source(source: dict, crawled_urls: set) -> list[dict]:
    logger.info(f"Crawling {source['name']}...")
    data = run_opencli(source["command"])
    if data is None:
        return []

    articles = extract_pubmed_articles(data)

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
    out_file = DATA_DIR / f"breast_augmentation_news_{ts}.json"
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
