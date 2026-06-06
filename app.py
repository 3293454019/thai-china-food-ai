# ===================== 标签页1：智能配餐功能 =====================
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 先打开卡片，再放标题（标题就会在白框里面）
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # 先打开卡片，再放标题（标题就会在白框里面）
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(t["result"])
        
        if "result" in st.session_state:
            st.markdown(st.session_state["result"])
        else:
            st.info("👈 请在左侧填写个人信息，然后点击「一键生成配餐方案」")
        
        st.markdown('</div>', unsafe_allow_html=True)
