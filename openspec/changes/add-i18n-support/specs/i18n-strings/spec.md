## ADDED Requirements

### Requirement: UI 字符串翻译
系统 SHALL 在 i18n/ 目录下提供英文翻译文件，覆盖 PaperMod 主题所有 UI 字符串。

#### Scenario: 英文翻译文件
- **WHEN** 用户访问英文版站点
- **THEN** 导航、分页、阅读时间等 UI 字符串 SHALL 显示英文

#### Scenario: 中文翻译覆盖
- **WHEN** 用户访问中文版站点
- **THEN** 导航、分页、阅读时间等 UI 字符串 SHALL 显示中文（与 PaperMod 内置一致）

### Requirement: 自定义字符串翻译
系统 SHALL 为自定义 UI 元素提供多语言支持。

#### Scenario: 搜索占位符
- **WHEN** 用户在英文版搜索
- **THEN** 搜索框占位符 SHALL 显示 "Search articles..."
- **WHEN** 用户在中文版搜索
- **THEN** 搜索框占位符 SHALL 显示 "搜索文章..."

#### Scenario: 免责声明
- **WHEN** 用户在英文版查看文章
- **THEN** 免责声明 SHALL 显示英文版本
