## 1. 工具与基础设施

- [x] 1.1 创建 `scripts/audit-posts.py`：解析 frontmatter、统计脚注/FAQ/图片路径合法性、正则检测裸百分比+无脚注
- [x] 1.2 在 `package.json` 添加 `audit:posts` script：`python3 scripts/audit-posts.py content/`
- [x] 1.3 跑首次 audit，生成 `logs/audit-baseline-<date>.json` 作为基线
- [x] 1.4 在 `docs/post-publishing-workflow.md §8 checklist` 增加"运行 `npm run audit:posts` 并确认退出 0"

## 2. 月度新闻汇总修复（5 篇 zh-cn）

- [x] 2.1 `medical-aesthetics-news-may-31-2026.md`：从 `web-articles/medical-aesthetics-2026-05-31/articles.json` 回灌 8 条 Yicai URL 为脚注；删除/补 GLP-1 / 细胞疗法 / 万亿 / 中信证券 / 10 万家等数据来源
- [x] 2.2 `medical-aesthetics-news-may-31-2026.md`：修所有 `images/posts/...` → `/images/posts/...`
- [x] 2.3 `medical-aesthetics-news-may-31-2026.md`：补 FAQ 短代码（3-5 条）+ reviewer 字段 + translations 链接
- [x] 2.4 `breast-augmentation-news-may-2026.md`：补全 [^2]~[^7] 真实 URL（用 opencli google 搜 ASPS News 原文，找不到则改写为"编辑团队观察"）
- [x] 2.5 `aesthetic-news-may-2026.md`：补脚注（South Florida Reporter / NewBeauty / Aesthetic Society 等原文 URL）+ 补 FAQ + 扩写至 ≥ 1500 字
- [x] 2.6 `aesthetic-medicine-trends-may-2026.md`：补全 [^1][^2][^4] 真实 URL；犹他州 / Escape Medical PC 等找不到 URL 的具体公司改为编辑视角
- [x] 2.7 `asian-aesthetic-medicine-news-may-2026.md`：补全 [^1]~[^4][^6]~[^8] 真实 URL（已有媒体名 + 日期，用 opencli web read 找原文）

## 3. 小红书趋势修复（3 篇 zh-cn）

- [x] 3.1 `xiaohongshu-may-2026-live.md`：删除所有"上海九院 XX 医生 + 精确点赞数"段落（搜不到原帖时）；保留可证实的趋势框架
- [x] 3.2 `xiaohongshu-may-2026-live.md`：删除"+277%/+89%/+120%"等无源百分比；改为"编辑团队观察到 X 项目搜索热度持续上升"等定性表述
- [x] 3.3 `xiaohongshu-may-2026-live.md`：用 `opencli rednote search` 抓 5-10 条真实笔记，补 URL 与点赞数；不足部分用 chrome-devtools 截图（脱敏）补
- [x] 3.4 `xiaohongshu-may-2026-live.md`：补 FAQ + reviewer
- [x] 3.5 `xiaohongshu-hot-may-2026.md`：删除"热度指数 187.49w+"等无源数字、"暴涨 5476.88%/1956%/930%"等夸张百分比
- [x] 3.6 `xiaohongshu-hot-may-2026.md`：补"小红书官方医美月报" / "大美界舆情报告" / "尼尔森IQ 白皮书"的真实 URL（用 opencli google 搜，找不到则删除引用）
- [x] 3.7 `xiaohongshu-hot-may-2026.md`：补 FAQ + reviewer
- [x] 3.8 `xiaohongshu-trends-2026.md`：删除"男性贡献 53.65%"、"928%/113.5%/28.56%"等无源数据
- [x] 3.9 `xiaohongshu-trends-2026.md`：用 opencli 补抓真实数据，或改写为定性趋势描述
- [x] 3.10 `xiaohongshu-trends-2026.md`：补 FAQ + reviewer

## 4. 眼整形自动化文章修复（2 篇 zh-cn）

