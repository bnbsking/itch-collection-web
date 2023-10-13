import os
import streamlit as st
import yaml
import utils
import extra_streamlit_components as stx

print("-"*25+"P0"+"-"*25)

# load config
cfg = yaml.safe_load(open('config.yaml', 'r'))

# About Sessions and Cookies
comments = """
1 st.session_state is empty initially, do not use it for login since data will be eradicated after refreshing
2 after using CookieManager, server generate session_id for client
3 Needs session.json additionally
    + session.json stores (ajs_anonymous_id,) that user login sucessfully
    + cookies stores (ajs_anonymous_id,)
4 methods of cookie_manager
    + get_all(), get(key), set(key,value), delete(key)
    + set and delete should time.sleep(0.5) afterwards
5. cookieManager cannot be initailized two times in a script even if del and st.session_state,
pass into function as args instead. (Global manager in utils cannot be updated)
"""
try:
    cookie_manager = stx.CookieManager()
except:
    utils.nav_page("P0-Login")

if utils.isLogin(cookie_manager):
    if st.button("Logout"):
        utils.logout(cookie_manager)
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
                utils.login(cookie_manager, hospital)
                utils.nav_page("P1-Patient-Filling") # not work after setting cookie
            else:
                st.error(":red[Incorrect Account or Passward]")