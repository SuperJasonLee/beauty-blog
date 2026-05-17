## ADDED Requirements

### Requirement: AdSense 发布商 ID 配置
系统 SHALL 通过 hugo.yaml 的 `params.adsense.publisherId` 配置 Google AdSense 发布商 ID。

#### Scenario: 配置读取
- **WHEN** Hugo 构建站点
- **THEN** 系统 SHALL 从 `site.Params.adsense.publisherId` 读取发布商 ID

#### Scenario: 空配置处理
- **WHEN** `params.adsense.publisherId` 未配置或为空
- **THEN** 系统 SHALL 不注入任何 AdSense 脚本

### Requirement: 全局 AdSense 脚本注入
系统 SHALL 在站点的全局 `<head>` 中注入 Google AdSense 自动广告脚本。

#### Scenario: 生产环境注入
- **WHEN** 站点为生产构建（hugo.IsProduction）
- **THEN** 系统 SHALL 注入 `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-PUBLISHER_ID" crossorigin="anonymous"></script>`

#### Scenario: 非生产环境不注入
- **WHEN** 站点为开发环境
- **THEN** 系统 SHALL 不注入 AdSense 脚本
