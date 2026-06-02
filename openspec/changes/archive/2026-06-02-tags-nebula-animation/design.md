## Context

标签页（/tags/）使用 Hugo 通用列表模板（layouts/_default/list.html），GSAP 已通过 CDN 加载，现有 gsap-animations.html 管理全站动效。需要添加星云粒子背景，仅作用于 tags 页面。

## Goals / Non-Goals

**Goals:**
- 标签页全屏背景星云粒子动画，GSAP 驱动
- 100-200 个发光粒子，缓慢流动形成星云效果
- 鼠标移动产生微妙视差/牵引效果
- 深色渐变背景衬托粒子发光
- 移动端降低粒子数（~60），尊重 prefers-reduced-motion
- 仅 tags 页面生效

**Non-Goals:**
- 不对首页列表页、文章页等其他页面生效
- 不引入 Canvas/WebGL（使用 DOM 元素 + GSAP）
- 不引入额外 npm 包或第三方库
- 不改变现有页面布局结构和内容可访问性

## Decisions

| 决策 | 选择 | 方案 | 理由 |
|---|---|---|---|
| 渲染方式 | DOM 元素 + GSAP | Canvas / WebGL | GSAP 已加载，DOM 方式与现有技术栈一致，无额外依赖。Canvas 方案需 requestAnimationFrame 循环，与 GSAP 引擎并行，增加复杂度 |
| 粒子数量 | 桌面端 150、移动端 60 | 统一 200 | 150 个 DOM 元素 GSAP 可流畅处理，移动端降级减少 repaint |
| 粒子生成 | JS 运行时动态创建 | HTML 硬编码 | JS 动态创建灵活控制数量和参数，不污染 HTML 结构 |
| 粒子运动 | GSAP `to()` 随机目标位置 + `repeat:-1,yoyo:true` | CSS animation | GSAP 提供缓动函数、时间线控制和鼠标交互集成能力 |
| 鼠标交互 | `mousemove` 事件驱动 `gsap.to()` 微调粒子位置 | - | GSAP 的 overwrite 和缓动效果比 CSS 更流畅自然 |
| 星云颜色 | HSL 蓝紫色系（200-320deg） | RGB 硬编码 | HSL 配合随机色相偏移产生丰富渐变效果 |
| 页面检测 | `document.body.classList.contains("list")` + URL 判断 | 仅 DOM 检测 | 现有 GSAP 架构已用 `isList` 标记，结合 `.page-header h1` 内容判断是否为 tags 页面 |
| 容器定位 | `.page-header` 下的绝对定位层 | body 背景 | 绝对定位在 header 下方作为背景层，z-index 控制内容在上层 |

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| 大量 DOM 粒子影响性能 | 移动端降至 60 粒子；GSAP 使用 `overwrite: "auto"` 避免同时动画过多属性；粒子无事件监听 |
| 与 PaperMod CSS 冲突 | 使用独立 `nebula-` 命名空间前缀 + `position: fixed` 全屏背景 |
| 阅读障碍 (prefers-reduced-motion) | `gsap.matchMedia()` 包裹，不匹配时完全跳过动画 |
| CDN GSAP 加载失败 | GSAP 可用性检查 `if (typeof gsap !== 'undefined')` |
