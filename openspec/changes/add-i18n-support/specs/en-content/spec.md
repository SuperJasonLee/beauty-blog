## ADDED Requirements

### Requirement: 英文内容目录
系统 SHALL 在 content/en/ 下创建英文内容目录结构。

#### Scenario: 目录创建
- **WHEN** 英文内容目录初始化
- **THEN** SHALL 创建 content/en/posts/、content/en/about/、content/en/archives/、content/en/search/ 目录

### Requirement: 英文示例文章
系统 SHALL 提供至少 2 篇英文示例文章。

#### Scenario: 英文文章内容
- **WHEN** 用户访问 /en/posts/
- **THEN** SHALL 显示英文文章列表，每篇文章 SHALL 使用英文 front matter
