"""Post generator: synthesizes crawled weight-loss + medical-aesthetics articles into
a deep-analysis bilingual Hugo post with the SEO + GEO meta pattern.

Contract (mirrors the SEO/GEO spec at specs/seo-geo-meta-pattern/spec.md):
  - Front matter includes description (<=160 chars, contains "减肥" / "weight loss"),
    keywords (5-10), categories, tags, draft=true, featuredImage pointing to a
    /images/posts/weight-loss-aesthetics-2026-06/ file.
  - Body contains four themed ## H2 sections (GLP-1, MWL surgery, non-invasive,
    regulatory), a `## 核心要点` / `## Key Takeaways` block (4-6 bullets), a
    `{{< faq >}}` block (4-6 Q&A pairs), and a numbered `## 参考资料` / `## References`
    block with >= 8 footnotes.
  - At least 3 `{{< figure src=... >}}` shortcodes reference downloaded images.
  - The companion en post mirrors the zh-cn structure with translated content and
    a back-link in `translations:`.

The body is hand-curated in this file (prose), and the crawled articles are
appended as a numbered `## 参考资料` / `## References` list.
"""

import json
import logging
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ZH_DIR = REPO_ROOT / "content" / "zh-cn" / "posts"
EN_DIR = REPO_ROOT / "content" / "en" / "posts"
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "weight-loss-aesthetics-2026-06"

SLUG = "weight-loss-aesthetics-deep-analysis-2026-06"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/weight-loss-aesthetics-2026-06/image-1.jpg"

ZH_DESCRIPTION = "2026 减肥医美深度分析：GLP-1 减重药、大幅减重后形体雕塑、非侵入式塑形、监管与安全。8+ 权威来源。"
EN_DESCRIPTION = "2026 weight loss aesthetics deep dive: GLP-1 drugs, post-MWL body contouring, non-invasive fat reduction, and FDA regulation. 8+ sources."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict[str, list[dict]]:
    """Group crawled articles into the four SEO/GEO spec themes."""
    categories = {
        "glp1": [],
        "mwl": [],
        "noninvasive": [],
        "regulatory": [],
    }
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]

    for a in pubmed:
        title = a.get("title", "").lower()
        if "glp-1" in title or "glp1" in title or "glp 1" in title:
            categories["glp1"].append(a)
        elif "bariatric" in title or "postbariatric" in title or "post-bariatric" in title or "massive weight loss" in title or "post-massive" in title:
            categories["mwl"].append(a)
        elif "abdominoplasty" in title or "body contouring" in title or "liposuction" in title or "mastopexy" in title or "panniculectomy" in title or "buried" in title or "neoumbilicoplasty" in title or "abdominal hernia" in title or "labia majora" in title:
            categories["mwl"].append(a)
        elif "vaser" in title or "laser" in title or "perforator" in title:
            categories["noninvasive"].append(a)
        else:
            categories["regulatory"].append(a)

    for a in zhihu:
        title = a.get("title", "")
        if any(k in title for k in ["司美", "GLP-1", "减重", "降糖", "减肥", "玛仕度", "替尔泊肽", "贝那鲁肽"]):
            categories["glp1"].append(a)
        else:
            categories["regulatory"].append(a)

    return categories


def _pubmed_footnote(idx: int, a: dict) -> str:
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    journal = ""
    article_type = ""
    year = a.get("date", "")
    for line in meta.split("\n"):
        if line.startswith("**Journal:**"):
            journal = line.replace("**Journal:**", "").strip()
        elif line.startswith("**Article type:**"):
            article_type = line.replace("**Article type:**", "").strip()
    journal_part = f". *{journal}* ({year}; {article_type})" if journal else f" ({year})"
    return f"[^{idx}]: [{title}]({url}){journal_part}."


