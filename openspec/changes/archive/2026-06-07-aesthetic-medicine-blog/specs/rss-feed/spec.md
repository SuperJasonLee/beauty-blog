## ADDED Requirements

### Requirement: RSS Feed 生成
站点 SHALL 自动生成 RSS Feed，包含最新文章列表。

#### Scenario: RSS Feed 访问
- **WHEN** 用户或 RSS 阅读器访问 /index.xml
- **THEN** SHALL 返回标准 RSS 2.0 XML，包含最新文章的标题、链接、摘要和发布日期

#### Scenario: Feed 自动发现
- **WHEN** 用户访问任何页面
- **THEN** <head> 中 SHALL 包含 <link rel="alternate" type="application/rss+xml"> 标签指向 RSS Feed
