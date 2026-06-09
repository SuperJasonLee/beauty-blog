## Why

通过审计发现 9 组重复图片（14 个冗余文件），涉及孤立文件堆积和跨 post 图片路径冗余。冗余图片增加仓库体积、造成维护困惑（同一图片存在两个副本导致更新时只改一个），且孤立文件是历史批量操作遗留物。

## What Changes

- 删除 10 个 `medical-aesthetics-2026-05-31/` 下的孤立重复文件
- 删除 3 个被其他 post 引用的孤立副本（`eye-surgery-news-20260601-001.jpg`、`news-card.jpg`、`clinic.jpg`）
- 合并 Group 9：`ipl_treatment.jpg` 跨两个 post 目录重复，统一指向 `en-xiaohongshu-trends-2026/` 路径

## Capabilities

### New Capabilities

<!-- 无新增能力 -->

### Modified Capabilities

- `dup-images-cleanup`: 新增审计脚本（可选），用于 CI 防止重复图片回流

## Impact

- 删除 14 个图片文件（`static/images/` 下）
- 修改 2 个 post 文件的图片路径（`xiaohongshu-hot-may-2026.md` 中英各 1 处）
- 无功能变化，纯清理操作
