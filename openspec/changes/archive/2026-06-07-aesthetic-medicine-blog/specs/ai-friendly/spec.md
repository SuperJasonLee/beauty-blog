## ADDED Requirements

### Requirement: 语义化 HTML5 元素
页面 SHALL 严格使用 HTML5 语义元素标记内容结构（header、nav、main、article、section、aside、footer）。

#### Scenario: AI 解析页面结构
- **WHEN** AI 爬虫（如 GPTBot、ClaudeBot）抓取页面
- **THEN** 文档大纲 SHALL 通过语义元素清晰可辨，每个 article 代表独立的内容单元

### Requirement: 清晰的 Heading 层级
页面 SHALL 保持严格的 heading 层级（h1 → h2 → h3），不跳级使用。

#### Scenario: Heading 层级验证
- **WHEN** AI 解析文章内容
- **THEN** 每个页面 SHALL 有且仅有一个 h1，内容层级 SHALL 从 h1 递增至 h2/h3，无跳级

### Requirement: Aria 标注
导航和交互元素 SHALL 包含适当的 ARIA 标签。

#### Scenario: 导航可访问性
- **WHEN** 屏幕阅读器或 AI 工具解析导航
- **THEN** <nav> 元素 SHALL 包含 aria-label，当前页面链接 SHALL 标注 aria-current="page"

### Requirement: 文章摘要元数据
文章页面 SHALL 在前端元数据中包含清晰的摘要描述。

#### Scenario: Meta description 提供摘要
- **WHEN** AI 工具提取文章摘要
- **THEN** <meta name="description"> 和 <meta property="og:description"> SHALL 包含文章的核心摘要

### Requirement: 纯净的 HTML 输出
页面 HTML SHALL 避免多余的嵌套和无关的标记，保持内容与表现的分离。

#### Scenario: 内容可提取性
- **WHEN** AI 工具提取文章正文
- **THEN** 正文内容 SHALL 集中于 <article> 元素内，无广告或无关标记干扰
