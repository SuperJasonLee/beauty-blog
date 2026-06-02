## Why

标签页（/tags/）目前为静态列表页，缺少视觉吸引力。添加 GSAP 驱动的星云粒子背景动画可以提升页面沉浸感，增强品牌调性，让网站在同类医疗美容博客中脱颖而出。星云视觉语言与"美"和"科技"的定位高度契合。

## What Changes

- 在标签页添加全屏星云粒子背景动画（GSAP 驱动）
- 粒子系统：数百个大小不一的发光粒子，形成缓慢流动的星云效果
- 鼠标交互：粒子对鼠标移动产生微妙响应（视差/吸引效果）
- CSS 支持：深色渐变背景 + 粒子半透明发光效果
- 性能优化：移动端降低粒子数量，尊重 prefers-reduced-motion
- 仅标签页生效，不影响其他页面

## Capabilities

### New Capabilities

- `nebula-animation`: GSAP 驱动的星云粒子动画系统，包含粒子渲染、运动逻辑、鼠标交互和响应式降级

### Modified Capabilities

<!-- No existing capabilities to modify -->

## Impact

- `layouts/_default/list.html`: 标签页模板需添加粒子容器（条件渲染，仅在 tags 页面）
- `layouts/partials/gsap-animations.html`: 添加星云动画逻辑
- `assets/css/extended/custom.css`: 添加粒子容器样式
- 性能: 首屏不阻塞，动画延迟初始化；移动端降级粒子数
