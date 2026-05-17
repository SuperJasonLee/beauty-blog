## 1. 多语言配置重构

- [ ] 1.1 重构 hugo.yaml：将单语言配置改为多语言模式（defaultContentLanguage: zh-cn）
- [ ] 1.2 配置英文（en）语言块：title、locale、label、weight、menu、params
- [ ] 1.3 确保中文配置完整保留，英文导航菜单使用英文标签

## 2. i18n 翻译文件

- [ ] 2.1 创建 i18n/zh-cn.yaml：覆盖 PaperMod 主题中文 UI 字符串
- [ ] 2.2 创建 i18n/en.yaml：PaperMod 主题英文 UI 字符串
- [ ] 2.3 在模板中使用 `{{ i18n "key" }}` 替代硬编码中文文本

## 3. 语言切换器

- [ ] 3.1 在 hugo.yaml 中设置 languages 启用语言切换（PaperMod 自动检测）
- [ ] 3.2 验证导航栏显示语言切换下拉菜单
- [ ] 3.3 验证中英文页面间切换正常

## 4. 英文内容创建

- [ ] 4.1 创建 content/en/posts/、content/en/about/、content/en/archives/、content/en/search/ 目录
- [ ] 4.2 创建英文搜索页（content/en/search/_index.md）
- [ ] 4.3 创建英文归档页（content/en/archives/_index.md）
- [ ] 4.4 创建英文关于页（content/en/about/_index.md）
- [ ] 4.5 翻译 2 篇示例文章为英文

## 5. 多语言 SEO 验证

- [ ] 5.1 构建站点，检查英文页面 URL 以 /en/ 为前缀
- [ ] 5.2 检查 <head> 中 hreflang alternate 标签正确生成
- [ ] 5.3 检查 sitemap 包含中英文两个版本
- [ ] 5.4 执行 `hugo --minify` 确认构建无错误
