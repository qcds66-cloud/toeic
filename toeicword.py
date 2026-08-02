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
    ["103", "minimum", "(n.)", "最小值;最低限度(adj.)最小的;最低限度的", "I must get a minimum of 40 questions right to pass the exam.", "我必須至少答對40題才能通過考試。"],
    ["104", "budget", "(n.)", "預算;預算方案(adj.)低廉的", "The department gets a small amount of the annual budget.", "該部門獲得少量年度預算。"],
    ["105", "manual", "(n.)", "手冊;指南(adj.)用手操作的", "The employee received a manual with instructions for the task.", "這名員工拿到一份包含任務說明的手冊。"],
    ["106", "result", "(n.)", "結果;成果(v.)發生;導致", "The promotional campaign produced excellent results.", "這次促銷活動產出了極佳的成效。"],
    ["107", "experience", "(n.)", "經驗;經歷(v.)經歷;體驗到", "The position requires three years of relevant work experience.", "那個職位要求三年的相關工作經驗。"],
    ["108", "form", "(n.)", "表格(v.)形成", "Please attach a recent photo to your application form.", "請在您的申請表格中附上一張近期照片。"],
    ["109", "tour", "(n.)", "參觀;遊覽(v.)參觀;遊覽", "We went on a guided tour of the historical city.", "我們參加了古城的導覽之旅。"],
    ["110", "award", "(n.)", "獎(v.)授予", "The company gives out awards at the end of the year.", "公司在年終時頒獎。"],
    ["111", "tax", "(n.)", "稅;稅金(v.)向 課稅", "They're increasing the tax on cigarettes.", "他們會提高菸草稅。"],
    ["112", "discount", "(n.)", "打折;折扣(v.)打折", "The store is offering a discount on all items this weekend.", "這家商店本週末打折促銷所有商品。"],
    ["113", "target", "(n.)", "目標(v.)把…作為目標(或對象)", "We need to change our target market to the 35-45 age groups.", "我們需要將目標市場改為35至45歲的年齡族群。"],
    ["114", "request", "(n.)", "請求;要求(v.)請求;要求", "He made a formal request for a leave of absence.", "他提出休假的正式請求。"],
    ["115", "aim", "(n.)", "目標(v.)打算;旨在", "Our aim is to increase sales by 10% in the next quarter.", "我們的目標是在下一季度將銷售額提高10%。"],
    ["116", "trade", "(n.)", "貿易;生意(v.)做買賣;交換", "Seventy percent of the country's trade is with Europe.", "該國70%的貿易是和歐洲進行的。"],
    ["117", "display", "(n.)", "展示;展覽;顯示(v.)陳列;顯示", "Her paintings will be on display at the gallery next month.", "她的畫作將於下個月在畫廊展出。"],
    ["118", "power", "(n.)", "電力;動力;權力(v.)驅動", "There was a power outage last night in the city.", "昨晚城裡停電了。"],
    ["119", "aid", "(n.)", "協助;輔助物(v.)協助", "The organization provides aid to people affected by the flood.", "該組織為受洪水影響的人們提供援助。"],
    ["120", "refund", "(n.)", "退款(v.)退款", "The item arrived too late. I'd like to get a refund.", "商品送達得太晚了,我要辦理退款。"],
    ["121", "lack", "(n.)", "缺乏;缺少(v.)缺乏;缺少", "The project was delayed due to a lack of resources.", "專案由於缺乏資源而延遲了。"],
    ["122", "process", "(n.)", "過程(v.)處理", "We are in the process of reviewing your feedback.", "我們正在審閱您的反饋意見。"],
    ["123", "loan", "(n.)", "貸款;借出(v.)借貸", "She applied for a loan to start her own business.", "她為了創業去申請貸款。"],
    ["124", "demand", "(n.)", "需求;需求量(v.)要求", "There is a high demand for the new product in the market.", "市場對新產品的需求量很高。"],
    ["125", "progress", "(n.)", "進展;進步(v.)進展;進步", "Our team has made significant progress on the project.", "我們團隊在專案上有重大進展。"],
    ["126", "network", "(n.)", "網絡;人際網絡(v.)建立關係", "The company expanded its distribution network across Asia.", "該公司擴展了在亞洲各地的分銷網絡。"],
    ["127", "survey", "(n.)", "調查(v.)調查", "We are conducting a survey to collect customers' feedback.", "我們正在進行一項調查以收集客戶的反饋。"],
    ["128", "range", "(n.)", "範圍;系列(v.)涉及………範圍", "The new product has a wide range of applications.", "這款新產品的應用範圍很廣。"],
    ["129", "experiment", "(n.)", "實驗;試驗(v.)實驗;試驗", "The scientist conducted an experiment to test their hypothesis.", "科學家進行了一場實驗來驗證他們的假設。"],
    ["130", "bargain", "(n.)", "折扣品;交易(v.)討價還價", "The client drove a hard bargain with the company.", "客戶與公司進行了艱難的討價還價。"],
    ["131", "draft", "(n.)", "草稿;匯票(v.)起草", "I finally finished the first draft of my dissertation.", "我終於完成了論文的初稿。"],
    ["132", "research", "(n.)", "研究;調查(v.)研究;調查", "I conducted research to gather data for my project.", "我做了一些研究以收集專案所需的數據。"],
    ["133", "raise", "(n.)", "加薪(v.)提高;引起", "He did not get a raise this year.", "他今年沒有得到加薪。"],
    ["134", "project", "(n.)", "專案;專題研究(v.)預計;預估", "The construction project will start next month.", "該建設項目將於下個月開始。"],
    ["135", "private", "(adj.)", "私人的;私立的", "They had a private conversation in the office.", "他們在辦公室進行私人談話。"],
    ["136", "personal", "(adj.)", "個人的", "She packed up her personal belongings and left.", "她收拾好個人物品後就離開了。"],
    ["137", "common", "(adj.)", "普遍的;共同的", "Chen is a fairly common family name in Taiwan.", "陳在台灣是一個相當普遍的姓氏。"],
    ["138", "regular", "(adj.)", "定期的;經常的", "They have regular meetings to discuss project updates.", "他們定期開會討論專案的最新狀況。"],
    ["139", "major", "(adj.)", "主要的;重大的", "Tokyo and New York are major financial centers.", "東京和紐約都是主要的金融中心。"],
    ["140", "vailable", "(adj.)", "(人)有空的;(物)可取得的", "Let's schedule an interview. When are you available?", "我們來安排一場面試吧。你什麼時候有空?"],
    ["141", "negative", "(adj.)", "負面的;消極的", "The company received negative feedback from its customers.", "公司收到了客戶的負面反饋。"],
    ["142", "temporary", "(adj.)", "暫時的;臨時的", "I am currently working in a temporary position.", "我目前正在一個臨時職位上工作。"],
    ["143", "primary", "(adj.)", "主要的;最初的", "English is the primary language in many countries.", "英語是許多國家的主要語言。"],
    ["144", "typical", "(adj.)", "典型的", "Typical symptoms include headaches, vomiting, and dizziness.", "典型的症狀包括頭痛、嘔吐和眩暈。"],
    ["145", "limited", "(adj.)", "有限的;限定的", "The company has limited resources to invest in new projects.", "公司能用來投資新項目的資源有限。"],
    ["146", "physical", "(adj.)", "身體的;生理的", "Regular exercise is important for maintaining physical health.", "經常運動對保持身體健康很重要。"],
    ["147", "annual", "(adj.)", "一年一次的;每年的", "Our company is having the annual end-of-year party today.", "我們公司今天要舉行一年一度的年終晚會。"],
    ["148", "frequent", "(adj.)", "頻繁的", "He travels to New York on frequent business trips.", "他經常去紐約出差。"],
    ["149", "various", "(adj.)", "各式各樣的;多種多樣的", "The hat is available in various colors.", "這頂帽子有各式各樣的顏色可供選擇。"],
    ["150", "suitable", "(adj.)", "合適的", "This movie is not suitable for children.", "這部電影不適宜兒童觀看。"],
    ["151", "practical", "(adj.)", "實際的;實用的", "Practical experience is important for learning a new skill.", "實際經驗對於學習新技能來說很重要。"],
    ["152", "due", "(adj.)", "到期的;應支付的", "The assignment is due tomorrow.", "這個作業的繳交日期是明天。"],
    ["153", "legal", "(adj.)", "合法的;法律的", "Marijuana is legal in some states in the US, but not all.", "大麻在美國的一些州是合法的,但不是所有的州。"],
    ["154", "traditional", "(adj.)", "傳統的", "The dancers were wearing traditional Hungarian costumes.", "舞者身穿傳統匈牙利服裝。"],
    ["155", "portable", "(adj.)", "便於攜帶的", "The laptop is lightweight and highly portable.", "這台筆記型電腦重量輕,便於攜帶。"],
    ["156", "harmful", "(adj.)", "有害的", "Smoking is harmful to your health.", "吸菸有害健康。"],
    ["157", "entire", "(adj.)", "全部的;整個的", "He read the entire book in just one day.", "他僅用一天時間就讀完了整本書。"],
    ["158", "stable", "(adj.)", "穩定的;穩固的", "She has a stable job with a steady income.", "她有一份穩定的工作,收入穩定。"],
    ["159", "optimistic", "(adj.)", "樂觀的", "Despite the challenges, she remains optimistic about the future.", "儘管困難重重,她對未來仍然保持樂觀。"],
    ["160", "capable", "(adj.)", "有能力的;能幹的", "He is a capable leader who can handle challenges well.", "他是一位有能力的領導者,擅長應對挑戰。"],
    ["161", "unlikely", "(adj.)", "不太可能的", "Let's face it. The team is most unlikely to win.", "面對現實吧,這隻球隊不太可能赢的。"],
    ["162", "detailed", "(adj.)", "詳細的", "Detailed instructions will be provided upon arrival.", "詳細說明將在抵達時提供。"],
    ["163", "obvious", "(adj.)", "明顯的;顯然的", "It's obvious that she's not happy with the decision.", "她明顯對這個決定感到不滿意。"],
    ["164", "aware", "(adj.)", "察覺的;知道的", "I am aware of the awkward vibes in the office.", "我察覺到辦公室裡的尷尬氣氛。"],
    ["165", "local", "(adj.)", "當地的(n.)當地人", "My article was published in the local newspaper.", "我的文章被登在當地的報紙上。"],
    ["166", "original", "(adj.)", "最初的;原作的;獨創的(n.)原稿;原作", "The original plan for the project has been modified.", "專案的最初計劃已被修改。"],
    ["167", "spare", "(adj.)", "多餘的;剩下的(n.)備用品;備件", "I have a spare pen you can borrow if you need it.", "如果你需要,我有多的筆可以借你。"],
    ["168", "present", "(adj.)", "現在的;在場的(v.)授予;提交", "This is the present situation we're facing.", "這就是我們目前面臨的情況。"],
    ["169", "secure", "(adj.)", "安全的;牢固的(v.)使安全;設法得到", "Please make sure to keep your personal information secure.", "請務必確保您的個人資訊安全。"],
    ["170", "initial", "(adj.)", "最初的(v.)簽全名的首字母", "The project is still in its initial stages of development.", "專案仍處於發展的初步階段。"],
    ["171", "immediately", "(adv.)", "立刻", "The new rules will be implemented immediately.", "新規則將立刻實施。"],
    ["172", "nearly", "(adv.)", "幾乎;差不多", "We are nearly finished with the project.", "我們快要完成這則專案了。"],
    ["173", "save", "(v.)", "儲存;省下;挽救", "She managed to save enough money to buy a car.", "她設法存夠錢,買了一輛車。"],
    ["174", "invite", "(v.)", "邀請", "Let's invite them over for dinner.", "我們請他們過來吃晚飯吧。"],
    ["175", "download", "(v.)", "下載", "Please download the latest version of the software.", "請下載最新版本的軟體。"],
    ["176", "attend", "(v.)", "參加;出席", "He did not attend the meeting yesterday due to a headache.", "由於頭痛,他昨天沒有參加會議。"],
    ["177", "cancel", "(v.)", "取消", "Your membership was canceled due to late payments.", "由於延遲付款,您的會員資格已被取消。"],
    ["178", "remind", "(v.)", "提醒", "Don't forget to remind me about the meeting tomorrow.", "別忘了提醒我明天有會議。"],
    ["179", "compare", "(v.)", "比較;對照", "We should compare the options before making the decision.", "我們應該在做出決定之前比較選項。"],
    ["180", "deliver", "(v.)", "遞送;發表演說", "The courier will deliver the package tomorrow.", "快遞員明天會將包裹送達。"],
    ["181", "apologize", "(v.)", "道歉", "I apologize for the late response.", "回覆晚了,非常抱歉。"],
    ["182", "remove", "(v.)", "去除;免職", "Please remove your belongings from the meeting room.", "請將您的物品帶出會議室。"],
    ["183", "organize", "(v.)", "安排;籌辦", "Let's organize a meeting to discuss the project details.", "我們安排一場會議,來討論專案的細節吧。"],
    ["184", "create", "(v.)", "創造;創作;創立", "The artist used different colors to create a vibrant painting.", "藝術家使用不同的顏色創作了一幅色彩鮮明的畫作。"],
    ["185", "recognize", "(v.)", "認出;認可;表揚", "He looked so different I could barely recognize him.", "他看起來完全不同,我幾乎認不出他了。"],
    ["186", "book", "(v.)", "預訂", "I would like to book a table for four at 7 P.M. tomorrow.", "我想預訂明天晚上七點四個人的位置。"],
    ["187", "respond", "(v.)", "回答;回應", "I will respond to your email as soon as possible.", "我會盡快回覆您的電子郵件。"],
    ["188", "mention", "(v.)", "提及", "I'll mention your ideas to the manager.", "我會跟經理提你的想法。"],
    ["189", "calculate", "(v.)", "計算", "I need to calculate how much time the assignment will take.", "我需要計算一下這份作業需要多少時間。"],
    ["190", "install", "(v.)", "安裝", "We need to install new software on all the computers.", "我們需要在所有電腦上安裝新軟體。"],
    ["191", "contain", "(v.)", "包含", "The bottle contains 500 milliliters of water.", "瓶子裡裝有500毫升的水。"],
    ["192", "match", "(v.)", "相符;相配", "The socks don't match my outfit.", "這雙襪子和我的穿著不搭。"],
    ["193", "afford", "(v.)", "負擔得起", "I cannot afford this luxurious lifestyle with my current salary.", "我現在的薪水負擔不起這種奢侈的生活方式。"],
    ["194", "assist", "(v.)", "協助", "Please reach out if there's anything we can assist you with.", "如果有什麼我們可以幫助您的,請聯繫我們。"],
    ["195", "attract", "(v.)", "吸引", "The colorful decorations will attract customers.", "色彩繽紛的佈置會吸引顧客上門。"],
    ["196", "develop", "(v.)", "發展;開發", "The company is planning to develop new products next year.", "公司計劃明年開發新產品。"],
    ["197", "confirm", "(v.)", "確認", "Please confirm your personal information on the form.", "請確認表格中您的個人資訊無誤。"],
    ["198", "apply", "(v.)", "申請;適用", "He applied for the manager position.", "他申請了經理職位。"],
    ["199", "reduce", "(v.)", "減少;降低", "We need to reduce our expenses to save money.", "我們需要減少開支來省錢。"],
    ["200", "reject", "(v.)", "拒絕;不錄用", "They rejected his job application due to lack of experience.", "他們以經驗不足為由,拒絕了他的工作應徵。"],
    ["201", "upload", "(v.)", "上傳", "The marketing team will upload the presentation tomorrow.", "行銷團隊明天會上傳簡報。"],
    ["202", "remain", "(v.)", "保持;仍然是", "He remained silent throughout the whole interrogation.", "整個審訊過程中,他一直保持沉默。"],
    ["203", "hire", "(v.)", "雇用;租用", "Let's hire someone professional to do our taxes this year.", "今年我們雇用專業人士來幫我們報稅吧。"],
    ["204", "expect", "(v.)", "預料;期望", "If you can get this client, you can expect a promotion.", "如果你能拿到這個客戶,你就可以期望升官了。"],
    ["205", "advertise", "(v.)", "打廣告;宣傳", "They plan to advertise their new product on television.", "他們計劃在電視上宣傳新產品。"],
    ["206", "arrange", "(v.)", "安排;排列", "We will arrange an interview with you within two days.", "我們將在兩天內安排與您面談。"],
    ["207", "represent", "(v.)", "代表", "The lawyer will represent the company in the legal proceedings.", "這位律師將在訴訟中代表該公司。"],
    ["208", "intend", "(v.)", "打算;計劃", "They intend to expand their business operations overseas.", "他們打算將業務擴展至海外。"],
    ["209", "recommend", "(v.)", "推薦;介紹", "I highly recommend this restaurant for its delicious food.", "我強烈推薦這家餐廳的美味食物。"],
    ["210", "participate", "(v.)", "參加;參與", "We encourage everyone to participate in the event.", "我們鼓勵大家參與此次活動。"],
    ["211", "require", "(v.)", "要求;需要", "They require that you bring only one guest to the dinner.", "他們要求您只帶一位客人參加晚宴。"],
    ["212", "subscribe", "(v.)", "訂閱", "If you like the video, please share and subscribe.", "如果喜歡這支影片,請分享和訂閱。"],
    ["213", "replace", "(v.)", "取代;代替", "It's time to replace the old furniture.", "是時候將舊家具汰換了。"],
    ["214", "perform", "(v.)", "進行;表演", "We ask interviewees to perform a few tasks on the computer.", "我們要求來面試的人用電腦執行幾個任務。"],
    ["215", "introduce", "(v.)", "引進;介紹", "New measures are introduced to ease traffic congestion.", "當局採用新措施以紓緩交通擠塞的情況。"],
    ["216", "prevent", "(v.)", "預防;阻止", "Regular exercise can help prevent certain diseases.", "經常運動有助於預防某些疾病。"],
    ["217", "reach", "(v.)", "聯絡到;到達", "You can reach me at this number if you have any questions.", "如果您有任何問題,可以撥打此號碼與我聯繫。"],
    ["218", "consider", "(v.)", "考慮;認為", "We need to consider all the factors before making a decision.", "在做出決定之前,我們需要考慮所有因素。"],
    ["219", "retire", "(v.)", "退休", "After working for 40 years, he decided to retire.", "在工作40年後,他決定退休。"],
    ["220", "attach", "(v.)", "附上;連接", "Don't forget to attach your résumé to the application.", "不要忘記將您的簡歷附在申請表上。"],
    ["221", "interrupt", "(v.)", "打斷;中斷", "Please do not interrupt the speaker while they are talking.", "請不要在講者發言時打斷他們。"],
    ["222", "seek", "(v.)", "尋求", "We seek to improve the quality of our products.", "我們尋求提高我們產品品質的方法。"],
    ["223", "depart", "(v.)", "啟程;出發", "The train will depart from platform six at 2 P.M.", "火車將於下午兩點從六號月台出發。"],
    ["224", "disturb", "(v.)", "打斷;擾亂", "Please do not disturb me while I'm working.", "請不要在我工作時打擾我。"],
    ["225", "propose", "(v.)", "提議", "I propose that we organize a team-building activity next month.", "我提議下個月安排一場團隊建立活動。"],
    ["226", "identify", "(v.)", "確認;辨識", "It can be difficult to identify the exact cause of the issue.", "可能很難確認問題的確切原因。"],
    ["227", "offer r", "(v.)", "提供;主動提議(n.)提供;主動提議", "They offered me a promotion and a higher salary.", "他們向我提供升職機會以及更高的薪水。"],
    ["228", "rise", "(v.)", "上升(n.)上升", "The price of cigarettes has risen again.", "香煙的價格又上漲了。"],
    ["229", "rent", "(v.)", "租(n.)租金", "We rented a car for the trip.", "我們為這次旅行租了一輛車。"],
    ["230", "increase", "(v.)", "增加(n.)增加", "The company plans to increase its production capacity.", "該公司計劃提高其生產能力。"],
    ["231", "contact", "(v.)", "聯絡(n.)聯絡;人脈", "Please feel free to contact us if you have any questions.", "如有任何疑問,請隨時與我們聯繫。"],
    ["232", "interview", "(v.)", "面試;採訪(n.)面試;採訪", "Candidates were invited for an interview early next month.", "應聘者被邀請參加下月初的面試。"],
    ["233", "repair", "(v.)", "修理;修復(n.)修理;修復", "The technician will repair the faulty equipment.", "技術人員將修復有故障的設備。"],
    ["234", "update", "(v.)", "更新(n.)更新;最新資訊", "Please update your contact information in the system.", "請更新您在系統中的聯絡資訊。"],
    ["235", "reserve", "(v.)", "預訂;保留(n.)保護區", "Please reserve a seat for me on the next flight.", "請為我預訂下一班機的機位。"],
    ["236", "support", "(v.)", "支持;資助(n.)支持", "The majority of people in the town support the plan.", "鎮上大多數人都支持這個計劃。"],
    ["237", "permit", "(v.)", "允許;同意(n.)許可證", "Smoking is not permitted in this building.", "本建築內禁止吸菸。"],
    ["238", "benefit", "(v.)", "對･･･有益(n.) 利益;好處", "I benefited a lot from the training sessions.", "我從培訓課程中受益匪淺。"],
    ["239", "supply", "(v.)", "供應(n.)供應量;供給量", "They supply us with the latest equipment.", "他們供應給我們最新的設備。"],
    ["240", "cause", "(v.)", "導致(n.)起因", "The flood was caused by the sudden heavy rain.", "突如其來的大雨導致了這場洪水。"],
    ["241", "praise", "(v.)", "讚揚;讚美(n.)讚揚;讚美", "The teacher praised the students for their excellent performance.", "老師表揚了學生的出色表現。"],
    ["242", "ban", "(v.)", "禁止(n.)禁令", "Smoking is banned in this area.", "本區域禁止吸菸。"],
    ["243", "damage", "(v.)", "損害(n.)損害;損失", "The storm damaged the roof of the house.", "暴風雨破壞了房子的屋頂。"],
    ["244", "transfer", "(v.)", "轉移;調部門;轉乘(n.)轉移;調部門;轉乘", "We were transferred from one bus to another.", "我們被從一輛巴士轉到另一輛巴士上。"],
    ["245", "launch", "(v.)", "開始;推出(n.)發表會", "We're going to launch a recruitment drive next month.", "我們下個月將發起一場招聘會。"],
    ["246", "command", "(v.)", "命令;控制(n.)控制權", "She commanded him to move out after their last fight.", "在他們最後一次爭吵之後,她命令他搬出去。"],
    ["247", "advance", "(v.)", "進步;進展(n.)進步;進展(adj.)預先的", "They were under orders to advance the next day.", "他們奉命第二天前進。"],
    ["248", "fit", "(v.)", "合適;合身(adj.)合適的;健壯的", "This dress doesn't fit me well.", "這件洋裝我穿起來不太合身。"],
    ["249", "select", "(v.)", "挑選(adj.)精選的;最優秀的", "Please select the items you want to purchase.", "請選擇您要購買的商品。"],
    ["250", "separate", "(v.)", "使分開;使分離(adj.)分開的;單獨的", "Police came to separate the people fighting on the street.", "警察過來把街上打架的人分開了。"],
    ["251", "regarding", "(prep.)", "關於", "I'll discuss with my manager regarding this problem.", "關於這個問題,我會跟我的經理討論。"],
    ["252", "construction", "(n.)", "建造;建設", "The construction of the new building will start next month.", "新建築的建設將於下個月開始。"],
    ["253", "appliance", "(n.)", "家用電器", "You can use all the kitchen appliances in the office.", "你可以使用辦公室內的所有廚房電器。"],
    ["254", "subscription", "(n.)", "訂閱", "She just signed up for a one-year magazine subscription.", "她剛訂了一年的雜誌訂閱。"],
    ["255", "ingredient", "(n.)", "成分;要素", "Salt is a key ingredient in this recipe.", "鹽是這份食譜的關鍵食材。"],
    ["256", "competitor", "(n.)", "競爭者;對手", "They lost the business to a competitor.", "他們把生意輸給了競爭對手。"],
    ["257", "certificate", "(n.)", "證書;證明", "She received a certificate for completing the training program.", "她完成培訓課程,獲得一份證書。"],
    ["258", "trend", "(n.)", "趨勢;傾向", "There's been an upward trend in sales in the last few years.", "過去幾年,銷售額一直呈上升趨勢。"],
    ["259", "balance", "(n.)", "餘額;平衡", "You can check the balance of your account from the app.", "您可以從 app 查看您的帳戶餘額。"],
    ["260", "summary", "(n.)", "摘要", "Please provide a short summary of the meeting.", "請提供這場會議的摘要。"],
    ["261", "deadline", "(n.)", "截止日", "Management has agreed to extend the deadline.", "上層已同意延後截止日期。"],
    ["262", "accountant", "(n.)", "會計師", "My sister is an accountant at a multinational company.", "我姐姐擔任跨國公司的會計師。"],
    ["263", "conference", "(n.)", "研討會;大會", "We attended the conference to fulfill our PD requirement.", "我們參加那個研討會是為了滿足工作的進修要求。"],
    ["264", "performance", "(n.)", "表現;表演", "Her performance in the play was outstanding.", "她在戲劇中的表現非常出色。"],
    ["265", "assignment", "(n.)", "任務;工作", "My boss gave me a tough assignment today.", "老闆今天給了我一個艱鉅的任務。"],
    ["266", "briefcase", "(n.)", "公事包", "He brings a leather briefcase to work every day.", "他每天都帶著一個真皮公文包去上班。"],
    ["267", "industry", "(n.)", "產業;工業", "The automotive industry plays a crucial role in the economy.", "汽車業在經濟中扮演關鍵角色。"],
    ["268", "instructor", "(n.)", "教練;大學講師", "The dance instructor taught the students new moves.", "舞蹈老師教導學生新的舞步。"],
    ["269", "donation", "(n.)", "捐獻;捐贈", "The donation will be used to support education programs.", "這筆捐款將用於支助教育計畫。"],
    ["270", "identification", "(n.)", "身分證明;識別", "Please provide identification when entering the building.", "進入大樓時請出示身分證明。"],
    ["271", "interest", "(n.)", "利息;興趣", "The bank offers competitive interest rates.", "這家銀行提供有競爭力的利率。"],
    ["272", "community", "(n.)", "社群;團體;社區", "There is a large LGBTQ community in San Francisco.", "舊金山有一個龐大的LGBTQ社群。"],
    ["273", "conclusion", "(n.)", "結論", "In conclusion, the project was a success.", "結論是專案取得了成功。"],
    ["274", "ceremony", "(n.)", "典禮", "The wedding ceremony will take place tomorrow at 10 A.M.", "婚禮將於明天上午10點舉行。"],
    ["275", "category", "(n.)", "類別;種類", "This book belongs to the sci-fi category.", "這本書屬於科幻類別。"],
    ["276", "fault", "(n.)", "過錯;責任", "It was his fault that the project was delayed.", "專案延遲是他的錯。"],
    ["277", "application", "(n.)", "申請;應用軟體", "The deadline for the application is this Friday.", "申請截止日期為本週五。"],
    ["278", "photocopier", "(n.)", "影印機", "The photocopier in the office needs more paper.", "辦公室的影印機需要補充紙張。"],
    ["279", "registration", "(n.)", "登記;報到;註冊", "Registration for the event is now open.", "活動的註冊現已開放。"],
    ["280", "transportation", "(n.)", "運輸;交通工具", "Public transportation is a cost-effective way to travel.", "搭乘大眾運輸是省錢的交通方式。"],
    ["281", "promotion", "(n.)", "升遷;促銷", "The manager received a promotion to regional director.", "經理被升職為區域總監。"],
    ["282", "pension", "(n.)", "退休金", "After retiring, she receives a monthly pension.", "退休後,她每月領取退休金。"],
    ["283", "majority", "(n.)", "大多數", "The majority of our employees have master's degrees.", "我們大多數員工都有碩士學位。"],
    ["284", "extension", "(n.)", "分機;展延;擴建部分", "The extension number for the reception is 101.", "服務台的分機號碼是101。"],
    ["285", "assembly", "(n.)", "集會;組裝", "The students gathered in the gym for the assembly.", "學生們聚集在體育館進行集會。"],
    ["286", "degree", "(n.)", "程度;學位", "She has a high degree of expertise in her field.", "她在自己的領域上擁有高度專業水平。"],
    ["287", "expense", "(n.)", "開銷;費用", "Traveling can be quite an expense, but it's worth it.", "旅行的開支可能不少,但仍然值得。"],
    ["288", "division", "(n.)", "部門", "The company has a division dedicated to customer service.", "公司有專門的客戶服務部門。"],
    ["289", "policy", "(n.)", "政策;保險單", "The new policy aims to promote environmental sustainability.", "新政策旨在倡導環境永續性。"],
    ["290", "employment", "(n.)", "就業;受雇", "She found employment at a local company.", "她在當地一家公司找到了工作。"],
    ["291", "investment", "(n.)", "投資", "He made a wise investment that yielded high returns.", "他做了一項明智的投資並獲得高額回報。"],
    ["292", "résumé", "(n.)", "履歷", "Your résumé should highlight your skills and achievements.", "你的履歷應該突顯你的能力和成就。"],
    ["293", "maintenance", "(n.)", "維護;保養", "Regular maintenance keeps the equipment in good condition.", "定期維護可使設備保持良好狀態。"],
    ["294", "outcome", "(n.)", "結果;效果", "The outcome of the negotiations was a win-win situation.", "談判的結果是雙贏的局面。"],
    ["295", "proposal", "(n.)", "提案", "Did he approve my proposal?", "他同意我的提案了嗎?"],
    ["296", "labor", "(n.)", "勞工;勞動", "Try to avoid buying from companies that use cheap labor.", "儘量避免跟使用廉價勞工的公司消費。"],
    ["297", "sector", "(n.)", "部門;領域", "She works in the financial sector.", "她在金融領域工作。"],
    ["298", "term", "(n.)", "條款;期;術語", "The contract contains specific terms and conditions.", "合約包含明確的條款和細則。"],
    ["299", "committee", "(n.)", "委員會", "The committee met to discuss the proposed changes.", "委員會開會討論提出的變更。"],
    ["300", "plant", "(n.)", "工廠;植物", "The company built a new plant for manufacturing.", "公司建了一座新的生產工廠。"],
    ["301", "outlet", "(n.)", "銷售據點", "The new California Pizza Kitchen outlet opened last week.", "新的 California Pizza Kitchen 分店上週開業。"],
    ["302", "duration", "(n.)", "期間;持續時間", "The next contract will be of a shorter duration.", "下一份合約的期限會更短。"],
    ["303", "database", "(n.)", "數據庫;資料庫", "The company maintains a database of customer records.", "公司維護著一個客戶記錄數據庫。"],
    ["304", "literacy", "(n.)", "讀寫能力;識字", "A high standard of literacy will be required for the job.", "這項工作需要高標準的讀寫能力。"],
    ["305", "structure", "(n.)", "結構;構造;建築物", "The building's structure is designed to withstand earthquakes.", "這棟建築的結構設計能承受地震。"],
    ["306", "firm", "(n.)", "事務所;公司", "She works for a big law firm.", "她在一家大律師事務所工作。"],
    ["307", "superior", "(n.)", "上司", "She is my superior at work and gives me guidance.", "她是我的上司,會給予我指導。"],
    ["308", "obligation", "(n.)", "義務;責任", "It is my obligation to complete the assigned tasks.", "我有責任將分配的工作完成。"],
    ["309", "unemployment", "(n.)", "失業狀態;失業人數", "The economic downturn led to a high unemployment rate.", "景氣低迷造成高失業率。"],
    ["310", "evidence", "(n.)", "證據;證明", "The new piece of evidence weakens the case against her.", "新的證據削弱了對她的指控。"],
    ["311", "dashboard", "(n.)", "儀表板", "The sales dashboard displays real-time data for executives.", "這個銷售儀表板為主管們顯示即時數據。"],
    ["312", "principle", "(n.)", "原則;準則", "Honesty is an important principle in business ethics.", "誠信是商業道德的重要原則。"],
    ["313", "editor", "(n.)", "編輯", "She's the editor of a popular magazine.", "她是一家流行雜誌的編輯。"],
    ["314", "consumer", "(n.)", "消費者", "Knowing our consumers will allow us to improve our products.", "了解我們的消費者能讓我們改進產品。"],
    ["315", "resource", "(n.)", "資源", "Natural resources such as oil and minerals are valuable.", "石油和礦產等自然資源非常珍貴。"],
    ["316", "candidate", "(n.)", "求職者;申請人;候選人", "There were two candidates for the last round of the interview.", "最後一輪面試有兩位候選人。"],
    ["317", "shipment", "(n.)", "運送的貨物;運輸", "The shipment of goods arrived on time.", "貨物按時送達。"],
    ["318", "applicant", "(n.)", "申請人", "All applicants will receive a confirmation email.", "所有申請者都會收到一封確認郵件。"],
    ["319", "administration", "(n.)", "行政工作;管理部門", "The new policy requires efficient administration.", "新政策需要高效的行政管理。"],
    ["320", "supervisor", "(n.)", "上司;監督者", "I'm meeting with my supervisor tomorrow to ask for a raise.", "我明天要和我主管開會,要求加薪。"],
    ["321", "session", "(n.)", "活動期間;授課期間", "The runner twisted his ankle in a training session today.", "那位跑者在今天的訓練過程中扭傷了腳踝。"],
    ["322", "improvement", "(n.)", "改善;增進", "The company made significant improvements in its processes.", "該公司對其流程進行了重大改進。"],
    ["323", "presentation", "(n.)", "(口頭)報告", "He gave an interesting presentation on human evolution.", "他做了一個關於人類進化的有趣演講。"],
    ["324", "hardware", "(n.)", "硬體設備;五金製品", "The company ordered new hardware for its computers.", "該公司為他們的電腦訂購了新的硬體。"],
    ["325", "excursion", "(n.)", "短程旅行", "We went on an excursion to the nearby waterfall.", "我們去附近的瀑布郊遊。"],
    ["326", "reception", "(n.)", "歡迎會;接待處", "The president gave a reception for the visiting guests.", "總統舉行招待會款待來訪的貴賓。"],
    ["327", "priority", "(n.)", "優先事項", "Our main priority is to provide excellent customer service.", "我們的首要任務是提供卓越的客戶服務。"],
    ["328", "trial", "(n.)", "試用;試驗", "The position comes with a three-month trial period.", "這個職缺有三個月的試用期。"],
    ["329", "economy", "(n.)", "經濟;節省", "The country's economy has been growing steadily.", "該國經濟一直在穩定成長。"],
    ["330", "accounting", "(n.)", "會計", "There is a position open in the accounting department.", "會計部門有一個職位空缺。"],
    ["331", "appreciation", "(n.)", "感激;增值", "In appreciation of your hard work, you'll receive a bonus.", "為了感謝你們的努力,你們都會得到獎金。"],
    ["332", "merchandise", "(n.)", "商品;貨物", "The store offers a wide range of merchandise for sale.", "這家商店銷售種類繁多的商品。"],
    ["333", "motivation", "(n.)", "動機;動力", "Jax is an intelligent student but lacks motivation.", "賈克斯是個聰明的學生,但缺乏動力。"],
    ["334", "technician", "(n.)", "技術人員;技師", "The technician repaired the faulty equipment.", "技術人員修理了故障的設備。"],
    ["335", "memo", "(n.)", "備忘錄;便條", "The manager sent a memo about the policy change.", "經理發了一份關於政策變更的備忘錄。"],
    ["336", "transit", "(n.)", "運輸;輸送", "The transit system in the city is efficient and reliable.", "市內的交通運輸系統高效又可靠。"],
    ["337", "layout", "(n.)", "空間的佈局;版面設計", "I like the layout of the house.", "我喜歡這間房子的佈局。"],
    ["338", "statement", "(n.)", "對帳單", "Please review your bank statement for any discrepancies.", "請檢查您的銀行對賬單是否有任何異常。"],
    ["339", "position", "(n.)", "職位;工作", "There is a position open in the language department.", "語言部門有職位開缺。"],
    ["340", "tenant", "(n.)", "房客;承租人", "The landlord found a new tenant for the apartment.", "房東找到了公寓的新房客。"],
    ["341", "feedback", "(n.)", "意見回饋", "The feedback is used to modify the course for next year.", "意見回饋是用來調整明年的課程的。"],
    ["342", "courier", "(n.)", "快遞員", "You can use any courier company to send the document.", "您可以用任何快遞公司來寄送這份文件。"],
    ["343", "responsibility", "(n.)", "職責;責任", "Taking care of the environment is everyone's responsibility.", "愛護環境人人有責。"],
    ["344", "commuter", "(n.)", "通勤者", "The MRT is always packed with commuters during rush hours.", "捷運在上下班尖峰時刻總是擠滿了通勤者。"],
    ["345", "quarter", "(n.)", "季度", "The financial report shows an increase in sales this quarter.", "財報顯示本季度銷售額有所增長。"],
    ["346", "stock", "(n.)", "存貨;股票", "The store has a wide variety of products in stock.", "這家商店現貨供應的商品種類繁多。"],
    ["347", "utilities", "(n.)", "公共事業費用(如水電費);公共事業", "The rent is $1500, not including utilities.", "租金為1500美元,不包括水電費。"],
    ["348", "layover", "(n.)", "轉機停留;短暫停留", "During his layover in Dubai, he checked business emails.", "在迪拜轉機停留期間,他查看了工作郵件。"],
    ["349", "agenda", "(n.)", "議程;會議待討論的事項", "The agenda for the meeting includes several important topics.", "會議議程包括幾個重要的主題。"],
    ["350", "transcript", "(n.)", "成績單;逐字稿", "The interview transcript will be available by tomorrow.", "面試逐字稿將在明天前提供。"],
    ["351", "proportion", "(n.)", "比例;部分", "The proportion of male to female participants is balanced.", "男女參加者的比例均衡。"],
    ["352", "reputation", "(n.)", "名譽;名聲", "The company's reputation for quality products is well-known.", "該公司以高品質產品聞名。"],
    ["353", "itinerary", "(n.)", "預定行程;行程安排", "The travel agency provided us with a detailed itinerary.", "旅行社提供我們詳細的行程安排。"],
    ["354", "consent", "(n.)", "許可;同意", "Verbal consent is important. Silence does not mean consent.", "口頭同意很重要。沉默不代表同意。"],
    ["355", "milestone", "(n.)", "里程碑", "The merger represents a major milestone for our company.", "這次合併對我們公司來說是一個重要的里程碑。"],
    ["356", "interface", "(n.)", "介面", "The new software interface streamlines our customer service operations.", "新的軟體介面簡化了我們的客戶服務操作流程。"],
    ["357", "certification", "(n.)", "認證;證書", "The company requires certification for all safety inspectors.", "公司要求所有安全檢查員都必須具備認證資格。"],
    ["358", "statistics", "(n.)", "統計數據", "Statistics suggest that women live longer than men.", "統計數據表明,女性的壽命比男性長。"],
    ["359", "individual", "(n.)", "個人;個體(adj.)個別的;個人的", "Every individual has rights that must never be taken away.", "每一個人都有不可被剝奪的權利。"],
    ["360", "reward", "(n.)", "報酬(v.)報答", "They receive a bonus as a reward for their hard work.", "他們因為辛勤工作而獲得獎金作為獎勵。"],
    ["361", "broadcast", "(n.)", "廣播;廣播節目(v.)廣播", "I heard the news on the radio broadcast.", "我在廣播中聽到了這則新聞。"],
    ["362", "influence", "(n.)", "影響(v.)影響", "Her speech had a great influence on the audience.", "她的演講對聽眾產生了很大的影響。"],
    ["363", "lecture", "(n.)", "講座;講課(v.)講授", "I attended a fascinating lecture on astronomy.", "我參加了一場引人入勝的天文學講座。"],
    ["364", "host", "(n.)", "主辦方;主持人;主人(v.)主辦;主持", "Who is the host of tonight's concert?", "今晚音樂會的主持人是誰?"],
    ["365", "retail", "(n.)", "零售(v.)零售", "She buys wholesale and sells retail.", "她批發採購,零售銷售。"],
    ["366", "strike", "(n.)", "罷工(v.)罷工", "Doctors at the hospital have gone on strike for two weeks.", "那間醫院的醫生已經罷工兩週了。"],
    ["367", "credit", "(n.)", "信用(v.)歸功於", "He has a good credit score and can get a loan easily.", "他的信用評分很好,可以輕易獲得貸款。"],
    ["368", "contract", "(n.)", "合約(v.)訂合約", "We signed a contract with the supplier.", "我們與供應商簽了合約。"],
    ["369", "rate", "(n.)", "費率;費用(v.)評價", "What's the standard rate for this type of work?", "這種工作一般酬金是多少?"],
    ["370", "shift", "(n.)", "輪班;轉移(v.)轉移", "She will switch to the night shift starting next week.", "她將於下週開始轉換到夜班。"],
    ["371", "profit", "(n.)", "利潤(v.)獲利", "The company reported a significant increase in profits.", "公司通報利潤大幅成長。"],
    ["372", "access", "(n.)", "有權使用;進入(v.)有權使用;進入", "The ID card will give you access to the building.", "這張識別證會給你權限進入大樓。"],
    ["373", "conflict", "(n.)", "衝突(v.)衝突", "He is in constant conflict with his manager.", "他經常跟他的經理發生衝突。"],
    ["374", "deposit", "(n.)", "訂金;押金(v.)支付預繳費用", "He put a deposit on the house.", "他付了那棟房的訂金。"],
    ["375", "debate", "(n.)", "辯論(v.)辯論", "The candidates engaged in a heated debate on the issue.", "候選人就此議題展開激烈的辯論。"],
    ["376", "impact", "(n.)", "衝擊;影響(v.)影響", "The new policy had a significant impact on the economy.", "新政策對經濟產生了重大影響。"],
    ["377", "forecast", "(n.)", "預測;預報(v.)預測;預報", "The sales team forecast strong growth for next quarter.", "銷售團隊預測下一季度會有強勁增長。"],
    ["378", "punctual", "(adj.)", "準時的", "The manager praised John for being consistently punctual.", "經理稱讚 John一直都很守時。"],
    ["379", "current", "(adj.)", "當前的;現有的", "What is your current location?", "你現在在哪裡?"],
    ["380", "specific", "(adj.)", "明確的;特定的", "The instructions we received were very specific.", "我們收到的指示非常明確。"],
    ["381", "incredible", "(adj.)", "極好的;難以置信的", "The team achieved an incredible victory against all odds.", "團隊克服萬難,取得了美妙的勝利。"],
    ["382", "affordable", "(adj.)", "負擔得起的", "The new housing development is an affordable option.", "這個新的住宅開發案是一個負擔得起的選擇。"],
    ["383", "flexible", "(adj.)", "有彈性的;可變通的", "Yoga exercises can make your body more flexible.", "瑜伽運動可以使你的身體更柔軟。"],
    ["384", "unique", "(adj.)", "獨特的", "Our app offers a unique solution to language learning.", "我們的應用程式提供了獨特的語言學習解決方案。"],
    ["385", "effective", "(adj.)", "生效的;有效的", "You are suspended for two weeks, effective immediately.", "你被停職兩週。立即生效。"],
    ["386", "diverse", "(adj.)", "多元的;迥異的", "New York is a very culturally diverse city.", "紐約是一個文化非常多元的城市。"],
    ["387", "constant", "(adj.)", "持續的", "His constant complaints are really getting on my nerves.", "他持續不停的抱怨真讓我心煩意亂。"],
    ["388", "gross", "(adj.)", "總額的", "Our company's gross profit increased by 20% compared to last year.", "我們公司的毛利相比去年成長了20%。"],
    ["389", "inexperienced", "(adj.)", "無經驗的", "The company hired inexperienced interns for the summer.", "公司在暑假期間雇用了沒有經驗的實習生。"],
    ["390", "adjacent", "(adj.)", "鄰近的", "The new office is adjacent to the shopping mall.", "新辦公室與購物中心相鄰。"],
    ["391", "economic", "(adj.)", "經濟上的;有經濟效益的", "The company is wrestling with difficult economic problems.", "公司正在努力解決困難的經濟問題。"],
    ["392", "relevant", "(adj.)", "密切相關的;有意義的", "Her presentation included relevant data and case studies.", "她的報告內容包含相關數據和案例研究。"],
    ["393", "domestic", "(adj.)", "國內的;家庭的", "The company focuses on domestic markets for its products.", "該公司的產品主要針對國內市場。"],
    ["394", "complimentary", "(adj.)", "免費贈送的", "The hotel provides complimentary breakfast.", "那間飯店提供免費早餐。"],
    ["395", "ongoing", "(adj.)", "進行中的;持續存在的", "The ongoing project is scheduled to be completed next month.", "進行中的專案預計將於下個月完成。"],
    ["396", "principal", "(adj.)", "最重要的", "This is the principal road between the two cities.", "這是兩個城市之間最重要的道路。"],
    ["397", "verbal", "(adj.)", "口頭的;言詞上的", "Verbal agreements are not legally binding.", "口頭協議不具有法律約束力。"],
    ["398", "spacious", "(adj.)", "寬敞的", "The office has a spacious conference room for meetings.", "辦公室有一間寬敞的會議室用於開會。"],
    ["399", "cautious", "(adj.)", "謹慎的;斟酌過的", "It's important to be cautious when crossing the street.", "過馬路時一定要保持警覺。"],
    ["400", "internal", "(adj.)", "內部的;國內的", "Internal communication is essential for effective teamwork.", "內部溝通對於有效的團隊合作至關重要。"],
    ["401", "overall", "(adj.)", "整體的;全部的", "The overall satisfaction of our customers is our priority.", "客戶整體的滿意度是我們的首要任務。"],
    ["402", "valid", "(adj.)", "有效力的;有根據的", "Make sure your passport is valid before traveling.", "在旅行前先確認你的護照有效。"],
    ["403", "fundamental", "(adj.)", "基礎的;根本的", "Communication skills are fundamental in the workplace.", "在工作場合,溝通技巧是根本技能。"],
    ["404", "medical", "(adj.)", "醫療的;醫學的", "The patient received medical treatment for his condition.", "病人因病情接受了治療。"],
    ["405", "accessible", "(adj.)", "可接近的;可得到的", "The museum is accessible for people with disabilities.", "這個博物館對於身障人士來說是無障礙的。"],
    ["406", "additional", "(adj.)", "附加的;額外的", "I need some additional information for my report.", "我的報告需要補充一些額外資訊。"],
    ["407", "reasonable", "(adj.)", "合理的", "The rent here is reasonable, and the location is perfect.", "這裡的租金很合理,位置也很完美。"],
    ["408", "appropriate", "(adj.)", "適當的;恰當的", "Please wear appropriate attire for the formal event.", "請穿著合適的服裝出席這場正式活動。"],
    ["409", "permanent", "(adj.)", "長久的;永遠的", "She accepted a permanent position at the company.", "她接受了該公司的長期職位。"],
    ["410", "abundant", "(adj.)", "豐富的;大量的", "The garden is abundant with colorful flowers.", "花園裡開滿了五顏六色的花朵。"],
    ["411", "anonymous", "(adj.)", "匿名的;不具名的", "The anonymous donor contributed generously to our company.", "這位匿名捐贈者慷慨地捐助了我們公司。"],
    ["412", "extensive", "(adj.)", "廣泛的", "He conducted an extensive research study on the topic.", "他對該主題進行了廣泛的研究。"],
    ["413", "potential", "(adj.)", "潛在的;可能的(n.)潜力", "The company was considered a potential partner.", "該公司被視為潛在的合作夥伴。"],
    ["414", "technical", "(adj.)", "技術性的;專業的", "He has excellent technical skills in computer programming.", "他在電腦程式設計方面有傑出的技術能力。"],
    ["415", "essential", "(adj.)", "必要的(n.)必需品", "Good time management is essential for productivity at work.", "善於時間管理對工作效率來說至關重要。"],
    ["416", "professional", "(adj.)", "專業的(n.)專家", "He is a professional accountant with years of experience.", "他是一位擁有多年經驗的專業會計師。"],
    ["417", "commercial", "(adj.)", "商業的;商務的(n.)商業廣告", "Companies fight to protect their own commercial interests.", "企業為了保護自己的商業利益而爭鬥。"],
    ["418", "overseas", "(adj.)", "海外的;國外的(adv.)在海外;到海外", "She went on an overseas trip last month.", "她上個月去海外旅行。"],
    ["419", "moderate", "(adj.)", "適度的;中等的(v.)主持", "She adopted a moderate approach to resolving the conflict.", "她採取了溫和的方式來解決衝突。"],
    ["420", "particularly", "(adv.)", "尤其;特別", "She is particularly interested in art history.", "她對藝術史特別感興趣。"],
    ["421", "approximately", "(adv.)", "大約;大概", "The journey will take approximately three hours by car.", "車程大約需要三個小時。"],
    ["422", "concentrate", "(v.)", "專心;集中;濃縮", "Try to concentrate on one thing at a time.", "試著一次專注在一件事情上就好。"],
    ["423", "scan", "(v.)", "掃描;快速瀏覽", "First, scan the text into the computer, then edit it.", "先把文字檔掃描到電腦中,然後再做編輯。"],
    ["424", "postpone", "(v.)", "延後;延期", "The meeting has been postponed to next week.", "會議已延期至下週舉行。"],
    ["425", "reschedule", "(v.)", "改期", "We had to reschedule the meeting due to a conflict.", "由於時間衝突,我們不得不重新安排會議。"],
    ["426", "affect", "(v.)", "影響", "A negative work environment can affect productivity.", "負面的工作環境會影響生產力。"],
    ["427", "predict", "(v.)", "預測", "Experts predict that the economy will improve next year.", "專家預測明年經濟將好轉。"],
]

# --- 4. 初始化 Session State ---
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

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

# --- 6. 介面佈局 (將起始編號與跳轉按鈕並排在同一行) ---
col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
with col_s1:
    start_input = st.number_input("跳至編號：", min_value=1, max_value=len(verb_db), value=st.session_state.index + 1)
with col_s2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # 調整對齊
    if st.button("跳轉"):
        st.session_state.index = int(start_input) - 1
        st.session_state.show_answer = False
        st.rerun()
with col_s3:
    pass

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

# 底部按鈕設定：未顯示答案時顯示「顯示答案」；顯示答案後顯示「重新播放」與「下一題」
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
