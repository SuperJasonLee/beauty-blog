"""Crawler module: uses opencli to search and extract eye-surgery + upper-face aesthetics news."""

import json
import logging
import os
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure npm bin directory is on PATH so opencli.cmd is discoverable on Windows
_NPM_BIN = Path(os.environ.get("APPDATA", "")) / "npm"
if _NPM_BIN.exists() and str(_NPM_BIN) not in os.environ.get("PATH", ""):
    os.environ["PATH"] = str(_NPM_BIN) + os.pathsep + os.environ.get("PATH", "")

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "crawled" / "eye-surgery-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    {
        "name": "pubmed",
        "command": [
            "opencli", "pubmed", "search",
            "blepharoplasty OR double eyelid surgery OR upper eyelid aesthetics OR brow lift 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "pubmed2",
        "command": [
            "opencli", "pubmed", "search",
            "Botox eyelid OR dermal filler tear trough OR upper face rejuvenation injection 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu",
        "command": [
            "opencli", "zhihu", "search",
            "双眼皮 开眼角 祛眼袋 眼部整形 医美 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "google",
        "command": [
            "opencli", "google", "search",
            "blepharoplasty double eyelid surgery eye plastic surgery trends 2026",
            "--limit", "10", "-f", "json",
        ],
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def load_crawled_urls() -> set:
    if DEDUP_FILE.exists():
        return set(json.loads(DEDUP_FILE.read_text(encoding="utf-8")))
    return set()


def save_crawled_urls(urls: set):
    DEDUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEDUP_FILE.write_text(json.dumps(sorted(urls), ensure_ascii=False, indent=2), encoding="utf-8")


def run_opencli(cmd: list[str], timeout: int = 60) -> Optional[object]:
    # On Windows opencli is a .cmd shim — call opencli.cmd directly to avoid shell=True issues
    exe = "opencli.cmd" if sys.platform == "win32" else cmd[0]
    full_cmd = [exe] + cmd[1:]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            logger.warning(f"opencli returned non-zero ({result.returncode}): {result.stderr[:300]}")
            return None
        if not result.stdout or not result.stdout.strip():
            logger.warning(f"opencli returned empty stdout for: {' '.join(full_cmd)}")
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout running: {' '.join(full_cmd)}")
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON from {' '.join(full_cmd)}: {e} — stdout[:200]: {result.stdout[:200] if 'result' in dir() else 'N/A'}")
    except Exception as e:
        logger.warning(f"Error running {' '.join(full_cmd)}: {e}")
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


def extract_zhihu_articles(data) -> list[dict]:
    articles = []
    for item in data or []:
        articles.append({
            "source_url": item.get("url", ""),
            "source_name": "知乎",
            "title": item.get("title", ""),
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "content_markdown": (
                f"**Author:** {item.get('author', '')}\n"
                f"**Type:** {item.get('type', '')}\n"
                f"**Votes:** {item.get('votes', 0)}"
            ),
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def extract_google_articles(data) -> list[dict]:
    articles = []
    if isinstance(data, list):
        for item in data:
            articles.append({
                "source_url": item.get("url") or item.get("saved", ""),
                "source_name": "Google",
                "title": item.get("title", ""),
                "date": date.today().isoformat(),
                "content_markdown": (
                    f"**Snippet:** {item.get('snippet', '-')}\n"
                    f"**Source:** {item.get('url', '-')}"
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

    if source["name"] in ("pubmed", "pubmed2"):
        articles = extract_pubmed_articles(data)
    elif source["name"] == "zhihu":
        articles = extract_zhihu_articles(data)
    elif source["name"] == "google":
        articles = extract_google_articles(data)
    else:
        return []

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
    out_file = DATA_DIR / f"eye_surgery_aesthetics_news_{ts}.json"
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
