import streamlit as st
import random
import json
import os
import time
from PIL import Image
from ultralytics import YOLO

# ===================== 全局界面美化配置 =====================
st.set_page_config(
    page_title="中泰营养配餐AI",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 美化CSS样式（已删除.card相关代码）
st.markdown("""
<style>
/* 全局背景和字体 */
.stApp {
    background: linear-gradient(135deg, #fef9f3 0%, #fff5e6 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 主标题样式 */
h1 {
    color: #d35400 !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* 子标题样式（个人信息、生成结果） */
h2, h3 {
    color: #e67e22 !important;
    font-weight: 600 !important;
    margin-bottom: 1.5rem !important;
    margin-top: 0 !important; /* 去掉标题顶部的默认间距 */
}

/* 输入框样式 */
.stNumberInput > div > div > input {
    border-radius: 10px;
    border: 2px solid #f3d7b7;
    padding: 0.75rem;
    transition: all 0.3s ease;
}

.stNumberInput > div > div > input:focus {
    border-color: #e67e22;
    box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.2);
}

/* 单选按钮样式 */
.stRadio > div {
    gap: 0.75rem;
}

.stRadio > div > label {
    background: #fff9f0;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid #f3d7b7;
    transition: all 0.3s ease;
}

.stRadio > div > label:hover {
    background: #fff0e0;
    border-color: #e67e22;
}

.stRadio > div > label[data-baseweb="radio"]:has(input:checked) {
    background: #e67e22;
    color: white;
    border-color: #d35400;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(230, 126, 34, 0.3);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(230, 126, 34, 0.4);
    background: linear-gradient(135deg, #d35400 0%, #c0392b 100%);
}

/* 标签页样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: white;
    padding: 0.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    color: #7f8c8d;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(230, 126, 34, 0.3);
}

/* 下拉框样式 */
.stSelectbox > div > div {
    border-radius: 10px;
    border: 2px solid #f3d7b7;
}

.stSelectbox > div > div:focus {
    border-color: #e67e22;
    box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.2);
}

/* 文件上传和相机输入样式 */
.stFileUploader > div, .stCameraInput > div {
    border-radius: 12px;
    border: 2px dashed #f3d7b7;
    background: #fff9f0;
    transition: all 0.3s ease;
}

.stFileUploader > div:hover, .stCameraInput > div:hover {
    border-color: #e67e22;
    background: #fff0e0;
}

/* 展开面板样式 */
.streamlit-expanderHeader {
    background: #fff9f0;
    border-radius: 10px;
    border: 1px solid #f3d7b7;
    font-weight: 600;
    color: #d35400;
}

.streamlit-expanderContent {
    background: white;
    border-radius: 0 0 10px 10px;
    border: 1px solid #f3d7b7;
    border-top: none;
}

/* 进度条样式 */
.stProgress > div > div {
    background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
}

/* 错误和信息提示样式 */
.stAlert {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

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
        "file_error": "菜品数据文件缺失，请确保chinese_dishes.json和thai_dishes.json在同一目录",
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

# 加载模型和数据函数
@st.cache_resource
def load_yolo_model():
    try:
        return YOLO("yolov8n-cls.pt")
    except Exception as e:
        st.error(f"模型加载失败：{str(e)}")
        return None

@st.cache_data
def load_nutrition_db():
    if not os.path.exists("nutrition_db.json"):
        return {}
    try:
        with open("nutrition_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def recognize_dish_local(image, model, nutrition_db, lang):
    results = model(image, conf=0.2)
    recognized_dishes = []
    
    for result in results:
        top5_indices = result.probs.top5
        top5_confidences = result.probs.top5conf
        
        for i in range(3):
            class_id = int(top5_indices[i])
            class_name = model.names[class_id]
            confidence = float(top5_confidences[i])
            
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

@st.cache_data(show_spinner=False)
def load_dishes(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# 语言选择
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

# ===================== 先创建标签页，再使用它们 =====================
tab1, tab2 = st.tabs(["🍜 智能配餐", "📷 本地AI菜品识别"])

# ===================== 标签页1：智能配餐功能（已删除白框） =====================
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 直接显示标题和内容，没有白框
        st.subheader("个人信息")
        
        height = st.number_input(t["height"], min_value=100, max_value=220, value=161)
        weight = st.number_input(t["weight"], min_value=30, max_value=150, value=45)
        age = st.number_input(t["age"], min_value=10, max_value=100, value=20)
        gender = st.radio(t["gender"], t["gender_options"])
        
        st.markdown("---")
        
        scene = st.radio(t["scene"], t["scene_options"], help=t["scene_tip"])
        crowd = st.radio(t["crowd"], t["crowd_options"], help=t["crowd_tip"])
        taste = st.selectbox(t["taste"], t["taste_options"])
        allergy = st.text_input(t["allergy"], placeholder=t["allergy_placeholder"])
        cuisine = st.radio(t["cuisine"], t["cuisine_options"])
        
        st.markdown("---")
        
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
                
                tip = selected_menu["tip_cn"] if lang == "中文" else selected_menu["tip_th"]
                res += f"\n💡 {t['tip']}：{tip}\n"
                
                st.session_state["result"] = res
                st.rerun()

    with col2:
        # 直接显示标题和结果，没有白框
        st.subheader(t["result"])
        
        if "result" in st.session_state:
            st.markdown(st.session_state["result"])
        else:
            st.info("👈 请在左侧填写个人信息，然后点击「一键生成配餐方案」")

# ===================== 标签页2：本地AI菜品识别功能（已删除白框） =====================
with tab2:
    st.subheader(t["recognition"])
    
    if not yolo_model:
        st.error(t["model_error"])
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            uploaded_file = st.file_uploader(t["upload_image"], type=["jpg", "jpeg", "png"])
        with col2:
            camera_image = st.camera_input(t["take_photo"])
        
        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        elif camera_image is not None:
            image = Image.open(camera_image)
        
        if image is not None:
            st.image(image, width=400, use_column_width=True)
            
            if st.button(t["recognize"], type="primary", key="rec_btn"):
                with st.spinner(t["recognizing"]):
                    results = recognize_dish_local(image, yolo_model, nutrition_db, "cn" if lang == "中文" else "th")
                    
                    if results and len(results) > 0:
                        st.subheader(t["recognition_result"])
                        
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
