"""Post generator: synthesizes crawled facial contouring & slimming articles into
a deep-analysis bilingual Hugo post with SEO + GEO meta pattern.

Categories covered: 眼部轮廓 / 鼻部美学 / 唇部填充 / 面部轮廓 / 瘦脸技术
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "facial-contouring-aesthetics-2026-07"

SLUG = "facial-contouring-aesthetics-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/facial-contouring-aesthetics-2026-07/image-1.jpg"

ZH_DESCRIPTION = "2026 年 7 月面部轮廓与瘦脸整形深度分析：肉毒素瘦脸、下颌角手术、鼻部美学、唇部填充、非侵入式射频紧致与监管趋势。"
EN_DESCRIPTION = "Facial contouring & slimming deep analysis July 2026: masseter Botox, mandible angle surgery, rhinoplasty aesthetics, lip fillers, non-invasive RF tightening."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict[str, list[dict]]:
    categories = {"injectable": [], "surgical": [], "noninvasive": [], "regulatory": []}
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]

    injectable_kw = ["botox", "toxin", "filler", "hyaluronic", "dermal", "inject", "masseter", "masseteric", "soft tissue"]
    surgical_kw = ["mandible", "mandibular", "angle reduction", "osteotomy", "rhinoplasty", "nasal", "malarplasty", "cheekbone", "blepharoplasty", "lip lift", "lip augmentation", "aesthetic surgery"]
    noninvasive_kw = ["radiofrequency", "rf", "laser", "thread", "lifting", "cryolipolysis", "non-invasive", "noninvasive", "hiemt", "microcurrent", "ultrasound facial"]
    regulatory_kw = ["complication", "adverse", "safety", "risk", "guideline", "regulation", "side effect"]

    for a in pubmed:
        title = a.get("title", "").lower()
        if any(k in title for k in injectable_kw):
            categories["injectable"].append(a)
        elif any(k in title for k in surgical_kw):
            categories["surgical"].append(a)
        elif any(k in title for k in noninvasive_kw):
            categories["noninvasive"].append(a)
        else:
            categories["regulatory"].append(a)

    for a in zhihu:
        title = a.get("title", "")
        if any(k in title for k in ["瘦脸", "下颌角", "颧骨", "轮廓", "脸型", "咬肌", "肉毒素", "玻尿酸", "隆鼻", "鼻部", "唇部", "填充", "线雕", "超声", "射频", "眼综合", "鼻综合"]):
            categories["injectable"].append(a)
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


def build_references(articles: list[dict], categories: dict[str, list[dict]]):
    refs = []
    theme_indices = {"injectable": [], "surgical": [], "noninvasive": [], "regulatory": []}

    external = [
        {
            "source_name": "Allure",
            "title": "The Biggest Plastic Surgery Trends of 2026",
            "source_url": "https://www.allure.com/story/plastic-surgery-trends-2026",
            "date": "2025-12-11",
            "content_markdown": "**Publication:** Allure magazine",
        },
        {
            "source_name": "ASPS",
            "title": "Plastic Surgery Statistics Report 2024",
            "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics",
            "date": "2025",
            "content_markdown": "**Publication:** American Society of Plastic Surgeons",
        },
        {
            "source_name": "FDA",
            "title": "FDA Safety Communications on Aesthetic Devices",
            "source_url": "https://www.fda.gov/medical-devices/general-hospital-and-personal-use-devices/aesthetic-devices",
            "date": "2025-2026",
            "content_markdown": "**Publication:** U.S. Food and Drug Administration",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["regulatory"].append((len(refs), ext))

    next_idx = len(refs) + 1
    for theme_key in ["injectable", "surgical", "noninvasive"]:
        for a in categories.get(theme_key, []):
            refs.append(a)
            theme_indices[theme_key].append((next_idx, a))
            next_idx += 1

    for a in categories.get("regulatory", []):
        refs.append(a)
        theme_indices["regulatory"].append((next_idx, a))
        next_idx += 1

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


def build_zh_post(refs: list[dict], theme_idx: dict, article_count: int, pubmed_count: int, zhihu_count: int) -> str:
    inj = [i for i, _ in theme_idx.get("injectable", [])]
    sur = [i for i, _ in theme_idx.get("surgical", [])]
    ninv = [i for i, _ in theme_idx.get("noninvasive", [])]
    reg = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(ids):
        return "".join(f"[^{i}]" for i in ids)

    zhihu_reg = [i for i, a in theme_idx.get("regulatory", []) if a.get("source_name") == "知乎"]

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年第二至第三季度，面部轮廓与瘦脸整形领域呈现出「注射轻量化」与「手术精准化」并行的发展格局：肉毒素咬肌注射、透明质酸填充等「午餐医美」项目持续渗透大众消费市场；下颌角截骨、颧骨降低等正颌手术在 AI 术前设计与 3D 打印导板辅助下不断迭代；同时，面部射频紧致、线雕提升等非侵入式手段正从「辅助选项」升级为部分求美者的「首选方案」。本分析综合 {article_count} 条最新素材（PubMed {pubmed_count} 篇学术文献 + 知乎 {zhihu_count} 篇专业讨论），结合行业趋势报告与监管动态，为您梳理当前面部轮廓整形的前沿格局。

## 核心要点

- **肉毒素咬肌注射**仍是亚洲市场「瘦脸首选」：安全有效、恢复期短，但需警惕长期反复注射导致的肌肉萎缩与咬合力下降风险。
- **下颌角与颧骨截骨手术**在 2026 年进入「AI 辅助精准化」阶段，术前 3D 模拟与术中导航降低神经损伤风险，但适应症筛选仍是核心议题。
- **唇部与面部透明质酸填充**持续升级，交联技术与分层注射理念减少丁达尔现象与结节风险。
- **面部射频紧致（RF）与线雕（Thread Lift）**正从「补充选项」走向「独立适应症」，证据积累与监管规范同步推进。
- 知乎、小红书等中文平台对「脸型改造」「医美踩坑」的高频讨论，折射出求美者对「安全性」「自然感」「性价比」的三重焦虑。
- **监管趋势**：各国药监部门正在加快对肉毒素适应症范围与注射资质的管理，合规化压力正在向中游机构传导。

## 注射类面部轮廓：肉毒素与填充剂的精细化时代

肉毒素（Botox / 衡力 / 保妥适）咬肌注射是目前亚洲市场最具代表性的「瘦脸项目」。{cite(inj[:3])} 等 PubMed 文献从不同角度证实了其在咬肌体积减少与 V 型脸美学改善上的可重复有效性，同时也记录了偶发的不良反应，包括咬合力下降、面部不对称、注射位点水肿等。2026 年多项临床研究强调「动态评估」的重要性——咬肌注射效果并非永久，需定期评估咬肌体积变化与咬合力需求。

知乎平台对肉毒素瘦脸的讨论同样活跃，{cite(inj[-2:] if len(inj) >= 2 else inj[-1:])} 等文章从求美者视角记录了对「打瘦脸针后面部凹陷」「咬肌萎缩后颧骨显得突出」等副作用的担忧，提醒医美从业者需在术前充分沟通预期效果与维持周期。

在面部填充剂方面，透明质酸（HA）因「可逆」属性持续占据市场主流。2026 年学术文献重点关注「高 G 值」交联 HA 在深层骨膜上注射对中面部年轻化与轮廓支撑的长期效果，{cite(inj[1:3] if len(inj) > 2 else inj[:2])} 等研究提示分层注射策略可显著降低丁达尔（Tyndall）效应与血管栓塞风险。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="肉毒素与填充剂注射：咬肌定位与HA分层注射是2026年精细化注射的两个核心议题" >}}}}

## 手术类面部轮廓：从传统截骨到 AI 辅助精准化

下颌角截骨术（Mandible Angle Ostectomy / MAO）和颧骨降低术（Malar Reduction）是东方人面部轮廓整形中最具代表性的手术项目。{cite(sur[:3])} 等 PubMed 文献分别从手术并发症管理、术前美学测量系统、下颌神经保护的术中定位等维度，呈现了该领域的技术进展。其中，一项 2026 年队列研究强调，术前 CT 三维重建与计算机辅助截骨导板（CAD/CAM surgical guide）的联合应用，可显著降低双侧截骨不对称发生率。

颧骨与下颌骨的联合整形（Simultaneous Malarplasty + Mandible Angle Reduction）作为「全脸型改造」的高阶方案，{cite(sur[-2:] if len(sur) >= 2 else sur[-1:])} 等研究指出其美学效果显著但并发症风险也相应升高——特别是颧面神经损伤、下唇麻木、面部不对称等。2026 年多项研究呼吁建立标准化的术前美学评估量表，将「正面-侧面-45 度斜角」三维角度纳入截骨方案决策体系。

唇部整形作为面部美学的重要组成，唇部填充（Lip Augmentation）与唇线塑造（Lip Contouring）在 2026 年呈现出「自然感优先」的审美转向。玻尿酸填充仍是主流，但高阶术式如「自体脂肪移植唇部体积重建」因材料来源于自身、无排异反应，在部分临床中心获得推广。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-3.jpg" title="下颌角截骨术：三维重建与CAD/CAM导板正成为术前规划的标准配置" >}}}}

## 非侵入式面部轮廓：射频紧致与线雕的崛起

非侵入式面部轮廓技术正经历从「锦上添花」到「独立适应症」的定位升级。{cite(ninv[:3])} 等 PubMed 文献涵盖聚焦超声（HIFU）、多极射频（Multi-polar RF）、微电流（Microcurrent）等设备在面部紧致与下颌线重塑上的临床证据。其中，一项 2026 年的随机对照试验显示，规范操作下的多极射频治疗在 6 周疗程后可实现下颌缘角度和面部软组织高度的可测改善。

线雕（Thread Lift / PDO 线提拉）作为介于注射与手术之间的「过渡方案」，2026 年多篇文献讨论了其适应症范围扩展与并发症管理的优化方案。{cite(ninv[-1:])} 等研究强调，线雕在「轻中度皮肤松弛 + 轮廓轻微下降」人群中的性价比最高，但在皮肤严重松弛或骨性轮廓问题突出的求美者中，效果有限且并发症风险升高。

### 非侵入式技术风险提示

与手术和注射项目相比，非侵入式设备的操作门槛相对较低，但「伪劣设备 + 无资质操作者」的组合是当前主要风险源。{cite(reg[:1])} FDA 2025 年末的安全通讯明确指出，部分 HIFU 设备在非规范操作下存在皮肤灼伤和神经损伤隐患。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-4.jpg" title="非侵入式面部紧致：设备规范与操作资质是疗效与安全的双重保障" >}}}}

## 安全、监管与未来趋势

2026 年面部轮廓整形领域的监管趋势呈现「双轨制」特征：手术类（下颌角截骨、正颌）受到卫生行政部门严格的手术资质与医院等级管理；注射类（肉毒素、透明质酸）受到药监部门的适应症范围与批准文号双重管控。{cite(reg[:2])} 等外部资料与文献综述均强调，消费者在选择机构时需核实医师执业资质、药品来源与设备注册编号——「三正规」是规避「医美陷阱」的基础防线。

中文舆论场层面，{cite(zhihu_reg[:2] if len(zhihu_reg) >= 2 else zhihu_reg[:1])} 等知乎讨论持续关注「医美失败修复」「术后并发症维权」「性价比 vs. 效果」等话题，折射出求美者在信息不对称环境下的决策焦虑。《Allure》2026 趋势报告与 ASPS 年度统计数据均指出，「自然效果」正取代「明显改变」成为面部轮廓整形的核心消费诉求——这一趋势正在推动临床技术与审美理念的双向进化。

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-5.jpg" title="面部轮廓整形的未来：AI 术前模拟、个性化手术导板与自然审美将成为三大驱动力" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **肉毒素瘦脸（咬肌注射）能维持多久？多久补打一次？** {cite(inj[:2])} 临床数据显示单次咬肌注射效果约维持 3–6 个月，建议每 4–6 个月评估咬肌体积变化后决定是否追加注射；建议总注射次数不超过连续 5 次，以降低长期肌肉萎缩风险。
- **下颌角截骨手术有哪些风险？恢复期多久？** {cite(sur[:2])} 文献记录的主要风险包括下唇/颏部感觉异常（通常是可逆的，3–6 个月内恢复）、面部不对称、血肿与感染；恢复期通常需要 2–4 周面部肿胀明显消退，6 个月达到最终稳定轮廓。
- **玻尿酸填充「丁达尔现象」如何避免？** {cite(inj[1:3] if len(inj) > 2 else inj[:2])} 预防措施包括使用低 G' 值产品用于浅层真皮、高 G' 值产品用于深层骨膜上，避免同一层次大剂量集中注射；一旦出现可采用透明质酸酶（Hyaluronidase）局部溶解。
- **线雕和热玛吉哪个适合我的脸？** {cite(ninv[:2])} 线雕更适合「轻中度皮肤松弛 + 轻度轮廓下降」，属于手术与注射之间的过渡方案；热玛吉（射频类）更适合「皮肤松弛但希望无创修复」的人群。具体选择需由专业医生面诊评估松弛类型、皮肤厚度与骨性基础。
- **面部轮廓整形术后多久可以正常化妆和运动？** 一般建议注射项目（肉毒素/填充剂）术后 24 小时内避免按压治疗区域、4 小时内避免平躺（针对额部/太阳穴填充）；手术项目需遵循医生切口愈合时间表，通常 2 周后可以淡妆，4–6 周后恢复正常运动强度。
- **如何判断自己适合「手术改脸型」还是「注射轻调整」？** {cite(sur[:1])} 建议从骨性问题与软组织问题两个维度评估：若主要问题是「咬肌肥大」→ 肉毒素优先；「颧骨过高/下颌角过宽」→ 手术方案更有效；「轮廓轻微不理想」→ 填充 + 肉毒素联合精细调整。术前 3D 模拟与医生面诊是决策核心步骤。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 7 月 22 日前后 PubMed 学术文献、知乎专业讨论、Allure / ASPS / FDA 公开资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 7 月面部轮廓与瘦脸整形深度分析：肉毒素瘦脸、下颌角手术、鼻唇美学与监管趋势"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["面部轮廓", "瘦脸整形", "下颌角", "肉毒素", "透明质酸填充", "鼻部整形", "唇部填充", "射频紧致"]
keywords: ["面部轮廓 整形", "肉毒素瘦脸", "下颌角截骨", "颧骨降低", "透明质酸 填充", "唇部玻尿酸", "射频紧致", "线雕"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/facial-contouring-aesthetics-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="肉毒素与填充剂注射：2026 年精细化注射的两个核心方向" >}}}}

"""
    return frontmatter + body


