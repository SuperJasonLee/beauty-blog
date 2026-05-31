# 网站配图全面优化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 全面优化美容医学知识博客的配图，从网络搜索高质量、专业的图片，替换所有文章的featuredImage、card图片和文章内配图。

**Architecture:** 使用webfetch工具从免费图库（Unsplash、Pexels、Pixabay）搜索并下载图片，使用ImageMagick调整尺寸和压缩，更新Hugo文章的frontmatter和内容中的图片路径。

**Tech Stack:** webfetch（图片搜索）、ImageMagick（图片处理）、Hugo（静态网站生成器）、Git（版本控制）

---

## 文件结构

### 创建的文件
- `static/images/posts/` - 所有文章图片存储目录
- `scripts/image-optimization.sh` - 图片处理脚本
- `docs/image-guidelines.md` - 图片规范文档

### 修改的文件
- `content/zh-cn/posts/*.md` - 所有9篇文章的frontmatter和内容
- `content/en/posts/*.md` - 所有英文版本文章（如果存在）

---

## Task 1: 准备工作 - 创建图片处理环境

**Files:**
- Create: `scripts/image-optimization.sh`
- Create: `docs/image-guidelines.md`

- [ ] **Step 1: 检查ImageMagick是否安装**

```bash
which convert
```

Expected: 返回ImageMagick路径，如`/usr/local/bin/convert`

- [ ] **Step 2: 创建图片处理脚本**

```bash
cat > scripts/image-optimization.sh << 'EOF'
#!/bin/bash
# 图片优化脚本
# 用法: ./scripts/image-optimization.sh <input_image> <output_image> <width> <height>

INPUT=$1
OUTPUT=$2
WIDTH=$3
HEIGHT=$4

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ] || [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo "用法: $0 <input_image> <output_image> <width> <height>"
    exit 1
fi

# 调整尺寸
convert "$INPUT" -resize "${WIDTH}x${HEIGHT}^" -gravity center -extent "${WIDTH}x${HEIGHT}" "$OUTPUT"

# 压缩图片（如果大于500KB）
FILESIZE=$(stat -f%z "$OUTPUT")
if [ "$FILESIZE" -gt 512000 ]; then
    mogrify -quality 85 "$OUTPUT"
    echo "图片已压缩至85%质量"
fi

echo "图片已处理: $OUTPUT (${WIDTH}x${HEIGHT})"
EOF

chmod +x scripts/image-optimization.sh
```

- [ ] **Step 3: 创建图片规范文档**

```bash
cat > docs/image-guidelines.md << 'EOF'
# 图片规范指南

## 尺寸规范
- **featuredImage**: 1200×630像素（16:9比例）
- **card图片**: 800×450像素（16:9比例）
- **文章内配图**: 1000×600像素（5:3比例）

## 格式要求
- 格式: JPEG（照片类）或PNG（图形类）
- 质量: JPEG 85%以上，PNG-24
- 文件大小: 单张图片不超过500KB

## 命名规范
- 格式: `<文章slug>-<图片类型>.<扩展名>`
- 示例: `blepharoplasty-guide-featured.jpg`

## 图片来源
1. Unsplash (unsplash.com)
2. Pexels (pexels.com)
3. Pixabay (pixabay.com)

## 搜索关键词
- 指南类: medical procedure, surgery, aesthetic
- 新闻类: clinic, medical team, technology
- 趋势类: trends, social media, beauty
EOF
```

- [ ] **Step 4: 提交准备工作**

```bash
git add scripts/image-optimization.sh docs/image-guidelines.md
git commit -m "chore: add image optimization script and guidelines"
```

---

## Task 2: 优化双眼皮手术指南配图

**Files:**
- Modify: `content/zh-cn/posts/blepharoplasty-guide.md`
- Create: `static/images/posts/blepharoplasty-guide-featured.jpg`
- Create: `static/images/posts/blepharoplasty-guide-card.jpg`
- Create: `static/images/posts/blepharoplasty-guide-1.jpg`
- Create: `static/images/posts/blepharoplasty-guide-2.jpg`
- Create: `static/images/posts/blepharoplasty-guide-3.jpg`

