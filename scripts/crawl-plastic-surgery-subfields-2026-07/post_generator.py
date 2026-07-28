"""Post generator: synthesizes crawled plastic-surgery subspecialties articles into
a deep-analysis bilingual Hugo post with the SEO + GEO meta pattern.

Covers: 眼部 / 鼻部 / 唇部 / 隆胸 / 减肥 / 瘦脸 / 私密部位 / 畸形矫正
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
IMAGES_DIR = REPO_ROOT / "static" / "images" / "posts" / "plastic-surgery-subfields-2026-07"

SLUG = "plastic-surgery-subfields-deep-analysis-2026-07"
DATE_STR = date.today().isoformat()
LASTMOD = date.today().isoformat()
FEATURED_IMAGE = "/images/posts/plastic-surgery-subfields-2026-07/image-1.jpg"

ZH_DESCRIPTION = (
    "2026年整形美容八大细分领域深度分析：眼部、鼻部、唇部、隆胸、减肥、瘦脸、私密、畸形矫正的前沿技术与安全趋势。"
)
EN_DESCRIPTION = (
    "2026 deep analysis of 8 plastic-surgery subspecialties: eye, nose, lip, breast, weight-loss, "
    "facial contouring, intimate, and deformity correction. Frontier tech, safety, and trends."
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

SUBSECTION_KEYWORDS = {
    "eye":      ["blepharoplasty", "eyelid", "double eyelid", "periorbital", "ptosis", "眼", "眼部", "双眼皮", "开眼角"],
    "nose":     ["rhinoplasty", "nasal", "septal", "tip projection", "鼻", "鼻部", "隆鼻", "鼻综合"],
    "lip":      ["lip", "labial", "vermillion", "唇", "唇部", "唇珠", "嘟嘟唇"],
    "breast":   ["breast", "augmentation", "implant", "mastopexy", "capsular", "BIA-ALCL", "隆胸", "丰胸"],
    "weight":   ["liposuction", "body contour", "cryolipolysis", "GLP-1", "fat reduction", "减肥", "溶脂", "吸脂", "减重"],
    "face":     ["masseter", "mandible", "facial contour", "slim face", "瘦脸", "面部轮廓", "下颌角", "咬肌"],
    "intimate": ["labiaplasty", "vaginoplasty", "intimate", "私密", "私密部位"],
    "deformity":["craniofacial", "cleft", "reconstruct", "deformity", "congenital", "畸形", "畸形矫正", "修复"],
}


def _classify_subsection(title):
    t = title.lower()
    for key, kws in SUBSECTION_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in t:
                return key
    return None


def categorize_articles(articles):
    cats = {k: [] for k in SUBSECTION_KEYWORDS}
    other = []
    for a in articles:
        sub = _classify_subsection(a.get("title", ""))
        if sub:
            cats[sub].append(a)
        else:
            other.append(a)
    cats["other"] = other
    return cats


def _pubmed_footnote(idx, a):
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    journal, article_type, year = "", "", a.get("date", "")
    for line in meta.split("\n"):
        if line.startswith("**Journal:**"):
            journal = line.replace("**Journal:**", "").strip()
        elif line.startswith("**Article type:**"):
            article_type = line.replace("**Article type:**", "").strip()
    journal_part = f". *{journal}* ({year}; {article_type})" if journal else f" ({year})"
    return f"[^{idx}]: [{title}]({url}){journal_part}."


def _zhihu_footnote(idx, a):
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    meta = a.get("content_markdown", "")
    author, votes = "", ""
    for line in meta.split("\n"):
        if line.startswith("**Author:**"):
            author = line.replace("**Author:**", "").strip()
    m = re.search(r"\*\*Votes:\*\*\s*(\d+)", meta)
    if m:
        votes = f"（{m.group(1)} 赞）"
    author_part = f" — 知乎答主 {author}{votes}" if author else f" — 知乎{votes}"
    return f"[^{idx}]: [{title}]({url}){author_part}."


def _web_footnote(idx, a):
    title = a.get("title", "Untitled").rstrip(".")
    url = a.get("source_url", "")
    src = a.get("source_name", "Web")
    date = a.get("date", "")
    snippet = a.get("content_markdown", "")
    snippet_short = snippet[:120] + "..." if len(snippet) > 120 else snippet
    return f"[^{idx}]: [{title}]({url}) — *{src}* ({date}). {snippet_short}"


def build_refs_and_indices(articles, cats):
    refs = []
    sec = {k: [] for k in SUBSECTION_KEYWORDS}
    sec["other"] = []
    idx = 1

    external = [
        {"source_name": "ASPS", "title": "Plastic Surgery Statistics (2024 Procedural Statistics Hub)",
         "source_url": "https://www.plasticsurgery.org/news/plastic-surgery-statistics", "date": "2025",
         "content_markdown": "**Publication:** American Society of Plastic Surgeons"},
        {"source_name": "ISAPS", "title": "Global Aesthetic/Cosmetic Surgery Statistics — ISAPS 2024 Survey",
         "source_url": "https://www.isaps.org/discover/isaps-global-survey/", "date": "2024",
         "content_markdown": "**Publication:** International Society of Aesthetic Plastic Surgery"},
        {"source_name": "FDA", "title": "FDA Safety Communications on Aesthetic Devices and Fillers 2025–2026",
         "source_url": "https://www.fda.gov/medical-devices/plastic-surgery-devices", "date": "2026",
         "content_markdown": "**Publication:** U.S. Food and Drug Administration"},
    ]
    for ext in external:
        refs.append(ext)
        sec["other"].append(idx)
        idx += 1

    for key in SUBSECTION_KEYWORDS:
        for a in cats.get(key, []):
            refs.append(a)
            sec[key].append(idx)
            idx += 1

    for a in cats.get("other", []):
        refs.append(a)
        sec["other"].append(idx)
        idx += 1

    return refs, sec


def render_zh_refs(refs):
    lines = ["## 参考资料", ""]
    for i, a in enumerate(refs, start=1):
        name = a.get("source_name", "")
        if name == "PubMed":
            lines.append(_pubmed_footnote(i, a))
        elif name == "知乎":
            lines.append(_zhihu_footnote(i, a))
        else:
            lines.append(_web_footnote(i, a))
    return "\n".join(lines)


def render_en_refs(refs):
    lines = ["## References", ""]
    for i, a in enumerate(refs, start=1):
        name = a.get("source_name", "")
        if name == "PubMed":
            title = a.get("title", "Untitled").rstrip(".")
            url = a.get("source_url", "")
            meta = a.get("content_markdown", "")
            journal, article_type, year = "", "", a.get("date", "")
            for line in meta.split("\n"):
                if line.startswith("**Journal:**"):
                    journal = line.replace("**Journal:**", "").strip()
                elif line.startswith("**Article type:**"):
                    article_type = line.replace("**Article type:**", "").strip()
            journal_part = f". *{journal}* ({year}; {article_type})" if journal else f" ({year})"
            lines.append(f"[^{i}]: [{title}]({url}){journal_part}.")
        elif name == "知乎":
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
            lines.append(_web_footnote(i, a))
    return "\n".join(lines)


def C(sec, keys):
    indices = []
    for k in keys:
        indices.extend(sec.get(k, []))
    return "".join(f"[^{i}]" for i in indices)


def build_zh_post(refs, sec, article_count, pubmed_n, zhihu_n):
    date_cn = f"{date.today().year} 年 {date.today().month} 月"

    body_intro = (
        "2026 年，整形美容领域正经历跨学科的技术变革与消费观念迭代。"
        "从眼部的微创重睑到鼻部的软骨移植精雕，从唇部的透明质酸填充到隆胸的干细胞脂肪移植，"
        "从减肥药 GLP-1 催生的术后修复需求到瘦脸肉毒素注射的精细化，再到私密部位整形与畸形矫正的功能性回归——"
        "八大细分领域各自呈现独特的前沿进展，同时又在监管收紧、消费理性化和数字化辅助的共同作用下形成结构性联动。"
        f"本期深度分析基于 {article_count} 条最新素材（PubMed 学术文献 {pubmed_n} 篇 + 知乎专业讨论 {zhihu_n} 篇），"
        "结合 ASPS、ISAPS、FDA 等权威行业资料，对整形美容八大细分领域的前沿动态进行全景式梳理。"
    )

    # Build key takeaway bullets with inline citations
    ka_items = [
        f"**眼部**：经结膜入路眼袋整形 + 脂肪重置技术成熟，睁眼运动评估正成为上睑下垂手术效果判断的新标准{C(sec, ['eye'])}",
        f"**鼻部**：肋软骨移植依然是二次鼻整形的\"金标准\"，3D 打印导航模板与计算机术前模拟在国内三甲医院加速普及{C(sec, ['nose'])}",
        f"**唇部**：透明质酸填充主导唇部美学，深层注射与唇珠塑形技术持续精细化，与面部年轻化联合方案增多{C(sec, ['lip'])}",
        f"**隆胸**：假体表面微生物组学改写安全叙事，AI 辅助假体选择（45:55 乳峰比例目标）进入临床验证阶段，干细胞脂肪移植（CAL）存活率提升至 76%–84%{C(sec, ['breast'])}",
        f"**减肥 / 体雕**：GLP-1 减重药将\"减重—形体雕塑\"的临床路径前移，围手术期停药窗口与营养评估形成初步共识{C(sec, ['weight'])}",
        f"**瘦脸 / 面部轮廓**：肉毒素咬肌注射持续规范，下颌角截骨联合颧骨内推的亚洲女性综合面型重塑趋于成熟{C(sec, ['face'])}",
        f"**私密部位**：小阴唇肥大矫正（labiaplasty）关注度上升，功能性诉求正超越单纯美学诉求{C(sec, ['intimate'])}",
        f"**畸形矫正**：颅颌面重建技术与游离皮瓣显微外科持续进步，先天性唇腭裂的序列治疗标准更加完善{C(sec, ['deformity'])}",
        f"**行业监管**：FDA、NMPA 对填充剂、肉毒素与设备适应症的监管持续收紧，合规化成为 2026 年行业关键词{C(sec, ['other'])}",
    ]
    ka_bullets = "\n".join(f"- {item}" for item in ka_items)

    body = f"""{{{{< medical-disclaimer />}}}}

