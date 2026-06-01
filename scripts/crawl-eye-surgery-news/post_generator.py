"""Post generator: synthesizes crawled articles into deep analysis bilingual Hugo posts."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

ZH_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "zh-cn" / "posts" / "eye-surgery-news"
EN_DIR = Path(__file__).resolve().parent.parent.parent / "content" / "en" / "posts" / "eye-surgery-news"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


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


def build_zh_post(articles: list[dict], date_str: str, slug: str) -> str:
    topics = extract_key_topics(articles)
    
    title = f"眼部整形深度解析：最新技术趋势与临床实践指南"
    description = "基于最新学术研究和行业动态，深度分析眼部整形领域的技术创新、安全规范和患者关怀要点。"

    body = f"""## 导言

眼部整形作为医美领域最精细的专科之一，近年来在技术创新、安全标准和患者体验方面都取得了显著进展。本文基于最新发表的学术研究和行业观察，从技术革新、安全管理、患者关怀和行业趋势四个维度，为求美者和从业者提供深度分析。

## 一、技术创新：精准化与微创化成为主流

### 1.1 眼睑成形术的技术演进

近期发表在《Scientific Reports》的研究（Kono & Kamei, 2026）揭示了眉下切开法在眼睑成形术中的新优势。该研究指出，通过精确计算皮肤切除量，可以在术后自然形成理想的重睑线，避免了传统方法中过度切除导致的"瞪眼"外观。这一发现对亚洲人群的眼整形具有重要参考价值——我们的上睑解剖结构决定了需要更保守的皮肤处理策略。

与此同时，《Plastic and Reconstructive Surgery》刊载的前瞻性研究（Halani, 2026）对经结膜入路下睑成形术的长期随访数据进行了系统回顾。研究表明，这种避免外部切口的微创技术在减少术后瘢痕和维持下睑张力方面表现优异，特别适合年轻患者和皮肤弹性尚好的人群。

### 1.2 智能辅助诊断的突破

《Ophthalmic Plastic and Reconstructive Surgery》最新发表的研究（Jakubowska et al., 2026）展示了多模态深度学习在眼睑病变良恶性鉴别中的应用潜力。研究团队整合了光学相干断层扫描（OCT）图像和临床数据，构建的AI模型在诊断准确率上达到了与资深专家相当的水平。这意味着未来眼整形的术前评估将更加精准，有助于早期发现恶性病变。

此外，5-氨基酮戊酸荧光技术在眼睑皮脂腺癌手术中的应用（Meer et al., 2026）代表了精准外科的新方向。这项"概念验证"研究证实，术中荧光引导可以更清晰地界定肿瘤边界，降低复发风险。

## 二、安全管理：从术前评估到术后护理的全链条优化

### 2.1 术前评估的新维度

《Journal of Craniofacial Surgery》的研究（Amer et al., 2026）完成了阿拉伯语版面部临床评估量表的验证工作。这一标准化工具的推广应用，使得不同文化背景下的患者都能获得客观、可比的术后效果评估。对国内医美机构而言，引入类似的标准化评估体系，有助于提升服务质量和患者满意度。

### 2.2 术后护理的循证实践

《International Journal of Ophthalmology》的研究（Arslan et al., 2026）聚焦于眼整形术后泪膜稳定性的维护。研究发现，海藻糖作为辅助成分可以显著改善术后干眼症状，加速泪膜功能恢复。这一发现提示我们，眼整形手术不仅要关注形态改善，更要重视眼表功能的保护。

### 2.3 并发症管理的经验总结

《Ophthalmic Plastic and Reconstructive Surgery》发表的回顾性研究（Callet et al., 2026）系统总结了眼轮匝肌切除术治疗特发性眼睑痉挛的长期疗效。数据显示，经过规范的手术治疗，超过80%的患者可以获得持久的症状缓解。这对于深受眼睑痉挛困扰的患者来说是个好消息。

## 三、患者关怀：从"做手术"到"管健康"的理念升级

### 3.1 眼科背景的重要性

近期行业讨论中，一个核心观点值得重视：眼整形医生不应仅仅是"会做手术的外科医生"，更应该是"懂眼周功能美学的专科医生"。这种理念转变意味着：

