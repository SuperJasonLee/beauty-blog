## ADDED Requirements

### Requirement: Statistical claims SHALL cite verifiable sources

All numerical claims (counts, percentages, rankings, growth rates, monetary figures) in POST content MUST either reference a footnote with a resolvable URL, or be explicitly attributed to "编辑团队观察" / "编辑团队估算".

#### Scenario: Numerical claim with footnote
- **WHEN** a POST states "美国本土整形手术量在 2026 年第一季度同比增长 22%"
- **THEN** the sentence MUST be followed by `[^N]` and the referenced footnote at the bottom of the POST MUST contain a URL (http/https) to the original source

#### Scenario: Numerical claim without verifiable source
- **WHEN** the author cannot provide a source URL for a numerical claim
- **THEN** the claim MUST be either deleted, or rewritten as a qualitative statement attributed to "编辑团队观察"

#### Scenario: Future-dated source reference
- **WHEN** a footnote references a media article like "ASPS News, March 2026"
- **THEN** the footnote MUST include the full article URL; bare publication name + date is insufficient

---

### Requirement: Named individuals SHALL link to their content

When a POST names a specific person (e.g., "上海九院戴婷婷", "Dr. Jamil Ahmad"), the first mention MUST be accompanied by a footnote pointing to their actual published content or institutional bio page.

#### Scenario: Named XHS blogger
- **WHEN** a POST cites "上海九院戴婷婷《九院医生再痛也要做的三个医美项目》获赞 2649"
- **THEN** the POST MUST link to the actual XHS note URL, OR delete the specific name and metrics and replace with anonymized trend description

#### Scenario: Named medical professional with institutional affiliation
- **WHEN** a POST names a medical society president or department head
- **THEN** a footnote MUST link to the official press release or institutional announcement

---

### Requirement: Footnote URLs SHALL be resolvable

All URLs in footnotes MUST be syntactically valid (parseable by Python's `urllib.parse`) and use whitelisted domains.

#### Scenario: Valid footnote URL
- **WHEN** `audit-posts.py` parses footnote `[^1]: ASPS Statistics. https://www.plasticsurgery.org/news/plastic-surgery-statistics`
- **THEN** the URL is extracted, parsed as valid HTTPS, and recorded as PASS

#### Scenario: Hallucinated URL pattern detection
- **WHEN** a URL contains suspicious patterns (e.g., PubMed ID > 99,999,999, fabricated DOI structure)
- **THEN** audit script flags as WARNING for manual review

#### Scenario: Footnote without URL
- **WHEN** a footnote is `[^4]: 钛媒体. 2026 刚开年，医美这一赛道迎来史上最惨烈"厮杀". 2026.` (no URL)
- **THEN** audit script flags as ERROR

---

### Requirement: News and trend POSTs SHALL include FAQ shortcode

POSTs of type `月度新闻汇总` or `小红书趋势` MUST include the `{{< faq >}}` shortcode with at least 3 Q/A pairs.

#### Scenario: News POST has FAQ
- **WHEN** a POST has `categories: ["行业资讯"]` or `categories: ["行业趋势"]`
- **THEN** the POST body MUST contain `{{< faq >}}` ... `{{< /faq >}}` block with ≥ 3 items

#### Scenario: FAQ format compliance
- **WHEN** FAQ shortcode is present
- **THEN** each item MUST follow `- **<question>?** <answer>` format (per docs/post-publishing-workflow.md §4.3)

---

### Requirement: Frontmatter SHALL contain complete E-E-A-T fields

All POSTs under `content/<lang>/posts/` MUST include `author`, `reviewer`, `lastReviewed`, `medicalAudience`, `translations`, `featuredImage` in frontmatter.

#### Scenario: Missing reviewer field
- **WHEN** audit script parses a POST frontmatter and `reviewer` key is absent
- **THEN** flag as ERROR with message "missing required field: reviewer"

#### Scenario: lastReviewed staleness
- **WHEN** `lastReviewed` is more than 180 days before today
- **THEN** flag as WARNING with message "lastReviewed > 6 months, consider refresh"

#### Scenario: Missing translations link
- **WHEN** a zh-cn POST has no `translations` field, but an `en` counterpart exists at the parallel path
- **THEN** flag as ERROR with message "translations field missing, but en sibling exists"

---

### Requirement: Image paths SHALL be absolute

All image references (in frontmatter `featuredImage`, in markdown `![](...)`, in `{{< figure src="..." >}}`) MUST start with `/`.

#### Scenario: Absolute image path
- **WHEN** a POST has `![现代医美诊所](/images/posts/clinic.jpg)`
- **THEN** audit script records as PASS

#### Scenario: Relative image path (broken)
- **WHEN** a POST has `![现代医美诊所](images/posts/clinic.jpg)` (missing leading slash)
- **THEN** flag as ERROR with file path and line number

---

### Requirement: audit-posts.py SHALL produce machine-readable output

The audit script MUST emit JSON to stdout and exit non-zero on errors.

#### Scenario: Run audit clean
- **WHEN** all POSTs pass all checks
- **THEN** exit code is 0 and stdout contains `{"status": "pass", "total": N, "errors": [], "warnings": []}`

#### Scenario: Run audit with errors
- **WHEN** any POST has at least one ERROR-level finding
- **THEN** exit code is 2 and stdout contains `{"status": "error", "errors": [...]}`

#### Scenario: Run audit with warnings only
- **WHEN** there are WARNING findings but no ERROR
- **THEN** exit code is 1 and stdout contains `{"status": "warning", "warnings": [...]}`

#### Scenario: Per-POST detail
- **WHEN** audit completes
- **THEN** each finding includes `file`, `line` (if applicable), `severity`, `rule_id`, `message`

---

### Requirement: Publishing workflow SHALL integrate audit check

The pre-publish checklist in `docs/post-publishing-workflow.md §8` MUST include running `npm run audit:posts` as a required step.

#### Scenario: Checklist contains audit step
- **WHEN** reviewing `docs/post-publishing-workflow.md`
- **THEN** §8 contains a bullet "run `npm run audit:posts` and confirm exit 0"

#### Scenario: package.json has audit script
- **WHEN** inspecting `package.json` scripts
- **THEN** `audit:posts` key exists and runs `python3 scripts/audit-posts.py content/`