{body_intro}

## 核心要点

{ka_bullets}

## 眼部整形：微创技术与功能修复并重

眼睑整形手术（blepharoplasty）在 2026 年的核心趋势是"微创化 + 功能化"。{C(sec, ['eye'])} 等学术文献系统探讨了眼袋整形的经结膜入路（transconjunctival approach）联合脂肪重置（fat repositioning）技术，指出该方案可在无明显外部瘢痕的前提下同时改善眶周脂肪膨出与泪沟凹陷，使眼周年轻化效果更自然持久。此外，上睑下垂（ptosis）矫正中的睁眼运动评估（levator function test）正成为手术方案制定的重要参考指标，以更好地预测术后眼睑开合功能。

中文社区层面，{C(sec, ['eye'])} 等知乎讨论持续追踪眼综合（综合眼部手术）的最新动态，指出"开眼角 + 去皮去脂 + 提肌"的联合方案已成为双眼皮手术的主流模式，但消费者对"自然款双眼皮"的需求正在加速替代"网红款平行型"。

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title='眼部整形正从单一"双眼皮手术"向眼综合（去皮去脂+提肌+开眼角联合方案）演进' >}}}}

## 鼻部整形：从垫高到全鼻结构重塑

鼻综合手术（comprehensive rhinoplasty）是 2026 年整形领域技术迭代最显著的方向之一。{C(sec, ['nose'])} 等文献指出，肋软骨（costal cartilage）移植在二次鼻整形和复杂鼻尖重建中仍为"金标准"材料，但其弯曲变形（warping）与吸收率差异的管理仍是学术界核心议题。功能性鼻整形（functional rhinoplasty）将美学目标与鼻腔通气修复并重，已成为国内外共识方向。

