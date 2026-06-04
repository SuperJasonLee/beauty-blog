# Post 发布标准流程（SOP）

> **最后更新：** 2026-06-04
> **适用站点：** beauty-blog（https://beauty-blog.cloud-ip.cc/）
> **状态：** 与 `layouts/partials/templates/schema_json.html`、`docs/image-guidelines.md`、`scripts/crawl-eye-surgery-news/` 保持同步
> **语言：** 中文（站点默认内容语言）

---

## 0. 文档说明

### 0.1 目的
沉淀本博客从"选题→发布"的可复用流水线，统一 4 类 post（精品指南 / 月度新闻汇总 / 小红书趋势 / 垂类新闻 pipeline）的发布质量，使新成员能 1 次 walk-through 即可独立发布。

### 0.2 读者
- **新成员**：顺序读完本文件，照 §7 walk-through 演练一遍
- **熟练工**：直接看 §8 发布前 checklist
- **新类型探索**：从 §1 决策点出发，跳到对应小节

### 0.3 术语表
| 术语 | 含义 |
|---|---|
| **post** | Hugo content 中的单篇文章（双语成对） |
| **draft** | 草稿状态（`draft: true`，`hugo` 默认不构建） |
| **featured image** | OG/Twitter 分享主图，对应 frontmatter `featuredImage` |
| **card 图** | 列表页卡片缩略图 |
| **inline 图** | 文章内部配图（`{{< figure >}}` 短代码） |
| **E-E-A-T** | Google 搜索质量框架：Experience / Expertise / Authoritativeness / Trustworthiness |
| **GEO** | Generative Engine Optimization：面向 ChatGPT / Perplexity / Gemini 等生成式引擎的优化 |
| **YMYL** | Your Money or Your Life：医疗类内容，Google 审核最严 |
| **JSON-LD** | 结构化数据（schema.org），用于富文本结果（Rich Results） |

### 0.4 Post 4 种类型一览

| 类型 | 典型代表 | 数据源 | 长度 | 频率 |
|---|---|---|---|---|
| 精品指南 | blepharoplasty-guide, rhinoplasty-guide, injectable-guide | 学术 / 权威机构 | 5000+ 字 | 季度或半年 |
| 月度新闻汇总 | medical-aesthetics-news-may-31-2026, breast-augmentation-news-may-2026 | 多源聚合 | 2000-3000 字 | 月度 |
| 小红书趋势 | xiaohongshu-trends-2026, xiaohongshu-hot-may-2026, xiaohongshu-may-2026-live | XHS 平台 + 实时数据 | 1500-2500 字 | 月度 / 不定期 |
| 垂类新闻 pipeline | eye-surgery-news-20260601 | opencli 自动抓取（PubMed/知乎/Google） | 2000-3000 字 | 不定期 |

---

## 1. 全局流程图

```
            ┌──────────────────────┐
            │  §2 内容搜索与调研    │  ← 决定 Post 类型
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  §3 配图素材下载优化  │  ← 真实照片优先
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  §4 文章生成（中文）  │  ← 先写中文，draft
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  §5 中英文翻译        │  ← EN 后译
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  §6 SEO & GEO 优化    │  ← frontmatter + JSON-LD + 短代码
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  §8 发布前 checklist  │  ← 15-20 项逐一打钩
            └──────────┬───────────┘
                       ▼
                 `draft: false`
                    发布
```

**决策点：** §2 结束时需明确"我要发的是哪一类 post"，后续每个阶段的"按类型分小节"才能精准对齐。

---

## 2. 阶段一：内容搜索与调研

### 2.1 通用搜索规则

**信息源白名单（按权威性排序）：**

1. **学术原始文献**：PubMed、CNKI、arXiv
2. **权威机构**：ASPS（美国整形外科医师协会）、ISAPS（国际整形美容外科协会）、AAFPRS、FDA、NMPA（国家药品监督管理局）
3. **行业新闻**：Reuters Health、Dermatology Times、PubMed News、行业垂直媒体
4. **专业社区**：知乎专业回答（带文献引用的）、ResearchGate
5. **平台原生数据**：小红书（rednote 适配器）、微博热搜（仅做趋势参考）

**禁止引用：** 纯营销 PR 稿、SEO 农场、未注明来源的"专家说"。

**搜索工具：** `opencli` 已内置 136 个站点适配器。常用命令格式：

```bash
opencli <adapter> <command> [args] -f json
```

**输出物保存：**
- 每次调研产物落到 `data/crawled/<topic-slug>/<YYYYMMDD_HHMMSS>.json`（与现有 `eye-surgery-news` pipeline 一致）
- 包含字段：`source_url`, `source_name`, `title`, `date`, `content_markdown`, `image_urls`, `crawled_at`

### 2.2 按类型分小节

#### 2.2.1 精品指南

**目标：** 达到 ASPS/ISAPS 同行评议级别的科普深度，YMYL 合规。

**搜索源：**
```bash
# PubMed 学术文献
opencli pubmed search "blepharoplasty AND Asian patients" --limit 20 -f json

# Google Scholar
opencli google-scholar search "double eyelid surgery technique review" --limit 15 -f json

# 权威机构指南
opencli web read --url "https://www.plasticsurgery.org/cosmetic-procedures/eyelid-surgery" -f json
opencli web read --url "https://www.isaps.org/discover/about-isaps/global-statistics/" -f json
```

