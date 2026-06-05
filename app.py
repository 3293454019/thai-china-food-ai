import streamlit as st
import random

# 中泰双语翻译（新增人群词条）
trans = {
    "中文": {
        "title": "中泰AI智能营养配餐与饮食科普系统",
        "height": "身高(cm)",
        "weight": "体重(kg)",
        "age": "年龄",
        "gender": "性别",
        "gender_options": ["男", "女"],
        "scene": "使用场景",
        "scene_options": ["居家", "出行"],
        "crowd": "人群类型",
        "crowd_options": ["普通人群", "过敏体质", "减脂人群", "老人儿童"],
        "taste": "口味偏好",
        "taste_options": ["清淡", "微辣", "酸辣", "重辣"],
        "allergy": "饮食忌口",
        "allergy_placeholder": "如：海鲜、牛奶、花生，多个用逗号分隔",
        "cuisine": "配餐菜系",
        "cuisine_options": ["中餐", "泰餐"],
        "generate": "一键生成配餐方案",
        "loading": "AI正在生成对应人群与场景的专属配餐方案...",
        "result": "生成结果",
        "nutrition": "营养分析",
        "total_cal": "总热量",
        "total_protein": "总蛋白质",
        "standard": "（符合每日推荐摄入量）",
        "origin": "起源",
        "suitable": "适宜",
        "taboo": "忌口",
        "tip": "健康提示",
        "scene_tip": "居家=可在家烹饪；出行=便携外卖/便利店可购",
        "crowd_tip": "过敏体质=加强过敏源过滤；减脂=低油低糖高蛋白；老人儿童=软烂易消化"
    },
    "ภาษาไทย": {
        "title": "ระบบ AI สร้างเมนูอาหารและวัฒนธรรมอาหารจีน-ไทย",
        "height": "ส่วนสูง (ซม.)",
        "weight": "น้ำหนัก (กก.)",
        "age": "อายุ",
        "gender": "เพศ",
        "gender_options": ["ชาย", "หญิง"],
        "scene": "สถานการณ์การใช้งาน",
        "scene_options": ["ที่บ้าน", "เดินทาง"],
        "crowd": "ประเภทผู้ใช้",
        "crowd_options": ["คนทั่วไป", "คนแพ้อาหาร", "คนลดน้ำหนัก", "ผู้สูงอายุและเด็ก"],
        "taste": "รสชาติที่ชอบ",
        "taste_options": ["อ่อน", "เผ็ดน้อย", "เผ็ดเปรี้ยว", "เผ็ดมาก"],
        "allergy": "อาหารที่แพ้",
        "allergy_placeholder": "เช่น: อาหารทะเล, นม, ถั่วลิสง, หลายอย่างคั่นด้วยจุลภาค",
        "cuisine": "ประเภทอาหาร",
        "cuisine_options": ["อาหารจีน", "อาหารไทย"],
        "generate": "สร้างเมนูอาหารทันที",
        "loading": "AI กำลังสร้างเมนูเฉพาะตามประเภทและสถานการณ์...",
        "result": "ผลลัพธ์",
        "nutrition": "การวิเคราะห์โภชนาการ",
        "total_cal": "แคลอรี่รวม",
        "total_protein": "โปรตีนรวม",
        "standard": "(ตรงกับเป้าหมายประจำวัน)",
        "origin": "ที่มา",
        "suitable": "เหมาะกับ",
        "taboo": "ห้ามกิน",
        "tip": "คำแนะนำสุขภาพ",
        "scene_tip": "ที่บ้าน=ทำได้ที่บ้าน; เดินทาง=พกพาสะดวก",
        "crowd_tip": "คนแพ้อาหาร=กรองแหล่งก่อภูมิ; ลดน้ำหนัก=น้ำมันต่ำโปรตีนสูง; ผู้สูงอายุและเด็ก=ย่อยง่าย"
    }
}

