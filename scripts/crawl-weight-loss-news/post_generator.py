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
STATIC_IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "images" / "posts" / "weight-loss-aesthetics-2026-06"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def ensure_cover_image(slug: str, fallback_cover: Optional[str] = None) -> Optional[str]:
    """Ensure a cover image exists for the given slug."""
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    target = STATIC_IMAGES_DIR / f"{slug}-cover.jpg"
    public_path = f"/images/posts/weight-loss-aesthetics-2026-06/{slug}-cover.jpg"

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
        f"No cover image for slug '{slug}' and no fallback_cover provided."
    )


def extract_key_topics(articles: list[dict]) -> dict:
    topics = {
        "surgical_techniques": [],
        "pharma_nutrition": [],
        "safety_complications": [],
        "trends_innovation": [],
        "patient_guidance": [],
    }

    for a in articles:
        title = a.get("title", "").lower()
        content = a.get("content_markdown", "").lower()
        combined = f"{title} {content}"

        if any(k in combined for k in ["liposuction", "body contouring", "surgery", "procedure", "术式", "手术", "吸脂", "溶脂", "bodyjet"]):
            topics["surgical_techniques"].append(a)
        elif any(k in combined for k in ["semaglutide", "glp-1", "ozempic", "drug", "pharmacotherapy", "nutrition", "司美格鲁肽", "药物", "营养"]):
            topics["pharma_nutrition"].append(a)
        elif any(k in combined for k in ["complication", "risk", "safety", "seroma", "lipoedema", "并发症", "风险", "安全"]):
            topics["safety_complications"].append(a)
        elif any(k in combined for k in ["ai", "deep learning", "innovation", "trend", "coolsculpting", "创新", "趋势", "冷冻溶脂"]):
            topics["trends_innovation"].append(a)
        else:
            topics["patient_guidance"].append(a)

    return topics


CATEGORY_ZH = {
    "surgical_techniques": "手术技术创新",
    "pharma_nutrition": "药物减肥与营养干预",
    "safety_complications": "安全规范与并发症管理",
    "trends_innovation": "行业趋势与前沿技术",
    "patient_guidance": "患者教育与就医指南",
}

CATEGORY_EN = {
    "surgical_techniques": "Surgical Innovation & Body Contouring",
    "pharma_nutrition": "Pharmacological & Nutritional Interventions",
    "safety_complications": "Safety Standards & Complication Management",
    "trends_innovation": "Industry Trends & Emerging Technologies",
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


# ─── Chinese section builders ───────────────────────────────────────

def _zh_surgical_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        top = pubmed[0]
        rest = pubmed[1:]
        lines.append(f"本期学术文献中，{_pubmed_ref(top)}的研究值得关注。")
        if rest:
            lines.append(f"此外，{_refs(rest)}等研究也报告了相关手术技术进展。吸脂塑形领域正在向精细化、微创化和智能化方向发展，水动力吸脂（water-assisted liposuction）、激光辅助吸脂和 BodyJet 等技术持续优化术后恢复体验和塑形精度。")
    if zhihu:
        lines.append(f"\n在知乎社区中，{_refs(zhihu)}等讨论反映了求美者对手术安全和术后效果的关注。")
    lines.append("")
    return "\n".join(lines)


def _zh_pharma_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"药物减肥干预方面，{_refs(pubmed)}等研究提供了最新循证证据。GLP-1 受体激动剂（如司美格鲁肽 semaglutide）在 2025—2026 年持续成为肥胖和超重管理领域的核心讨论热点，其减重疗效和代谢改善获益已获得大规模 III 期临床数据支持。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等内容反映了求美者对非手术减重方案的关注。从用药体验到生活方式调整，信息透明度在持续提升。")
    lines.append("")
    return "\n".join(lines)


