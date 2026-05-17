## Why

当今医疗美容市场信息混乱，求美者难以获取系统、可靠的知识内容。一个专注于整形美容知识的静态博客网站，能以低成本提供高质量、结构化的医美科普内容，同时对 AI 抓取和搜索引擎排名高度友好，帮助用户做出更明智的决策。

## What Changes

- 使用 Hugo 静态站点生成器搭建整形美容知识博客
- 实现 SEO 优化（语义化 HTML、结构化数据、sitemap、robots.txt、Open Graph、Twitter Card）
- 实现 AI 友好特性（语义 HTML 元素、JSON-LD 结构化数据、清晰的 heading 层级、语义化导航）
- 按手术/项目分类的知识体系与标签系统
- 基于 Markdown 的内容管理流程
- 响应式设计，支持移动端阅读
- RSS feed 支持
- 全文搜索功能

## Capabilities

### New Capabilities

- `site-foundation`: 站点基础架构，包括 Hugo 项目初始化、主题选择/定制、构建配置
- `content-organization`: 内容分类与组织结构，包括分类法（categories/tags）、导航、归档页面
- `seo`: SEO 优化，包括结构化数据（JSON-LD）、sitemap.xml、robots.txt、Open Graph/Twitter Card 元标签
- `ai-friendly`: AI 友好的语义标记，包括语义 HTML5 元素、清晰的 heading 层级、aria 标注、文章摘要 meta
- `content-management`: 基于 Markdown 的内容管理工作流，包括 front matter 规范、写作指南
- `search`: 站内全文搜索功能
- `rss-feed`: RSS Feed 订阅支持
- `responsive-design`: 响应式设计与移动端优化

### Modified Capabilities

<!-- No existing capabilities to modify -->

## Impact

- 新建 Hugo 静态站点项目
- 需要选择或定制 Hugo 主题
- 内容以 Markdown 文件存放在 content/ 目录
- 构建产物输出到 public/ 目录，可部署到任何静态托管平台
