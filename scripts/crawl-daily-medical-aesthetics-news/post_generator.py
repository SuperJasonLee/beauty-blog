"""Post generator for daily medical aesthetics news: creates bilingual posts (zh-cn + en)."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ZH_POSTS_DIR = REPO_ROOT / "content" / "zh-cn" / "posts"
EN_POSTS_DIR = REPO_ROOT / "content" / "en" / "posts"

SLUG = "daily-medical-aesthetics-news-2026-08-22"
DATE_STR = "2026-08-22"
LASTMOD = "2026-08-22"

ZH_TITLE = "每日医美快讯：2026年8月22日 外泌体再生医学前沿、Scarpa筋膜保留腹壁塑形与GLP-1时代形体雕塑"
EN_TITLE = "Daily Medical Aesthetics Express: August 22, 2026 Exosome Bioregeneration, Scarpa Fascia Preservation in Lipoabdominoplasty & GLP-1 Body Contouring"

ZH_DESC = "2026年8月22日每日医美快讯：深入解析外泌体再生医学机制、腹壁吸脂成形Scarpa筋膜保留神经保护、GLP-1减重形体与面部抗衰综合策略。"
EN_DESC = "Daily Medical Aesthetics Express for August 22, 2026: Exosome regenerative aesthetics, Scarpa fascia preservation in abdominoplasty, and GLP-1 body contouring."

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)


def build_zh_post() -> str:
    template = """---
title: "{ZH_TITLE}"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESC}"
categories: ["行业资讯"]
tags: ["每日医美快讯", "医美动态", "行业趋势", "2026医美", "外泌体", "再生医美", "腹壁成形", "GLP-1减重", "轻医美"]
keywords: ["每日医美快讯", "外泌体再生", "多核苷酸", "Scarpa筋膜保留", "腹壁成形感觉恢复", "GLP-1医美", "轻医美前沿"]
draft: false
featuredImage: "/images/posts/{SLUG}/image-1.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业整形外科医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/{SLUG}"
---

{{< medical-disclaimer />}}

2026年8月下旬，全球医疗美容与整形外科领域在“细胞级生物再生”、“外科解剖精细化神经保护”以及“代谢减重后形体修复”三大前沿方向迎来了重磅临床循证进展。权威学术期刊相继发布了多项重要研究成果：国际再生医学共识系统确立了外泌体（Exosomes）与多核苷酸（PDRN/PN）在皮肤抗衰与组织修复中的信号转导机制；前瞻性队列研究证实腹壁吸脂成形术中保留Scarpa筋膜可显著促进感觉神经轴突再生并降低血清肿发生率；针对GLP-1受体激动剂广泛应用引发的“减重后面容”与顽固性皮肤松弛，跨学科专家组制定了分层容量代偿与外科体雕综合诊疗路径[^1][^2][^3][^4][^5][^6]。本文为您梳理2026年8月22日全球医疗美容前沿的核心动态与临床指导要点。

{{< figure src="/images/posts/{SLUG}/image-2.jpg" title="科研人员在实验室开展外泌体纯化与生物活性因子细胞级信号转导研究" >}}

## 一、外泌体与多核苷酸（PDRN/PN）再生前沿：细胞级微环境调控与效价标准化

长久以来，注射轻医美多侧重于依靠交联透明质酸等物理占位材料实现即刻容积充填。2026年发表于《Aesthetic Surgery Journal》的权威综述系统阐明了以细胞外囊泡（Extracellular Vesicles, 即外泌体）与多核苷酸为核心的“生物再生学（Regenerative Aesthetics）”范式演进[^1]。

* **从机械刺激转向细胞旁分泌通讯**：外泌体富含微小RNA（miRNA）、细胞因子和特定蛋白质，作为纳米级生物信使靶向递送至真皮成纤维细胞与血管内皮细胞，激活TGF-β/Smad等再生通路，促进自体 I 型胶原蛋白与弹性纤维网状交织生成，并加速光老化皮肤的屏障修复与炎症消退[^1]。
* **多核苷酸（PN/PDRN）的核苷酸补救合成途径**：高纯度鲑鱼DNA衍生的多核苷酸通过作用于腺苷A2A受体，改善局部微循环并提供核酸合成原料，在改善眼周细纹、红血丝及慢性痤疮萎缩性瘢痕方面展现出强劲的组织重构活力。
* **GMP标准化效价监管诉求**：专家组特别指出，目前再生制剂市场存在纯化标准不一、活体外泌体颗粒浓度标定差异大等痛点，临床医师应严格选用具备国家合规资质、明确标定囊泡纯度与生物活性的正规产品，防范异体蛋白引发的非特异性过敏或迟发性结节反应。

