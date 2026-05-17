## Context

当前站点仅支持简体中文（zh-cn），使用 Hugo + PaperMod 搭建。PaperMod 主题已内置多语言支持和 i18n 翻译系统。需要新增英文（en）版本，与中文共享同一套主题模板。

## Goals / Non-Goals

**Goals:**
- Hugo 配置重构为多语言模式（zh-cn + en）
- 英文内容可独立管理（content/en/）
- 导航栏显示语言切换器
- UI 字符串使用 Hugo i18n 翻译
- 英文 URL 以 /en/ 为前缀
- 多语言 SEO 标签自动生成

**Non-Goals:**
- 不自动翻译中文内容为英文（人工编写独立英文内容）
- 不支持双向文本（如阿拉伯语）
- 不涉及内容翻译管理平台
- 不涉及多语言评论系统

## Decisions

| 决策 | 选择 | 方案 | 理由 |
|---|---|---|---|
| URL 结构 | /en/ 前缀子目录 | 子域名 en.example.com | Hugo 多语言子目录模式最易配置，无需额外 DNS 配置 |
| 内容管理 | 手动编写英文内容 | 自动机器翻译 | 医学内容准确性要求高，人工编写保证质量 |
| 语言切换器 | PaperMod 内置语言切换 | 自定义实现 | PaperMod 已内置语言切换 UI，开启 `disableLangToggle: false` 即可 |
| i18n 机制 | Hugo 原生 i18n | 自定义方案 | Hugo 通过 i18n/ 目录 + `{{ i18n "key" }}` 函数原生支持，与 PaperMod 兼容 |

## Risks / Trade-offs

| 风险 | 缓解措施 |
|---|---|
| 英文内容不足导致多语言体验差 | 初期仅翻译导航/UI 字符串，英文文章逐步添加 |
| 中文 URL 路径变化影响 SEO | 保持中文 URL 结构不变（/posts/ 不变），英文以 /en/posts/ 路径 |
| 维护成本翻倍 | 内容结构与主题模板共享，只需管理两套内容文件 |
