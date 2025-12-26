#!/bin/bash

# 下载 README 中的特殊格式图片

IMAGES=(
  "640-20251121225945521.jpeg"
  "640-20251121225950556.jpeg"
  "640-20251121225951800.png"
  "640-20251121230025209.jpeg"
  " 640-20251121230031902.png"
)

BASE_URL="https://maynor123-1301929665.cos.ap-guangzhou.myqcloud.com"
OUTPUT_DIR="gpt4o-image-prompts-master/images"

echo "下载 README 中的特殊图片..."

for img in "${IMAGES[@]}"; do
  url="${BASE_URL}/${img}"
  echo "下载: $img"
  curl -s -o "${OUTPUT_DIR}/${img}" "$url"

  if [ $? -eq 0 ]; then
    echo "  ✓ 成功"
  else
    echo "  ✗ 失败"
  fi
done

echo ""
echo "下载完成！"
