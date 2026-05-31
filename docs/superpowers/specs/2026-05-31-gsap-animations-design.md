# GSAP 全站动效系统设计

## 概述

为 Beauty Blog（Hugo + PaperMod）引入 GSAP 动画引擎，通过 ScrollTrigger 驱动的滚动动效和 GSAP 核心动画，提升全站交互体验。所有动效尊重 `prefers-reduced-motion`。

## 技术方案

### 依赖加载

- **GSAP + ScrollTrigger**: 通过 CDN 加载（`https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js` + `ScrollTrigger.min.js`）
- 在 `layouts/partials/extend_head.html` 中添加 CDN 脚本标签
- 无需 npm 安装，适合 Hugo 静态站构建流程

### 动效脚本

- 新建 `layouts/partials/gsap-animations.html` — 包含所有 GSAP 动效逻辑
- 动态监听 `document.fonts.ready` 确保字体加载完成后再初始化
- 使用 `gsap.matchMedia()` 包裹所有动效，以支持 `prefers-reduced-motion` 和响应式断点

### 脚本引入

- 在 `footer.html` 中 `extend_footer` 位置引入 `gsap-animations.html`
- 具体位置：在现有内联脚本之后、`</body>` 之前

## 动效详细设计

### 1. 导航栏智能隐藏/显示

| 属性 | 值 |
|------|-----|
| **目标元素** | `.header` |
| **触发方式** | ScrollTrigger 滚动方向检测 |
| **行为** | 向下滚动 > 50px 时隐藏（`y: -100%`），向上滚动时显示 |
| **动画参数** | `duration: 0.3, ease: "power2.out"` |
| **滚动容器** | 视口 |
| **无障碍** | 仅在桌面端生效（`min-width: 768px`），`prefers-reduced-motion` 时跳过 |

### 2. 导航菜单项悬浮动效

| 属性 | 值 |
|------|-----|
| **目标元素** | `#menu a` |
| **触发方式** | Hover（mouseenter / mouseleave） |
| **行为** | 伪元素宽度从 0 过渡到 100%（下滑线效果） |
| **实现** | GSAP `to()` 控制 `transform: scaleX()` 或宽度 |

### 3. 首页/列表页卡片滚动入场

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-card` |
| **触发方式** | ScrollTrigger.batch() |
| **入场动画** | `fromTo()`：`{ y: 60, opacity: 0 }` → `{ y: 0, opacity: 1 }` |
| **动画参数** | `duration: 0.6, ease: "power2.out", stagger: 0.1` |
| **触发位置** | `start: "top 90%"`, `once: true` |
| **特性** | 仅首次进入触发，不重复播放 |

### 4. 卡片悬停动效增强

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-card` |
| **触发方式** | Hover（mouseenter / mouseleave） |
| **行为** | 上移 `y: -6` + 阴影增强（比现有 CSS 更平滑） |
| **动画参数** | `duration: 0.3, ease: "power2.out"` |
| **注意** | 保留 `.post-card-image img` 的 CSS scale 切换（不需要 GSAP） |

### 5. 文章标题弹性入场

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-single .post-title` |
| **触发方式** | 页面加载（仅文章页） |
| **入场动画** | `from()`：`{ y: -30, opacity: 0, scale: 0.95 }` → 当前状态 |
| **动画参数** | `duration: 0.8, ease: "back.out(1.7)"` |
| **延迟** | `delay: 0.1` |

### 6. 特色图片缩放淡入

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-single .entry-cover img` |
| **触发方式** | 页面加载 |
| **入场动画** | `fromTo()`：`{ scale: 1.1, opacity: 0 }` → `{ scale: 1, opacity: 1 }` |
| **动画参数** | `duration: 0.8, ease: "power2.out"` |
| **延迟** | `delay: 0.2` |

### 7. 正文段落滚动入场

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-single .post-content > p, .post-single .post-content > h2, .post-single .post-content > h3` |
| **触发方式** | ScrollTrigger.batch() |
| **入场动画** | `from()`：`{ y: 30, opacity: 0 }` → 当前状态 |
| **动画参数** | `duration: 0.5, ease: "power1.out", stagger: 0.08` |
| **触发位置** | `start: "top 85%"`, `once: true` |
| **注意** | 广告段落、短代码容器等特殊元素跳过动画 |

### 8. 文章图片滚动展示

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-single .post-content img` |
| **触发方式** | ScrollTrigger |
| **入场动画** | `from()`：`{ scale: 0.95, opacity: 0, clipPath: "inset(5%)" }` |
| **动画参数** | `duration: 0.7, ease: "power2.out"` |
| **触发位置** | `start: "top 85%"`, `once: true` |

