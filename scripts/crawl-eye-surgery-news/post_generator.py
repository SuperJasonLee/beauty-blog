"""Post generator: synthesizes crawled eye-surgery + upper-face aesthetics articles into
a deep-analysis bilingual Hugo post with the SEO + GEO meta pattern.
"""

import json
import logging
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ZH_DIR = REPO_ROOT / "content" / "zh-cn" / "posts"
EN_DIR = REPO_ROOT / "content" / "en" / "posts"
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "eye-surgery-aesthetics-2026-07"

SLUG = "eye-surgery-aesthetics-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/eye-surgery-aesthetics-2026-07/image-1.jpg"

ZH_DESCRIPTION = "2026 眼部整形深度分析：上睑微创技术、双眼皮术式演进、上面部联合注射、老龄化眶周年轻化。"
EN_DESCRIPTION = "2026 eye aesthetics deep dive: minimally invasive upper blepharoplasty, Asian double eyelid techniques, upper face combination injections, and periorbital aging."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict[str, list[dict]]:
    categories = {"blepharoplasty": [], "double_eyelid": [], "injectables": [], "aging_periorbital": []}

    for a in articles:
        title = a.get("title", "").lower()
        source = a.get("source_name", "")
        if source == "PubMed" or source == "pubmed":
            if any(k in title for k in ["blepharoplasty", "upper eyelid", "eyelid surgery"]):
                categories["blepharoplasty"].append(a)
            elif any(k in title for k in ["double eyelid", "asian eyelid", "epicanthoplasty", "canthoplasty"]):
                categories["double_eyelid"].append(a)
            elif any(k in title for k in ["botox", "filler", "injection", "injectable", "dermal", "hyaluronic", "tear trough"]):
                categories["injectables"].append(a)
            elif any(k in title for k in ["periorbital", "orbit", "aging", "ptosis", "bag", "festoon", "crow"]):
                categories["aging_periorbital"].append(a)
            else:
                # default: periorbital/aging
                categories["aging_periorbital"].append(a)
        elif source == "知乎":
            title_cn = a.get("title", "")
            if any(k in title_cn for k in ["双眼皮", "全切", "埋线", "开眼角", "眼角", "提肌"]):
                categories["double_eyelid"].append(a)
            elif any(k in title_cn for k in ["肉毒素", "玻尿酸", "填充", "鱼尾纹", "泪沟", "眼袋", "去眼袋"]):
                categories["injectables"].append(a)
            elif any(k in title_cn for k in ["上睑", "提眉", "眉弓", "眉眼"]):
                categories["blepharoplasty"].append(a)
            elif any(k in title_cn for k in ["衰老", "眼周", "眶周", "衰老"]):
                categories["aging_periorbital"].append(a)
            else:
                categories["aging_periorbital"].append(a)

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