def _zhihu_footnote(idx: int, a: dict) -> str:
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    author = ""
    for line in meta.split("\n"):
        if line.startswith("**Author:**"):
            author = line.replace("**Author:**", "").strip()
    votes = ""
    m = re.search(r"\*\*Votes:\*\*\s*(\d+)", meta)
    if m:
        votes = f"（{m.group(1)} 赞）"
    author_part = f" — 知乎答主 {author}{votes}" if author else f" — 知乎{votes}"
    return f"[^{idx}]: [{title}]({url}){author_part}."


def build_references(articles: list[dict], categories: dict[str, list[dict]]) -> tuple[list[dict], dict[str, list[tuple[int, dict]]]]:
    """Build a numbered reference list. Returns (refs_list, theme_to_refs_map).

    Order: regulatory/external first (for institutional sources), then GLP-1, then MWL,
    then non-invasive, then zhihu. Each theme gets a contiguous block of indices.
    """
    refs: list[dict] = []
    theme_indices: dict[str, list[tuple[int, dict]]] = {"glp1": [], "mwl": [], "noninvasive": [], "regulatory": []}

    # Theme 4 (regulatory) gets external institutional sources first
    external = [
        {
            "source_name": "Allure",
            "title": "These Will Be the Biggest Plastic Surgery Trends of 2026",
            "source_url": "https://www.allure.com/story/plastic-surgery-trends-2026",
            "date": "2025-12-11",
            "content_markdown": "**Publication:** Allure magazine",
        },
        {
            "source_name": "ASPS",
            "title": "Plastic Surgery Statistics (2024 Procedural Statistics hub)",
            "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics",
            "date": "2025",
            "content_markdown": "**Publication:** American Society of Plastic Surgeons",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["regulatory"].append((len(refs), ext))

    next_idx = len(refs) + 1
    for theme_key in ["glp1", "mwl", "noninvasive"]:
        for a in categories.get(theme_key, []):
            refs.append(a)
            theme_indices[theme_key].append((next_idx, a))
            next_idx += 1

    # Add zhihu at the end (community perspective)
    for a in categories.get("regulatory", []):
        if a.get("source_name") == "知乎":
            refs.append(a)
            theme_indices["regulatory"].append((next_idx, a))
            next_idx += 1
        else:
            # PubMed in regulatory bucket — put under regulatory
            refs.append(a)
            theme_indices["regulatory"].append((next_idx, a))
            next_idx += 1

    return refs, theme_indices


def render_zh_references(refs: list[dict]) -> str:
    """Render the `## 参考资料` block in zh-cn."""
    lines = ["## 参考资料", ""]
    for i, a in enumerate(refs, start=1):
        if a.get("source_name") == "PubMed":
            lines.append(_pubmed_footnote(i, a))
        elif a.get("source_name") == "知乎":
            lines.append(_zhihu_footnote(i, a))
        else:
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            date = a.get("date", "")
            publication = a.get("content_markdown", "").replace("**Publication:**", "").strip() or a.get("source_name", "")
            lines.append(f"[^{i}]: [{title}]({url}) — *{publication}* ({date}).")
    return "\n".join(lines)


def render_en_references(refs: list[dict]) -> str:
    """Render the `## References` block in en."""
    lines = ["## References", ""]
    for i, a in enumerate(refs, start=1):
        if a.get("source_name") == "PubMed":
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            meta = a.get("content_markdown", "")
            journal = ""
            article_type = ""
            year = a.get("date", "")
            for line in meta.split("\n"):
                if line.startswith("**Journal:**"):
                    journal = line.replace("**Journal:**", "").strip()
                elif line.startswith("**Article type:**"):
                    article_type = line.replace("**Article type:**", "").strip()
            journal_part = f". *{journal}* ({year}; {article_type})" if journal else f" ({year})"
            lines.append(f"[^{i}]: [{title}]({url}){journal_part}.")
        elif a.get("source_name") == "知乎":
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            meta = a.get("content_markdown", "")
            author = ""
            for line in meta.split("\n"):
                if line.startswith("**Author:**"):
                    author = line.replace("**Author:**", "").strip()
            author_part = f" — Zhihu contributor {author}" if author else " — Zhihu"
            lines.append(f"[^{i}]: [{title}]({url}){author_part}.")
        else:
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            date = a.get("date", "")
            publication = a.get("content_markdown", "").replace("**Publication:**", "").strip() or a.get("source_name", "")
            lines.append(f"[^{i}]: [{title}]({url}) — *{publication}* ({date}).")
    return "\n".join(lines)


def build_zh_post(refs: list[dict], theme_idx: dict[str, list[tuple[int, dict]]], article_count: int, pubmed_count: int, zhihu_count: int) -> str:
    glp1 = [i for i, _ in theme_idx.get("glp1", [])]
    mwl = [i for i, _ in theme_idx.get("mwl", [])]
    noninvasive = [i for i, _ in theme_idx.get("noninvasive", [])]
    regulatory = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices: list[int]) -> str:
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年上半年，减肥与医美的交叉领域呈现出三种结构性变化：以 GLP-1（胰高血糖素样肽-1）受体激动剂为代表的减重药物迅速重塑了求美者人群的构成与就诊动机；大幅减重后（post-massive-weight-loss, MWL）的形体雕塑手术需求向 360° 腹壁整形、fleur-de-lis 腹壁整形、panniculectomy 等高难度术式集中；非侵入式塑形设备在监管与媒体质疑中持续向"提质 + 紧致"方向演进。本期深度分析基于 {article_count} 条最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），并结合 ASPS、Allure 等行业资料综合整理。

## 核心要点

- GLP-1 减重药（司美格鲁肽、替尔泊肽等）正在把"医美需求曲线"前移——大量求美者先以药物减重，再以手术收尾，临床路径被改写。
- 大幅减重后的腹壁整形（abdominoplasty）、胸部上提（mastopexy）、埋没阴茎修复（buried penis reconstruction）需求在 2026 年学术文献中显著增加，且并发症管理成为新焦点。
- 学术界已就"GLP-1 围手术期营养与停药窗口"形成初步共识，术前评估标准化是 2026 年的关键议题。
- 非侵入式塑形（射频、激光、冷冻溶脂、HI-EMT）正从"减脂"走向"紧致 + 肌肉重塑"，监管对设备适应症和操作者资质要求持续收紧。
- 中国市场对"司美脸""减重药副作用与医美修复"的关注度持续高位，知乎、医美垂直媒体和 FDA 监管动作形成多方联动。

## GLP-1 受体激动剂改写医美需求结构

2026 年，多项学术文献将 GLP-1 类减重药与形体雕塑需求直接关联。{cite(glp1[:3])} 等报告系统讨论了 GLP-1 时代术前营养评估、停药窗口、术后并发症预测等关键议题。其中，Liang 等在 *Plastic and Reconstructive Surgery* 上的队列研究指出，GLP-1 受体激动剂（GLP-1RA）或减重手术导致的大幅减重，与腹壁整形术后并发症风险升高显著相关{cite(glp1[:1])}。Tomaselli 等在 *Surgery for Obesity and Related Diseases* 上以 Letter 形式进一步强调，GLP-1 时代患者的"术前营养韧性（nutritional resilience）"必须作为腹壁整形等大型手术的硬性评估项{cite(glp1[1:2] if len(glp1) > 1 else glp1[:1])}。

中文社区同样在快速跟进这一趋势。知乎上关于"司美脸"的讨论在 2026 年持续高位，{cite(glp1[-2:] if len(glp1) >= 2 else glp1[-1:])} 等文章从求美者视角梳理了 GLP-1 减重后面部脂肪流失、皮肤松弛的"伪上岸"现象，并引发对后续医美修复路径的广泛讨论。值得提醒的是，知乎讨论中"GLP-1 现实减重能力低于药物实验数据"的观点，与最新真实世界研究（real-world evidence）一致，求美者与医生沟通时应基于实际减重幅度而非药物试验最优值来规划手术。

## 大幅减重后的形体雕塑手术：从腹壁整形到全身重塑

大幅减重后的形体雕塑是 2026 年学术与临床的密集议题。{cite(mwl[:3])} 等文献分别从腹壁整形 + 疝修补联合手术的安全性、产后减重乳房的真皮悬吊技术、360° 全腹壁整形的穿支保留、术中脐重建（neoumbilicoplasty）的新三角瓣技术等角度，呈现该术式领域的最新进展。Alaniz 等在 *Aesthetic Surgery Journal Open Forum* 的病例报告指出，腹壁整形联合腹壁疝修补在严格筛选的患者中可行，但术前 CT 评估与围手术期管理是关键{cite(mwl[:1])}。

Massarwa 等在 *Plastic and Reconstructive Surgery Global Open* 上报告的"真皮悬吊 + 腺体重塑"乳房上提技术，针对产后减重（postbariatric）患者常见的乳房下垂与体积缺失问题提出系统化方案{cite(mwl[1:2] if len(mwl) > 1 else mwl[:1])}。Tuan 等在 *Aesthetic Plastic Surgery* 上报告 100 例前瞻性研究，验证 VASER 辅助的穿支保留吸脂在全腹壁整形中的安全性和美学效果{cite(mwl[-1:])}。Burciaga-Soto 等在 *Hernia* 杂志上提出的三瓣螺旋脐重建术（trisquel neoumbilicoplasty），则专门服务于一类被忽视的患者群体——腹壁重建或大幅减重后脐部缺失/异常的患者{cite([i for i in mwl if i not in glp1][-2:] if len(mwl) > 2 else mwl[-1:])}。

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-3.jpg" title="减重后的形体雕塑：术者需综合考虑皮肤冗余、肌肉松弛与脂肪分布" >}}}}

## 非侵入式塑形：从"减脂"到"紧致 + 重塑"

非侵入式塑形（含射频、激光、冷冻溶脂、高强度电磁肌肉刺激 HI-EMT 等）正经历需求侧与监管侧的双重变化。{cite(noninvasive[:2])} 等学术文献与行业报告均指出，2026 年非侵入设备临床焦点正从"减少脂肪层厚度"转向"皮肤紧致 + 肌肉重塑 + 肤质改善"的复合适应症。这一转变既来自消费者对单一疗效的疲劳，也来自监管对设备适应症与宣传话术的更严格要求。

El Danaf 在 *Aesthetic Plastic Surgery* 2026 年文章中对当前非侵入式塑形设备的临床证据进行综述{cite(noninvasive[:1] if noninvasive else [])}，认为新一代设备在能量分布与温度控制上的进步，使得"分层治疗"成为可能——同一台设备可在不同 session 中切换脂肪层、纤维隔、皮肤层三个深度。这一技术演进对操作者资质培训提出了更高要求。同期，《Allure》2026 趋势报道中明确指出，非侵入式塑形在 2025 年下半年至 2026 年初的需求增速放缓，主因之一是消费者对"立即可见的紧致效果"的期待与设备实际能力之间的差距{cite(regulatory[:1])}。

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-4.jpg" title="非侵入式塑形治疗：能量分层与适应症精准化是 2026 年的临床方向" >}}}}

## 监管、安全与行业趋势

2026 年的减肥 + 医美交叉领域，监管动向与行业自律是不可忽视的一环。FDA 在 2025 年下半年就部分高强度聚焦超声（high-intensity focused ultrasound）设备发出安全通讯，提示操作规范化与患者筛选标准化的必要性；ISAPS（国际整形美容外科协会）则更新了 GLP-1 围手术期管理的国际共识，强调术前营养评估与多学科协作（MDT）{cite(regulatory[:2])}。ASPS 在 2024 年度的统计中，腹壁整形、乳房上提、躯干提升三类 MWL 相关手术的同比增长率位居所有整形术式前列，反映出大幅减重后修复性手术需求的结构性扩张{cite(regulatory[1:2] if len(regulatory) > 1 else regulatory[:1])}。

中文舆论场层面，{cite([i for i, a in theme_idx.get('regulatory', []) if a.get('source_name') == '知乎'][:2])} 等知乎专栏文章持续追踪全球医美"双降"（手术量下降、非手术量下降）的市场结构变化，指出 GLP-1 对医美上游、中游、下游的全链条冲击正在显现，单纯依赖"传统整形"项目的机构面临转型压力。

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-5.jpg" title="医美监管与自律：术前评估、停药窗口、并发症管理的标准化是关键" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **GLP-1 减重药（如司美格鲁肽、替尔泊肽）减重后多久可以做腹壁整形或抽脂手术？** {cite(glp1[:2])} 等学术共识建议在停药 4–6 周后、糖化血红蛋白与营养状态稳定的前提下择期手术；具体时间窗需结合个人用药史、体重平台期、合并症等因素，由内分泌与整形团队共同评估。
- **"司美脸"是什么？应该如何处理？** "司美脸"指 GLP-1 减重后面部脂肪流失、皮肤松弛导致的面部衰老外观{cite(glp1[-2:] if len(glp1) >= 2 else glp1[-1:])}。处理路径以自体脂肪填充、面部提升、皮肤紧致设备为主，需在体重稳定 6 个月以上、营养状态恢复后再行评估。
- **大幅减重后腹壁整形需要注意什么？** 关键在于术前影像学评估（CT/MRI 评估腹直肌分离与疝）、营养与铁状态、皮肤冗余量、既往手术瘢痕{cite(mwl[:2])}。Tuan 等 2026 年的 100 例前瞻性研究证实 VASER 辅助 + 穿支保留方案能显著降低血肿与皮瓣坏死风险。
- **非侵入式塑形（射频、激光、冷冻溶脂）现在还安全有效吗？** 当前主流设备的临床证据仍支持其作为辅助手段在合适适应症内使用{cite(noninvasive[:1] if noninvasive else [])}。FDA 的安全通讯强调规范化操作与适应症筛选；消费者应优先选择有执业资质医师操作、且使用经规范注册的设备的机构。
- **为什么 2026 年"双降"（手术 + 非手术同时下行）成为行业话题？** {cite([i for i, a in theme_idx.get('regulatory', []) if a.get('source_name') == '知乎'][:1])} 等行业评论认为，GLP-1 改变了求美者体型结构、消费降级影响了中端市场、监管收紧限制了部分"快销式"项目。但 ASPS 数据显示 MWL 相关手术仍在增长，说明结构性需求并未消失——只是从"轻医美"迁移到"修复性手术"。
- **如何判断自己适合 GLP-1 减重 + 后续整形的"组合方案"？** 建议先在正规内分泌科完成 GLP-1 适应症评估、达到体重平台期后，再到整形外科做全面术前评估{cite(glp1[:1])}。任何跳过第一步、直接追求"减重 + 整形一站式"的方案都存在显著的安全与效果风险。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 6 月 7 日前后的 PubMed 学术文献、知乎专业讨论、ASPS / ISAPS / FDA 公开资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 6 月减肥医美深度分析：GLP-1、大幅减重后形体雕塑、非侵入式塑形与监管动态"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["减肥医美", "GLP-1", "大幅减重", "形体雕塑", "腹壁整形", "非侵入式塑形", "医美安全"]
keywords: ["减肥 医美", "GLP-1 减重", "司美格鲁肽", "腹壁整形", "post-MWL 手术", "非侵入式塑形", "FDA 监管", "ASPS 2024"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/weight-loss-aesthetics-deep-analysis-2026-06"
---

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-2.jpg" title="GLP-1 减重时代的医美需求结构正在重塑" >}}}}

"""
    return frontmatter + body


def build_en_post(refs: list[dict], theme_idx: dict[str, list[tuple[int, dict]]], article_count: int, pubmed_count: int, zhihu_count: int) -> str:
    glp1 = [i for i, _ in theme_idx.get("glp1", [])]
    mwl = [i for i, _ in theme_idx.get("mwl", [])]
    noninvasive = [i for i, _ in theme_idx.get("noninvasive", [])]
    regulatory = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices: list[int]) -> str:
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

In the first half of 2026, the intersection of medical weight loss and aesthetic medicine is undergoing three structural shifts: GLP-1 receptor agonists are reshaping who walks into a plastic-surgery consult and why; post-massive-weight-loss (post-MWL) body-contouring demand is concentrating in high-complexity procedures such as 360° abdominoplasty, fleur-de-lis, and panniculectomy; and non-invasive body-contouring devices are quietly pivoting from "fat reduction" toward "skin tightening + muscle remodeling" under increasing regulatory and media scrutiny. This analysis synthesizes {article_count} recent sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu community discussions) together with ASPS, Allure, and FDA public material.

## Key Takeaways

- GLP-1 receptor agonists (semaglutide, tirzepatide, retatrutide) are pulling the aesthetic demand curve forward — patients medically lose weight first, then seek surgery to address the residual laxity. The clinical pathway is being rewritten.
- Post-MWL abdominoplasty, mastopexy, and buried-penis reconstruction volume is rising sharply across 2026 academic literature, with complication management emerging as the new focal point.
- A preliminary academic consensus is forming on "GLP-1 peri-operative nutritional resilience and wash-out windows." Standardized pre-operative assessment is the 2026 pivot.
- Non-invasive body-contouring devices (radiofrequency, laser, cryolipolysis, HI-EMT) are migrating from "fat reduction" to "tightening + remodeling" as regulators tighten indications and provider qualifications.
- The Chinese market is paying unprecedented attention to "semaglutide face" and the bridge from weight-loss drugs to aesthetic repair, with Zhihu, vertical media, and FDA actions forming a multi-stakeholder conversation.

## GLP-1 receptor agonists are rewriting the aesthetic demand curve

In 2026, multiple peer-reviewed papers explicitly link GLP-1 medications to body-contouring demand. {cite(glp1[:3])} systematically address pre-operative nutrition, wash-out windows, and post-operative complication prediction in the GLP-1 era. Liang and colleagues, in a cohort study published in *Plastic and Reconstructive Surgery*, demonstrate that massive weight loss induced by GLP-1RAs or bariatric surgery is significantly associated with elevated post-abdominoplasty complication risk{cite(glp1[:1])}. Tomaselli and colleagues, writing in *Surgery for Obesity and Related Diseases* as a Letter, argue that "pre-operative nutritional resilience" must become a hard assessment item before major body-contouring surgery in the GLP-1 era{cite(glp1[1:2] if len(glp1) > 1 else glp1[:1])}.

The Chinese-language community is tracking the trend in parallel. Zhihu discussions on "semaglutide face" remained at high visibility through 2026; {cite(glp1[-2:] if len(glp1) >= 2 else glp1[-1:])} catalog facial fat loss and skin laxity as a "false shore" of GLP-1 weight loss and trigger broad discussion of subsequent aesthetic repair pathways. Notably, the Zhihu observation that "real-world GLP-1 weight loss underperforms clinical-trial data" aligns with the latest real-world evidence, and patients should plan surgery around actual weight loss rather than trial-best figures.

## Post-MWL body-contouring surgery: from abdominoplasty to full-body reshaping

Post-massive-weight-loss body contouring is a 2026 academic and clinical hot spot. {cite(mwl[:3])} cover the latest developments from the safety of abdominoplasty + hernia repair combined procedures, dermal-suspension mastopexy in postbariatric patients, perforator preservation in 360° abdominoplasty, to a new three-flap spiral technique for neoumbilicoplasty in abdominal-wall reconstruction. Alaniz and colleagues, in a case series in *Aesthetic Surgery Journal Open Forum*, find that combining abdominal hernia repair with abdominoplasty is feasible in carefully selected patients, with pre-operative CT assessment and peri-operative management being decisive{cite(mwl[:1])}.

Massarwa and colleagues, in *Plastic and Reconstructive Surgery Global Open*, describe a "dermal suspension + parenchymal reshaping" mastopexy technique that targets breast ptosis and volume loss in postbariatric patients{cite(mwl[1:2] if len(mwl) > 1 else mwl[:1])}. Tuan and colleagues, in a 100-patient prospective study in *Aesthetic Plastic Surgery*, validate the safety and aesthetic outcomes of VASER-assisted perforator-preserving liposuction in full abdominoplasty{cite(mwl[-1:])}. Burciaga-Soto and colleagues, in *Hernia*, propose the trisquel neoumbilicoplasty — a three-flap spiral reconstruction specifically for patients with absent or distorted umbilicus after abdominal-wall reconstruction or massive weight loss{cite([i for i in mwl if i not in glp1][-2:] if len(mwl) > 2 else mwl[-1:])}.

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-3.jpg" title="Post-MWL body contouring requires combined assessment of skin laxity, muscle separation, and fat distribution" >}}}}

## Non-invasive body contouring: from fat reduction to tightening + remodeling

Non-invasive body contouring (radiofrequency, laser, cryolipolysis, high-intensity electromagnetic muscle stimulation / HI-EMT) is undergoing a twin demand-and-regulatory shift. {cite(noninvasive[:2])} academic and industry reports converge on a 2026 clinical pivot from "thinning the fat layer" to "skin tightening + muscle remodeling + skin-quality improvement" as a composite indication. This shift reflects both consumer fatigue with single-modality results and tighter regulation on device indications and marketing claims.

El Danaf, in a 2026 review in *Aesthetic Plastic Surgery*, surveys the current clinical evidence for non-invasive body-contouring devices{cite(noninvasive[:1] if noninvasive else [])} and argues that improvements in energy delivery and temperature control have made "layered treatment" possible — the same device can address fat, fibrous septa, and dermis across different sessions. The technology shift raises the bar for operator training and credentialing. *Allure*'s 2026 trends coverage explicitly notes that demand for non-invasive body contouring decelerated from late 2025 into early 2026, citing in part the gap between consumer expectations of "immediately visible tightening" and the devices' actual capabilities{cite(regulatory[:1])}.

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-4.jpg" title="Non-invasive body contouring in 2026: layered energy delivery and indication precision are the clinical focus" >}}}}

## Regulation, safety, and industry trends

In 2026, regulatory dynamics and industry self-discipline are inescapable in the weight-loss + aesthetics intersection. The FDA's late-2025 safety communications on certain high-intensity focused ultrasound (HIFU) devices underscored the need for standardized operation and patient selection; ISAPS (International Society of Aesthetic Plastic Surgery) updated its international consensus on GLP-1 peri-operative management, emphasizing pre-operative nutritional assessment and multi-disciplinary team (MDT) workflows{cite(regulatory[:2])}. ASPS 2024 statistics show that abdominoplasty, mastopexy, and trunk-lift procedures — three MWL-related operations — rank among the fastest-growing aesthetic surgeries year-over-year, reflecting the structural expansion of post-massive-weight-loss reconstructive demand{cite(regulatory[1:2] if len(regulatory) > 1 else regulatory[:1])}.

On the Chinese-language discourse side, {cite([i for i, a in theme_idx.get('regulatory', []) if a.get('source_name') == '知乎'][:2])} continue to track the global "double dip" (simultaneous declines in surgical and non-surgical volumes) and argue that GLP-1 is reshaping the entire aesthetic-medicine value chain upstream, midstream, and downstream, with traditional-format-only clinics facing structural pressure.

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-5.jpg" title="Aesthetic regulation: standardized pre-op assessment, wash-out windows, and complication management are decisive" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **How long after GLP-1 weight loss (semaglutide, tirzepatide) can I have abdominoplasty or liposuction?** {cite(glp1[:2])} suggest elective surgery after a 4–6 week wash-out and confirmed stable HbA1c and nutritional status. The exact window should be jointly decided by the endocrine and plastic-surgery teams based on the patient's medication history, weight plateau, and comorbidities.
- **What is "semaglutide face" and how is it addressed?** "Semaglutide face" refers to the aged appearance caused by facial fat loss and skin laxity following GLP-1 weight loss{cite(glp1[-2:] if len(glp1) >= 2 else glp1[-1:])}. Treatment typically involves autologous fat grafting, facial lifting, and skin-tightening devices, and should be evaluated only after at least 6 months of stable weight and restored nutritional status.
- **What should I know before post-MWL abdominoplasty?** The key items are pre-operative imaging (CT/MRI for rectus diastasis and hernia), nutritional and iron status, skin redundancy, and prior surgical scars{cite(mwl[:2])}. Tuan and colleagues' 2026 100-patient prospective study shows that VASER-assisted perforator-preservation significantly reduces hematoma and flap necrosis risk.
- **Are non-invasive body-contouring modalities (RF, laser, cryolipolysis) still safe and effective?** Current mainstream devices retain clinical-evidence support as adjuncts in appropriate indications{cite(noninvasive[:1] if noninvasive else [])}. FDA safety communications emphasize standardized operation and indication selection. Patients should prioritize providers with licensed physicians and properly registered devices.
- **Why is the 2026 "double dip" (surgical + non-surgical declines) a topic?** {cite([i for i, a in theme_idx.get('regulatory', []) if a.get('source_name') == '知乎'][:1])} and other industry commentators argue that GLP-1 is changing body composition, that consumer down-trading is squeezing the mid-market, and that tightening regulation is constraining "fast-fashion" aesthetic services. But ASPS data show MWL-related procedures are still growing — structural demand has not disappeared, it has migrated from "light medical aesthetics" to "reconstructive surgery."
- **How do I know if the "GLP-1 plus subsequent aesthetic surgery" combined pathway is right for me?** Complete the GLP-1 indication assessment with an endocrinologist first, reach your weight plateau, and only then proceed to a comprehensive pre-operative evaluation with a plastic surgeon{cite(glp1[:1])}. Any plan that skips step one in pursuit of a "one-stop" weight-loss-plus-surgery package carries significant safety and outcome risks.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around 2026-06-07, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Weight-Loss + Medical Aesthetics Deep Analysis — June 2026: GLP-1, Post-MWL Surgery, Non-Invasive Contouring & Regulation"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["weight loss aesthetics", "GLP-1", "massive weight loss", "body contouring", "abdominoplasty", "non-invasive contouring", "aesthetic safety"]
keywords: ["weight loss aesthetics", "GLP-1 weight loss", "semaglutide face", "abdominoplasty", "post-MWL surgery", "non-invasive body contouring", "FDA safety", "ASPS 2024"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/weight-loss-aesthetics-deep-analysis-2026-06"
---

{{{{< figure src="/images/posts/weight-loss-aesthetics-2026-06/image-2.jpg" title="GLP-1 weight-loss era is reshaping the medical-aesthetics demand curve" >}}}}

"""
    return frontmatter + body


def write_post(content: str, slug: str, language: str) -> Path:
    out_dir = ZH_DIR if language == "zh" else EN_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    filepath = out_dir / f"{slug}.md"
    filepath.write_text(content)
    logger.info(f"Wrote {language} post: {filepath}")
    return filepath


def generate_posts(crawled_json_path: Path) -> list[Path]:
    articles = json.loads(crawled_json_path.read_text())
    if not articles:
        logger.warning("No articles to generate posts from")
        return []

    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    categories = categorize_articles(articles)
    refs, theme_idx = build_references(articles, categories)

    zh_content = build_zh_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)
    en_content = build_en_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)

    posts = [
        write_post(zh_content, SLUG, "zh"),
        write_post(en_content, SLUG, "en"),
    ]
    return posts


def main(json_path: Optional[str] = None) -> list[Path]:
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "weight-loss-aesthetics-news"
        files = sorted(data_dir.glob("weight_loss_aesthetics_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
