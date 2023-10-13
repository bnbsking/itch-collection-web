import datetime, glob, sys, time
import streamlit as st
import pandas as pd
import yaml
import utils
import extra_streamlit_components as stx

print("-"*25+"P4"+"-"*25)

# meta
try:
    cookie_manager = stx.CookieManager()
except:
    utils.nav_page("P4-Table")
if not utils.isLogin(cookie_manager):
    utils.nav_page("P0-Login")
    sys.exit()
hospital = utils.getHospital(cookie_manager)
cfg = yaml.safe_load(open('config.yaml', 'r'))
data_path = f"{cfg['data_path']}/data/{hospital}"
cdm = pd.read_csv("./pages/cdm.csv").set_index('Unnamed: 0') # (5,56)

# title
title = f"<h1 style='text-align: center'> {hospital} - 癢症資料收集系統 </h1>"
subtitle = "<h3 style='text-align: center'> (醫師填寫) </h3>"
st.markdown(title, unsafe_allow_html=True)
st.markdown(subtitle, unsafe_allow_html=True)

# small password
account_in, password_in, submit_btn, login = st.empty(), st.empty(), st.empty(), False
account = account_in.text_input("Account", max_chars=100, value=cfg["account"] if cfg["autofill"] else "")
password = password_in.text_input("Passward", max_chars=100, value=cfg["password"] if cfg["autofill"] else "", type="password")
submit = submit_btn.button("Login")
if submit:
    if account==cfg["account"] and password==cfg["password"]:
        login = True
        account_in.empty()
        password_in.empty()
        submit_btn.empty()
    else:
        st.error(":red[Incorrect Account or Passward]")
if not login:
    sys.exit()

# load table
path = f"{data_path}/export_tab/data.csv"
date_cols = cdm.columns[cdm.loc["Type"]=="date"]
if glob.glob(path):
    df = pd.read_csv(path)
    for col in date_cols:
        df[col] = df[col].apply(lambda x: datetime.datetime.strptime(str(x),"%Y%m%d").date() )
else:
    st.write("No data now")
    sys.exit()

# merge table
df = df.sort_values(by=["HOSPITAL", "STUDY_DATE", "PATIENT_ID"]).reset_index(drop=True)
column_config = {} # col -> column_setting
today = datetime.datetime.now().date()
for col in df.columns:
    chinese, data_type, format, default, _ = cdm[col]
    help = f"{chinese}; {data_type}; {format}"
    if data_type=="str":
        column_config[col] = st.column_config.TextColumn(col, help=help, default=default)
    elif data_type=="date":
        column_config[col] = st.column_config.DateColumn(col, help=help, \
            default=today,
            max_value=today,
            format="YYYYMMDD" # for show # the save format always be "YYYY-MM-DD"
        )
    elif data_type=="bool":
        column_config[col] = st.column_config.CheckboxColumn(col, help=help, default=default)
    elif data_type in ("int","float"):
        minv, maxv = format.split("-") if format else (None,None)
        column_config[col] = st.column_config.NumberColumn(col, help=help, default=default, \
            min_value=eval(f"{data_type}({minv})") if minv else None,
            max_value=eval(f"{data_type}({maxv})") if maxv else None
        )
    elif data_type=="category":
        column_config[col] = st.column_config.SelectboxColumn(col, help=help, default=default, \
            options=format.split('/')
        )
lockL = ["HOSPITAL", "STUDY_DATE", "PATIENT_ID", "DISEASE", "BMI", "DLQI"]
st.subheader("Tabular data")
df = st.data_editor(df, key="table", disabled=lockL, column_config=column_config)

# Submit
def save(df):
    global path
    for col in date_cols:
        df[col] = df[col].apply(lambda x: str(x).replace('-',''))
    df["BMI"] = df["BW"]/((df["BH"]+1e-10)*0.01)**2
    df.to_csv(path, index=False)
st.button("save", key=f"save_btn", on_click=save, args=(df,))
st.write(f"table shape = {df.shape}")
st.divider()

# stats
st.subheader("Image data")
imageD = {}
for disease in utils.diseaseD:
    imageD[disease] = [ utils.diseaseD[disease], len(glob.glob(f"{data_path}/export_img/{disease}/*.jpg")) ]
df_image = pd.DataFrame(imageD)
df_image.rename(index={0:"Chinese", 1:"Counts"}, inplace=True)
st.dataframe(df_image)

# barrier
time.sleep(86400)