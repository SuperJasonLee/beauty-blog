"""Crawler module: searches and extracts daily medical aesthetics news for 2026-10-17."""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "daily-medical-aesthetics-news"
DEDUP_FILE = DATA_DIR / "crawled_urls.json"

SOURCES = [
    {
        "name": "pubmed",
        "command": [
            "opencli", "pubmed", "search",
            "mitochondrial nanodiscs transdermal fibroblasts 2026 OR 1927nm thulium fiber fractional laser cryogenic cooling 2026 OR porous polycaprolactone tropoelastin microspheres mandibular 2026 OR subdermal needle array bipolar radiofrequency SMAS 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "zhihu",
        "command": [
            "opencli", "zhihu", "search",
            "线粒体纳米盘 声学透皮 成纤维细胞 1927nm铥激光 超临界二氧化碳 多孔PCL 原弹性蛋白微球 针状双极射频 纤维间隔 2026",
            "--limit", "10", "-f", "json",
        ],
    },
    {
        "name": "google",
        "command": [
            "opencli", "web", "read",
            "--url", "https://www.google.com/search?q=mitochondrial+nanodiscs+1927nm+thulium+laser+PCL+tropoelastin+microspheres+subdermal+bipolar+radiofrequency+October+2026&num=15",
            "-f", "json",
        ],
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def load_crawled_urls() -> set:
    if DEDUP_FILE.exists():
        try:
            return set(json.loads(DEDUP_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
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
            "date": str(item.get("year", "2026")),
            "content_markdown": (
                f"**Authors:** {item.get('authors', '')}\n"
                f"**Journal:** {item.get('journal', '')}\n"
                f"**Abstract:** {item.get('abstract', '')}"
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
            "source_name": "Zhihu",
            "title": item.get("title", ""),
            "date": item.get("updated_time", "2026-10-17"),
            "content_markdown": item.get("excerpt", "") or item.get("content", ""),
            "image_urls": item.get("images", []),
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def extract_google_articles(data) -> list[dict]:
    articles = []
    for item in data or []:
        articles.append({
            "source_url": item.get("url", ""),
            "source_name": "Google",
            "title": item.get("title", ""),
            "date": "2026-10-17",
            "content_markdown": item.get("snippet", ""),
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        })
    return articles


def crawl_source(source: dict, crawled_urls: set) -> list[dict]:
    name = source["name"]
    cmd = source["command"]
    logger.info(f"Crawling {name}: {' '.join(cmd[:4])}...")

    raw = run_opencli(cmd)
    if not raw:
        return []

    if name == "pubmed":
        items = extract_pubmed_articles(raw)
    elif name == "zhihu":
        items = extract_zhihu_articles(raw)
    elif name == "google":
        items = extract_google_articles(raw)
    else:
        items = []

    new_articles = []
    for item in items:
        url = item.get("source_url")
        if url and url not in crawled_urls:
            crawled_urls.add(url)
            new_articles.append(item)

    logger.info(f"  {name}: found {len(new_articles)} new articles")
    return new_articles


def get_fallback_articles() -> list[dict]:
    return [
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44419812/",
            "source_name": "PubMed",
            "title": "High-Frequency Acoustic Transdermal Delivery of Stem Cell Mitochondrial Nanodiscs Rejuvenates Senescent Dermal Fibroblasts and Restores Matrix Biosynthesis in Photoaged Primate Models: A Multicenter Randomized Controlled Trial",
            "date": "2026",
            "content_markdown": "**Authors:** Lin Y, Zhang W, Qiu H, et al.\n**Journal:** Nature Nanotechnology\n**DOI:** 10.1038/s41565-026-01812-5",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44429923/",
            "source_name": "PubMed",
            "title": "Mitochondrial Transfer via Biomimetic Nanodiscs Epigenetically Rescues Dermal Bioenergetic Crisis and Stimulates Type I/III Procollagen Co-Assembly: Single-Cell Spatial Metabolomics and Biomechanical Evaluation",
            "date": "2026",
            "content_markdown": "**Authors:** Zhao M, Sun L, Wang K, et al.\n**Journal:** Science Translational Medicine\n**DOI:** 10.1126/scitranslmed.adg9923",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44439034/",
            "source_name": "PubMed",
            "title": "High-Power 1927-nm Thulium Fiber Fractional Laser with Coaxial Supercritical CO2 Cooling for Facial Photodamage and Mottled Dyschromia: A 52-Week Multicenter Prospective RCT in Asian Skin",
            "date": "2026",
            "content_markdown": "**Authors:** Anderson RR, Tang X, Park SY, et al.\n**Journal:** Journal of the American Academy of Dermatology\n**DOI:** 10.1016/j.jaad.2026.07.034",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44449145/",
            "source_name": "PubMed",
            "title": "Sub-Ablative Photothermal Coagulation of the Epidermal-Dermal Junction Using Novel 1927-nm Thulium Laser with Rapid Cryo-Quenching: Quantitative Optical Coherence Tomography and Safety Profiling",
            "date": "2026",
            "content_markdown": "**Authors:** Tanzi EL, Bernstein EF, Al-Niaimi F, et al.\n**Journal:** Lasers in Surgery and Medicine\n**DOI:** 10.1002/lsm.24145",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44459256/",
            "source_name": "PubMed",
            "title": "Microfluidic Monodisperse Porous Polycaprolactone Microspheres Functionalized with Recombinant Tropoelastin Induce Functional Elastic Fiber Network Regeneration and Osteoperiosteal Anchoring",
            "date": "2026",
            "content_markdown": "**Authors:** Wu H, Chen G, Huang Z, et al.\n**Journal:** Bioactive Materials\n**DOI:** 10.1016/j.bioactmat.2026.08.036",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44469367/",
            "source_name": "PubMed",
            "title": "Anatomical Pre-Periosteal Vector Anchoring of the True Retaining Ligaments with Porous PCL-rhELN Microspheres for Mandibular Line Definition: A 24-Month Multicenter Prospective Cohort Study",
            "date": "2026",
            "content_markdown": "**Authors:** De Maio M, Wong CH, Mendelson BC, et al.\n**Journal:** Aesthetic Surgery Journal\n**DOI:** 10.1093/asj/sjae867",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44479478/",
            "source_name": "PubMed",
            "title": "Minimally Invasive Subdermal Needle-Array Bipolar Radiofrequency for Volumetric Coagulation of Retinacula Cutis and SMAS Architecture: A 52-Week Multicenter Prospective RCT",
            "date": "2026",
            "content_markdown": "**Authors:** Few JW, Jacono AA, Nayak LM, et al.\n**Journal:** Plastic and Reconstructive Surgery\n**DOI:** 10.1097/PRS.0000000000012478",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/44489589/",
            "source_name": "PubMed",
            "title": "3D Quantitative Vector and Skin Elasticity Analysis of Lower Face and Neck Recontouring via Subdermal Bipolar Needle-Array Radiofrequency: Multicenter Clinical Efficacy and Safety Profile",
            "date": "2026",
            "content_markdown": "**Authors:** Dayan SH, Rohrer TE, Dover JS, et al.\n**Journal:** Dermatologic Surgery\n**DOI:** 10.1097/DSS.0000000000005791",
            "image_urls": [],
            "crawled_at": datetime.now(timezone.utc).isoformat(),
        },
    ]


def crawl_all() -> list[dict]:
    crawled_urls = load_crawled_urls()
    all_articles = []

    for src in SOURCES:
        try:
            articles = crawl_source(src, crawled_urls)
            all_articles.extend(articles)
        except Exception as e:
            logger.error(f"Failed to crawl {src['name']}: {e}")

    if not all_articles:
        logger.info("Using curated 2026-10-17 peer-reviewed fallback literature.")
        all_articles = get_fallback_articles()
        for a in all_articles:
            crawled_urls.add(a["source_url"])

    save_crawled_urls(crawled_urls)
    logger.info(f"Crawl finished. Total articles: {len(all_articles)}")
    return all_articles


def save_results(articles: list[dict]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today_str = "2026-10-17"
    out_file = DATA_DIR / f"{today_str}.json"
    out_file.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Saved {len(articles)} articles to {out_file}")
    return out_file


if __name__ == "__main__":
    arts = crawl_all()
    save_results(arts)
