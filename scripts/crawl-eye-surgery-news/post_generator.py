"""Post generator: synthesizes crawled articles into deep analysis bilingual Hugo posts."""

import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

ZH_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "zh-cn" / "posts" / "eye-surgery-news"
EN_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "en" / "posts" / "eye-surgery-news"
STATIC_IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "images" / "eye-surgery-news"

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
    3. Otherwise, raise ``RuntimeError``. Silently copying a sibling
       *-cover.jpg is forbidden — that was the root cause of the
       2026-06-06 cover being byte-identical to the 2026-06-01 cover.

    To skip cover synthesis entirely (e.g. for a post that genuinely does
    not want a featured image), wrap the call in try/except and pass the
    resulting exception up to the caller, which can then omit featuredImage
    from the frontmatter.
    """
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    target = STATIC_IMAGES_DIR / f"{slug}-cover.jpg"
    public_path = f"/images/eye-surgery-news/{slug}-cover.jpg"

    if target.exists():
        logger.info(f"Cover exists: {target.name}")
        return public_path

    if fallback_cover is not None:
        fallback_path = Path(fallback_cover)
        if not fallback_path.is_absolute():
            fallback_path = (Path(__file__).resolve().parent.parent.parent / fallback_cover).resolve()
        if not fallback_path.exists():
            raise FileNotFoundError(
                f"fallback_cover does not exist: {fallback_path}"
            )
        shutil.copy(fallback_path, target)
        logger.info(f"Copied fallback_cover {fallback_path.name} → {target.name}")
        return public_path

    raise RuntimeError(
        f"No cover image for slug '{slug}' and no fallback_cover provided. "
        f"Refusing to silently copy a sibling cover (this caused the 2026-06-06 "
        f"duplicate-cover bug). Pass fallback_cover=... or synthesize a cover "
        f"before calling this function."
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
        
        if any(k in combined for k in ["technique", "surgery", "blepharoplasty", "procedure", "术式", "手术", "整形", "修复"]):
            topics["surgical_techniques"].append(a)
        elif any(k in combined for k in ["recovery", "postoperative", "care", "术后", "护理", "恢复"]):
            topics["patient_care"].append(a)
        elif any(k in combined for k in ["complication", "risk", "safety", "并发症", "风险", "安全"]):
            topics["safety_complications"].append(a)
        elif any(k in combined for k in ["ai", "deep learning", "innovation", "trend", "创新", "趋势", "技术"]):
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
    """Format a single article as an inline reference: [title](url)"""
    t = a.get("title", "Untitled").replace("...", "").rstrip(".")
    u = a.get("source_url", "")
    return f"[{t}]({u})" if u else t


def _refs(articles: list[dict]) -> str:
    """Format a list of articles as comma-separated references."""
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


def _build_zh_analysis_section(heading: str, articles: list[dict], template_fn) -> str:
    """Build a section if there are articles, otherwise return empty."""
    if not articles:
        return ""
    return template_fn(heading, articles)


def _zh_technique_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        top = pubmed[0]
        rest = pubmed[1:]
        lines.append(f"本期学术文献中，{_pubmed_ref(top)}的研究值得关注。")
        if rest:
            lines.append(f"此外，{_refs(rest)}等研究也报告了相关技术进展。手术入路的微创化、精准化仍是当前的主流方向，经结膜入路和眉下切口的改良方案持续出现。")
    if zhihu:
        lines.append(f"\n在知乎社区中，{_refs(zhihu)}等讨论反映了求美者对术式选择和医生资质的高度关注。")
    lines.append("")
    return "\n".join(lines)


def _zh_patient_care_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"本期关于术后管理的文献中，{_refs(pubmed)}提示术后护理方案的个体化设计和循证优化值得重视。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等分享为患者提供了来自一线的参考经验。")
    lines.append("")
    return "\n".join(lines)


def _zh_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"安全与并发症管理方面，{_refs(pubmed)}提供了新的循证证据。这些发现强调了术前评估标准化和术后并发症早期识别的重要性。")
    if zhihu:
        lines.append(f"\n知乎上关于{_refs(zhihu)}的讨论也提示，患者在决策过程中对安全信息的关注度持续提升。")
    lines.append("")
    return "\n".join(lines)


def _zh_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"行业趋势方面，{_refs(pubmed)}反映了学科前沿的发展方向。AI辅助诊断、标准化评估工具和数字化技术正加速渗透到眼整形临床实践中。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等话题也折射出行业生态的演变。")
    lines.append("")
    return "\n".join(lines)


def _zh_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"本期{_refs(pubmed)}等研究为患者教育提供了可参考的学术依据。")
    if zhihu:
        lines.append(f"\n知乎上，{_refs(zhihu)}等内容持续为求美者提供决策参考。从医生选择到术后护理，信息对称度的提升有助于降低不合理的预期。")
    lines.append("")
    return "\n".join(lines)


def build_zh_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    month = date_str[:7]
    title = f"眼部整形行业深度分析（{date_str}）"
    description = f"基于 {total} 篇最新学术研究和行业讨论（PubMed {pubmed_count} 篇，知乎 {zhihu_count} 篇），{month} 眼部整形领域的技术创新、安全规范和患者关怀深度解读。"

    sections = []

    intro = f"""## 导言