def _zh_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"安全与并发症管理方面，{_refs(pubmed)}提供了新的循证证据。吸脂术后并发症（包括血清肿、皮肤凹凸不平、色素沉着和感染）的风险控制仍是临床关注重点，规范化操作流程和围手术期管理方案的持续优化有助于降低不良事件发生率。")
    if zhihu:
        lines.append(f"\n知乎上关于{_refs(zhihu)}的讨论也提示，患者在决策过程中对安全信息的关注度持续提升，理性就医意识在增强。")
    lines.append("")
    return "\n".join(lines)


def _zh_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"行业趋势方面，{_refs(pubmed)}反映了学科前沿的发展方向。非侵入式减脂技术（如冷冻溶脂 coolsculpting、射频溶脂）在 2026 年持续迭代，而 AI 辅助术前设计和脂肪分布评估也正在成为吸脂手术的新标配。")
    if zhihu:
        lines.append(f"\n社区讨论中，{_refs(zhihu)}等话题也折射出行业生态的演变——从「以手术为中心」向「手术 + 药物 + 生活方式综合管理」转型的讨论越来越多。")
    lines.append("")
    return "\n".join(lines)


def _zh_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"本期{_refs(pubmed)}等研究为患者教育提供了可参考的学术依据。")
    if zhihu:
        lines.append(f"\n知乎上，{_refs(zhihu)}等内容持续为求美者提供决策参考。从术式选择到术后护理，信息对称度的提升有助于降低不合理的预期。")
    lines.append("")
    return "\n".join(lines)


# ─── English section builders ──────────────────────────────────────

def _en_surgical_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        top = pubmed[0]
        rest = pubmed[1:]
        lines.append(f"Among recent literature, {_pubmed_ref(top)} is particularly noteworthy. ")
        if rest:
            ref_str = ", ".join(_ref(a) for a in rest)
            lines.append(f"Additional studies including {ref_str} report continued progress in minimally invasive liposuction, water-assisted liposuction (WAL), laser-assisted lipolysis, and BodyJet technology—all contributing to improved precision and faster recovery. ")
    if zhihu:
        ref_str = ", ".join(_ref(a) for a in zhihu)
        lines.append(f"\nOn Zhihu, discussions such as {ref_str} reflect growing patient interest in surgical safety and postoperative outcomes. ")
    lines.append("")
    return "\n".join(lines)


def _en_pharma_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"In pharmacological weight management, studies including {', '.join(_pubmed_ref(a) for a in pubmed)} provide the latest evidence-based insights. GLP-1 receptor agonists such as semaglutide continue to dominate clinical and public discussion in 2025-2026, with phase III data demonstrating significant and sustained weight reduction alongside metabolic benefits. ")
    if zhihu:
        lines.append(f"\nCommunity discussions including {', '.join(_ref(a) for a in zhihu)} reflect growing patient awareness of non-surgical weight management options. ")
    lines.append("")
    return "\n".join(lines)


def _en_safety_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"On safety and complications, {', '.join(_pubmed_ref(a) for a in pubmed)} provide new evidence reinforcing the need for standardized protocols. Post-liposuction complications including seroma, contour irregularities, dyschromia, and infection remain key clinical concerns, and continued optimization of perioperative management protocols is critical. ")
    if zhihu:
        lines.append(f"\nCommunity discussions including {', '.join(_ref(a) for a in zhihu)} also highlight patient demand for transparent safety information and realistic outcome expectations. ")
    lines.append("")
    return "\n".join(lines)


def _en_trend_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"Regarding industry trends, {', '.join(_pubmed_ref(a) for a in pubmed)} point to accelerating adoption of non-invasive fat reduction technologies such as cryolipolysis (CoolSculpting) and radiofrequency lipolysis, alongside AI-assisted preoperative planning and body composition assessment. ")
    if zhihu:
        lines.append(f"\nCommunity discussions including {', '.join(_ref(a) for a in zhihu)} reflect a broader industry shift from surgery-only to an integrated model combining surgery, pharmacotherapy, and lifestyle management. ")
    lines.append("")
    return "\n".join(lines)