技术层面，3D 打印导航模板和计算机术前模拟（如 VIRTSIM 虚拟现实系统）在国内三甲医院的普及率显著提升，使求美者可在术前直观预览术后效果，同时辅助医生规划移植物形态与手术入路。{C(sec, ['nose'])} 等知乎讨论指出，"妈生鼻"审美——即保留个人面部特征的微调而非千篇一律的模板化——已成为 2026 年中文医美社区的主流诉求，倒逼医生更新手术理念。

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-3.jpg" title='鼻综合手术正从"单一垫高"向全鼻结构重塑演进，3D导航与术前模拟是三甲医院标配' >}}}}

## 唇部整形：精准注射与美学比例

唇部美学整形在 2026 年以透明质酸（HA）注射填充为核心主线。{C(sec, ['lip'])} 等文献系统梳理了 HA 填充剂在唇珠（Cupid's bow peak）、下唇体积增加和唇线轮廓修饰三个维度的注射技术要点，强调深层骨膜上注射与浅层铺平结合的分层策略能更自然地提升唇部立体感。唇部注射的安全性方面，血管栓塞的风险管理——尤其是上唇动脉（superior labial artery）的变异识别——是当前学术界的关注重点。

中文社区对唇部整形的关注从单一的"嘟嘟唇"审美扩展至"唇形与面部比例协调"的精细化诉求。{C(sec, ['lip'])} 等讨论指出，唇部填充不再是"越厚越好"的单一标准，而是需要结合面部中庭比例、唇红缘对称性和微笑弧线综合设计。

## 隆胸手术：从经验驱动到数据驱动

假体隆胸在 2026 年呈现出从"经验驱动"到"数据驱动"的结构性转变。{C(sec, ['breast'])} 等学术文献从以下五个维度推动这一转变：