{date_str} 的眼部整形行业动态显示，该领域在技术创新、安全管理、患者教育和行业生态方面持续演进。本期分析基于 {total} 篇最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），从技术趋势、临床实践、安全规范和患者决策等维度进行解读。
"""
    sections.append(intro)

    # Build sections in a fixed order, each only shows if articles exist in that category
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

本期 {date_str} 的眼整形行业分析显示，技术微创化、安全标准化、信息透明化是当前三大趋势。学术研究在术式改良和并发症管理上不断提供新证据，而社区讨论则加速了患者认知升级。建议从业者和求美者持续关注高质量学术输出和专业讨论，以支持理性决策。

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
draft: true
description: "{description}"
tags: ["眼部整形", "技术趋势", "行业分析", "安全规范"]
categories: ["眼部整形"]
keywords: ["眼部整形", "行业分析", "眼整形技术", "眼部整形安全", "眼部整形 {date_str}"]
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{date_str}"
medicalAudience: "Patient"
{('featuredImage: "' + cover_path + '"') if cover_path else '# featuredImage: (no cover available)'}
translations: ["/en/posts/eye-surgery-news/{slug}"]
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
            lines.append(f"Additional studies including {ref_str} report continued progress in minimally invasive and precision approaches to blepharoplasty and periorbital surgery. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nOn Zhihu, discussions such as {ref_str} reflect growing patient interest in surgical technique selection and provider qualification. ")
    lines.append("")
    return "\n".join(lines)


def _en_patient_care_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"In postoperative care, studies including {', '.join(_pubmed_ref(a) for a in pubmed)} highlight the importance of evidence-based recovery protocols and individualized patient management plans. ")
    lines.append("")
    return "\n".join(lines)


def _en_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"On safety and complications, {', '.join(_pubmed_ref(a) for a in pubmed)} provide new evidence reinforcing the need for standardized preoperative assessment and early complication recognition. ")
    lines.append("")
    return "\n".join(lines)


def _en_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"Regarding industry trends, {', '.join(_pubmed_ref(a) for a in pubmed)} point to accelerating adoption of AI-assisted diagnostics, standardized assessment tools, and digital technologies in oculoplastic practice. ")
    if zhihu:
        lines.append(f"\nCommunity discussions including {', '.join(_ref(a) for a in zhihu)} also reflect evolving industry dynamics. ")
    lines.append("")
    return "\n".join(lines)


def _en_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"For patient education, {', '.join(_pubmed_ref(a) for a in pubmed)} offer valuable reference material. ")
    if zhihu:
        lines.append(f"\nOn Zhihu, content such as {', '.join(_ref(a) for a in zhihu)} continues to help patients make informed decisions—from surgeon selection to postoperative care. ")
    lines.append("")
    return "\n".join(lines)


def build_en_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    title = f"Eye Plastic Surgery: Deep Analysis of Latest Trends ({date_str})"
    description = f"In-depth analysis of {total} recent articles on eye plastic surgery innovations, safety standards, and patient care — {pubmed_count} from PubMed, {zhihu_count} from Zhihu."

    sections = []

    intro = f"""## Introduction

The eye plastic surgery landscape continues to evolve rapidly. This analysis covers {total} recent sources ({pubmed_count} from PubMed, {zhihu_count} from Zhihu) published around {date_str}, examining key developments in surgical technique, patient care, safety, and industry trends.
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

The analysis of eye plastic surgery developments around {date_str} reveals three dominant trends: surgical technique refinement toward minimally invasive approaches, standardization of safety protocols, and growing information transparency for patients. Academic research continues to provide evidence for practice improvement, while community discussions accelerate patient education.

---

**References:**
""" + "\n".join(ref_lines) + "\n\n**Disclaimer:** This content is for informational purposes only and does not constitute medical advice. Please consult a qualified physician for any surgical procedures."

    sections.append(conclusion)

    body = "\n".join(sections)

    frontmatter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: true
description: "{description}"
tags: ["eye surgery", "surgical techniques", "industry analysis", "patient safety"]
categories: ["Eye Surgery"]
keywords: ["eye plastic surgery", "blepharoplasty", "eyelid surgery", "oculoplastic trends", "eye surgery {date_str}"]
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{date_str}"
medicalAudience: "Patient"
{('featuredImage: "' + cover_path + '"') if cover_path else '# featuredImage: (no cover available)'}
translations: ["/zh-cn/posts/eye-surgery-news/{slug}"]
---"""

    return f"{frontmatter}\n\n{body}"


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

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = f"eye-surgery-news-{datetime.now().strftime('%Y%m%d')}"

    # Ensure a cover image exists for this slug. See ensure_cover_image() for
    # the post-2026-06-07 contract: it raises RuntimeError if neither a
    # fresh cover nor an explicit fallback_cover is available. If you want
    # a graceful no-cover path here, wrap the call in try/except and omit
    # featuredImage from the frontmatter.
    cover_path = ensure_cover_image(slug)
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
        data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "eye-surgery-news"
        files = sorted(data_dir.glob("eye_surgery_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]

    return generate_posts(path)


if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(json_file)
