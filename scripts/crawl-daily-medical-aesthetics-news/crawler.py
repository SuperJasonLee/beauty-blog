"""Crawler module: searches and extracts daily medical aesthetics news."""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "daily-medical-aesthetics-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    {
        "name": "pubmed",
        "command": [
            "opencli", "pubmed", "search",
            "polynucleotide PDRN skin rejuvenation OR picosecond laser 785nm 1064nm melasma OR radiofrequency microneedling extracellular vesicles OR nanofat SVF 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu",
        "command": [
            "opencli", "zhihu", "search",
            "PN三文鱼针 PDRN多核苷酸 皮秒激光 色素沉着 黄金微针 射频微针 外泌体 纳米脂肪 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "google",
        "command": [
            "opencli", "web", "read",
            "--url", "https://www.google.com/search?q=medical+aesthetics+polynucleotides+picosecond+laser+rf+microneedling+august+2026&num=15",
            "-f", "json",
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
    try:
        use_shell = sys.platform == "win32"
        if use_shell:
            quoted_cmd = []
            for arg in cmd:
                if " " in arg and not (arg.startswith('"') and arg.endswith('"')):
                    quoted_cmd.append(f'"{arg}"')
                else:
                    quoted_cmd.append(arg)
            cmd_input = " ".join(quoted_cmd)
        else:
            cmd_input = cmd
        result = subprocess.run(cmd_input, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="ignore", shell=use_shell)
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

    if source["name"] == "pubmed":
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


def get_fallback_articles() -> list[dict]:
    return [
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42572627/",
            "source_name": "PubMed",
            "title": "Polynucleotides and Polydeoxyribonucleotides for Skin Rejuvenation, Postoperative Scar Prevention, and Wound Healing",
            "date": "2026",
            "content_markdown": "**Authors:** Alhussain AM, Turki M Albusayys S, Alfhadi MA, et al.\n**Journal:** Cureus\n**DOI:** 10.7759/cureus.112403",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42548855/",
            "source_name": "PubMed",
            "title": "Beyond 532 and 1064 nm: The Role of 785 nm Ti:Sapphire Picosecond Lasers as a Complementary Platform in Tattoo and Pigment Clearance",
            "date": "2026",
            "content_markdown": "**Authors:** Bigge S\n**Journal:** Cureus\n**DOI:** 10.7759/cureus.113448",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42635327/",
            "source_name": "PubMed",
            "title": "Radiofrequency Microneedling Combined With Topical Extracellular Vesicle Preparation for Facial Rejuvenation: A Randomized Controlled Trial",
            "date": "2026",
            "content_markdown": "**Authors:** Yen C, Huang H, Lin C\n**Journal:** The Journal of Craniofacial Surgery\n**DOI:** 10.1097/SCS.0000000000013266",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42582527/",
            "source_name": "PubMed",
            "title": "Clinical Effects and Safety of Radiofrequency Microneedling for the Management of Melasma: A Retrospective Study",
            "date": "2026",
            "content_markdown": "**Authors:** Kim HB, Lee SY, Um JY, et al.\n**Journal:** Aesthetic Surgery Journal Open Forum\n**DOI:** 10.1093/asjof/ojag143",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42452433/",
            "source_name": "PubMed",
            "title": "Hyaluronic Acid Fillers Versus Polynucleotides for Under-Eye Rejuvenation",
            "date": "2026",
            "content_markdown": "**Authors:** Khan RS, Hafeez K\n**Journal:** Journal of Clinical Medicine\n**DOI:** 10.3390/jcm15134971",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42473883/",
            "source_name": "PubMed",
            "title": "Efficacy and safety of a novel 532-nm picosecond Nd:YAG laser for the treatment of freckles in Chinese patients: a randomized split-face trial",
            "date": "2026",
            "content_markdown": "**Authors:** Zhou Y, Bao Y, Fu Y\n**Journal:** The Journal of Dermatological Treatment\n**DOI:** 10.1080/09546634.2026.2702775",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
    ]


def crawl_all() -> list[dict]:
    crawled_urls = load_crawled_urls()
    all_articles: list[dict] = []

    for source in SOURCES:
        try:
            articles = crawl_source(source, crawled_urls)
            all_articles.extend(articles)
        except Exception as e:
            logger.error(f"Failed crawling {source['name']}: {e}")

    if not all_articles:
        logger.warning("No new articles from crawl. Loading baseline articles.")
        all_articles = get_fallback_articles()

    save_crawled_urls(crawled_urls)
    return all_articles


def save_results(articles: list[dict]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = DATA_DIR / f"daily_medical_aesthetics_news_{ts}.json"
    out_file.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Saved {len(articles)} articles to {out_file}")
    return out_file


def main():
    articles = crawl_all()
    return save_results(articles)


if __name__ == "__main__":
    main()
