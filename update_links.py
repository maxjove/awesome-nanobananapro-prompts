#!/usr/bin/env python3
import re
import os

# 读取图片文件扩展名映射
image_dir = "gpt4o-image-prompts-master/images"
extensions = {}

for f in os.listdir(image_dir):
    if re.match(r'^\d+\.(png|jpeg|jpg)$', f):
        id_num = int(f.split('.')[0])
        ext = f.split('.')[1]
        extensions[id_num] = ext

# 读取 script.js
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换图片链接
def replace_img(match):
    id_num = int(match.group(1))
    ext = extensions.get(id_num, 'png')
    new_link = f'https://raw.githubusercontent.com/xianyu110/awesome-nanobananapro-prompts/main/gpt4o-image-prompts-master/images/{id_num}.{ext}'
    # 保持原有的行，只替换 img 部分
    line = match.group(0)
    return re.sub(r'img: "[^"]+"', f'img: "{new_link}"', line)

# 使用更简单的正则替换每一行
lines = content.split('\n')
new_lines = []

for line in lines:
    # 匹配 id: X, ... img: "..." 的行
    match = re.search(r'id: (\d+)', line)
    if match and 'img: "' in line:
        id_num = int(match.group(1))
        ext = extensions.get(id_num, 'png')
        new_link = f'https://raw.githubusercontent.com/xianyu110/awesome-nanobananapro-prompts/main/gpt4o-image-prompts-master/images/{id_num}.{ext}'
        line = re.sub(r'img: "[^"]+"', f'img: "{new_link}"', line)
    new_lines.append(line)

# 写回文件
with open('script.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f"已更新 {len(extensions)} 个图片链接")
