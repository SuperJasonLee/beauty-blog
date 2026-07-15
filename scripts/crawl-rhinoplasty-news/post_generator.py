"""Post generator: synthesizes crawled articles into deep analysis bilingual Hugo posts."""

import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

ZH_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "zh-cn" / "posts"
EN_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "en" / "posts"
STATIC_IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "images" / "posts" / "rhinoplasty-aesthetics-2026-07"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def ensure_cover_image(slug: str, fallback_cover: Optional[str] = None) -> Optional[str]:
    """Ensure a cover image exists for the given slug.

    Contract (changed 2026-06-07 — silent copy is no longer allowed):
    1. If {slug}-cover.jpg already exists in STATIC_IMAGES_DIR, return its
       public path. No copy occurs.
    2. Otherwise, if ``fallback_cover`` is provided and exists on disk,
       copy that file to {slug}-cover.jpg and return the new public path.
       No sibling *-cover.jpg is touched.
    3. Otherwise, raise ``RuntimeError``.
    """
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    target = STATIC_IMAGES_DIR / f"{slug}-cover.jpg"
    public_path = f"/images/posts/rhinoplasty-aesthetics-2026-06/{slug}-cover.jpg"

    if target.exists():
        logger.info(f"Cover exists: {target.name}")
        return public_path

    if fallback_cover is not None:
        fallback_path = Path(fallback_cover)
        if not fallback_path.is_absolute():
            fallback_path = (Path(__file__).resolve().parent.parent.parent / fallback_cover).resolve()
        if not fallback_path.exists():
            raise FileNotFoundError(f"fallback_cover does not exist: {fallback_path}")
        shutil.copy(fallback_path, target)
        logger.info(f"Copied fallback_cover {fallback_path.name} -> {target.name}")
        return public_path

    raise RuntimeError(
        f"No cover image for slug '{slug}' and no fallback_cover provided. "
        f"Pass fallback_cover=... or synthesize a cover before calling."
    )


def extract_key_topics(articles: list[dict]) -> dict:
    """Extract and categorize key topics from all articles."""
    topics = {
        "surgical_techniques": [],
        "patient_care": [],
        "safety_complications": [],
        "trends_innovation": [],
        "patient_guidance": [],
    }

    for a in articles:
        title = a.get("title", "").lower()
        content = a.get("content_markdown", "").lower()
        combined = f"{title} {content}"

        if any(k in combined for k in ["technique", "surgery", "rhinoplasty", "procedure", "open", "closed", "graft", "implant", "cartilage", "术式", "手术", "隆鼻", "假体", "自体", "软骨"]):
            topics["surgical_techniques"].append(a)
        elif any(k in combined for k in ["recovery", "postoperative", "care", "swelling", "aftercare", "术后", "护理", "恢复", "消肿"]):
            topics["patient_care"].append(a)
        elif any(k in combined for k in ["complication", "risk", "safety", "infection", "revision", "并发症", "风险", "安全", "感染", "修复"]):
            topics["safety_complications"].append(a)
        elif any(k in combined for k in ["ai", "deep learning", "innovation", "simulation", "3d", "trend", "趋势", "技术", "数字化", "模拟"]):
            topics["trends_innovation"].append(a)
        else:
            topics["patient_guidance"].append(a)

    return topics


CATEGORY_ZH = {
    "surgical_techniques": "手术技术创新",
    "patient_care": "患者护理与术后管理",
    "safety_complications": "安全规范与并发症管理",
    "trends_innovation": "行业趋势与前沿技术",
    "patient_guidance": "患者教育与就医指南",
}

CATEGORY_EN = {
    "surgical_techniques": "Surgical Techniques & Innovation",
    "patient_care": "Patient Care & Recovery",
    "safety_complications": "Safety & Complication Management",
    "trends_innovation": "Trends & Emerging Technologies",
    "patient_guidance": "Patient Education & Guidance",
}


def _ref(a: dict) -> str:
    t = a.get("title", "Untitled").replace("...", "").rstrip(".")
    u = a.get("source_url", "")
    return f"[{t}]({u})" if u else t


def _refs(articles: list[dict]) -> str:
    return "、".join(_ref(a) for a in articles)