**调研清单（每篇指南必查）：**
- [ ] 最新 1-2 篇 Cochrane / 高影响因子综述
- [ ] ASPS / ISAPS 当年统计数据
- [ ] FDA / NMPA 对相关设备/材料的批准信息
- [ ] 中文学术文献 1-2 篇（用 CNKI 适配器）
- [ ] 知乎或专业社区对争议性话题的讨论

**输出物：** `data/crawled/<topic>-guide/<YYYYMMDD_HHMMSS>.json` + 笔记 `web-articles/<topic>/<paper>.md`

#### 2.2.2 月度新闻汇总

**目标：** 当月医美行业全景式观察，多源拼图。

**搜索源：**
```bash
# 多源并行（参考 crawl-eye-surgery-news 模板）
opencli google search "aesthetic medicine news 2026 May" --limit 10 -f json
opencli reuters search "plastic surgery" --limit 10 -f json
opencli baidu-scholar search "医美 行业 2026" --limit 10 -f json
opencli pubmed search "aesthetic medicine May 2026" --limit 15 -f json
```

**去重规则：** 同一新闻事件出现在 3+ 源，视为"主流关注"，优先采用；只在 1 源出现但来源权威，保留为"长尾"。

**时间窗口：** 上一自然月 1 日到最后一日。

**输出物：** `data/crawled/news/<YYYY-MM>-news.json`，按 4 个维度分类（政策/技术/市场/消费）。

#### 2.2.3 小红书趋势

**目标：** 平台原生数据 + 真实用户讨论。

**搜索源：**
```bash
# XHS 平台（rednote 适配器）
opencli rednote search "医美 趋势" --limit 30 -f json
opencli rednote search "双眼皮 修复" --limit 20 -f json

# 平台榜单 / 实时
opencli rednote hot --category "aesthetic" --limit 50 -f json
```

**人工补充：** 平台搜索结果需人工浏览热门笔记补充语境（机器抓取不返回完整评论）。

**去重与排序：** 按点赞数 + 收藏数排序，TOP10 入选。

**输出物：** `data/crawled/xhs/<YYYY-MM>/trends.json` + `data/crawled/xhs/<YYYY-MM>/top-posts.md`（人工整理的笔记标题 + 关键评论摘要）

#### 2.2.4 垂类新闻 pipeline（自动化）

**适用场景：** 固定话题（如"眼部整形"）的常态化跟踪。

**现成 pipeline：** `scripts/crawl-eye-surgery-news/`

```bash
# 一键跑完 crawl → image download → post generation
npm run crawl:eye-news

# 单独跑某一步（debug 用）
cd scripts/crawl-eye-surgery-news
python crawler.py           # 只爬
python image_downloader.py  # 只下图片
python post_generator.py    # 只生成 draft
```

**现有数据源配置**（`scripts/crawl-eye-surgery-news/crawler.py` 中 `SOURCES` 列表）：
- PubMed
- 知乎
- Google

**输出物：**
- 中间数据：`data/crawled/eye-surgery-news/<ts>.json` + `crawled_urls.json`（去重）
- 图片：`static/images/eye-surgery-news/eye-surgery-news-<date>-<NNN>.<ext>`
- Draft：`content/zh-cn/posts/eye-surgery-news/<slug>.md` + `content/en/posts/eye-surgery-news/<slug>.md`

**新建垂类 pipeline 的步骤：**
1. 复制 `scripts/crawl-eye-surgery-news/` 到 `scripts/crawl-<topic>-news/`
2. 改 `SOURCES`、关键词、输出目录
3. 在 `package.json` 添加 `crawl:<topic>-news` npm script
4. 改 `post_generator.py` 的 `build_zh_post` / `build_en_post` 模板（参考 §4.4.4）

---

## 3. 阶段二：配图素材下载与优化

### 3.1 通用图片规范

**完整规范见 [`docs/image-guidelines.md`](./image-guidelines.md)。摘要：**

| 类型 | 尺寸 | 命名 |
|---|---|---|
| featuredImage | 1200×630（16:9） | `<slug>-featured.jpg` |
| card 图 | 800×450（16:9） | `<slug>-card.jpg` |
| 文章内配图 | 1000×600（5:3） | `<slug>-<N>.jpg` |

- 格式：JPEG（照片）/ PNG（图形）
- 单张 ≤ 500KB
- **来源白名单：** Unsplash, Pexels, Pixabay

**存储路径：**
- 手工挑选：`static/images/posts/<slug>-*`
- 爬取图片：`static/images/<topic-dir>/<descriptive>.jpg`

### 3.2 按类型分小节

#### 3.2.1 精品指南

**图片来源：** Unsplash / Pexels（搜索关键词：`medical procedure`, `surgery`, `aesthetic`, `clinic`）

**数量：** 3-5 张内嵌图 + 1 张 featured + 1 张 card

**筛选原则：**
- ✅ 真实场景、真实人物、专业场景
- ❌ AI 生成图（commit `dc2b659`, `dc5f84b`, `c417833` 已替换所有 AI 图为真实图）
- ❌ 过于血腥或术后特写
- ❌ 营销水印

#### 3.2.2 月度新闻汇总

