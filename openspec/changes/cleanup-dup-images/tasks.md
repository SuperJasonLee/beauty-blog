# Tasks: cleanup-dup-images

## Task 1: 删除孤立重复文件（medical-aesthetics-2026-05-31/）

删除以下 10 个文件（均为孤立文件，无 post 引用）：

```bash
rm static/images/posts/medical-aesthetics-2026-05-31/cn11_e39db85c75.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/art1_img2_e39db85c75.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/dermal_filler.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/beauty_treatment.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/art7_img2_b3a069a8b3.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/cn12_b3a069a8b3.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/art6_img2_08483c3867.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/cn13_08483c3867.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/art0_img2_6e000b1942.jpg
rm static/images/posts/medical-aesthetics-2026-05-31/cn10_6e000b1942.jpg
```

## Task 2: 删除 3 个孤立副本

```bash
rm static/images/eye-surgery-news/eye-surgery-news-20260601-001.jpg
rm static/images/posts/news-card.jpg
rm static/images/posts/clinic.jpg
```

## Task 3: 合并 Group 9 — 更新 hot post 路径

修改 2 个文件的 1 处路径：

- `content/zh-cn/posts/xiaohongshu-hot-may-2026.md:48`
  - `/images/posts/en-xiaohongshu-hot-may-2026/ipl_treatment.jpg`
  → `/images/posts/en-xiaohongshu-trends-2026/ipl_treatment.jpg`

- `content/en/posts/xiaohongshu-hot-may-2026.md:43`
  - `/images/posts/en-xiaohongshu-hot-may-2026/ipl_treatment.jpg`
  → `/images/posts/en-xiaohongshu-trends-2026/ipl_treatment.jpg`

## Task 4: 删除 Group 9 孤立副本

```bash
rm static/images/posts/en-xiaohongshu-hot-may-2026/ipl_treatment.jpg
```

## Task 5: 验证

- 运行 `python3 scripts/audit-dup-covers.py` 确认无 cover 重复
- 运行 Hugo 构建验证无 404
- `git diff --stat` 确认变更符合预期（14 个文件删除，2 个 post 修改）