def _en_guidance_section(heading: str, articles: list[dict]) -> str:
    pubmed = [a for a in articles if a.get("source_name") == "PubMed"]
    zhihu = [a for a in articles if a.get("source_name") == "知乎"]
    lines = [f"## {heading}\n"]
    if pubmed:
        lines.append(f"For patient education, {', '.join(_pubmed_ref(a) for a in pubmed)} offer valuable academic reference points. ")
    if zhihu:
        lines.append(f"\nOn Zhihu, content such as {', '.join(_ref(a) for a in zhihu)} continues to help patients make informed decisions regarding surgical technique selection, postoperative care, and realistic outcome expectations. ")
    lines.append("")
    return "\n".join(lines)


# ─── Post builders ─────────────────────────────────────────────────

def build_zh_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    month = date_str[:7]
    title = f"减肥医美行业深度分析（{date_str}）"
    description = f"基于 {total} 篇最新学术研究和行业讨论（PubMed {pubmed_count} 篇，知乎 {zhihu_count} 篇），{month} 减肥医美领域的手术技术创新、药物干预与安全规范深度解读。"

    sections = []

    intro = f"""## 导言

{date_str} 的减肥医美（weight loss aesthetics / body contouring）行业动态显示，该领域正处于"手术 + 药物 + 非侵入式技术"三驾马车并行的结构性拐点。GLP-1 受体激动剂的爆发式增长、吸脂塑形技术的持续精细化、以及非侵入式减脂设备的迭代，正在重塑减肥医美的临床版图和患者认知。本期分析基于 {total} 篇最新素材（PubMed 学术文献 {pubmed_count} 篇 + 知乎专业讨论 {zhihu_count} 篇），从手术技术创新、药物干预进展、安全管理、行业趋势和患者决策等维度进行解读。
"""
    sections.append(intro)

    zh_builders = [
        ("surgical_techniques", _zh_surgical_section),
        ("pharma_nutrition", _zh_pharma_section),
        ("safety_complications", _zh_safety_section),
        ("trends_innovation", _zh_trend_section),
        ("patient_guidance", _zh_guidance_section),
    ]

    for key, builder in zh_builders:
        arts = topics.get(key, [])
        if arts:
            sections.append(builder(CATEGORY_ZH[key], arts))

    conclusion = f"""## 结语

本期 {date_str} 的减肥医美行业分析显示，三个结构性趋势正在同步演进：

**第一，手术塑形向精细化、微创化转型。** 水动力吸脂（WAL）、激光辅助吸脂和 BodyJet 等技术持续优化术中舒适度和术后恢复体验，术前三维数字化设计和 AI 辅助脂肪分布评估正在成为临床新标配。

**第二，药物减肥重塑行业生态。** 司美格鲁肽等 GLP-1 受体激动剂的临床数据改变了医美从业者和求美者对"手术 vs. 药物"的二元框架——越来越多患者寻求"生活方式管理 + 局部塑形"的组合方案，而非单一手术。

**第三，安全监管与信息透明化同步升级。** 监管部门对吸脂设备、减重药物和非侵入式设备的合规性审查持续趋严，患者教育需求随之增长。

建议从业者和求美者持续关注高质量学术输出和权威监管动态，以支持基于证据的理性决策。

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
    ref_lines.append("**免责声明：** 本文内容仅供参考，不构成医疗建议。如有减肥或医美需求，请咨询专业执业医师。")
    sections.append(conclusion + "\n".join(ref_lines))

    body = "\n".join(sections)

    frontmatter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: true
description: "{description}"
tags: ["减肥医美", "吸脂塑形", "GLP-1", "司美格鲁肽", "非侵入式减脂", "医美安全"]
categories: ["减肥医美"]
keywords: ["减肥医美", "吸脂", "溶脂", "GLP-1", "司美格鲁肽", "冷冻溶脂", "body contouring", "减肥医美 {date_str}"]
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{date_str}"
medicalAudience: "Patient"
{('featuredImage: "' + cover_path + '"') if cover_path else '# featuredImage: (no cover available)'}
translations: ["/en/posts/{slug}"]
---"""

    return f"{frontmatter}\n\n{body}"


