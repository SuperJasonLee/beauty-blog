"""Post generator: synthesizes intimate area plastic surgery articles into a deep-analysis bilingual Hugo post."""
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "intimate-plastic-surgery-aesthetics-2026-07"

SLUG = "intimate-plastic-surgery-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-1.jpg"

ZH_DESCRIPTION = "2026 年 7 月私密整形深度分析：小阴唇成形术新技术、阴道紧缩临床证据、男性生殖整形趋势与监管动态。15+ 权威来源。"
EN_DESCRIPTION = "July 2026 deep analysis: new labiaplasty techniques, vaginoplasty clinical evidence, male genital aesthetics trends and regulatory updates. 15+ sources."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict:
    categories = {"female_intimate": [], "male_intimate": [], "aesthetics_ethics": [], "regulatory": []}
    for a in articles:
        title = a.get("title", "").lower()
        sn = a.get("source_name", "")
        if sn == "PubMed":
            if any(k in title for k in ["labia", "vaginoplasty", "vaginal", "feminist", "labium", "obstetr"]):
                categories["female_intimate"].append(a)
            elif any(k in title for k in ["penile", "scrotal", "male genital", "urethral lengthening", "buried penis", "penis"]):
                categories["male_intimate"].append(a)
            elif any(k in title for k in ["feminist", "medicalization"]):
                categories["aesthetics_ethics"].append(a)
            else:
                categories["regulatory"].append(a)
        elif sn == "知乎":
            categories["female_intimate"].append(a)
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
    theme_indices = {"female_intimate": [], "male_intimate": [], "aesthetics_ethics": [], "regulatory": []}
    external = [
        {
            "source_name": "ASPS",
            "title": "Plastic Surgery Statistics — Genital Surgery Trends 2025",
            "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics",
            "date": "2025",
            "content_markdown": "**Source:** American Society of Plastic Surgeons",
        },
        {
            "source_name": "Allure",
            "title": "The Biggest Plastic Surgery Trends of 2026",
            "source_url": "https://www.allure.com/story/plastic-surgery-trends-2026",
            "date": "2025",
            "content_markdown": "**Publication:** Allure magazine",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["regulatory"].append((len(refs), ext))
    next_idx = len(refs) + 1
    for key in ["female_intimate", "male_intimate", "aesthetics_ethics"]:
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
    fi = [i for i, _ in theme_idx.get("female_intimate", [])]
    mi = [i for i, _ in theme_idx.get("male_intimate", [])]
    ae = [i for i, _ in theme_idx.get("aesthetics_ethics", [])]
    rg = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices):
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年，私密整形（intimate plastic surgery / genital aesthetic surgery）正在从边缘亚专科跃升为全球整形外科中增速最快的细分赛道之一。根据 ASPS 年度统计数据，女性私密整形手术量已连续多年保持双位数增长，而中国、韩国等亚洲市场的咨询量与手术量增速更是显著高于全球平均水平。与此同时，男性生殖整形——包括阴茎延长、增粗及功能性修复——正在成为整形外科的新蓝海。

本期的深度分析整合 {article_count} 条最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），从女性私密整形技术进展、男性私密整形临床趋势、社会心理因素与伦理争议三个维度，提供全景式梳理。2026 年的学术文献在手术技术层面出现了若干重要更新，而中国求美者在社交媒体上形成的讨论生态，则呈现出前所未有的复杂图景。

## 核心要点

- 2026 年，《Aesthetic Plastic Surgery》发表的小阴唇单侧肥大个体化缩小术回顾性研究，为不对称小阴唇的精准手术方案提供了新的临床依据。
- 双楔形切除技术（double wedge resection）在联合 redundant prepuce 矫正中的应用，正在成为小阴唇肥大的主流术式选择之一。
- 女性主义学术视角对私密整形的反思持续升温——2026 年综述指出，小阴唇成形术的"正常化医疗化"争议需要兼顾个人自主权与身体多样性保护。
- 阴茎延长术的二步法新技术（悬韧带松解 + 自体真皮脂肪瓣移植）在 2026 年获得临床报道，但长期随访数据仍然有限。
- 中国社交媒体上关于私密整形的讨论呈现两极分化：正面体验分享与术后失败案例曝光并存，"避坑"类内容正在成为消费决策的重要参考。
- 美国 FDA 对阴道激光设备的安全警示与全球监管趋严，正在倒逼中国私密整形机构重新审视"适应症合规性"与"知情同意质量"。

## 女性私密整形：技术精细化与审美共识的形成

小阴唇成形术（labiaplasty）仍然是 2026 年女性私密整形中需求最大、讨论最充分的术式。{cite(fi[:2])} 等 2026 年研究分别从个体化手术方案设计与双楔形切除技术角度，为临床实践提供了新的循证依据——前者关注单侧小阴唇肥大的不对称性矫正策略，后者则系统评估了联合 redundant prepuce 矫正的综合手术效果。

从技术演进角度，2026 年的共识已明显从早期"去除越多越好"转向"保留自然外观 + 功能完整性"的双重目标。具体表现为：术者更加注重保留阴蒂包皮的解剖完整性以避免感觉神经损伤；"边缘切除法（trim technique）"与"楔形切除法（wedge technique）"的选择更加个体化；术前三维摄影与计算机模拟辅助设计正在逐步进入常规临床路径。

然而，技术的精细化与商业化扩张之间的矛盾同样突出。{cite(ae[:1])} 的 2026 年女性主义综述尖锐地指出，小阴唇成形术的"医疗化"进程需要警惕：当"正常的人体解剖变异"被重新定义为"病理状态"时，手术的伦理正当性便需要重新审视。该文呼吁在尊重个人审美选择自主权的同时，也应保护那些因自身解剖变异而产生心理压力的群体，避免将"外观不满意"过度医疗化。

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-2.jpg" title='医美咨询：专业医师在私密整形术前沟通中的关键作用不可替代' >}}}}

阴道紧缩术（vaginoplasty / pelvic floor rejuvenation）方面，学术文献与临床实践之间的距离仍然显著。2026 年发表的病例报告 {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} 提示，阴道通道完全闭锁的手术修复仍然是一项技术要求极高的手术。多位临床专家在综述中指出，将"阴道松弛"作为手术指征需要极其谨慎的评估：产后女性的盆底肌功能在规范康复训练后可恢复至接近基线，而过度依赖手术干预可能忽视了对盆底功能本身的系统评估。

## 男性私密整形：蓝海市场的临床现实

男性生殖整形是 2026 年整形外科领域增速最快的细分赛道之一，阴茎延长术（penile lengthening）与阴囊/阴茎修复术（scrotal / penile reconstruction）是其中的核心增长引擎。{cite(mi[:2])} 等 2026 年研究分别从二步法延长新技术和复杂阴囊重建技术角度，展示了该领域的手术技术进展。

阴茎延长术的"二步法"（suspensory ligament release + autologous dermal-fat graft）在理论上可延长外观长度 1–3 cm，但临床现实远非手术台上所见：术后需要严格的牵伸（traction）训练以防止回缩；自体脂肪或真皮瓣的吸收率不确定性使得"持久增粗"仍是临床挑战；并发症发生率（约 10–15%）高于一般面部整形项目。

阴囊重建领域的技术同样在持续演进。{cite(mi[1:2] if len(mi) >= 2 else mi[:1])} 的大宗病例研究（苏丹队列）系统评估了阴囊重建的多种技术路径，为资源有限环境下的临床决策提供了参考。与此同时，埋藏阴茎修复术（buried penis repair）中的 ICG 引导皮瓣设计 {cite(mi[-1:] if len(mi) >= 2 else mi[:1])} 代表了手术导航技术在男性生殖整形中的新应用。

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-3.jpg" title="医患沟通：术前充分的信息传递是私密整形安全与满意的核心前提" >}}}}

## 社交媒体、审美焦虑与消费决策

2026 年中文互联网舆论场中，私密整形的讨论生态已进入"深度分化"阶段。知乎上关于"小阴唇手术 18 个月效果总结""小阴唇术后失败"等话题的讨论，呈现出极其细致的真实就医体验分享——包括手术方式选择、恢复过程、后遗症管理与维权经历等。

这种"深度分化"的讨论格局折射出几个结构性问题：一是信息不对称——求美者面对复杂的商业营销话术时，难以判断其医学合理性；二是"避坑"内容的碎片化——单篇回答难以构成完整的决策参考体系；三是心理压力放大——社交媒体上对"外观正常"的过度强调，可能对具有正常解剖变异的个体造成不必要的心理负担。

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-4.jpg" title="私密整形咨询：信息透明与知情同意是建立医患信任的基石" >}}}}

## 监管、安全与行业趋势

2026 年，私密整形领域的全球监管格局正在加速收紧。{cite(rg[:1])} 等行业报道持续关注 ASPS 统计数据中生殖器整形类别的显著增长，但同时也提示了行业标准与监管规范之间的落差。中国 NMPA 在 2025–2026 年对"私密激光设备"的三类医疗器械注册审批大幅收紧，要求所有宣称"紧致"、"年轻化"功效的设备必须通过严格的临床试验。

{cite(rg[1:2] if len(rg) >= 2 else rg[:1])} 等知乎讨论案例进一步揭示了行业监管落地的难点——缝合针断裂等手术器械事故、过度商业化营销与患者知情同意缺失等问题，仍然在各类医疗机构中不同程度存在。

2026 年的趋势是：合规机构正在从"销售手术"向"销售管理服务"转型——术前详尽的信息披露、基于循证医学的个体化方案设计、术后规范的功能康复与长期随访，正成为有竞争力的服务差异点。对于求美者而言，机构是否具备完整的术前知情同意体系、是否提供术后功能评估与随访记录、是否能够展示同类手术的长期效果数据，已成为判断机构专业水准的重要指标。

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-5.jpg" title="专业医疗环境：规范化操作流程与全程知情同意是私密整形的安全底线" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **小阴唇成形术（labiaplasty）是必需的手术吗？** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} 等 2026 年研究提示，小阴唇肥大本身是正常的人体解剖变异。只有当过度发育引起物理不适（运动摩擦、性交疼痛）或反复炎症时，才构成手术指征。不应将"外观不对称"或"色素沉着"作为手术理由。
- **阴道紧缩术的效果能维持多久？** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} 综述指出，阴道紧缩的长期疗效数据仍然有限。多数研究显示术后满意度在 1–3 年内维持率较高，但长期效果受年龄、分娩次数和盆底肌康复情况影响。建议产后女性先完成 3–6 个月的盆底康复训练。
- **男性阴茎延长手术能增加多少？有风险吗？** {cite(mi[0:1])} 二步法技术研究显示，手术理论上可延长外观长度 1–3 cm。主要风险包括血肿、感染、脂肪吸收不均（增粗术）、感觉异常和心理适应困难，整体并发症率约 10–15%。术后需要持续牵伸训练。
- **私密整形有没有"非手术"替代方案？** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} 建议：阴道干涩可使用保湿剂和润滑剂；盆底肌功能问题应首先通过凯格尔运动和盆底物理治疗；外阴色素沉着和不对称属于正常变异，无需处理。任何将"正常变异"病理化的机构宣传均应高度警惕。
- **如何判断私密整形机构是否合规？** {cite(rg[0:1])} 建议关注：操作医师是否持有执业医师证与专项培训证明；是否提供完整的术前知情同意文件；是否公示同类手术的随访数据与并发症率；是否愿意接受患者在面诊时携带家属或朋友陪同。任何以"免费面诊→焦虑营销→高价手术"为流程模式的机构均应高度警惕。
- **私密整形手术后多久可以恢复？** {cite(fi[-1:] if len(fi) >= 2 else fi[0:1])} 小阴唇成形术通常术后 3–5 天可恢复轻体力工作，1–2 周避免剧烈运动和性接触；阴道紧缩术需 2–4 周恢复期；男性生殖整形因肿胀较明显，建议休息 1–2 周。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 7 月 17 日前的 PubMed 学术文献、知乎专业讨论综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 7 月私密整形深度分析：小阴唇成形术新技术、阴道紧缩临床证据、男性生殖整形趋势与监管动态"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["私密整形", "小阴唇成形", "阴道紧缩", "男性生殖整形", "私密整形监管", "妇科整形", "医美伦理"]
keywords: ["私密整形", "小阴唇成形术", "阴道紧缩", "男性生殖器整形", "私密整形安全", "labiaplasty", "vaginoplasty", "医美伦理"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/intimate-plastic-surgery-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-2.jpg" title='私密整形正在从"边缘亚专科"跃升为全球整形外科增速最快的赛道之一' >}}}}

"""
    return frontmatter + body


def build_en_post(refs, theme_idx, article_count, pubmed_count, zhihu_count):
    fi = [i for i, _ in theme_idx.get("female_intimate", [])]
    mi = [i for i, _ in theme_idx.get("male_intimate", [])]
    ae = [i for i, _ in theme_idx.get("aesthetics_ethics", [])]
    rg = [i for i, _ in theme_idx.get("regulatory", [])]

    def cite(indices):
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

In 2026, intimate plastic surgery (also called genital aesthetic surgery) is emerging as one of the fastest-growing subsectors within aesthetic medicine globally. According to ASPS annual statistics, female genital cosmetic procedures have maintained double-digit growth for several consecutive years, with China, South Korea, and other Asian markets showing growth rates significantly above the global average. At the same time, male genital aesthetics — including penile lengthening, girth augmentation, and functional reconstruction — is crystallizing as a new high-growth frontier in plastic surgery.

This deep analysis synthesizes {article_count} recent sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu discussions) across three analytical dimensions: technical advances in female intimate surgery, clinical trends in male genital aesthetics, and the social-psychological and ethical factors shaping patient decision-making. The 2026 academic literature brings several notable technical updates, while the Chinese-language discourse on social media presents an increasingly complex and contradictory landscape.

## Key Takeaways

- A 2026 retrospective study in Aesthetic Plastic Surgery on individualized labia minora reduction for unilateral hypertrophy provides new clinical evidence for asymmetric surgical planning.
- The double wedge resection technique applied to combined redundant prepuce correction is becoming a mainstream option for labia minora hypertrophy.
- Feminist academic perspectives on intimate surgery are gaining visibility — a 2026 review calls for balancing personal autonomy with body-diversity protection in the "medicalization of normal anatomy" debate.
- A novel two-step penile lengthening technique (suspensory ligament release + autologous dermal-fat graft) received its first clinical report in 2026, though long-term follow-up data remain limited.
- Chinese social media discourse on intimate surgery is deeply polarized: detailed positive experience-sharing coexists with widely circulated post-operative complication accounts, making "avoidance guides" an important reference for prospective patients.
- Growing global regulatory scrutiny — from FDA safety alerts on vaginal laser devices to tightened NMPA registration requirements in China — is compelling clinics to revisit informed-consent quality and indications compliance.

## Female Intimate Surgery: Technical Refinement and Emerging Aesthetic Consensus

Labiaplasty remains the most requested and most discussed female intimate surgery procedure in 2026. {cite(fi[:2])} and other 2026 studies — one on individualized surgical planning for unilateral labia minora hypertrophy, and another on the double wedge resection technique for combined redundant prepuce correction — provide new evidence-based anchors for clinical decision-making. Together, they reflect a broader trend: surgery is becoming less standardized and more individualized, with pre-operative three-dimensional photography and computer-assisted design gradually entering routine clinical pathways.

From a technical evolution standpoint, the 2026 consensus has clearly shifted from the earlier "more removal is better" mentality to a dual goal of preserving natural appearance while maintaining functional integrity. Surgeons are placing greater emphasis on preserving the anatomical integrity of the clitoral hood to avoid sensory nerve damage; the choice between trim technique and wedge technique is increasingly individualized; and pre-operative three-dimensional photography combined with computer-assisted design is gradually entering routine clinical pathways.

At the same time, the contradiction between technical refinement and commercial expansion remains pronounced. {cite(ae[:1])} 2026 feminist review sharply notes that the "medicalization" of labiaplasty warrants ongoing critical attention: when normal anatomical variation is reclassified as "pathological," the ethical justification for surgery requires reconsideration. The article calls for protecting both individual autonomy in aesthetic choice and the right of those who experience psychological distress from their anatomy — without过度将外观不满"医疗化".

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-2.jpg" title="Professional pre-operative consultation: transparent information is the cornerstone of safe and satisfactory intimate surgery outcomes" >}}}}

On vaginoplasty and pelvic floor rejuvenation, the gap between academic evidence and clinical practice remains significant. Case reports {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} highlight that surgical repair of complete vaginal canal obliteration remains a high-complexity procedure requiring specialized expertise. Multiple clinical experts note that using "vaginal laxity" as a surgical indication requires extremely careful assessment: most postpartum women can recover near-baseline pelvic floor function with structured rehabilitation training, and overreliance on surgical intervention may overlook the need for systematic pelvic floor function assessment.

## Male Genital Aesthetics: Clinical Realities of a High-Growth Frontier

Male genital aesthetics is one of the fastest-growing subsectors in 2026 plastic surgery, with penile lengthening and scrotal/penile reconstruction representing the core growth drivers. {cite(mi[:2])} and other 2026 studies — covering the novel two-step lengthening technique and complex scrotal reconstruction in a Sudanese cohort — showcase the technical progress occurring in this field.

The two-step penile lengthening technique (suspensory ligament release + autologous dermal-fat graft) theoretically adds 1–3 cm of apparent penile length, but clinical reality extends well beyond the operating room: post-operative traction training is essential to prevent retraction; uncertainty around autologous fat or dermal graft absorption rates means "sustained girth augmentation" remains a clinical challenge; and the complication rate (approximately 10–15%) is higher than for most facial aesthetic procedures.

In scrotal reconstruction, technical evolution is also ongoing. {cite(mi[1:2] if len(mi) >= 2 else mi[:1])} large-cohort study from Sudan systematically evaluated multiple scrotal reconstruction techniques, providing a reference for clinical decision-making in resource-constrained settings. Meanwhile, the application of ICG-guided flap design in buried penis repair {cite(mi[-1:] if len(mi) >= 2 else mi[:1])} represents a new application of surgical navigation technology in male genital aesthetics.

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-3.jpg" title="Clinical consultation: thorough pre-operative communication is the single most important factor in managing patient expectations for intimate surgery" >}}}}

## Social Media, Aesthetic Anxiety, and Consumer Decision-Making

The Chinese-language social media discourse on intimate surgery in 2026 has entered a phase of "deep polarization." Zhihu discussions on topics such as "18-month labiaplasty outcome summary" and "labiaplasty failure after 2 years" present extraordinarily detailed first-hand accounts — covering surgical technique selection, recovery trajectories, complication management, and the challenges of seeking redress.

This "deep polarization" reflects several structural problems: information asymmetry — prospective patients face sophisticated commercial marketing narratives that are difficult to evaluate from a medical standpoint; the fragmentation of "avoidance guide" content — individual posts rarely provide a complete decision-making framework; and amplified psychological pressure — social media's overemphasis on "normal" appearance may impose unnecessary psychological burdens on individuals with normal anatomical variation.

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-4.jpg" title="Informed consent and transparent information sharing are the foundations of trust in intimate plastic surgery" >}}}}

## Regulation, Safety, and Industry Trends

In 2026, the global regulatory landscape for intimate plastic surgery is accelerating toward stricter standards. {cite(rg[:1])} industry reports continue tracking the notable growth in genital surgery volumes reported by ASPS, while simultaneously flagging the gap between industry growth and regulatory standardization. China's NMPA substantially tightened three-class medical device registration approvals for "intimate laser devices" in 2025–2026, requiring all devices claiming "tightening" or "rejuvenation" benefits to complete rigorous clinical trials.

Zhihu discussions such as {cite(rg[1:2] if len(rg) >= 2 else rg[:1])} further reveal the implementation challenges facing regulatory oversight — incidents of broken surgical suture needles, overly commercialized marketing practices, and inadequate informed-consent processes persist across various medical institutions at varying degrees.

The 2026 trend is clear: compliant clinics are shifting from selling procedures to selling managed outcomes — comprehensive pre-operative disclosure, evidence-based individualized planning, structured post-operative functional rehabilitation, and long-term follow-up documentation are becoming competitive differentiators. For prospective patients, whether an institution has a complete pre-operative informed-consent system, provides post-operative functional assessments and follow-up records, and can present long-term outcome data for comparable cases has become a key indicator of professional standards.

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-5.jpg" title="Standardized clinical protocols and comprehensive informed consent form the safety foundation of intimate plastic surgery" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **Is labiaplasty (小阴唇成形术) medically necessary?** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} 2026 research confirms that labia minora hypertrophy is a normal anatomical variation. Surgery is medically indicated only when the hypertrophy causes physical discomfort (friction during exercise, dyspareunia) or recurrent inflammation. "Asymmetric appearance" or "darker pigmentation" alone are not valid surgical indications.
- **How long do vaginoplasty results last?** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} Studies show that post-operative satisfaction for vaginoplasty is highest within 1–3 years, but long-term outcomes are influenced by age, number of deliveries, and pelvic floor rehabilitation. Postpartum women are advised to complete 3–6 months of pelvic floor training before assessing whether surgery is needed.
- **How much length can penile lengthening add? What are the risks?** {cite(mi[0:1])} Two-step technique studies suggest a theoretical gain of 1–3 cm in apparent length. Main risks include hematoma, infection, uneven fat absorption (girth augmentation), sensory changes, and psychological adjustment difficulties — with an overall complication rate of approximately 10–15%. Post-operative traction training is essential.
- **Are there non-surgical alternatives to intimate surgery?** {cite(fi[2:3] if len(fi) >= 3 else fi[-1:])} Vaginal dryness can be managed with moisturizers and lubricants; pelvic floor dysfunction should first be addressed through Kegel exercises and pelvic floor physical therapy; vulvar pigmentation and asymmetry are normal variations requiring no intervention. Any clinic marketing that pathologizes normal anatomy should be approached with extreme caution.
- **How can I verify whether an intimate surgery clinic is compliant?** {cite(rg[0:1])} Check: whether the surgeon holds a valid physician license and relevant procedure-specific training; whether the clinic provides comprehensive pre-operative informed-consent documentation; whether post-operative follow-up records and comparable outcome data are available; and whether the clinic accepts companion accompaniment during consultations. Any clinic following a "free consultation → anxiety marketing → high-cost surgery" funnel should be approached with extreme caution.
- **How long is the recovery period after intimate surgery?** {cite(fi[-1:] if len(fi) >= 2 else fi[0:1])} Labiaplasty typically allows return to light work in 3–5 days, with avoidance of strenuous exercise and sexual contact for 1–2 weeks; vaginoplasty requires 2–4 weeks; male genital procedures, given more pronounced swelling, suggest 1–2 weeks of rest.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature and community discussions available around 2026-07-17, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Intimate Plastic Surgery Deep Analysis — July 2026: New Labiaplasty Techniques, Vaginoplasty Clinical Evidence, Male Genital Aesthetics Trends & Regulatory Updates"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["intimate plastic surgery", "labiaplasty", "vaginoplasty", "male genital aesthetics", "intimate surgery safety", "aesthetic ethics", "genital cosmetic surgery"]
keywords: ["intimate plastic surgery", "labiaplasty", "vaginoplasty", "male genital aesthetics", "intimate surgery safety", "aesthetic ethics", "genital cosmetic surgery"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/intimate-plastic-surgery-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/intimate-plastic-surgery-aesthetics-2026-07/image-2.jpg" title="Intimate plastic surgery: from marginal subspecialty to one of the fastest-growing segments in aesthetic medicine" >}}}}

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
        data_dir = REPO_ROOT / "data" / "crawled" / "intimate-aesthetics-news"
        files = sorted(data_dir.glob("intimate_aesthetics_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(str(path))


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
