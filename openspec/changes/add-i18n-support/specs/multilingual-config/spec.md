## ADDED Requirements

### Requirement: 多语言配置
系统 SHALL 在 hugo.yaml 中配置两种语言：zh-cn（默认）和 en。

#### Scenario: 语言定义
- **WHEN** Hugo 构建站点
- **THEN** SHALL 定义 `languages.zh-cn` 和 `languages.en`，其中 zh-cn 为默认语言（weight: 1），en 为第二语言（weight: 2）

#### Scenario: 英文站点标题
- **WHEN** 用户访问英文版站点
- **THEN** 站点标题 SHALL 为 "Aesthetic Medicine Knowledge Base"

#### Scenario: 英文 URL 前缀
- **WHEN** 用户访问英文版文章
- **THEN** URL SHALL 以 /en/ 为前缀，如 /en/posts/2026/rhinoplasty-guide/

### Requirement: 英文版导航菜单
英文版 SHALL 有独立的导航菜单配置。

#### Scenario: 英文导航
- **WHEN** 用户在英文版浏览
- **THEN** 导航菜单 SHALL 显示英文标签：Home、Articles、Categories、Tags、Archives、About
