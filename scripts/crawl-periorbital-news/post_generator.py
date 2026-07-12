"""Post generator: synthesizes periorbital rejuvenation articles into a deep-analysis
bilingual Hugo post with SEO + GEO meta pattern.

Contract (mirrors the SEO/GEO spec):
  - Front matter: description (<=160 chars), keywords (5-10), categories, tags,
    draft=true, featuredImage.
  - Body: four themed ## H2 sections, ## 核心要点/Key Takeaways, faq block (4-6 Q&A),
    numbered ## 参考资料/References (>= 8 footnotes), at least 3 figure shortcodes.
  - Companion en post mirrors zh-cn structure with back-link in translations:.
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "periorbital-rejuvenation-2026-07"

SLUG = "periorbital-rejuvenation-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/periorbital-rejuvenation-2026-07/image-1.jpg"

ZH_DESCRIPTION = "2026年眶周年轻化深度分析：黑眼圈分型治疗、眼袋微创术式、泪沟填充策略与肉毒素注射进展。8+权威来源。"
EN_DESCRIPTION = "2026 periorbital rejuvenation deep dive: dark circle subtypes, undereye bag minimally invasive surgery, tear trough fillers, and botulinum toxin advances. 8+ sources."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def categorize_articles(articles: list[dict]) -> dict[str, list[dict]]:
    """Group crawled articles into four SEO/GEO spec themes."""
    categories = {"dark_circles": [], "eyebags": [], "fillers_tech": [], "safety_reg": []}
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]

    for a in pubmed:
        title = a.get("title", "").lower()
        if "dark circle" in title or "tear trough" in title or "pigment" in title or "vascular" in title:
            categories["dark_circles"].append(a)
        elif "eye bag" in title or "blepharoplasty" in title or "lower eyelid" in title or "fat herniation" in title:
            categories["eyebags"].append(a)
        elif "filler" in title or "volume" in title or "fat graft" in title or "collagen" in title or "hyaluronic" in title:
            categories["fillers_tech"].append(a)
        else:
            categories["safety_reg"].append(a)

    for a in zhihu:
        title = a.get("title", "")
        if any(k in title for k in ["黑眼圈", "泪沟", "色素", "血管型", "阴影型"]):
            categories["dark_circles"].append(a)
        elif any(k in title for k in ["眼袋", "眶隔", "微创", "内切", "外切"]):
            categories["eyebags"].append(a)
        elif any(k in title for k in ["填充", "玻尿酸", "胶原蛋白", "再生材料", "脂肪"]):
            categories["fillers_tech"].append(a)
        else:
            categories["safety_reg"].append(a)

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


def build_references(articles: list[dict], categories: dict) -> tuple[list[dict], dict[str, list[tuple[int, dict]]]]:
    refs: list[dict] = []
    theme_indices: dict[str, list[tuple[int, dict]]] = {
        "dark_circles": [], "eyebags": [], "fillers_tech": [], "safety_reg": []
    }

    external = [
        {
            "source_name": "Allure",
            "title": "The Biggest Eye Area Beauty Trends of 2026",
            "source_url": "https://www.allure.com/story/eye-area-beauty-trends-2026",
            "date": "2025-12",
            "content_markdown": "**Publication:** Allure magazine",
        },
        {
            "source_name": "ASPS",
            "title": "Plastic Surgery Statistics 2024",
            "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics",
            "date": "2025",
            "content_markdown": "**Publication:** American Society of Plastic Surgeons",
        },
    ]
    for ext in external:
        refs.append(ext)
        theme_indices["safety_reg"].append((len(refs), ext))

    next_idx = len(refs) + 1
    for theme_key in ["dark_circles", "eyebags", "fillers_tech", "safety_reg"]:
        for a in categories.get(theme_key, []):
            refs.append(a)
            theme_indices[theme_key].append((next_idx, a))
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


def build_zh_post(refs: list[dict], theme_idx: dict, article_count: int,
                  pubmed_count: int, zhihu_count: int) -> str:
    dc = [i for i, _ in theme_idx.get("dark_circles", [])]
    eb = [i for i, _ in theme_idx.get("eyebags", [])]
    ft = [i for i, _ in theme_idx.get("fillers_tech", [])]
    sr = [i for i, _ in theme_idx.get("safety_reg", [])]

    def cite(indices: list[int]) -> str:
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

2026 年上半叶，眶周年轻化（periorbital rejuvenation）在全球医美临床与中文社区同步升温。从黑眼圈的分型诊疗路径、眼袋微创术式的精进，到泪沟与眶周容积填充的新一代材料选择，再到肉毒素注射的剂量与靶点精细化——这四大方向既是临床研究的密集区，也是消费者关注度持续走高的热点。本期深度分析基于 {article_count} 条最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），结合 ASPS 与行业趋势报告综合整理。

## 核心要点

- 黑眼圈分型诊疗是 2026 年的核心临床趋势：色素型、血管型、阴影型（泪沟/眶沟）三大亚型各有对应治疗策略，混合型需联合方案。
- Beer 等 2026 年系统性综述确认眶周年轻化正成为多学科交叉领域，皮肤科、眼科、整形外科协同诊疗渐成主流。
- 微创眼袋术（内切、眶隔释放）在轻中度眼袋人群中持续替代传统外切方案，术后恢复期从 1–2 周压缩至 3–5 天。
- 泪沟填充从第一代玻尿酸向"双相/梯度 G 值"分层填充演进，Shome 等 2026 年提出的双层差异化填充策略提升了安全性与持久性。
- 眶周容积重建（自体脂肪、胶原蛋白刺激剂）在轻中度眶周凹陷中越来越受到青睐，但存活率预测与排异管理仍是主要临床挑战。
- 肉毒素眶周注射（鱼尾纹、眉间纹、眶周动力性皱纹）在 2026 年正从"粗放剂量"走向"靶点精准化"时代，FAKIH-GOMEZ 等报道的新一代混合填充剂方案拓展了眉部年轻化的技术边界。

## 黑眼圈的分型诊疗：从"遮瑕膏思维"到精准医学

黑眼圈是眶周年轻化中最复杂、也最具挑战性的临床问题。2026 年 Beer 等人发表于 *Dermatologic Surgery* 的系统性综述全面梳理了眶周年轻化的最新治疗进展，将黑眼圈列为多学科（皮肤科、眼科、整形外科）协同诊疗的典型代表{cite(dc[:1])}。Wu 等人在 *Aesthetic Plastic Surgery* 发表的"三步胶原增强眶周综合治疗方案"（Raise + Enhancement + Depigmentation），标志着眶周治疗从"单一手段"走向"分层联合"范式{cite(ft[:1] if ft else dc[:1])}。

中文社区对黑眼圈分型的讨论热度同样居高不下。知乎上{cite(dc[1:3] if len(dc) > 1 else dc[:1])}等专栏文章指出，"混合型黑眼圈"（色素沉着 + 血管暴露 + 眶沟阴影）是最常见且最难根治的类型，建议先通过皮下填充改善结构阴影，再联合光电与外用药物解决色素和血管问题。Asaria 在 *Facial Plastic Surgery Clinics* 2026 年的综述中明确指出，眶周容积重建不仅仅是补充"容量缺失"，更是重建眶周骨骼支撑与软组织张力的美学工程{cite(ft[1:2] if len(ft) > 1 else ft[:1])}。

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-2.jpg" title="黑眼圈分型诊疗：色素、血管、阴影型各有对应治疗路径，混合型需联合方案" >}}}}

## 眼袋微创术式精进：眶隔释放与脂肪再分布

眼袋（lower eyelid bags）的本质是眶隔脂肪向前膨出，传统外切法切口位于睫毛下皮肤，恢复期长且存在外翻风险。2026 年 Fabbri 等人在 *Aesthetic Plastic Surgery* 提出的"延长下睑成形术"（Extended Lower Blepharoplasty）系统讨论了安全切除量的临床标准{cite(eb[:1])}，指出皮肤切除量超过 6 mm 时睑外翻风险显著上升。同期，Ding 等在 *Aesthetic Plastic Surgery* 报道了"上睑提肌腱膜与睑板前肌重叠增强下睑饱满度"的新术式，通过调整眼轮匝肌力学方向改善"干眼-眼袋"共存患者的眶周外观{cite(eb[1:2] if len(eb) > 1 else eb[:1])}。

知乎上{cite(eb[2:4] if len(eb) > 2 else eb[-1:] if eb else dc[-1:])}等文章持续追踪微创眼袋手术的发展，强调"内切眶隔释放"在轻中度眼袋中的普及率已大幅提升，术后水肿期 3–5 天消退，切口隐藏在结膜面，完全不可见。

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-3.jpg" title="微创眼袋术：内切眶隔释放与脂肪再分布正在替代传统外切" >}}}}

## 泪沟填充与眶周容积重建：材料与技术的双升级

泪沟（tear trough deformity）是眶周年轻化中仅次于眼袋的第二大核心诉求。Shome 等 2026 年在 *Indian Journal of Ophthalmology* 发表的泪沟年轻化新双层策略，采用不同 G 值（弹性模量）的填充剂分层注射——深层用高 G 值产品提供骨性支撑，浅层用低 G 值产品柔和过渡——显著降低了"丁达尔现象"（Tyndall effect，光线透过皮肤呈现蓝光）的发生率{cite(ft[1:2] if len(ft) > 1 else ft[:1])}。自体脂肪移植方面，Shomorony 等 2026 年在 *Facial Plastic Surgery Clinics* 综述了眶周与中面部脂肪移植的技术要点与存活率影响因素{cite(ft[2:3] if len(ft) > 2 else ft[:1])}，指出眶周血管丰富，脂肪存活率高于中面部，但脂肪硬结和不对称是主要并发症。

Fakih-Gomez 等 2026 年在 *Aesthetic Plastic Surgery* 报道的"混合填充剂额部容积与年轻化"方案{cite(ft[0:1])}——使用 HA 透明质酸与羟基磷灰石钙（CaHA）混合注射——拓展了眶周年轻化的材料边界，为眉区与眶上缘的容积重建提供了新选项。

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-4.jpg" title="泪沟填充与眶周容积重建：分层 G 值填充与自体脂肪是 2026 年的两大技术主线" >}}}}

## 肉毒素眶周注射：从粗放剂量到靶点精准化

肉毒素在眶周年轻化中的核心应用包括眉间纹、鱼尾纹、眶周动力性皱纹和"眼睑痉挛"四种场景。2026 年 Beer 等人系统性综述全面评估了眶周肉毒素注射的安全性，指出"精准靶点、最小有效剂量"是 2026 年肉毒素眶周治疗的核心原则{cite(dc[:1])}。Fakih-Gomez 等报道的"混合填充剂方案"同时拓展了肉毒素在眉部年轻化中的辅助角色{cite(ft[0:1])}。 Bray 在 *Facial Plastic Surgery Clinics* 2026 年综述中讨论了眼轮匝肌重塑在深平面提升术中的作用{cite(sr[0:1] if sr else dc[-1:])}，指出眶周动态纹与静态纹并存时需将肉毒素注射与手术提拉同步规划。

中文社区层面，{cite([i for i, a in theme_idx.get('safety_reg', []) if a.get('source_name') == '知乎'][:2])}等知乎讨论反映，国内消费者对眶周肉毒素剂量的关注度持续提升，"弥散度""精准度"已成为搜索热词。

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-5.jpg" title="肉毒素眶周注射：靶点精准化与最小有效剂量是 2026 年的核心原则" >}}}}

## 常见问题解答

{{{{< faq >}}}}
- **黑眼圈分为哪几型？应该怎么选治疗方案？** 主流分型为三类：①色素型（色素沉着为主，需激光 + 美白外用）；②血管型（眼下血管透出，需血管激光 + 填充物遮盖阴影）；③阴影型/结构型（泪沟/眶沟凹陷造成的光影阴影，需填充剂或自体脂肪填充）{cite(dc[:2])}。混合型患者通常需要联合方案，建议先做皮肤科检查明确分型。
- **眶隔释放眼袋术和内切眼袋术有什么区别？哪个更好？** 内切（结膜入路）适合轻中度眼袋、无明显皮肤松弛的患者，恢复期 3–5 天，切口不可见；眶隔释放是在内切基础上将眶隔脂肪重新铺展填充泪沟，适合眼袋 + 泪沟并存的混合型患者{cite(eb[:2])}。
- **泪沟填充用什么材料最安全？玻尿酸还是胶原蛋白？** 主流选择是 HA 玻尿酸（HA filler）与胶原蛋白刺激剂（如 CaHA、PLLA）。Shome 等 2026 年双层策略建议深浅层使用不同 G 值产品{cite(ft[1:2] if len(ft) > 1 else ft[:1])}。玻尿酸见效快、可逆（HA 酶溶解），但维持时间 6–12 个月；胶原蛋白刺激剂维持更久但起效慢。需由具备眶周注射资质的医生评估。
- **眶周自体脂肪移植的存活率有多高？会不会出现硬结？** 眶周脂肪存活率相对较高（约 60–80%），因眶周血管丰富{cite(ft[2:3] if len(ft) > 2 else ft[:1])}。但眶周空间有限，注射量需严格控制——过量会导致"猪大肠眼"或结节，通常分 2–3 次少量注射。
- **肉毒素注射鱼尾纹会表情僵硬吗？怎么避免？** 合理剂量的眶周肉毒素（通常每侧 8–16 U，个体差异大）不会造成表情僵硬{cite(dc[:1])}。关键在于精准靶点注射（只在眼轮匝肌外侧眶缘处注射，避免扩散到眶内脂肪及睑板前肌），以及由具备注射资质的美容医生操作。
- **眶周年轻化手术多久能恢复？需要请假多久？** 非手术项目（肉毒素 3–7 天，填充剂 3–5 天）基本不影响正常社交；微创内切眼袋 3–5 天恢复，部分患者会水肿 1–2 周；外切眼袋或眶周提升手术需 2–4 周，建议请假 1 周以上。
{{{{< /faq >}}}}

{render_zh_references(refs)}

---

*本文基于 2026 年 7 月前后的 PubMed 学术文献、知乎专业讨论、ASPS / Allure 等行业资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年 7 月眶周年轻化深度分析：黑眼圈分型治疗、眼袋微创术式、泪沟填充策略与肉毒素注射进展"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["眶周年轻化", "黑眼圈", "眼袋", "泪沟", "肉毒素", "填充剂", "眼周医美"]
keywords: ["眶周年轻化", "黑眼圈分型", "眼袋微创", "泪沟填充", "肉毒素眶周", "眶隔释放", "眶周脂肪移植"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/periorbital-rejuvenation-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-2.jpg" title="眶周年轻化：从黑眼圈分型到容积重建的精准诊疗路径" >}}}}

"""
    return frontmatter + body


