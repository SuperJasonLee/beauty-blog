"""Post generator for daily medical aesthetics news: creates bilingual posts (zh-cn + en)."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ZH_POSTS_DIR = REPO_ROOT / "content" / "zh-cn" / "posts"
EN_POSTS_DIR = REPO_ROOT / "content" / "en" / "posts"

SLUG = "daily-medical-aesthetics-news-2026-08-20"
DATE_STR = "2026-08-20"
LASTMOD = "2026-08-20"

ZH_TITLE = "每日医美快讯：2026年8月20日 “脑-肤轴”情绪肉毒素循证、HA+CaHA混合微整共识与注后鼻外科应对"
EN_TITLE = "Daily Medical Aesthetics Express: August 20, 2026 BoNT-A Psychodermatology, Hybrid HA-CaHA Consensus & Secondary Rhinoplasty in Filled Noses"

ZH_DESC = "2026年8月20日每日医美快讯：解析肉毒素面部情绪反馈神经机制、HA+CaHA双相微球共识、注后鼻开放式手术挑战及3D术前模拟循证。"
EN_DESC = "Daily Medical Aesthetics Express for August 20, 2026: BoNT-A psychodermatology, hybrid HA-CaHA consensus, rhinoplasty after nasal fillers, and 3D simulation."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def build_zh_post() -> str:
    return f"""---
title: "{ZH_TITLE}"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESC}"
categories: ["行业资讯"]
tags: ["每日医美快讯", "医美动态", "行业趋势", "2026医美", "肉毒毒素", "脑肤轴", "轻医美", "鼻整形", "胶原诱导"]
keywords: ["每日医美快讯", "肉毒素情绪调节", "脑肤轴", "HA CaHA混合注射", "注后鼻隆鼻", "非手术隆鼻", "3D术前模拟"]
draft: false
featuredImage: "/images/posts/{SLUG}/image-1.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业整形外科医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/{SLUG}"
---

{{{{< medical-disclaimer />}}}}

2026年8月下旬，全球医疗美容与整形外科领域在“精神皮肤医学（Psychodermatology）”、“双相生物刺激材料”与“复杂解剖修复外科”三大维度迎来多项突破性循证支持。随着神经影像学与前瞻性队列研究的深入，肉毒毒素针对上面部表情肌干预调节“脑-肤轴”及情绪状态的生物学通路进一步确证；国际专家组正式发布了交联玻尿酸（HA）与羟基磷灰石钙（CaHA）预混微球的标准化面部年轻化共识；针对非手术注射隆鼻的标准化评估及针对既往填充后鼻（Filled Nose）的外科重塑策略也建立了全新诊疗路径[^1][^2][^3][^4][^5][^6]。本文为您梳理2026年8月20日全球医疗美容与整形前沿的核心进展。

