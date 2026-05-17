## Why

网站已完成基础搭建，需要通过广告联盟实现流量变现以维持长期运营。Google AdSense 是最成熟的广告平台之一，能根据网站内容和访问者自动匹配相关广告，在保证用户体验的前提下创造收入。

## What Changes

- 在站点全局 `<head>` 中注入 Google AdSense 验证脚本
- 在文章页正文中插入广告位（文章内嵌广告）
- 在文章列表页之间插入广告位（列表广告）
- 在侧边栏（若有）添加广告位
- 实现广告位在移动端的响应式适配
- 遵守 Google AdSense 政策，不做违规展示

## Capabilities

### New Capabilities

- `adsense-setup`: Google AdSense 账号关联与全局脚本注入
- `in-article-ads`: 文章正文中的内嵌广告位
- `in-list-ads`: 文章列表页之间的广告位
- `responsive-ads`: 广告位的响应式适配，确保移动端正常展示

### Modified Capabilities

<!-- No existing capabilities to modify -->

## Impact

- 站点全局模板（baseof.html、extend_head.html）需要修改
- 文章页模板（single.html）需要添加广告位
- 列表页模板（list.html）需要添加广告位
- 新增 Google AdSense 发布商 ID 配置项
- 需确保广告展示不影响 AI 抓取和 SEO 评分
