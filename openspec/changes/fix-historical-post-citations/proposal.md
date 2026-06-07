## Why

历史 POST 全量诊断（13 篇 zh-cn + 12 篇 en）发现系统性问题：**源数据真实存在但被生成流程丢弃**，导致大量"裸数字"与"无源博主名"留在线上。这对 YMYL（医疗类）站点是严重风险，会触发 Google Helpful Content 降权，并让生成式引擎（ChatGPT/Perplexity/Gemini）拒绝引用，直接断送 GEO 流量。

具体表现：
- 3 篇小红书趋势文充斥"上海九院 X 医生 + 精确点赞数 + 增长 %X" 但 0 个 URL
- 5 篇月度新闻汇总缺脚注或脚注无 URL（其中 `medical-aesthetics-news-may-31-2026` 在 `web-articles/` 中有 8 条真实 Yicai 源但 0 引用回灌）
- 2 篇眼整形自动生成文：1 篇链接堆砌可读性极差、1 篇文献引用无 PMID/DOI
- 17 篇 `lastReviewed` 全部为 `2026-05-27`（批量改痕迹）
- news/xhs 全部缺 FAQ 短代码（GEO 抽取入口）

## What Changes

- **回灌引用**：将 `web-articles/<topic>/articles.json`、`data/crawled/<topic>/*.json` 中的真实 URL 回灌为脚注或正文链接
- **删除/标注无源数据**：找不到源的博主名、点赞数、百分比，统一删除或改为"编辑团队估算（无原始数据）"
- **补 FAQ**：为所有 news/XHS POST 补 `{{< faq >}}` 短代码（3-5 条/篇）
- **统一 frontmatter**：补 `reviewer` 字段；`lastReviewed` 按真实修订时间设置；补 `translations` 双向链接
- **修断链图片**：`medical-aesthetics-news-may-31-2026` 等的 `images/posts/...` 改为 `/images/posts/...`
- **重写 2 篇**：`aesthetic-news-may-2026.md`（76 行过短）和 `eye-surgery-news-20260606.md`（链接堆砌）按 SOP 重做
- **新增 audit 脚本**：`scripts/audit-posts.py` 静态检查 POST 引用完整性、frontmatter 规范、图片路径，输出 JSON 报告
- **publishing workflow 更新**：发布前 checklist 加入 audit 脚本运行
- **BREAKING**: `xiaohongshu-may-2026-live.md` 的伪"实时数据"部分必须删除（含编造的博主名 + 假百分比），保留经核实的趋势分析

## Capabilities

### New Capabilities
- `post-citation-integrity`: 所有正文统计/事实必须可追溯到脚注 URL 或被显式标注为"编辑团队观察"；audit 脚本守门

### Modified Capabilities
（无 — 现有 spec 中没有覆盖 POST 内容质量的）

## Impact

**受影响代码 / 内容：**
- `content/zh-cn/posts/*.md`（13 篇）+ `content/en/posts/*.md`（12 篇）
- `scripts/audit-posts.py`（新建）
- `package.json`（新增 `audit:posts` script）
- `docs/post-publishing-workflow.md`（§8 checklist 增加 audit 步骤）
- `static/images/posts/medical-aesthetics-2026-05-31/`（路径前缀修正不涉及移动文件）

**数据源依赖：**
- `web-articles/medical-aesthetics-2026-05-31/articles.json`（已有 14 条 Yicai/ELLE 真实 URL）
- `data/crawled/eye-surgery-news/`（已有 5 份带 PMID 的 PubMed 数据）
- 部分 XHS 数据无原始源 → 需用 `opencli rednote search` 补抓或删除

**风险：**
- XHS 三篇删除"假数据"后字数会显著下降，可能影响排名 → 用真实趋势分析 + opencli 补抓数据补足
- `lastmod` 改动会触发 sitemap 全量更新 → Google 重新抓取（短期波动可接受）

**不影响：**
- 已完成 OpenSpec change（aesthetic-medicine-blog、tags-cloud-page 等）
- 主题 / 模板 / JSON-LD（已生成正确，问题在内容侧）
- 自动发布脚本（pipeline 本身正确，问题在 LLM 合成阶段，下次跑前已修）
