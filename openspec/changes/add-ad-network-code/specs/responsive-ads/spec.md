## ADDED Requirements

### Requirement: 响应式广告单元
所有广告位 SHALL 使用 Google AdSense 的响应式广告单元，自动适配不同屏幕尺寸。

#### Scenario: 桌面端展示
- **WHEN** 用户使用桌面设备（>1024px）浏览
- **THEN** 广告单元 SHALL 显示桌面端优化的尺寸

#### Scenario: 移动端展示
- **WHEN** 用户使用移动设备（<768px）浏览
- **THEN** 广告单元 SHALL 自动适配移动端屏幕宽度

### Requirement: 广告容器 CSS
广告容器 SHALL 通过 CSS 设置最小高度以防止布局偏移（CLS）。

#### Scenario: 容器最小高度
- **WHEN** 广告容器被渲染
- **THEN** CSS SHALL 设置 `min-height: 100px` 为广告位预留空间

### Requirement: 广告不影响 AI 抓取
广告容器 SHALL 使用语义中立的 `<div>` 标签，避免干扰 AI 和搜索引擎对正文内容的抓取。

#### Scenario: 广告语义隔离
- **WHEN** AI 或搜索引擎爬虫抓取页面
- **THEN** 广告代码 SHALL 不在 `<article>` 等语义标签内，确保正文内容提取不受影响
