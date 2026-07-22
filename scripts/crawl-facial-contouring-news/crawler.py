"""Crawler module: uses opencli (via powershell & call-operator) to search and extract
facial contouring & slimming news from PubMed, Zhihu, and Google."""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "facial-contouring-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

OPENCLI_PS1 = r"C:\Users\Administrator\AppData\Roaming\npm\opencli.ps1"


def _opencli_cmd(*args: str) -> list[str]:
    """Build a subprocess command list that invokes opencli via PowerShell call-operator.
    Each arg is shell-quoted individually to survive PowerShell whitespace splitting.
    """
    import shlex
    quoted = [shlex.quote(a) for a in args]
    return [
        "powershell", "-NoProfile", "-Command",
        f"& '{OPENCLI_PS1}' " + " ".join(quoted),
    ]


SOURCES = [
    {
        "name": "pubmed",
        "command": _opencli_cmd(
            "pubmed", "search",
            "facial contouring OR mandible angle reduction OR buccal fat removal OR masseter botox 2026",
            "--limit", "10", "-f", "json",
        ),
    },
    {
        "name": "pubmed2",
        "command": _opencli_cmd(
            "pubmed", "search",
            "radiofrequency facial tightening OR thread lift OR rhinoplasty aesthetic 2026",
            "--limit", "10", "-f", "json",
        ),
    },
    {
        "name": "zhihu",
        "command": _opencli_cmd(
            "zhihu", "search",
            "面部轮廓整形 瘦脸 下颌角 颧骨 医美 2026",
            "--limit", "10", "-f", "json",
        ),
    },
    {
        "name": "zhihu2",
        "command": _opencli_cmd(
            "zhihu", "search",
            "咬肌注射 玻尿酸填充 线雕提升 面部吸脂 唇部填充 2026",
            "--limit", "10", "-f", "json",
        ),
    },
    {
        "name": "google",
        "command": _opencli_cmd(
            "web", "read",
            "--url", "https://www.google.com/search?q=facial+contouring+aesthetic+surgery+trends+2026&num=15",
            "-f", "json",
        ),
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
    DEDUP_FILE.write_text(json.dumps(sorted(urls), ensure_ascii=False, indent=2), encoding="utf-8")


def run_opencli(cmd: list[str], timeout: int = 60) -> Optional[object]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        if result.returncode not in (0, 1):
            logger.warning(f"opencli returned non-zero ({result.returncode}): {result.stderr[:300]}")
            return None
        if not result.stdout.strip():
            logger.warning(f"opencli returned empty stdout")
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout running: {' '.join(cmd)}")
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON ({e}): {result.stdout[:200] if 'result' in dir() else 'N/A'}")
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
            saved = item.get("saved", "")
            articles.append({
                "source_url": item.get("url") or saved,
                "source_name": "Google",
                "title": item.get("title", ""),
                "date": item.get("publish_time", "") or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "content_markdown": (
                    f"**Author:** {item.get('author', '-')}\n"
                    f"**Publish time:** {item.get('publish_time', '-')}\n"
                    f"**Saved file:** {saved}\n"
                    f"**Status:** {item.get('status', '-')}\n"
                    f"**Size:** {item.get('size', '-')}"
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
    elif source["name"] in ("zhihu", "zhihu2"):
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
    out_file = DATA_DIR / f"facial_contouring_news_{ts}.json"
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
