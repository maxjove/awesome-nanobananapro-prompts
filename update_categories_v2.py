#!/usr/bin/env python3
import re
import json

# 读取 script.js
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义更详细的分类规则
category_rules = [
    # 角色类
    (r'(角色|character|GTA|迷你模型|人偶|公仔|手办)', 'character'),
    (r'(肖像|portrait|拼图肖像|人脸|人物)', 'portrait'),

    # 风格/艺术类
    (r'(刺绣|毛毡|粘土|像素|像素风|雕塑|马赛克|熔化|变异|霓虹|玻璃|陶瓷|金属|橡皮|气球|编织|折纸| Origami|剪纸|木头|木雕|木偶|锡玩具|浮雕)', 'art'),
    (r'(风格|style)', 'style'),
    (r'(捷克木偶|Czech)', 'art'),
    (r'(青花瓷)', 'art'),

    # 场景类
    (r'(场景|scene|微缩|树屋|洞穴|海洋|雨|街道|走廊|房间|森林|花园|城市|景观|环境)', 'scene'),

    # 海报/设计类
    (r'(海报|poster|品牌设计|设计指南|排版)', 'poster'),
    (r'(Logo|图标|icon|标志|徽标|badge)', 'logo'),
    (r'(UI|界面|按键|键盘|屏幕)', 'ui'),
    (r'(包装|packaging|纸折叠|纸玻璃|容器|盒子)', 'packaging'),

    # 产品/广告类
    (r'(产品|product|广告|brand|品牌)', 'product'),
    (r'(美妆|化妆|化妆品|cosmetic)', 'beauty'),
    (r'(食品|食物|美食|饮料)', 'food'),

    # 摄影类
    (r'(摄影|photography|照片|写实|镜头|棚拍|mugshot|证件照)', 'photography'),

    # 拼贴类
    (r'(拼贴|collage|九宫格|网格|联系表|组合)', 'collage'),

    # 游戏类
    (r'(游戏|game|GTA|塞尔达|我的世界|Minecraft|任天堂|Switch|游戏场景|军事训练)', 'game'),

    # 漫画/翻译类
    (r'(漫画|manga|翻译|上色|连环画|无声电影)', 'comic'),

    # 传统/文化类
    (r'(传统|traditional|古诗|书法|古风|古画|古籍|中国|戏曲|洞壁画|岩画|民族风)', 'traditional'),

    # 时尚类
    (r'(时尚|fashion|穿搭|服装|衣服|鞋|包包|珠宝|首饰)', 'fashion'),

    # 信息图/教育类
    (r'(信息图|infographic|卡片|图表|指南|MBTI)', 'infographic'),

    # 技术类
    (r'(技术|technical|工程|图纸|爆炸图|解剖|机械|齿轮)', 'technical'),

    # 编辑/修改类
    (r'(编辑|editing|修改|变换|转换|retexture|重制)', 'editing'),

    # 圣诞类
    (r'(圣诞|christmas|圣诞特辑|Xmas)', 'christmas'),

    # 3D/渲染类
    (r'(3D|渲染|render|voxel|等距|isometric)', '3d'),

    # 幻想/超现实类
    (r'(幻想|fantasy|超现实|surreal|梦��|魔法|魔法|神话|童话|奇幻|精灵|巨龙)', 'fantasy'),

    # 动物类
    (r'(动物|animal|宠物|pet|猫|狗|昆虫|鸟类|蜜蜂|熊猫)', 'animal'),

    # 文字/字体类
    (r'(文字|文本|font|字母|text|typography|标语|slogan)', 'text'),

    # 情绪/心理类
    (r'(情绪|心理|emotion|思想|思考|表情)', 'emotion'),

    # 粒子/特效类
    (r'(粒子|particle|特效|fx|发光|glow|bloom|火花|火焰)', 'effects'),
]

# 解析数据
cases = []
for line in content.split('\n'):
    if line.strip().startswith('{ id:'):
        # 提取 JSON 部分
        json_match = re.search(r'\{ id: (\d+), title: "([^"]+)", category: "([^"]+)", author: "([^"]+)", tags: (\[[^\]]+\]), img: "([^"]+)", prompt: "([^"]+)" \}', line)
        if json_match:
            case_id = int(json_match.group(1))
            title = json_match.group(2)
            old_category = json_match.group(3)
            author = json_match.group(4)
            tags = json_match.group(5)
            img = json_match.group(6)
            prompt = json_match.group(7)

            # 尝试重新分类
            new_category = 'general'
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

# 统计 general 的标题（用于分析）
general_titles = [case['title'] for case in cases if case['category'] == 'general']
print(f"\n剩余 {len(general_titles)} 个 general 案例")
print("部分标题示例:")
for title in general_titles[:20]:
    print(f"  - {title[:50]}...")