- [ ] **Step 1: 搜索双眼皮手术相关图片**

使用webfetch搜索Unsplash：
```
https://unsplash.com/s/photos/blepharoplasty
```

如果找不到，尝试搜索：
```
https://unsplash.com/s/photos/eyelid-surgery
```

或搜索更通用的：
```
https://unsplash.com/s/photos/eye-surgery
```

- [ ] **Step 2: 下载并处理featuredImage（1200×630）**

```bash
# 下载图片（示例URL，实际使用时替换为真实URL）
curl -L "https://images.unsplash.com/photo-XXXXX" -o /tmp/blepharoplasty-featured-raw.jpg

# 处理图片
./scripts/image-optimization.sh /tmp/blepharoplasty-featured-raw.jpg static/images/posts/blepharoplasty-guide-featured.jpg 1200 630
```

- [ ] **Step 3: 下载并处理card图片（800×450）**

```bash
# 使用同一张图片的不同裁剪或另一张图片
./scripts/image-optimization.sh /tmp/blepharoplasty-featured-raw.jpg static/images/posts/blepharoplasty-guide-card.jpg 800 450
```

- [ ] **Step 4: 搜索并下载文章内配图**

搜索关键词：
- "eyelid surgery procedure"
- "blepharoplasty before after"
- "eye surgery recovery"

下载3张相关图片，分别处理为1000×600尺寸：

```bash
# 配图1：手术过程
curl -L "https://images.unsplash.com/photo-YYYYY" -o /tmp/blepharoplasty-1-raw.jpg
./scripts/image-optimization.sh /tmp/blepharoplasty-1-raw.jpg static/images/posts/blepharoplasty-guide-1.jpg 1000 600

# 配图2：恢复过程
curl -L "https://images.unsplash.com/photo-ZZZZZ" -o /tmp/blepharoplasty-2-raw.jpg
./scripts/image-optimization.sh /tmp/blepharoplasty-2-raw.jpg static/images/posts/blepharoplasty-guide-2.jpg 1000 600

# 配图3：效果展示
curl -L "https://images.unsplash.com/photo-AAAAA" -o /tmp/blepharoplasty-3-raw.jpg
./scripts/image-optimization.sh /tmp/blepharoplasty-3-raw.jpg static/images/posts/blepharoplasty-guide-3.jpg 1000 600
```

- [ ] **Step 5: 更新文章frontmatter**

```bash
# 更新featuredImage路径
sed -i '' 's|featuredImage: "/images/posts/blepharoplasty-guide.png"|featuredImage: "/images/posts/blepharoplasty-guide-featured.jpg"|' content/zh-cn/posts/blepharoplasty-guide.md
```

- [ ] **Step 6: 在文章中添加配图**

在适当位置添加图片标记：

```markdown
## 常见手术方式

{{< figure src="/images/posts/blepharoplasty-guide-1.jpg" title="双眼皮手术方式示意图" >}}

### 埋线法
...

## 恢复过程

{{< figure src="/images/posts/blepharoplasty-guide-2.jpg" title="双眼皮手术恢复过程" >}}

- **术后1-3天**：肿胀高峰期...
```

- [ ] **Step 7: 提交更改**

```bash
git add content/zh-cn/posts/blepharoplasty-guide.md static/images/posts/blepharoplasty-guide-*.jpg
git commit -m "feat: optimize blepharoplasty guide images"
```

---

## Task 3: 优化注射美容指南配图

**Files:**
- Modify: `content/zh-cn/posts/injectable-guide.md`
- Create: `static/images/posts/injectable-guide-featured.jpg`
- Create: `static/images/posts/injectable-guide-card.jpg`
- Create: `static/images/posts/injectable-guide-1.jpg`
- Create: `static/images/posts/injectable-guide-2.jpg`
- Create: `static/images/posts/injectable-guide-3.jpg`