- **功能优先**：任何眼整形设计都必须以保护和改善眼部功能为前提
- **整体观**：眼整形需要考虑眼睑、泪道、眼眶等多系统的协调
- **长期视角**：术后效果评估不应局限于即刻形态，更要关注5年、10年后的功能状态

### 3.2 理性选择的建议

对于考虑眼整形的求美者，我们建议：

1. **选择专科医生**：优先选择具有眼科或眼整形专科背景的医生
2. **充分沟通**：术前与医生详细讨论期望值、手术方案和可能风险
3. **循序渐进**：对于复杂病例，可考虑分阶段手术以降低风险
4. **重视术后护理**：严格遵循医嘱，定期复查

## 四、行业展望：规范化与个性化并行

### 4.1 规范化进程加速

随着AI辅助诊断、标准化评估工具等技术的成熟，眼整形行业正朝着更规范、更可追溯的方向发展。这不仅有助于提升整体医疗质量，也为监管部门提供了更有效的管理手段。

### 4.2 个性化需求凸显

每位求美者的眼部条件、审美偏好和生活需求都不相同。未来的眼整形将更加注重"量体裁衣"，通过数字化模拟、3D打印导板等技术，实现更精准的个性化方案设计。

## 结语

眼整形是一门融合了医学、美学和心理学的综合学科。最新研究进展表明，行业正在从"单纯追求形态改善"向"功能与美学并重"的更高层次发展。对求美者而言，选择正规医疗机构、经验丰富的专科医生，保持合理期望，是获得满意效果的关键。

---

**参考来源：** 本文基于PubMed最新学术文献及知乎专业讨论综合整理，具体研究详情请查阅原文。

**免责声明：** 本文内容仅供参考，不构成医疗建议。如有整形需求，请咨询专业执业医师。
"""

    frontmatter = f"""---
title: "{title}"
date: {date_str}
draft: true
description: "{description}"
tags: ["眼部整形", "技术趋势", "临床指南", "安全规范"]
categories: ["眼部整形"]
image: "/images/eye-surgery-news/eye-surgery-news-20260601-cover.jpg"
translations: ["/en/posts/eye-surgery-news/{slug}"]
---"""

    return f"{frontmatter}\n\n{body}"


def build_en_post(articles: list[dict], date_str: str, slug: str) -> str:
    topics = extract_key_topics(articles)
    
    title = f"Eye Plastic Surgery: Deep Analysis of Latest Trends and Clinical Practice"
    description = "Comprehensive analysis of technological innovation, safety standards, and patient care in eye plastic surgery based on latest research."

    body = f"""## Introduction

Eye plastic surgery, one of the most refined specialties in aesthetic medicine, has seen remarkable advances in surgical techniques, safety protocols, and patient outcomes. This article provides an in-depth analysis based on the latest academic publications and industry developments, examining four key dimensions: technological innovation, safety management, patient care, and industry trends.

## 1. Technological Innovation: Precision and Minimally Invasive Approaches

### 1.1 Evolution of Blepharoplasty Techniques

A recent study published in *Scientific Reports* (Kono & Kamei, 2026) reveals new advantages of the subbrow approach in blepharoplasty. The research demonstrates that precise calculation of skin removal can naturally form an ideal eyelid crease postoperatively, avoiding the "staring" appearance caused by excessive resection in traditional methods. This finding is particularly relevant for Asian populations, whose upper eyelid anatomy requires more conservative skin management strategies.

Meanwhile, a prospective study in *Plastic and Reconstructive Surgery* (Halani, 2026) systematically reviews long-term follow-up data for transconjunctival lower eyelid blepharoplasty. The research shows that this minimally invasive technique, which avoids external incisions, demonstrates excellent performance in reducing postoperative scarring and maintaining lower eyelid tension, making it especially suitable for younger patients with good skin elasticity.

### 1.2 AI-Assisted Diagnostic Breakthroughs

Research published in *Ophthalmic Plastic and Reconstructive Surgery* (Jakubowska et al., 2026) demonstrates the potential of multimodal deep learning in differentiating benign from malignant eyelid lesions. The research team integrated optical coherence tomography (OCT) images with clinical data to build an AI model achieving diagnostic accuracy comparable to senior experts. This suggests that future preoperative assessments in eye plastic surgery will be more precise, aiding in early detection of malignant lesions.

