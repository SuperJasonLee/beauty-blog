## ADDED Requirements

### Requirement: 站内全文搜索
系统 SHALL 集成 Pagefind 实现站内全文搜索功能，无需外部服务。

#### Scenario: 搜索入口
- **WHEN** 用户点击搜索按钮或按 Ctrl+K
- **THEN** SHALL 弹出搜索模态框，包含搜索输入框

#### Scenario: 搜索结果
- **WHEN** 用户输入关键词
- **THEN** SHALL 实时显示匹配的文章标题、摘要片段和链接

#### Scenario: 中文搜索
- **WHEN** 用户输入中文关键词
- **THEN** Pagefind SHALL 正确索引和匹配中文内容

### Requirement: 搜索索引构建
Pagefind SHALL 在 Hugo 构建完成后自动索引 public/ 目录的内容。

#### Scenario: 索引生成
- **WHEN** 执行构建脚本（hugo && npx pagefind）
- **THEN** SHALL 在 public/pagefind/ 生成搜索索引文件

### Requirement: 搜索 UI 集成
搜索界面 SHALL 与站点主题风格一致，支持键盘导航。

#### Scenario: 键盘操作
- **WHEN** 搜索模态框打开
- **THEN** ESC SHALL 关闭模态框，上下箭头 SHALL 导航搜索结果，Enter SHALL 打开选中结果
