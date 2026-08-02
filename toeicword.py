import streamlit as st
from gtts import gTTS
from io import BytesIO

# --- 1. 頁面基本設定 ---
st.set_page_config(
    page_title="英語單字學習程式",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 自訂 CSS 樣式 (極致緊湊、手機全螢幕顯示) ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .main-word {
        font-size: 2rem;
        font-weight: bold;
        color: #90CAF9;
        text-align: center;
        margin-bottom: 2px !important;
        line-height: 1.1;
    }
    .pos-text {
        font-size: 1rem;
        color: #B0BEC5;
        text-align: center;
        margin-bottom: 3px !important;
    }
    .mean-text {
        font-size: 1.3rem;
        font-weight: bold;
        color: #FFAB91;
        text-align: center;
        margin-bottom: 5px !important;
        line-height: 1.2;
    }
    .sentence-box {
        background-color: #1E1E1E;
        padding: 8px 10px;
        border-radius: 6px;
        text-align: left;
        color: #CFD8DC;
        font-size: 0.9rem;
        margin-bottom: 6px !important;
        line-height: 1.2;
    }
    .stButton>button {
        width: 100%;
        height: 2.3em;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 6px;
        padding: 0px;
    }
    hr {
        margin: 5px 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 完整英文單字資料庫 ---
verb_db = [
    ["1", "company", "(n.)", "公司;陪伴", "She works for a tech company in the Bay Area as an engineer.", "她在灣區的一家科技公司擔任工程師。"],
    ["2", "passenger", "(n.)", "乘客", "All passengers should wear a mask on the train.", "所有乘客在火車上都應佩戴口罩。"],
    ["3", "subject", "(n.)", "主題", "The professor discussed various subjects in the lecture.", "教授在演講中討論了好幾個主題。"],
    ["4", "area", "(n.)", "地區;領域", "This building is located in a busy commercial area.", "這棟建築位於繁忙的商業區。"],
    ["5", "cashier", "(n.)", "收銀員", "The cashier will help you with the return process.", "收銀員會協助您完成退貨流程。"],
    ["6", "amount", "(n.)", "數量;總額", "The amount of work I got for the quarter is ridiculous!", "我這個季度的工作量太荒謬了!"],
    ["7", "clinic", "(n.)", "診所", "I'm going to the clinic to get a flu shot.", "我要去診所打流感疫苗。"],
    ["8", "fee", "(n.)", "費用;服務費用", "There is an admission fee for the museum.", "博物館有入場費。"],
    ["9", "appointment", "(n.)", "預約;任命,委派", "I'll miss the meeting due to a doctor's appointment.", "因為預約要看醫生,這次開會我會缺席。"],
    ["10", "reservation", "(n.)", "預訂;保護區", "I'd like to make a reservation for eight people at 6 tonight.", "我想預訂今晚六點八人的位子。"],
    ["11", "employee", "(n.)", "員工;受雇者", "The employee received a promotion for his hard work.", "這位員工因工作努力而獲得了晉升。"],
    ["12", "task", "(n.)", "任務;工作", "He has been assigned a challenging task.", "他被分配了一項有挑戰性的任務。"],
    ["13", "label", "(n.)", "標籤;品牌", "The label on the package indicates the contents.", "包裝上的標籤標明了內容物。"],
    ["14", "lobby", "(n.)", "大廳;門廊", "I met him in the hotel lobby last Monday.", "我上星期一在飯店大廳遇見了他。"],
    ["15", "option", "(n.)", "選項;選擇", "Students at the school have the option of studying abroad.", "這所學校的學生有出國留學的選項。"],
    ["16", "receipt", "(n.)", "收據;收到", "Don't forget to keep the receipt for your purchase.", "別忘記保留購物收據。"],
    ["17", "printer", "(n.)", "印表機", "The office printer needs more paper and toner.", "辦公室的印表機需要更多紙張和碳粉。"],
    ["18", "pharmacy", "(n.)", "藥房;藥局", "You can pick up your medicines at the pharmacy next door.", "您可以在隔壁的藥房取藥。"],
    ["19", "destination", "(n.)", "目的地;終點", "Paris is a popular tourist destination in Europe.", "巴黎是歐洲著名的旅遊勝地。"],
    ["20", "goal", "(n.)", "目標", "His goal was to get into Harvard University.", "他的目標是進入哈佛大學。"],
    ["21", "author", "(n.)", "作者", "He is the author of several best-selling novels.", "他是寫了幾本暢銷小說的作者。"],
    ["22", "description", "(n.)", "描述", "The catalog gives a full description of each product.", "目錄中對每件產品都有完整的描述。"],
    ["23", "reminder", "(n.)", "提醒;提示", "This is a friendly reminder that smoking is prohibited.", "友善提醒一下這裡禁菸。"],
    ["24", "goods", "(n.)", "商品;貨物", "The store sells various goods, including clothing.", "這家商店出售包括服裝在內的各種商品。"],
    ["25", "flight", "(n.)", "班機;航程", "I booked a flight to London for next week.", "我訂了下週飛往倫敦的機票。"],
    ["26", "brand", "(n.)", "品牌", "The advertisement effectively promoted the brand.", "那支廣告替該品牌做了有效的宣傳。"],
    ["27", "vehicle", "(n.)", "車輛;交通工具", "The road is closed to all vehicles. We'll need to walk.", "道路對所有車輛關閉。我們需要步行前往。"],
    ["28", "site", "(n.)", "地點;場所", "The construction site is located downtown.", "施工地點位於市中心。"],
    ["29", "occupation", "(n.)", "職業", "Teaching is a rewarding occupation.", "教學是一項令人滿足的職業。"],
    ["30", "payment", "(n.)", "支付;支付款項", "Please make the payment before the due date.", "請在截止日期前付款。"],
    ["31", "account", "(n.)", "帳戶;描述;客戶", "You'll need to bring your passport to open a new account.", "您需要帶護照來開立新帳戶。"],
    ["32", "region", "(n.)", "區域;地區", "The company operates in several regions around the world.", "該公司在全球多個地區營運。"],
    ["33", "receptionist", "(n.)", "接待人員", "The receptionist greeted visitors at the company's main entrance.", "接待員在公司大門口迎接訪客。"],
    ["34", "Volume", "(n.)", "音量;量;(書)冊", "I can't hear the music. Can you turn up the volume?", "我聽不到音樂。你可以把音量調大聲一點嗎?"],
    ["35", "item", "(n.)", "項目;品項", "Let's move on to the last item on the agenda.", "我們接著來討論議程上的最後一個項目吧。"],
    ["36", "department", "(n.)", "部門", "She works in the marketing department of the company.", "她在公司的行銷部工作。"],
    ["37", "situation", "(n.)", "狀況;處境", "The situation got so bad that they had to call the police.", "狀況惡化到他們不得不報警。"],
    ["38", "audience", "(n.)", "聽眾;觀眾", "Please rewrite the speech for the younger audience.", "請為年輕聽眾改寫演講稿。"],
    ["39", "client", "(n.)", "客戶;顧客", "The company provides excellent service to its clients.", "該公司為客戶提供一流的服務。"],
    ["40", "fare", "(n.)", "車票價;車資", "How much is the fare to Kaohsiung?", "到高雄的車票要多少錢?"],
    ["41", "staff", "(n.)", "全體員工", "The staff is working hard to meet the deadline.", "全體員工正在努力趕在期限前完成工作。"],
    ["42", "permission", "(n.)", "允許;同意", "You must ask for permission if you want to leave early.", "你必須徵得同意才可以早退。"],
    ["43", "income", "(n.)", "收入", "He earns a high income from his successful business.", "他從成功的生意中賺取高收入。"],
    ["44", "period", "(n.)", "一段時期", "The company plans to extend the trial period of the product.", "公司計劃延長這項產品的試用期。"],
    ["45", "equipment", "(n.)", "設備;裝備", "The lab has state-of-the-art equipment.", "實驗室擁有最先進的設備。"],
    ["46", "attendance", "(n.)", "出席;出席人數", "Attendance is required for this evening's meeting.", "今晚的會議一定要出席。"],
    ["47", "software", "(n.)", "軟體", "The company released new accounting software last month.", "這家公司上個月發布了新的會計軟體。"],
    ["48", "material", "(n.)", "材料;原料", "The table is made of sturdy and durable materials.", "這張桌子是用堅固耐用的材料制成的。"],
    ["49", "route", "(n.)", "路線;途徑", "She took the scenic route to San Francisco.", "她選擇了風景優美的路線前往舊金山。"],
    ["50", "response", "(n.)", "回答;回應", "His response to the question was concise and clear.", "他對問題的回答簡明扼要。"],
    ["51", "sum", "(n.)", "金額;總數", "Huge sums of money are spent on national defense.", "巨額的錢財都投入到國防上。"],
    ["52", "wage", "(n.)", "工資;薪水", "The job pays very low hourly wages.", "這份工作的時薪非常低。"],
    ["53", "fuel", "(n.)", "燃料", "I'd like my next car to have the best fuel efficiency.", "我希望我的下一輛車是最省燃料的。"],
    ["54", "decision", "(n.)", "決定", "The decision to expand the business was strategic.", "將業務擴大的決定是策略性的。"],
    ["55", "energy", "(n.)", "能源;精力", "Renewable energy sources are becoming increasingly popular.", "可再生能源正變得越來越受歡迎。"],
    ["56", "section", "(n.)", "部分;區域", "The book is divided into sections.", "這本書被分為幾個部分。"],
    ["57", "purpose", "(n.)", "目的", "The purpose of the meeting is to discuss student progress.", "會議的目的是討論學生的進展。"],
    ["58", "selection", "(n.)", "選擇;挑選", "The selection process for the job will begin next week.", "這份工作的選拔過程將於下週開始。"],
    ["59", "opportunity", "(n.)", "機會;良機", "Some opportunities only come once in a lifetime.", "有些機會一生只有一次。"],
    ["60", "sample", "(n.)", "樣品;樣本", "The store offers free samples of its new products.", "這間商店提供其新產品的免費樣品。"],
    ["61", "quantity", "(n.)", "數量", "Please specify the quantity of items you need to order.", "請註明您需要訂購的商品數量。"],
    ["62", "method", "(n.)", "方法;方式", "The teacher explained the scientific method to the students.", "老師向學生們講解科學方法。"],
    ["63", "data", "(n.)", "數據;資料", "We still need to analyze the data.", "我們還需要分析數據。"],
    ["64", "pollution", "(n.)", "污染", "Air pollution is a major concern in urban areas.", "空氣污染是都市地區的重大問題。"],
    ["65", "article", "(n.)", "新聞報導;文章", "The newspaper apologized for the misleading article.", "該報為誤導性文章道歉。"],
    ["66", "theme", "(n.)", "主題", "The theme of the party is \"Under the Sea.\"", "派對的主題是「海底世界」。"],
    ["67", "condition", "(n.)", "狀態;狀況;條件", "The company, although new, is in very good condition.", "這家公司雖然很新,但狀態很好。"],
    ["68", "departure", "(n.)", "出發;離開", "The flight's departure was delayed due to weather.", "由於天氣因素,航班延遲起飛。"],
    ["69", "emergency", "(n.)", "緊急情況", "In case of an emergency, please call the emergency hotline.", "如遇緊急情況,請撥打緊急專線。"],
    ["70", "figure", "(n.)", "數字;圖表;人物", "He earns a six-figure salary.", "他賺六位數的薪水。"],
    ["71", "solution", "(n.)", "解決方案", "The team worked together to find a solution to the problem.", "團隊共同努力尋求解決問題的方法。"],
    ["72", "device", "(n.)", "裝置;手段", "The new app might not be compatible with an old device.", "新的APP可能跟舊的機子不兼容。"],
    ["73", "confidence", "(n.)", "信心;把握", "Confidence plays a key role in a successful interview.", "自信在成功的面試中起著關鍵作用。"],
    ["74", "district", "(n.)", "區域", "Our office is located in the downtown district.", "我們的辦公室位於市中心區。"],
    ["75", "status", "(n.)", "狀態;身分地位", "The project is currently in a pending status.", "專案目前處於有待確定的狀態。"],
    ["76", "source", "(n.)", "來源", "They traced the source of the problem to a faulty wire.", "他們追查到問題的來源是一根故障的電線。"],
    ["77", "career", "(n.)", "職業生涯", "She has had a successful career in the fashion industry.", "她在時尚界事業有成。"],
    ["78", "instruction", "(n.)", "指示;教導", "You'll be fine if you follow your manager's instructions.", "如果你聽從經理的指示,你會沒事的。"],
    ["79", "insurance", "(n.)", "保險", "Our employees are all entitled to receive health insurance.", "我們的員工都有權享有健康保險。"],
    ["80", "growth", "(n.)", "成長;增長", "The company has experienced significant growth in sales.", "公司的銷售額有顯著的成長。"],
    ["81", "charity", "(n.)", "慈善;公益", "The company made a generous donation to charity.", "那家公司向慈善機構慷慨捐贈。"],
    ["82", "property", "(n.)", "所有物;房地產", "We are not responsible for any loss of personal property.", "我們不承擔個人所有物遺失的責任。"],
    ["83", "variety", "(n.)", "各式各樣;多樣性", "They put out a variety of snacks in the office every day.", "他們每天在辦公室擺出各式各樣的零食。"],
    ["84", "accommodation", "(n.)", "住宿", "Accommodations will be provided for the business trip.", "出差期間將提供住宿。"],
    ["85", "admission", "(n.)", "入場費;准許進入", "Admission is free for children under 12.", "12歲以下兒童免費入場。"],
    ["86", "customs", "(n.)", "海關", "The shipment was delayed at customs for inspection.", "貨物因在海關檢查而延誤。"],
    ["87", "beverage", "(n.)", "飲料", "The office always has free snacks and beverages.", "辦公室總是有免費的點心和飲料。"],
    ["88", "anniversary", "(n.)", "周年紀念日", "The store is having a big sale to celebrate its anniversary.", "這家商店為了慶祝周年紀念日有促銷活動。"],
    ["89", "expert", "(n.)", "專家", "He is an expert in his field and is highly respected.", "他是所在領域的專家,並且備受尊敬。"],
    ["90", "sequence", "(n.)", "順序;一連串", "The steps must be followed in a specific sequence.", "這些步驟必須按照特定的順序執行。"],
    ["91", "colleague", "(n.)", "同事", "She was recommended for the position by a colleague.", "她是同事推薦來做這個職位的。"],
    ["92", "spreadsheet", "(n.)", "試算表", "The accountant updated the financial data in the spreadsheet.", "會計師在試算表中更新了財務數據。"],
    ["93", "advantage", "(n.)", "優勢;好處", "The agreement is to our advantage.", "這個協議對我們有優勢。"],
    ["94", "currency", "(n.)", "貨幣", "I need to exchange my currency for the local one.", "我需要將錢兌換成當地貨幣。"],
    ["95", "facility", "(n.)", "設施;(特定用途)場所", "The theme park is the area's most popular tourist facility.", "那個主題公園是那一帶最受歡迎的旅遊設施。"],
    ["96", "complaint", "(n.)", "客訴;投訴", "The customer filed a complaint about the faulty product.", "客戶對有問題的產品提出投訴。"],
    ["97", "venue", "(n.)", "會場;舉辦地點", "The concert will be held at a popular venue in the city.", "演唱會將在市內一個熱門場所舉行。"],
    ["98", "supplier", "(n.)", "供應商", "We have a reliable supplier for our raw materials.", "我們有一個可靠的原料供應商。"],
    ["99", "announcement", "(n.)", "公告;聲明", "The manager sends out weekly announcements every Monday.", "經理每週一都會發送每週公告。"],
    ["100", "terminal", "(n.)", "航廈;終端機", "The passengers waited at the terminal for their flight.", "乘客在航廈等待他們的航班。"],
    ["101", "warehouse", "(n.)", "倉庫", "The company stores its products in a large warehouse.", "公司將其產品收存在一座大型倉庫中。"],
    ["102", "standard", "(n.)", "標準(adj.)標準的", "His work is not up to standard.", "他的工作表現沒有達到標準。"],
]

# --- 4. 初始化 Session State ---
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'start_no' not in st.session_state:
    st.session_state.start_no = 1

# --- 5. 語音生成函數 ---
def get_audio_bytes(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

# --- 6. 介面佈局 ---
col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    start_input = st.number_input("起始編號：", min_value=1, max_value=len(verb_db), value=st.session_state.start_no, label_visibility="collapsed")
with col_s2:
    if st.button("設定/重置"):
        st.session_state.index = int(start_input) - 1
        st.session_state.start_no = int(start_input)
        st.session_state.show_answer = False
        st.rerun()

st.markdown("---")

current_data = verb_db[st.session_state.index]
no, word, pos, mean, sen_en, sen_zh = current_data

st.markdown(f"**進度：{no} / {len(verb_db)} 筆**")

st.markdown(f'<div class="main-word">{word}</div>', unsafe_allow_html=True)

audio_bytes = get_audio_bytes(word)
if audio_bytes:
    st.audio(audio_bytes, format='audio/mp3', autoplay=True)

if st.session_state.show_answer:
    st.markdown(f'<div class="pos-text">{pos}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="mean-text">{mean}</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sentence-box">
            <b>例句：</b>{sen_en}<br>
            <b>翻譯：</b>{sen_zh}
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 調整按鈕佈局：若尚未顯示答案，按鈕佔滿整行；若已顯示答案，則分左右各半
if not st.session_state.show_answer:
    if st.button("👁️ 顯示答案", type="primary"):
        st.session_state.show_answer = True
        st.rerun()
else:
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 重新播放"):
            st.rerun()
    with col_btn2:
        if st.button("➡️ 下一題", type="primary"):
            if st.session_state.index < len(verb_db) - 1:
                st.session_state.index += 1
                st.session_state.show_answer = False
                st.rerun()
            else:
                st.success("🎉 複習完畢！")
