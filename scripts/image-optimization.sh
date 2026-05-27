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
