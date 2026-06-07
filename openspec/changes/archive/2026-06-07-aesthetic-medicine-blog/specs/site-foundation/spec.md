## ADDED Requirements

### Requirement: Hugo 项目初始化
系统 SHALL 使用 Hugo 静态站点生成器搭建项目骨架。

#### Scenario: Hugo 项目创建
- **WHEN** 执行 `hugo new site` 初始化项目
- **THEN** 生成标准的 Hugo 目录结构（archetypes、content、layouts、static、config 等）

#### Scenario: 配置文件加载
- **WHEN** Hugo 构建站点
- **THEN** SHALL 从 hugo.yaml 或 config/ 目录加载站点配置

### Requirement: 站点基础配置
站点 SHALL 配置 site title、baseURL、语言（zh-cn）、主题等基础元数据。

#### Scenario: 站点元数据配置
- **WHEN** 页面渲染
- **THEN** <title> 和 <meta> 标签 SHALL 使用站点配置中的 title 和 description

### Requirement: 主题集成
站点 SHALL 使用基于 PaperMod 定制的主题，支持黑暗模式和响应式布局。

#### Scenario: 主题应用
- **WHEN** Hugo 构建站点
- **THEN** SHALL 加载 theme/ 目录下的主题模板

#### Scenario: 黑暗模式切换
- **WHEN** 用户点击黑暗模式切换按钮
- **THEN** 页面 SHALL 在 light/dark 模式间切换，偏好 SHALL 存储在 localStorage 中

### Requirement: 构建与部署
站点 SHALL 支持一键构建并输出到 public/ 目录，构建产物可直接部署到静态托管平台。

#### Scenario: 生产构建
- **WHEN** 执行 `hugo --minify` 命令
- **THEN** 输出到 public/ 目录，HTML/CSS/JS 被压缩

#### Scenario: GitHub Pages 部署
- **WHEN** 推送代码到 main 分支
- **THEN** GitHub Actions SHALL 自动构建并部署到 GitHub Pages