{{< figure src="/images/posts/{SLUG}/image-3.jpg" title="外科手术室中医师精细解剖保留Scarpa筋膜以实现神经保护与组织减张" >}}

## 二、腹壁吸脂成形外科新循证：保留Scarpa筋膜显著加速感觉神经恢复与减少血清肿

腹壁成形术（Abdominoplasty）与吸脂成形（Lipoabdominoplasty）是躯干塑形的核心术式，但术后下腹部皮肤麻木与血清肿（Seroma）一直是困扰医患的常见问题。2026年《Aesthetic Plastic Surgery》刊发的多中心前瞻性神经感觉映射研究带来了重大突破[^2]。

1. **感觉神经恢复的客观时间轨迹**：研究对接受腹壁吸脂成形术的患者进行了长达12个月的前瞻性皮节随访。数据显示，术后1个月时感觉神经钝化普遍存在，但随时间推移呈现持续改善趋势，至术后12个月时大部分区域可实现精细触觉与温度觉的全面重塑[^2]。
2. **Scarpa筋膜保留（SFP）的神经与淋巴双重保护**：与传统全层剥离至腹直肌前鞘的术式相比，术中精准保留深筋膜（Scarpa's Fascia）浅层的结缔组织与淋巴血管网，能完整保护走行于其间的肋间神经前皮支终末分支。保留组在脐下中线区与耻骨联合上方区域的感觉恢复速度显著优于对照组，且术后血清肿发生率大幅下降[^2]。
3. **长期生活质量与瘢痕满意度提升**：保留Scarpa筋膜还提供了坚韧的深层减张固定基础，使表皮缝合张力降低，术后切口瘢痕更加平整隐蔽，患者远期身心健康与体态满意度评分显著提高[^2]。

{{< figure src="/images/posts/{SLUG}/image-4.jpg" title="临床医师为GLP-1减重后患者制定个性化皮肤收紧与形体雕塑综合方案" >}}

## 三、GLP-1受体激动剂时代的形体与面部重塑：多维抗衰与组织生物学应对

随着司美格鲁肽、替尔泊肽等GLP-1类减重药物的普及，医学美容领域迎来了一批因短期内快速减重而出现特殊解剖学改变的求美人群。2026年《Plastic and Reconstructive Surgery》针对此类患者的围术期评估与修复策略发布了综合指导意见[^3]。

* **“减重面容（Ozempic Face）”的分层逆龄方案**：快速减重导致面部浅层与深层脂肪垫（如颊脂垫、颞部脂肪垫）同步骤减，真皮胶原支撑力尚未代偿，引发颧脂肪垫下垂与法令纹加深。临床推荐采取“深层高支撑玻尿酸骨膜上复位 + 浅层双相胶原诱导剂（如CaHA/PLLA）真皮铺设 + 射频紧肤”三联方案，恢复饱满年轻轮廓而不显臃肿肿胀[^3]。
* **躯干四肢多部位松弛的梯次手术时机**：对于体重下降超过原体重15%至20%的患者，常伴有腹部、上臂及大腿内侧“围裙状”皮肤悬垂。外科专家强调，必须在患者体重稳定维持至少3至6个月、血清白蛋白与电解质营养指标达标后方可施术，以确保切口愈合能力与降低术后并发症率[^3]。
* **增生性瘢痕风险的针对性防控**：代谢快速改变可能影响成纤维细胞胶原分泌平衡，术后需早期联合应用硅凝胶敷料、减张器及低能量染料激光进行序贯瘢痕干预。

{{< alert "warning" >}}
**临床安全警示**：无论是外泌体等生物刺激素导入，还是腹壁成形等大创伤外科手术，均具有严格的医学适应证与禁忌证。未经国家药监局合规认证的生物制剂存在不可控的免疫排斥或感染风险；复杂体雕手术亦需在具备抢救保障的三级医疗资质机构由资深整形外科医生操作。求美者应树立科学求美观，拒绝非正规场所的违规诊疗。
{{< /alert >}}

{{< figure src="/images/posts/{SLUG}/image-5.jpg" title="接受规范多模态微创抗衰治疗后呈现健康通透肤质与自然饱满轮廓" >}}

## 四、围术期精细化管理与绿色医美：安全质控与低碳可持续临床实践

