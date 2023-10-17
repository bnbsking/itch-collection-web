import datetime, json, sys
import pandas as pd
import streamlit as st
import yaml
import utils
import extra_streamlit_components as stx

print("-"*25+"P1"+"-"*25)

# meta
try:
    cookie_manager = stx.CookieManager()
except:
    utils.nav_page("P1-Patient-Filling")
if not utils.isLogin(cookie_manager):
    utils.nav_page("P0-Login")
    sys.exit()
hospital = utils.getHospital(cookie_manager)
cfg = yaml.safe_load(open('config.yaml', 'r'))
data_path = f"{cfg['data_path']}/data/{hospital}"
cdm = pd.read_csv("./pages/cdm.csv").set_index('Unnamed: 0')

# title
title = f"<h1 style='text-align: center'> {hospital} - 癢症資料收集系統 </h1>"
subtitle = "<h3 style='text-align: center'> (病患填寫) </h3>"
st.markdown(title, unsafe_allow_html=True)
st.markdown(subtitle, unsafe_allow_html=True)

# patient data
D = {}

# 1 Basic -> 8 features
minDate = datetime.datetime(1900,1,1)
today = datetime.datetime.now().date()
D["STUDY_DATE"] = st.date_input(cdm["STUDY_DATE"]["Chinese"], format="YYYY/MM/DD", value=today, disabled=True)
D["INDEX_DATE"] = st.date_input(cdm["INDEX_DATE"]["Chinese"], min_value=minDate, max_value=today, format="YYYY/MM/DD")
D["GENDER"] = st.radio(cdm["GENDER"]["Chinese"], cdm["GENDER"]["Format"].split('/'), horizontal=True)
D["DATE_OF_BIRTH"] = st.date_input(cdm["DATE_OF_BIRTH"]["Chinese"], min_value=minDate, max_value=today, format="YYYY/MM/DD")
D["BH"] = st.number_input(cdm["BH"]["Chinese"]+" (cm)", min_value=0.0, max_value=300.0, step=0.1, value=0.0, format="%f")
D["BW"] = st.number_input(cdm["BW"]["Chinese"]+" (kg)", min_value=0.0, max_value=300.0, step=0.1, value=0.0, format="%f")
D["BMI"] = st.number_input(cdm["BMI"]["Chinese"], min_value=0.0, step=0.1, 
    value=round(D["BW"]/((D["BH"]+1e-10)*0.01)**2,2), format="%f", disabled=True)
D["SMOKE"] = st.selectbox(cdm["SMOKE"]["Chinese"], options=["","是","否"])
st.divider()

# 2 Env -> 4 features
for col in ["OCCUPATION", "EXPOSURE", "RESIDENCE", "WORKING_SITE"]:
    D[col] = st.text_input(cdm[col]['Chinese'], max_chars=100)
st.divider()

# 3 Score -> 2 features
D["Itch_NRS"] = st.slider("癢程度 - 評分表", min_value=0, max_value=10, value=0, step=1)
st.write("皮膚病生活質量指數 DLQI - 評分表")
scoreL = []
for question,options in utils.DLQI.items():
    scoreL.append( st.radio(question, options, horizontal=True, index=len(options)-1) )
score = scoreL.count("非常嚴重")*3 + scoreL.count("嚴重")*2 + scoreL.count("較輕")*1 + scoreL.count("是")*1
D["DLQI"] = st.number_input("DLQI", min_value=0, max_value=30, step=1, value=score, disabled=True)
st.divider()

# 4 History -> 6 features
chronicL = ["高血壓", "高血糖", "高血脂"]
selectL = st.multiselect("有 高血壓 or 高血糖 or 高血脂", chronicL)
for col in chronicL:
    D[col] = col in selectL
#
historyL = ["MEDICATION_USE_STATUS", "DRUG_ALLERGY_HISTORY", "ALLERGY_HISTORY_EXCEPT_DRUG"]
historyAdditionL = ["服用西藥/中藥/保健食品", "任何藥物", "如塵蟎,食物,..."]
for col, addition in zip(historyL, historyAdditionL):
    ans = st.selectbox(f"{cdm[col]['Chinese']} ({addition})", options=["","是","否"])
    if ans=="是":
        col1, col2 = st.columns(2)
        with col2:
            D[col] = st.text_input("請說明", max_chars=100, key=col)
    else:
        D[col] = ans
st.divider()

assert len(D.keys() - set(cdm.columns)) == 0
assert len(D)==((cdm.loc["Page"]=="1").sum()) # 20

if st.button("submit"):
    bool_cols = list(cdm.columns[ (cdm.loc["Page"]=="1") & (cdm.loc["Type"]=="bool") ]) # 1 smoke + 3 chronic
    date_cols = list(cdm.columns[ (cdm.loc["Page"]=="1") & (cdm.loc["Type"]=="date") ]) # 3 study,index,birth
    str_cols  = list(cdm.columns[ (cdm.loc["Page"]=="1") & (cdm.loc["Type"]=="str") ])  # 4 env + 3 history

    # empty check
    emptyL = []
    for col in ["BH", "BW"] + bool_cols + str_cols:
        if D[col]=="":
            emptyL.append(cdm[col]["Chinese"])
    if emptyL:
        error_msg = ", ".join(emptyL) + " 不可為空"
        st.write(f":red[{error_msg}]")
        sys.exit()

    # type conversion + save
    for col in bool_cols:
        D[col] = D[col]=="是"
    for col in date_cols:
        D[col] = str(D[col]).replace('-','')
    for col in str_cols:
        D[col] = D[col].strip()
        D[col] = "_"*int(not D[col] or D[col][0].isnumeric() or D[col][0]==".") + D[col]
    D['now'] = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    json.dump(D, open(f"{data_path}/.tmp/patient_data.json","w"))
    
    # change page
    utils.alert("Submit successfully")
    utils.nav_page("P2-Doctor-Filling-A")