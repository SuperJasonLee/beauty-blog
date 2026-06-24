"""Pipeline orchestrator: crawl -> download images -> generate posts."""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("=" * 60)
    logger.info("Rhinoplasty News Pipeline - Starting")
    logger.info("=" * 60)

    # Step 1: Crawl
    logger.info("[Step 1/3] Crawling latest rhinoplasty news...")
    from crawler import crawl_all, save_results

    articles = crawl_all()
    if not articles:
        logger.error("No articles crawled. Aborting.")
        sys.exit(1)

    json_path = save_results(articles)
    logger.info(f"[Step 1/3] Done: {len(articles)} articles")

    # Step 2: Download images
    logger.info("[Step 2/3] Downloading images...")
    from image_downloader import main as download_images

    image_url_map = download_images(str(json_path))
    logger.info(f"[Step 2/3] Done: {len(image_url_map)} images")

    # Step 3: Generate posts
    logger.info("[Step 3/3] Generating bilingual posts...")
    from post_generator import main as generate_posts

    posts = generate_posts(str(json_path))
    logger.info(f"[Step 3/3] Done: {len(posts)} posts generated")

    logger.info("=" * 60)
    logger.info("Pipeline complete!")
    logger.info(f"  Articles crawled: {len(articles)}")
    logger.info(f"  Images downloaded: {len(image_url_map)}")
    logger.info(f"  Posts generated: {len(posts)}")
    logger.info("=" * 60)
    logger.info("Posts are marked as drafts. Review before publishing.")
    logger.info("Run 'hugo server -D' to preview.")


if __name__ == "__main__":
    run_pipeline()
