import streamlit as st
import cv2
import numpy as np
import datetime, glob, json, os, re, shutil, sys
import pandas as pd
import yaml
import utils
import extra_streamlit_components as stx
from unidecode import unidecode

print("-"*25+"P2"+"-"*25)

# meta
try:
    cookie_manager = stx.CookieManager()
except:
    utils.nav_page("P2-Doctor-Filling-A")
if not utils.isLogin(cookie_manager):
    utils.nav_page("P0-Login")
    sys.exit()
hospital = utils.getHospital(cookie_manager)
cfg = yaml.safe_load(open('config.yaml', 'r'))
data_path = f"{cfg['data_path']}/data/{hospital}"
cdm = pd.read_csv("./pages/cdm.csv").set_index('Unnamed: 0') # (5,56)

# title
title = f"<h1 style='text-align: center'> {hospital} - 癢症資料收集系統 </h1>"
subtitle = "<h3 style='text-align: center'> (醫師填寫 - A) </h3>"
st.markdown(title, unsafe_allow_html=True)
st.markdown(subtitle, unsafe_allow_html=True)

# basic
patientD_path = f"{data_path}/.tmp/patient_data.json"
patientD = json.load(open(patientD_path,'r')) if glob.glob(patientD_path) else {"now":""}
patient_time = st.text_input("Last patient submit time", max_chars=100, value=patientD['now'], disabled=True)
patient_id = st.text_input("Patient ID", max_chars=100)
disease_id = st.radio("Disease", [d.replace('-',' ') for d in utils.diseaseD.keys()], horizontal=True)
disease_id = disease_id.replace(' ', '-')
if not patient_id or not patient_time:
    sys.exit()
else: # patient data # 1 Basic -> 3 features
    D = patientD
    D.pop("now")
    D["HOSPITAL"], D["PATIENT_ID"], D["DISEASE"] = hospital, patient_id, disease_id
    st.divider()

# image - file uploader
with st.form("my-form", clear_on_submit=True):
    fileL = st.file_uploader("File uploader", accept_multiple_files=True)
    submitted = st.form_submit_button("Upload")
    if submitted:
        for file in fileL:
            bt_str = file.getvalue()
            try:
                img = np.frombuffer(bt_str, dtype=np.uint8)
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                filepath = unidecode(f"{data_path}/.tmp/{file.name.split('.')[0]}.jpg").replace(' ','')
                cv2.imwrite(filepath, img)
            except:
                print(f"Not image file: {file.name}")

# image - preview
def delete(path):
    os.remove(path)
    st.write("")
st.write("Current images")
colList = st.columns(4)
for i,path in enumerate(glob.glob(f"{data_path}/.tmp/*.jpg")):
    image = cv2.imread(path)[:,:,::-1]
    with colList[i%4]:
        st.image(image)
        st.checkbox(os.path.basename(path), key=f"select_{i}", value=True)
        st.button("delete", key=f"delete_{i}", on_click=delete, args=(path,))
st.divider()

# 2 lesion distribution -> 8 features
lesionL = ["UPPER_LIMBS", "LOWER_LIMBS", "TRUNK", "HEAD_AND_NECK", "INGUINAL_AREA", "AXILLA", "UMBILICUS", "FINGERWEB"]
selectL = st.multiselect("病灶分佈", [cdm[col]["Chinese"].replace("病灶分佈-","") for col in lesionL])
for col in lesionL:
    D[col] = cdm[col]["Chinese"].replace("病灶分佈-","") in selectL

# 3 lesion presentation -> 4 features
presentL = ["CUTANEOUS_FINDING_紅疹", "CUTANEOUS_FINDING_丘疹", "CUTANEOUS_FINDING_水泡", "MUCOSA_INVOLVEMEN"]
selectL = st.multiselect("病灶表現", presentL)
for col in presentL:
    D[col] = col in selectL
st.divider()

assert len(D.keys() - set(cdm.columns)) == 0
assert len(D)==( (cdm.loc["Page"]=="1") | (cdm.loc["Page"]=="2") ).sum() # 18+15=33

# export 
if st.button("Export"):
    today = datetime.datetime.now().strftime("%Y%m%d")
    filePrefix = f"{hospital}_{today}_{patient_id}_{disease_id}"

    # image
    if not any( getattr(st.session_state, f"select_{i}") for i in range(len(glob.glob(f"{data_path}/.tmp/*.jpg"))) ):
        st.write(":red[Image cannot be null]")
        sys.exit()
    for i,path in enumerate(glob.glob(f"{data_path}/.tmp/*.jpg")):
        check = getattr(st.session_state, f"select_{i}")
        if check:
            maxExpPath = max(glob.glob(f"{os.path.dirname(path)}/../export_img/*/{filePrefix}_*")+[''])
            maxExpId = int(re.findall(f"_([0-9]+)\.jpg",maxExpPath)[0]) if maxExpPath else -1
            shutil.move(path, f"{os.path.dirname(path)}/../export_img/{disease_id}/{filePrefix}_{maxExpId+1}.jpg")
        else:
            os.remove(path)
    
    # tabular
    with open(f"{os.path.dirname(patientD_path)}/{filePrefix}.json", "w") as f:
        json.dump(D, f)
    os.remove(patientD_path)
    
    # reset
    utils.alert("Export successfully")
    #utils.nav_page("P3-Doctor-Filling-B")
    utils.nav_page("P1-Patient-Filling")
