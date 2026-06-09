## 目标

清理 static/images/ 下 9 组重复图片，涉及 14 个冗余文件和 2 个 post 路径修改。

## 数据来源

审计脚本输出（2026-06-09）：

- 135 张图片文件，9 组重复，22 个冗余文件（含同 post 内的孤立副本）
- 6 组为纯孤立文件（无 post 引用），3 组涉及跨 post 引用

## 重复分组

### 类型 A：孤立重复（10 个文件，全部删除）

均位于 `static/images/posts/medical-aesthetics-2026-05-31/`，无任何 post 引用：

| # | 文件 1 | 文件 2 | 大小 |
|---|--------|--------|------|
| 1 | `cn11_e39db85c75.jpg` | `art1_img2_e39db85c75.jpg` | 361,084 B |
| 2 | `dermal_filler.jpg` | `beauty_treatment.jpg` | 122,925 B |
| 3 | `art7_img2_b3a069a8b3.jpg` | `cn12_b3a069a8b3.jpg` | 104,447 B |
| 5 | `art6_img2_08483c3867.jpg` | `cn13_08483c3867.jpg` | 86,611 B |
| 7 | `art0_img2_6e000b1942.jpg` | `cn10_6e000b1942.jpg` | 62,010 B |

### 类型 B：有引用 + 孤立副本（3 组）

| 组 | 保留（被引用） | 删除（孤立） | 引用 post |
|---|----------------|---------------|-----------|
| 4 | `eye-surgery-news-20260601-cover.jpg` | `eye-surgery-news-20260601-001.jpg` | 2 个 post（中英各 1） |
| 6 | `aesthetic-news-card.jpg` | `news-card.jpg` | 1 个 post（en） |
| 8 | `aesthetic_clinic.jpg` | `clinic.jpg` | 2 个 post（中英各 1） |

### 类型 C：跨目录重复（1 组，需合并路径）

| 文件 | 路径 A（保留） | 路径 B（删除并更新引用） |
|------|---------------|--------------------------|
| `ipl_treatment.jpg` | `en-xiaohongshu-trends-2026/` | `en-xiaohongshu-hot-may-2026/` |

引用路径 A（保留，不变）：
- `content/zh-cn/posts/xiaohongshu-trends-2026.md:44`
- `content/en/posts/xiaohongshu-trends-2026.md:31`

引用路径 B（需更新）：
- `content/zh-cn/posts/xiaohongshu-hot-may-2026.md:48`
  - 旧：`/images/posts/en-xiaohongshu-hot-may-2026/ipl_treatment.jpg`
  - 新：`/images/posts/en-xiaohongshu-trends-2026/ipl_treatment.jpg`
- `content/en/posts/xiaohongshu-hot-may-2026.md:43`
  - 旧：`/images/posts/en-xiaohongshu-hot-may-2026/ipl_treatment.jpg`
  - 新：`/images/posts/en-xiaohongshu-trends-2026/ipl_treatment.jpg`

## 风险评估

- **数据丢失风险**：低 — 所有被删除文件要么是孤立文件，要么与保留文件 sha256 完全一致
- **构建风险**：极低 — Hugo 构建不会受影响，路径修改正确则无 404
- **回滚**：所有删除文件均可从 git 历史恢复
