## ADDED Requirements

### Requirement: 语言切换器
导航栏 SHALL 显示语言切换按钮，用户可切换中/英文版本。

#### Scenario: 切换器显示
- **WHEN** 用户浏览任何页面
- **THEN** 导航栏右侧 SHALL 显示语言切换下拉菜单，包含中文和英文选项

#### Scenario: 切换行为
- **WHEN** 用户点击英文链接
- **THEN** 跳转到当前页面对应的英文版（如有翻译），否则跳转到英文版首页

### Requirement: PaperMod 语言切换集成
系统 SHALL 利用 PaperMod 内置的 `disableLangToggle` 功能，确保语言切换器正常工作。

#### Scenario: 配置启用
- **WHEN** hugo.yaml 中 languages 配置了多个语言
- **THEN** PaperMod SHALL 自动显示语言切换器，无需额外模板修改