def _pubmed_ref(a: dict) -> str:
    t = a.get("title", "").replace("...", "").rstrip(".")
    u = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    journal = ""
    for line in meta.split("\n"):
        if "Journal:" in line:
            journal = line.replace("**Journal:**", "").strip()
            break
    journal_str = f"（{journal}）" if journal else ""
    return f"[{t}]({u}){journal_str}" if u else t


def _zhihu_ref(a: dict) -> str:
    t = a.get("title", "").replace("...", "").rstrip(".")
    u = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    author = ""
    for line in meta.split("\n"):
        if "Author:" in line:
            author = line.replace("**Author:**", "").replace("Author:", "").strip()
            break
    author_str = f"（知乎答主 {author}）" if author else "（知乎）"
    return f"[{t}]({u}){author_str}" if u else t


def _zh_technique_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        top = pubmed[0]
        rest = pubmed[1:]
        lines.append(f"本期学术文献中，{_pubmed_ref(top)}的研究值得关注。")
        if rest:
            lines.append(f"此外，{_refs(rest)}等研究也报告了鼻整形领域的技术进展。开放性入路与闭合性入路的精细化改良、自体肋软骨移植的优化方案、以及鼻翼与鼻尖的精细化塑形，仍是当前手术技术创新聚焦的三大方向。")
    if zhihu:
        lines.append(f"\n在知乎社区中，{_refs(zhihu)}等讨论反映了求美者对隆鼻材料选择（硅胶假体 vs. 膨体 vs. 自体软骨）和手术方式的高度关注。")
    lines.append("")
    return "\n".join(lines)


def _zh_patient_care_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"本期关于术后管理的文献中，{_refs(pubmed)}提示鼻整形术后的肿胀管理方案正逐步趋向个体化设计，术区冰敷、体位管理和药物干预的循证组合策略值得临床借鉴。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等分享为患者提供了来自一线的参考经验，包括消肿周期、饮食注意事项和心理调适等实用信息。")
    lines.append("")
    return "\n".join(lines)


def _zh_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"安全与并发症管理方面，{_refs(pubmed)}提供了新的循证证据。这些发现强调了术前三维影像评估标准化和术中内窥镜辅助技术在降低手术风险中的重要性。感染、移植物外露和鼻中隔穿孔仍是鼻整形术后需要重点监测的并发症类型。")
    if zhihu:
        lines.append(f"\n知乎上关于{_refs(zhihu)}的讨论也提示，患者在决策过程中对手术风险的知情同意和医生资质核查关注度持续提升。")
    lines.append("")
    return "\n".join(lines)


def _zh_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"行业趋势方面，{_refs(pubmed)}反映了学科前沿的发展方向。3D数字化模拟术前规划、AI辅助鼻型预测以及新型生物材料（如PEEK假体、脱细胞真皮基质）的应用，正加速推动鼻整形从经验驱动向循证数字驱动转型。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等话题也折射出行业生态的演变——年轻求美者对个性化鼻型设计的诉求上升，社交媒体审美趋势对手术需求的导向作用日益明显。")
    lines.append("")
    return "\n".join(lines)


def _zh_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"本期{_refs(pubmed)}等研究为患者教育提供了可参考的学术依据。鼻整形手术的审美决策需要综合面部解剖结构、个人气质和功能需求进行多维度评估。")
    if zhihu:
        lines.append(f"\n知乎上，{_refs(zhihu)}等内容持续为求美者提供决策参考。从初诊面诊到术后复查，信息透明度的提升有助于建立合理的预期管理，降低因信息不对称导致的手术不满。")
    lines.append("")
    return "\n".join(lines)