# ===================== 结构化菜品数据库（菜系-场景-人群-口味 四级分类） =====================
# 中餐菜品库（中文）
cn_dishes = {
    "居家": {
        "普通人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "玉米胡萝卜排骨汤+小笼包", "cal": 360, "protein": 15.9, "origin": "粤式靓汤+江南小吃", "suitable": "老少皆宜", "taboo": "痛风、小麦过敏慎食"}],
                    "lunch": [{"name": "扬州炒饭+番茄炒蛋", "cal": 532, "protein": 20.0, "origin": "淮扬菜经典", "suitable": "一般人群", "taboo": "鸡蛋过敏禁食"}],
                    "dinner": [{"name": "糖醋排骨+清炒时蔬", "cal": 370, "protein": 20.9, "origin": "苏式家常菜", "suitable": "食欲不振者", "taboo": "糖尿病、肥胖慎食"}],
                    "tip": "日常均衡饮食，建议搭配适量水果"
                }
            ],
            "微辣": [
                {
                    "breakfast": [{"name": "鲜肉小馄饨", "cal": 240, "protein": 8.1, "origin": "江浙传统早点", "suitable": "一般人群", "taboo": "小麦过敏慎食"}],
                    "lunch": [{"name": "鱼香肉丝+清炒油麦菜", "cal": 375, "protein": 24.3, "origin": "川式微辣经典", "suitable": "下饭首选", "taboo": "肠胃弱慎食"}],
                    "dinner": [{"name": "青椒肉片+冬瓜清汤", "cal": 295, "protein": 24.2, "origin": "家常微辣菜", "suitable": "一般人群", "taboo": "肠胃疾病慎食"}],
                    "tip": "微辣开胃，适量食用即可"
                }
            ]
        },
        "过敏体质": {
            "清淡": [
                {
                    "breakfast": [{"name": "小米粥+白煮蛋", "cal": 220, "protein": 10.5, "origin": "北方传统早餐", "suitable": "过敏体质、肠胃弱", "taboo": "鸡蛋过敏禁食"}],
                    "lunch": [{"name": "清蒸鸡胸肉+清炒土豆丝", "cal": 305, "protein": 33.0, "origin": "低敏家常菜", "suitable": "过敏体质", "taboo": "鸡肉过敏禁食"}],
                    "dinner": [{"name": "冬瓜丸子汤+清炒娃娃菜", "cal": 215, "protein": 8.6, "origin": "清淡汤品", "suitable": "所有人群", "taboo": "无特殊忌口"}],
                    "tip": "过敏体质请务必确认食材成分，避免交叉污染"
                }
            ],
            "微辣": [
                {
                    "breakfast": [{"name": "白粥+蒸饺", "cal": 250, "protein": 7.8, "origin": "清淡早点", "suitable": "轻度过敏体质", "taboo": "小麦过敏慎食"}],
                    "lunch": [{"name": "清炒里脊+手撕包菜", "cal": 320, "protein": 22.5, "origin": "低敏炒菜", "suitable": "过敏体质", "taboo": "猪肉过敏禁食"}],
                    "dinner": [{"name": "丝瓜豆腐汤+白米饭", "cal": 180, "protein": 7.0, "origin": "清淡汤饭", "suitable": "所有人群", "taboo": "大豆过敏慎食"}],
                    "tip": "避免食用加工食品，优先选择新鲜食材"
                }
            ]
        },
        "减脂人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "燕麦粥+水煮蛋", "cal": 180, "protein": 12.3, "origin": "减脂经典早餐", "suitable": "减脂、健身人群", "taboo": "鸡蛋过敏禁食"}],
                    "lunch": [{"name": "香煎鸡胸肉+西兰花+糙米饭", "cal": 350, "protein": 35.5, "origin": "高蛋白减脂餐", "suitable": "减脂人群", "taboo": "鸡肉过敏禁食"}],
                    "dinner": [{"name": "番茄豆腐汤+凉拌黄瓜", "cal": 120, "protein": 6.5, "origin": "低卡晚餐", "suitable": "减脂人群", "taboo": "大豆过敏慎食"}],
                    "tip": "每日热量控制在1200-1500kcal，配合30分钟有氧运动效果更佳"
                }
            ],
            "微辣": [
                {
                    "breakfast": [{"name": "全麦面包+无糖豆浆", "cal": 210, "protein": 10.8, "origin": "减脂便携早餐", "suitable": "减脂人群", "taboo": "小麦、大豆过敏慎食"}],
                    "lunch": [{"name": "水煮牛肉+清炒生菜", "cal": 320, "protein": 28.7, "origin": "高蛋白微辣餐", "suitable": "减脂人群", "taboo": "牛肉过敏禁食"}],
                    "dinner": [{"name": "冬瓜海带汤+玉米段", "cal": 95, "protein": 4.2, "origin": "低卡汤品", "suitable": "减脂人群", "taboo": "海带过敏慎食"}],
                    "tip": "多喝水，少吃精制碳水，保证充足睡眠"
                }
            ]
        },
        "老人儿童": {
            "清淡": [
                {
                    "breakfast": [{"name": "山药瘦肉粥+蒸蛋羹", "cal": 295, "protein": 10.2, "origin": "养生早餐", "suitable": "老人、儿童", "taboo": "鸡蛋过敏禁食"}],
                    "lunch": [{"name": "清蒸鲈鱼+南瓜泥+软米饭", "cal": 320, "protein": 28.5, "origin": "易消化营养餐", "suitable": "老人、儿童", "taboo": "鱼类过敏禁食"}],
                    "dinner": [{"name": "蔬菜豆腐羹+小米粥", "cal": 185, "protein": 7.8, "origin": "软烂晚餐", "suitable": "老人、儿童", "taboo": "大豆过敏慎食"}],
                    "tip": "食物切小块煮软烂，细嚼慢咽，避免呛咳"
                }
            ],
            "微辣": [
                {
                    "breakfast": [{"name": "南瓜粥+小包子", "cal": 230, "protein": 6.5, "origin": "温和早餐", "suitable": "能吃微辣的儿童", "taboo": "小麦过敏慎食"}],
                    "lunch": [{"name": "番茄炖牛腩+软米饭", "cal": 380, "protein": 25.3, "origin": "营养炖菜", "suitable": "老人、儿童", "taboo": "牛肉过敏禁食"}],
                    "dinner": [{"name": "鸡蛋羹+青菜粥", "cal": 160, "protein": 8.2, "origin": "清淡晚餐", "suitable": "老人、儿童", "taboo": "鸡蛋过敏禁食"}],
                    "tip": "儿童避免过辣，老人注意控制盐分摄入"
                }
            ]
        }
    },
    "出行": {
        "普通人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "全麦三明治+纯牛奶", "cal": 320, "protein": 12.5, "origin": "西式便携早餐", "suitable": "上班族、学生", "taboo": "小麦、牛奶过敏慎食"}],
                    "lunch": [{"name": "鸡肉饭团+原味酸奶", "cal": 460, "protein": 18.4, "origin": "日式便携主食", "suitable": "出行人群", "taboo": "鸡肉、牛奶过敏慎食"}],
                    "dinner": [{"name": "番茄鸡蛋盖浇饭+苹果", "cal": 402, "protein": 13.0, "origin": "国民快餐", "suitable": "出行人群", "taboo": "鸡蛋过敏禁食"}],
                    "tip": "出行注意饮食卫生，避免生冷食物"
                }
            ]
        },
        "过敏体质": {
            "清淡": [
                {
                    "breakfast": [{"name": "白粥+茶叶蛋", "cal": 210, "protein": 10.3, "origin": "传统便携早餐", "suitable": "过敏体质", "taboo": "鸡蛋过敏禁食"}],
                    "lunch": [{"name": "叉烧饭+矿泉水", "cal": 420, "protein": 18.7, "origin": "粤式快餐", "suitable": "过敏体质", "taboo": "猪肉过敏慎食"}],
                    "dinner": [{"name": "白切鸡饭+香蕉", "cal": 390, "protein": 30.6, "origin": "清淡快餐", "suitable": "过敏体质", "taboo": "鸡肉过敏禁食"}],
                    "tip": "选择连锁餐厅，避免路边摊，主动告知服务员过敏情况"
                }
            ]
        },
        "减脂人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "无糖酸奶+燕麦片", "cal": 190, "protein": 11.2, "origin": "减脂便携早餐", "suitable": "减脂人群", "taboo": "牛奶过敏禁食"}],
                    "lunch": [{"name": "鸡胸肉沙拉+糙米饭", "cal": 320, "protein": 28.5, "origin": "减脂沙拉餐", "suitable": "减脂人群", "taboo": "鸡肉过敏禁食"}],
                    "dinner": [{"name": "蔬菜卷+无糖豆浆", "cal": 210, "protein": 9.8, "origin": "低卡便携餐", "suitable": "减脂人群", "taboo": "大豆过敏慎食"}],
                    "tip": "避免奶茶、油炸食品，选择无糖饮品"
                }
            ]
        },
        "老人儿童": {
            "清淡": [
                {
                    "breakfast": [{"name": "牛奶+蒸蛋糕", "cal": 250, "protein": 7.8, "origin": "温和早餐", "suitable": "老人、儿童", "taboo": "牛奶、小麦过敏慎食"}],
                    "lunch": [{"name": "儿童套餐（蒸蛋+米饭+青菜）", "cal": 320, "protein": 12.5, "origin": "儿童专属餐", "suitable": "儿童", "taboo": "鸡蛋过敏禁食"}],
                    "dinner": [{"name": "粥品+小包子", "cal": 280, "protein": 6.2, "origin": "易消化晚餐", "suitable": "老人、儿童", "taboo": "小麦过敏慎食"}],
                    "tip": "出行携带保温杯，避免吃太烫或太冰的食物"
                }
            ]
        }
    }
}

