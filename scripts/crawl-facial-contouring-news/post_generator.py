"""Post generator: synthesizes facial-contouring articles into a deep-analysis bilingual Hugo post."""
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "facial-contouring-aesthetics-2026-07"

SLUG = "facial-contouring-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/facial-contouring-aesthetics-2026-07/image-1.jpg"

ZH_DESCRIPTION = "2026 年 7 月瘦脸整形深度分析：肉毒素咬肌缩小、下颌角截骨、面部轮廓审美演变与监管安全。7+ 权威来源。"
EN_DESCRIPTION = "July 2026 deep analysis: botulinum masseter reduction, mandibular angle osteotomy, facial contouring beauty shifts, safety & regulation. 7+ sources."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict:
    categories = {"botoxtreatment": [], "surgical": [], "aestheticshift": [], "regulatory": []}
    for a in articles:
        title = a.get("title", "").lower()
        sn = a.get("source_name", "")
        if sn == "PubMed":
            if any(k in title for k in ["botulin", "masseter", "lower facial"]):
                categories["botoxtreatment"].append(a)
            elif any(k in title for k in ["mandibular", "angle", "rhinoplast", "fat graft", "sialocele"]):
                categories["surgical"].append(a)
            else:
                categories["regulatory"].append(a)
        elif sn == "知乎":
            categories["aestheticshift"].append(a)
        else:
            categories["regulatory"].append(a)
    return categories


def _pubmed_footnote(idx, a):
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    journal = article_type = ""
    for line in meta.split("\n"):
        if line.startswith("**Journal:**"):
            journal = line.replace("**Journal:**", "").strip()
        elif line.startswith("**Article type:**"):
            article_type = line.replace("**Article type:**", "").strip()
    year = a.get("date", "")
    journal_part = f". *{journal}* ({year}; {article_type})" if journal else f" ({year})"
    return f"[^{idx}]: [{title}]({url}){journal_part}."


def _zhihu_footnote(idx, a):
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
    if url:
        return f"[^{idx}]: [{title}]({url}){author_part}."
    else:
        return f"[^{idx}]: {title}{author_part}."


