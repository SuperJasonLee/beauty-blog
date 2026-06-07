## Context

Beauty-blog 是 YMYL（Your Money or Your Life）医疗类 Hugo 站点，13 篇 POST 中：
- 源数据真实存在于 `web-articles/`、`data/crawled/`（已验证 14 条 Yicai URL、10 个 PubMed ID）
- 但生成 POST 时 LLM 把 URL 全部"消化"成正文文字，未保留为脚注
- 部分 POST（XHS 三篇）则混入了**完全无源**的博主名 + 增长百分比，疑似 LLM 幻觉

修复时必须解决三个核心矛盾：
1. **保留 vs 删除**：找不到源的"事实"是删掉还是改为"编辑团队观察"？
2. **回灌精度**：脚注要精确到具体文章 URL，但有些数据需要重新搜（搜索成本）
3. **守门成本**：手工回灌一次没价值，要有 audit 脚本兜底未来 POST

## Goals / Non-Goals

**Goals:**
- 100% POST 内的统计 / 事实 / 人名都可追溯到脚注 URL，或显式标注为"编辑团队观察"
- 所有 news/XHS POST 含 FAQ 短代码（3-5 条），GEO 抽取友好
- frontmatter 字段统一（reviewer / lastReviewed / translations 全齐）
- `scripts/audit-posts.py` 静态检查，单跑 < 5 秒，纳入 publish checklist
- 不删任何 POST（保 SEO 权重）；只删/改 POST 内"假数据片段"

**Non-Goals:**
- 不重做整个 LLM pipeline（`scripts/crawl-eye-surgery-news/post_generator.py` 留给下个 change）
- 不补抓 XHS 数据源（rednote 适配器有限流，单独再开 change）
- 不引入 CI（先本地 audit，CI 之后看效果）
- 不改主题 / 模板 / JSON-LD（schema_json.html 已生成正确）

## Decisions

### 决策 1：找不到源的数据 — 删除而非"标注存疑"

**选 删除**，理由：
- YMYL 类 POST 留"标注存疑"等同于声明"我们也不确定"，Google E-E-A-T 直接降分
- LLM 幻觉的博主名（如"上海九院戴婷婷"）若搜不到原帖，留下是诽谤风险
- 字数损失可用真实趋势分析补足（编辑视角 + 已有的真实数据点）

**替代方案**：
- ❌ 全文标注"待核" → 用户看着像免责声明轰炸
- ❌ 替换为"业内人士"等含糊表述 → LLM 反而会引用错误源
- ✅ 删除假数据，保留可证实的趋势框架，编辑视角填充

### 决策 2：脚注 URL 来源优先级

```
1. web-articles/<topic>/articles.json   ← 已抓取，零成本（首选）
2. data/crawled/<topic>/*.json          ← 已抓取
3. opencli <adapter> search "..."       ← 重新搜（仅当 1、2 缺失且数据关键）
4. 删除该数据                            ← opencli 也搜不到时
```

不允许 LLM 直接合成 URL（即使"看起来很合理"也禁止）。

### 决策 3：audit 脚本范围

**MVP 范围（本 change 内）：**
- 解析 frontmatter，检查必填字段（reviewer / lastReviewed / featuredImage / translations）
- 解析正文，统计：脚注数 / FAQ 短代码数 / 图片路径合法性（必须以 `/` 开头）
- 正则检测"裸百分比 + 无脚注"（`+\d+%` 后 50 字符内无 `[^`）
- 正则检测"博主名 + 点赞数 + 无 URL"

**输出**：JSON 报告到 stdout + 退出码（0 通过 / 1 警告 / 2 错误）。

**不做（留下个 change）：**
- ❌ 不做 LLM 内容质量评分
- ❌ 不做 URL 可达性检查（网络请求慢）
- ❌ 不做与源数据的 fact-checking 比对

### 决策 4：双语处理顺序

**先全量修中文，再批量修英文**。理由：
- 中文是 source of truth（`defaultContentLanguage: zh-cn`）
- 英文翻译可直接用相同的脚注 URL（URL 是中性的）
- 减少修改面，降低出错率

### 决策 5：FAQ 内容来源

不让 LLM 生成 FAQ（容易再次幻觉）。FAQ 必须来自：
- 源文章的原始问题（如 Yicai 评论区）
- POST 已有正文的核心观点改写为 Q/A
- SOP §4.3 推荐的常见医美问题模板

## Risks / Trade-offs

- [字数下降影响排名] → 用真实趋势分析 + opencli 补抓数据补足；最坏情况合并相似 POST
- [大量改动触发 sitemap 全量更新] → 接受短期排名波动；分 2 批 commit（先精品/news、后 XHS）方便观察
- [审查清单未覆盖某种假数据形态] → audit 脚本设计成"规则可扩展"（YAML 规则文件），后续按需增规则
- [LLM 幻觉博主名删错] → 删除前在 `web-articles/`、`opencli rednote search` 双重确认；保留 git history 可回滚
- [reviewer 字段集中改写仍像批量] → `lastReviewed` 按 commit 时间分批设置，不全部统一

## Migration Plan

**分阶段（每阶段独立 commit，可回滚）：**

```
Phase 1: 工具 (1 天)
  ├─ scripts/audit-posts.py
  ├─ package.json: audit:posts script
  └─ docs/post-publishing-workflow.md §8 checklist

Phase 2: 月度新闻 5 篇 (1-2 天)
  ├─ 用 web-articles/ 数据回灌 URL（medical-aesthetics-may-31）
  ├─ 其余 4 篇用 opencli 补搜 URL
  └─ 补 FAQ + reviewer + translations

Phase 3: 小红书 3 篇 (1-2 天)
  ├─ 删除幻觉博主名 + 假百分比
  ├─ 重写为真实趋势分析（用 opencli rednote 抓真数据）
  └─ 补 FAQ

Phase 4: 眼整形 2 篇 (1 天)
  ├─ 0606: 重构链接堆砌段落
  └─ 0601: 用 data/crawled/ 中真 PMID 替换无源作者名

Phase 5: 精品指南 3 篇 (0.5 天)
  └─ 精确化脚注 URL（从 ASPS 主域名 → 具体文章页）

Phase 6: 英文翻译同步 (1 天)
  └─ 套用相同 URL/FAQ，翻译 FAQ 文本

Phase 7: 验证 (0.5 天)
  ├─ npm run audit:posts → 0 错误
  ├─ npm run build:full → 无报错
  └─ 抽样 5 篇人工 review
```

**Rollback：** 每阶段独立 commit，任何阶段失败可 `git revert <sha>` 回到上阶段。

## Open Questions

1. **XHS 数据补抓预算**：opencli rednote 有限流，单日可抓约 200 条。3 篇 XHS 各需 30-50 条新数据，需 1-2 个工作日窗口。是否先用 SOP §3.2.3 的"人工浏览 + chrome-devtools 截图"兜底？
2. **被删数据的处理**：删除"上海九院戴婷婷点赞 2649"这类陈述时，是否保留 git history 的 diff 作为审计证据？（默认保留）
3. **FAQ 的医生 reviewer 字段**：当前 `reviewer: "执业医师审核"` 是占位文字，未来是否需要实名签名？（本 change 不动）