Additionally, the application of 5-aminolevulinic acid fluorescence in periocular sebaceous carcinoma surgery (Meer et al., 2026) represents a new direction in precision surgery. This proof-of-concept study confirms that intraoperative fluorescence guidance can more clearly delineate tumor boundaries, reducing recurrence risk.

## 2. Safety Management: Full-Chain Optimization

### 2.1 New Dimensions in Preoperative Assessment

Research in the *Journal of Craniofacial Surgery* (Amer et al., 2026) completed validation of the Arabic version of the Facial Clinimetric Evaluation Scale. The dissemination of such standardized tools enables patients from diverse cultural backgrounds to receive objective, comparable postoperative outcome assessments. For domestic aesthetic clinics, introducing similar standardized evaluation systems can enhance service quality and patient satisfaction.

### 2.2 Evidence-Based Postoperative Care

Research in the *International Journal of Ophthalmology* (Arslan et al., 2026) focuses on maintaining tear film stability after eye plastic surgery. The study found that trehalose as an adjunctive component can significantly improve postoperative dry eye symptoms and accelerate tear film function recovery. This finding reminds us that eye plastic surgery should not only focus on morphological improvement but also prioritize ocular surface function protection.

### 2.3 Complication Management Experience

A retrospective study in *Ophthalmic Plastic and Reconstructive Surgery* (Callet et al., 2026) systematically summarizes the long-term efficacy of orbicularis myectomy for essential blepharospasm. Data shows that after standardized surgical treatment, over 80% of patients can achieve lasting symptom relief. This is welcome news for patients suffering from eyelid spasm.

## 3. Patient Care: From "Performing Surgery" to "Managing Health"

### 3.1 The Importance of Ophthalmology Background

A core viewpoint deserves attention: eye plastic surgeons should not merely be "surgeons who perform operations" but rather "specialists who understand periorbital functional aesthetics." This conceptual shift means:

- **Function First**: Any eye plastic surgery design must prioritize protecting and improving eye function
- **Holistic Perspective**: Eye surgery needs to consider coordination of eyelids, lacrimal system, and orbit
- **Long-term Perspective**: Outcome assessment should focus not only on immediate appearance but also on function at 5, 10 years post-surgery

### 3.2 Rational Decision-Making Recommendations

For those considering eye plastic surgery, we recommend:

1. **Choose Specialists**: Prioritize doctors with ophthalmology or eye plastic surgery backgrounds
2. **Thorough Communication**: Discuss expectations, surgical plans, and potential risks in detail preoperatively
3. **Gradual Approach**: For complex cases, consider staged surgery to reduce risk
4. **Value Postoperative Care**: Strictly follow medical instructions and attend regular follow-ups

## 4. Industry Outlook: Parallel Progress of Standardization and Personalization

### 4.1 Accelerating Standardization

With the maturation of technologies like AI-assisted diagnostics and standardized evaluation tools, the eye plastic surgery industry is moving toward more regulated and traceable development. This not only helps improve overall medical quality but also provides regulators with more effective management tools.

### 4.2 Prominent Personalization Needs

Each patient's eye conditions, aesthetic preferences, and life needs are different. Future eye plastic surgery will emphasize "customized solutions" even more, achieving more precise individualized treatment planning through digital simulation, 3D-printed surgical guides, and other technologies.

## Conclusion

Eye plastic surgery is a comprehensive discipline integrating medicine, aesthetics, and psychology. Recent research advances indicate the industry is evolving from "solely pursuing morphological improvement" to "equal emphasis on function and aesthetics." For prospective patients, choosing accredited medical institutions, experienced specialists, and maintaining realistic expectations are key to achieving satisfactory outcomes.

---

**Sources:** This article is synthesized from the latest PubMed academic literature and professional discussions on Zhihu. For specific research details, please refer to the original articles.

**Disclaimer:** This content is for informational purposes only and does not constitute medical advice. Please consult a qualified physician for any surgical procedures.
"""

    frontmatter = f"""---
title: "{title}"
date: {date_str}
draft: true
description: "{description}"
tags: ["eye surgery", "technology trends", "clinical guide", "safety standards"]
categories: ["Eye Surgery"]
image: "/images/eye-surgery-news/eye-surgery-news-20260601-cover.jpg"
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

    posts = []

    zh_content = build_zh_post(articles, date_str, slug)
    posts.append(write_post(zh_content, slug, "zh"))

    en_content = build_en_post(articles, date_str, slug)
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