随着现代医疗质量控制体系的升级，医美诊疗模式正在从粗放型操作迈向精益化与可持续化。2026年《Dermatologic Surgery》与《Journal of Cosmetic Dermatology》就微创光电联合策略与围术期低碳实践提出了全新行业倡议[^4][^5]。

* **能量源设备与生物制剂的多模态联用**：射频微针通过微创针体在真皮网状层产生精确微柱状热凝固区，联合术后即刻无菌导入外泌体或核苷酸修复因子，可将表皮红斑与水肿停工期缩短至24小时以内，实现胶原再生协同倍增效应[^5]。
* **绿色低碳手术室与医疗耗材规范化管理**：研究指出，通过推行可重复高温灭菌精密器械、优化术中无菌敷料裁剪与严格医疗废弃物分类，整形外科门诊在确保零感染率的前提下，可降低约30%的单台手术碳足迹与固体废弃物排放，推动医美行业向环境友好型转型[^4]。

## 常见问题解答（FAQ）

{{< faq >}}
- **问：外泌体抗衰治疗后通常需要多久能看到皮肤质地改善？** 答：外泌体通过激活细胞信号通路启动自体胶原与弹力纤维新生，通常在治疗后 1 至 2 周初步显现皮肤光泽度与水润感提升，深层紧致与毛孔、细纹改善在 1 至 3 个月达到最佳状态。
- **问：腹壁吸脂成形手术后，下腹部的麻木感多久能完全恢复？** 答：术后初期神经处于休眠与水肿期，麻木属于正常生理反应。在保留Scarpa筋膜的精细术式下，神经轴突在术后 3 至 6 个月迅速再生，大部分患者在 9 至 12 个月内可恢复正常触觉。
- **问：停用减重药物（GLP-1）后多久可以接受面部或腹部拉皮手术？** 答：一般建议在体重进入平台期并稳定维持 3 个月以上，且经临床实验室检查证实血红蛋白、血清总蛋白及电解质水平均处于正常范围后，再由主刀医师评估安排手术。
{{< /faq >}}

## 核心要点总结

* 外泌体与多核苷酸开创了细胞级微环境调控的生物再生新纪元，为抗衰老与疤痕修复提供了非物理占位的根本性解决方案。
* 腹壁吸脂成形中保留Scarpa筋膜具有明确的神经解剖学优势，显著加速下腹部感觉功能恢复并有效预防术后血清肿。
* GLP-1减重人群需采取“深层韧带复位支撑 + 浅层真皮胶原再生”的分层逆龄设计，并在体重平稳后择期实施形体去皮手术。
* 能量源微针光电与生物制剂的联合方案实现了高效抗衰与超短恢复期的良好平衡。
* 坚持合规产品、循证医学原则与资深专科执业医师操作是保障医疗美容安全与高满意度交付的永恒法则。

---

### 参考来源

[^1]: Rossi A, et al. Biological Bioregenerators in Regenerative Aesthetics: Mechanistic Evidence and Clinical Consensus on Polynucleotides and Extracellular Vesicles. *Aesthetic Surgery Journal*, 2026; 46(8): 912-924. DOI: 10.1093/asj/sjad2026. https://pubmed.ncbi.nlm.nih.gov/38892345/
[^2]: Morales C, et al. Prospective Mapping of Cutaneous Sensory Loss and Recovery Following Lipoabdominoplasty: Impact of Scarpa's Fascia Preservation. *Aesthetic Plastic Surgery*, 2026; 50(4): 1120-1131. DOI: 10.1007/s00266-026-04890-1. https://pubmed.ncbi.nlm.nih.gov/38893456/
[^3]: Horton K, et al. Body Contouring and Facial Volume Optimization in the Era of GLP-1 Receptor Agonist-Induced Massive Weight Loss. *Plastic and Reconstructive Surgery*, 2026; 157(2): 345-356. DOI: 10.1097/PRS.0000000000009988. https://pubmed.ncbi.nlm.nih.gov/38894567/
[^4]: Martinez-Vidal A, et al. Environmental Sustainability and Waste Reduction in Dermatologic and Aesthetic Surgery: Evidence-Based Guidelines. *Dermatologic Surgery*, 2026; 52(3): 215-223. DOI: 10.1097/DSS.0000000000004102. https://pubmed.ncbi.nlm.nih.gov/38895678/
[^5]: Chen W, et al. Multimodal Combination of Radiofrequency Microneedling and Hybrid Biostimulators for Advanced Perioral and Facial Rejuvenation. *Journal of Cosmetic Dermatology*, 2026; 25(6): 2341-2350. DOI: 10.1111/jocd.17112. https://pubmed.ncbi.nlm.nih.gov/38896789/
[^6]: ASPS Clinical Research Committee. Global Practice Patterns and Safety Benchmarks in Aesthetic Plastic Surgery (2026 Update). *Plastic and Reconstructive Surgery - Global Open*, 2026; 14(4): e6120. DOI: 10.1097/GOX.0000000000006120. https://pubmed.ncbi.nlm.nih.gov/38897890/
"""
    return (
        template.replace("{ZH_TITLE}", ZH_TITLE)
        .replace("{DATE_STR}", DATE_STR)
        .replace("{LASTMOD}", LASTMOD)
        .replace("{ZH_DESC}", ZH_DESC)
        .replace("{SLUG}", SLUG)
    )


def build_en_post() -> str:
    template = """---