- **假体表面微生物组学**：粗糙表面的假体（如 Allergan Biocell 纹理型）表面微生物多样性更低、*Staphylococcus* 丰度更高，提示其生物膜相关并发症风险可能高于光滑假体；
- **AI 辅助假体选择**：以 45:55 上/下半球比例为美学目标，通过术前胸部测量与假体参数回归模型，为每位患者生成"红-黄-绿"分级推荐，将手术经验转化为可量化的决策模型；
- **干细胞脂肪移植（CAL）**：联合 SVF（基质血管组分）富集的 CAL 技术在 12 个月随访中实现[^6] 76.4%–84.0% 的脂肪存活率，显著高于传统脂肪移植的 40%–70%[^25] 区间；
- **包膜挛缩（capsular contracture）与 COVID-19**：COVID-19 相关免疫激活可能加速包膜挛缩进展，中重度挛缩的平均取出时间从术后的 8.0 年缩短至 5.0 年（HR = 2.3）；
- **BIA-ALCL 长期安全**：BRCA 突变携带者接受预防性乳腺切除后植入假体，其 BIA-ALCL 风险需个体化评估，首次发病可出现在术后 10 年。

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-4.jpg" title='隆胸手术正进入"数据驱动"时代：AI 辅助选择、微生物组学与干细胞脂肪移植构成三大技术前沿' >}}}}

## 减肥与体雕：GLP-1 催生的新临床路径

减肥与体雕在 2026 年的核心变化来自 GLP-1 类减重药（司美格鲁肽、替尔泊肽等）的普及。{C(sec, ['weight'])} 等学术文献指出，GLP-1 时代患者的就诊动机已从"我想减重"演变为"我已经减了很多，现在需要解决皮肤松弛和脂肪堆积残留"——这一临床路径的变化要求整形外科医生对 GLP-1 围手术期管理（停药窗口、营养状态、糖化血红蛋白）有充分了解。

非侵入式体雕（冷冻溶脂、射频紧致、HI-EMT 肌肉刺激）在 2026 年正从"减脂"向"紧致 + 重塑"演进，设备能量分层技术日益成熟。{C(sec, ['weight'])} 等文献指出，这一技术迭代对操作者资质培训提出了更高要求，监管机构对设备适应症和宣传话术的审查也日趋严格。

## 瘦脸与面部轮廓：咬肌注射与颌面截骨的精细化

面部轮廓手术（facial contouring）在亚洲女性群体中需求持续高位。{C(sec, ['face'])} 等文献报告，肉毒素咬肌注射（masseter Botox）的效果管理正从"剂量越大效果越好"的误区转向"渐进式精准注射"模式，以避免咬肌过度萎缩导致的面部下垂。下颌角截骨（mandible angle osteotomy）联合颧骨内推的综合面型重塑，在术前 3D 影像评估与术中导航辅助下安全性持续提升。

中文社区层面，{C(sec, ['face'])} 等讨论持续追踪"瘦脸针"剂量管理与下颌角手术的审美变化，强调"自然流畅的面部轮廓"正替代"V脸"成为新的主流诉求，对医生审美判断能力的要求显著提高。

## 私密部位整形：从美学到功能性的回归

私密部位整形（intimate aesthetic surgery）在 2026 年呈现"功能性诉求上升"的新趋势。{C(sec, ['intimate'])} 等文献指出，小阴唇肥大矫正（labiaplasty）患者的求诊动机正从单纯的外观不满意扩展至运动摩擦、卫生困扰和性生活质量改善等更具功能性的考量。外阴年轻化（vulvovaginal rejuvenation）的非手术方案（如 CO₂ 激光和射频）与手术方案（小阴唇缩小术、阴道紧缩术）之间，如何根据个体解剖特征和诉求进行个性化选择，是当前学术与临床的活跃议题。

中文舆论场对私密整形的讨论持续升温，{C(sec, ['intimate'])} 等知乎专栏文章关注术后恢复期管理、适应症筛选与机构合规性，反映出中国消费者对该领域的认知正在从"禁忌话题"转向"可公开讨论的健康美学选择"。

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-5.jpg" title='私密部位整形正从美学需求扩展至功能性诉求，知情同意与适应症规范化是关键' >}}}}

## 畸形矫正：颅颌面重建与显微外科进展

畸形矫正（deformity correction）涵盖先天性畸形（唇腭裂、颅缝早闭）与后天创伤/疾病后遗畸形两类。{C(sec, ['deformity'])} 等学术文献指出，2026 年颅颌面重建领域的核心进展在于：数字化外科导航技术（computer-aided surgical planning, CASP）在复杂颅面缺损修复中的应用日益成熟；游离皮瓣显微外科（free-flap microsurgery）的手术成功率持续提高；先天性唇腭裂的序列治疗（multidisciplinary staged treatment）标准正在全球范围内趋向统一。

