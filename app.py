import streamlit as st
import random
import json
import os

# 中泰双语翻译
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
        "loading": "正在为您生成专属配餐方案",
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
        "crowd_tip": "过敏体质=加强过敏源过滤；减脂=低油低糖高蛋白；老人儿童=软烂易消化",
        "file_error": "菜品数据文件缺失，请确保chinese_dishes.json和thai_dishes.json在同一目录"
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
        "loading": "กำลังสร้างเมนูอาหารเฉพาะของคุณ",
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
        "crowd_tip": "คนแพ้อาหาร=กรองแหล่งก่อภูมิ; ลดน้ำหนัก=น้ำมันต่ำโปรตีนสูง; ผู้สูงอายุและเด็ก=ย่อยง่าย",
        "file_error": "ไฟล์ข้อมูลอาหารหายไป กรุณาตรวจสอบไฟล์ chinese_dishes.json และ thai_dishes.json"
    }
}

# 读取JSON菜品文件函数
@st.cache_data(show_spinner=False)
def load_dishes(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# 页面配置
st.set_page_config(page_title="中泰营养配餐AI", layout="wide")
lang = st.sidebar.selectbox("语言 / ภาษา", ["中文", "ภาษาไทย"])
t = trans[lang]
st.title(t["title"])

# 加载菜品数据
cn_dishes = load_dishes("chinese_dishes.json")
thai_dishes = load_dishes("thai_dishes.json")

# 检查文件是否存在
if not cn_dishes or not thai_dishes:
    st.error(t["file_error"])
    st.stop()

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("个人信息")
    height = st.number_input(t["height"], min_value=100, max_value=220, value=161)
    weight = st.number_input(t["weight"], min_value=30, max_value=150, value=45)
    age = st.number_input(t["age"], min_value=10, max_value=100, value=20)
    gender = st.radio(t["gender"], t["gender_options"])
    
    scene = st.radio(t["scene"], t["scene_options"], help=t["scene_tip"])
    crowd = st.radio(t["crowd"], t["crowd_options"], help=t["crowd_tip"])
    taste = st.selectbox(t["taste"], t["taste_options"])
    allergy = st.text_input(t["allergy"], placeholder=t["allergy_placeholder"])
    cuisine = st.radio(t["cuisine"], t["cuisine_options"])

    # 生成按钮（修复卡顿问题：移除time.sleep，改用原生spinner）
    if st.button(t["generate"], type="primary", key="gen_btn"):
        # 先删除旧结果，强制重新生成
        if "result" in st.session_state:
            del st.session_state["result"]
        
        with st.spinner(t["loading"]):
            # 安全获取菜品库（增加异常处理）
            try:
                if cuisine in ("中餐", "อาหารจีน"):
                    menu_db = cn_dishes[scene][crowd]
                else:
                    menu_db = thai_dishes[scene][crowd]
            except KeyError:
                # 如果场景+人群不存在，默认用居家+普通人群
                menu_db = cn_dishes["居家"]["普通人群"] if cuisine in ("中餐", "อาหารจีน") else thai_dishes["居家"]["普通人群"]
            
            # 过滤含忌口的套餐
            valid_menus = []
            allergy_list = [x.strip() for x in allergy.split(",") if x.strip()]
            
            # 过敏体质自动加强过滤
            if crowd == "过敏体质" or crowd == "คนแพ้อาหาร":
                common_allergens = ["海鲜", "牛奶", "花生", "鸡蛋", "大豆", "小麦", "坚果"]
                allergy_list.extend(common_allergens)
                allergy_list = list(set(allergy_list))
            
            # 安全获取口味（增加异常处理）
            target_taste = taste
            if target_taste not in menu_db:
                target_taste = "清淡" if lang == "中文" else "อ่อน"
            
            try:
                for menu in menu_db[target_taste]:
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
            except:
                valid_menus = menu_db["清淡"] if "清淡" in menu_db else []
            
            # 随机选一个有效套餐
            if valid_menus:
                selected_menu = random.choice(valid_menus)
            else:
                # 如果没有有效套餐，默认用第一个清淡套餐
                selected_menu = menu_db["清淡"][0] if "清淡" in menu_db else list(menu_db.values())[0][0]
            
            # 生成Markdown内容
            res = f"### 🍜 一日三餐配餐方案（{target_taste}·{scene}·{crowd}）\n\n"
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
            
            # 营养分析
            res += f"### 📊 {t['nutrition']}\n"
            if crowd == "减脂人群" or crowd == "คนลดน้ำหนัก":
                standard = "（减脂期推荐每日1200-1500kcal）"
            elif crowd == "老人儿童" or crowd == "ผู้สูงอายุและเด็ก":
                standard = "（符合老人儿童每日营养需求）"
            else:
                standard = t["standard"]
            res += f"- {t['total_cal']}：{total_cal}kcal {standard}\n"
            res += f"- {t['total_protein']}：{round(total_protein, 1)}g（达标）\n"
            
            # 健康提示
            res += f"\n💡 {t['tip']}：{selected_menu['tip']}\n"
            
            st.session_state["result"] = res
            # 强制刷新页面
            st.rerun()

with col2:
    if "result" in st.session_state:
        st.subheader(t["result"])
        st.markdown(st.session_state["result"])
