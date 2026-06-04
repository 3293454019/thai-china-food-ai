import streamlit as st
import requests
import json
import os

# ====================== 替换成你的讯飞星火API密钥 ======================
SPARK_APP_ID = "你的APP_ID"
SPARK_API_KEY = "你的API_KEY"
SPARK_API_SECRET = "你的API_SECRET"
# ====================================================================

# 中泰菜品数据库（内置）
CHINESE_FOODS = {
    "螺蛳粉": {"calories": 132, "protein": 5.6, "allergy": "小麦、大豆、花生", "origin": "起源于广西柳州，20世纪80年代由夜市摊点发展而来，融合柳州米粉文化与酸辣风味", "suitable": "一般人群，尤其适合喜酸辣的年轻人", "taboo": "肠胃疾病患者、孕妇、过敏体质者慎食"},
    "玉米胡萝卜排骨汤": {"calories": 65, "protein": 4.2, "allergy": "无常见强过敏源", "origin": "粤式经典靓汤，源自岭南\"清补凉\"饮食文化，讲究食材本味与养生", "suitable": "老少皆宜，术后恢复、体质虚弱者尤佳", "taboo": "痛风急性期禁食，肾功能不全者适量"},
    "糖醋排骨": {"calories": 280, "protein": 16.7, "allergy": "大豆（酱油）", "origin": "起源于江苏无锡，淮扬菜经典代表，酸甜口味风靡全国", "suitable": "一般人群，食欲不振者尤佳", "taboo": "糖尿病、肥胖、胃酸过多者慎食"},
    "桂林米粉": {"calories": 118, "protein": 3.8, "allergy": "小麦、大豆", "origin": "起源于广西桂林，距今2000余年，相传与秦始皇开凿灵渠有关", "suitable": "一般人群，适合早餐/快餐", "taboo": "肠胃疾病患者慎食，过敏体质者注意卤料成分"},
    "银耳羹": {"calories": 38, "protein": 0.5, "allergy": "无常见强过敏源", "origin": "古代宫廷滋补甜品，有\"平民燕窝\"之称，滋阴润肺", "suitable": "一般人群，女性、老年人、阴虚火旺者尤佳", "taboo": "风寒咳嗽、腹泻患者慎食"},
    "八宝饭": {"calories": 225, "protein": 4.8, "allergy": "坚果、小麦、大豆", "origin": "源自古代\"八宝粥\"，传统节日食品，象征团圆吉祥", "suitable": "一般人群，节日食用", "taboo": "糖尿病、肥胖、消化不良者慎食"},
    "宫保鸡丁": {"calories": 189, "protein": 16.3, "allergy": "花生、大豆", "origin": "起源于清朝，由四川总督丁宝桢发明，川菜经典名菜", "suitable": "一般人群，下饭首选", "taboo": "花生过敏者、痛风患者慎食"},
    "麻婆豆腐": {"calories": 135, "protein": 8.1, "allergy": "大豆", "origin": "起源于四川成都，清代陈麻婆创制，川菜标志性菜品", "suitable": "一般人群，下饭首选", "taboo": "肾病、痛风、大豆过敏者慎食"},
    "鱼香肉丝": {"calories": 168, "protein": 10.2, "allergy": "大豆、小麦", "origin": "起源于四川，川菜经典家常菜，因调味有鱼香味得名", "suitable": "一般人群，下饭首选", "taboo": "糖尿病、肠胃疾病患者慎食"},
    "红烧肉": {"calories": 395, "protein": 11.4, "allergy": "大豆（酱油）", "origin": "中国传统家常菜，各地均有特色，肥而不腻", "suitable": "一般人群，体力劳动者尤佳", "taboo": "高血压、高血脂、冠心病患者慎食"},
    "番茄炒蛋": {"calories": 86, "protein": 4.2, "allergy": "鸡蛋", "origin": "中国最普及的家常菜，做法简单营养均衡", "suitable": "老少皆宜，几乎所有人群", "taboo": "鸡蛋过敏者禁食，胃酸过多者适量"},
    "清炒时蔬": {"calories": 45, "protein": 2.1, "allergy": "无常见强过敏源", "origin": "中国传统家常菜，清淡少油保留食材本味", "suitable": "老少皆宜，减肥、三高人群尤佳", "taboo": "无特殊忌口，注意食材新鲜"},
    "扬州炒饭": {"calories": 180, "protein": 5.8, "allergy": "鸡蛋、小麦", "origin": "起源于江苏扬州，淮扬菜经典主食，相传与隋炀帝有关", "suitable": "一般人群，快餐首选", "taboo": "糖尿病、肥胖人群适量"},
    "兰州拉面": {"calories": 110, "protein": 4.6, "allergy": "小麦、牛肉", "origin": "起源于甘肃兰州，中国最具影响力面食，有\"一清二白三红四绿五黄\"标准", "suitable": "一般人群，早餐/午餐首选", "taboo": "小麦过敏者禁食，痛风患者慎食"},
    "重庆小面": {"calories": 125, "protein": 5.1, "allergy": "小麦、大豆", "origin": "起源于重庆，重庆四大特色之一，麻辣鲜香", "suitable": "一般人群，喜麻辣者", "taboo": "肠胃疾病、痔疮、孕妇慎食"},
    "武汉热干面": {"calories": 152, "protein": 4.9, "allergy": "小麦、芝麻", "origin": "起源于湖北武汉，中国十大名面之一，武汉人早餐首选", "suitable": "一般人群，早餐首选", "taboo": "小麦过敏者禁食，消化不良者适量"},
    "北京烤鸭": {"calories": 436, "protein": 18.3, "allergy": "无常见强过敏源", "origin": "起源于南北朝，北京标志性美食，被誉为\"天下第一美味\"", "suitable": "一般人群，宴请首选", "taboo": "高血压、高血脂、肥胖人群慎食"},
    "小笼包": {"calories": 230, "protein": 7.5, "allergy": "小麦、猪肉", "origin": "起源于上海，江南经典小吃，皮薄馅大汤汁鲜美", "suitable": "一般人群，早餐/点心首选", "taboo": "小麦过敏者禁食，肥胖人群适量"},
    "饺子": {"calories": 240, "protein": 7.8, "allergy": "小麦、猪肉", "origin": "起源于东汉，医圣张仲景发明，中国传统节日食品", "suitable": "老少皆宜，节日食用", "taboo": "小麦过敏者禁食，消化不良者适量"},
    "馄饨": {"calories": 110, "protein": 4.2, "allergy": "小麦、猪肉", "origin": "起源于西汉，历史比饺子更悠久，各地叫法不同（云吞/抄手）", "suitable": "一般人群，早餐/夜宵首选", "taboo": "小麦过敏者禁食，肠胃疾病患者适量"},
    "汤圆": {"calories": 260, "protein": 3.2, "allergy": "糯米、芝麻", "origin": "起源于宋朝，元宵节传统食品，象征团圆美满", "suitable": "一般人群，节日食用", "taboo": "糖尿病、肥胖、消化不良者慎食"},
    "粽子": {"calories": 220, "protein": 4.5, "allergy": "糯米、红枣/肉类", "origin": "起源于战国，端午节纪念屈原的传统食品", "suitable": "一般人群，节日食用", "taboo": "糖尿病、肥胖、消化不良者慎食"},
    "广式月饼": {"calories": 425, "protein": 6.1, "allergy": "小麦、鸡蛋、坚果", "origin": "起源于唐朝，中秋节传统食品，广式月饼皮薄馅大", "suitable": "一般人群，节日食用", "taboo": "糖尿病、肥胖、高血脂患者慎食"},
    "珍珠奶茶": {"calories": 52, "protein": 0.8, "allergy": "牛奶、茶叶", "origin": "起源于中国台湾，全球流行饮品，融合茶与奶的风味", "suitable": "一般人群，年轻人", "taboo": "糖尿病、肥胖、失眠者慎食"},
    "豆浆油条": {"calories": 380, "protein": 8.5, "allergy": "大豆、小麦", "origin": "中国传统早餐组合，豆浆起源于西汉，油条起源于南宋", "suitable": "一般人群，早餐首选", "taboo": "大豆过敏者禁食，高血脂患者适量"}
}

