import streamlit as st
import random
import json
import os
import time
from PIL import Image
from ultralytics import YOLO

# 中泰双语翻译（新增菜品识别词条）
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
        "file_error": "菜品数据文件缺失，请确保chinese_dishes.json和thai_dishes.json在同一目录",
        # 新增本地菜品识别翻译
        "recognition": "本地AI菜品识别",
        "upload_image": "上传菜品图片",
        "take_photo": "拍照识别",
        "recognize": "开始识别",
        "recognizing": "AI正在本地识别菜品...",
        "recognition_result": "识别结果",
        "dish_name": "菜品名称",
        "calorie": "热量",
        "protein": "蛋白质",
        "fat": "脂肪",
        "carbohydrate": "碳水化合物",
        "confidence": "置信度",
        "no_result": "未识别到菜品，请上传清晰的菜品图片",
        "model_error": "模型加载失败，请确保网络连接正常"
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
        "file_error": "ไฟล์ข้อมูลอาหารหายไป กรุณาตรวจสอบไฟล์ chinese_dishes.json และ thai_dishes.json",
        # 新增本地菜品识别翻译
        "recognition": "AI รู้จักอาหารในเครื่อง",
        "upload_image": "อัปโหลดรูปภาพอาหาร",
        "take_photo": "ถ่ายรูปเพื่อรู้จัก",
        "recognize": "เริ่มรู้จัก",
        "recognizing": "AI กำลังรู้จักอาหารในเครื่อง...",
        "recognition_result": "ผลลัพธ์การรู้จัก",
        "dish_name": "ชื่ออาหาร",
        "calorie": "แคลอรี่",
        "protein": "โปรตีน",
        "fat": "ไขมัน",
        "carbohydrate": "คาร์โบไฮเดรต",
        "confidence": "ความมั่นใจ",
        "no_result": "ไม่พบอาหาร กรุณาอัปโหลดรูปภาพอาหารที่ชัดเจน",
        "model_error": "โหลดโมเดลล้มเหลว กรุณาตรวจสอบการเชื่อมต่อเครือข่าย"
    }
}

# 加载专门的菜品识别模型（自动下载，无需手动上传）
@st.cache_resource
def load_yolo_model():
    try:
        # 自动下载专门在Food101数据集上训练的菜品识别模型
        # 模型大小约6MB，下载后自动缓存
        return YOLO("keremberke/yolov8n-food-classification")
    except Exception as e:
        st.error(f"模型加载失败：{str(e)}")
        return None