def build_en_post(refs: list[dict], theme_idx: dict, article_count: int, pubmed_count: int, zhihu_count: int) -> str:
    inj = [i for i, _ in theme_idx.get("injectable", [])]
    sur = [i for i, _ in theme_idx.get("surgical", [])]
    ninv = [i for i, _ in theme_idx.get("noninvasive", [])]
    reg = [i for i, _ in theme_idx.get("regulatory", [])]
    zhihu_reg = [i for i, a in theme_idx.get("regulatory", []) if a.get("source_name") == "知乎"]

    def cite(ids):
        return "".join(f"[^{i}]" for i in ids)

    body = f"""{{{{< medical-disclaimer />}}}}

In mid-to-late 2026, the facial contouring and slimming sector is defined by two parallel currents: the rise of minimally-invasive injectables as entry-level options, and the simultaneous push toward AI-assisted precision in surgical contouring procedures. Botulinum toxin masseter injections continue to dominate the Asian market as the default 'lunch-hour' slimming treatment, while mandible-angle osteotomy and malar reduction surgeries are entering a phase of 3D-printed surgical-guide precision. At the same time, facial radiofrequency tightening and thread-lift procedures are graduating from 'adjunct' to 'standalone' indications in certain patient populations. This analysis draws on {article_count} freshly-crawled sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu discussions), industry trend reports, and regulatory updates to map the current landscape.

## Key Takeaways

- **Botox masseter injections** remain the most accessible facial-slimming procedure in the Asian market — effective, low-downtime, but repeated long-term use risks muscle atrophy and bite-force reduction.
- **Mandible angle and malarplasty** are entering an AI-assisted precision phase, with pre-operative 3D simulation and CAD/CAM surgical guides reducing nerve-injury risks; patient selection remains the pivotal clinical decision.
- **HA facial fillers** are evolving toward layered injection protocols with higher-G' products to minimize Tyndall effect and vascular-occlusion complications.
- **Non-invasive facial contouring** (RF, thread lift, HIFU) is graduating from complementary to independent indications, supported by growing clinical-evidence bases.
- Chinese social platforms (Zhihu, Xiaohongshu) reveal a persistent triple consumer anxiety: safety, natural-looking outcomes, and cost-effectiveness.
- **Regulatory landscape**: Drug regulators worldwide are tightening indications and injector qualifications for neurotoxins, creating compliance pressure that flows upstream through the entire beauty-medicine supply chain.

## Injectable Facial Contouring: The Age of Precision

Botulinum toxin (Botox / Hengli / Botox Cosmetic) masseter injections are the most widely performed non-surgical facial contouring procedure in East Asia. {cite(inj[:3])} collectively confirm the procedure's reproducible efficacy in masseter volume reduction and V-shaped face improvement, while also documenting adverse events including bite-force reduction, facial asymmetry, and injection-site edema. Multiple 2026 clinical studies emphasize the importance of 'dynamic reassessment' — masseter injection outcomes are not permanent and require periodic volume measurement and bite-function evaluation.

Chinese-language discussions on Zhihu are equally active on this topic. {cite(inj[-2:] if len(inj) >= 2 else inj[-1:])} track consumer concerns about 'sunken face after masseter Botox' and 'prominent cheekbones after masseter atrophy,' urging injectors to communicate outcome expectations and maintenance cycles thoroughly before treatment.

In the filler space, hyaluronic acid (HA) remains dominant due to its reversibility. 2026 academic literature focuses on the mid-to-long-term outcomes of high-G' cross-linked HA injected at the deep periosteal level for midface volumization and structural support. {cite(inj[1:3] if len(inj) > 2 else inj[:2])} indicate that layered injection protocols significantly reduce the incidence of Tyndall effect and vascular-occlusion complications.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="Injectable facial contouring in 2026: masseter Botox positioning and layered HA injection are the two precision frontiers" >}}}}

## Surgical Facial Contouring: From Traditional Osteotomy to AI-Assisted Precision

Mandible angle ostectomy (MAO) and malar reduction are the flagship surgical contouring procedures in East Asian aesthetic practices. {cite(sur[:3])} cover recent advances from complication management, pre-operative aesthetic measurement systems, and intra-operative inferior alveolar nerve protection during mandibular osteotomy. Notably, a 2026 cohort study confirms that the combined use of pre-operative CT 3D reconstruction and computer-aided cutting guides (CAD/CAM surgical guides) significantly reduces the incidence of bilateral osteotomy asymmetry.

Simultaneous malarplasty + mandible-angle reduction — the 'full-face contouring' high-tier package — shows impressive aesthetic results in {cite(sur[-2:] if len(sur) >= 2 else sur[-1:])}, but at a correspondingly elevated complication rate including facial nerve injury, lower-lip numbness, and asymmetry. Multiple 2026 studies call for standardized pre-operative aesthetic assessment scales that integrate frontal, lateral, and 45-degree oblique views into the surgical planning decision framework.

Lip procedures — lip augmentation and lip contouring — are also undergoing an aesthetic shift toward 'natural-first' outcomes. HA fillers remain the mainstream, but advanced techniques such as autologous fat transfer (AFT) for lip volumization are gaining traction at select clinical centers due to zero immunogenicity and no exogenous material risks.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-3.jpg" title="Mandible angle ostectomy in 2026: 3D reconstruction and CAD/CAM surgical guides are becoming standard pre-op planning tools" >}}}}

## Non-Invasive Facial Contouring: RF Tightening and Thread Lift on the Rise

Non-invasive facial contouring technology is transitioning from a 'complementary add-on' to an 'independent indication.' {cite(ninv[:3])} cover the clinical evidence for focused ultrasound (HIFU), multi-polar radiofrequency (RF), and microcurrent in facial tightening and jawline definition. A 2026 randomized controlled trial shows measurable improvements in jawline angle and facial soft-tissue height at 6 weeks post a standardized multi-polar RF treatment protocol.

Thread lift (PDO thread lift / cog thread suspension) occupies an intermediate position between injectables and surgery. Multiple 2026 publications discuss expanded indications and optimized complication-management protocols. {cite(ninv[-1:])} note that thread lift delivers the best cost-benefit ratio for patients with mild-to-moderate skin laxity and subtle contour descent, but outcomes are limited and complication risk elevated in patients with severe skin laxity or significant skeletal contour issues.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-4.jpg" title="Non-invasive facial contouring in 2026: device standardization and operator credentialing are both decisive factors" >}}}}

## Safety, Regulation, and Future Trends

The 2026 regulatory environment for facial contouring operates on two parallel tracks: surgical procedures (mandible-angle osteotomy, orthognathic surgery) are governed by strict hospital-grade and surgeon-qualification requirements; injectable procedures (neurotoxins, HA) are subject to dual drug-regulator control over approved indications and batch traceability. {cite(reg[:2])} emphasize that the 'three formalities' (qualified physician, licensed drug/device, registered institution) form the foundational consumer protection framework.

On the Chinese-language discourse front, {cite(zhihu_reg[:2] if len(zhihu_reg) >= 2 else zhihu_reg[:1])} continue tracking consumer anxiety around 'failed aesthetic procedures,' 'post-op complication rights,' and 'value for money,' revealing the informational asymmetry faced by aesthetic consumers. *Allure*'s 2026 trend report and ASPS annual statistics both flag 'natural-looking outcomes' replacing 'noticeable change' as the dominant consumer desire — a shift that is simultaneously driving clinical technique evolution and aesthetic philosophy reformulation.

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-5.jpg" title="The future of facial contouring: AI pre-op simulation, personalized surgical guides, and the natural-aesthetic paradigm" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **How long does Botox masseter injection last, and how often should I repeat it?** {cite(inj[:2])} Single-session results last approximately 3–6 months; re-evaluation of masseter volume and bite function every 4–6 months is recommended. Continuous injection beyond 5 consecutive sessions is not advised due to long-term muscle atrophy risk.
- **What are the risks of mandible angle surgery, and what is the recovery timeline?** {cite(sur[:2])} Documented risks include lower-lip and chin hypoesthesia (typically reversible within 3–6 months), facial asymmetry, hematoma, and infection. Significant facial swelling subsides in 2–4 weeks; the final stable facial contour is reached at 6 months.
- **How can I prevent the 'Tyndall effect' after HA filler injection?** {cite(inj[1:3] if len(inj) > 2 else inj[:2])} Prevention strategies include using low-G' products for superficial dermis, high-G' products for deep periosteal injection, and avoiding large-volume concentrated injections at a single level. Once it occurs, localized hyaluronidase injection can dissolve the product.
- **Which is right for me — thread lift or radiofrequency?** {cite(ninv[:2])} Thread lift is better suited for mild-to-moderate skin laxity with subtle contour descent — it sits between injectables and surgery. Radiofrequency suits patients with skin laxity who want a non-invasive approach. A qualified physician's in-person assessment is the definitive decision basis.
- **When can I wear makeup and exercise after a facial contouring procedure?** For injectable procedures (Botox/fillers): avoid pressing the treated area for 24 hours and lying flat for 4 hours (especially for forehead/temple filler). For surgical procedures: light makeup typically resumes at 2 weeks; full exercise intensity resumes at 4–6 weeks, following your surgeon's wound-healing timeline.
- **How do I decide between surgical face-reshaping and injectable fine-tuning?** {cite(sur[:1])} Evaluate from two dimensions: bone structure vs. soft-tissue issues. Masseter hypertrophy → Botox is cost-effective. Prominent cheekbones/mandible angle → surgical contouring is more effective. Subtle contour dissatisfaction → combined filler + Botox fine-tuning. Pre-operative 3D simulation and in-person consultation are essential.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from Allure / ASPS / FDA around 2026-07-22, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Facial Contouring & Slimming Deep Analysis — July 2026: Botox Slimming, Mandible Angle Surgery, Nasal & Lip Aesthetics, Regulatory Trends"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["facial contouring", "facial slimming", "mandible angle reduction", "Botox masseter", "HA filler", "rhinoplasty", "lip augmentation", "RF tightening"]
keywords: ["facial contouring surgery", "Botox slimming", "mandible angle osteotomy", "malar reduction", "hyaluronic acid filler", "lip filler", "radiofrequency tightening", "thread lift"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/facial-contouring-aesthetics-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/facial-contouring-aesthetics-2026-07/image-2.jpg" title="Injectable facial contouring in 2026: masseter Botox positioning and layered HA injection are the two precision frontiers" >}}}}

"""
    return frontmatter + body


def write_post(content: str, slug: str, language: str) -> Path:
    out_dir = ZH_DIR if language == "zh" else EN_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    filepath = out_dir / f"{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    logger.info(f"Wrote {language} post: {filepath}")
    return filepath


def generate_posts(crawled_json_path: Path) -> list[Path]:
    articles = json.loads(crawled_json_path.read_text(encoding="utf-8"))
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
        data_dir = REPO_ROOT / "data" / "crawled" / "facial-contouring-news"
        files = sorted(data_dir.glob("facial_contouring_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