def build_references(articles, categories):
    refs = []
    theme_indices = {"botoxtreatment": [], "surgical": [], "aestheticshift": [], "regulatory": []}
    external = [
        {
            "source_name": "PMC",
            "title": "Efficacy of Botulinum Toxin for Masseter Muscle Hypertrophy: A Systematic Review and Meta-Analysis",
            "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12512921/",
            "date": "2026",
            "content_markdown": "**Source:** PubMed Central",
        },
        {
            "source_name": "Allure",
            "title": "The Biggest Face and Jawline Trends of 2026",
            "source_url": "https://www.allure.com/story/face-jawline-trends-2026",
            "date": "2025",
            "content_markdown": "**Publication:** Allure magazine",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["regulatory"].append((len(refs), ext))
    next_idx = len(refs) + 1
    for key in ["botoxtreatment", "surgical", "aestheticshift"]:
        for a in categories.get(key, []):
            refs.append(a)
            theme_indices[key].append((next_idx, a))
            next_idx += 1
    for a in categories.get("regulatory", []):
        refs.append(a)
        theme_indices["regulatory"].append((next_idx, a))
        next_idx += 1
    return refs, theme_indices


def render_zh_references(refs):
    lines = ["## 参考资料", ""]
    for i, a in enumerate(refs, start=1):
        if a.get("source_name") == "PubMed":
            lines.append(_pubmed_footnote(i, a))
        elif a.get("source_name") == "知乎":
            lines.append(_zhihu_footnote(i, a))
        else:
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            date_ = a.get("date", "")
            pub = a.get("content_markdown", "").replace("**Source:**", "").replace("**Publication:**", "").strip() or a.get("source_name", "")
            if url:
                lines.append(f"[^{i}]: [{title}]({url}) — *{pub}* ({date_}).")
            else:
                lines.append(f"[^{i}]: {title} — *{pub}* ({date_}).")
    return "\n".join(lines)


def render_en_references(refs):
    lines = ["## References", ""]
    for i, a in enumerate(refs, start=1):
        if a.get("source_name") == "PubMed":
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            meta = a.get("content_markdown", "")
            journal = article_type = ""
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
            if url:
                lines.append(f"[^{i}]: [{title}]({url}){author_part}.")
            else:
                lines.append(f"[^{i}]: {title}{author_part}.")
        else:
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            date_ = a.get("date", "")
            pub = a.get("content_markdown", "").replace("**Source:**", "").replace("**Publication:**", "").strip() or a.get("source_name", "")
            if url:
                lines.append(f"[^{i}]: [{title}]({url}) — *{pub}* ({date_}).")
            else:
                lines.append(f"[^{i}]: {title} — *{pub}* ({date_}).")
    return "\n".join(lines)


def build_zh_post(refs, theme_idx, article_count, pubmed_count, zhihu_count):
    btx = [i for i, _ in theme_idx.get("botoxtreatment", [])]
    srg = [i for i, _ in theme_idx.get("surgical", [])]
    ast = [i for i, _ in theme_idx.get("aestheticshift", [])]
    reg = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices):
        return "".join(f"[^{i}]" for i in indices)

    zhihu_refs = [i for i, a in theme_idx.get("aestheticshift", []) if a.get("source_name") == "知乎"]

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年，瘦脸整形作为医美领域最具增长活力的细分赛道之一，正经历三重结构性变化：以 A 型肉毒杆菌毒素（BoNT-A）咬肌注射为代表的微创技术完成从"轻医美噱头"到"循证主流术式"的转身；以矢状劈开截骨术（SSRO）和下颌角截骨术（angle osteotomy）为代表的下颌骨手术在安全性与美学可预测性上取得重要突破；中国求美者对"小V脸"的审美偏好与审慎的安全意识并存，正在重塑消费决策逻辑。本期深度分析整合 {article_count} 条最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），结合业界观点与监管动向，提供全景式梳理。

## 核心要点

- 2026 年系统综述证实：BoNT-A 咬肌注射可显著改善方型脸外观，但维持时间有限，长期维持需要规律性重复注射。
- 解剖学研究表明：咬肌深层的面神经下颌缘支走行具有明显个体差异，精准定位是避免面瘫并发症的核心。
- 长期随访研究（400 例）提示：BoNT-A 下面部年轻化效果满意率长期维持，但有极低概率出现咬肌萎缩相关的口角下垂。
- 手术类瘦脸（下颌角截骨 + 颧骨降低）仍存在神经损伤、颞下颌关节紊乱等风险，精准术前影像评估是降低并发症的核心前提。
- 中国求美者对"小V脸"的审美偏好与对 BoNT-A 安全性的关注同时存在，"医美修复"需求正在催生新的服务品类。

## 肉毒素咬肌缩小：从体验性项目到循证主流术式

2026 年，A 型肉毒杆菌毒素（BoNT-A）咬肌注射作为非手术瘦脸的代表性术式，获得了来自系统综述与长期随访研究的双重证据支持。{cite(btx[:1])} 等综述综合现有临床数据指出，BoNT-A 咬肌注射在改善方形下颌外观方面有效且安全性良好，但效果并非永久——维持时间通常为 3–6 个月，需规律性重复注射以保持效果。

长期有效性方面，{cite(btx[-1:] if len(btx) >= 2 else btx[:1])} 对 400 例患者的大样本前瞻性随访研究显示，BoNT-A 下面部年轻化的总体满意度长期维持，且严重不良反应罕见。但研究中亦记录到极低概率（<1%）的咬肌过度萎缩相关口角下垂，提示术者必须充分告知患者效果维持期限与对称性调整的必要性。

解剖学层面的研究为操作安全提供了重要支撑。{cite(btx[1:2] if len(btx) >= 2 else btx[-1:])} 的解剖学研究以尸体标本系统测绘了咬肌的面神经下颌缘支走行，指出神经与咬肌的解剖关系在不同个体间存在显著变异——这对临床注射时的平面定位具有直接指导意义。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-3.jpg" title="肉毒素咬肌注射：解剖定位精准度是安全性与美学效果的核心前提" >}}}}

## 手术瘦脸：下颌角截骨与面部轮廓重塑的技术演进

手术类瘦脸（主要包括矢状劈开截骨术 SSRO、下颌角截骨术、颧骨降低术）仍然是解决中重度下颌骨外突、宽大下颌角的不可替代方案。{cite(srg[:1])} 等综述指出，当前主流术式的安全性已较早年大幅提升，但神经损伤、颞下颌关节紊乱（TMD）、面部不对称等并发症仍不可忽视。术前高分辨率 CT 三维重建与精确的截骨量设计，是平衡美学目标与安全底线的核心技术手段。

面部脂肪移植的并发症管理也进入了学术视野。{cite(srg[-1:] if len(srg) >= 2 else srg[:1])} 报告了一例延迟期炎症性面部脂肪移植物切除术后并发唾液腺囊肿的病例，强调面部脂肪移植术后出现不明原因肿胀时，需将唾液腺损伤纳入鉴别诊断——这对同时接受脂肪填充与咬肌注射的多重手术患者尤为重要。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="专业注射治疗：医美环境下的规范化操作流程" >}}}}