**图片来源：**
1. 优先：爬取文章中的实拍图（由 `image_downloader.py` 自动下载到 `static/images/<topic-dir>/`）
2. 兜底：Unsplash 关键词（`clinic`, `medical team`, `technology`, `trends`）

**数量：** 4-6 张内嵌图（每章节一张）+ featured + card

**注意事项：** 爬取的图片需检查版权（仅抓取 CC0 / 政府机构 / 医院官网图），并在文末"参考来源"中注明。

#### 3.2.3 小红书趋势

**图片来源：**
1. 真实 XHS 笔记截图（首选）—— 用 `chrome-devtools_take_screenshot` 或 `opencli browser screenshot` 抓取
2. XHS 平台官方宣传图（次选）
3. Unsplash 兜底（关键词：`beauty`, `social media`, `trends`）

**数量：** 5-8 张（每条趋势配 1-2 张）

**注意事项：**
- XHS 截图**必须脱敏**：打码用户 ID、头像、违规内容
- 截图尺寸统一调整为 800 宽
- 仅做"事实性引用 + 评论"，不做营销搬运

#### 3.2.4 垂类新闻 pipeline

**全自动：** `image_downloader.py` 处理。

**人工 review：** 跑完 pipeline 后人工检查 `static/images/<topic-dir>/`，剔除：
- 损坏的 / 缩略图占位符
- 明显无关的图
- 版权可疑的图

### 3.3 图片优化 SOP

```bash
# macOS 自带 sips 工具（项目已用，commit 5aee372）
# 调整尺寸
sips -Z 1200 input.jpg --out output-1200.jpg
sips -Z 600 input.jpg --out output-600.jpg

# 转 JPEG 85% 质量
sips -s format jpeg -s formatOptions 85 input.png --out output.jpg

# 批量脚本（参考 scripts/ 下历史图片优化脚本）
for f in static/images/posts/<slug>/*.jpg; do
  sips -Z 1200 "$f" --out "$f.tmp" && mv "$f.tmp" "$f"
done
```

**验收标准：**
- 每张图 ≤ 500KB
- 尺寸符合 §3.1 表格
- 视觉清晰、无水印

---

## 4. 阶段三：文章生成

### 4.1 通用结构模板

```
[导言 / Introduction]              ← 1 段，≤ 200 字，点题
[正文分章节 H2]                     ← 3-6 个章节，H2 / H3 嵌套
  ├─ 每个 H2 章节开头 1 段引子
  ├─ 主体内容（含数据 / 引用 / 配图）
  └─ 必要时用 alert 短代码提示风险
[结语 / Conclusion]                 ← 1 段，总结 + 给读者建议
---
参考来源（脚注 [^N] 或末尾 References）   ← 学术/权威源
免责声明（医疗 disclaimer 必含）          ← 法律风险隔离
```

### 4.2 frontmatter 模板

**最小可用集（所有 post 必填）：**
```yaml
---
title: "..."                       # ≤ 60 字符，含主关键词
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
description: "..."                 # 120-160 字符，含主关键词 + 价值主张
categories: ["..."]                # 单分类
tags: ["...", "..."]               # 3-6 个
keywords: ["...", "..."]           # 5-8 个，SEO 用
draft: true                        # 发布前必为 true
featuredImage: "/images/posts/<slug>-featured.jpg"
author: "Beauty-Blog 医学审核团队"   # 默认值
lastReviewed: "YYYY-MM-DD"          # E-E-A-T 关键字段
medicalAudience: "Patient"          # Patient / Professional
translations:                       # 双语互链
  - "/en/posts/<path>/<slug>"
---
```

**可选字段（按类型使用）：**
```yaml
reviewer: "执业医师审核"            # 精品指南必填
images: ["img1.jpg", "img2.jpg"]  # 列表页多图（可选）
series: ["..."]                    # 系列文章分组
```

**字段详解与示例见 §6.1 SEO 清单。**

### 4.3 短代码使用约定

| 短代码 | 用途 | 必用场景 |
|---|---|---|
| `{{< medical-disclaimer />}}` | 顶部免责声明 | **所有医疗类 post 必用** |
| `{{< figure src="..." title="..." >}}` | 图片 + 图注 | 内嵌图统一格式 |
| `{{< alert "warning" >}}` ... `{{< /alert >}}` | 风险/警告提示块 | 涉及风险/并发症/价格/术后 |
| `{{< faq >}}` ... `{{< /faq >}}` | FAQ 列表 + JSON-LD | 精品指南、月度新闻汇总 |
| `{{< term "..." >}}` | 术语解释 | 中文医学术语首次出现时 |

**FAQ 短代码格式（注意 `- **Q**：A` 格式，冒号必须为中文全角冒号或英文冒号+空格，commit `9722a68` 修过此 bug）：**
```
{{< faq >}}
- **双眼皮手术能维持多久？** 切开法双眼皮通常是永久性的...
- **双眼皮手术疼吗？** 手术在局部麻醉下进行...
{{< /faq >}}
```

### 4.4 按类型分小节

#### 4.4.1 精品指南

**目标长度：** 5000+ 字（含参考与免责声明）