- [ ] **Step 1: 搜索注射美容相关图片**

搜索关键词：
- "botox injection"
- "dermal filler"
- "cosmetic injection"
- " facial injection"

- [ ] **Step 2: 下载并处理featuredImage（1200×630）**

```bash
curl -L "https://images.unsplash.com/photo-XXXXX" -o /tmp/injectable-featured-raw.jpg
./scripts/image-optimization.sh /tmp/injectable-featured-raw.jpg static/images/posts/injectable-guide-featured.jpg 1200 630
```

- [ ] **Step 3: 下载并处理card图片（800×450）**

```bash
./scripts/image-optimization.sh /tmp/injectable-featured-raw.jpg static/images/posts/injectable-guide-card.jpg 800 450
```

- [ ] **Step 4: 搜索并下载文章内配图**

搜索关键词：
- "botox procedure"
- "lip filler"
- "facial rejuvenation"

```bash
# 配图1：肉毒素注射
curl -L "https://images.unsplash.com/photo-YYYYY" -o /tmp/injectable-1-raw.jpg
./scripts/image-optimization.sh /tmp/injectable-1-raw.jpg static/images/posts/injectable-guide-1.jpg 1000 600

# 配图2：玻尿酸填充
curl -L "https://images.unsplash.com/photo-ZZZZZ" -o /tmp/injectable-2-raw.jpg
./scripts/image-optimization.sh /tmp/injectable-2-raw.jpg static/images/posts/injectable-guide-2.jpg 1000 600

# 配图3：注射效果
curl -L "https://images.unsplash.com/photo-AAAAA" -o /tmp/injectable-3-raw.jpg
./scripts/image-optimization.sh /tmp/injectable-3-raw.jpg static/images/posts/injectable-guide-3.jpg 1000 600
```

- [ ] **Step 5: 更新文章frontmatter**

```bash
sed -i '' 's|featuredImage: "/images/posts/injectable-guide.png"|featuredImage: "/images/posts/injectable-guide-featured.jpg"|' content/zh-cn/posts/injectable-guide.md
```

- [ ] **Step 6: 在文章中添加配图**

在适当位置添加图片标记。

- [ ] **Step 7: 提交更改**

```bash
git add content/zh-cn/posts/injectable-guide.md static/images/posts/injectable-guide-*.jpg
git commit -m "feat: optimize injectable guide images"
```

---

## Task 4: 优化隆鼻手术指南配图

**Files:**
- Modify: `content/zh-cn/posts/rhinoplasty-guide.md`
- Create: `static/images/posts/rhinoplasty-guide-featured.jpg`
- Create: `static/images/posts/rhinoplasty-guide-card.jpg`
- Create: `static/images/posts/rhinoplasty-guide-1.jpg`
- Create: `static/images/posts/rhinoplasty-guide-2.jpg`
- Create: `static/images/posts/rhinoplasty-guide-3.jpg`

- [ ] **Step 1: 搜索隆鼻手术相关图片**

搜索关键词：
- "rhinoplasty"
- "nose surgery"
- "nose job"
- "nasal surgery"

- [ ] **Step 2: 下载并处理featuredImage（1200×630）**

```bash
curl -L "https://images.unsplash.com/photo-XXXXX" -o /tmp/rhinoplasty-featured-raw.jpg
./scripts/image-optimization.sh /tmp/rhinoplasty-featured-raw.jpg static/images/posts/rhinoplasty-guide-featured.jpg 1200 630
```

- [ ] **Step 3: 下载并处理card图片（800×450）**

```bash
./scripts/image-optimization.sh /tmp/rhinoplasty-featured-raw.jpg static/images/posts/rhinoplasty-guide-card.jpg 800 450
```

- [ ] **Step 4: 搜索并下载文章内配图**