### 9. 标签交错入场

| 属性 | 值 |
|------|-----|
| **目标元素** | `.post-tags li` |
| **触发方式** | ScrollTrigger |
| **入场动画** | `from()`：`{ y: 20, opacity: 0 }` |
| **动画参数** | `duration: 0.4, ease: "power2.out", stagger: 0.05` |
| **触发位置** | `start: "top 90%"`, `once: true` |

### 10. 页脚淡入

| 属性 | 值 |
|------|-----|
| **目标元素** | `.footer` |
| **触发方式** | ScrollTrigger |
| **入场动画** | `from()`：`{ y: 30, opacity: 0 }` |
| **动画参数** | `duration: 0.6, ease: "power2.out"` |
| **触发位置** | `start: "top 95%"`, `once: true` |

### 11. 返回顶部按钮

| 属性 | 值 |
|------|-----|
| **目标元素** | `#top-link` |
| **当前行为** | 基于 `onscroll` 切换 `.hidden` class（保留） |
| **GSAP 增强** | 按钮出现时用 GSAP `to()` 做弹性缩放，消失时缩小淡出 |
| **点击行为** | 原生 `window.scrollTo({ top: 0, behavior: "smooth" })`，无需额外插件 |
| **动画参数** | 出现：`duration: 0.4, ease: "back.out(2)"`，消失：`duration: 0.2, ease: "power2.in"` |

### 12. 主题切换平滑过渡

| 属性 | 值 |
|------|-----|
| **实现** | CSS 层面添加 `transition: background-color 0.3s, color 0.3s` |
| **GSAP 角色** | 不使用 GSAP，仅靠 CSS transition 实现 |
| **原因** | 主题切换涉及大量 CSS 变量变化，CSS transition 更高效 |

## 代码结构

### 脚本加载方式

GSAP 脚本直接在 `footer.html` 中动效脚本之前加载，避免 `defer` 导致的执行时序问题：

```html
{{- if not (site.Params.disableGSAP | default false) }}
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
{{- end }}
{{- partial "gsap-animations.html" . }}
```

脚本放在 `</body>` 关闭前，加载不阻塞首屏渲染。`gsap-animations.html` 紧随其后，确保 GSAP 可用。

### gsap-animations.html 结构

```javascript
// 1. 注册 ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// 2. matchMedia 包装
let mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // 根据屏幕宽度设置不同的动画参数
  // A. 导航栏智能隐藏（桌面端）
  // B. 卡片滚动入场（列表页）
  // C. 文章页动效（文章页）
  // D. 页脚动效
  // E. 返回顶部增强
  // F. 悬停动效

  return () => { /* 清理 */ };
});

// 3. 菜单悬浮动效（独立于 matchMedia，始终需要）
```

### footer.html 引入位置

在现有内联脚本块之后，`</body>` 之前添加：

```html
{{- partial "gsap-animations.html" . }}
```

## 性能考量

- **ScrollTrigger.batch()** 代替逐个创建 Trigger，减少实例数量
- **once: true** 确保动效只执行一次，不浪费性能
- **gsap.matchMedia()** 在匹配条件不满足时自动清理所有动效
- 移动端（< 768px）降低 stagger 值和动效幅度
- 所有动效使用 `transform` 和 `opacity`，避免触发 Layout

## 响应式策略

| 断点 | 调整内容 |
|------|---------|
| `min-width: 768px` | 全量动效 |
| `max-width: 767px` | 卡片 stagger 减半、段落入场简化、导航隐藏禁用 |
| `prefers-reduced-motion: reduce` | 所有 GSAP 动效跳过 |

## 风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| CDN 加载失败 | 使用 `defer` 属性不影响页面渲染；JS 中做 `if (typeof gsap === 'undefined')` 保护 |
| 与现有 JS 冲突 | 现有 JS 为原生内联脚本，GSAP 在独立作用域运行，无冲突风险 |
| SEO 影响 | GSAP 不影响 DOM 内容，仅操作样式，无 SEO 问题 |
| 构建流程变更 | 无需变更构建流程，CDN 加载不涉及 npm/webpack |
