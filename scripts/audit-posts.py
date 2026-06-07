#!/usr/bin/env python3
"""
audit-posts.py - Static checker for Hugo POST citation integrity.

Implements requirements from openspec/specs/post-citation-integrity/spec.md
(once archived: openspec/specs/post-citation-integrity/spec.md).

Exit codes:
  0 = all pass
  1 = warnings only
  2 = errors found
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

REQUIRED_FRONTMATTER_FIELDS = [
    "title",
    "date",
    "description",
    "categories",
    "tags",
    "draft",
    "author",
    "lastReviewed",
    "medicalAudience",
    "featuredImage",
]

NEWS_TREND_CATEGORIES = {"行业资讯", "行业趋势", "Industry News", "Industry Trends"}

FAQ_OPEN_RE = re.compile(r"\{\{<\s*faq\s*>\}\}")
FAQ_CLOSE_RE = re.compile(r"\{\{<\s*/\s*faq\s*>\}\}")
FAQ_ITEM_RE = re.compile(r"^\s*-\s+\*\*[^*]+\*\*", re.MULTILINE)

FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.+)$", re.MULTILINE)
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]]+)\]")
URL_RE = re.compile(r"https?://[^\s\)\]>]+")

FIGURE_SRC_RE = re.compile(r'\{\{<\s*figure\s+[^>]*src="([^"]+)"')
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

PCT_RE = re.compile(r"([+\-]?\s*\d{1,4}(?:\.\d+)?\s*%)")

CHINESE_NAME_LIKES_RE = re.compile(
    r"(上海九院|北京协和|复旦|华西|湘雅|301|301医院)[^\n]{0,30}?获赞\s*(\d+)"
)

PERSON_NUM_LIKES_RE = re.compile(r"获赞\s*(\d+)")

WARN_DOMAINS_SUSPICIOUS = {"example.com", "test.com"}


@dataclass
class Finding:
    file: str
    line: int | None
    severity: str  # "error" | "warning" | "info"
    rule_id: str
    message: str


def parse_frontmatter(text: str) -> tuple[dict, int, int]:
    """Return (fields dict, fm_start_line, body_start_line)."""
    if not text.startswith("---"):
        return {}, 0, 1
    end_match = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not end_match:
        return {}, 0, 1
    fm_text = text[3 : end_match.start() + 3]
    fm_start_line = 1
    body_start_line = fm_text.count("\n") + 2
    fields: dict = {}
    current_key = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^(\w[\w\-]*)\s*:\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            value = m.group(2).strip()
            if not value:
                fields[current_key] = []
            elif value.startswith("["):
                items = re.findall(r'"([^"]*)"', value)
                fields[current_key] = items
            elif value.startswith('"') and value.endswith('"'):
                fields[current_key] = value[1:-1]
            else:
                fields[current_key] = value
        elif line.lstrip().startswith("-") and current_key is not None:
            val_match = re.match(r'^\s*-\s*"?([^"]*)"?\s*$', line)
            if val_match:
                v = val_match.group(1).strip()
                if isinstance(fields.get(current_key), list):
                    fields[current_key].append(v)
                else:
                    fields[current_key] = [v]
    return fields, fm_start_line, body_start_line


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_frontmatter(path: Path, text: str, fields: dict) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(path)

    for key in REQUIRED_FRONTMATTER_FIELDS:
        if key not in fields or fields.get(key) in (None, "", []):
            findings.append(
                Finding(rel, 1, "error", "FM001", f"missing required field: {key}")
            )

    if "translations" not in fields or not fields.get("translations"):
        sibling = _sibling_translation(path)
        if sibling and sibling.exists():
            findings.append(
                Finding(
                    rel,
                    1,
                    "error",
                    "FM002",
                    f"translations field missing; sibling exists at {sibling}",
                )
            )

    if "reviewer" not in fields:
        findings.append(
            Finding(rel, 1, "warning", "FM003", "missing recommended field: reviewer")
        )

    last_reviewed = fields.get("lastReviewed")
    if last_reviewed:
        from datetime import datetime, date

        try:
            d = datetime.strptime(last_reviewed, "%Y-%m-%d").date()
            days = (date.today() - d).days
            if days > 180:
                findings.append(
                    Finding(
                        rel,
                        1,
                        "warning",
                        "FM004",
                        f"lastReviewed > 180 days ({days}d), consider refresh",
                    )
                )
        except ValueError:
            findings.append(
                Finding(
                    rel,
                    1,
                    "warning",
                    "FM005",
                    f"lastReviewed not YYYY-MM-DD: {last_reviewed}",
                )
            )

    featured = fields.get("featuredImage", "")
    if featured and not featured.startswith("/"):
        findings.append(
            Finding(
                rel,
                1,
                "error",
                "IMG001",
                f"featuredImage must start with /: {featured}",
            )
        )

    return findings


def _sibling_translation(path: Path) -> Path | None:
    parts = path.parts
    if "zh-cn" in parts:
        new_parts = tuple("en" if p == "zh-cn" else p for p in parts)
    elif "en" in parts:
        new_parts = tuple("zh-cn" if p == "en" else p for p in parts)
    else:
        return None
    return Path(*new_parts)


def check_images(path: Path, text: str, body_start: int) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(path)
    for m in MD_IMG_RE.finditer(text):
        src = m.group(1).strip()
        if src.startswith("http"):
            continue
        if not src.startswith("/"):
            findings.append(
                Finding(
                    rel,
                    line_of(text, m.start()),
                    "error",
                    "IMG002",
                    f"markdown image path missing leading /: {src}",
                )
            )
    for m in FIGURE_SRC_RE.finditer(text):
        src = m.group(1).strip()
        if src.startswith("http"):
            continue
        if not src.startswith("/"):
            findings.append(
                Finding(
                    rel,
                    line_of(text, m.start()),
                    "error",
                    "IMG003",
                    f"figure shortcode src missing leading /: {src}",
                )
            )
    return findings


def check_footnotes(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(path)
    defs: dict[str, tuple[str, int]] = {}
    for m in FOOTNOTE_DEF_RE.finditer(text):
        defs[m.group(1)] = (m.group(2), line_of(text, m.start()))

    for key, (body, ln) in defs.items():
        urls = URL_RE.findall(body)
        if not urls:
            findings.append(
                Finding(
                    rel,
                    ln,
                    "error",
                    "CITE001",
                    f"footnote [^{key}] has no URL: {body[:80]}",
                )
            )
            continue
        for u in urls:
            try:
                parsed = urlparse(u)
                if parsed.scheme not in {"http", "https"}:
                    findings.append(
                        Finding(
                            rel,
                            ln,
                            "error",
                            "CITE002",
                            f"footnote [^{key}] non-http URL: {u}",
                        )
                    )
                if parsed.netloc in WARN_DOMAINS_SUSPICIOUS:
                    findings.append(
                        Finding(
                            rel,
                            ln,
                            "warning",
                            "CITE003",
                            f"suspicious domain in [^{key}]: {parsed.netloc}",
                        )
                    )
                if "pubmed.ncbi.nlm.nih.gov" in parsed.netloc:
                    pmid_match = re.search(r"/(\d{6,})/", parsed.path)
                    if pmid_match:
                        pmid = int(pmid_match.group(1))
                        if pmid > 99_999_999:
                            findings.append(
                                Finding(
                                    rel,
                                    ln,
                                    "warning",
                                    "CITE004",
                                    f"suspicious PubMed ID {pmid} in [^{key}]",
                                )
                            )
            except ValueError:
                findings.append(
                    Finding(
                        rel,
                        ln,
                        "error",
                        "CITE005",
                        f"unparseable URL in [^{key}]: {u}",
                    )
                )

    refs = set(FOOTNOTE_REF_RE.findall(text))
    refs -= set(defs.keys())
    for r in refs:
        findings.append(
            Finding(
                rel,
                None,
                "error",
                "CITE006",
                f"footnote ref [^{r}] used but never defined",
            )
        )

    unused = set(defs.keys()) - set(FOOTNOTE_REF_RE.findall(text))
    for u in unused:
        findings.append(
            Finding(rel, defs[u][1], "warning", "CITE007", f"unused footnote def [^{u}]")
        )
    return findings


def check_faq(path: Path, text: str, fields: dict) -> list[Finding]:
    findings: list[Finding] = []
    rel = str(path)
    categories = fields.get("categories", [])
    if isinstance(categories, str):
        categories = [categories]
    is_news_or_trend = any(c in NEWS_TREND_CATEGORIES for c in categories)
    has_faq = FAQ_OPEN_RE.search(text) and FAQ_CLOSE_RE.search(text)
    if is_news_or_trend and not has_faq:
        findings.append(
            Finding(
                rel,
                None,
                "error",
                "FAQ001",
                f"news/trend POST missing {{< faq >}} shortcode",
            )
        )
    if has_faq:
        open_pos = FAQ_OPEN_RE.search(text).start()
        close_pos = FAQ_CLOSE_RE.search(text).end()
        faq_block = text[open_pos:close_pos]
        items = FAQ_ITEM_RE.findall(faq_block)
        if len(items) < 3:
            findings.append(
                Finding(
                    rel,
                    line_of(text, open_pos),
                    "warning",
                    "FAQ002",
                    f"FAQ has only {len(items)} items, recommend ≥ 3",
                )
            )
    return findings


def check_unsourced_stats(path: Path, text: str) -> list[Finding]:
    """Detect bare percentages without nearby footnote ref."""
    findings: list[Finding] = []
    rel = str(path)
    body = _strip_frontmatter(text)
    body = _strip_code_blocks(body)
    for m in PCT_RE.finditer(body):
        pct = m.group(1).strip()
        try:
            num = float(pct.rstrip("%").replace("+", "").replace("-", "").strip())
        except ValueError:
            continue
        if num < 5 or num > 10000:
            pass
        window = body[max(0, m.start() - 80) : m.end() + 80]
        if FOOTNOTE_REF_RE.search(window):
            continue
        if "编辑团队" in window or "editorial" in window.lower():
            continue
        if "无原始数据" in window or "estimate" in window.lower():
            continue
        findings.append(
            Finding(
                rel,
                line_of(text, m.start() + (len(text) - len(body))),
                "warning",
                "STAT001",
                f"percentage '{pct}' without nearby footnote or editorial attribution",
            )
        )
    return findings


def check_named_metrics(path: Path, text: str) -> list[Finding]:
    """Detect 'XX 获赞 N' patterns without nearby URL or footnote."""
    findings: list[Finding] = []
    rel = str(path)
    body = _strip_frontmatter(text)
    body = _strip_code_blocks(body)
    for m in PERSON_NUM_LIKES_RE.finditer(body):
        window = body[max(0, m.start() - 120) : m.end() + 120]
        if URL_RE.search(window) or FOOTNOTE_REF_RE.search(window):
            continue
        findings.append(
            Finding(
                rel,
                line_of(text, m.start() + (len(text) - len(body))),
                "error",
                "CITE008",
                f"named-person-like-count without URL/footnote: ...{m.group(0)}...",
            )
        )
    return findings


def _strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end_match = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not end_match:
        return text
    return text[end_match.end() + 3 :]


def _strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def audit_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    fields, _, body_start = parse_frontmatter(text)
    findings: list[Finding] = []
    findings.extend(check_frontmatter(path, text, fields))
    findings.extend(check_images(path, text, body_start))
    findings.extend(check_footnotes(path, text))
    findings.extend(check_faq(path, text, fields))
    findings.extend(check_unsourced_stats(path, text))
    findings.extend(check_named_metrics(path, text))
    return findings


def is_post(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    parts = path.parts
    return "posts" in parts and path.name != "_index.md"


def iter_posts(root: Path) -> Iterable[Path]:
    for p in sorted(root.rglob("*.md")):
        if is_post(p):
            yield p


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit Hugo POST citation integrity")
    ap.add_argument("root", type=Path, help="content/ directory or subdirectory")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="warning",
        help="minimum severity to include in output",
    )
    args = ap.parse_args()

    sev_order = {"info": 0, "warning": 1, "error": 2}
    min_sev = sev_order[args.severity]

    all_findings: list[Finding] = []
    posts = list(iter_posts(args.root))
    for p in posts:
        all_findings.extend(audit_file(p))

    filtered = [f for f in all_findings if sev_order[f.severity] >= min_sev]

    errors = [f for f in filtered if f.severity == "error"]
    warnings = [f for f in filtered if f.severity == "warning"]

    status = "pass"
    exit_code = 0
    if errors:
        status = "error"
        exit_code = 2
    elif warnings:
        status = "warning"
        exit_code = 1

    if args.format == "json":
        report = {
            "status": status,
            "total_posts": len(posts),
            "errors": [asdict(f) for f in errors],
            "warnings": [asdict(f) for f in warnings],
            "counts": {
                "errors": len(errors),
                "warnings": len(warnings),
                "by_rule": _by_rule(filtered),
            },
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Posts: {len(posts)}  Errors: {len(errors)}  Warnings: {len(warnings)}")
        for f in filtered:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"  [{f.severity.upper()}][{f.rule_id}] {loc}  {f.message}")

    return exit_code


def _by_rule(findings: list[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.rule_id] = counts.get(f.rule_id, 0) + 1
    return counts


if __name__ == "__main__":
    sys.exit(main())
