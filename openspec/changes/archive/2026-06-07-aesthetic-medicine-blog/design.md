## Context

当前项目根目录下尚无任何网站源码。需要从零搭建一个专注于整形美容知识的静态博客网站。用户要求对 AI 友好（语义化 HTML、结构化数据）且对搜索引擎友好（SEO 最佳实践）。

## Goals / Non-Goals

**Goals:**
- 基于 Hugo 搭建高性能静态博客
- 实现完整 SEO 优化（JSON-LD、sitemap、robots.txt、OG/Twitter Card）
- 实现 AI 爬取友好（语义化 HTML5 元素、aria 标注、清晰层级）
- 建立按手术/项目分类的知识体系
- 支持 Markdown 内容工作流
- 响应式设计，移动端优先
- RSS Feed 订阅
- 站内全文搜索

**Non-Goals:**
- 不涉及用户登录/注册系统
- 不涉及评论系统（初期）
- 不涉及多语言支持（初期仅中文）
- 不涉及后端服务或数据库

## Decisions

| 决策 | 选择 | 方案 | 理由 |
|---|---|---|---|
| 静态站点生成器 | Hugo | Jekyll, Next.js SSG | Hugo 构建速度极快，单二进制部署，Go 模板强大，社区主题丰富 |
| 主题方案 | 基于 PaperMod 定制 | 纯手工 CSS, 其他 Hugo 主题 | PaperMod 轻量、SEO 友好、支持黑暗模式、维护活跃 |
| 内容格式 | Markdown + Front Matter | 无头 CMS (Strapi 等) | 纯文件管理，对 AI 最友好，Git 版本控制，无数据库依赖 |
| 结构化数据 | JSON-LD (Schema.org) | Microdata, RDFa | Google 推荐格式，易于注入，AI 爬取最佳 |
| 搜索方案 | Hugo 原生 + Pagefind | Lunr.js, Algolia | Pagefind 零配置、无后端、隐私友好、中文分词支持好 |
| 部署平台 | GitHub Pages | Netlify, Vercel | 免费、与 Git 工作流集成、自动 HTTPS |
| 构建工具 | Hugo + NPM (PostCSS) | 纯 Hugo | 需要 PostCSS 处理样式优化，minify 等 |

## Risks / Trade-offs

| 风险 | 缓解措施 |
|---|---|
| 医疗内容准确性要求高 | 建立内容审核流程，每篇文章标注参考来源和免责声明 |
| 中文 SEO 竞争激烈 | 专注长尾关键词，建立内容矩阵，注重 EEAT 信号 |
| 静态站点内容更新不实时 | 采用 GitHub Actions 自动构建部署，推送即发布 |
| Pagefind 中文分词准确性 | 配置 Pagefind 语言为 zh，测试中文字词索引效果 |
| 医疗广告法规合规 | 内容仅做科普知识介绍，不做诊疗推荐，不发布未认证的医疗广告 |