**结构（参考 `content/zh-cn/posts/blepharoplasty-guide.md`）：**
1. 导言（统计引用 + 点题）
2. 是什么（医学定义 + 流行病学）
3. 常见方式（埋线 / 切开 / 韩式三点等并列）
4. 术前准备
5. 风险告知（`{{< alert "warning" >}}`）
6. 恢复过程
7. 术后护理
8. FAQ（5-8 条，`{{< faq >}}` 短代码）
9. 如何选择医生
10. 参考资料（脚注 `[^N]`）

**E-E-A-T 信号：**
- `reviewer: "执业医师审核"` 必填
- `lastReviewed` 必填且 ≤ 6 个月
- 文末有真实参考来源（ASPS/ISAPS/PubMed）
- 不做"绝对化"承诺

#### 4.4.2 月度新闻汇总

**目标长度：** 2000-3000 字

**结构（参考 `medical-aesthetics-news-may-31-2026.md`）：**
1. 总览段（点出本月 3-4 个核心趋势）
2. 政策维度（章节 H2）
3. 技术维度（章节 H2）
4. 市场维度（章节 H2）
5. 消费维度（章节 H2）
6. 编辑团队观察（编辑性视角，区别于纯新闻）
7. 免责声明

**特征：**
- 每章开头用"本月 5 月，X 领域出现了 Y 变化"作为引子
- 数据必须带来源（`据 XX 数据显示`）
- 编辑观察章节体现"独立判断"，不是搬运

#### 4.4.3 小红书趋势

**目标长度：** 1500-2500 字

**结构（参考 `xiaohongshu-hot-may-2026.md`）：**
1. 导言（点出 TOP 3 趋势）
2. 趋势 1：XXX（标题党可接受，但要基于数据）
3. 趋势 2：XXX
4. 趋势 N：XXX
5. 评论区高频问题（FAQ）
6. 趋势解读 / 风险提示

**特征：**
- 标题可稍口语化（"X 突然火了"），但不要标题党
- 大量截图引用（XHS 真实数据 + 脱敏截图）
- FAQ 来自真实评论高频问题
- 必须有"风险提示"章节（平台讨论有偏差，需纠偏）

#### 4.4.4 垂类新闻 pipeline

**目标长度：** 2000-3000 字

**生成流程：**
1. `scripts/crawl-eye-surgery-news/post_generator.py` 自动生成 draft
2. 人工 review 重点：
   - 学术文献引用是否准确
   - 医学概念是否有误
   - 图片是否对应正文
   - 引言/结语是否自然
3. 必要时用 LLM 二次润色（保持作者风格统一）

**人工 review checklist：**
- [ ] 学术引用作者姓名拼写正确
- [ ] 期刊名准确（*Plastic and Reconstructive Surgery* 等斜体）
- [ ] 数字/年份未篡改
- [ ] 没有 LLM 幻觉内容（"据 XX 研究显示"必须能溯源）
- [ ] featuredImage 路径与 frontmatter 一致

---

## 5. 阶段四：中英文翻译

### 5.1 翻译策略：**中文先写、英文后译**

**为什么不用 LLM 直接生成双语？**
- 中文是站点默认语言（`defaultContentLanguage: zh-cn`）
- 医学术语在中文语境下更可控（避免英文 LLM 误用术语）
- 双语成对时翻译质量更稳定（中文 source of truth）

**流程：**
1. 中文版发布并稳定 1-2 周后
2. 用 LLM（如 `gpt-4o`）批量翻译，提示词要求：
   - 保留所有医学术语的英文原文
   - 保留所有 `{{< shortcode >}}` 不动
   - 保留 frontmatter 字段名，只翻译值
   - 保留所有 `![alt](path)` 路径不动
3. 人工 review 关键医学术语
4. 加 `translations` 双向链接

### 5.2 翻译输出

**文件命名配对（与现有 post 一致）：**
```
content/zh-cn/posts/<slug>.md
content/en/posts/<slug>.md
```

**frontmatter 翻译对应：**
| 字段 | zh-cn | en |
|---|---|---|
| title | "双眼皮手术：术前必读指南" | "Blepharoplasty: Pre-Surgery Guide" |
| description | "..." | "..." |
| categories | ["面部整形"] | ["Facial Surgery"] |
| tags | ["双眼皮", ...] | ["blepharoplasty", ...] |
| keywords | ["双眼皮手术", ...] | ["blepharoplasty", ...] |
| translations | ["/en/posts/..."] | ["/zh-cn/posts/..."] |

**翻译术语表（参考现有 post 对应）：**
| 中文 | English |
|---|---|
| 双眼皮手术 / 重睑术 | Blepharoplasty / Double Eyelid Surgery |
| 埋线法 | Suture Method / Non-incisional Blepharoplasty |
| 切开法 | Incisional Blepharoplasty |
| 眼睑成形术 | Eyelid Plasty (general term) |
| 医美 | Aesthetic Medicine |
| 整形 | Plastic Surgery |
| 微整 | Minimally Invasive Procedure |
| 求美者 | Patient / Prospective Patient |

### 5.3 翻译验收

- [ ] 医学术语对照表核对
- [ ] frontmatter 所有 user-facing 字段已翻译
- [ ] 双向 `translations` 链接正确
- [ ] slug 与文件路径与中文版完全对应
- [ ] 短代码、图片路径、参考链接完全一致

---

## 6. 阶段五：SEO & GEO 优化