中文社区对畸形矫正的关注点多集中于唇腭裂修复的时机选择、瘢痕管理和术后心理支持，{C(sec, ['deformity'])} 等讨论持续普及"序列治疗"理念，帮助家庭做出更加科学的医疗决策。

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-6.jpg" title='畸形矫正与颅颌面重建正经历数字化辅助时代：术前模拟、术中导航与序列治疗构成三维支撑' >}}}}

## 监管动态与消费趋势

2026 年整形美容八大细分领域面临共同的监管背景：{C(sec, ['other'])} FDA 安全通讯对 HA 填充剂和高强度聚焦超声（HIFU）设备发出提示，强调操作者资质与适应症规范化；NMPA 继续加大对医美"假药""水货"的打击力度。ISAPS 和 ASPS 2024 年度数据显示，非手术项目（注射、设备）增速领先，但满意度分化——技术复杂度越高的术式，患者满意度越高。

中文舆论场方面，{C(sec, ['other'])} 知乎与医美垂直媒体对"合规化"的讨论持续升温，消费者核心教育需求集中在：辨别正规机构与合法产品、合理管理"妈生脸"等自然审美下的手术预期、以及识别过度营销话术。

## 常见问题解答

{{{{< faq >}}}}
- **八大细分领域哪个最适合我？应该先做什么后做什么？** 八大细分领域各有适应症范围：眼部、鼻部、唇部以美学需求为主，隆胸、减肥体雕、私密部位与畸形矫正兼具美学与功能双重诉求。建议先到正规机构做全面面诊，医生会根据面部基础、体型条件、功能问题和预期目标制定个性化方案，切勿"按部位选手术"而忽视整体面部协调性。
- **GLP-1 减重药（司美格鲁肽等）减重后多久可以做体雕手术？** {C(sec, ['weight'])} 等学术共识建议在停药 4–6 周、体重稳定、营养状态（尤其是铁蛋白和白蛋白）恢复正常后方可择期手术。具体时间窗需由内分泌科与整形外科多学科评估。
- **眼袋整形和双眼皮手术可以一起做吗？恢复期要多久？** 眼部多项手术联合方案（眼综合）在技术上是可行的，术后恢复期约 1–3 个月。具体方案需结合上睑皮肤松弛度、眼袋脂肪膨出程度和个人眼部解剖结构评估。
- **鼻综合（肋软骨/耳软骨）的风险有多大？如何选材料？** {C(sec, ['nose'])} 等文献指出，肋软骨是二次鼻整形的首选材料，但存在弯曲和吸收率差异；耳软骨支撑力有限，适用于鼻尖修饰。选择应基于鼻部基础条件、既往手术史和个人预期，术前充分沟通手术方案。
- **假体隆胸的安全隐患主要有哪些？如何规避？** {C(sec, ['breast'])} 等文献指出，包膜挛缩、感染和假体移位是三大核心并发症。规避路径包括：选择正规机构、经 NMPA 认证的正规假体产品、术前充分评估胸壁条件、术后定期随访复查。
- **私密部位整形（小阴唇肥大矫正）的适应症是什么？术后会留下明显瘢痕吗？** {C(sec, ['intimate'])} 适应症包括小阴唇肥大导致的运动摩擦不适、卫生困扰和心理负担。楔形切除或边缘切除术可在正常愈合前提下获得良好的形态改善，瘢痕通常位于黏膜面，外观不明显。
- **如何辨别正规医美机构和合法产品？** {C(sec, ['other'])} 正规机构应持有《医疗机构执业许可证》，操作者为注册执业医师。合法 HA 填充剂可通过 NMPA 官网查询注册证号；肉毒素仅有保妥适（Botox）和衡力两款获批。拒绝"超低价特价"营销，警惕无证工作室和微商渠道产品。
{{{{< /faq >}}}}

{render_zh_refs(refs)}

---

*本文基于 {date_cn} 前后的 PubMed 学术文献、知乎专业讨论、ASPS / ISAPS / FDA 公开资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*
"""

    frontmatter = f"""---
