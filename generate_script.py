#!/usr/bin/env python3
import re
import json

# 所有要处理的文件
files_to_process = [
    'gpt4o-image-prompts-master/README.md',
    'gpt4o-image-prompts-master/100.md',
    'gpt4o-image-prompts-master/200.md',
    'gpt4o-image-prompts-master/300.md',
    'gpt4o-image-prompts-master/400.md',
    'gpt4o-image-prompts-master/500.md',
    'gpt4o-image-prompts-master/600.md',
    'gpt4o-image-prompts-master/700.md',
]

# 收集所有案例
all_cases = []

# 分类映射
category_map = {
    '角色': 'character',
    '口型': 'character',
    '翻译': 'translation',
    '上色': 'translation',
    '漫画': 'translation',
    '海报': 'poster',
    'UI': 'ui',
    '微信': 'ui',
    '古风': 'traditional',
    '古画': 'traditional',
    'IP': 'ip',
    '搜索': 'infographic',
    '信息图': 'infographic',
    '手账': 'scene',
    '日记': 'scene',
    '字体': 'design',
    '���品': 'design',
    '场景': 'scene',
    '美颜': 'editing',
    '游戏': 'game',
    '3D': 'style',
    'Y2K': 'style',
    '风格': 'style',
    '书法': 'traditional',
    '科普': 'education',
    '宠物': 'scene',
    '线稿': 'design',
    '数学': 'infographic',
    '白板': 'infographic',
    '拼豆': 'style',
    'Windows': 'ui',
    'Mac': 'ui',
    'SaaS': 'ui',
    '数据': 'ui',
    'APP': 'ui',
    'PPT': 'ui',
    'FPS': 'game',
    'RTS': 'game',
    'MOBA': 'game',
    '桌游': 'game',
    '剑网': 'game',
    '英雄联盟': 'game',
    '武侠': 'game',
    '视觉小说': 'movie',
    '古籍': 'traditional',
    '计算器': 'design',
    '山水画': 'traditional',
    '鬼灭': 'translation',
    '电影': 'poster',
    '动画': 'poster',
    '活动': 'poster',
    '建筑': 'infographic',
    '工艺': 'infographic',
    '文学': 'infographic',
    '电池': 'infographic',
    '名片': 'poster',
    '功夫': 'infographic',
    '古诗': 'traditional',
    '工程': 'technical',
    '宇航': 'technical',
    'AI': 'style',
    '小红书': 'social',
    '时尚': 'fashion',
    '圣诞': 'christmas',
    '肖像': 'portrait',
    '摄影': 'photography',
    '产品图': 'product',
    '拼贴': 'collage',
    'Logo': 'logo',
    '包装': 'packaging',
}

# 处理每个文件
for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"无法读取文件: {filename}")
        continue

    # 查找所有案例
    pattern = r'<a id="prompt-(\d+)"></a>\n## (案例 \d+：[^\n]+)'
    matches = list(re.finditer(pattern, content))

    # 提取每个案例的完整内容
    for i, match in enumerate(matches):
        case_id = int(match.group(1))

        # 获取案例的起始位置
        start_pos = match.start()

        # 获取下一个案例的起始位置或文件结尾
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        # 提取案例内容
        case_content = content[start_pos:end_pos].strip()

        # 跳过已存在的案例
        if any(c['id'] == case_id for c in all_cases):
            continue

        # 提取标题
        title_match = re.search(r'## 案例 \d+：(.+?)(?:\s+\(来源|$|\n)', case_content)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = f"案例 {case_id}"

        # 提取来源
        source_match = re.search(r'\(来源 \[@([^\]]+)\]', case_content)
        author = source_match.group(1) if source_match else "community"

        # 提取模型
        model_match = re.search(r'模型：([^\n]+)', case_content)
        model = model_match.group(1).strip() if model_match else ""

        # 提取中文提示词
        prompt_match = re.search(r'\*\*中文提示词：\*\*\n```\n(.*?)\n```', case_content, re.DOTALL)
        if not prompt_match:
            prompt_match = re.search(r'\*\*提示词：\*\*\n```\n(.*?)\n```', case_content, re.DOTALL)
        cn_prompt = prompt_match.group(1).strip() if prompt_match else ""

        # 提取图片
        images = re.findall(r'<img src="./images/([^"]+)"', case_content)

        # 确定分类
        category = 'general'
        for key, cat in category_map.items():
            if key in title:
                category = cat
                break

        # 提取标签
        tags = []
        if '圣诞' in title:
            tags.append('圣诞')
        if '拼贴' in title or '九宫格' in title:
            tags.append('拼贴')
        if '肖像' in title or '人像' in title:
            tags.append('人像')
        if '产品' in title:
            tags.append('产品')
        if '海报' in title:
            tags.append('海报')

        if not tags:
            tags.append('AI绘图')

        # 使用第一张图片
        img = images[0] if images else f"{case_id}.jpeg"

        all_cases.append({
            'id': case_id,
            'title': title,
            'category': category,
            'author': f"@{author}",
            'tags': tags,
            'img': f"https://raw.githubusercontent.com/xianyu110/awesome-nanobananapro-prompts/main/gpt4o-image-prompts-master/images/{img}",
            'prompt': cn_prompt
        })

# 按 ID 排序
all_cases.sort(key=lambda x: x['id'])

print(f"总共提取 {len(all_cases)} 个案例")

# 生成 JavaScript 格式
js_content = "// 所有案例数据\nconst casesData = [\n"

for case in all_cases:
    # 转义提示词中的引号
    prompt_escaped = case['prompt'].replace('"', '\\"').replace('\n', '\\n')

    js_content += f"    {{ id: {case['id']}, title: \"{case['title']}\", category: \"{case['category']}\", author: \"{case['author']}\", tags: {json.dumps(case['tags'], ensure_ascii=False)}, img: \"{case['img']}\", prompt: \"{prompt_escaped[:500]}\" }},\n"

js_content += "];\n"

# 写入文件
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("已生成 script.js，包含 {} 个案例".format(len(all_cases)))