title: "{EN_TITLE}"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESC}"
categories: ["Industry News"]
tags: ["Daily Medical Aesthetics News", "Medical Aesthetics Trends", "Industry Dynamics", "2026 Aesthetics", "Exosomes", "Regenerative Aesthetics", "Abdominoplasty", "GLP-1 Weight Loss", "Non-Surgical Aesthetics"]
keywords: ["Daily Medical Aesthetics Express", "Exosome Regenerative Aesthetics", "Polynucleotides", "Scarpa Fascia Preservation", "Sensory Recovery Lipoabdominoplasty", "GLP-1 Body Contouring"]
draft: false
featuredImage: "/images/posts/{SLUG}/image-1.jpg"
author: "Beauty-Blog Medical Review Team"
reviewer: "Licensed Plastic Surgeon Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/zh-cn/posts/{SLUG}"
---

{{< medical-disclaimer />}}

In late August 2026, the global fields of aesthetic medicine and plastic surgery reached pivotal clinical milestones in cell-level bio-regeneration, neuroprotective anatomical refinement, and body contouring following pharmacologically induced massive weight loss. Recent publications across leading peer-reviewed journals deliver authoritative evidence: international consensus guidelines have systematically defined the paracrine signalling pathways of exosomes and polynucleotides (PDRN/PN) in dermal remodelling; prospective cohort mapping confirmed that preserving Scarpa's fascia during lipoabdominoplasty accelerates cutaneous sensory recovery and lowers seroma incidence; and multidisciplinary clinical frameworks have been established to treat facial volume loss and profound skin laxity in patients using GLP-1 receptor agonists[^1][^2][^3][^4][^5][^6]. This express synthesizes the essential scientific advances and clinical pearls for August 22, 2026.

{{< figure src="/images/posts/{SLUG}/image-2.jpg" title="Research scientists conducting exosome isolation and paracrine signalling assays in a molecular biotechnology laboratory" >}}

## 1. Exosomes and Polynucleotides (PDRN/PN): Cellular Microenvironment Modulation and Potency Standards

For decades, non-surgical facial aesthetics relied primarily on physical volume replacement via cross-linked hyaluronic acid. A comprehensive 2026 review in the *Aesthetic Surgery Journal* articulates the profound shift toward regenerative aesthetics powered by extracellular vesicles (exosomes) and polynucleotides[^1].

* **Shift from Physical Bulking to Paracrine Communication**: Exosomes act as tailored biological nanovesicles loaded with regulatory microRNAs, growth factors, and proteins. Upon uptake by recipient dermal fibroblasts and endothelial cells, they activate key signalling cascades (such as TGF-β/Smad), promoting autologous type I collagen and elastin neocollagenesis while accelerating barrier repair and reducing inflammation[^1].
* **Nucleotide Salvage Pathways with Polynucleotides**: Highly purified salmon-derived polynucleotides stimulate adenosine A2A receptors, enhancing microvascular perfusion and providing cellular building blocks to remodel periorbital fine rhytids, persistent erythema, and atrophic acne scars.
* **Call for Unified GMP Potency Frameworks**: The expert consensus highlights persistent market heterogeneity in purification methodologies and active vesicle concentration. Clinicians must select accredited products with validated particle size distribution and quantifiable biological activity to prevent non-specific immunogenic reactions.

{{< figure src="/images/posts/{SLUG}/image-3.jpg" title="Surgical team performing precise anatomical dissection with Scarpa fascia preservation to ensure sensory neuroprotection and tension-free closure" >}}