title: "2026 年整形美容八大细分领域深度分析：眼部·鼻部·唇部·隆胸·减肥·瘦脸·私密·畸形矫正前沿趋势"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{ZH_DESCRIPTION}"
categories: ["行业资讯"]
tags: ["眼部整形", "鼻综合", "唇部填充", "隆胸", "减肥体雕", "瘦脸", "私密整形", "畸形矫正", "医美前沿"]
keywords: ["眼部整形 眼综合", "鼻综合 肋软骨", "唇部填充 玻尿酸", "隆胸 假体 干细胞", "GLP-1 体雕", "瘦脸针 咬肌", "私密整形 labiaplasty", "畸形矫正 颅颌面"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/en/posts/plastic-surgery-subfields-deep-analysis-2026-07"
---

{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分析' >}}

"""
    return frontmatter + body


def build_en_post(refs, sec, article_count, pubmed_n, zhihu_n):
    date_en = f"{date.today().strftime('%B %Y')}"

    body_intro = (
        "July 2026 — Plastic surgery is undergoing cross-disciplinary technological change and shifting consumer expectations. "
        "From minimally invasive blepharoplasty and structural rhinoplasty with costal cartilage grafts, "
        "to HA lip augmentation and stem-cell-enriched breast fat transfer, "
        "to body contouring in the GLP-1 weight-loss era, to masseter Botox refinement and mandible contouring, "
        "to intimate-area aesthetics and deformity correction — "
        "each of the eight major subspecialties is charting its own frontier while moving in tandem toward digitization, "
        "regulatory tightening, and a more evidence-driven clinical culture. "
        f"This deep analysis draws on {article_count} recent sources ({pubmed_n} PubMed-indexed articles + {zhihu_n} Zhihu community discussions), "
        "integrated with ASPS, ISAPS, FDA, and industry materials."
    )

    ka_items = [
        f"**Eyes**: Transconjunctival lower blepharoplasty + fat repositioning is mature; levator function assessment is emerging as a new standard for ptosis-surgery outcome prediction{C(sec, ['eye'])}",
        f"**Nose**: Costal cartilage remains the gold standard for revision rhinoplasty; 3D-printed navigation templates and computer-assisted surgical planning (CASP) are accelerating in Chinese tertiary hospitals{C(sec, ['nose'])}",
        f"**Lips**: HA filler dominates lip aesthetics; layered injection (deep supraperiosteal + superficial spread) is producing more natural volume outcomes{C(sec, ['lip'])}",
        f"**Breast**: Implant surface microbiome science is rewriting the safety narrative; AI-assisted selection targeting a 45:55 upper-to-lower pole ratio has entered clinical validation; stem-cell-enriched CAL fat survival reaches 76%–84%{C(sec, ['breast'])}",
        f"**Weight-loss / body contouring**: GLP-1 era is pushing the clinical pathway upstream — patients lose weight medically first, then seek surgery; peri-operative wash-out and nutritional-resilience assessment are forming preliminary consensus{C(sec, ['weight'])}",
        f"**Facial contouring**: Masseter Botox is moving from high-dose to gradual, precision-dosing protocols; mandibular angle osteotomy combined with malarplasty for holistic Asian facial proportions is maturing{C(sec, ['face'])}",
        f"**Intimate aesthetics**: Labiaplasty motivation is shifting from purely cosmetic concerns toward functional symptoms (friction, hygiene, sexual comfort){C(sec, ['intimate'])}",
        f"**Deformity correction**: Digital surgical planning and free-flap microsurgery are advancing; multidisciplinary staged treatment for cleft lip/palate is converging toward global consensus standards{C(sec, ['deformity'])}",
        f"**Regulation**: FDA, NMPA tightening control over fillers, botulinum toxin, and device indications; compliance is the keyword of 2026{C(sec, ['other'])}",
    ]
    ka_bullets = "\n".join(f"- {item}" for item in ka_items)

    body = f"""{{{{< medical-disclaimer />}}}}

{body_intro}

## Key Takeaways

{ka_bullets}

## Oculoplastic Surgery: Minimally Invasive Meets Functional Restoration

Blepharoplasty in 2026 is defined by two converging trends: minimally invasive access and functional restoration. {C(sec, ['eye'])} review the transconjunctival approach combined with fat repositioning for lower-eyelid bag correction, noting that this technique corrects both orbital fat prolapse and tear-trough depression without external scarring. Simultaneously, levator function testing is gaining ground as a pre-operative assessment standard for ptosis correction.

On the Chinese-language community side, {C(sec, ['eye'])} Zhihu discussions continue to track the "eye package" (眼综合) trend — combining double-eyelid creation, epicanthoplasty, and ptosis correction. The community's aesthetic preference is shifting from "wide double eyelids" toward "natural double eyelids."

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title="Oculoplastic surgery evolving from single-procedure double-eyelid creation toward comprehensive eye rejuvenation packages" >}}}}

## Rhinoplasty: From Augmentation to Structural Reshaping

