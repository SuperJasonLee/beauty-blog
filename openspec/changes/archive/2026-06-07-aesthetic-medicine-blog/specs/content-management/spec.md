## ADDED Requirements

### Requirement: Markdown 内容管理
所有文章内容 SHALL 使用 Markdown 格式编写，存储在 content/posts/ 目录下。

#### Scenario: 文章创建
- **WHEN** 作者创建新文章
- **THEN** 在 content/posts/ 下创建 .md 文件，使用 Hugo archetype 生成 front matter 模板

### Requirement: Front Matter 规范
每篇文章 SHALL 包含完整的 front matter：title、date、description、categories、tags、draft、featuredImage。

#### Scenario: Front Matter 验证
- **WHEN** Hugo 构建文章页面
- **THEN** front matter 中的 title SHALL 用作页面标题，description 用作 meta description

#### Scenario: 草稿模式
- **WHEN** 文章 front matter 中 draft: true
- **THEN** Hugo 构建时 SHALL 跳过该文章，除非使用 -D 标志

### Requirement: 文章内容规范
文章内容 SHALL 遵循统一的写作规范，包括引用标注、免责声明和参考来源。

#### Scenario: 免责声明
- **WHEN** Hugo 渲染不含免责声明的文章
- **THEN** 系统 SHALL 自动在文章底部追加标准医疗免责声明

#### Scenario: 参考来源
- **WHEN** 文章内容包含引用
- **THEN** 文末 SHALL 以 ## 参考资料 章节列出引用来源

### Requirement: 短代码支持
系统 SHALL 提供自定义 Hugo shortcodes 用于常见内容格式（警告框、提示框、术语解释）。

#### Scenario: 警告样式
- **WHEN** 文章使用 {{< alert "warning" >}} 短代码
- **THEN** 渲染为带警告图标的彩色提示框
