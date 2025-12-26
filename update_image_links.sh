#!/bin/bash

# 更新 script.js 中的图片链接为按 id 命名

# 备份原文件
cp script.js script.js.bak

# 使用 perl 替换（因为需要更复杂的正则）
perl -i -pe 's/id: (\d+).*?img: "https://raw\.githubusercontent\.com/xianyu110/awesome-nanobananapro-prompts/main/gpt4o-image-prompts-master/images/[^"]+"/"id: $1" . $& =~ s/img: "[^"]+"/" . get_extension($1) . "/ge' script.js

echo "图片链接已更新"
