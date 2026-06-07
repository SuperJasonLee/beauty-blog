## Why

The beauty blog needs fresh, timely content about eye plastic surgery (眼部整形美容手术) to attract readers and improve search rankings. Manually researching and writing bilingual posts is time-consuming. An automated pipeline to crawl the latest news, synthesize bilingual content, and incorporate relevant images will accelerate content production while maintaining quality.

## What Changes

- Create a Python script using `crawl4ai` to scrape the latest news about eye plastic surgery from reputable medical sites
- Implement an LLM-based content synthesis step to generate bilingual (Chinese/English) post drafts
- Download relevant images from crawled sources to `static/images/` for local embedding
- Generate Hugo-compatible markdown files for both `content/zh-cn/posts/` and `content/en/posts/`
- Add npm/CLI script to run the full pipeline on demand

## Capabilities

### New Capabilities
- `eye-surgery-news-crawler`: Automated web crawling of eye plastic surgery latest news using crawl4ai, with content extraction and deduplication
- `bilingual-post-generator`: LLM-powered synthesis of crawled content into bilingual posts (Chinese + English) with Hugo front matter
- `image-downloader`: Download and store crawled images locally, integrate into generated posts

### Modified Capabilities

<!-- No existing capabilities are modified -->

## Impact

- New `scripts/crawl-eye-surgery-news/` directory with Python scripts
- New `package.json` script entry for one-click execution
- New Hugo posts will appear under `content/zh-cn/posts/` and `content/en/posts/`
- Downloaded images stored in `static/images/eye-surgery-news/`
- Requires `crawl4ai` and `openai` Python packages