### 6.1 通用 SEO 清单

| 项目 | 规范 | 验收 |
|---|---|---|
| `title` | ≤ 60 字符，含主关键词 | 必填 |
| `description` | 120-160 字符，含关键词 + 价值主张 | 必填 |
| `keywords` | 5-8 个，逗号分隔，与 tags 不全重合 | 必填 |
| `canonical` | 由 `canonifyURLs: true` 自动处理 | 自动 |
| `hreflang` | 由 i18n 自动处理 | 自动 |
| `featuredImage` | 1200×630，OG/Twitter 分享主图 | 必填 |
| `lastmod` | 实际修改日期 | 必填 |
| `categories` / `tags` | 1 个 / 3-6 个 | 必填 |

**OG/Twitter meta 由 `layouts/partials/templates/opengraph.html` 自动生成**，无需手工。

### 6.2 JSON-LD 结构化数据

**由 `layouts/partials/templates/schema_json.html` 自动注入：**

| Schema 类型 | 注入位置 | 触发条件 |
|---|---|---|
| Organization | 全部页面 | 自动 |
| BreadcrumbList | 非首页 | 自动 |
| WebSite + SearchAction | 首页 | 自动 |
| MedicalWebPage（E-E-A-T 增强） | 全部 post | 自动（含 `author`, `reviewedBy`, `citation`, `speakable`） |
| FAQPage | FAQ 短代码 | 使用 `{{< faq >}}` 时 |

**作者侧只负责：**
- 提供正确的 frontmatter 字段（`author`, `reviewer`, `lastReviewed`, `medicalAudience`）
- 用 `{{< faq >}}` 短代码而非手写 FAQ

### 6.3 GEO 优化

GEO（Generative Engine Optimization）是面向 ChatGPT / Perplexity / Gemini 等生成式引擎的优化。

**核心原则：**
1. **直接答案 + 结构化事实** —— LLMs 倾向引用明确陈述的事实段落
2. **权威引用** —— 引用 ASPS/ISAPS/PubMed 等 LLM 已识别的权威源
3. **FAQ 短答案** —— 短代码 FAQ 是 LLM 提取的"金矿"
4. **统计数字 + 时间戳** —— `2026 年 5 月`、`32 万例` 等具体数字
5. **明确的医疗免责声明** —— 既保护站点也让 LLM 知道内容边界

**站点已实现的 GEO 增强（`schema_json.html`）：**
- `speakable` 字段标识 LLM 可朗读区域
- `citation` 字段列出权威源
- `lastReviewed` 标注时效
- `isAccessibleForFree: true` 标识开放

### 6.4 按类型分小节

#### 6.4.1 精品指南

- [ ] 5+ 条 FAQ（覆盖 LLM 检索高频问题）
- [ ] 章节小标题用 H2/H3（LLM 解析层级）
- [ ] 包含权威统计（ASPS/ISAPS 数字 + 年份）
- [ ] 包含脚注引用（LLM 倾向引用有 footnote 的源）
- [ ] 顶部 `{{< medical-disclaimer />}}`

#### 6.4.2 月度新闻汇总

- [ ] 文末"参考来源"列出所有原始链接
- [ ] 包含时间戳（"2026 年 5 月"重复出现）
- [ ] 编辑观察章节明确表达独立判断（区别于二手转述）
- [ ] 涉及未来预测时明确标注"编辑团队观察"
- [ ] 顶部 `{{< medical-disclaimer />}}`

#### 6.4.3 小红书趋势

- [ ] 标题含时间戳 + 平台名（"小红书 2026 趋势"）
- [ ] 每条趋势标题清晰可被 LLM 提取为"答案"
- [ ] 平台截图带 alt 文本（`![alt](path)` 不要留空 alt）
- [ ] 包含"风险提示"章节
- [ ] 顶部 `{{< medical-disclaimer />}}`（即使是趋势也涉及医疗）

#### 6.4.4 垂类新闻 pipeline

- [ ] 跑完 pipeline 后人工校对所有学术引用
- [ ] 移除 LLM 幻觉内容
- [ ] featuredImage 路径正确
- [ ] 短代码格式合规（与现有 post 一致）

---

## 7. 完整 walk-through 示例：从 0 到 draft

**演示场景：** 发布"双眼皮手术 2026 Q3 更新版"（精品指南）。

### 7.1 阶段 1：搜索与调研

```bash
# 1. 学术搜索
opencli pubmed search "blepharoplasty Asian 2026" --limit 20 -f json > data/crawled/blepharoplasty-guide/20260604_pubmed.json
opencli google-scholar search "double eyelid surgery review" --limit 15 -f json > data/crawled/blepharoplasty-guide/20260604_scholar.json

# 2. 权威机构
opencli web read --url "https://www.plasticsurgery.org/cosmetic-procedures/eyelid-surgery" -f json > data/crawled/blepharoplasty-guide/20260604_asps.json
opencli web read --url "https://www.isaps.org/discover/about-isaps/global-statistics/" -f json > data/crawled/blepharoplasty-guide/20260604_isaps.json

# 3. 中文文献
opencli baidu-scholar search "重睑术 综述" --limit 10 -f json > data/crawled/blepharoplasty-guide/20260604_cnki.json
```