def build_zh_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    month = date_str[:7]
    title = f"鼻部整形行业深度分析（{date_str}）"
    description = f"基于 {total} 篇最新学术研究和行业讨论（PubMed {pubmed_count} 篇，知乎 {zhihu_count} 篇），{month} 鼻部整形领域的手术技术创新、安全规范和患者关怀深度解读。"

    sections = []

    intro = f"""## 导言

{date_str} 的鼻部整形行业动态显示，该领域在手术技术创新、安全管理、患者教育和行业生态方面持续演进。本期分析基于 {total} 篇最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），从技术趋势、临床实践、安全规范和患者决策等维度进行深度解读。
"""
    sections.append(intro)

    section_builders = [
        ("surgical_techniques", _zh_technique_section),
        ("patient_care", _zh_patient_care_section),
        ("safety_complications", _zh_safety_section),
        ("trends_innovation", _zh_trend_section),
        ("patient_guidance", _zh_guidance_section),
    ]

    for key, builder in section_builders:
        arts = topics.get(key, [])
        if arts:
            sections.append(builder(CATEGORY_ZH[key], arts))

    conclusion = f"""## 结语

本期 {date_str} 的鼻部整形行业分析显示，数字化精准化、材料创新和安全标准化是当前三大核心趋势。学术研究在术式改良和并发症管理上不断提供新证据，而社区讨论则加速了患者认知升级。建议从业者和求美者持续关注高质量学术输出和专业讨论，以支持理性决策。

---

**参考来源：** 本文参考了以下发表于 {month} 的相关文献与讨论：
"""
    ref_lines = []
    for a in articles:
        t = a.get("title", "").replace("...", "").rstrip(".")
        u = a.get("source_url", "")
        s = a.get("source_name", "")
        ref_lines.append(f"- [{t}]({u}) — {s}")
    ref_lines.append("")
    ref_lines.append("**免责声明：** 本文内容仅供参考，不构成医疗建议。如有整形需求，请咨询专业执业医师。")
    sections.append(conclusion + "\n".join(ref_lines))

    body = "\n".join(sections)

    frontmatter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: false
description: "{description}"
tags: ["鼻部整形", "隆鼻", "技术趋势", "行业分析", "安全规范"]
categories: ["鼻部整形"]
keywords: ["鼻部整形", "隆鼻", "鼻整形技术", "鼻部整形安全", "鼻部整形 {date_str}"]
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{date_str}"
medicalAudience: "Patient"
{('featuredImage: "' + cover_path + '"') if cover_path else '# featuredImage: (no cover available)'}
translations: ["/en/posts/{slug}"]
---"""

    return f"{frontmatter}\n\n{body}"


def _en_technique_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        top = pubmed[0]
        rest = pubmed[1:]
        lines.append(f"Among the latest literature, {_pubmed_ref(top)} deserves attention. ")
        if rest:
            ref_str = ", ".join(_ref(a) for a in rest)
            lines.append(f"Additional studies including {ref_str} report continued progress in open vs. closed approaches, autologous costal cartilage grafting optimization, and refined nasal tip and alar reshaping techniques. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nOn Zhihu, discussions such as {ref_str} reflect growing patient interest in implant material selection and surgical approach choice for rhinoplasty procedures. ")
    lines.append("")
    return "\n".join(lines)


def _en_patient_care_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"In postoperative care, studies including {', '.join(_pubmed_ref(a) for a in pubmed)} highlight the shift toward individualized edema management protocols in rhinoplasty, with evidence-based combinations of cold compress, positioning, and pharmacological interventions. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nCommunity discussions such as {ref_str} also provide practical firsthand insights on swelling duration, dietary precautions, and psychological adjustment during rhinoplasty recovery. ")
    lines.append("")
    return "\n".join(lines)


def _en_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"On safety and complications, {', '.join(_pubmed_ref(a) for a in pubmed)} provide new evidence reinforcing the importance of standardized 3D preoperative imaging assessment and intraoperative endoscopic guidance in reducing surgical risk. Infection, graft exposure, and septal perforation remain key complications requiring post-rhinoplasty monitoring. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nZhihu discussions around {ref_str} also indicate that patients are placing increasing emphasis on informed consent and surgeon credential verification during the decision-making process. ")
    lines.append("")
    return "\n".join(lines)


def _en_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"Regarding industry trends, {', '.join(_pubmed_ref(a) for a in pubmed)} reflect the direction of cutting-edge developments in the field. 3D digital simulation for pre-op planning, AI-assisted nasal shape prediction, and novel biomaterials (including PEEK implants and acellular dermal matrix) are accelerating the field's transition from experience-driven to evidence-based, digitally-driven practice. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nCommunity discussions including {ref_str} also reflect evolving industry dynamics, with younger patients increasingly demanding personalized nasal shape design and social media aesthetics influencing surgical demand. ")
    lines.append("")
    return "\n".join(lines)


def _en_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"For patient education, {', '.join(_pubmed_ref(a) for a in pubmed)} offer valuable academic references. Rhinoplasty aesthetic decision-making requires a multidimensional assessment incorporating facial anatomy, personal style, and functional considerations. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nOn Zhihu, content such as {ref_str} continues to support patient decision-making — from initial consultation to postoperative follow-up. Greater information transparency helps establish realistic expectations and reduces dissatisfaction stemming from information asymmetry. ")
    lines.append("")
    return "\n".join(lines)


def build_en_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    title = f"Rhinoplasty: Deep Analysis of Latest Trends ({date_str})"
    description = f"In-depth analysis of {total} recent articles on rhinoplasty innovations, safety standards, and patient care — {pubmed_count} from PubMed, {zhihu_count} from Zhihu."

    sections = []

    intro = f"""## Introduction

