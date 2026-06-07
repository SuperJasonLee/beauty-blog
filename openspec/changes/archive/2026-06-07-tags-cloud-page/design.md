## Context

当前 `/tags/` 页面渲染为平面 `<ul class="terms-tags">` 列表，包含约 56 个标签，其中 41 个标签有 1 篇文章，9 个有 2 篇，6 个有 3 篇。页面使用 `layouts/_default/terms.html` 模板，GSAP 已通过 CDN 加载。

## Goals / Non-Goals

**Goals:**
- 标签字号根据 post count 自动缩放（count 1 → 基础字号，count 3 → 约 1.6x）
- 流式云状布局：标签在容器内自动换行排列，视觉上错落有致
- GSAP 滚动触发交错入场动画
- 悬停动效：scale 放大 + 高亮色
- 仅 `/tags/` 页面生效
- 响应式：移动端降低字号差距幅度

**Non-Goals:**
- 不使用 Canvas/WebGL 渲染（纯 DOM + CSS + GSAP）
- 不对单个标签页面（/tags/<name>/）做改变
- 不做强制排序——保持字母序排列（Alphabetical）

## Decisions

| 决策 | 选择 | 方案 | 理由 |
|---|---|---|---|
| 布局方式 | CSS `flex-wrap` 居中排列 | JavaScript 绝对定位计算 | flex-wrap 自动换行且易维护，无需 JS 计算碰撞检测 |
| 字号缩放 | `clamp()` CSS 函数 + data-* 属性 | 内联 style | `clamp(min, preferred, max)` 天然响应式，配合 count 映射 |
| 字号范围 | count1: `clamp(0.85rem, 2.5vw, 1rem)` → count3: `clamp(1.2rem, 4vw, 1.8rem)` | 固定比例 | 视觉层次清晰，最大/最小跨度 2x 以内保持可读 |
| 颜色变化 | count 越高颜色越亮/饱和 | 统一颜色 | 悬停时统一变色，不因 count 产生额外色差 |
| 标签背景 | 圆角背景块（pill 风格），半透明 | 纯文字 | pill 风格增加可点击区域和视觉重量 |
| 入场动画 | ScrollTrigger.batch 交错入场 | 一次性载入 | containers stretch 场景下 batch 更合适 |
| 悬停动画 | GSAP `to()` scale(1.15) + 背景高亮 | CSS transition | GSAP 缓动更平滑，与全站现有的 GSAP 悬停风格一致 |

## Risks / Trade-offs

| 风险 | 缓解措施 |
|---|---|
| 标签文字过长导致换行混乱 | `white-space: nowrap` 防止折行；长标签自然占用更多空间 |
| 移动端字号过小 | 使用 `clamp()` + 基础字号下限保证可读性 |
| `prefers-reduced-motion` | GSAP `matchMedia()` 包裹，不匹配时跳过动画 |