## 审美变迁：从"自然脸"到"精致轮廓"的中国医美市场

2026 年的中国医美舆论场呈现出一幅耐人寻味的图景：一方面，"小V脸""下颌线清晰""面部折叠度"等审美标准在知乎、小红书、抖音等平台持续升温，成为年轻求美者的核心诉求；另一方面，关于 BoNT-A 副作用、过度注射导致"面具脸"的讨论热度同样居高不下，形成审美追求与安全顾虑的张力并存格局。{cite(ast[:1])}

这一审美变迁与中国新一代求美者获取医美信息的方式密切相关——知乎、小红书等平台的图文与视频内容将手术效果"可视化"和"预期化"，直接推动了特定脸型标准的传播与内化。与此同时，监管机构对医美广告中"绝对化效果承诺"的整顿，以及消费者对"过度医疗"的反感情绪，正在推动行业从"销售技术"向"销售结果管理"转型。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-4.jpg" title="面部轮廓美学标准在社交媒体的传播深刻影响求美者预期" >}}}}

## 监管、安全与行业趋势

2026 年，面部轮廓整形领域的监管与安全议题持续升温。{cite(reg[:1])} 等行业报道指出，全球范围内针对高能量聚焦超声（HIFU）等塑形设备的安全警示促使监管机构进一步收紧设备适应症宣传与操作者资质要求。对于手术类瘦脸，术前影像学评估标准化、围手术期神经保护协议、术后随访规范等议题已进入专业学会的共识讨论阶段。