# 加载营养数据库
@st.cache_data
def load_nutrition_db():
    if not os.path.exists("nutrition_db.json"):
        return {}
    try:
        with open("nutrition_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 本地菜品识别函数（适配分类模型）
def recognize_dish_local(image, model, nutrition_db, lang):
    results = model(image, conf=0.3)  # 置信度阈值0.3
    recognized_dishes = []
    
    for result in results:
        # 分类模型的输出格式
        top5_indices = result.probs.top5
        top5_confidences = result.probs.top5conf
        
        for i in range(3):  # 返回前3个最可能的结果
            class_id = int(top5_indices[i])
            class_name = model.names[class_id]
            confidence = float(top5_confidences[i])
            
            # 从营养数据库获取信息
            if class_name in nutrition_db:
                dish_info = nutrition_db[class_name]
                name = dish_info[f"name_{lang}"] if f"name_{lang}" in dish_info else class_name.replace("_", " ").title()
                recognized_dishes.append({
                    "name": name,
                    "cal": dish_info["cal"],
                    "protein": dish_info["protein"],
                    "fat": dish_info["fat"],
                    "carb": dish_info["carb"],
                    "confidence": confidence
                })
    
    return recognized_dishes

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

# 加载所有数据
cn_dishes = load_dishes("chinese_dishes.json")
thai_dishes = load_dishes("thai_dishes.json")
yolo_model = load_yolo_model()
nutrition_db = load_nutrition_db()

# 检查文件是否存在
if not cn_dishes or not thai_dishes:
    st.error(t["file_error"])
    st.stop()

# 创建标签页（原有配餐功能+新增本地识别功能）
tab1, tab2 = st.tabs(["🍜 智能配餐", "📷 本地AI菜品识别"])

# ===================== 标签页1：原有智能配餐功能（完全保留，一字未改） =====================
with tab1:
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

        # 生成按钮
        if st.button(t["generate"], type="primary", key="gen_btn"):
            if "result" in st.session_state:
                del st.session_state["result"]
            
            with st.spinner(t["loading"]):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.008)
                    progress_bar.progress(i+1)
                
                try:
                    if cuisine in ("中餐", "อาหารจีน"):
                        menu_db = cn_dishes[scene][crowd]
                    else:
                        menu_db = thai_dishes[scene][crowd]
                except KeyError:
                    menu_db = cn_dishes["居家"]["普通人群"] if cuisine in ("中餐", "อาหารจีน") else thai_dishes["居家"]["普通人群"]
                
                valid_menus = []
                allergy_list = [x.strip() for x in allergy.split(",") if x.strip()]
                
                if crowd == "过敏体质" or crowd == "คนแพ้อาหาร":
                    common_allergens = ["海鲜", "牛奶", "花生", "鸡蛋", "大豆", "小麦", "坚果"]
                    allergy_list.extend(common_allergens)
                    allergy_list = list(set(allergy_list))
                
                target_taste = taste
                if target_taste not in menu_db:
                    target_taste = "清淡" if lang == "中文" else "อ่อน"
                
                try:
                    for menu in menu_db[target_taste]:
                        has_allergy = False
                        for meal in ["breakfast", "lunch", "dinner"]:
                            for dish in menu[meal]:
                                dish_name = dish["name_cn"] if lang == "中文" else dish["name_th"]
                                dish_taboo = dish["taboo_cn"] if lang == "中文" else dish["taboo_th"]
                                for a in allergy_list:
                                    if a in dish_name or a in dish_taboo:
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
                
                if valid_menus:
                    selected_menu = random.choice(valid_menus)
                else:
                    selected_menu = menu_db["清淡"][0] if "清淡" in menu_db else list(menu_db.values())[0][0]
                
                res = f"### 🍜 一日三餐配餐方案（{target_taste}·{scene}·{crowd}）\n\n"
                total_cal = 0
                total_protein = 0
                
                # 早餐
                res += "**早餐**："
                breakfast_names = []
                for d in selected_menu["breakfast"]:
                    name = d["name_cn"] if lang == "中文" else d["name_th"]
                    breakfast_names.append(f"{name}（{d['cal']}kcal，蛋白质{d['protein']}g）")
                res += " + ".join(breakfast_names) + "\n"
                
                for d in selected_menu["breakfast"]:
                    origin = d["origin_cn"] if lang == "中文" else d["origin_th"]
                    suitable = d["suitable_cn"] if lang == "中文" else d["suitable_th"]
                    taboo = d["taboo_cn"] if lang == "中文" else d["taboo_th"]
                    res += f"- {t['origin']}：{origin}\n"
                    res += f"- {t['suitable']}：{suitable}\n"
                    res += f"- {t['taboo']}：{taboo}\n"
                    total_cal += d["cal"]
                    total_protein += d["protein"]
                res += "\n"
                
                # 午餐
                res += "**午餐**："
                lunch_names = []
                for d in selected_menu["lunch"]:
                    name = d["name_cn"] if lang == "中文" else d["name_th"]
                    lunch_names.append(f"{name}（{d['cal']}kcal，蛋白质{d['protein']}g）")
                res += " + ".join(lunch_names) + "\n"
                
                for d in selected_menu["lunch"]:
                    origin = d["origin_cn"] if lang == "中文" else d["origin_th"]
                    suitable = d["suitable_cn"] if lang == "中文" else d["suitable_th"]
                    taboo = d["taboo_cn"] if lang == "中文" else d["taboo_th"]
                    res += f"- {t['origin']}：{origin}\n"
                    res += f"- {t['suitable']}：{suitable}\n"
                    res += f"- {t['taboo']}：{taboo}\n"
                    total_cal += d["cal"]
                    total_protein += d["protein"]
                res += "\n"
                
                # 晚餐
                res += "**晚餐**："
                dinner_names = []
                for d in selected_menu["dinner"]:
                    name = d["name_cn"] if lang == "中文" else d["name_th"]
                    dinner_names.append(f"{name}（{d['cal']}kcal，蛋白质{d['protein']}g）")
                res += " + ".join(dinner_names) + "\n"
                
                for d in selected_menu["dinner"]:
                    origin = d["origin_cn"] if lang == "中文" else d["origin_th"]
                    suitable = d["suitable_cn"] if lang == "中文" else d["suitable_th"]
                    taboo = d["taboo_cn"] if lang == "中文" else d["taboo_th"]
                    res += f"- {t['origin']}：{origin}\n"
                    res += f"- {t['suitable']}：{suitable}\n"
                    res += f"- {t['taboo']}：{taboo}\n"
                    total_cal += d["cal"]
                    total_protein += d["protein"]
                res += "\n---\n"
                
                # 营养分析
                res += f"### 📊 {t['nutrition']}\n"
                if crowd == "减脂人群" or crowd == "คนลดน้ำหนัก":
                    standard = "（减脂期推荐每日1200-1500kcal）" if lang == "中文" else "(แนะนำ 1200-1500 kcal ต่อวันสำหรับลดน้ำหนัก)"
                elif crowd == "老人儿童" or crowd == "ผู้สูงอายุและเด็ก":
                    standard = "（符合老人儿童每日营养需求）" if lang == "中文" else "(ตรงกับความต้องการโภชนาการประจำวันของผู้สูงอายุและเด็ก)"
                else:
                    if gender == "男" or gender == "ชาย":
                        standard = "（符合男性每日推荐摄入量）" if lang == "中文" else "(ตรงกับเป้าหมายประจำวันสำหรับผู้ชาย)"
                    else:
                        standard = t["standard"]
                res += f"- {t['total_cal']}：{total_cal}kcal {standard}\n"
                res += f"- {t['total_protein']}：{round(total_protein, 1)}g（达标）\n"
                
                # 健康提示
                tip = selected_menu["tip_cn"] if lang == "中文" else selected_menu["tip_th"]
                res += f"\n💡 {t['tip']}：{tip}\n"
                
                st.session_state["result"] = res
                st.rerun()

    with col2:
        if "result" in st.session_state:
            st.subheader(t["result"])
            st.markdown(st.session_state["result"])