THAI_FOODS = {
    "冬阴功汤": {"calories": 85, "protein": 6.2, "allergy": "海鲜、虾、柠檬草", "origin": "泰国国汤，起源于大城王朝，\"冬阴\"=酸辣，\"功\"=虾", "suitable": "一般人群，喜酸辣者", "taboo": "肠胃疾病、孕妇、海鲜过敏者禁食"},
    "青木瓜沙拉": {"calories": 45, "protein": 1.8, "allergy": "鱼露、虾酱、花生", "origin": "起源于泰国东北部，泰国最受欢迎凉菜，酸辣脆爽", "suitable": "一般人群，减肥人群尤佳", "taboo": "海鲜、花生过敏者慎食"},
    "芒果糯米饭": {"calories": 210, "protein": 3.1, "allergy": "糯米、芒果、椰子", "origin": "起源于素可泰王朝，泰国标志性甜品，象征甜蜜丰收", "suitable": "一般人群，喜甜食者", "taboo": "糖尿病、肥胖、消化不良者慎食"},
    "泰式椰汁鸡": {"calories": 125, "protein": 8.7, "allergy": "鸡肉、椰子", "origin": "起源于泰国中部，融合椰文化与中式煲汤理念", "suitable": "一般人群，体质虚弱者尤佳", "taboo": "椰子过敏者禁食，痛风患者慎食"},
    "泰式酸辣凤爪": {"calories": 120, "protein": 15.3, "allergy": "鱼露、柠檬", "origin": "起源于泰国街头，国民小吃，酸辣开胃", "suitable": "一般人群，下酒/零食首选", "taboo": "肠胃疾病、孕妇慎食"},
    "泰式咖喱蟹": {"calories": 168, "protein": 14.2, "allergy": "海鲜、蟹、椰子", "origin": "起源于曼谷，泰国海鲜料理代表，咖喱与海鲜完美融合", "suitable": "一般人群，宴请首选", "taboo": "海鲜、椰子过敏者禁食"},
    "菠萝炒饭": {"calories": 180, "protein": 5.6, "allergy": "鸡蛋、菠萝、虾", "origin": "起源于泰国中部，经典主食，酸甜可口色彩鲜艳", "suitable": "一般人群，儿童/年轻人尤佳", "taboo": "海鲜、鸡蛋过敏者慎食"},
    "泰式炒河粉": {"calories": 145, "protein": 5.3, "allergy": "大米、鸡蛋、虾", "origin": "起源于曼谷，世界十大美食之一，泰国国民面食", "suitable": "一般人群，快餐首选", "taboo": "海鲜、鸡蛋过敏者慎食"},
    "绿咖喱鸡": {"calories": 135, "protein": 9.1, "allergy": "鸡肉、椰子、辣椒", "origin": "起源于泰国中部，最辣的泰国咖喱，颜色来自新鲜青辣椒", "suitable": "一般人群，喜辣味者", "taboo": "椰子过敏者禁食，肠胃疾病患者慎食"},
    "红咖喱牛肉": {"calories": 152, "protein": 12.3, "allergy": "牛肉、椰子、辣椒", "origin": "起源于泰国东北部，颜色来自干辣椒，口感浓郁辛辣", "suitable": "一般人群，喜辣味者", "taboo": "椰子过敏者禁食，痛风患者慎食"},
    "黄咖喱鱼": {"calories": 128, "protein": 11.5, "allergy": "海鲜、鱼、椰子", "origin": "起源于泰国南部，颜色来自姜黄，口感温和受众广", "suitable": "一般人群，家庭食用", "taboo": "海鲜、椰子过敏者禁食"},
    "泰式烤鸡": {"calories": 215, "protein": 20.1, "allergy": "鸡肉", "origin": "起源于泰国东北部，街头最常见美食，香茅柠檬叶腌制烤制", "suitable": "一般人群，烧烤爱好者", "taboo": "无特殊忌口，适量食用"},
    "香蕉煎饼": {"calories": 280, "protein": 4.2, "allergy": "小麦、香蕉、鸡蛋", "origin": "起源于泰国街头，国民甜品小吃，酥脆香甜", "suitable": "一般人群，年轻人", "taboo": "糖尿病、肥胖人群慎食"},
    "椰子冻": {"calories": 150, "protein": 2.1, "allergy": "椰子", "origin": "起源于泰国热带地区，天然椰壳制作，清凉爽滑", "suitable": "一般人群，夏季食用", "taboo": "椰子过敏者禁食，糖尿病患者适量"},
    "泰式奶茶": {"calories": 95, "protein": 1.2, "allergy": "牛奶、茶叶", "origin": "起源于泰国，本地红茶加炼乳制作，橙红香甜", "suitable": "一般人群，年轻人", "taboo": "糖尿病、肥胖、失眠者慎食"},
    "芒果汁": {"calories": 45, "protein": 0.5, "allergy": "芒果", "origin": "泰国芒果主产国，国民饮品，香甜浓郁", "suitable": "一般人群，全年龄段", "taboo": "芒果过敏者禁食，糖尿病患者适量"},
    "榴莲糯米饭": {"calories": 245, "protein": 3.5, "allergy": "糯米、榴莲、椰子", "origin": "起源于泰国南部，\"水果之王\"与糯米饭的经典搭配", "suitable": "一般人群，榴莲爱好者", "taboo": "糖尿病、肥胖、上火者慎食"},
    "青咖喱汤": {"calories": 75, "protein": 4.8, "allergy": "椰子、辣椒、海鲜", "origin": "起源于泰国中部，经典汤品，酸辣浓郁带椰香", "suitable": "一般人群，喜辣味者", "taboo": "椰子、海鲜过敏者禁食"},
    "泰式春卷": {"calories": 190, "protein": 4.5, "allergy": "小麦、蔬菜、虾", "origin": "源自中国传入泰国改良，薄皮包裹食材炸制", "suitable": "一般人群，点心首选", "taboo": "海鲜、小麦过敏者慎食"},
    "炸鱼饼": {"calories": 185, "protein": 10.2, "allergy": "海鲜、鱼", "origin": "起源于泰国南部，经典小吃，新鲜鱼肉打泥炸制", "suitable": "一般人群，下酒首选", "taboo": "海鲜过敏者禁食"},
    "酸辣海鲜汤": {"calories": 90, "protein": 7.8, "allergy": "海鲜、虾、贝类", "origin": "起源于泰国沿海，冬阴功汤海鲜升级版，食材丰富", "suitable": "一般人群，海鲜爱好者", "taboo": "海鲜过敏者禁食，肠胃疾病患者慎食"},
    "泰式炒空心菜": {"calories": 65, "protein": 2.8, "allergy": "鱼露、虾酱", "origin": "泰国最常见蔬菜料理，虾酱辣椒炒制", "suitable": "一般人群，搭配主食", "taboo": "海鲜过敏者慎食"},
    "罗勒炒猪肉": {"calories": 165, "protein": 12.5, "allergy": "猪肉、罗勒", "origin": "起源于泰国东北部，国民家常菜，香辣下饭", "suitable": "一般人群，下饭首选", "taboo": "无特殊忌口，适量食用"},
    "椰汁西米露": {"calories": 120, "protein": 1.1, "allergy": "椰子、西米", "origin": "泰国经典甜品，香甜爽滑带椰香", "suitable": "一般人群，夏季食用", "taboo": "椰子过敏者禁食，糖尿病患者适量"},
    "泰式烤鱿鱼": {"calories": 110, "protein": 18.3, "allergy": "海鲜、鱿鱼", "origin": "起源于泰国沿海，街头烧烤美食，口感Q弹", "suitable": "一般人群，海鲜爱好者", "taboo": "海鲜过敏者禁食，痛风患者慎食"}
}