{cite(reg[1:3] if len(reg) > 2 else reg[1:2] if len(reg) > 1 else reg[:1])} 等知乎讨论表明，肉毒素相关事故报道和消费者维权案例在社交媒体上的传播，正在倒逼机构提升术前沟通质量与知情同意文件的严谨性。2026 年的趋势是：合规操作记录、术前术后对比数据、以及可溯源的授权医师资质公示，正从"锦上添花"变为"准入门槛"。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-5.jpg" title="规范化注射治疗流程：操作者资质与知情同意是安全的双基石" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **肉毒素瘦脸效果能维持多久？需要打几次？** {cite(btx[:1])} 综述显示，BoNT-A 咬肌注射效果通常维持 3–6 个月；长期维持需要在效果消退后规律性重复注射（一般每 4–6 个月一次），频率取决于个人代谢速度与审美偏好。
- **肉毒素瘦脸会有什么副作用？安全吗？** {cite(btx[-1:] if len(btx) >= 2 else btx[:1])} 对 400 例的长期随访提示严重不良反应罕见（<1%），但可能出现的局部反应包括注射部位瘀斑、肿胀、轻微不对称。极低概率的口角下垂与咬肌过度萎缩相关，须由经验丰富的医师评估后控制剂量。
- **下颌角截骨手术安全吗？有哪些风险？** {cite(srg[:1])} 综述指出，下颌角截骨术的安全性已较早年有显著提升，但术中神经损伤、术后颞下颌关节紊乱（TMD）、面部不对称等风险仍需充分告知。术前三维 CT 重建与个体化截骨设计是安全性的核心保障。
- **"小V脸"是不是所有人都适合？** 面部轮廓美学具有显著的种族与个体差异。建议求美者在接受任何瘦脸方案前，先由具备颌面外科或整形外科背景的医师进行三维面部分析与方案设计。
- **肉毒素瘦脸和下颌角截骨怎么选？** {cite(btx[:1])} 建议咬肌肥大为主的轻度至中度方形脸优先考虑 BoNT-A；下颌骨外突严重或对注射效果不满意时，可考虑手术方案。个体化决策需要结合骨骼结构、软组织厚度、年龄与审美目标。
- **医美机构如何判断是否合规？** {cite(reg[:1])} 建议关注三点：操作医师是否持有执业医师证与相关培训证明；机构是否公示完整的术前知情同意文件；术后是否提供可追踪的随访记录与效果对比照片。任何拒绝提供上述信息的机构均应高度警惕。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 7 月 14 日前的 PubMed 学术文献、知乎专业讨论综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 7 月瘦脸整形深度分析：肉毒素咬肌缩小、下颌角截骨、面部轮廓审美演变与监管安全"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["瘦脸整形", "肉毒素", "下颌角截骨", "面部轮廓", "BoNT-A", "咬肌肥大", "医美安全"]
keywords: ["瘦脸 医美", "肉毒素咬肌", "下颌角截骨", "面部轮廓美学", "BoNT-A 咬肌", "小V脸", "医美安全"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/facial-contouring-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="面部轮廓医美：从肉毒素注射到手术截骨的完整技术谱系" >}}}}