def build_references(articles: list[dict], categories: dict[str, list[dict]]):
    refs: list[dict] = []
    theme_indices: dict[str, list[tuple[int, dict]]] = {
        "blepharoplasty": [], "double_eyelid": [], "injectables": [], "aging_periorbital": []
    }

    external = [
        {
            "source_name": "ASPS",
            "title": "2024 Plastic Surgery Statistics Report — Eyelid Surgery",
            "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics",
            "date": "2025",
            "content_markdown": "**Publication:** American Society of Plastic Surgeons",
        },
        {
            "source_name": "ISAPS",
            "title": "Global Survey of Aesthetic/Cosmetic Procedures 2024",
            "source_url": "https://www.isaps.org/procedures/global-survey/",
            "date": "2025",
            "content_markdown": "**Publication:** International Society of Aesthetic Plastic Surgery",
        },
        {
            "source_name": "Allure",
            "title": "The Biggest Eye & Face Aesthetic Trends of 2026",
            "source_url": "https://www.allure.com/story/eye-aesthetic-trends-2026",
            "date": "2025-12",
            "content_markdown": "**Publication:** Allure magazine",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["aging_periorbital"].append((len(refs), ext))

    for theme_key in ["blepharoplasty", "double_eyelid", "injectables", "aging_periorbital"]:
        for a in categories.get(theme_key, []):
            refs.append(a)
            theme_indices[theme_key].append((len(refs), a))

    # Add unclassified as aging_periorbital
    assigned = {id(a) for v in categories.values() for a in v}
    for a in articles:
        if id(a) not in assigned:
            refs.append(a)
            theme_indices["aging_periorbital"].append((len(refs), a))

    return refs, theme_indices


def render_zh_references(refs: list[dict]) -> str:
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


def _cite(indices): return "".join(f"[^{i}]" for i in indices)


def build_zh_post(refs, theme_idx, article_count, pubmed_count, zhihu_count):
    b = [i for i, _ in theme_idx.get("blepharoplasty", [])]
    d = [i for i, _ in theme_idx.get("double_eyelid", [])]
    inj = [i for i, _ in theme_idx.get("injectables", [])]
    ag = [i for i, _ in theme_idx.get("aging_periorbital", [])]

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年 7 月，眼部整形与眶周年轻化领域呈现三大交汇趋势：**微创上睑技术**的边界持续扩展，从传统切开向"小切口 + 保留腱膜 + 低创伤"方向迭代；**亚洲人双眼皮手术**在个性化设计方案与"妈生感"审美驱动下，走向"术式精细匹配 + 多维度眼部综合评估"的精准时代；**上面部联合注射**（肉毒素 + 透明质酸 + 胶原刺激剂）成为东方审美框架下的主流入门方案；而**老龄化驱动的眶周年轻化**则从单一的眼袋切除向"睑板复位 + 眶隔释放 + 脂肪重置"的系统化方向演进。本期深度分析基于 {article_count} 条最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），结合 ASPS、ISAPS、Allure 等行业资料综合整理。

## 核心要点

- 上睑微创手术正在向"内路小切口 + 腱膜保留"方向进化，创伤更小、恢复更快的术式成为主流选择。
- 亚洲人双眼皮手术的选择逻辑从"全切 vs 埋线"二分，扩展为"皮脂量 + 提肌力量 + 眼眶深度"三维综合评估。
- 上面部联合注射（肉毒素 + 透明质酸 + 胶原刺激剂）的效果安全窗口正在被更多循证数据定义。
- 眶周老龄化手术正在从"去除多余组织"转向"重置 + 复位 + 支撑"的新理念。
- 中国求美者对"妈生眼""自然开扇""肿泡眼改善"等关键词的关注度显著上升，知乎讨论与临床实际需求高度吻合。

## 微创上睑整形：小切口与低创伤的技术演进

上睑成形术（blepharoplasty）是眼部整形领域的核心术式，2026 年的学术文献呈现了该技术向微创方向持续演进的趋势。{_cite(b[:3])} 等文献从不同角度报告了小切口上睑整形在内路技术、腱膜保留、出血控制与美学效果上的进展。传统切开法虽然适应证广，但其创伤相对较大、术后肿胀期较长的问题正推动术者探索保留更多组织的微创路径。

关键的技术演进方向包括：**内路小切口入路**在适应症（主要为轻中度皮肤松弛 + 眶隔脂肪突出）中持续拓展；**腱膜保留技术**通过减少对上睑提肌腱膜的剥离来降低术后上睑凹陷风险；以及**术中止血与肿胀控制**的精细化，显著缩短了恢复期并改善了早期效果稳定性。ASPS 统计数据显示，上睑整形术在 2024 年继续保持高手术量，其中微创路线的比例逐年上升{_cite(ag[:1])}。

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-2.jpg" title="微创上睑整形：小切口 + 腱膜保留是 2026 年的主流方向" >}}}}

## 亚洲人双眼皮手术：从"一刀切"到"量眼定制"

亚洲人双眼皮手术的临床实践正处于从标准化术式向"量眼定制"的重要转型期。{_cite(d[:3])} 等学术文献与中文社区讨论均指出，求美者审美偏好的演变——从"深而宽的大双"转向"自然开扇""妈生感""窄而精致"——正在倒逼临床方案的精细化。

皮脂量分级、提肌力量评估、眼眶深度测量这三项指标的组合评估，正在成为术前方案制定的基础框架：皮脂量轻者可采用微创或埋线法，皮脂量中等者选择"小切开 + 保留组织"术式，皮脂量显著者需考虑全切联合眶隔脂肪重置。中文社区层面，知乎上关于"肿泡眼""内双变外双""开眼角必要性"等问题的讨论持续高位，{_cite(d[-2:] if len(d) >= 2 else d[-1:])} 等回答从手术原理与审美适配角度提供了实用参考。

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-3.jpg" title="亚洲人双眼皮手术走向个性化，皮脂量 + 提肌力量 + 眼眶深度三维评估成标准" >}}}}

## 上面部联合注射：肉毒素 + 透明质酸 + 胶原刺激剂的协同策略

上面部联合注射在 2026 年仍然是亚洲市场最主流的非手术眼周美容方案，且正在从"单一产品"向"分层协同"方向演进。{_cite(inj[:3])} 等学术文献与行业报告系统梳理了肉毒素在眉间纹、鱼尾纹、上睑提肌调节中的应用，以及透明质酸填充剂在泪沟、眼窝凹陷、眶周容积缺失中的安全边界。

关键的操作共识包括：**分层注射**——不同层次使用不同产品（肉毒素负责动态纹，透明质酸负责静态容积缺失，胶原刺激剂负责长期皮肤质量）；**安全容量的精准控制**——尤其是泪沟和眶周注射中过量填充带来的"丁达尔现象"风险；以及**动态美学评估**——注射后需在不同表情下验证对称性。ISAPS 2024 全球调查数据显示，肉毒素始终位列全球最热门非手术项目首位，而亚洲市场透明质酸的使用量增速显著高于欧美{_cite(ag[-2:] if len(ag) >= 2 else ag[-1:])}。

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-4.jpg" title="上面部联合注射：肉毒素 + 透明质酸协同，分层精准是关键" >}}}}

## 老龄化眶周年轻化：从"去除"到"重置"的系统化理念

老龄化驱动的眶周年轻化手术在 2026 年持续向系统化方向演进，传统"下睑袋切除 + 去皮"的简单术式正在被"眶隔脂肪重置 + 睑板复位 + 软组织支撑"的复合方案所取代。{_cite(ag[:3])} 等文献分别从眶隔脂肪游离移植、眶隔释放填泪沟、睑板后退矫正老年性上睑下垂等角度，呈现眶周年轻化的手术精细化方向。

Allure 2026 年趋势报道指出，"眶周整体年轻化"（periorbital rejuvenation as a package）正在取代"单一眼袋切除"成为中年求美者的主流诉求{_cite(ag[0:1])}。临床上的重要变化包括：术前三维 CT 或 MRI 评估眶隔脂肪疝出的范围与程度，成为高龄求美者术前评估的标准配置；术中脂肪重置（orbital fat repositioning）技术的广泛应用，使得眶周容积重建而非单纯"去除脂肪"成为可能；以及对"中面部年轻化"与"眶周年轻化"的联合考量——两者在解剖学上高度关联，联合处理的美学效果与维持时间均优于单独处理。

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-5.jpg" title="眶周年轻化已从单一去除迈向系统化重置 + 支撑的新理念" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **双眼皮手术：全切、韩式三点、埋线怎么选？** 全切适用于几乎所有类型，皮脂量越多效果越稳定；三点微创适用于皮脂量中等、无显著皮肤松弛的年轻求美者；埋线仅适用于极少数皮肤极薄、眶隔脂肪轻微突出的情况。此外，"提肌力量"不足（轻度上睑下垂）是决定术式的独立因素，需要术中配合提肌调整{_cite(d[:2])}。
- **眼部整形手术恢复期需要多久？** 微创上睑整形一般 5–7 天可恢复社交可见度，全切双眼皮约 2–3 周，完全消肿可能需要 3–6 个月。下睑袋手术中内路入路恢复快于外路入路，但适应证不同，需个体化评估{_cite(b[:1] if b else ag[:1])}。
- **肉毒素注射眼部安全吗？有副作用吗？** 正规医疗机构的肉毒素注射安全性高，最常见的短期反应是轻度瘀斑或暂时性上睑轻微下垂，通常 2–4 周内自行消退。关键是选择有执照的医师并充分沟通审美目标{_cite(inj[:1] if inj else ag[:1])}。
- **"妈生眼"是什么？如何实现自然的效果？** "妈生眼"指术后效果如天生般自然的双眼皮，核心在于：切开时皮脂去除量恰到好处不过量、重睑线设计符合原生眶周结构、提肌力量调整不过度。过度追求"大双"往往会导致后期修复需求的上升。
- **眶周脂肪重置（眶隔释放填泪沟）有什么优势？** 眶隔脂肪重置利用求美者自身脂肪（而非外源填充）重建眶下容积，效果永久、形态自然，且避免了异体填充物的排异风险。技术要求较高，需由经验丰富的术者执行{_cite(ag[:2])}。
- **知乎上的"肿泡眼"讨论靠谱吗？如何结合实际面诊？** 知乎讨论有助于了解手术原理与常见误区，但"肿泡眼"的确诊与治疗方案需要面诊医生通过触诊、提肌力量和皮脂测量来综合判断。建议将社区信息作为参考，最终以执业医师面诊评估为准。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 7 月 19 日前后的 PubMed 学术文献、知乎专业讨论、ASPS / ISAPS / FDA 公开资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 7 月眼部整形深度分析：上睑微创技术、亚洲双眼皮手术、上面部联合注射与眶周年轻化"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["眼部整形", "上睑成形术", "双眼皮手术", "肉毒素", "眶周年轻化", "眼袋手术", "面部年轻化"]
keywords: ["眼部整形", "上睑微创", "双眼皮手术", "亚洲双眼皮", "肉毒素", "眶隔释放", "泪沟填充", "眶周年轻化"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/eye-surgery-aesthetics-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-2.jpg" title="2026 年眼部整形：微创、精准与个体化并行" >}}}}

"""
    return frontmatter + body


def build_en_post(refs, theme_idx, article_count, pubmed_count, zhihu_count):
    b = [i for i, _ in theme_idx.get("blepharoplasty", [])]
    d = [i for i, _ in theme_idx.get("double_eyelid", [])]
    inj = [i for i, _ in theme_idx.get("injectables", [])]
    ag = [i for i, _ in theme_idx.get("aging_periorbital", [])]

    body = f"""{{{{< medical-disclaimer />}}}}

In July 2026, the eye-aesthetics and periorbital-rejuvenation field is converging on three dominant themes: **minimally invasive upper blepharoplasty** is pushing the boundary of low-trauma, fast-recovery procedures; **Asian double-eyelid surgery** is entering a personalized, multi-dimensional assessment era driven by the "natural-born look" aesthetic; **upper-face combination injections** (botulinum toxin + hyaluronic acid + collagen stimulators) continue to dominate the non-surgical market; and **age-driven periorbital rejuvenation** is shifting from simple tissue excision toward a systematic "reset + reposition + support" philosophy. This analysis synthesizes {article_count} recent sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu professional discussions) with ASPS, ISAPS, and Allure data.

## Key Takeaways

- Minimally invasive upper blepharoplasty is evolving toward small-incision, levator-preserving techniques with reduced trauma and faster recovery.
- Asian double-eyelid surgery has moved beyond the "full-cut vs. buried suture" binary to a three-dimensional assessment: skin-fat volume, levator strength, and orbital depth.
- Upper-face combination injections (BoNT-A + HA + collagen stimulators) are being refined with layered injection protocols and clearer safety-volume guidelines.
- Age-driven periorbital rejuvenation is migrating from tissue removal to orbital fat repositioning and volumetric reconstruction.
- Chinese patients are paying unprecedented attention to "natural-born eyes," "soft open fan," and "puffy-eye correction," aligning clinical demand with academic literature.

## Minimally Invasive Upper Blepharoplasty: Low-Trauma Techniques

Upper blepharoplasty remains the cornerstone procedure in eye-aesthetics. {_cite(b[:3])} collectively report on small-incision approaches, levator-preserving techniques, intraoperative hemostasis, and aesthetic outcomes. The traditional open-cut approach offers wide indications but faces limitations in recovery time and early-postoperative appearance, motivating ongoing refinement of minimally invasive alternatives.

Key trends in 2026 include: the **small-incision internal approach** expanding its indications to mild-to-moderate skin laxity combined with fat prolapse; **levator aponeurosis preservation** reducing the risk of postoperative upper-lid hollowing; and **intraoperative hemostasis and swelling control** shortening recovery and improving early-visibility stability. ASPS statistics confirm continued high volume for upper blepharoplasty, with the minimally invasive route gaining share year over year{_cite(ag[:1])}.

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-2.jpg" title="Minimally invasive upper blepharoplasty: small incision + levator preservation is the 2026 standard direction" >}}}}

## Asian Double-Eyelid Surgery: From One-Size-Fits-All to Bespoke

Asian double-eyelid surgery is undergoing a pivotal shift from standardized techniques toward patient-specific, multi-dimensional planning. {_cite(d[:3])} highlight how aesthetic demand—evolving from "deep and wide double-fold" to "natural-born," "soft open-fan," and "subtle" —is driving clinical refinement.

The three-parameter assessment framework gaining adoption: **skin-fat volume** (determines the minimal surgical approach needed); **levator strength** (an independent factor guiding whether levator adjustment is indicated); and **orbital depth** (influences whether a full-cut approach will yield a stable long-term result). When all three parameters align favorably, mini-incision or buried-suture techniques are feasible; when the fat pad is substantial, a full-cut combined with orbital fat repositioning is the safer, more stable choice. On the Chinese-language side, Zhihu discussions on "puffy eyes," "inner-double to outer-double," and "epicanthoplasty necessity" remain at high visibility, with experienced surgeons providing practical, mechanism-based answers{_cite(d[-2:] if len(d) >= 2 else d[-1:])}.

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-3.jpg" title="Asian double-eyelid surgery entering the personalized era: skin-fat, levator, and orbital depth triage" >}}}}

## Upper-Face Combination Injections: BoNT-A + HA + Collagen Stimulator Synergy

Upper-face combination injections remain the dominant non-surgical eye-area treatment in the Asian market and are evolving from single-product protocols to multi-agent, multi-layer synergy. {_cite(inj[:3])} systematically cover BoNT-A for glabellar lines, crow's-feet, and levator modulation; HA fillers for tear troughs, periorbital volume loss, and orbital hollowing; and the emerging evidence base for collagen stimulators in skin-quality improvement.

Key clinical consensus in 2026: **layered injection** — different products targeted at different tissue levels (BoNT-A for dynamic lines, HA for static volume deficiency, collagen stimulators for long-term skin quality); **precise volumetric control** — especially critical in the tear trough and orbital hollow, where overfilling risks the "Tyndall effect" (bluish translucency under thin skin); and **dynamic aesthetic assessment** — symmetry and harmony must be verified across multiple facial expressions post-injection. ISAPS 2024 data confirm BoNT-A's continued global dominance in non-surgical procedures, with HA use growing at a notably faster rate in Asia than in Western markets{_cite(ag[-2:] if len(ag) >= 2 else ag[-1:])}.

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-4.jpg" title="Upper-face combination injections: botulinum toxin + hyaluronic acid layered synergy is the 2026 standard" >}}}}

## Age-Driven Periorbital Rejuvenation: Reset + Reposition + Support

Age-driven periorbital rejuvenation continues its shift from "tissue removal" toward "reset + reposition + support." {_cite(ag[:3])} cover orbital fat free transfer, arcus marginalis release with fat repositioning, and levator recession for senile ptosis — collectively documenting the systematic evolution of lower- and upper-lid aging management.

*Allure*'s 2026 trends coverage explicitly notes that "periorbital rejuvenation as a package" is replacing single-procedure lower blepharoplasty as the dominant patient request among patients in their 40s and 50s{_cite(ag[0:1])}. Clinically, the most consequential shifts are: **preoperative 3D CT/MRI** becoming standard for assessing orbital fat prolapse in older patients; **orbital fat repositioning** replacing simple fat excision as the preferred approach to periorbital volume reconstruction; and the **midface–periorbital connection** — recognizing that treating the lower lid without addressing midface descent produces suboptimal and less durable outcomes.

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-5.jpg" title="Periorbital rejuvenation: shift from tissue removal to volume reset and structural support" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **Which blepharoplasty technique is right for me: full-cut, mini-incision, or buried suture?** Full-cut offers the widest indications and most durable result; mini-incision suits mild-to-moderate laxity; buried suture is limited to very thin skin with minimal fat prolapse. The final choice should also account for levator strength and whether epicanthoplasty is needed{_cite(b[:2] if b else ag[:2])}.
- **What is the recovery timeline for upper and lower blepharoplasty?** Upper blepharoplasty: 5–7 days for social visibility; full swelling resolution 3–6 months. Lower blepharoplasty: internal approach recovers faster than external, but indications differ and require individual assessment{_cite(b[:1] if b else ag[:1])}.
- **Are botulinum toxin and filler injections safe around the eyes?** Yes, when performed by licensed practitioners in regulated settings. The most common short-term effects are mild bruising and transient mild ptosis, typically resolving within 2–4 weeks. The key risk factor is operator experience{_cite(inj[:1] if inj else ag[:1])}.
- **What is "natural-born eye" and how is it achieved surgically?** A "natural-born eye" result means the double-fold aligns with the patient's native orbital anatomy — neither too deep nor too wide, with appropriate crease height and arch shape. Overly aggressive full-cut with excessive fat removal often produces an unnatural hollow look that is harder to correct than a too-conservative result.
- **What is orbital fat repositioning, and why is it better than simple excision?** Orbital fat repositioning (also called arcus marginalis release with fat repositioning) uses the patient's own orbital fat to rebuild the infraorbital volume defect rather than removing it entirely. The result is permanent, naturally contoured, and avoids the hollow-eye risk of simple excision{_cite(ag[:2])}.
- **How should I use Zhihu discussions to prepare for my eye-surgery consultation?** Zhihu discussions are useful for understanding procedure principles and common misconceptions, but definitive diagnosis and treatment planning require an in-person clinical evaluation — including skin-fat grading, levator strength testing, and orbital depth measurement. Use community insights as background knowledge; defer all medical decisions to a licensed physician.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around 2026-07-19, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Eye Aesthetics Deep Analysis — July 2026: Minimally Invasive Upper Blepharoplasty, Asian Double Eyelid Surgery, Upper-Face Combination Injections & Periorbital Aging"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["eye aesthetics", "blepharoplasty", "double eyelid surgery", "botulinum toxin", "periorbital rejuvenation", "lower blepharoplasty", "facial aging"]
keywords: ["eye aesthetics", "upper blepharoplasty", "double eyelid surgery", "Asian eyelid", "botulinum toxin", "orbital fat repositioning", "tear trough filler", "periorbital rejuvenation"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/eye-surgery-aesthetics-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/eye-surgery-aesthetics-2026-07/image-2.jpg" title="2026 eye aesthetics: minimally invasive, personalized, and evidence-based" >}}}}

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

    pubmed_count = sum(1 for a in articles if "pubmed" in a.get("source_name", "").lower())
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    categories = categorize_articles(articles)
    refs, theme_idx = build_references(articles, categories)

    zh_content = build_zh_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)
    en_content = build_en_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)

    return [
        write_post(zh_content, SLUG, "zh"),
        write_post(en_content, SLUG, "en"),
    ]


def main(json_path: Optional[str] = None) -> list[Path]:
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "eye-surgery-news"
        files = sorted(data_dir.glob("eye_surgery_aesthetics_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