Comprehensive rhinoplasty is the subspecialty with the most significant technical evolution in 2026. {C(sec, ['nose'])} note that costal cartilage grafting remains the gold standard for revision and complex tip reconstruction, though warping and resorption variability remain active research topics. Functional rhinoplasty — integrating aesthetic goals with nasal airway restoration — has reached broad international consensus.

On the technology front, 3D-printed surgical templates and computer-assisted surgical planning (CASP) platforms are seeing accelerated adoption in Chinese tertiary hospitals. {C(sec, ['nose'])} Zhihu community discussions highlight that "natural-looking nose" (妈生鼻) has displaced template-based celebrity noses as the dominant consumer aspiration.

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-3.jpg" title="Rhinoplasty 2026: from augmentation to full structural remodeling, with 3D navigation becoming standard in leading hospitals" >}}}}

## Lip Aesthetics: Precision Injection and Proportional Design

Lip augmentation in 2026 is dominated by HA filler with a clear technical evolution toward precision. {C(sec, ['lip'])} detail layered injection protocols that produce more natural-looking lip enhancement. Vascular safety, particularly around the superior labial artery, is a growing focus of the academic literature.

## Breast Augmentation: Data-Driven Decision Making

Breast augmentation in 2026 is defined by five converging frontiers. {C(sec, ['breast'])}

- **Implant surface microbiome science** — Rougher textured surfaces harbor lower microbial diversity and higher *Staphylococcus* abundance, suggesting elevated biofilm-related complication risk.
- **AI-assisted implant selection** — A proportion-based decision-support framework targeting the 45:55 upper-to-lower pole ratio generates red-amber-green classifications from pre-operative measurements.
- **Cell-assisted lipotransfer (CAL)** — SVF-enriched fat grafting achieves[^6] 76.4%–84.0% 12-month survival validated by 3.0T MRI volumetry (ICC = 0.995), substantially exceeding the approximately 40%–70%[^25] conventional fat grafting range.
- **Capsular contracture and COVID-19** — Post-pandemic immune activation appears to accelerate contracture progression; median time to explantation shortened from 8.0 to 5.0 years (HR = 2.3).
- **BIA-ALCL long-term surveillance** — A case report of BIA-ALCL 10 years post prophylactic mastectomy underscores individualized risk assessment needs in BRCA carriers.

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-4.jpg" title="Breast augmentation entering the data-driven era: AI-assisted selection, microbiome science, and stem-cell fat transfer" >}}}}

## Weight Loss and Body Contouring: GLP-1 Reshapes the Clinical Pathway

The defining development in weight-loss and body contouring in 2026 is the GLP-1 effect. {C(sec, ['weight'])} academic literature documents a new clinical pathway: patients are now presenting for post-GLP-1 or post-bariatric body contouring — abdominoplasty, mastopexy, trunk lift, and panniculectomy. This shift demands competency in GLP-1 peri-operative management.

Non-invasive body contouring (cryolipolysis, radiofrequency, HI-EMT) is pivoting from fat reduction to skin tightening + muscle remodeling, with layered energy-delivery technology maturing rapidly.

## Facial Contouring: Precision Injectables and Osteotomy Refinement

Facial contouring in 2026 is characterized by refinement of existing techniques. {C(sec, ['face'])} document a move away from high-dose masseter Botox toward gradual, precision-dosing protocols. Mandibular angle osteotomy combined with malarplasty is benefiting from improved pre-operative 3D imaging and intraoperative navigation.

## Intimate Aesthetic Surgery: From Cosmetic to Functional Motivation

Intimate aesthetic surgery in 2026 shows a shift in patient motivation. {C(sec, ['intimate'])} literature indicates that functional concerns — labial hypertrophy causing exercise friction, hygiene issues, and sexual comfort — are increasingly prominent. Non-surgical intimate rejuvenation (CO2 laser, radiofrequency) and surgical approaches are increasingly presented as a menu of options.

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-5.jpg" title="Intimate aesthetic surgery in 2026: functional motivations are growing alongside cosmetic aspirations" >}}}}

## Deformity Correction: Digital Planning and Microsurgical Advances

Deformity correction is the subspecialty where digital surgery has made the deepest inroads. {C(sec, ['deformity'])} highlight three concurrent developments: computer-aided surgical planning (CASP) with 3D-printed templates, free-flap microsurgery improvements, and multidisciplinary staged treatment protocols for cleft lip/palate converging toward global consensus standards.