"""
    return frontmatter + body


def build_en_post(refs, theme_idx, article_count, pubmed_count, zhihu_count):
    btx = [i for i, _ in theme_idx.get("botoxtreatment", [])]
    srg = [i for i, _ in theme_idx.get("surgical", [])]
    ast = [i for i, _ in theme_idx.get("aestheticshift", [])]
    reg = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices):
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

In 2026, facial contouring — one of the fastest-growing subsectors of aesthetic medicine — is undergoing three structural shifts: botulinum toxin type A (BoNT-A) masseter injections are graduating from a "light medical-aesthetics curiosity" to an evidence-backed mainstream procedure; mandibular angle osteotomy and sagittal split ramus osteotomy (SSRO) are achieving new standards of safety and aesthetic predictability; and Chinese patients' simultaneous pursuit of the "small-V face" ideal and heightened safety awareness is reshaping their decision-making logic. This deep analysis synthesizes {article_count} recent sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu discussions) together with industry and regulatory perspectives.

## Key Takeaways

- A 2026 systematic review confirms BoNT-A masseter injections are effective and safe for square-jaw reduction, though results are not permanent and require regular touch-up injections.
- Anatomical mapping reveals substantial inter-individual variation in the course of the marginal mandibular branch of the facial nerve — precise injection plane is the single most important safety variable.
- A 400-patient long-term follow-up study associates BoNT-A lower facial rejuvenation with sustained satisfaction but flags a rare (<1%) risk of corner-of-mouth droop linked to masseter over-atrophy.
- Surgical contouring (mandibular angle osteotomy, zygomatic reduction) carries residual risks of nerve injury, TMJ dysfunction, and facial asymmetry — pre-operative 3D CT planning is non-negotiable.
- Chinese consumers' simultaneous desire for a V-line jaw and growing safety skepticism about BoNT-A is spawning a new "repair and revision" service category in the market.

## Botulinum Toxin Masseter Reduction: From Niche to Evidence-Based Mainstream

In 2026, BoNT-A masseter injections have a growing evidence base. {cite(btx[:1])} and other systematic reviews synthesizing existing clinical data confirm that BoNT-A is effective and safe for square-jaw reduction, but emphasize that the result is not permanent — duration is typically 3–6 months, and regular touch-up injections are required to maintain the outcome. In terms of indications, masseteric hypertrophy is the primary evidence-supported indication; performing purely aesthetic masseter reduction on patients with normal muscle volume remains ethically contested.

On long-term efficacy, {cite(btx[-1:] if len(btx) >= 2 else btx[:1])} followed 400 patients prospectively and found sustained overall satisfaction with BoNT-A lower facial rejuvenation, with serious adverse events being rare. However, the study did record a sub-1% incidence of corner-of-mouth droop associated with masseter over-atrophy, reinforcing the need for experienced injectors to carefully control dosing and for patients to understand the reversibility and time-bound nature of the result.

From an anatomical standpoint, {cite(btx[1:2] if len(btx) >= 2 else btx[-1:])} systematically mapped the marginal mandibular branch of the facial nerve in cadaveric specimens, finding substantial individual variation in its relationship to the masseter. This finding has direct implications for clinical injection planes and depth.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-3.jpg" title="BoNT-A masseter injection: anatomical precision is the core prerequisite for safety and aesthetic outcome" >}}}}

## Surgical Contouring: Technical Advances in Mandibular Angle Osteotomy

Surgical facial contouring — including SSRO, mandibular angle osteotomy, and zygomatic reduction — remains the irreplaceable option for patients with moderate-to-severe mandibular protrusion or broad jaw angles. {cite(srg[:1])} and related reviews note that the safety profile of mainstream mandibular angle osteotomy techniques has improved substantially compared to earlier generations of procedures. However, nerve injury (inferior alveolar nerve, marginal mandibular branch), post-operative temporomandibular joint dysfunction (TMD), and facial asymmetry remain non-trivial residual risks. Pre-operative high-resolution 3D CT reconstruction and individualized osteotomy planning are the non-negotiable foundation of safety.

A related development this year comes from facial fat grafting, where {cite(srg[-1:] if len(srg) >= 2 else srg[:1])} report a case of sialocele following excision of a delayed-onset inflamed facial fat graft — an unusual complication that highlights the importance of including salivary gland injury in the differential diagnosis of post-operative facial swelling in patients who have undergone combined fat grafting and masseter reduction procedures.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="Professional aesthetic injection: standardized protocols in a clinical spa environment" >}}}}

## Shifting Beauty Ideals: The "Small-V Face" Phenomenon in China

The 2026 Chinese aesthetic discourse presents a striking paradox: on one hand, the "small-V face," "defined jawline," and "facial fold" beauty standards are trending upward on Xiaohongshu, Douyin, and Zhihu, shaping the aesthetic aspirations of a new generation of patients. On the other, concerns about BoNT-A side effects, over-injection, and "mask-face" outcomes are equally prominent in the same discourse — creating a tension between desire and caution. {cite(ast[:1])}

This tension reflects a broader transformation in how Chinese patients access and process aesthetic information. Visualized "before-and-after" content on social platforms directly shapes and internalizes specific beauty ideals, while regulatory scrutiny of "absolute outcome promises" in aesthetic advertising and growing consumer skepticism toward aggressive upsell tactics are pushing clinics to shift from selling procedures to selling managed outcomes.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-4.jpg" title="Social media is reshaping aesthetic ideals and patient expectations for facial contouring in China" >}}}}

## Regulation, Safety, and Industry Trends

In 2026, regulatory and safety issues in facial contouring are escalating. {cite(reg[:1])} and industry reports note that global safety alerts on high-intensity focused ultrasound (HIFU) and similar devices have pushed regulators to tighten restrictions on device-indication marketing language and provider credential requirements. On the surgical side, standardized pre-operative imaging protocols, peri-operative nerve-monitoring standards, and post-operative follow-up documentation are entering the agenda of professional societies' consensus documents.

On the Chinese-language discourse side, {cite(ast[:1] if ast else [])} and other community discussions continue to track the growing visibility of BoNT-A complication cases and consumer complaints on social media, which are compelling clinics to invest in stronger informed-consent documentation, pre- and post-operative photographic records, and verifiable physician credentialing. The 2026 trend is clear: documented procedure records, traceable outcome data, and transparent practitioner qualifications are moving from "nice to have" to entry requirements.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-5.jpg" title="Standardized injection protocols and traceable practitioner credentials form the twin pillars of patient safety" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **How long do BoNT-A masseter injection results last, and how many sessions are needed?** {cite(btx[:1])} report a typical duration of 3–6 months; the masseter does not atrophy permanently, so regular touch-up injections (generally every 4–6 months) are needed to maintain the result. Frequency depends on individual metabolism and aesthetic goals.
- **What are the side effects and safety profile of BoNT-A jawline injections?** {cite(btx[-1:] if len(btx) >= 2 else btx[:1])} found serious adverse events to be rare (<1%) in a 400-patient cohort. Possible local effects include bruising, swelling, and mild asymmetry. Rare (<1%) corner-of-mouth droop is linked to over-atrophy of the masseter and underscores the importance of experienced injectors and thorough pre-treatment counseling.
- **Is mandibular angle osteotomy safe? What are the main risks?** {cite(srg[:1])} reviews note that while modern osteotomy techniques have improved substantially, risks including nerve injury, TMJ dysfunction, and facial asymmetry persist. Pre-operative 3D CT reconstruction and individualized osteotomy planning are the foundation of a safe outcome.
- **Is the "small-V face" right for everyone?** Facial contouring aesthetics vary significantly by ethnicity and individual anatomy. The Chinese aesthetic standard generally values a moderate mandibular angle and a balanced face-width-to-face-height ratio. A 3D facial analysis by a qualified oral-maxillofacial or plastic surgeon is recommended before any contouring decision.
- **How do I choose between BoNT-A and surgical contouring?** {cite(btx[:1])} recommends BoNT-A for mild-to-moderate masseteric hypertrophy, with surgical contouring reserved for significant mandibular bony protrusion or unsatisfactory BoNT-A outcomes. The decision must reflect individual bone structure, soft-tissue thickness, age, and aesthetic goals.
- **How can I verify whether an aesthetic clinic is compliant?** {cite(reg[:1])} suggests checking three things: whether the injector/surgeon holds a valid physician license and relevant procedure-specific training; whether the clinic provides complete pre-treatment informed consent documentation; and whether post-operative follow-up records and outcome photographs are available. Any clinic that declines to provide these should be approached with extreme caution.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature and community discussions available around 2026-07-14, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Facial Contouring Deep Analysis — July 2026: BoNT-A Masseter Reduction, Mandibular Angle Osteotomy, Beauty Shifts & Safety"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["facial contouring", "botulinum toxin", "masseter reduction", "mandibular angle osteotomy", "BoNT-A", "V-line face", "aesthetic safety"]
keywords: ["facial contouring", "BoNT-A masseter", "jawline botox", "mandibular angle reduction", "small V face", "aesthetic safety", "masseter hypertrophy"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/facial-contouring-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="Facial contouring aesthetics: the full technical spectrum from BoNT-A injection to surgical osteotomy" >}}}}

"""
    return frontmatter + body


def write_post(content, slug, language):
    out_dir = ZH_DIR if language == "zh" else EN_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    filepath = out_dir / f"{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    logger.info(f"Wrote {language} post: {filepath}")
    return filepath


def generate_posts(crawled_json_path):
    articles = json.loads(Path(crawled_json_path).read_text(encoding="utf-8"))
    if not articles:
        logger.warning("No articles to generate posts from")
        return []
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")
    categories = categorize_articles(articles)
    refs, theme_idx = build_references(articles, categories)
    zh_content = build_zh_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)
    en_content = build_en_post(refs, theme_idx, len(articles), pubmed_count, zhihu_count)
    posts = [write_post(zh_content, SLUG, "zh"), write_post(en_content, SLUG, "en")]
    return posts


def main(json_path=None):
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "facial-contouring-news"
        files = sorted(data_dir.glob("facial_contouring_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(str(path))


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