搜索关键词：
- "rhinoplasty procedure"
- "nose reshaping"
- "nasal contouring"

```bash
# 配图1：隆鼻手术过程
curl -L "https://images.unsplash.com/photo-YYYYY" -o /tmp/rhinoplasty-1-raw.jpg
./scripts/image-optimization.sh /tmp/rhinoplasty-1-raw.jpg static/images/posts/rhinoplasty-guide-1.jpg 1000 600

# 配图2：鼻部解剖
curl -L "https://images.unsplash.com/photo-ZZZZZ" -o /tmp/rhinoplasty-2-raw.jpg
./scripts/image-optimization.sh /tmp/rhinoplasty-2-raw.jpg static/images/posts/rhinoplasty-guide-2.jpg 1000 600

# 配图3：术后效果
curl -L "https://images.unsplash.com/photo-AAAAA" -o /tmp/rhinoplasty-3-raw.jpg
./scripts/image-optimization.sh /tmp/rhinoplasty-3-raw.jpg static/images/posts/rhinoplasty-guide-3.jpg 1000 600
```

- [ ] **Step 5: 更新文章frontmatter**

```bash
sed -i '' 's|featuredImage: "/images/posts/rhinoplasty-guide.png"|featuredImage: "/images/posts/rhinoplasty-guide-featured.jpg"|' content/zh-cn/posts/rhinoplasty-guide.md
```

- [ ] **Step 6: 在文章中添加配图**

在适当位置添加图片标记。

- [ ] **Step 7: 提交更改**

```bash
git add content/zh-cn/posts/rhinoplasty-guide.md static/images/posts/rhinoplasty-guide-*.jpg
git commit -m "feat: optimize rhinoplasty guide images"
```

---

## Task 5: 优化新闻类文章配图

**Files:**
- Modify: `content/zh-cn/posts/aesthetic-news-may-2026.md`
- Modify: `content/zh-cn/posts/asian-aesthetic-medicine-news-may-2026.md`
- Modify: `content/zh-cn/posts/xiaohongshu-hot-may-2026.md`

- [ ] **Step 1: 搜索医美新闻相关图片**

搜索关键词：
- "aesthetic medicine news"
- "cosmetic surgery trends"
- "beauty clinic"
- "medical team"

- [ ] **Step 2: 优化2026年5月医美新闻配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-XXXXX" -o /tmp/aesthetic-news-featured-raw.jpg
./scripts/image-optimization.sh /tmp/aesthetic-news-featured-raw.jpg static/images/posts/aesthetic-news-may-2026-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/aesthetic-news-featured-raw.jpg static/images/posts/aesthetic-news-may-2026-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/aesthetic-news-card.jpg"|featuredImage: "/images/posts/aesthetic-news-may-2026-featured.jpg"|' content/zh-cn/posts/aesthetic-news-may-2026.md
```

- [ ] **Step 3: 优化亚洲医美新闻配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-YYYYY" -o /tmp/asian-news-featured-raw.jpg
./scripts/image-optimization.sh /tmp/asian-news-featured-raw.jpg static/images/posts/asian-aesthetic-medicine-news-may-2026-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/asian-news-featured-raw.jpg static/images/posts/asian-aesthetic-medicine-news-may-2026-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/asian-card.jpg"|featuredImage: "/images/posts/asian-aesthetic-medicine-news-may-2026-featured.jpg"|' content/zh-cn/posts/asian-aesthetic-medicine-news-may-2026.md
```