def build_en_post(articles: list[dict], date_str: str, slug: str, cover_path: Optional[str] = None) -> str:
    topics = extract_key_topics(articles)
    total = len(articles)
    pubmed_count = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_count = sum(1 for a in articles if a.get("source_name") == "知乎")

    title = f"Weight Loss Aesthetics: Deep Analysis of Body Contouring & Fat Reduction Trends ({date_str})"
    description = f"In-depth analysis of {total} recent sources on weight loss aesthetics — liposuction, GLP-1 pharmacotherapy, non-invasive fat reduction, and safety standards. {pubmed_count} from PubMed, {zhihu_count} from Zhihu."

    sections = []

    intro = f"""## Introduction

The weight loss aesthetics and body contouring industry is undergoing a structural transformation driven by three concurrent forces: the explosive growth of GLP-1 receptor agonists (such as semaglutide), the continued refinement of liposuction techniques, and the iterative advancement of non-invasive fat reduction technologies. This analysis covers {total} recent sources ({pubmed_count} from PubMed, {zhihu_count} from Zhihu) published around {date_str}, examining key developments in surgical innovation, pharmacological interventions, safety management, and industry trends.
"""
    sections.append(intro)

    en_builders = [
        ("surgical_techniques", _en_surgical_section),
        ("pharma_nutrition", _en_pharma_section),
        ("safety_complications", _en_safety_section),
        ("trends_innovation", _en_trend_section),
        ("patient_guidance", _en_guidance_section),
    ]

    for key, builder in en_builders:
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

The analysis of weight loss aesthetics developments around {date_str} reveals three dominant trends:

**First, surgical body contouring is shifting toward precision and minimally invasive approaches.** Technologies including water-assisted liposuction (WAL), laser-assisted lipolysis, and BodyJet continue to enhance intraoperative comfort and postoperative recovery. AI-assisted preoperative planning and 3D body composition assessment are becoming clinical standards.

**Second, pharmacological weight management is reshaping the industry ecosystem.** Semaglutide and other GLP-1 receptor agonists have fundamentally altered how both practitioners and patients frame the "surgery vs. drug" decision, driving increased interest in combined lifestyle-plus-local-contouring treatment plans.

**Third, safety regulation and information transparency are advancing in parallel.** Regulatory bodies continue tightening oversight of liposuction devices, weight-loss drugs, and non-invasive technologies, while patient education demand grows in parallel.

Stakeholders are advised to monitor high-quality academic output and authoritative regulatory updates to support evidence-based decision-making.

---

**References:**
""" + "\n".join(ref_lines) + "\n\n**Disclaimer:** This content is for informational purposes only and does not constitute medical advice. Please consult a qualified physician for any medical procedures."

    sections.append(conclusion)

    body = "\n".join(sections)

    frontmatter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
draft: true
description: "{description}"
tags: ["weight loss aesthetics", "liposuction", "body contouring", "GLP-1", "semaglutide", "non-invasive fat reduction"]
categories: ["Weight Loss Aesthetics"]
keywords: ["weight loss aesthetics", "liposuction", "body contouring", "semaglutide", "GLP-1", "coolsculpting", "fat reduction", "weight loss aesthetics {date_str}"]
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
    slug = f"weight-loss-aesthetics-deep-analysis-{datetime.now().strftime('%Y-%m')}"

    # Use existing image-1.jpg as cover (existing post pattern for this directory)
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    existing_cover = STATIC_IMAGES_DIR / "image-1.jpg"
    if existing_cover.exists():
        cover_path = "/images/posts/weight-loss-aesthetics-2026-06/image-1.jpg"
        logger.info(f"Using existing cover: {cover_path}")
    else:
        raise RuntimeError(
            f"No existing cover image found in {STATIC_IMAGES_DIR}. "
            f"Expected image-1.jpg from existing post."
        )

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
        data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "crawled" / "weight-loss-news"
        files = sorted(data_dir.glob("weight_loss_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]

    return generate_posts(path)


if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(json_file)
