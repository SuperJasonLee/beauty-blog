## ADDED Requirements

### Requirement: 列表页广告插入
系统 SHALL 在文章列表页的每 3 篇文章条目后插入一个 AdSense 展示广告单元。

#### Scenario: 列表广告显示
- **WHEN** 用户浏览文章列表页
- **THEN** 在第 3、6、9… 篇文章条目后各插入一个广告位

#### Scenario: 首页不展示列表广告
- **WHEN** 用户访问首页（.IsHome）
- **THEN** 不插入列表广告，避免影响首页展示效果

### Requirement: 列表广告容器
列表广告 SHALL 包裹在 `<div class="adsense-in-list">` 容器中，位于 `<article>` 条目之间。

#### Scenario: 广告位置验证
- **WHEN** 列表页渲染
- **THEN** 广告位 SHALL 出现在 `<article>` 条目之间，不在 `<article>` 内部
