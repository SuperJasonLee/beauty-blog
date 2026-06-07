## 1. Setup & Dependencies

- [x] 1.1 Create `scripts/crawl-eye-surgery-news/` directory structure
- [x] 1.2 Create Python virtual environment and install `crawl4ai`, `openai`, `httpx` dependencies
- [x] 1.3 Create `data/crawled/eye-surgery-news/` and `static/images/eye-surgery-news/` directories
- [x] 1.4 Add npm script entry `"crawl:eye-news"` in package.json
- [x] 1.5 Create `.env.example` with OPENAI_API_KEY placeholder and add `.env` to `.gitignore`

## 2. Crawler Script

- [x] 2.1 Implement `crawler.py` with crawl4ai configuration (sources list, polite delays, User-Agent)
- [x] 2.2 Configure 3-5 source URLs for latest eye plastic surgery news
- [x] 2.3 Implement article extraction: title, date, content markdown, image URLs
- [x] 2.4 Implement error handling for unreachable sources with logging
- [x] 2.5 Implement URL deduplication (skip already-crawled URLs)
- [x] 2.6 Implement JSON output to `data/crawled/eye-surgery-news/` with timestamp

## 3. Image Downloader Script

- [x] 3.1 Implement `image_downloader.py` that reads crawled JSON and downloads images
- [x] 3.2 Implement unique filename generation (`eye-surgery-news-{date}-{increment}.{ext}`)
- [x] 3.3 Implement error handling for failed image downloads with logging
- [x] 3.4 Implement post content update to reference local image paths

## 4. Bilingual Post Generator Script

- [x] 4.1 Implement `post_generator.py` with OpenAI API client (gpt-4o-mini)
- [x] 4.2 Implement Chinese post generation prompt and Hugo markdown output
- [x] 4.3 Implement English post generation prompt and Hugo markdown output
- [x] 4.4 Implement Hugo front matter generation (title, date, draft: true, tags, categories, image, description)
- [x] 4.5 Implement bilingual post pairing via translation links in front matter
- [x] 4.6 Integrate downloaded image paths into generated posts

## 5. Pipeline Orchestration

- [x] 5.1 Create `run.sh` or Python entrypoint that chains crawl → download → generate
- [x] 5.2 Implement progress logging throughout the pipeline
- [x] 5.3 Test end-to-end run and verify Hugo output files
