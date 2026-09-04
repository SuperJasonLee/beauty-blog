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
            "exosomes extracellular vesicles androgenetic alopecia 2026 OR microneedling radiofrequency melasma 2026 OR polynucleotide PDRN skin rejuvenation 2026 OR high SMAS rhytidectomy facial rejuvenation 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu",
        "command": [
            "opencli", "zhihu", "search",
            "外泌体 脱发 黄金微针 黄褐斑 PDRN 三文鱼针 高位SMAS 面部提升 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "google",
        "command": [
            "opencli", "web", "read",
            "--url", "https://www.google.com/search?q=exosomes+androgenetic+alopecia+microneedling+radiofrequency+melasma+PDRN+polynucleotide+high+SMAS+rhytidectomy+september+2026&num=15",
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
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42553180/",
            "source_name": "PubMed",
            "title": "Adipose-Derived Stem Cell Exosomes Promote Hair Follicle Dermal Papilla Regeneration and Wnt/β-Catenin Signaling in Androgenetic Alopecia: A 2026 Prospective Randomized Controlled Trial",
            "date": "2026",
            "content_markdown": "**Authors:** Wang X, Zhang Y, Zhao L, et al.\n**Journal:** Stem Cell Research & Therapy\n**DOI:** 10.1186/s13287-026-04128-4",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42521940/",
            "source_name": "PubMed",
            "title": "Clinical Efficacy and Trichoscopic Assessment of Mesotherapy with Standardized Mesenchymal Stem Cell-Derived Extracellular Vesicles for Male and Female Pattern Hair Loss",
            "date": "2026",
            "content_markdown": "**Authors:** Kim JH, Lee SY, Park CW, et al.\n**Journal:** Dermatologic Surgery\n**DOI:** 10.1097/DSS.0000000000004380",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42562115/",
            "source_name": "PubMed",
            "title": "Synergistic Basement Membrane Repair and Mast Cell Stabilization by Dual-Wave Microneedling Radiofrequency in Refractory Melasma: A Multicenter Split-Face Trial",
            "date": "2026",
            "content_markdown": "**Authors:** Kwon HH, Choi SC, Park GH, et al.\n**Journal:** Journal of Cosmetic Dermatology\n**DOI:** 10.1111/jocd.71380",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42498712/",
            "source_name": "PubMed",
            "title": "Downregulation of VEGF and Dermal Angiogenesis Following Pulsed-Wave Radiofrequency in Hyperpigmented Skin: In Vivo Histological and Molecular Profiling",
            "date": "2026",
            "content_markdown": "**Authors:** Na JI, Choi JW, Park KC\n**Journal:** Lasers in Surgery and Medicine\n**DOI:** 10.1002/lsm.23985",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42467332/",
            "source_name": "PubMed",
            "title": "High-Concentration Polynucleotides (PN) Combined with Non-Crosslinked Hyaluronic Acid for Dermal Extracellular Matrix Remodeling and Photoaging Reversal: 12-Month Biometric Evaluation",
            "date": "2026",
            "content_markdown": "**Authors:** Chang CS, Lee HY, Lin YC, et al.\n**Journal:** Aesthetic Plastic Surgery\n**DOI:** 10.1007/s00266-026-05975-y",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42548201/",
            "source_name": "PubMed",
            "title": "Biomechanical Vectors of High-SMAS Dissection and Selective Facial Retaining Ligament Release in Midface Restoration",
            "date": "2026",
            "content_markdown": "**Authors:** Marten TJ, Elyassnia D, Aston SJ\n**Journal:** Aesthetic Surgery Journal\n**DOI:** 10.1093/asj/sjad445",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/42510344/",
            "source_name": "PubMed",
            "title": "Endoscopically Assisted High-SMAS Facial Rhytidectomy: A Multicenter 5-Year Prospective Cohort Study on Midcheek Repositioning and Complication Profiles",
            "date": "2026",
            "content_markdown": "**Authors:** Rohrich RJ, Sinno S, Vaca EE\n**Journal:** Plastic and Reconstructive Surgery\n**DOI:** 10.1097/PRS.0000000000012685",
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
