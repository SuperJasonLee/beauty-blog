## Context

The beauty blog is a Hugo-based bilingual (zh-cn/en) site using the PaperMod theme. Currently, content is manually authored. This change introduces an automated pipeline to crawl the latest news about eye plastic surgery using crawl4ai, synthesize bilingual posts via LLM, and integrate images locally. The pipeline runs as a CLI script and outputs Hugo-compatible markdown files.

## Goals / Non-Goals

**Goals:**
- Automated crawling of latest eye plastic surgery news from 3-5 reputable medical/aesthetic sources
- LLM-based synthesis of crawled content into bilingual (Chinese + English) post drafts
- Automatic download and local storage of crawled images
- Generate Hugo-compatible markdown files with proper front matter, placed in their respective content directories
- One-command execution via npm script

**Non-Goals:**
- Automated publishing or deployment (human review before publishing)
- Scheduled/running on a cron job (manual execution only)
- Covering all plastic surgery topics (eye-specific only)
- SEO optimization beyond standard Hugo front matter

## Decisions

1. **crawl4ai over Scrapy/BeautifulSoup** → crawl4ai provides LLM-optimized content extraction out of the box, reducing boilerplate. It handles JavaScript-rendered pages and returns clean markdown.
2. **OpenAI API for bilingual synthesis** → Best-in-class multilingual quality. Use `gpt-4o-mini` for cost efficiency with structured output JSON mode.
3. **One script per capability** → Pipeline consists of 3 standalone Python scripts wired by a shell/npm entrypoint. Each script can be run independently for debugging.
4. **Images downloaded to `static/images/eye-surgery-news/`** → Hugo convention for static assets. Images referenced via relative path in front matter.
5. **Hugo content placement** → Posts go to `content/zh-cn/posts/eye-surgery-news/` and `content/en/posts/eye-surgery-news/` with matching filenames for bilingual pairing.

## Risks / Trade-offs

- **Crawled site availability** → Some sites may block scraping. Mitigation: include polite delays, User-Agent headers, and a list of fallback sources.
- **Image copyright** → Downloaded images may have usage restrictions. Mitigation: only crawl sites with permissive licenses, add source attribution in post metadata.
- **LLM hallucination in synthesis** → Generated content may contain inaccuracies. Mitigation: posts are drafts requiring human review before publishing. Add disclaimer in front matter.
- **Content freshness** → News is time-sensitive. Mitigation: include crawled date in post front matter so editors can assess timeliness.