# 中泰膳食标准
DIET_STANDARDS = {
    "中国": {
        "male": {"calories": 2250, "protein": 65},
        "female": {"calories": 1800, "protein": 55},
        "ratio": {"protein": "10-15%", "carbs": "50-65%", "fat": "20-30%"}
    },
    "泰国": {
        "male": {"calories": 2100, "protein": 60},
        "female": {"calories": 1700, "protein": 50},
        "ratio": {"protein": "10-15%", "carbs": "55-70%", "fat": "20-30%"}
    }
}

# 中泰双语翻译
trans = {
    "中文": {
        "title": "中泰AI智能营养配餐与饮食科普系统",
        "height": "身高(cm)",
        "weight": "体重(kg)",
        "age": "年龄",
        "gender": "性别",
        "taste": "口味偏好",
        "allergy": "饮食忌口",
        "cuisine": "配餐菜系",
        "generate": "一键生成配餐方案",
        "loading": "AI正在生成三餐食谱+菜品文化介绍...",
        "result": "生成结果",
        "nutrition": "营养分析",
        "culture": "菜品文化科普"
    },
    "ภาษาไทย": {
        "title": "ระบบ AI สร้างเมนูอาหารและวัฒนธรรมอาหารจีน-ไทย",
        "height": "ส่วนสูง (ซม.)",
        "weight": "น้ำหนัก (กก.)",
        "age": "อายุ",
        "gender": "เพศ",
        "taste": "รสชาติที่ชอบ",
        "allergy": "อาหารที่แพ้",
        "cuisine": "ประเภทอาหาร",
        "generate": "สร้างเมนูอาหารทันที",
        "loading": "AI กำลังสร้างเมนูอาหารและข้อมูลวัฒนธรรม...",
        "result": "ผลลัพธ์",
        "nutrition": "การวิเคราะห์โภชนาการ",
        "culture": "ข้อมูลวัฒนธรรมอาหาร"
    }
}