**产物：** 4 个 JSON 文件 + 1 份人工整理的笔记 `web-articles/blepharoplasty-guide/research-notes.md`

### 7.2 阶段 2：配图下载

```bash
# Unsplash 搜索（CLI 通过 opencli web 命令）
opencli web read --url "https://unsplash.com/s/photos/blepharoplasty" -f json
# → 手工挑选 3 张真实场景图
# 下载并用 sips 优化
sips -Z 1200 unsplash-blepharoplasty-1.jpg --out static/images/posts/blepharoplasty-guide-1.jpg
sips -Z 1200 unsplash-blepharoplasty-2.jpg --out static/images/posts/blepharoplasty-guide-2.jpg
sips -Z 1200 unsplash-blepharoplasty-3.jpg --out static/images/posts/blepharoplasty-guide-3.jpg

# featured + card
sips -Z 1200 unsplash-cover.jpg --out static/images/posts/blepharoplasty-guide-featured.jpg
sips -Z 800  unsplash-card.jpg  --out static/images/posts/blepharoplasty-guide-card.jpg
```

**产物：** 5 张图（`static/images/posts/blepharoplasty-guide-*.jpg`）

### 7.3 阶段 3：写中文 draft

**创建文件** `content/zh-cn/posts/blepharoplasty-guide-2026q3.md`：

```yaml
---
title: "双眼皮手术：2026 Q3 术前必读指南"
date: 2026-07-15
lastmod: 2026-07-15
description: "双眼皮手术（重睑术）2026 Q3 更新版。基于 2026 年最新 ASPS 数据、PubMed 综述与中文临床指南，为求美者提供手术方式、术前评估、风险、恢复全流程指导。"
categories: ["面部整形"]
tags: ["双眼皮", "重睑术", "眼部整形", "术前准备", "2026更新"]
keywords: ["双眼皮手术 2026", "重睑术", "埋线双眼皮", "切开双眼皮", "双眼皮恢复", "双眼皮风险", "双眼皮医院选择"]
draft: true
featuredImage: "/images/posts/blepharoplasty-guide-featured.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "2026-07-15"
medicalAudience: "Patient"
translations:
  - "/en/posts/blepharoplasty-guide-2026q3"
---

{{< medical-disclaimer />}}

[正文...参考现有 blepharoplasty-guide.md 结构]
```

### 7.4 阶段 4：翻译

```bash
# 1. 复制中文版
cp content/zh-cn/posts/blepharoplasty-guide-2026q3.md content/en/posts/blepharoplasty-guide-2026q3.md

# 2. 用 LLM 翻译正文（保留 frontmatter 字段名 + 短代码 + 图片路径）
# 推荐 prompt: "Translate the following Chinese medical article to English.
#   - Keep all Hugo frontmatter keys in English
#   - Translate values
#   - DO NOT translate content inside {{< ... >}}
#   - DO NOT translate image paths
#   - Use the medical terminology glossary from §5.2"

# 3. 人工 review 医学术语 + 双向 translations 链接
```

### 7.5 阶段 5：SEO & GEO

**自动化部分：** `schema_json.html` 已生成所有 JSON-LD。

**手工检查：**
- [ ] `title` 含"2026 Q3"和主关键词"双眼皮手术"
- [ ] `description` 120-160 字符
- [ ] `keywords` 7 个
- [ ] `lastReviewed` 是 2026-07-15
- [ ] `reviewer` 字段已填
- [ ] `{{< faq >}}` 短代码有 5+ 条
- [ ] 文中含脚注引用 `[^N]`
- [ ] 文末有"参考来源"段
- [ ] `translations` 链接双向正确

### 7.6 本地预览

```bash
# 启动 Hugo 开发服务器
npm run dev
# 打开 http://localhost:1313/posts/blepharoplasty-guide-2026q3/
# 检查：1) 中英文版均可访问 2) OG 图正确显示 3) FAQ 折叠展开正常
# 4) schema.org 结构化数据无误（用 https://search.google.com/test/rich-results 测试）

# 确认无误后
# 1. 改 draft: false（中文版）
# 2. 改 draft: false（英文版）
# 3. git add + commit
```

---

## 8. 发布前 checklist（draft → published）

发布前请逐项打钩：

**Frontmatter：**
- [ ] `title` ≤ 60 字符，含主关键词
- [ ] `description` 120-160 字符
- [ ] `keywords` 5-8 个
- [ ] `lastmod` 是真实修改日期
- [ ] `featuredImage` 路径正确，文件存在
- [ ] `author` + `reviewer` 已填
- [ ] `lastReviewed` ≤ 6 个月
- [ ] `translations` 双向链接已配对

**内容：**
- [ ] 顶部 `{{< medical-disclaimer />}}`
- [ ] H2/H3 层级清晰
- [ ] 至少 3 张内嵌图，配 alt
- [ ] 至少 1 个 `{{< alert >}}`（如涉及风险）
- [ ] 至少 3 条 `{{< faq >}}`（精品指南 ≥ 5 条）
- [ ] 参考资料有真实链接
- [ ] 文末"免责声明"

**SEO/GEO：**
- [ ] `https://search.google.com/test/rich-results` 通过
- [ ] OG 图在 Facebook Debugger 显示正确
- [ ] hreflang 双向正确

**双语：**
- [ ] 中英成对发布（或标记"先发中文，英文 X 日内补"）
- [ ] 翻译术语表核对完毕

