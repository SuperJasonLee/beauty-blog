## Why

整形美容知识具有全球化需求，英文内容的加入能覆盖更广泛的中英文读者群体，提升网站在国际搜索引擎中的可见性，同时为未来的多语言扩展奠定基础。

## What Changes

- 在现有中文站基础上新增英文版本（`/en/`）
- 配置 Hugo 多语言模式，共享主题模板
- 创建中英文 i18n 翻译文件覆盖 UI 字符串
- 实现语言切换器，在导航栏中切换中/英文
- 英文内容独立管理，与中文共用主题和布局
- 配置多语言 SEO：hreflang 标签、语言版本 sitemap

## Capabilities

### New Capabilities

- `multilingual-config`: Hugo 多语言配置，包括 zh-cn 和 en 两种语言的站点参数
- `i18n-strings`: Hugo i18n 翻译文件，覆盖 PaperMod 主题及自定义 UI 字符串
- `language-switcher`: 导航栏中的语言切换器 UI
- `en-content`: 英文内容目录结构及至少 2 篇示例文章
- `multilingual-seo`: 多语言 SEO 配置，包括 hreflang、alternate link 和语言版本 URL

### Modified Capabilities

<!-- No existing capabilities to modify -->

## Impact

- hugo.yaml 配置需要重构为多语言模式
- 需为英文创建独立的 content/en/ 目录
- 现有的 zh-cn 内容不受影响，保留在 content/posts/ 下
- UI 字符串（导航标签、按钮文字、页脚）需要 i18n 翻译
- SEO 配置自动适配多语言（hreflang 自动由 Hugo 生成）
- 现有 URL 结构不变（中文路径不变），英文路径以 /en/ 为前缀