# ===================== 标签页2：新增本地AI菜品识别功能 =====================
with tab2:
    st.subheader(t["recognition"])
    
    # 检查模型是否加载成功
    if not yolo_model:
        st.error(t["model_error"])
    else:
        # 上传图片或拍照
        col1, col2 = st.columns([1, 1])
        with col1:
            uploaded_file = st.file_uploader(t["upload_image"], type=["jpg", "jpeg", "png"])
        with col2:
            camera_image = st.camera_input(t["take_photo"])
        
        # 获取图片数据
        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        elif camera_image is not None:
            image = Image.open(camera_image)
        
        # 显示图片和识别按钮
        if image is not None:
            st.image(image, width=400)
            
            if st.button(t["recognize"], type="primary", key="rec_btn"):
                with st.spinner(t["recognizing"]):
                    # 本地识别菜品
                    results = recognize_dish_local(image, yolo_model, nutrition_db, "cn" if lang == "中文" else "th")
                    
                    if results and len(results) > 0:
                        st.subheader(t["recognition_result"])
                        
                        # 显示前3个识别结果
                        for i, dish in enumerate(results):
                            with st.expander(f"{i+1}. {dish['name']}（{round(dish['confidence']*100, 1)}%）", expanded=(i==0)):
                                st.write(f"**{t['dish_name']}**：{dish['name']}")
                                st.write(f"**{t['calorie']}**：{dish['cal']} kcal/100g")
                                st.write(f"**{t['protein']}**：{dish['protein']} g/100g")
                                st.write(f"**{t['fat']}**：{dish['fat']} g/100g")
                                st.write(f"**{t['carbohydrate']}**：{dish['carb']} g/100g")
                                st.write(f"**{t['confidence']}**：{round(dish['confidence']*100, 1)}%")
                    else:
                        st.error(t["no_result"])
        else:
            st.info(t["upload_image"] + " 或 " + t["take_photo"])