**图片：**
- [ ] 所有图 ≤ 500KB
- [ ] 命名符合 `<slug>-<type>.<ext>`
- [ ] featured + card + inline 三类齐全

**构建：**
- [ ] `npm run dev` 本地无报错
- [ ] `npm run build:full` 构建成功（含 pagefind 索引）
- [ ] RSS feed 已更新

**发布：**
- [ ] 提交 Google Search Console（已自动，verify 通过 commit `936fefd`）
- [ ] commit message 格式：`post: <title> (zh/en)` 或 `feat: add <category> <title>`

---

## 9. 工具速查表

### 9.1 opencli 搜索

| 命令 | 用途 |
|---|---|
| `opencli pubmed search "<query>"` | PubMed 学术搜索 |
| `opencli google-scholar search "<query>"` | Google Scholar |
| `opencli baidu-scholar search "<query>"` | 百度学术（中文） |
| `opencli google search "<query>"` | Google 网页 |
| `opencli rednote search "<query>"` | 小红书 |
| `opencli zhihu search "<query>"` | 知乎 |
| `opencli web read --url <url>` | 抓取任意网页（LLM 提取） |
| `opencli browser screenshot` | 浏览器截图（XHS 脱敏截图） |
| `-f json` | 输出 JSON 格式 |
| `--limit N` | 限制结果数 |

**完整适配器列表：** `opencli list`

### 9.2 npm scripts

| 命令 | 用途 |
|---|---|
| `npm run dev` | Hugo dev server（含 draft） |
| `npm run build` | Hugo minify build |
| `npm run build:full` | Build + pagefind 索引 |
| `npm run search-index` | 仅生成 pagefind 索引 |
| `npm run crawl:eye-news` | 跑眼部整形 pipeline（新增 topic 时在 `package.json` 添加） |

### 9.3 图片优化

| 命令 | 用途 |
|---|---|
| `sips -Z 1200 in.jpg --out out.jpg` | 等比缩放最长边 1200 |
| `sips -s format jpeg -s formatOptions 85 in.png --out out.jpg` | 转 JPEG 85% |
| `sips -g pixelWidth -g pixelHeight in.jpg` | 查看尺寸 |

### 9.4 Hugo

| 命令 | 用途 |
|---|---|
| `hugo new posts/<slug>.md` | 用 archetype 创建新 post |
| `hugo server -D` | Dev server 含 draft |
| `hugo --minify` | 生产构建 |
| `hugo --templateMetrics` | 模板性能分析 |

### 9.5 短代码

| 短代码 | 文件 |
|---|---|
| `{{< medical-disclaimer />}}` | `layouts/shortcodes/medical-disclaimer.html` |
| `{{< figure src="" title="" >}}` | PaperMod 内置 |
| `{{< alert "warning" >}}` | `layouts/shortcodes/alert.html` |
| `{{< faq >}}` | `layouts/shortcodes/faq.html` |
| `{{< term "" >}}` | `layouts/shortcodes/term.html` |

---

## 10. 常见坑与 FAQ

### Q1: draft 改 false 后页面 404
**原因：** `buildDrafts: false`（`hugo.yaml`），draft 在 build 时不输出。
**解决：** 确认 `hugo server -D` 包含 draft，部署前移除 draft 标记。

### Q2: featuredImage 在文章页不显示
**原因：** 使用了 `image` 而非 `featuredImage` 字段名。
**解决：** 检查 `layouts/partials/templates/opengraph.html` 第 48-50 行（`Params.featuredImage` 优先于 `cover.image`）。统一用 `featuredImage`。

### Q3: FAQ 短代码解析后 Q/A 没显示
**原因：** `- **Q**：A` 用了全角冒号但缺少冒号后空格，或 Q/A 分隔符号不对。
**解决：** 参考 §4.3 FAQ 短代码格式。冒号后必须有空格，且每个 Q/A 必须独立一行（commit `9722a68` 修过此 bug）。

### Q4: 中文版改了，但英文版没同步
**原因：** `translations` 链接没配对。
**解决：** 每次改 frontmatter，双语都要改；CI 不强制（手工守门）。

### Q5: sitemap.xml 没更新
**原因：** Hugo build 时 `sitemap.changefreq: weekly` 自动生成。
**解决：** 重新 build：`npm run build:full`。

### Q6: 图片加载慢
**原因：** 尺寸超标（> 500KB），或未用 sips 优化。
**解决：** 跑 §3.3 优化 SOP。Hero 图用 `loading="lazy"`（PaperMod 默认）。

### Q7: Google Search Console 报"未编入索引"
**原因：** 新发布未提交 sitemap，或 robots.txt 阻止。
**解决：** 检查 `static/robots.txt` + 提交 `https://beauty-blog.cloud-ip.cc/sitemap.xml`。

### Q8: opencli 某 adapter 失败
**原因：** 站点改版、IP 限流、维护中。
**解决：** `opencli adapter status <name>` 检查；降级到 `opencli web read --url <url>` 通用抓取。

### Q9: 双语 post slug 不一致
**原因：** 中文用 `<slug>.md`，英文用 `<slug>-en.md`。
**解决：** 统一用**相同 slug**（仅 `content/` 子目录区分语言）。`translations` 链接要写相对路径。

