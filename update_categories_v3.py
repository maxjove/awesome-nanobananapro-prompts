#!/usr/bin/env python3
import re
import json

# 读取 script.js
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义更详细的分类规则（按优先级排序）
category_rules = [
    # 艺术/手工类
    (r'(刺绣|毛毡|毛线|编织|粘土|像素|像素风|雕塑|马赛克|熔化|变异|霓虹|玻璃|陶瓷|金属|橡皮|气球|折纸|Origami|剪纸|木头|木雕|木偶|锡玩具|浮雕|手工)', 'art'),

    # 角色类
    (r'(角色|character|GTA|迷你模型|人偶|公仔|手办)', 'character'),
    (r'(肖像|portrait|拼图肖像)', 'portrait'),

    # 风格类
    (r'(风格|style)', 'style'),
    (r'(捷克木偶|Czech)', 'art'),

    # 场景类
    (r'(场景|scene|微缩|树屋|洞穴|海洋|雨|街道|走廊|房间|森林|花园|城市|景观|环境|山脉|峡谷|洞穴|岛屿)', 'scene'),

    # 海报/设计类
    (r'(海报|poster|品牌设计|设计指南|排版)', 'poster'),
    (r'(Logo|图标|icon|标志|徽标|badge)', 'logo'),
    (r'(UI|界面|按键|键盘|屏幕)', 'ui'),
    (r'(包装|packaging|纸折叠|纸玻璃|容器|盒子|袋子)', 'packaging'),

    # 产品/广告/品牌类
    (r'(产品|product|广告|advert|brand|品牌|促销)', 'product'),
    (r'(美妆|化妆|化妆品|cosmetic)', 'beauty'),
    (r'(食品|食物|美食|饮料|bread|水果|蔬菜|糖果|chocolate|coffee|茶|酒)', 'food'),

    # 摄影类
    (r'(摄影|photography|照片|写实|镜头|棚拍|mugshot|证件照|cinematic|电影级)', 'photography'),

    # 拼贴类
    (r'(拼贴|collage|九宫格|网格|联系表|组合)', 'collage'),

    # 游戏类
    (r'(游戏|game|GTA|塞尔达|我的世界|Minecraft|任天堂|Switch|游戏场景|军事训练|士兵|指挥官|作战)', 'game'),

    # 漫画/动画类
    (r'(漫画|manga|翻译|上色|连环画|无声电影|cartoon|卡通|动画|anime)', 'comic'),

    # 传统/文化类
    (r'(传统|traditional|古诗|书法|古风|古画|古籍|中国|戏曲|洞壁画|岩画|民族风|复古|vintage|古典)', 'traditional'),

    # 时尚类
    (r'(时尚|fashion|穿搭|服装|衣服|鞋|包包|珠宝|首饰|外套|夹克|裙子|裤子|帽子|眼镜|围巾|手套)', 'fashion'),

    # 信息图/教育类
    (r'(信息图|infographic|卡片|图表|指南|MBTI|数据|教学|科普)', 'infographic'),

    # 技术类
    (r'(技术|technical|工程|图纸|爆炸图|解剖|机械|齿轮|机器人|科技|futuristic|未来)', 'technical'),

    # 编辑/修改类
    (r'(编辑|editing|修改|变换|转换|retexture|重制|transform)', 'editing'),

    # 圣诞类
    (r'(圣诞|christmas|圣诞特辑|Xmas|snow|雪|snowman|圣诞树|驯鹿)', 'christmas'),

    # 3D/渲染类
    (r'(3D|渲染|render|voxel|等距|isometric)', '3d'),

    # 幻想/超现实类
    (r'(幻想|fantasy|超现实|surreal|梦境|梦境|魔法|魔法|神话|童话|奇幻|精灵|巨龙|龙|独角兽|女巫|wizard)', 'fantasy'),

    # 动物类
    (r'(动物|animal|宠物|pet|猫|dog|狗|昆虫|鸟类|蜜蜂|bear|熊|panda|熊猫|lion|狮子|tiger|老虎|elephant|象)', 'animal'),

    # 文字/字体类
    (r'(文字|文本|font|字母|text|typography|标语|slogan|标题|title|标志|text)', 'text'),

    # 情绪/心理类
    (r'(情绪|心理|emotion|思想|思考|表情|expression|feeling)', 'emotion'),

    # 粒子/特效/光效类
    (r'(粒子|particle|特效|fx|发光|glow|bloom|火花|火焰|fire|火|光|light|霓虹|neon|aurora|极光)', 'effects'),

    # 自然/风景类
    (r'(自然|nature|风景|landscape|山|mountain|海|sea|ocean|湖|lake|河|river|天空|sky|云|cloud|sun|sun|月|moon|星空|星星|雨|rain|雪|snow)', 'nature'),

    # 建筑/室内类
    (r'(建筑|architecture|室内|interior|房子|house|房间|room|building|楼|塔|桥梁|桥|城堡|castle|宫殿|palace)', 'architecture'),

    # 交通工具类
    (r'(车|car|汽车|摩托车|motorcycle|自行车|bicycle|船|boat|飞机|airplane|火车|train|地铁|subway|bus|公交)', 'vehicle'),

    # 运动类
    (r'(运动|sport|跑步|running|健身|gym|足球|football|篮球|basketball|网球|tennis)', 'sport'),

    # 音乐类
    (r'(音乐|music|乐器|instrument|吉他|guitar|钢琴|piano|鼓|drum|歌手|singer|乐队|band)', 'music'),

    # 书籍/文具类
    (r'(书|book|书籍|笔记本|notebook|笔|pen|纸|paper|铅笔|pencil|文具|stationery)', 'stationery'),

    # 植物/花卉类
    (r'(植物|plant|花|flower|树|tree|草|grass|叶子|leaf|叶子|花朵|bloom|花园|garden)', 'plant'),

    # 科技/AI类
    (r'(AI|机器人|robot|智能|smart|电脑|computer|手机|phone|app|应用|软件|software|网络|network|代码|code|编程|program)', 'tech'),

    # 抽象/概念类
    (r'(抽象|abstract|概念|concept|几何|geometric|形状|shape|形式|form|符号|symbol)', 'abstract'),

    # 微型/迷你类
    (r'(微型|miniature|mini|迷你|小巧|tiny|小人国|微缩模型)', 'miniature'),

    # 奇幻/魔法类
    (r'(魔法|magic|magical|enchanted|附魔|spell|咒语|witch|wizard巫师)', 'magic'),

    # 恐怖/惊悚类
    (r'(恐怖|horror|惊悚|thriller|ghost|鬼|zombie|僵尸|vampire|吸血鬼|skull|骷髅)', 'horror'),
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
if len(general_titles) > 0:
    print("部分标题示例:")
    for title in general_titles[:10]:
        print(f"  - {title[:60]}...")
