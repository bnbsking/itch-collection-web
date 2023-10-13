### Installation
+ Python 3+: [Miniconda3](https://docs.conda.io/projects/miniconda/en/latest/)
+ Open terminal then install the following package
    + pip
        ```bash
        pip install streamlit pandas numpy opencv-python pyyaml extra-streamlit-components unidecode
        ```
+ Download the code to a folder
    + method 1
        ```bash
        git clone https://github.com/bnbsking/itch-collection-web.git
        ```
    + method 2
        + Download by zip (Remember to check the correctness of Chinese format after extracting)


### Quick start
+ method 1: script (Linux/MacOS only)
    ```bash
    ./start.sh
    ```
+ method 2: commands
    ```bash
    ipconfig # "ipconfig" is for windows, "ifconfig" is for Linux/MacOS
    streamlit run main.py  --server.address 0.0.0.0
    ```
It will show the ip address of the web server. To connect to the server by another device, type the "ip:8501" on the web address bar then enter it.


### File structure
+ start.sh | start the web server
+ main.py | auto nevigate to P0-Login.py
+ utils.py | some functions
+ pages/
    + P0-Login.py | Select hospital and login / logout
    + P1-Patient-Filling.py
    + P2-Doctor-Filling-A.py | Collect images 
    + P3-Doctor-Filling-B.py | Collect reset columns
    + P4-Table.py | Editable tabular data for all patients and Non-editable images stats
    + cdm.csv | common data model of each columns
+ data/
    + VGHKS/ or EDA/ or KCGMH/ or  KMU/ | hospital name
        + .tmp/ | Uploaded images. Can be previewed and deleted by web
            + patient_data.json | Generated after P1. Note that submit at P1 again will **replace** this file. Be deleted after P2
            + \<hospital_name\>\_\<date\>\_\<patient_id\>\_\<disease\>.json | Generated after P2. Note that submit at P2 again will **keep** this file. Be deleted after P3
            + *.jpg | Generated in P2 and be moved to export_img/ (if checked) or be deleted (if not checked) after submitting
        + export_img/ | Exported images. Cannot be previewed or deleted by web
            + Atopic-Dermatitis/*.jpg
            + Contact-Dermatitis/*.jpg
            + Fixed-drug-eruption/*.jpg
            + Fungal-disease/*.jpg
            + Insect-Bites-or-Scables-or-Others/*.jpg
            + Psoriasis/*.jpg
            + Urticaria/*.jpg
        + export_tab/
            + data.csv | Exported Tabular data. Can be edited in P4
+ show/*.png | pages
+ config.yaml | configuration include login information
+ session.json | store login permission and data of clients for the web server


### Deploy notes
+ config.yaml
    + autofill must be false


### Pages
Login Page
![Login Page](show/p0.png)
First Page
![First Page](show/p1.png)
Second Page
![Second Page](show/p2.png)
Third Page
![Third Page](show/p3.png)
Fourth Page
![Fourth Page](show/p4.png)