### Q10: 小红书截图被识别为营销搬运
**原因：** 截图未脱敏（用户 ID、头像清晰可见）。
**解决：** §3.2.3 强调脱敏。仅引用文字摘要 + 关键截图，不做整笔记搬运。

---

## 11. 每日自动发布（12:00 触发，5 阶段全自动）

> **状态：** 已部署（2026-06-04）。当前**仅调度垂类新闻 pipeline**（`npm run crawl:eye-news`），其他类型 pipeline 待补。

### 11.1 架构

```
┌────────────────────────────────────────────┐
│  macOS launchd (StartCalendarInterval)     │
│  每天 12:00 触发 com.beautyblog.dailypublish│
└──────────────────┬─────────────────────────┘
                   ▼
┌────────────────────────────────────────────┐
│  scripts/daily-publish/daily-publish.sh    │
│  1. Kill switch check                      │
│  2. npm run crawl:eye-news   (Stage 1-4)   │
│  3. draft: true → false      (Stage 5)     │
│  4. git commit (AUTO_COMMIT, default on)   │
│  5. git push    (AUTO_PUSH, default OFF)   │
│  6. macOS notification                     │
└────────────────────────────────────────────┘
                   ▼
            logs/daily-publish/<ts>.log
```

### 11.2 关键安全机制

| 机制 | 默认 | 说明 |
|---|---|---|
| **Kill switch** `.disabled` 文件 | OFF | `touch scripts/daily-publish/.disabled` 立即停 |
| **Auto commit** | ON | 发布后自动 git commit（可逆） |
| **Auto push** | **OFF** | 不会推 remote，强制人工 `git push` 触发部署——保留刹车 |
| **.bak 备份** | ON | 翻转 draft 前备份原文件 |
| **失败通知** | ON | 任一阶段失败 → Basso 音警告 + 日志路径 |

### 11.3 安装与卸载

```bash
# 安装（macOS 一次）
./scripts/daily-publish/install.sh

# 卸载
./scripts/daily-publish/uninstall.sh

# 立即测试（不等 12:00）
./scripts/daily-publish/daily-publish.sh

# 暂停 / 恢复
touch scripts/daily-publish/.disabled    # 暂停
rm scripts/daily-publish/.disabled       # 恢复
```

### 11.4 设计决策（不计划扩展）

1. **post_generator.py 是硬编码模板**（**有意为之**）—— 每天输出同一深度分析文章，只换日期 slug 和 E-E-A-T 字段。这样保证医学准确性 100% 可控（LLM 合成可能引入幻觉）。要"每日独特"需要修改这个决定
2. **只调一个 pipeline** —— 仅 `crawl:eye-news`（垂类新闻）。其他类型（小红书/精品指南/月度汇总）需各自新建 pipeline 脚本
3. **YMYL 风险** —— 医疗类内容跳过人工 review，AdSense/Google 2024-03 core update 对此敏感。建议保留 `.disabled` 兜底

### 11.5 后续路线图（可选项）

- [ ] 新建 `scripts/crawl-xhs-trends/`、`scripts/crawl-monthly-news/`
- [ ] Telegram bot 通知（替代 macOS notification，跨设备）
- [ ] GitHub Actions 镜像（Mac 不在线时由云端跑）

### 11.6 相关文件

- [`scripts/daily-publish/daily-publish.sh`](../../scripts/daily-publish/daily-publish.sh) —— 主脚本
- [`scripts/daily-publish/com.beautyblog.dailypublish.plist`](../../scripts/daily-publish/com.beautyblog.dailypublish.plist) —— launchd 配置
- [`scripts/daily-publish/install.sh`](../../scripts/daily-publish/install.sh) —— 安装
- [`scripts/daily-publish/README.md`](../../scripts/daily-publish/README.md) —— 完整说明

---

## 附录 A：变更日志

| 日期 | 变更 | 作者 |
|---|---|---|
| 2026-06-04 | 初版：基于 8+ 篇历史 post + `crawl-eye-surgery-news` pipeline + image-guidelines 沉淀 | Beauty-Blog 团队 |
| 2026-06-04 | §11 新增：每日 12:00 自动发布（v1 launchd + 5 阶段全自动 + kill switch） | Beauty-Blog 团队 |

## 附录 B：相关文档索引

- [`docs/image-guidelines.md`](./image-guidelines.md) —— 图片规范
- [`docs/image-optimization-report.md`](./image-optimization-report.md) —— 图片优化记录
- [`openspec/changes/crawl-eye-plastic-surgery-news/`](../../openspec/changes/crawl-eye-plastic-surgery-news/) —— 垂类新闻 pipeline spec
- [`scripts/crawl-eye-surgery-news/`](../../scripts/crawl-eye-surgery-news/) —— 垂类新闻 pipeline 代码
- [`scripts/daily-publish/`](../../scripts/daily-publish/) —— 每日 12:00 自动发布调度（v1）
- [`layouts/partials/templates/schema_json.html`](../../layouts/partials/templates/schema_json.html) —— JSON-LD 模板
- [`layouts/partials/templates/opengraph.html`](../../layouts/partials/templates/opengraph.html) —— OG/Twitter meta
- [`hugo.yaml`](../../hugo.yaml) —— Hugo 全局配置
