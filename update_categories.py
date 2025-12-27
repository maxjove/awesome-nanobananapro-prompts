#!/usr/bin/env python3
import re
import json

# 读取 script.js
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义分类规则
category_rules = [
    # 角色类
    (r'(角色|character|GTA|卡通人物|迷你模型|人偶|公仔|手办)', 'character'),
    (r'(肖像|portrait|拼图肖像)', 'portrait'),

    # 风格类
    (r'(风格|style|刺绣|毛毡|粘土|粘土|像素|像素风|立体模型|雕塑|马赛克|熔化|变异|霓虹|玻璃|陶瓷|金属|橡皮筋|气球)', 'style'),
    (r'(青花瓷|Iznik)', 'style'),

    # 场景类
    (r'(场景|scene|微缩|树屋|洞穴|海洋|雨|街道|走廊|房间|洞穴|环境)', 'scene'),

    # 设计类
    (r'(海报|poster|品牌设计|设计指南)', 'poster'),
    (r'(Logo|图标|icon|标志)', 'logo'),
    (r'(UI|界面|按键)', 'ui'),
    (r'(包装|packaging|纸折叠|纸玻璃|容器)', 'packaging'),

    # 产品类
    (r'(产品|product|广告|brand|品牌)', 'product'),
    (r'(美妆|化妆|化妆品)', 'beauty'),

    # 摄影类
    (r'(摄影|photography|照片|写实|镜头|棚拍)', 'photography'),

    # 拼贴类
    (r'(拼贴|collage|九宫格|网格|联系表)', 'collage'),

    # 游戏类
    (r'(游戏|game|GTA|塞尔达|我的世界|Minecraft|任天堂|Switch)', 'game'),

    # 漫画/翻译类
    (r'(漫画|manga|翻译|上色)', 'translation'),

    # 传统/文化类
    (r'(传统|traditional|古诗|书法|古风|古画|古籍|刺绣|中国|戏曲)', 'traditional'),

    # 时尚类
    (r'(时尚|fashion|穿搭|服装|衣服)', 'fashion'),

    # 信息图类
    (r'(信息图|infographic|卡片|图表)', 'infographic'),

    # 技术类
    (r'(技术|technical|工程|图纸|爆炸图)', 'technical'),

    # 编辑类
    (r'(编辑|editing|修改|变换)', 'editing'),

    # 圣诞类
    (r'(圣诞|christmas|圣诞特辑)', 'christmas'),

    # 3D类
    (r'(3D|渲染|render)', '3d'),
]

# 解析 JSON 数据
cases = []
for line in content.split('\n'):
    if line.strip().startswith('{ id:'):
        # 解析每个案例
        case_match = re.search(r'\{ id: (\d+), title: "([^"]+)", category: "([^"]+)", author: "([^"]+)", tags: (\[[^\]]+\]), img: "([^"]+)", prompt: "([^"]+)" \}', line)
        if case_match:
            case_id = int(case_match.group(1))
            title = case_match.group(2)
            category = case_match.group(3)
            author = case_match.group(4)
            tags = case_match.group(5)
            img = case_match.group(6)
            prompt = case_match.group(7)

            # 尝试重新分类
            new_category = category
            for pattern, cat in category_rules:
                if re.search(pattern, title, re.IGNORECASE):
                    new_category = cat
                    break

            cases.append({
                'id': case_id,
                'title': title,
                'category': new_category,
                'author': author,
                'tags': tags,
                'img': img,
                'prompt': prompt
            })

print(f"处理了 {len(cases)} 个案例")

# 生成新的 script.js
js_content = "// 所有案例数据\nconst casesData = [\n"

for case in cases:
    js_content += f"    {{ id: {case['id']}, title: \"{case['title']}\", category: \"{case['category']}\", author: \"{case['author']}\", tags: {case['tags']}, img: \"{case['img']}\", prompt: \"{case['prompt']}\" }},\n"

js_content += "];\n"

# 写入文件
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# 统计分类
category_count = {}
for case in cases:
    cat = case['category']
    category_count[cat] = category_count.get(cat, 0) + 1

print("\n分类统计:")
for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count}")
