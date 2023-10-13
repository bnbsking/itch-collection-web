from streamlit.components.v1 import html
import extra_streamlit_components as stx
import json, random, time

id_chars = "".join(map(str,range(10))) + "".join( chr(ord('a')+i) for i in range(26) )

def isLogin(cookie_manager):
    session_id = cookie_manager.get("session_id")
    time.sleep(0.5)
    session = json.load(open("session.json","r"))
    return session_id in session

def login(cookie_manager, hospital):
    session_id = "".join( random.choice(id_chars) for _ in range(32) )
    cookie_manager.set("session_id", session_id)
    time.sleep(0.5)
    session = json.load(open("session.json","r"))
    session[session_id] = hospital
    json.dump(session, open("session.json", "w"))

def logout(cookie_manager):
    session_id = cookie_manager.get("session_id")
    cookie_manager.delete("session_id")
    time.sleep(0.5)
    session = json.load(open("session.json","r"))
    session.pop(session_id)
    json.dump(session, open("session.json", "w"))

def getHospital(cookie_manager):
    session_id = cookie_manager.get("session_id")
    session = json.load(open("session.json","r"))
    return session[session_id]

diseaseD = {
    "Atopic-Dermatitis": "過敏性皮膚炎",
    "Contact-Dermatitis": "接觸性皮膚炎",
    "Fixed-drug-eruption": "固定性藥物疹",
    "Fungal-disease": "真菌感染疾病",
    "Psoriasis": "乾癬",
    "Urticaria": "蕁麻疹",
    "Insect-Bites-or-Scables": "蟲咬或疥瘡",
    "Others": "其他"
}

def nav_page(page_name, timeout_secs=3):
    # https://github.com/streamlit/streamlit/issues/4832
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click(); // click here
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

def alert(msg):
    alert_script = """
    <script type="text/javascript">
        alert("%s");
        </script>
    """ % (msg,)
    html(alert_script)

DLQI = {
    "1.上週內，你的皮膚的搔癢或疼痛（包括酸痛、刺痛等等）的症狀重嗎？": ["非常嚴重", "嚴重", "較輕", "無"],
    "2.上週內，你的皮膚病變有多少次讓你覺察或讓你感到尷尬？": ["非常嚴重", "嚴重", "較輕", "無"],
    "3.上週內，你的皮膚病變在多大程度上影響了購物、家務或園藝活動？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "4.上週內，你的皮膚病變在多大程度上影響了你的穿著？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "5.上週內，你的皮膚病變在多大程度上影響了你的社交或休閒活動？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "6.上週內，你的皮膚病變在多大程度上讓運動變得困難？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "7.上週內，你的皮膚病變使你妨礙工作或學習？": ["是","否","不相關"],
    "如果“否”，上週的工作或學習中，你的皮膚病變對你造成了多大的困擾？如果上題選“是”，這題請選“無”": ["嚴重","較輕","無"],
    "8.上週內，你的皮膚病變在多大程度上給你的同伴、親密朋友或家人帶來麻煩？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "9.上週內，你的皮膚病變在多大程度上造成性生活的困難？": ["非常嚴重", "嚴重", "較輕", "無", "不相關"],
    "10.上週內，治療過程中有多大的困難？例如使家中變得不潔淨或耽誤時間": ["非常嚴重", "嚴重", "較輕", "無", "不相關"]
}