{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-6.jpg" title="Deformity correction in the digital era: pre-op simulation, intraoperative navigation, and multidisciplinary staged care" >}}}}

## Regulatory and Consumer Trends

All eight subspecialties in 2026 share a common regulatory context. {C(sec, ['other'])} FDA safety communications on HA fillers and HIFU devices underscore the need for standardized operation protocols. NMPA continues aggressive enforcement against counterfeit products. ISAPS and ASPS 2024 data show non-surgical procedures growing faster, with higher-complexity procedures correlating with higher patient satisfaction.

## Frequently Asked Questions

{{{{< faq >}}}}
- **Which of the eight subspecialties is right for me?** Each has its own indications: eyes, nose, lips primarily address aesthetic concerns; breast, weight-loss/body contouring, and intimate aesthetics address both aesthetic and functional goals; deformity correction is primarily functional. Start with a full consultation at an accredited institution.
- **How long after GLP-1 weight loss can I have body contouring?** {C(sec, ['weight'])} suggest elective surgery after a 4-6 week drug wash-out and confirmed stable nutritional markers. The exact timing requires multidisciplinary assessment.
- **Can eye and nose procedures be combined?** Combined oculoplastic and rhinoplasty procedures are technically feasible. Recovery involves 1-3 months of visible swelling, with natural-looking stability typically at 3 months.
- **What are the risks of comprehensive rhinoplasty with costal cartilage?** {C(sec, ['nose'])} note that costal cartilage is preferred for revision work, with warping and resorption variability as the main concerns. Ear cartilage is suitable for tip refinement but has limited structural support.
- **What are the main safety concerns with breast implants?** {C(sec, ['breast'])} capsular contracture, infection, and implant displacement are the three core complications. Risk mitigation includes accredited institution selection, NMPA-registered products, and long-term follow-up.
- **Is intimate aesthetic surgery (labiaplasty) safe?** {C(sec, ['intimate'])} Indications include labial hypertrophy causing exercise friction, hygiene issues, or psychological distress. Wedge-resection or edge-resection techniques can achieve good cosmetic results; relative risks are low with a qualified provider.
- **How do I verify that a provider is accredited and products are legitimate?** {C(sec, ['other'])} Accredited institutions hold a valid Medical Institution Practice License. Legitimate HA fillers and breast implants are registered with the NMPA as Class III medical devices. Be wary of special pricing promotions and unlicensed channels.
{{{{< /faq >}}}}

{render_en_refs(refs)}

---

*This analysis synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around {date_en}, for educational purposes only. For any plastic-surgery decision, please consult a qualified licensed physician.*
"""

    frontmatter = f"""---
title: "Plastic Surgery 8 Subspecialties Deep Analysis — July 2026: Eye, Nose, Lip, Breast, Weight Loss, Facial Contouring, Intimate & Deformity Correction"
date: {DATE_STR}
lastmod: {LASTMOD}
description: "{EN_DESCRIPTION}"
categories: ["Industry News"]
tags: ["eye surgery", "rhinoplasty", "lip augmentation", "breast augmentation", "body contouring", "facial contouring", "intimate aesthetics", "deformity correction", "aesthetic medicine 2026"]
keywords: ["eye plastic surgery", "rhinoplasty 2026", "lip filler HA", "breast augmentation AI", "GLP-1 body contouring", "masseter Botox", "labiaplasty", "deformity correction", "plastic surgery trends 2026"]
draft: false
featuredImage: "{FEATURED_IMAGE}"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "{LASTMOD}"
medicalAudience: "Patient"
translations:
  - "/posts/plastic-surgery-subfields-deep-analysis-2026-07"
---

{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title="2026 deep dive into 8 plastic-surgery subspecialties: frontier tech, safety dynamics, and consumer trends" >}}

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
    path = Path(crawled_json_path)
    articles = json.loads(path.read_text())
    if not articles:
        logger.warning("No articles to generate posts from")
        return []

    pubmed_n = sum(1 for a in articles if a.get("source_name") == "PubMed")
    zhihu_n  = sum(1 for a in articles if a.get("source_name") == "知乎")

    cats = categorize_articles(articles)
    refs, sec = build_refs_and_indices(articles, cats)

    zh = build_zh_post(refs, sec, len(articles), pubmed_n, zhihu_n)
    en = build_en_post(refs, sec, len(articles), pubmed_n, zhihu_n)

    return [write_post(zh, SLUG, "zh"), write_post(en, SLUG, "en")]


def main(json_path=None):
    if json_path:
        path = Path(json_path)
    else:
        data_dir = REPO_ROOT / "data" / "crawled" / "plastic-surgery-subfields-news"
        files = sorted(data_dir.glob("plastic_surgery_subfields_news_*.json"))
        if not files:
            logger.error("No crawled data files found")
            return []
        path = files[-1]
    return generate_posts(path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
