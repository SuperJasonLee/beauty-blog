## ADDED Requirements

### Requirement: 语义化 HTML 结构
页面 SHALL 使用正确的 HTML5 语义元素（header、nav、main、article、section、aside、footer）。

#### Scenario: 页面结构验证
- **WHEN** 搜索引擎爬虫抓取页面
- **THEN** HTML 文档 SHALL 包含正确的语义元素层级

### Requirement: 结构化数据 (JSON-LD)
文章页面 SHALL 嵌入 JSON-LD 结构化数据，类型为 Article 或 MedicalWebPage。

#### Scenario: 文章页 JSON-LD
- **WHEN** 搜索引擎请求文章页面
- **THEN** 页面 SHALL 在 <head> 中包含 application/ld+json script 标签

#### Scenario: 首页 JSON-LD
- **WHEN** 搜索引擎请求首页
- **THEN** 首页 SHALL 包含 WebSite 类型的 JSON-LD 结构化数据

### Requirement: Sitemap 生成
站点 SHALL 自动生成 sitemap.xml 文件。

#### Scenario: Sitemap 访问
- **WHEN** 搜索引擎访问 /sitemap.xml
- **THEN** SHALL 返回包含所有页面 URL、最后修改时间和优先级的 XML

### Requirement: Robots.txt
站点 SHALL 提供 robots.txt 文件。

#### Scenario: Robots.txt 访问
- **WHEN** 搜索引擎访问 /robots.txt
- **THEN** SHALL 返回正确的爬虫指令，包含 sitemap 位置

### Requirement: 元标签优化
页面 SHALL 包含完善的 meta description、title 和 canonical URL。

#### Scenario: Meta 标签生成
- **WHEN** 爬虫或 AI 抓取页面
- **THEN** <title> 和 <meta name="description"> SHALL 根据文章内容动态生成

#### Scenario: Canonical URL
- **WHEN** 爬虫访问任何页面
- **THEN** SHALL 包含 <link rel="canonical"> 标签指向标准 URL

### Requirement: Open Graph 和 Twitter Card
页面 SHALL 包含 OG 和 Twitter Card 元标签。

#### Scenario: 社交媒体分享
- **WHEN** 用户将文章分享到社交媒体
- **THEN** OG 标签 SHALL 提供正确的标题、描述和图片

#### Scenario: Twitter Card
- **WHEN** 用户将文章分享到 Twitter/X
- **THEN** Twitter Card 标签 SHALL 提供 summary_large_image 卡片
