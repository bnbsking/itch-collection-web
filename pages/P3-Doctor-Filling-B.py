import streamlit as st
import glob, json, os, sys
import pandas as pd
import yaml
import utils
import extra_streamlit_components as stx

print("-"*25+"P3"+"-"*25)

# meta
try:
    cookie_manager = stx.CookieManager()
except:
    utils.nav_page("P3-Doctor-Filling-B")
if not utils.isLogin(cookie_manager):
    utils.nav_page("P0-Login")
    sys.exit()
hospital = utils.getHospital(cookie_manager)
cfg = yaml.safe_load(open('config.yaml', 'r'))
data_path = f"{cfg['data_path']}/data/{hospital}"
cdm = pd.read_csv("./pages/cdm.csv").set_index('Unnamed: 0') # (5,56)

# title
title = f"<h1 style='text-align: center'> {hospital} - 癢症資料收集系統 </h1>"
subtitle = "<h3 style='text-align: center'> (醫師填寫 - B) </h3>"
st.markdown(title, unsafe_allow_html=True)
st.markdown(subtitle, unsafe_allow_html=True)

# basic
try:
    patients = { path.split("_")[2]:path for path in glob.glob(f"{data_path}/.tmp/*.json") }
except:
    st.write("No data yet")
    sys.exit()
patient_id = st.selectbox("Patient", [""]+list(patients.keys()))
if not patient_id:
    sys.exit()
else:
    patientD_path = patients[patient_id]
    patientD = json.load(open(patients[patient_id],'r'))
    D = patientD
    st.divider()

# 1 allergic test -> 4 features
for col in ["KOH", "SHRIMP", "AIR", "MIXED_FOOD"]:
    D[col] = st.selectbox(col + " | " + cdm.at["Chinese",col], options=["","是","否"])
st.divider()

# 2 numbers -> 6+2 features
floatL = ['ECP', 'IgE', 'EOSINOPHILS', 'TSH', 'T3', 'FREE_T4']
for col in floatL:
    D[col] = st.number_input(col + " | " + cdm.at["Chinese",col], min_value=0.0, max_value=1e10, value=0.0, format="%f")
st.write("#") # linebreak
intL =["AST", "ALT"]
for col in intL:
    D[col] = st.number_input(col + " | " + cdm.at["Chinese",col], min_value=0, max_value=10**10, value=0, format="%d")
st.divider()

# 3 score and other tests -> 3 features
for col in ["BSA", 'EASI', 'PASI']:
    D[col] = st.number_input(col + " | " + cdm.at["Chinese",col], min_value=0.0, max_value=72.0, value=0.0, format="%f")
st.divider()

# 4 score and other tests -> 1+2 features
for col in ["MAST"]:
    D[col] = st.text_input(col + " | " + cdm.at["Chinese",col], max_chars=100)
for col in ['COMPATIBLE_BIOPSY_REPORT', 'PATCH_TEST']:
    D[col] = st.selectbox(col + " | " + cdm.at["Chinese",col], options=["","是","否"])
st.divider()

# 5 Climates -> 5 features
for col in ['AQI', 'PM2.5', "PM10", "O3", "SO2", "NO2", "CH4", "CO", "THC"]:
    D[col] = st.number_input(col + " | " + cdm.at["Chinese",col], min_value=0.0, max_value=1e10, value=0.0, step=0.01, format="%f")
st.markdown( "Reference: [環境部-空氣品質監測網](https://airtw.moenv.gov.tw/CHT/Query/StationData.aspx)" )
st.divider()
for col in ['UV_INDEX', 'HUMIDITY']:
    D[col] = st.number_input(col + " | " + cdm.at["Chinese",col], min_value=0.0, max_value=100.0, value=0.0, step=0.01, format="%f")
st.markdown( "Reference: [交通部-中央氣象署](https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6400900)" )
st.divider()
for col in ['PH']:
    D[col] = st.slider(col + " | " + cdm.at["Chinese",col], min_value=0.0, max_value=14.0, value=7.0, step=0.01)
st.markdown( "Reference: [台灣自來水公司-水質即時資訊](https://www.water.gov.tw/wq/)" )
st.divider()

assert set(D.keys()) == set(cdm.columns), (len(D.keys()), D.keys()) # 37+30=67

# export
export = st.button("Export")
if export:
    bool_cols = list(cdm.columns[ (cdm.loc["Page"]=="3") & (cdm.loc["Type"]=="bool") ]) # 1 smoke + 4 history
    str_cols  = list(cdm.columns[ (cdm.loc["Page"]=="3") & (cdm.loc["Type"]=="str") ])  # 4 env

    # empty check
    emptyL = []
    for col in bool_cols:
        if not bool(D[col]):
            emptyL.append(cdm.at["Chinese",col])
    if emptyL:
        error_msg = ", ".join(emptyL) + " 不可為空"
        st.write(f":red[{error_msg}]")
        sys.exit()

    # type conversion
    for col in bool_cols:
        D[col] = D[col]=="是"
    for col in str_cols:
        D[col] = D[col].strip()
        D[col] = "_"*int(not D[col] or D[col][0].isnumeric() or D[col][0]==".") + D[col]

    # tabular ＃ overall 67 columns
    pre_data_path = f"{data_path}/export_tab/data.csv"
    if glob.glob(pre_data_path):
        df = pd.read_csv(pre_data_path)
    else:
        df = pd.DataFrame({ col:[cdm.at["Default",col]] for col in cdm.columns }) # Default is for type alignment only
    df_patient = pd.DataFrame({key:[D[key]] for key in D})[cdm.columns]
    df = pd.concat([df, df_patient], axis=0).reset_index(drop=True)
    df.drop(0, inplace=True) if not glob.glob(pre_data_path) else None
    df.to_csv(pre_data_path, index=False)

    # reset
    os.remove(patientD_path)
    utils.alert("Export successfully")
    utils.nav_page("P3-Doctor-Filling-B")