# 泰餐菜品库（中文，分场景-人群-口味）
thai_cn_dishes = {
    "居家": {
        "普通人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "椰浆糯米饭+水煮蛋", "cal": 320, "protein": 7.8, "origin": "泰国南部传统早餐", "suitable": "一般人群", "taboo": "椰子过敏慎食"}],
                    "lunch": [{"name": "椰汁嫩鸡汤+清炒空心菜", "cal": 380, "protein": 23.0, "origin": "泰国中部经典汤品", "suitable": "体质虚弱者", "taboo": "椰子过敏禁食"}],
                    "dinner": [{"name": "香茅蒸鸡+糙米饭", "cal": 390, "protein": 29.0, "origin": "泰式蒸菜", "suitable": "一般人群", "taboo": "鸡肉过敏禁食"}],
                    "tip": "泰式椰浆菜品热量较高，适量食用"
                }
            ]
        },
        "减脂人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "泰式南瓜粥", "cal": 210, "protein": 4.2, "origin": "泰式养生粥", "suitable": "减脂人群", "taboo": "无特殊忌口"}],
                    "lunch": [{"name": "白煮鸡胸+泰式杂蔬沙拉", "cal": 255, "protein": 33.8, "origin": "低卡泰餐", "suitable": "减脂人群", "taboo": "鸡肉过敏禁食"}],
                    "dinner": [{"name": "山药鸡汤+糙米", "cal": 230, "protein": 11.0, "origin": "泰式养生汤", "suitable": "减脂人群", "taboo": "鸡肉过敏禁食"}],
                    "tip": "避免椰浆、油炸泰式小吃，选择清蒸、水煮菜品"
                }
            ]
        }
    },
    "出行": {
        "普通人群": {
            "清淡": [
                {
                    "breakfast": [{"name": "泰式香蕉煎饼", "cal": 280, "protein": 4.2, "origin": "泰国街头小吃", "suitable": "年轻人", "taboo": "香蕉过敏慎食"}],
                    "lunch": [{"name": "鸡肉盖浇饭+椰子水", "cal": 399, "protein": 22.7, "origin": "泰式快餐", "suitable": "出行人群", "taboo": "鸡肉、椰子过敏慎食"}],
                    "dinner": [{"name": "泰式炒河粉+芒果", "cal": 360, "protein": 11.5, "origin": "泰国国民美食", "suitable": "一般人群", "taboo": "大米、芒果过敏慎食"}],
                    "tip": "泰国街头小吃注意卫生，避免生食海鲜"
                }
            ]
        }
    }
}