# 调用讯飞星火API
def get_spark_response(prompt):
    url = "https://spark-api.xfyun.cn/v3.5/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": SPARK_APP_ID,
        "api_key": SPARK_API_KEY,
        "api_secret": SPARK_API_SECRET,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"生成失败，请稍后重试：{str(e)}"

# 页面配置
st.set_page_config(page_title="中泰营养配餐AI", layout="wide")

# 侧边栏语言切换
lang = st.sidebar.selectbox("语言 / ภาษา", ["中文", "ภาษาไทย"])
t = trans[lang]

# 主页面
st.title(t["title"])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("个人信息")
    height = st.number_input(t["height"], min_value=100, max_value=220, value=165)
    weight = st.number_input(t["weight"], min_value=30, max_value=150, value=55)
    age = st.number_input(t["age"], min_value=10, max_value=100, value=20)
    gender = st.radio(t["gender"], ["男", "女"])
    taste = st.selectbox(t["taste"], ["清淡", "微辣", "酸辣", "重辣"])
    allergy = st.multiselect(t["allergy"], ["海鲜过敏", "坚果过敏", "素食", "乳糖不耐受"])
    cuisine = st.radio(t["cuisine"], ["中餐", "泰餐"])

    if st.button(t["generate"], type="primary"):
        with st.spinner(t["loading"]):
            # 核心Prompt（内置数据库，保证数据准确）
            food_db = CHINESE_FOODS if cuisine == "中餐" else THAI_FOODS
            standard = DIET_STANDARDS["中国" if cuisine == "中餐" else "泰国"]
            target_calories = standard["male"]["calories"] if gender == "男" else standard["female"]["calories"]
            target_protein = standard["male"]["protein"] if gender == "男" else standard["female"]["protein"]

            prompt = f"""
            你是中泰饮食营养专家，用{lang}输出。
            用户信息：身高{height}cm，体重{weight}kg，年龄{age}岁，性别{gender}，口味{taste}，忌口{allergy}，想要{cuisine}配餐。
            每日目标热量：{target_calories}kcal，每日目标蛋白质：{target_protein}g。
            只能从以下菜品中选择：{list(food_db.keys())}
            请生成一日三餐搭配，每道菜标注：
            1. 菜品名称
            2. 每份热量(kcal)、蛋白质(g)含量
            3. 菜品起源文化和地域习俗科普
            4. 适宜人群和忌口提示
            最后附上总热量和总蛋白质的营养分析。
            格式清晰，分点列出，不要超过500字。
            """
            result = get_spark_response(prompt)
            st.session_state["result"] = result

with col2:
    if "result" in st.session_state:
        st.subheader(t["result"])
        st.write(st.session_state["result"])