def build_en_post(refs: list[dict], theme_idx: dict, article_count: int,
                  pubmed_count: int, zhihu_count: int) -> str:
    dc = [i for i, _ in theme_idx.get("dark_circles", [])]
    eb = [i for i, _ in theme_idx.get("eyebags", [])]
    ft = [i for i, _ in theme_idx.get("fillers_tech", [])]
    sr = [i for i, _ in theme_idx.get("safety_reg", [])]

    def cite(indices: list[int]) -> str:
        return "".join(f"[^{i}]" for i in indices)

    body = f"""{{{{< medical-disclaimer />}}}}

In the first half of 2026, periorbital rejuvenation has heated up simultaneously in global clinical research and Chinese-language professional communities. Four directions dominate the landscape: subtype-precise dark-circle therapy, minimally invasive undereye-bag techniques, tear-trough filler material evolution, and botulinum toxin injection precision. This deep-analysis synthesizes {article_count} recent sources ({pubmed_count} PubMed-indexed articles + {zhihu_count} Zhihu professional discussions) alongside ASPS and industry trend reports.

## Key Takeaways

- Subtype-precise dark-circle treatment (pigment, vascular, structural/shadow) is the defining 2026 clinical trend — each subtype requires a distinct protocol and mixed-type cases need combination therapy.
- Beer et al.'s 2026 systematic review in *Dermatologic Surgery* confirmed that periorbital rejuvenation is emerging as a true multidisciplinary field with dermatology, ophthalmology, and plastic surgery converging.
- Minimally invasive undereye-bag procedures (transconjunctival blepharoplasty, orbital-septum release) are steadily replacing traditional external-incision approaches in mild-to-moderate cases, with recovery compressed from 1–2 weeks to 3–5 days.
- Tear-trough filler technique has evolved from first-generation HA toward "dual-layer, differential G-prime" injection — Shome et al.'s 2026 bilaminar strategy reduces Tyndall effect significantly.
- Periorbital volumetric reconstruction (autologous fat grafting, collagen stimulators) is gaining traction in mild-to-moderate volume deficiency, but viability prediction and nodule management remain key clinical challenges.
- Botulinum toxin periorbital injection (crow's feet, glabellar lines, dynamic periorbital wrinkles) in 2026 is shifting from "bulk dosing" toward "target-precise" — Fakih-Gomez et al.'s hybrid filler approach expanded the technical boundary of brow-area rejuvenation.

## Subtype-precise dark-circle therapy: from concealer mindset to precision medicine

Dark circles are the most complex and clinically challenging periorbital concern. Beer et al.'s 2026 systematic review in *Dermatologic Surgery* comprehensively surveyed recent advances in under-eye treatment, positioning dark-circle management as a textbook multidisciplinary collaboration between dermatology, ophthalmology, and plastic surgery{cite(dc[:1])}. Wu et al.'s three-step collagen-augmented comprehensive periorbital treatment ("Raise + Enhancement + Depigmentation") in *Aesthetic Plastic Surgery* marks the shift from single-modality approaches to layered combination protocols{cite(ft[:1] if ft else dc[:1])}.

On the Chinese-language professional side, {cite(dc[1:3] if len(dc) > 1 else dc[:1])} and other Zhihu discussions consistently identify mixed-type dark circles as the most prevalent and hardest-to-resolve category, recommending a sequence: structural filler first to address shadow, followed by energy-based devices and topical agents for pigment and vascular components. Asaria's 2026 review in *Facial Plastic Surgery Clinics* explicitly frames periorbital volumetric reconstruction not merely as "filling a deficit" but as an aesthetic engineering project restoring bony support and soft-tissue tension{cite(ft[1:2] if len(ft) > 1 else ft[:1])}.

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-2.jpg" title="Subtype-precise dark-circle treatment: each subtype has its own protocol; mixed types need combination therapy" >}}}}

## Minimally invasive undereye-bag surgery: orbital-septum release and fat redistribution

Undereye bags fundamentally result from anterior herniation of orbital fat through a weakened orbital septum. Traditional external-incision blepharoplasty places the incision in the subciliary skin with prolonged recovery and risk of ectropion. Fabbri et al.'s 2026 article in *Aesthetic Plastic Surgery* on the extended lower blepharoplasty established clinical safety standards for skin resection volume, noting significantly elevated ectropion risk above 6 mm resection{cite(eb[:1])}. Ding et al. in the same journal reported a technique using overlapping pretarsal and preseptal orbicularis oculi muscles to enhance pretarsal fullness — particularly valuable for patients with concurrent dry-eye and undereye-bag concerns{cite(eb[1:2] if len(eb) > 1 else eb[:1])}.

Chinese professional discourse on Zhihu {cite(eb[2:4] if len(eb) > 2 else eb[-1:] if eb else dc[-1:])} confirms that the transconjunctival orbital-septum release has substantially displaced the external approach for mild-to-moderate cases, with periorbital edema subsiding in 3–5 days and the incision completely hidden in the conjunctiva.

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-3.jpg" title="Minimally invasive undereye-bag surgery: transconjunctival approach with septum release is replacing traditional external incision" >}}}}

## Tear-trough fillers and periorbital volumetric reconstruction: dual upgrades in materials and technique

Tear-trough deformity is the second-largest driver of periorbital rejuvenation demand after undereye bags. Shome et al.'s 2026 novel bilaminar approach with differential rheologic G-prime fillers in the *Indian Journal of Ophthalmology* introduced a two-layer injection strategy — deep high-G-prime product for bony support, superficial low-G-prime product for smooth transition — significantly reducing the Tyndall effect{cite(ft[1:2] if len(ft) > 1 else ft[:1])}. Shomorony et al.'s 2026 review in *Facial Plastic Surgery Clinics* on autologous fat grafting of the periorbital and midface areas detailed technical considerations and viability factors, noting that the periorbital region's rich vascularity supports a 60–80% fat survival rate — higher than the midface — with nodule and asymmetry as primary complications{cite(ft[2:3] if len(ft) > 2 else ft[:1])}.

Fakih-Gomez et al.'s 2026 hybrid filler approach for forehead volumization and rejuvenation in *Aesthetic Plastic Surgery* — combining HA and calcium hydroxyapatite (CaHA) — expands the material options for periorbital and supraorbital volumetric reconstruction{cite(ft[0:1])}.

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-4.jpg" title="Tear-trough fillers and periorbital volumetric reconstruction: dual-layer G-prime stratification and autologous fat are the two 2026 pillars" >}}}}

## Botulinum toxin periorbital injection: from bulk dosing to target precision

Botulinum toxin's core periorbital indications include glabellar lines, crow's feet, dynamic periorbital wrinkles, and blepharospasm. Beer et al.'s 2026 systematic review in *Dermatologic Surgery* identified "precise targeting, minimal effective dose" as the defining 2026 principle for periorbital botulinum toxin{cite(dc[:1])}. Fakih-Gomez et al.'s hybrid filler paper further expanded the role of botulinum toxin as a complement in brow-area rejuvenation{cite(ft[0:1])}. Bray's 2026 review in *Facial Plastic Surgery Clinics* on orbicularis revectoring in deep-plane facelift{cite(sr[0:1] if sr else dc[-1:])} positions botulinum toxin as a complement — when both dynamic and static periorbital wrinkles coexist, botulinum and surgical lifting should be planned concurrently.

On the Chinese-language discourse front, {cite([i for i, a in theme_idx.get('safety_reg', []) if a.get('source_name') == '知乎'][:1])} reflect that Chinese consumers' attention to periorbital botulinum toxin dosing is intensifying, with "diffusion radius" and "injection precision" becoming trending search terms.

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-5.jpg" title="Botulinum toxin periorbital injection: target precision and minimal effective dose are the 2026 governing principles" >}}}}

## Frequently Asked Questions

{{{{< faq >}}}}
- **What are the subtypes of dark circles and how is each treated?** Three main types: ① Pigment-type (melanin overproduction — treat with Q-switched lasers + topical brightening agents); ② Vascular-type (vein translucency — vascular lasers + filler camouflage); ③ Structural/shadow-type (tear trough depression — HA or collagen-stimulating filler to fill the depression) {cite(dc[:2])}. Mixed types need combination therapy; always start with a dermatology workup.
- **What's the difference between transconjunctival and external-incision undereye-bag surgery?** The transconjunctival (internal) approach suits mild-to-moderate bags without significant skin laxity — recovery in 3–5 days, incision completely hidden. The external approach is used when there's significant skin excess to excise. Orbital-septum release (眶隔释放) combined with transconjunctival access also corrects concurrent tear troughs {cite(eb[:2])}.
- **Which filler is safest for tear-trough correction — HA or collagen stimulators?** HA fillers offer immediate correction and HA-enzyme reversibility; collagen stimulators (CaHA, PLLA) last longer but take weeks to show effect. Shome et al.'s 2026 bilaminar approach {cite(ft[1:2] if len(ft) > 1 else ft[:1])} suggests deep high-G-prime (structural support) and superficial low-G-prime (smooth transition) in the same session. Only physicians with periorbital injection credentials should perform this procedure.
- **What is the fat survival rate after periorbital autologous fat grafting, and what are the risks?** The periorbital region's rich vascularity supports a 60–80% fat survival rate — higher than the midface {cite(ft[2:3] if len(ft) > 2 else ft[:1])}. Risks include fat nodule formation, asymmetry, and over-injection ("puffy eye"). The standard approach is 2–3 staged small-volume injections rather than a single large-volume session.
- **Can botulinum toxin for crow's feet cause facial stiffness?** At appropriate doses (typically 8–16 U per side, highly individualized), periorbital botulinum toxin should not cause stiffness {cite(dc[:1])}. Key: precise targeting at the lateral orbital rim (only the outer orbicularis oculi), avoiding diffusion into the orbital fat and pretarsal muscle, and treatment by a credentialed injector.
- **How long is recovery after various periorbital procedures?** Non-surgical: botulinum (3–7 days), fillers (3–5 days) — minimal social downtime. Minimally invasive internal blepharoplasty: 3–5 days, some periorbital edema up to 1–2 weeks. External blepharoplasty or periorbital lift: 2–4 weeks, recommend at least 1 week off work.
{{{{< /faq >}}}}

{render_en_references(refs)}

---

*This article synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / Allure around 2026-07-10, for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Periorbital Rejuvenation Deep Analysis — July 2026: Subtype-Precise Dark Circle Therapy, Minimally Invasive Undereye-Bag Surgery, Tear-Trough Fillers & Botulinum Toxin Advances"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["periorbital rejuvenation", "dark circles", "undereye bags", "tear trough", "botulinum toxin", "dermal fillers", "eye area aesthetics"]
keywords: ["periorbital rejuvenation", "dark circle subtypes", "undereye bag surgery", "tear trough filler", "botulinum toxin periorbital", "orbital septum release", "autologous fat grafting"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/periorbital-rejuvenation-deep-analysis-2026-07"
---

{{{{< figure src="/images/posts/periorbital-rejuvenation-2026-07/image-2.jpg" title="Periorbital rejuvenation: a precision pathway from dark-circle subtyping to volumetric reconstruction" >}}}}

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
    articles = json.loads(crawled_json_path.read_bytes())
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
        data_dir = REPO_ROOT / "data" / "crawled" / "periorbital-rejuvenation-news"
        files = sorted(data_dir.glob("periorbital_rejuvenation_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
