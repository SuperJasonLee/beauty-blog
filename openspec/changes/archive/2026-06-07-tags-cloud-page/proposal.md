## Why

标签页（/tags/）目前以纯列表方式展示所有标签，视觉单调。标签云（Tag Cloud）通过不同字号反映标签热度，让访客一目了然地看到热门主题，提升页面浏览体验和信息传达效率。

## What Changes

- 将 `/tags/` 的平面标签列表改为标签云布局
- 每个标签的字号根据文章数量（count）自动缩放
- 标签呈流式排列，形成云状布局
- GSAP 驱动标签入场动画（滚动触发交错入场）
- 标签悬停动效增强
- 仅 `/tags/` 标签云页面生效，不影响单个标签页面

## Capabilities

### New Capabilities

- `tag-cloud-layout`: 标签云布局系统，包括 fontSize 按 count 缩放、流式云状排列、响应式适配

### Modified Capabilities

<!-- No existing capabilities to modify -->

## Impact

- `layouts/_default/terms.html`: 重构标签渲染部分，从 `<ul>` 改为标签云
- `layouts/partials/gsap-animations.html`: 添加标签云入场动画逻辑
- `assets/css/extended/custom.css`: 添加标签云样式（字号缩放、hover 效果、浮动布局）
