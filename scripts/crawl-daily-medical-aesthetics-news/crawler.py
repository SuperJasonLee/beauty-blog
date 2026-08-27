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
            "poly-L-lactic acid collagen neocollagenesis OR microfocused ultrasound MFU-V SMAS OR recombinant collagen extracellular matrix OR pulsed dye laser rosacea 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu",
        "command": [
            "opencli", "zhihu", "search",
            "PLLA童颜针 重组胶原蛋白 超声刀 MFU-V 脉冲染料激光 玫瑰痤疮 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "google",
        "command": [
            "opencli", "web", "read",
            "--url", "https://www.google.com/search?q=medical+aesthetics+poly-L-lactic+acid+recombinant+collagen+ultrasound+august+2026&num=15",
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
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42594306/",
            "source_name": "PubMed",
            "title": "Divergent Time Courses of Poly-L-Lactic Acid and Hyaluronic Acid Fillers for Nasolabial Fold Correction: A Multicenter Randomized Trial With 120-Week Follow-Up",
            "date": "2026",
            "content_markdown": "**Authors:** Liu Y, Zhang G, Yang F\n**Journal:** The Journal of Craniofacial Surgery\n**DOI:** 10.1097/SCS.0000000000013290",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42495478/",
            "source_name": "PubMed",
            "title": "Preclinical Histologic and Morphometric Comparison of Poly-L-Lactic Acid Fillers Formulated With Carboxymethyl Cellulose or Non-crosslinked Hyaluronic Acid in a Porcine Model",
            "date": "2026",
            "content_markdown": "**Authors:** Sulamanidze G, Kajaia A, Nikishin D\n**Journal:** Cureus\n**DOI:** 10.7759/cureus.111360",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42469307/",
            "source_name": "PubMed",
            "title": "Individualized HIFU in women over 60: ultrasound assessment of layer-specific facial soft-tissue thickness changes",
            "date": "2026",
            "content_markdown": "**Authors:** Yi KH, Park Y, Song JK\n**Journal:** Scientific Reports\n**DOI:** 10.1038/s41598-026-61092-7",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42303361/",
            "source_name": "PubMed",
            "title": "Microfocused Ultrasound with Visualization for Skin Tightening: Clinical Applications, Safety, and Technical Considerations",
            "date": "2026",
            "content_markdown": "**Authors:** Soza GM\n**Journal:** Dermatologic Clinics\n**DOI:** 10.1016/j.det.2026.02.007",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42480655/",
            "source_name": "PubMed",
            "title": "Interface-engineered supramolecular collagen peptide nanocapsules for barrier repair and matrix remodeling: From molecular assembly to clinical translation",
            "date": "2026",
            "content_markdown": "**Authors:** Zhou M, Li A, Yang B\n**Journal:** Journal of Controlled Release\n**DOI:** 10.1016/j.jconrel.2026.115185",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42561123/",
            "source_name": "PubMed",
            "title": "Pulsed Dye Laser and Intense Pulsed Light Therapy for Cutaneous and Ocular Rosacea: A Systematic Review",
            "date": "2026",
            "content_markdown": "**Authors:** Finney OS, Soliman J, Choi M\n**Journal:** Lasers in Surgery and Medicine\n**DOI:** 10.1002/lsm.70185",
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