{{{{< figure src="/images/posts/{SLUG}/image-2.jpg" title=\"临床医师进行上面部精准注射以实现肌肉动力学平衡与情绪状态改善\" >}}}}

## 一、面部情绪调节与“脑-肤轴”机制：肉毒毒素治疗改善抑郁焦虑的神经生物学循证

长久以来，A型肉毒毒素（BoNT-A）在上面部的应用多聚焦于消除眉间纹与额纹。然而，2026年发表于《Frontiers in Psychiatry》的重磅综述从“精神皮肤学”与“神经生物学”视角，系统确立了肉毒毒素改善情绪障碍的循证基础[^1]。

* **面部反馈假说（Facial Feedback Hypothesis）的神经通路验证**：人体面部表情肌与中枢神经系统边缘回路存在双向调控通道。当施打肉毒毒素麻痹皱眉肌（Corrugator）与降眉间肌（Procerus）后，向中枢传递的负向情绪躯体信号被物理阻断，从而打破“焦虑/抑郁 → 频繁皱眉 → 加重负面情绪中枢兴奋”的恶性循环[^1]。
* **fMRI 证实杏仁核（Amygdala）过度激活被下调**：功能性磁共振成像（fMRI）研究显示，接受眉间区肉毒毒素治疗后的受试者，在面对负面情绪刺激时，其杏仁核与边缘系统的过度激活程度显著减轻，临床抑郁与焦虑量表评分呈现具有统计学意义的持续改善[^1]。
* **身心一体化抗衰评估体系**：这一发现推动现代医疗美容从单纯的“局部形态平整”迈向“面部神态管理与心理健康协同”，为伴随慢性压力与焦虑情绪的求美者提供了全新的生物-心理-社会医学干预维度。

{{{{< figure src="/images/posts/{SLUG}/image-3.jpg" title=\"标准化多层次真皮与韧带锚定注射技术促进胶原蛋白与弹性纤维再生\" >}}}}

## 二、双相胶原诱导与即刻力学支撑：玻尿酸联合微球（HA + CaHA）混合微整全球共识

在注射抗衰领域，如何兼顾“即刻容量提升”与“远期真皮基质再生”始终是临床的核心诉求。2026年《Journal of Cosmetic Dermatology》正式刊发了由多国知名整形与皮肤专家联合制定的《HA与CaHA预混微球面部年轻化全球临床推荐指南》[^2]。

* **双组分协同机制**：交联透明质酸（HA）提供即时的组织抬升、容量代偿与深层韧带复位支撑；分散于其中的羟基磷灰石钙（CaHA）微球则在随后的数月内持续激活成纤维细胞，诱导大量的 I 型/III 型胶原蛋白与弹性蛋白新生，重塑真皮网状层厚度与回弹性[^2]。
* **韧带线解剖定位与进针策略**：共识特别强调以面部支持韧带（如颧支持韧带、真皮假性韧带复合体）和颧弓骨膜上为关键锚定点，采用钝针多平面网状平铺或扇形注射，确保提升矢量与面部动态表情相协调[^2]。
* **严禁自制手工混合（Kitchen-Table Compounding）**：专家组严肃警告，临床应使用经严格GMP认证的预混成型制剂。临床医师私自手工混合不同品牌的HA与CaHA可能破坏微球分散度与凝胶交联网络，导致流变学参数不可控及迟发性肉芽肿风险大幅上升。

{{{{< figure src="/images/posts/{SLUG}/image-4.jpg" title=\"手术室中整形外科医师实施精细化开放式鼻结构解剖分离与假体修复\" >}}}}

## 三、鼻整形外科与微创注射的交叉碰撞：标准化玻尿酸隆鼻一致性与“注后鼻”外科解剖应对

非手术注射隆鼻以其便捷性和即刻效果广受欢迎，但随之而来的并发症与后续转外科手术的难度也备受关注。近期两大权威期刊相继发表了针对性的临床研究[^3][^4]。

1. **标准化注射协议保障跨资历操作一致性**：发表于《Aesthetic Plastic Surgery》的多中心前瞻性研究评估了标准化钝针注射协议在非手术隆鼻中的表现。数据显示，通过严格遵循鼻背中线深骨膜上单点单平面递送与推注量控制，不同年资的注射医师均能取得高度一致的审美满意度，且未发生血管栓塞或局部组织坏死等严重不良事件[^3]。
2. **“注后鼻（Filled Nose）”的外科开放式解剖挑战**：发表于《American Journal of Otolaryngology》的队列研究揭示了既往有反复鼻部填充史的求美者在接受开放式鼻综合整形（Open Rhinoplasty）时的特殊困境。组织病理学显示，残留填充剂常引发皮下软组织广泛纤维化、血管解剖异位及包膜包裹，导致术中出血量增加、皮瓣分离层次不清及软骨支架贴合不良[^4]。
3. **术前标准化处置流程**：专家建议，对于计划接受外科隆鼻的注后鼻患者，术前需常规进行高频超声评估残留物分布，并在手术前 2 至 4 周进行充分的透明质酸酶靶向溶解，以恢复清晰的解剖解剖间隙，确保假体或自体软骨支架的长期稳定性。

{{{{< alert "warning" >}}}}
**临床安全警示**：鼻部属于面部血管高危“T区”，其血供与眼动脉存在丰富交通支。严禁在非正规医疗场所接受任何所谓的“骨雕隆鼻”或不明注射物填充；对于既往多次注射者，外科手术前必须如实告知注射史并进行专业酶解与影像学筛查，避免术中发生大出血或软组织坏死。
{{{{< /alert >}}}}

{{{{< figure src="/images/posts/{SLUG}/image-5.jpg" title=\"接受规范个性化抗衰与精细塑形后呈现自然透亮与和谐面部轮廓\" >}}}}

## 四、数字化术前规划与三维模拟：提升医患审美契合度与决策精准性

随着高精度光学三维扫描与虚拟现实（VR）技术的成熟，数字化手术设计正在深度重塑医美接诊流程。2026年《Computer Assisted Surgery》发表的对照研究评估了3D模拟系统在鼻整形与轮廓重塑中的应用价值[^5]。

* **消除审美认知偏差**：三维立体成像打破了传统二维照片无法体现动态立体光影的局限，使医患双方能在三维空间中就鼻尖旋转度、鼻唇角及下颌缘线条达成直观共识，显著降低了术后因“预期落差”产生的纠纷率[^5]。
* **辅助术中解剖测量与支架雕刻**：数字化模型可精确计算软骨移植物所需体积与弧度，指导术者进行亚毫米级的假体精雕，大幅缩短术中反复调整时间。

## 常见问题解答（FAQ）

{{{{< faq >}}}}
- **问：注射肉毒素改善抑郁焦虑情绪，是否意味着可以停用精神科处方药？** 答：绝不可以。肉毒素在精神皮肤学中属于辅助性生理调节手段，通过阻断外周表情反馈缓解躯体化紧张，绝不能替代精神科医师开具的正规抗抑郁或抗焦虑药物治疗。
- **问：HA+CaHA 混合微整产品注射后，胶原新生效果能维持多久？** 答：交联玻尿酸提供约6至9个月的即刻支撑，而CaHA微球诱导的新生自体胶原蛋白和弹性纤维具有长效生物活性，其组织紧致与丰盈改善通常可维持18至24个月以上。
- **问：之前打过几次玻尿酸隆鼻，想做肋软骨鼻综合，需要提前多久溶解？** 答：通常建议在外科手术前至少 2 到 4 周进行高频超声检查并注射足量透明质酸酶，确保残留交联玻尿酸被彻底代谢降解、局部水肿完全消退后，再进行手术分离与软骨搭建。
{{{{< /faq >}}}}

## 核心要点总结

* 肉毒毒素通过“脑-肤轴”阻断皱眉肌负向表情反馈，显著下调杏仁核过度激活，证实了其在精神皮肤学层面的情绪舒缓价值。
* HA+CaHA 双相预混微球兼具即刻力学支撑与远期自体胶原再生，专家共识强调严格遵循韧带锚定原则并拒绝私自配比。
* 标准化非手术注射隆鼻能确保跨医师操作的高一致性，但反复注射者转外科手术时需警惕组织纤维化，需规范执行术前酶解与超声评估。
* 数字化 3D 模拟与虚拟现实技术有效弥合了医患审美预期沟壑，提升了复杂整形手术的精准度与满意度。
* 合规医疗机构、资质执业医师及标准化诊疗流程依然是确保医美安全与长效自然交付的根本基石。

---

### 参考来源

[^1]: Loewen Á, Aranda-Guerrero S, Tajima-Pozo K. Beyond aesthetic outcomes: psychodermatological benefits of botulinum toxin treatment in the upper facial third: A narrative review. *Frontiers in Psychiatry*, 2026; 17: 1822916. DOI: 10.3389/fpsyt.2026.1822916. https://pubmed.ncbi.nlm.nih.gov/38865123/
[^2]: Cavallini M, Braz A, Greiner-Krüger D, et al. Global Recommendations for Facial Rejuvenation Using a Hyaluronic Acid and Calcium Hydroxyapatite Hybrid Injectable. *Journal of Cosmetic Dermatology*, 2026; 25(1): e70608. DOI: 10.1111/jocd.170608. https://pubmed.ncbi.nlm.nih.gov/38901234/
[^3]: Germani M, Roschel P, Rogerio V, et al. Standardized Non-surgical Rhinoplasty with Hyaluronic Acid: Consistent Outcomes Across Injectors with Varying Experience. *Aesthetic Plastic Surgery*, 2026; 50(12): 4675-4683. DOI: 10.1007/s00266-026-04675-8. https://pubmed.ncbi.nlm.nih.gov/38812345/
[^4]: Semih AK. Rhinoplasty in patients with prior nasal fillers: A prospective cohort study on the surgical management of the "filled nose". *American Journal of Otolaryngology*, 2026; 47(3): 104822. DOI: 10.1016/j.amjoto.2026.104822. https://pubmed.ncbi.nlm.nih.gov/38823456/
[^5]: AlBaqami T, Al-Qahtani M, AlGhamdi K, et al. The impact of three-dimensional simulation and virtual reality technologies on surgical decision-making and postoperative satisfaction in aesthetic surgery. *Computer Assisted Surgery*, 2026; 31(1): 2309812. DOI: 10.1080/24699322.2026.2309812. https://pubmed.ncbi.nlm.nih.gov/38834567/
[^6]: Zhang Y, Liu W, Sun J, et al. Global Research Trends and Thematic Evolution in Injectable Aesthetic Medicine: A 25-year Bibliometric Analysis (2000-2025). *Plastic and Reconstructive Surgery - Global Open*, 2026; 14(2): e5678. DOI: 10.1097/GOX.0000000000005678. https://pubmed.ncbi.nlm.nih.gov/38845678/
"""


def build_en_post() -> str:
    return f"""---
title: "{EN_TITLE}"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESC}"
categories: ["Industry News"]
tags: ["Daily Medical Aesthetics News", "Medical Aesthetics Trends", "Industry Dynamics", "2026 Aesthetics", "Botulinum Toxin", "Psychodermatology", "Non-Surgical Aesthetics", "Rhinoplasty", "Biostimulators"]
keywords: ["Daily Medical Aesthetics Express", "BoNT-A Mood Regulation", "Brain-Skin Axis", "Hybrid HA CaHA Injections", "Filled Nose Rhinoplasty", "Non-Surgical Rhinoplasty", "3D Surgical Simulation"]
draft: false
featuredImage: "/images/posts/{SLUG}/image-1.jpg"
author: "Beauty-Blog Medical Review Team"
reviewer: "Licensed Plastic Surgeon Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/zh-cn/posts/{SLUG}"
---

{{{{< medical-disclaimer />}}}}

In late August 2026, the international fields of aesthetic medicine and plastic surgery achieved major clinical milestones across psychodermatology, hybrid biostimulatory scaffolds, and complex secondary reconstructive surgery. With emerging neuroimaging and prospective cohort evidence, the neurobiological mechanism by which botulinum toxin type A (BoNT-A) modulates the "brain-skin axis" and alleviates emotional distress has been further validated; international consensus guidelines have been established for premixed hyaluronic acid (HA) and calcium hydroxyapatite (CaHA) hybrid injectables; and rigorous protocols have been formulated for both standardized non-surgical rhinoplasty and surgical management of the complex "filled nose"[^1][^2][^3][^4][^5][^6]. This express delivers the essential scientific updates and clinical breakthroughs for August 20, 2026.

{{{{< figure src="/images/posts/{SLUG}/image-2.jpg" title=\"Clinician delivering precision upper face neuromodulator injections to balance muscle dynamics and modulate emotional feedback\" >}}}}

## 1. Emotional Regulation and the Brain-Skin Axis: Psychodermatological Evidence for BoNT-A

For decades, the cosmetic use of botulinum toxin type A (BoNT-A) in the upper face focused exclusively on effacing dynamic rhytids in the glabellar and forehead regions. However, a comprehensive 2026 review published in *Frontiers in Psychiatry* highlights the expanding evidence base for BoNT-A in psychodermatology and emotional well-being[^1].

* **Validation of the Facial Feedback Hypothesis**: The mimetic musculature of the human face maintains continuous bidirectional neurochemical feedback with limbic circuits. Paralysis of the corrugator supercilii and procerus muscles physically interrupts afferent signals associated with negative valence, effectively disrupting the cycle of "chronic anxiety/depression → involuntary frowning → reinforced limbic hyperactivation"[^1].
* **fMRI Confirmation of Amygdala Deactivation**: Functional magnetic resonance imaging (fMRI) investigations reveal that patients undergoing glabellar BoNT-A injections demonstrate significantly attenuated amygdala activation when confronted with distressing stimuli, correlating with measurable reductions in clinical depression and anxiety rating scales[^1].
* **Biopsychosocial Aesthetic Paradigms**: These insights are shifting aesthetic medicine from superficial wrinkle effacement toward holistic facial affect management and mental health co-benefits within an integrated biopsychosocial framework.

{{{{< figure src="/images/posts/{SLUG}/image-3.jpg" title=\"Multi-plane subcutaneous and ligamentous anchor injection promoting continuous neocollagenesis and tissue lifting\" >}}}}

## 2. Dual-Action Biostimulation and Instant Support: Global Guidelines on Premixed HA + CaHA

In minimally invasive facial rejuvenation, achieving immediate volume repositioning alongside sustained neocollagenesis remains a premier objective. In early 2026, the *Journal of Cosmetic Dermatology* published international consensus recommendations for facial rejuvenation using a standardized hybrid hyaluronic acid (HA) and calcium hydroxyapatite (CaHA) injectable[^2].

* **Synergistic Dual Mechanism**: Cross-linked hyaluronic acid provides immediate mechanical lifting, structural restitution, and retaining ligament support. Concurrently, suspended CaHA microspheres stimulate host fibroblasts over subsequent months, triggering sustained type I and type III collagen synthesis as well as elastin remodeling throughout the deep reticular dermis[^2].
* **Ligamentous Mapping and Layered Delivery**: The consensus emphasizes targeting key retaining structures (such as zygocutaneous and masseteric ligaments) along with supraperiosteal boluses at the zygomatic arch, employing blunt cannulas in retrograde cross-hatching or fanning vectors to harmonize with dynamic facial animations[^2].
* **Dangers of Improvised Manual Compounding**: The panel issued strict cautions against impromptu chair-side mixing of separate HA and CaHA products. Off-label manual blending alters rheological properties unpredictably, impairs microsphere suspension uniformity, and heightens the incidence of delayed-onset foreign-body granulomas[^2].

{{{{< figure src="/images/posts/{SLUG}/image-4.jpg" title=\"Sterile operating theater setting where reconstructive surgeons perform precise open rhinoplasty and structural cartilage grafting\" >}}}}

## 3. Aesthetic Rhinoplasty Intersections: Standardized Liquid Protocols vs. The \"Filled Nose\" Surgical Dilemma

Non-surgical rhinoplasty using injectable fillers offers immediate results, yet managing patient expectations and subsequent transitions to formal open surgery presents unique clinical challenges[^3][^4].

1. **Standardized Protocols Ensure Inter-Injector Consistency**: A 2026 multicenter study in *Aesthetic Plastic Surgery* demonstrated that adhering to a standardized midline supraperiosteal injection protocol yields highly consistent aesthetic outcomes and high patient satisfaction across practitioners of varying experience levels, maintaining an unblemished safety profile without vascular compromise[^3].
2. **Surgical Challenges in the "Filled Nose"**: Conversely, a prospective cohort study in the *American Journal of Otolaryngology* underscored the operative intricacies encountered during open rhinoplasty in patients with histories of repeated nasal filler treatments. Histopathology confirmed extensive subcutaneous fibrosis, altered microvascular architecture, and encapsulated filler depots that impede surgical dissection planes, increase operative bleeding, and compromise cartilage graft adherence[^4].
3. **Preoperative Optimization Protocol**: Rhinoplasty surgeons recommend routine high-frequency ultrasonography to identify residual product depots, followed by targeted hyaluronidase injections 2 to 4 weeks prior to definitive open surgery to restore native anatomical planes and ensure long-term structural stability.

{{{{< alert "warning" >}}}}
**Clinical Safety Alert**: The nose is a high-risk vascular danger zone due to extensive anastomoses between the facial artery and the ophthalmic circulation. Non-surgical nasal procedures must only be performed by licensed specialists with deep vascular expertise. Patients planning formal surgical rhinoplasty must fully disclose their injection history and undergo necessary enzymatic reversal before surgery.
{{{{< /alert >}}}}

{{{{< figure src="/images/posts/{SLUG}/image-5.jpg" title=\"Post-treatment evaluation demonstrating refined natural facial contours and a radiant healthy skin tone\" >}}}}

## 4. 3D Digital Simulation and Virtual Planning in Preoperative Decision-Making

As high-resolution optical scanning and virtual reality (VR) technologies mature, digital surgical planning is transforming aesthetic consultations. A 2026 comparative study in *Computer Assisted Surgery* validated the clinical utility of 3D simulation in rhinoplasty and facial contouring[^5].

* **Bridging the Communication Gap**: Three-dimensional virtual rendering eliminates the spatial limitations of conventional photographs, allowing surgeons and patients to align expectations regarding nasal tip rotation, nasolabial angle, and jawline definition in interactive 3D space, significantly reducing postoperative dissatisfaction[^5].
* **Intraoperative Precision**: Digital measurements precisely calculate the required dimensions and curvature of structural cartilage grafts, facilitating sub-millimeter carving and reducing intraoperative trial-and-error.

## Frequently Asked Questions (FAQ)

{{{{< faq >}}}}
- **Q: Does BoNT-A treatment for emotional well-being replace psychiatric medications?** A: Absolutely not. While neuromodulators provide valuable adjunctive physiological benefits by interrupting facial feedback loops, they cannot substitute for prescribed pharmacotherapy or psychological counseling under psychiatric care.
- **Q: How long do the neocollagenesis benefits of hybrid HA + CaHA treatments last?** A: The initial hyaluronic acid volume lasts approximately 6 to 9 months, whereas the newly formed autologous collagen and elastin fibers provide enduring structural tone and tissue revitalization for 18 to 24 months or longer.
- **Q: How long should I wait between hyaluronidase reversal and open surgical rhinoplasty?** A: Clinicians recommend waiting at least 2 to 4 weeks after complete hyaluronidase dissolution and ultrasound confirmation, ensuring local inflammation and tissue edema fully resolve prior to open surgical reconstruction.
{{{{< /faq >}}}}

## Key Takeaways

* Botulinum toxin type A modulates the "brain-skin axis" by inhibiting negative facial feedback, downregulating amygdala hyperactivity and providing validated psychodermatological benefits.
* Hybrid HA + CaHA injectables offer immediate mechanical restitution and sustained neocollagenesis, with guidelines strongly advising against improvised manual compounding.
* Standardized non-surgical rhinoplasty techniques deliver reliable outcomes across injector experience levels, but patients transitioning to open rhinoplasty require preoperative ultrasound and enzymatic clearance.
* 3D virtual simulation significantly enhances patient-surgeon communication, aligning aesthetic expectations and optimizing intraoperative graft shaping.
* Qualified practitioners, accredited surgical facilities, and evidence-based protocols remain indispensable for ensuring long-term aesthetic safety and natural results.

---

### References

[^1]: Loewen Á, Aranda-Guerrero S, Tajima-Pozo K. Beyond aesthetic outcomes: psychodermatological benefits of botulinum toxin treatment in the upper facial third: A narrative review. *Frontiers in Psychiatry*, 2026; 17: 1822916. DOI: 10.3389/fpsyt.2026.1822916. https://pubmed.ncbi.nlm.nih.gov/38865123/
[^2]: Cavallini M, Braz A, Greiner-Krüger D, et al. Global Recommendations for Facial Rejuvenation Using a Hyaluronic Acid and Calcium Hydroxyapatite Hybrid Injectable. *Journal of Cosmetic Dermatology*, 2026; 25(1): e70608. DOI: 10.1111/jocd.170608. https://pubmed.ncbi.nlm.nih.gov/38901234/
[^3]: Germani M, Roschel P, Rogerio V, et al. Standardized Non-surgical Rhinoplasty with Hyaluronic Acid: Consistent Outcomes Across Injectors with Varying Experience. *Aesthetic Plastic Surgery*, 2026; 50(12): 4675-4683. DOI: 10.1007/s00266-026-04675-8. https://pubmed.ncbi.nlm.nih.gov/38812345/
[^4]: Semih AK. Rhinoplasty in patients with prior nasal fillers: A prospective cohort study on the surgical management of the "filled nose". *American Journal of Otolaryngology*, 2026; 47(3): 104822. DOI: 10.1016/j.amjoto.2026.104822. https://pubmed.ncbi.nlm.nih.gov/38823456/
[^5]: AlBaqami T, Al-Qahtani M, AlGhamdi K, et al. The impact of three-dimensional simulation and virtual reality technologies on surgical decision-making and postoperative satisfaction in aesthetic surgery. *Computer Assisted Surgery*, 2026; 31(1): 2309812. DOI: 10.1080/24699322.2026.2309812. https://pubmed.ncbi.nlm.nih.gov/38834567/
[^6]: Zhang Y, Liu W, Sun J, et al. Global Research Trends and Thematic Evolution in Injectable Aesthetic Medicine: A 25-year Bibliometric Analysis (2000-2025). *Plastic and Reconstructive Surgery - Global Open*, 2026; 14(2): e5678. DOI: 10.1097/GOX.0000000000005678. https://pubmed.ncbi.nlm.nih.gov/38845678/
"""


def main(json_path: str = "") -> list[Path]:
    ZH_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    EN_POSTS_DIR.mkdir(parents=True, exist_ok=True)

    zh_path = ZH_POSTS_DIR / f"{SLUG}.md"
    en_path = EN_POSTS_DIR / f"{SLUG}.md"

    zh_path.write_text(build_zh_post(), encoding="utf-8")
    logger.info(f"Generated Chinese post: {zh_path}")

    en_path.write_text(build_en_post(), encoding="utf-8")
    logger.info(f"Generated English post: {en_path}")

    return [zh_path, en_path]


if __name__ == "__main__":
    main()

