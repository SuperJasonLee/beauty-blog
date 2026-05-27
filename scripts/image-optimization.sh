#!/bin/bash
# 图片优化脚本（使用macOS sips工具）
# 用法: ./scripts/image-optimization.sh <input_image> <output_image> <width> <height>

INPUT=$1
OUTPUT=$2
WIDTH=$3
HEIGHT=$4

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ] || [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    echo "用法: $0 <input_image> <output_image> <width> <height>"
    exit 1
fi

# 检查输入文件是否存在
if [ ! -f "$INPUT" ]; then
    echo "错误: 输入文件不存在: $INPUT"
    exit 1
fi

# 创建临时文件
TEMPFILE=$(mktemp /tmp/image-optimize.XXXXXX)

# 使用sips调整尺寸（保持宽高比，裁剪到目标尺寸）
# 首先调整到足够大的尺寸，然后裁剪
sips -z $HEIGHT $WIDTH "$INPUT" --out "$TEMPFILE" > /dev/null 2>&1

# 如果调整失败，尝试其他方法
if [ $? -ne 0 ]; then
    # 尝试只调整宽度
    sips --resampleWidth $WIDTH "$INPUT" --out "$TEMPFILE" > /dev/null 2>&1
fi

# 复制到输出文件
cp "$TEMPFILE" "$OUTPUT"

# 清理临时文件
rm -f "$TEMPFILE"

# 检查文件大小，如果大于500KB则压缩
FILESIZE=$(stat -f%z "$OUTPUT")
if [ "$FILESIZE" -gt 512000 ]; then
    # 使用sips降低质量
    sips -s formatOptions 85 "$OUTPUT" --out "$OUTPUT" > /dev/null 2>&1
    echo "图片已压缩至85%质量"
fi

echo "图片已处理: $OUTPUT ($(stat -f%z "$OUTPUT") bytes)"