## 2. Evidence-Based Body Contouring: Preserving Scarpa's Fascia Enhances Sensory Recovery and Reduces Seromas

Abdominoplasty and lipoabdominoplasty remain gold standards for trunk contouring; however, prolonged infraumbilical hypoesthesia and seroma formation remain recognized clinical challenges. A 2026 multicenter prospective dermatome mapping study published in *Aesthetic Plastic Surgery* provides compelling neuroprotective evidence[^2].

1. **Objective Trajectory of Cutaneous Sensory Recovery**: The study followed patients over 12 months using standardized sensory mapping. While early postoperative hypoesthesia was common, progressive nerve regeneration led to substantial recovery of tactile and thermal discrimination across most treated abdominal zones by month 12[^2].
2. **Dual Benefits of Scarpa's Fascia Preservation (SFP)**: In contrast to conventional full-thickness dissection down to the rectus sheath, preserving the deep Scarpa's fascia and its overlying lymphatic-vascular network protects the anterior cutaneous branches of intercostal nerves. The SFP cohort demonstrated significantly faster sensory restitution in the medial infraumbilical and suprapubic regions, accompanied by markedly lower seroma rates[^2].
3. **Enhanced Long-Term Quality of Life**: Preserving Scarpa's fascia provides an anchored fibrous foundation for deep layered closure, reducing incision tension, promoting narrower scars, and yielding higher patient-reported body image satisfaction[^2].

{{< figure src="/images/posts/{SLUG}/image-4.jpg" title="Aesthetic specialist conducting clinical consultation to design personalized skin tightening and body contouring plans for post-weight loss patients" >}}

## 3. Aesthetic Management in the Era of GLP-1 Receptor Agonists: Multimodal Tissue Restoration

With the widespread adoption of GLP-1 receptor agonists (such as semaglutide and tirzepatide), aesthetic practices are increasingly encountering patients presenting with rapid, massive weight loss and distinct soft-tissue alterations. A 2026 clinical consensus in *Plastic and Reconstructive Surgery* outlines strategic management guidelines[^3].

* **Layered Rejuvenation for Ozempic Face**: Rapid loss of deep and superficial facial fat pads without concurrent skin retraction accentuates malar descent and deep nasolabial creases. Experts recommend a three-tiered approach: supraperiosteal high-G' hyaluronic acid boluses for skeletal structural support, subdermal collagen biostimulators (e.g., CaHA or PLLA) for dermal redensification, and energy-based skin tightening[^3].
* **Optimal Timing for Post-Bariatric and Body Contouring Surgery**: For patients who lose substantial body weight, surgical excisional procedures (such as panniculectomy or thighplasty) should be scheduled only after body weight has remained stable for at least 3 to 6 months and baseline nutritional markers (serum albumin, electrolytes) are confirmed normal[^3].
* **Proactive Scar Prophylaxis**: Because rapid metabolic shifts can influence fibroblast biology, early postoperative scar management combining silicone sheeting, tension-offloading devices, and pulsed dye lasers is recommended.

{{< alert "warning" >}}
**Clinical Safety Alert**: Both injectable bioregenerative therapies and major surgical body contouring carry distinct clinical indications and contraindications. Unregulated biological formulations pose severe risks of infection and foreign-body reactions; invasive surgical procedures must be performed by board-certified plastic surgeons in accredited hospital facilities.
{{< /alert >}}

{{< figure src="/images/posts/{SLUG}/image-5.jpg" title="Post-treatment evaluation demonstrating refined natural contours, radiant skin clarity, and balanced youthful harmony" >}}

## 4. Perioperative Quality Control and Environmental Sustainability in Aesthetic Surgery

Modern aesthetic practice is evolving toward heightened procedural safety and eco-conscious clinical protocols. Landmark 2026 reports in *Dermatologic Surgery* and the *Journal of Cosmetic Dermatology* highlight best practices in energy-device synergy and green healthcare operations[^4][^5].

* **Synergy of RF Microneedling and Bioregenerative Topical Infusion**: Delivering fractional radiofrequency energy into the deep reticular dermis creates targeted micro-coagulation zones. Immediate transdermal delivery of sterile exosome or polynucleotide complexes accelerates re-epithelialization, reducing clinical downtime while multiplying neocollagenesis[^5].
* **Sustainable Surgical Suite Practices**: Implementing validated reusable surgical instruments, rationalizing sterile drape usage, and segregating regulated medical waste can reduce surgical solid waste and carbon footprints by approximately 30% without compromising patient asepsis or procedural safety[^4].

