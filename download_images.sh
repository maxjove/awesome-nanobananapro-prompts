#!/bin/bash

# 下载并重命名图片的脚本
# 从 script.js 提取 id 和腾讯云图片 URL 的映射

OUTPUT_DIR="./downloaded_images"
mkdir -p "$OUTPUT_DIR"

echo "正在提取图片链接..."

# 从 git diff 中提取原始的腾讯云链接和对应的 id
git diff script.js | grep -E '^\-.*id: [0-9]+' | \
  sed -E 's/.*id: ([0-9]+).*img: "([^"]+)".*/\1|\2/' | \
  sort -t '|' -k1 -n > /tmp/image_mapping.txt

echo "找到 $(wc -l < /tmp/image_mapping.txt) 张图片"
echo "开始下载..."

# 下载并重命名图片
while IFS='|' read -r id url; do
  # 获取文件扩展名
  ext="${url##*.}"
  output_file="$OUTPUT_DIR/${id}.${ext}"

  echo "下载 ID $id -> $output_file"
  curl -s -o "$output_file" "$url"

  if [ $? -eq 0 ]; then
    echo "  ✓ 成功"
  else
    echo "  ✗ 失败"
  fi
done < /tmp/image_mapping.txt

echo ""
echo "下载完成！图片保存在: $OUTPUT_DIR"
echo ""
echo "现在你可以将这些图片复制到 gpt4o-image-prompts-master/images/ ��录"
