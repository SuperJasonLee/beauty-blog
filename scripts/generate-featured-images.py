#!/usr/bin/env python3
"""Regenerate all featured images with proper Chinese font support.

Usage:
    python3 scripts/generate-featured-images.py [--all | --name NAME]

Requires: Pillow (pip3 install Pillow)

Font paths (macOS):
  - Chinese: /System/Library/Fonts/STHeiti Medium.ttc
  - Fallback: /Library/Fonts/Arial Unicode.ttf
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(BASE, "static", "images", "posts")
DEST = os.path.join(BASE, "static", "images")

W, H = 1200, 630

FONT_CN = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_EN = "/Library/Fonts/Arial Unicode.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(path, size, index=0)
        except Exception:
            return ImageFont.load_default()


def draw_bg(draw):
    for y in range(H):
        r = int(15 + (26 - 15) * y / H)
        g = int(15 + (26 - 15) * y / H)
        b = int(26 + (46 - 26) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    for x in range(0, W, 2):
        p = x / W
        draw.line([(x, 0), (x, 10)], fill=(int(255 - p * 40), int(107 - p * 40), int(107 - p * 20)))


def draw_glow(draw, img):
    for cx, cy, rad, alpha in [(W - 180, -80, 300, 30), (-100, H - 100, 250, 25), (W // 2, H // 2, 400, 10)]:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for r in range(rad, 0, -5):
            a = int(alpha * (1 - r / rad))
            od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 100, 100, a))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def draw_dots(draw):
    for i in range(30):
        x = (i * 137 + 50) % W
        y = (i * 89 + 30) % H
        r = 2 + (i % 3)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 200, 200, 80))


def draw_footer(draw, text="Beauty-Blog.cloud-ip.cc"):
    f = load_font(FONT_EN, 18)
    _, _, w, h = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - w) // 2, H - 40), text, fill=(120, 120, 140), font=f)


def draw_side_deco(draw):
    draw.line([(40, 180), (40, H - 100)], fill=(255, 107, 107, 60), width=3)


def make_image(title_lines, subtitle, tagline, lang, filepath):
    img = Image.new("RGB", (W, H), "#0f0f1a")
    draw = ImageDraw.Draw(img)
    draw_bg(draw)
    img = draw_glow(draw, img)
    draw = ImageDraw.Draw(img)
    draw_dots(draw)

    ft = load_font(FONT_CN if lang == "zh" else FONT_EN, 58)
    fs = load_font(FONT_CN if lang == "zh" else FONT_EN, 28)
    fg = load_font(FONT_CN if lang == "zh" else FONT_EN, 22)

    y = 100
    for line in title_lines:
        _, _, w, h = draw.textbbox((0, 0), line, font=ft)
        draw.text(((W - w) // 2 + 2, y + 2), line, fill=(0, 0, 0, 120), font=ft)
        draw.text(((W - w) // 2, y), line, fill="white", font=ft)
        y += h + 8

    y += 12
    _, _, w, h = draw.textbbox((0, 0), subtitle, font=fs)
    pad = 16
    draw.rounded_rectangle([(W - w) // 2 - pad, y - 4, (W + w) // 2 + pad, y + h + 4], radius=20, fill=(255, 107, 107, 40))
    draw.text(((W - w) // 2, y), subtitle, fill="#FF6B6B", font=fs)
    y += h + 20

    _, _, w, h = draw.textbbox((0, 0), tagline, font=fg)
    draw.text(((W - w) // 2, y), tagline, fill="#CCCCCC", font=fg)

    draw_side_deco(draw)
    draw_footer(draw)
    img.save(filepath, "PNG", optimize=True)
    print(f"  Generated: {os.path.basename(filepath)}")


SPECS = [
    # (title_lines, subtitle, tagline, lang, filename, subdir)
    (
        ["2026小红书医美", "趋势报告"],
        "基于小红书官方月报深度解析",
        "光子嫩肤 · 轮廓固定 · 黄金微针 · 馒化修复 · 轻医美",
        "zh", "xiaohongshu-trends-2026.png", "posts",
    ),
    (
        ["2026 Xiaohongshu", "Aesthetic Medicine", "Trends Report"],
        "Based on XHS official monthly data",
        "IPL · Facial Contouring · Gold Microneedling · Min. Invasive",
        "en", "en-xiaohongshu-trends-2026.png", "posts",
    ),
    (
        ["双眼皮手术", "术前必读指南"],
        "重睑术全解析 · 术前评估 · 恢复过程",
        "埋线法 · 切开法 · 术后护理 · 注意事项",
        "zh", "blepharoplasty-guide.png", "posts",
    ),
    (
        ["Blepharoplasty", "Essential Pre-op Guide"],
        "Complete guide to eyelid surgery",
        "Suture Method · Incision Method · Recovery · Care",
        "en", "en-blepharoplasty-guide.png", "posts",
    ),
    (
        ["鼻整形（隆鼻术）", "全解析"],
        "从假体选择到术后护理",
        "硅胶 · 膨体 · 自体软骨 · 术后护理要点",
        "zh", "rhinoplasty-guide.png", "posts",
    ),
    (
        ["Rhinoplasty", "The Complete Guide"],
        "From implant selection to recovery",
        "Silicone · ePTFE · Autologous Cartilage · Aftercare",
        "en", "en-rhinoplasty-guide.png", "posts",
    ),
    (
        ["注射美容：肉毒素与", "玻尿酸的区别与选择"],
        "两种最常见注射项目的全面对比",
        "除皱 · 填充 · 效果对比 · 安全注意事项",
        "zh", "injectable-guide.png", "posts",
    ),
    (
        ["5月小红书医美", "热搜榜 2026"],
        "最新热门项目TOP10全解析",
        "光子嫩肤 · 黄金微针 · 轮廓固定 · 馒化修复",
        "zh", "xiaohongshu-hot-may-2026.png", "posts",
    ),
    (
        ["Xiaohongshu's Hottest", "Aesthetic Procedures", "May 2026 TOP10"],
        "Real XHS data · April-May 2026",
        "IPL · Gold Microneedling · Contouring · Overfill Repair",
        "en", "en-xiaohongshu-hot-may-2026.png", "posts",
    ),
    (
        ["5月小红书医美", "实时热搜盘点"],
        "基于2026.5.25实时搜索数据",
        "黄金微针 · 热玛吉 · 超声炮 · 轮廓固定 · 馒化修复",
        "zh", "xiaohongshu-may-2026-live.png", "posts",
    ),
    (
        ["Xiaohongshu Live", "Hottest Aesthetic", "Procedures May 2026"],
        "Real-time XHS search data · May 25, 2026",
        "Gold Microneedling · Thermage · Contouring · Overfill Repair",
        "en", "en-xiaohongshu-may-2026-live.png", "posts",
    ),
    (
        ["Beauty-Blog"],
        "整形美容知识百科 | Aesthetic Medicine Knowledge Base",
        "AI + SEO friendly beauty content",
        "en", "site-feature.png", ".",
    ),
]


def main():
    want_all = "--all" in sys.argv
    want_name = None
    for a in sys.argv[1:]:
        if a.startswith("--name="):
            want_name = a.split("=", 1)[1]

    for tl, sub, tag, lang, fname, subdir in SPECS:
        if not want_all and not want_name:
            continue
        if want_name and want_name not in fname:
            continue
        if subdir == ".":
            dest = os.path.join(DEST, fname)
        else:
            dest = os.path.join(DEST, subdir, fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        make_image(tl, sub, tag, lang, dest)

    if not want_all and not want_name:
        print(__doc__)
        print("\nAvailable specs:")
        for _, _, _, _, fname, _ in SPECS:
            print(f"  --name={fname}")
        print("\n  --all  regenerate everything")


if __name__ == "__main__":
    main()