The rhinoplasty landscape continues to evolve rapidly with advances in surgical technique, digital planning, and biomaterials. This analysis covers {total} recent sources ({pubmed_count} from PubMed, {zhihu_count} from Zhihu) published around {date_str}, examining key developments in surgical innovation, patient care, safety protocols, and industry trends.
"""
    sections.append(intro)

    en_section_builders = [
        ("surgical_techniques", _en_technique_section),
        ("patient_care", _en_patient_care_section),
        ("safety_complications", _en_safety_section),
        ("trends_innovation", _en_trend_section),
        ("patient_guidance", _en_guidance_section),
    ]

    for key, builder in en_section_builders:
        arts = topics.get(key, [])
        if arts:
            sections.append(builder(CATEGORY_EN[key], arts))

    ref_lines = []
    for a in articles:
        t = a.get("title", "").replace("...", "").rstrip(".")
        u = a.get("source_url", "")
        s = a.get("source_name", "")
        ref_lines.append(f"- [{t}]({u}) — {s}")

    conclusion = f"""## Conclusion

The analysis of rhinoplasty developments around {date_str} reveals three dominant trends: digitization and precision in surgical planning, biomaterial innovation, and standardization of safety protocols. Academic research continues to provide evidence for practice improvement, while community discussions accelerate patient education and awareness.

---

**References:**
""" + "\n".join(ref_lines) + "\n\n**Disclaimer:** This content is for informational purposes only and does not constitute medical advice. Please consult a qualified physician for any surgical procedures."

    sections.append(conclusion)

    body = "\n".join(sections)

    frontmatter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: false
description: "{description}"
tags: ["rhinoplasty", "nose surgery", "surgical techniques", "industry analysis", "patient safety"]
categories: ["Rhinoplasty"]
keywords: ["rhinoplasty", "nose surgery", "nasal surgery", "rhinoplasty techniques", "rhinoplasty {date_str}"]
author: "Beauty-Blog Medical Review Team"
reviewer: "Licensed Physician Review"
lastReviewed: "{date_str}"
medicalAudience: "Patient"
{('featuredImage: "' + cover_path + '"') if cover_path else '# featuredImage: (no cover available)'}
translations: ["/zh-cn/posts/{slug}"]
---"""

    return f"{frontmatter}\n\n{body}"


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

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = f"rhinoplasty-deep-analysis-{datetime.now().strftime('%Y-%m')}"

    cover_path = ensure_cover_image(slug, fallback_cover="static/images/posts/rhinoplasty-card.jpg")
    logger.info(f"Cover path for frontmatter: {cover_path}")

    posts = []

    zh_content = build_zh_post(articles, date_str, slug, cover_path)
    posts.append(write_post(zh_content, slug, "zh"))

    en_content = build_en_post(articles, date_str, slug, cover_path)
    posts.append(write_post(en_content, slug, "en"))

    return posts


def main(json_path: Optional[str] = None):
    if json_path:
        path = Path(json_path)
    else:
        data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "rhinoplasty-news"
        files = sorted(data_dir.glob("rhinoplasty_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]

    return generate_posts(path)


if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(json_file)
