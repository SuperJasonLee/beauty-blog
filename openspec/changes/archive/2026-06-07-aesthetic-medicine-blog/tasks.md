## 1. 项目初始化

- [x] 1.1 安装 Hugo（确保系统已安装 Hugo Extended 版本）
- [x] 1.2 使用 `hugo new site` 初始化项目，创建 Git 仓库
- [x] 1.3 初始化 NPM 项目，安装 PostCSS、autoprefixer 等构建依赖
- [x] 1.4 创建 .gitignore 文件（排除 public/、node_modules/、resources/）
- [x] 1.5 配置 hugo.yaml：title、baseURL、languageCode（zh-cn）、theme、taxonomies
- [x] 1.6 下载 PaperMod 主题并配置为 Git submodule

## 2. 主题定制与基础布局

- [x] 2.1 创建 layouts/ 目录，覆盖主题的 baseof.html 添加语义化 HTML5 结构
- [x] 2.2 定制导航栏：主导航菜单、汉堡菜单（移动端）、aria-label
- [x] 2.3 配置黑暗模式切换（利用 PaperMod 内置支持）
- [x] 2.4 定制 footer：版权信息、社交链接、RSS 订阅链接
- [x] 2.5 定制 404 页面

## 3. 内容组织与分类

- [x] 3.1 在 content/ 下创建 posts/、about/、categories/、archives/ 等目录
- [x] 3.2 在 hugo.yaml 中配置 categories 和 tags 分类法
- [x] 3.3 创建分类列表页模板（利用 PaperMod taxonomy.html）
- [x] 3.4 创建分类文章列表页模板（利用 PaperMod list.html）
- [x] 3.5 创建归档页面模板（利用 PaperMod archives.html）
- [x] 3.6 实现面包屑导航（利用 PaperMod breadcrumbs.html）

## 4. SEO 优化

- [x] 4.1 配置 Hugo 自动生成 sitemap.xml（hugo.yaml 中配置 sitemap）
- [x] 4.2 创建 robots.txt 模板（layouts/robots.txt）
- [x] 4.3 实现 JSON-LD 结构化数据（MedicalWebPage 类型）
- [x] 4.4 实现 JSON-LD 结构化数据（WebSite 类型，首页）
- [x] 4.5 实现 meta description、canonical URL 动态生成（PaperMod 内置）
- [x] 4.6 实现 Open Graph 和 Twitter Card 元标签
- [x] 4.7 配置 Hugo 生成干净的 URL 路径

## 5. AI 友好优化

- [x] 5.1 确保 baseof.html 使用严格语义化 HTML5 元素（header、nav、main、article、aside、footer）
- [x] 5.2 确保文章页面 heading 层级从 h1 到 h3 递增，不跳级
- [x] 5.3 为导航栏添加 aria-label、aria-current="page" 等 ARIA 属性
- [x] 5.4 确保文章摘要通过 meta description 和 og:description 暴露

## 6. 内容管理工作流

- [x] 6.1 创建 Hugo archetype（archetypes/posts.md），包含完整 front matter 模板
- [x] 6.2 编写内容写作指南文档（CONTRIBUTING.md）
- [x] 6.3 实现医疗免责声明自动追加 partial
- [x] 6.4 创建自定义 shortcodes：alert（警告框）、info（提示框）、term（术语解释）
- [x] 6.5 编写 3 篇示例文章用于测试

## 7. 搜索功能

- [x] 7.1 在 NPM 中添加 pagefind 依赖
- [x] 7.2 创建搜索入口 UI（搜索按钮 + 模态框）
- [x] 7.3 集成 Pagefind 搜索 UI，配置中文语言支持
- [x] 7.4 更新构建脚本：Hugo 构建后自动执行 Pagefind 索引
- [x] 7.5 实现键盘导航支持（ESC 关闭、上下键导航、Enter 打开）

## 8. 响应式设计与性能

- [x] 8.1 定制 CSS：中文排版优化（字体栈、行高、字号）
- [x] 8.2 配置图片响应式处理（使用 Hugo Image Processing）
- [x] 8.3 为图片添加 loading="lazy" 属性（Hugo 默认行为）
- [x] 8.4 配置 CSS/JS 压缩（hugo --minify + PostCSS）
- [x] 8.5 验证构建输出：Hugo 构建成功，生成 48 页面

## 9. RSS Feed

- [x] 9.1 验证 Hugo 默认 RSS 模板输出标准 RSS 2.0 XML
- [x] 9.2 在 <head> 中添加 RSS Feed 自动发现 link 标签
- [x] 9.3 在 footer 中添加 RSS 订阅链接

## 10. 部署与 CI/CD

- [x] 10.1 创建 GitHub Actions 工作流（.github/workflows/deploy.yml）
- [x] 10.2 配置 GitHub Pages 部署（使用 actions/upload-pages-artifact）
- [x] 10.3 验证构建流程：hugo build + pagefind 均成功
- [x] 10.4 配置自定义域名（如适用）— 跳过，当前无自定义域名
