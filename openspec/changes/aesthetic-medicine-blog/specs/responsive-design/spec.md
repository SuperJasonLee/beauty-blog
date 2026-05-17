## ADDED Requirements

### Requirement: 移动端适配
站点 SHALL 在移动端、平板和桌面端均提供良好的阅读体验。

#### Scenario: 响应式布局
- **WHEN** 用户在手机（<768px）、平板（768-1024px）或桌面（>1024px）设备上浏览
- **THEN** 布局 SHALL 自动适配，文字大小、间距、图片尺寸 SHALL 在不同断点下合理显示

#### Scenario: 触摸交互
- **WHEN** 用户在触摸设备上操作
- **THEN** 所有交互元素（按钮、链接、搜索）SHALL 有足够大的触摸目标（≥44px）

### Requirement: 图片响应式
图片 SHALL 使用响应式技术（srcset、sizes、loading="lazy"）进行优化。

#### Scenario: 响应式图片加载
- **WHEN** 用户使用不同分辨率设备浏览
- **THEN** 图片 SHALL 根据视口宽度加载适当分辨率的版本

#### Scenario: 懒加载
- **WHEN** 用户滚动页面
- **THEN** 视口外的图片 SHALL 使用 loading="lazy" 延迟加载

### Requirement: 字体与排版
排版 SHALL 针对中文阅读优化，使用合适的字体栈和行高。

#### Scenario: 中文排版
- **WHEN** 用户阅读文章
- **THEN** 正文字体 SHALL 优先使用系统中文字体（PingFang SC, Microsoft YaHei），行高 1.8，字号 16-18px