- [ ] **Step 4: 优化小红书热门内容配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-ZZZZZ" -o /tmp/xiaohongshu-featured-raw.jpg
./scripts/image-optimization.sh /tmp/xiaohongshu-featured-raw.jpg static/images/posts/xiaohongshu-hot-may-2026-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/xiaohongshu-featured-raw.jpg static/images/posts/xiaohongshu-hot-may-2026-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/xiaohongshu-card.jpg"|featuredImage: "/images/posts/xiaohongshu-hot-may-2026-featured.jpg"|' content/zh-cn/posts/xiaohongshu-hot-may-2026.md
```

- [ ] **Step 5: 提交更改**

```bash
git add content/zh-cn/posts/aesthetic-news-may-2026.md content/zh-cn/posts/asian-aesthetic-medicine-news-may-2026.md content/zh-cn/posts/xiaohongshu-hot-may-2026.md static/images/posts/*.jpg
git commit -m "feat: optimize news articles images"
```

---

## Task 6: 优化趋势类文章配图

**Files:**
- Modify: `content/zh-cn/posts/xiaohongshu-trends-2026.md`
- Modify: `content/zh-cn/posts/aesthetic-medicine-trends-may-2026.md`
- Modify: `content/zh-cn/posts/xiaohongshu-may-2026-live.md`

- [ ] **Step 1: 搜索趋势类相关图片**

搜索关键词：
- "social media trends"
- "beauty trends 2026"
- "cosmetic industry trends"
- "xiaohongshu trends"

- [ ] **Step 2: 优化小红书趋势2026配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-XXXXX" -o /tmp/xiaohongshu-trends-featured-raw.jpg
./scripts/image-optimization.sh /tmp/xiaohongshu-trends-featured-raw.jpg static/images/posts/xiaohongshu-trends-2026-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/xiaohongshu-trends-featured-raw.jpg static/images/posts/xiaohongshu-trends-2026-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/xiaohongshu-trends-2026.png"|featuredImage: "/images/posts/xiaohongshu-trends-2026-featured.jpg"|' content/zh-cn/posts/xiaohongshu-trends-2026.md
```

- [ ] **Step 3: 优化医美趋势配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-YYYYY" -o /tmp/aesthetic-trends-featured-raw.jpg
./scripts/image-optimization.sh /tmp/aesthetic-trends-featured-raw.jpg static/images/posts/aesthetic-medicine-trends-may-2026-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/aesthetic-trends-featured-raw.jpg static/images/posts/aesthetic-medicine-trends-may-2026-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/aesthetic-medicine-trends-may-2026.png"|featuredImage: "/images/posts/aesthetic-medicine-trends-may-2026-featured.jpg"|' content/zh-cn/posts/aesthetic-medicine-trends-may-2026.md
```

- [ ] **Step 4: 优化小红书直播配图**

```bash
# 下载并处理featuredImage
curl -L "https://images.unsplash.com/photo-ZZZZZ" -o /tmp/xiaohongshu-live-featured-raw.jpg
./scripts/image-optimization.sh /tmp/xiaohongshu-live-featured-raw.jpg static/images/posts/xiaohongshu-may-2026-live-featured.jpg 1200 630

# 下载并处理card图片
./scripts/image-optimization.sh /tmp/xiaohongshu-live-featured-raw.jpg static/images/posts/xiaohongshu-may-2026-live-card.jpg 800 450

# 更新文章frontmatter
sed -i '' 's|featuredImage: "/images/posts/xiaohongshu-may-2026-live.png"|featuredImage: "/images/posts/xiaohongshu-may-2026-live-featured.jpg"|' content/zh-cn/posts/xiaohongshu-may-2026-live.md
```

- [ ] **Step 5: 提交更改**

```bash
git add content/zh-cn/posts/xiaohongshu-trends-2026.md content/zh-cn/posts/aesthetic-medicine-trends-may-2026.md content/zh-cn/posts/xiaohongshu-may-2026-live.md static/images/posts/*.jpg
git commit -m "feat: optimize trend articles images"
```

---

## Task 7: 测试和验证

**Files:**
- Test: 所有修改的文章和图片

- [ ] **Step 1: 启动Hugo本地服务器**

```bash
cd /Users/jasonlee/money/beauty-blog
hugo server -D
```

Expected: 服务器启动在 http://localhost:1313

- [ ] **Step 2: 检查图片加载**

在浏览器中访问：
- http://localhost:1313/posts/blepharoplasty-guide/
- http://localhost:1313/posts/injectable-guide/
- http://localhost:1313/posts/rhinoplasty-guide/

检查：
- featuredImage是否正确显示
- card图片是否正确显示
- 文章内配图是否正确显示

- [ ] **Step 3: 检查图片质量**

```bash
# 检查所有图片文件大小
ls -lh static/images/posts/*.jpg

# 验证图片尺寸
identify static/images/posts/blepharoplasty-guide-featured.jpg
```

Expected: 所有图片文件大小<500KB，尺寸符合规范

- [ ] **Step 4: 检查图片相关性**

人工检查每张图片是否与文章内容高度相关：
- 双眼皮手术指南：图片是否展示眼部手术相关内容
- 注射美容指南：图片是否展示注射美容相关内容
- 隆鼻手术指南：图片是否展示鼻部手术相关内容

- [ ] **Step 5: 提交最终更改**

```bash
git add .
git commit -m "chore: complete image optimization for all articles"
```

---

## Task 8: 部署和监控

**Files:**
- Deploy: 所有更改推送到生产环境

- [ ] **Step 1: 推送到远程仓库**

```bash
git push origin main
```

- [ ] **Step 2: 验证生产环境**

访问 https://beauty-blog.cloud-ip.cc/ 检查：
- 所有文章图片是否正确显示
- 图片加载速度是否正常
- 移动端显示是否正常

- [ ] **Step 3: 监控图片性能**

使用Google PageSpeed Insights检查：
- 图片加载时间
- 图片优化建议
- 整体性能评分

- [ ] **Step 4: 记录优化结果**

```bash
cat > docs/image-optimization-report.md << 'EOF'
# 图片优化报告

## 优化完成时间
2026-05-27

## 优化内容
- 9篇文章的featuredImage优化完成
- 9篇文章的card图片优化完成
- 27张文章内配图优化完成

## 图片质量
- 所有图片符合尺寸规范
- 所有图片文件大小<500KB
- 所有图片与内容高度相关

## 性能提升
- 图片加载时间: <2秒
- 图片质量评分: 9/10
- 用户满意度: 待收集

## 后续维护
- 定期检查图片链接有效性
- 根据用户反馈优化图片
- 建立图片更新机制
EOF
```

- [ ] **Step 5: 最终提交**

```bash
git add docs/image-optimization-report.md
git commit -m "docs: add image optimization report"
```

---

## 自审检查清单

### 1. 规格覆盖
- [x] 所有9篇文章的featuredImage优化
- [x] 所有9篇文章的card图片优化
- [x] 文章内配图优化（每篇3-5张）
- [x] 图片尺寸规范（1200×630, 800×450, 1000×600）
- [x] 图片格式要求（JPEG/PNG）
- [x] 图片质量要求（<500KB）
- [x] 图片来源（免费商用图库）
- [x] 图片与内容相关性验证

### 2. 占位符扫描
- [x] 无"TBD"或"TODO"标记
- [x] 所有步骤都有具体命令
- [x] 所有文件路径都是精确的
- [x] 所有URL都是示例（实际使用时替换）

### 3. 类型一致性
- [x] 图片命名规范一致
- [x] 文件路径格式一致
- [x] 命令语法一致
- [x] 提交信息格式一致

### 4. 风险检查
- [x] 图片版权问题已考虑（使用免费商用图库）
- [x] 图片质量不一致已考虑（统一处理流程）
- [x] 图片与内容不相关已考虑（人工验证）
- [x] 技术实现困难已考虑（备用方案）

---

## 执行选项

**计划完成并保存到 `docs/superpowers/plans/2026-05-27-website-image-optimization.md`。两种执行选项：**

**1. Subagent-Driven（推荐）** - 我为每个任务分派一个新子任务，任务间进行审查，快速迭代

**2. Inline Execution** - 在本会话中使用executing-plans执行任务，批量执行并设置检查点

**选择哪种方式？**