# 页面配置
st.set_page_config(page_title="中泰营养配餐AI", layout="wide")
lang = st.sidebar.selectbox("语言 / ภาษา", ["中文", "ภาษาไทย"])
t = trans[lang]
st.title(t["title"])

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("个人信息")
    height = st.number_input(t["height"], min_value=100, max_value=220, value=161)
    weight = st.number_input(t["weight"], min_value=30, max_value=150, value=45)
    age = st.number_input(t["age"], min_value=10, max_value=100, value=20)
    gender = st.radio(t["gender"], t["gender_options"])
    
    # 场景选择
    scene = st.radio(t["scene"], t["scene_options"], help=t["scene_tip"])
    
    # 新增：人群类型选择
    crowd = st.radio(t["crowd"], t["crowd_options"], help=t["crowd_tip"])
    
    taste = st.selectbox(t["taste"], t["taste_options"])
    allergy = st.text_input(t["allergy"], placeholder=t["allergy_placeholder"])
    cuisine = st.radio(t["cuisine"], t["cuisine_options"])

    if st.button(t["generate"], type="primary", key="gen_btn"):
        if "result" in st.session_state:
            del st.session_state["result"]
        with st.spinner(t["loading"]):
            # 选择对应菜品库（菜系→场景→人群→口味）
            if cuisine in ("中餐", "อาหารจีน"):
                menu_db = cn_dishes[scene][crowd]
            else:
                menu_db = thai_cn_dishes[scene][crowd]
            
            # 过滤含忌口的套餐
            valid_menus = []
            allergy_list = [x.strip() for x in allergy.split(",") if x.strip()]
            # 过敏体质自动加强过滤常见过敏源
            if crowd == "过敏体质" or crowd == "คนแพ้อาหาร":
                common_allergens = ["海鲜", "牛奶", "花生", "鸡蛋", "大豆", "小麦", "坚果"]
                allergy_list.extend(common_allergens)
                allergy_list = list(set(allergy_list))  # 去重
            
            for menu in menu_db.get(taste, menu_db["清淡"]):  # 无对应口味默认用清淡
                has_allergy = False
                for meal in ["breakfast", "lunch", "dinner"]:
                    for dish in menu[meal]:
                        for a in allergy_list:
                            if a in dish["name"] or a in dish["taboo"]:
                                has_allergy = True
                                break
                        if has_allergy:
                            break
                    if has_allergy:
                        break
                if not has_allergy:
                    valid_menus.append(menu)
            
            # 随机选一个有效套餐
            selected_menu = random.choice(valid_menus) if valid_menus else random.choice(menu_db["清淡"])
            
            # 生成Markdown内容（标题带场景+人群）
            res = f"### 🍜 一日三餐配餐方案（{t['taste_options'][t['taste_options'].index(taste)]}·{scene}·{crowd}）\n\n"
            total_cal = 0
            total_protein = 0
            
            # 早餐
            res += "**早餐**："
            breakfast_names = [f"{d['name']}（{d['cal']}kcal，蛋白质{d['protein']}g）" for d in selected_menu["breakfast"]]
            res += " + ".join(breakfast_names) + "\n"
            for d in selected_menu["breakfast"]:
                res += f"- {t['origin']}：{d['origin']}\n"
                res += f"- {t['suitable']}：{d['suitable']}\n"
                res += f"- {t['taboo']}：{d['taboo']}\n"
                total_cal += d["cal"]
                total_protein += d["protein"]
            res += "\n"
            
            # 午餐
            res += "**午餐**："
            lunch_names = [f"{d['name']}（{d['cal']}kcal，蛋白质{d['protein']}g）" for d in selected_menu["lunch"]]
            res += " + ".join(lunch_names) + "\n"
            for d in selected_menu["lunch"]:
                res += f"- {t['origin']}：{d['origin']}\n"
                res += f"- {t['suitable']}：{d['suitable']}\n"
                res += f"- {t['taboo']}：{d['taboo']}\n"
                total_cal += d["cal"]
                total_protein += d["protein"]
            res += "\n"
            
            # 晚餐
            res += "**晚餐**："
            dinner_names = [f"{d['name']}（{d['cal']}kcal，蛋白质{d['protein']}g）" for d in selected_menu["dinner"]]
            res += " + ".join(dinner_names) + "\n"
            for d in selected_menu["dinner"]:
                res += f"- {t['origin']}：{d['origin']}\n"
                res += f"- {t['suitable']}：{d['suitable']}\n"
                res += f"- {t['taboo']}：{d['taboo']}\n"
                total_cal += d["cal"]
                total_protein += d["protein"]
            res += "\n---\n"
            
            # 营养分析（根据人群动态调整标准）
            res += f"### 📊 {t['nutrition']}\n"
            if crowd == "减脂人群" or crowd == "คนลดน้ำหนัก":
                standard = "（减脂期推荐每日1200-1500kcal）"
            elif crowd == "老人儿童" or crowd == "ผู้สูงอายุและเด็ก":
                standard = "（符合老人儿童每日营养需求）"
            else:
                standard = t["standard"]
            res += f"- {t['total_cal']}：{total_cal}kcal {standard}\n"
            res += f"- {t['total_protein']}：{round(total_protein, 1)}g（达标）\n"
            
            # 专属健康提示
            res += f"\n💡 {t['tip']}：{selected_menu['tip']}\n"
            
            st.session_state["result"] = res
            st.rerun()

with col2:
    if "result" in st.session_state:
        st.subheader(t["result"])
        st.markdown(st.session_state["result"])