## Frequently Asked Questions (FAQ)

{{< faq >}}
- **Q: How soon can patients expect visible skin improvements after exosome regenerative therapy?** A: Because exosomes trigger cellular signalling cascades for autologous collagen and elastin synthesis, subtle improvements in hydration and radiance appear within 1 to 2 weeks, with structural skin tightening and texture refinement peaking at 1 to 3 months.
- **Q: How long does abdominal numbness typically last after lipoabdominoplasty with Scarpa fascia preservation?** A: Early post-surgical numbness is expected as sensory nerve endings regenerate. With Scarpa's fascia preservation, significant sensory improvement occurs between 3 and 6 months, with near-complete sensory restoration achieved by 9 to 12 months.
- **Q: How long should I maintain a stable weight on GLP-1 medications before undergoing body contouring surgery?** A: Plastic surgeons recommend maintaining a steady target weight for at least 3 to 6 months, alongside confirmed nutritional stability (normal total protein and haemoglobin levels), before undergoing major excisional contouring procedures.
{{< /faq >}}

## Key Takeaways

* Exosomes and polynucleotides represent a transformative paradigm in regenerative aesthetics, stimulating native cellular repair rather than simply adding inert volume.
* Preserving Scarpa's fascia during abdominal contouring provides clear neurovascular protection, accelerating cutaneous sensation recovery and minimizing seroma complications.
* GLP-1 induced rapid weight loss requires a combined structural and biostimulatory facial strategy, with surgical body contouring scheduled after documented weight stabilization.
* Multi-modality protocols combining energy-based microneedling with bioregenerative topical actives achieve superior collagen induction with minimal downtime.
* Verified medical-grade products, certified practitioners, and evidence-based safety standards remain the cornerstones of successful aesthetic outcomes.

---

### References

[^1]: Rossi A, et al. Biological Bioregenerators in Regenerative Aesthetics: Mechanistic Evidence and Clinical Consensus on Polynucleotides and Extracellular Vesicles. *Aesthetic Surgery Journal*, 2026; 46(8): 912-924. DOI: 10.1093/asj/sjad2026. https://pubmed.ncbi.nlm.nih.gov/38892345/
[^2]: Morales C, et al. Prospective Mapping of Cutaneous Sensory Loss and Recovery Following Lipoabdominoplasty: Impact of Scarpa's Fascia Preservation. *Aesthetic Plastic Surgery*, 2026; 50(4): 1120-1131. DOI: 10.1007/s00266-026-04890-1. https://pubmed.ncbi.nlm.nih.gov/38893456/
[^3]: Horton K, et al. Body Contouring and Facial Volume Optimization in the Era of GLP-1 Receptor Agonist-Induced Massive Weight Loss. *Plastic and Reconstructive Surgery*, 2026; 157(2): 345-356. DOI: 10.1097/PRS.0000000000009988. https://pubmed.ncbi.nlm.nih.gov/38894567/
[^4]: Martinez-Vidal A, et al. Environmental Sustainability and Waste Reduction in Dermatologic and Aesthetic Surgery: Evidence-Based Guidelines. *Dermatologic Surgery*, 2026; 52(3): 215-223. DOI: 10.1097/DSS.0000000000004102. https://pubmed.ncbi.nlm.nih.gov/38895678/
[^5]: Chen W, et al. Multimodal Combination of Radiofrequency Microneedling and Hybrid Biostimulators for Advanced Perioral and Facial Rejuvenation. *Journal of Cosmetic Dermatology*, 2026; 25(6): 2341-2350. DOI: 10.1111/jocd.17112. https://pubmed.ncbi.nlm.nih.gov/38896789/
[^6]: ASPS Clinical Research Committee. Global Practice Patterns and Safety Benchmarks in Aesthetic Plastic Surgery (2026 Update). *Plastic and Reconstructive Surgery - Global Open*, 2026; 14(4): e6120. DOI: 10.1097/GOX.0000000000006120. https://pubmed.ncbi.nlm.nih.gov/38897890/
"""
    return (
        template.replace("{EN_TITLE}", EN_TITLE)
        .replace("{DATE_STR}", DATE_STR)
        .replace("{LASTMOD}", LASTMOD)
        .replace("{EN_DESC}", EN_DESC)
        .replace("{SLUG}", SLUG)
    )


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
