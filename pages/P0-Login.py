import os, json
import streamlit as st
import yaml
import utils

print("-"*25+"P0"+"-"*25)

# load config
cfg = yaml.safe_load(open('config.yaml', 'r'))

# About Sessions and Cookies
comments = """
1 st.session_state is empty initially, do not use it for login since data will be eradicated after refreshing
2 after using CookieManager, there are two keys stores in cookie
    + ajs_anonymous_id: depends on browser user, keep while redirecting, keep while refreshing
    + _xsrf: refresh page: depends on browser user, keep while redirecting, change while refreshing
3 Needs session.json additionally
    + session.json stores (ajs_anonymous_id,) that user login sucessfully
    + cookies stores (ajs_anonymous_id,)
4 methods of cookie_manager
    + get_all(), get(key), set(key,value), delete(key)
"""
session, ajs = utils.get_session_ajs()
if ajs in session: # login
    if st.button("Logout"):
        session.pop(ajs)
        json.dump(session, open("session.json","w"))
        utils.nav_page("P0-Login")
else:
    # init folders
    for hos in cfg['hospitals']:
        os.makedirs(f"{cfg['data_path']}/data/{hos}/.tmp", exist_ok=True)
        for disease in utils.diseaseD.keys():
            os.makedirs(f"{cfg['data_path']}/data/{hos}/export_img/{disease}", exist_ok=True)
        os.makedirs(f"{cfg['data_path']}/data/{hos}/export_tab", exist_ok=True)

    # title
    title = f"<h1 style='text-align: center'> 癢症資料收集系統 </h1>"
    st.markdown(title, unsafe_allow_html=True)

    # login
    hospital = st.selectbox("Hospital", options=[""]+cfg["hospitals"])
    if hospital:
        account = st.text_input("Account", max_chars=100, value=cfg["account"] if cfg["autofill"] else "")
        password = st.text_input("Passward", max_chars=100, value=cfg["password"] if cfg["autofill"] else "", type="password")
        submit = st.button("Login")
        if submit:
            if account==cfg["account"] and password==cfg["password"]:
                session[ajs] = hospital
                json.dump(session, open("session.json","w"))
                utils.nav_page("P1-Patient-Filling")
            else:
                st.error(":red[Incorrect Account or Passward]")