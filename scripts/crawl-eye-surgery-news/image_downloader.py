"""Image downloader: fetches images from crawled articles and stores locally."""

import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx

IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "images" / "eye-surgery-news"
IMAGE_URL_PATTERN = re.compile(r"!\[([^\]]*)\]\((https?://[^)]+)\)")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def generate_filename(url: str, date: str, increment: int) -> str:
    ext = Path(url).suffix.split("?")[0][:5] or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    return f"eye-surgery-news-{date}-{increment:03d}{ext}"


def download_image(url: str, filename: str, timeout: int = 30) -> Optional[str]:
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BeautyBlog/1.0)"})
            resp.raise_for_status()
            filepath = IMAGES_DIR / filename
            filepath.write_bytes(resp.content)
            logger.info(f"Downloaded: {filename} ({len(resp.content)} bytes)")
            return filename
    except httpx.HTTPError as e:
        logger.warning(f"Failed to download {url}: {e}")
    except Exception as e:
        logger.warning(f"Error downloading {url}: {e}")
    return None


def download_images_from_article(article: dict, date_str: str, counter_start: int) -> tuple[dict, int]:
    content = article.get("content_markdown", "")
    image_urls = article.get("image_urls", [])
    downloaded = {}
    counter = counter_start

    for url in image_urls:
        filename = generate_filename(url, date_str, counter)
        result = download_image(url, filename)
        if result:
            downloaded[url] = f"/images/eye-surgery-news/{filename}"
            counter += 1

    for url, local_path in downloaded.items():
        content = content.replace(url, local_path)

    article["content_markdown"] = content
    return article, counter


def process_crawled_file(json_path: Path) -> dict:
    articles = json.loads(json_path.read_text(encoding="utf-8"))
    date_str = datetime.now().strftime("%Y%m%d")
    counter = 1
    url_map = {}

    for article in articles:
        article, counter = download_images_from_article(article, date_str, counter)
        for img_url in article.get("image_urls", []):
            local = f"/images/eye-surgery-news/{generate_filename(img_url, date_str, counter)}"
            if img_url in article["content_markdown"]:
                url_map[img_url] = local

    json_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Processed {len(articles)} articles, downloaded {counter - 1} images")
    return url_map


def main(json_path: Optional[str] = None):
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    if json_path:
        path = Path(json_path)
    else:
        data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "eye-surgery-news"
        files = sorted(data_dir.glob("eye_surgery_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return {}
        path = files[-1]

    return process_crawled_file(path)


if __name__ == "__main__":
    import sys
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(json_file)