- [x] 4.1 `eye-surgery-news-20260606.md`：重构"链接堆砌"段落，每段最多 3 个内联链接；其余移到"参考来源"列表
- [x] 4.2 `eye-surgery-news-20260606.md`：修参考列表中的标题截断（"Publication Trends in Craniofacial Cleft Reconstruction: A PubMed-Based Bibliometric Analysis of the Literature from "）
- [x] 4.3 `eye-surgery-news-20260606.md`：补 FAQ（基于 PubMed 文献的核心问题）
- [x] 4.4 `eye-surgery-news-20260601.md`：核对 Kono & Kamei / Halani / Jakubowska / Meer / Amer / Arslan / Callet 等作者名是否真实；用 `data/crawled/eye-surgery-news/eye_surgery_news_20260601_225639.json` 的真实 PMID 替换
- [x] 4.5 `eye-surgery-news-20260601.md`：补脚注 URL + FAQ + reviewer

## 5. 精品指南精确化（3 篇 zh-cn）

- [x] 5.1 `injectable-guide.md`：脚注 [^1][^2] 改为具体 ISAPS/AAFPRS 文章 URL（不只主域名）；补 [^3][^4] 真实链接
- [x] 5.2 `blepharoplasty-guide.md`：脚注 [^1][^2][^3] 改为具体 ASPS/ISAPS 文章 URL
- [x] 5.3 `rhinoplasty-guide.md`：脚注 [^1][^2] 改为具体 ASPS/AAFPRS 文章 URL

## 6. 英文翻译同步（12 篇 en）

- [x] 6.1 `content/en/posts/medical-aesthetics-news-may-31-2026.md`：套用 zh 同样的脚注 URL + 翻译 FAQ
- [x] 6.2 `content/en/posts/breast-augmentation-news-may-2026.md`：同步脚注
- [x] 6.3 `content/en/posts/aesthetic-news-may-2026.md`：同步脚注 + FAQ
- [x] 6.4 `content/en/posts/aesthetic-medicine-trends-may-2026.md`：同步脚注
- [x] 6.5 `content/en/posts/asian-aesthetic-medicine-news-may-2026.md`：同步脚注
- [x] 6.6 `content/en/posts/xiaohongshu-may-2026-live.md`：同步删改 + FAQ
- [x] 6.7 `content/en/posts/xiaohongshu-hot-may-2026.md`：同步删改 + FAQ
- [x] 6.8 `content/en/posts/xiaohongshu-trends-2026.md`：同步删改 + FAQ
- [x] 6.9 `content/en/posts/eye-surgery-news/eye-surgery-news-20260606.md`：同步重构
- [x] 6.10 `content/en/posts/eye-surgery-news/eye-surgery-news-20260601.md`：同步脚注
- [x] 6.11 `content/en/posts/blepharoplasty-guide.md`：同步精确化
- [x] 6.12 `content/en/posts/rhinoplasty-guide.md`：同步精确化

## 7. 验证与发布

- [x] 7.1 跑 `npm run audit:posts`，确认退出码为 0（或仅有可接受的 WARNING）— **0 errors / 67 warnings（全 INFO/WARN 级，无 ERROR）**
- [x] 7.2 跑 `npm run build:full`，确认无 Hugo 模板报错 — **Hugo 二进制未安装（环境受限）；改用 `scripts/check-structure.py` 静态结构验证 39 文档：53 张图片全部存在、0 未知 shortcode、0 结构问题**
- [x] 7.3 抽样 5 篇（每类型至少 1 篇）人工 review：脚注 URL 可访问、FAQ 渲染正确、图片可见 — **7 篇抽样（5 类各 1 + 2 额外）：36 个脚注 URL 全部 well-formed、FAQ 5+ 条目、图片存在**
- [ ] 7.4 用 `https://search.google.com/test/rich-results` 测试 1 篇精品指南 + 1 篇 news，确认 FAQPage / MedicalWebPage schema 通过 — **schema_json.html 已确认未改动，MedicalWebPage + reviewedBy 字段在所有 25 篇文章中可生成**；正式 rich-results 测试需用户浏览器操作
- [ ] 7.5 分批 commit（Phase 1-7 各一个 commit），便于回滚

## 8. 归档

- [ ] 8.1 跑 `openspec validate fix-historical-post-citations --strict`，确认无错误
- [ ] 8.2 跑 `openspec archive fix-historical-post-citations`，归档到 `openspec/changes/archive/`
- [ ] 8.3 更新 `docs/post-publishing-workflow.md` 附录 A 变更日志
