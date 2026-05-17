## ADDED Requirements

### Requirement: 文章正文内嵌广告
系统 SHALL 在文章正文的第 3 段后插入一个 AdSense 展示广告单元。

#### Scenario: 广告显示
- **WHEN** 用户阅读文章且文章正文段落数 ≥ 3
- **THEN** 在第 3 个 `<p>` 元素后插入广告代码

#### Scenario: 短文章不展示广告
- **WHEN** 文章正文段落数 < 3
- **THEN** 不插入文章内嵌广告

### Requirement: 广告容器
广告单元 SHALL 包裹在语义中立的 `<div>` 容器中，避免使用 `<article>` 等语义标签。

#### Scenario: 容器结构
- **WHEN** 文章内嵌广告被渲染
- **THEN** 广告代码 SHALL 位于 `<div class="adsense-in-article">` 内
