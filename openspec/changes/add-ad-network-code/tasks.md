## 1. AdSense 全局配置与脚本注入

- [x] 1.1 在 hugo.yaml 中添加 `params.adsense.publisherId` 配置项
- [x] 1.2 创建 `layouts/partials/adsense-head.html`：全局 AdSense 自动广告脚本 partial
- [x] 1.3 在 `layouts/partials/extend_head.html` 中引入 adsense-head partial，仅生产环境加载

## 2. 文章内嵌广告

- [x] 2.1 创建 `layouts/partials/adsense-in-article.html`：文章内嵌广告单元 partial
- [x] 2.2 创建 `layouts/_default/single.html` 覆盖 PaperMod 的 single.html，在文章正文第 3 段后插入广告
- [x] 2.3 验证短文章（< 3 段落）不展示内嵌广告

## 3. 列表页广告

- [x] 3.1 创建 `layouts/partials/adsense-in-list.html`：列表广告单元 partial
- [x] 3.2 创建 `layouts/_default/list.html` 覆盖 PaperMod 的 list.html，在每 3 篇文章后插入广告
- [x] 3.3 验证首页不展示列表广告

## 4. 响应式适配与 CSS

- [x] 4.1 在 `assets/css/extended/custom.css` 中添加广告容器样式（min-height、居中、间距）
- [ ] 4.2 验证移动端广告显示正常（需等待 adSlot 配置后手动验证）
- [ ] 4.3 验证广告容器不干扰 AI 抓取（使用非语义 div，代码层面已完成）

## 5. 构建验证

- [x] 5.1 执行 `hugo --minify` 确认构建无错误
- [x] 5.2 检查生成的 HTML 中 AdSense 脚本和广告位代码正确注入
- [x] 5.3 确认非生产环境不输出广告代码
