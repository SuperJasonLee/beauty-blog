## ADDED Requirements

### Requirement: Hreflang 标签
站点在英文和中文页面 SHALL 自动生成 hreflang 标签。

#### Scenario: 中文页 Hreflang
- **WHEN** 搜索引擎爬取中文页面
- **THEN** <head> 中 SHALL 包含 `<link rel="alternate" hreflang="en" href="...">` 和 `<link rel="alternate" hreflang="zh-cn" href="...">`

#### Scenario: 英文页 Hreflang
- **WHEN** 搜索引擎爬取英文页面
- **THEN** <head> 中 SHALL 包含对应的 hreflang 标签

### Requirement: 语言版本 Sitemap
站点 SHALL 为每个语言版本生成独立的 sitemap。

#### Scenario: 中文 Sitemap
- **WHEN** 搜索引擎访问 /sitemap.xml
- **THEN** SHALL 包含中文页面的 URL

#### Scenario: 英文 Sitemap
- **WHEN** 搜索引擎访问 /en/sitemap.xml
- **THEN** SHALL 包含英文页面的 URL
