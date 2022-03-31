#載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random

from fileinput import filename
import gspread
gc=gspread.service_account(filename='smile-world-340813-6b2b86613f09.json')
sh=gc.open_by_key('1FsfvfBLAazAehvUqaVH9rH6zzdCowoYpedVsDSkuAdk')
worksheet=sh.sheet1
app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('6yo/DqXY5g3m5Xa8MSmtMJ+4GcHbPbBcEEmwMIptohE6ko3jcTv6DxD0P5CoGfOTweYFmaAlhSxFN7UG6OP22VZBhkA77CK8MCAXYMu+r9FHa4ekpvI5c4JuOzxPOEMnCucHbNvZBz/z0arFcgcuEgdB04t89/1O/w1cDnyilFU=')
 
# 必須放上自己的Channel Secret
handler = WebhookHandler('7db1582c7eff2381ee81ec616b1c0dbf')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
  
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message=event.message.text
    message=message.encode('utf-8')
    if event.message.text=="開始遊戲":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經開始遊戲，要重新開始請輸入「重置遊戲」。"))
        else:
            userid_list=worksheet.col_values(1)
            x=len(userid_list)
            list=[]
            for i in range(65,70):
                list.append(chr(i)+str(x+1))
            #寫入ID
            worksheet.update(list[0],event.source.user_id)
            #初始值設定到AX
            for i in range(1,len(list)):
                worksheet.update(list[i],int(0))
            worksheet.update(list[4],int(1))
            list_talk=[]
            list_talk.append(TextSendMessage("選擇遊戲視角"))
            image_carousel_template_message = TemplateSendMessage(
                alt_text='選擇視角',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://upload.cc/i1/2022/03/30/K9D6Xw.jpg?fbclid=IwAR3TXV-o2OBUFuPpOursWi-w4pik7hG__iqpSahR59P7CcBaeb76ZvWKQPM',
                            action=MessageTemplateAction(
                                label='日翔',
                                text='以日翔的視角進行遊戲'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://upload.cc/i1/2022/03/30/dRcCSl.jpg?fbclid=IwAR0LgBlXQ2LP-Ag99jBXJALWmbv2zF-DUX9BXp6dTEGn494AIAUKrxOr6q4',
                            action=MessageTemplateAction(
                                label='曉光',
                                text='以曉光的視角進行遊戲'
                            )
                        )
                    ]
                )
            )
            list_talk.append(image_carousel_template_message)
            line_bot_api.reply_message(event.reply_token,list_talk)   

    elif event.message.text=="以日翔的視角進行遊戲":
        userid_list=worksheet.col_values(1)
        #ID已寫入
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            #ID已寫入且未選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(1))
                list=[]
                list.append(ImageSendMessage(original_content_url='https://i.imgur.com/2cCaBmx.jpeg', preview_image_url='https://i.imgur.com/2cCaBmx.jpeg'))
                list.append(TextSendMessage(text="「唉......今天又被塞了一堆工作啊......」成為社畜後的日翔，每天過著上班族朝九晚五的生活。早上和一堆人擠著去上班，工作又多又忙連喘息的時間都沒有，晚上回到家早就累壞了。"+'\n'+'「如果能回到大學時期就好了啊......」某天工作回家的日翔突然感嘆起大學生活，大學可謂人生的最顛峰時期，不但沒有工作壓力的負擔，還有很多空閒時間可以讓他盡情做想做的事。這時，日翔的電子信箱突然跳出了一封信，開頭標題寫著「想回到過去嗎？」'+'\n'+'該不會是被誰監視了？雖然這麼想，出於好奇日翔還是點開了信件，內容寫著「路過的小精靈聽到你的願望送上的檔案，並沒有病毒。」，還附上了一個檔案「Code-140.136.py」。'+'\n'+'……哪個詐騙集團會說自己不是詐騙集團呢，日翔吐槽道。'+'\n'+'或許是想回到過去的願望過於強烈，日翔還是不由自主地下載了檔案。'))
                list.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/06/q4DPkj.png', preview_image_url='https://upload.cc/i1/2022/03/06/q4DPkj.png'))
                list.append(TextSendMessage(text='#1 檔案只有短短幾行程式碼，請問日翔該輸入什麼才能執行此函式，讓結果非None呢？（請輸入半形英文字母）'))
                line_bot_api.reply_message(event.reply_token,list)
            #ID已寫入建立且視角!=0
            elif worksheet.acell(list[0]).value=="1":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選擇日翔視角。"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選曉光視角，要重置請輸入「重置遊戲」。"))
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))

    elif event.message.text=="以曉光的視角進行遊戲":
        userid_list=worksheet.col_values(1)
        #ID已寫入
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            #ID已寫入且已選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(2))
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="選擇了曉光視角！"))
            #個人檔案已建立且視角!=0
            elif worksheet.acell(list[0]).value=="2":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選曉光視角，要重置請輸入「重置遊戲」。"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選日翔視角，要重置請輸入「重置遊戲」。"))
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))

    #1答案
    elif event.message.text=="return":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            list.append('F'+str(j))
            #ID已寫入、日向視角、Q1=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="執行程式後，日翔的螢幕發出了一道刺眼的閃光，幾乎讓日翔睜不開眼睛。日翔隱約聽見一個聲音在耳邊說著：「嘻嘻，這樣人情就還清了，剩下的就看你在學校的表現了。」聲音一落下，刺眼的光就消失了，日翔才緩緩地睜開眼睛。"+"\n"+"「剛剛那是什麼！？」日翔不記得自己欠過誰人情呀？過了一會，日翔才發現自己站在老家的房間裡，連房裡的擺設都跟以前一模一樣，難道自己真的回到過去了嗎？"+"\n"+"「日翔！你怎麼還在房間裡！大學不是今天開學嗎，難道你想第一天上學就遲到嗎？」呃！連媽媽的聲音都跟以前一樣，話說回來剛剛的聲音好像提到了學校？總之先去學校看看吧，搞不好能找到有關那個聲音的線索？"))
                list_talk.append(TextSendMessage(text="#2 要出發去學校了，輔大的地址是？（請以「ＯＯ市ＯＯ區ＯＯ路ＯＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
   #2答案
    elif event.message.text=="新北市新莊區中正路510號":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('F'+str(j))
            list.append('G'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔將上課需要的東西塞進書包匆匆出門了，從日翔老家前往輔大最方便的交通工具就是捷運了，不僅不像公車可能會遇上塞車，在開通環狀線後學生搭捷運所需通勤時間大幅縮短，甚至設有以輔大命名的捷運站直達校門口。"))
                list_talk.append(TextSendMessage(text="#3 請問離校園最近的捷運出口爲？（請以「Ｏ號」回答。Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #3答案
    elif event.message.text=="1號":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('G'+str(j))
            list.append('H'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="還好學生證裡還有足夠錢可以讓日翔坐車，日翔倚靠在車門邊沿途欣賞環狀線行經的景色。此刻的他正感到無比放鬆，同樣是在交通巔峰通勤，但日翔現在不必時刻煩惱公司那惱人的報表、業績考核，如果現在發生的一切都是夢的話，拜託讓他多享受一下再醒吧。"+"\n"+"捷運放慢速度進了站，因為是轉乘站的關係，在這站上下車的人數比較多，在一陣推擠後車門終於關上了。捷運再次啟動，這時車廂內傳來的小小聲的驚呼讓日翔的目光從窗外回到車廂，日翔注意到腳邊不知何時出現了一張卡，上頭熟悉的圖案讓日翔一眼認出是輔大的學生證。"+"\n"+"日翔將學生證撿了起來，順便看了一眼學生證上頭的學生資訊，想看看到底是哪個冒失鬼遺落了學生證。經歷過一次大學生活的日翔知道學生證對輔大學生的重要性，學生證不僅可以作為悠遊卡使用，有些教授在期中期末考也會要求學生出示學生證以辨認學生身分。"+"\n"+"學生證上是一張青澀的女孩子的照片，總覺得看起來很熟悉......？往下瞧竟然也是資訊管理系，開學第一天就遇到同系的人嗎？還真巧啊，日翔莞爾。不過看見對方的姓名欄時日翔愣住了，白底黑字清清楚楚地寫著「何曉光」三個字。"+"\n"+"何曉光——在過去和日翔同班，不僅是個大學霸，還是系上的系花，更重要的是！曉光還是日翔單戀了整整四年的女神，不過日翔在過去因為成績太差而不敢高攀曉光。曉光總是安安靜靜地坐在位置上看書，給人一種「可遠觀不可褻玩焉」的感覺，曉光無論是舉手投足間的優雅，還是不冷不熱的語調都讓日翔很是喜歡。"+"\n"+"曉光的學生證掉落在這裡表示曉光也在這班車上嗎！？日翔朝車廂內望去，果不其然發現了正四處張望尋找遺落的學生證的曉光，日翔其實很猶豫到底要不要跟曉光搭話，但少了學生證曉光也出不了站。既然神都給他和曉光說上話的機會了，他又何嘗不把握呢？"))
                list_talk.append(TextSendMessage(text="「妳在找這個吧？」日翔做足了心理準備朝曉光遞出學生證。"+"\n"+"「對......謝謝你。」曉光驚訝地道謝接過。"+"\n"+"「不會。」沒想到能有被曉光道謝一天，日翔在心裡默默感謝那個神秘聲音，「我剛剛看了妳的學生證發現我們同一班呢。我叫游日翔，請多指教啦。」和曉光說上話讓日翔心裡感覺輕飄飄的。"))
                list_talk.append(TextSendMessage(text="#4 曉光的學號是「408402132」，請問曉光是民國幾年入學、甲班還是乙班、座號幾號呢？（請以「ＯＯ年、Ｏ班、ＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #4答案
    elif event.message.text=="08年、乙班、13號":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('H'+str(j))
            list.append('I'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="做完簡單自我介紹後，兩人幾乎是沒有什麼更進一步的對話了。一來是因為日翔本來就不是很了解曉光，在過去別說是互動了，他們甚至連招呼都沒有打過！再來是因為上學第一天重逢女神的衝擊，日翔在歸還學生證後也緊張地幾乎擠不出什麼話。不過曉光似乎是無所謂的感覺，或許她本來就比較喜歡安靜的環境？"+"\n"+"終於到了輔大站，日翔和曉光兩人像是約好一樣從出車廂維持著日翔在前曉光在後跟著，日翔對此並沒有任何表示，反正兩人目的本來就是一樣的。回到了母校輔大，日翔從遠處就能看得見的白色三面水泥柱，代表三個教會團體共同復校同心協力的精神。上面大大的寫著輔大的中英文全名。"))
                list_talk.append(TextSendMessage(text="#5 輔大英文全名是？"+"\n"+"（Ａ）Fu Jen Catholic University"+"\n"+"（Ｂ）Fu Jen Christian University"+"\n"+"（Ｃ）Fang Jia University"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#5',
                    template=ButtonsTemplate(
                        title='#5',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='Fu Jen Catholic University'
                            ),
                            MessageAction(
                                label='B',
                                text='Fu Jen Christian University'
                            ),
                            MessageAction(
                                label='C',
                                text='Fang Jia University'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
   
    #5答案
    elif event.message.text=="Fu Jen Catholic University":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('I'+str(j))
            list.append('J'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔從畢業後就沒有再回來學校看過了，他甚至不清楚學校是否在他畢業以後有沒有改建過。走進校園，不僅建築物、銅像甚至是一草一木都和日翔記憶中一模一樣……日翔偷偷捏了自己一把，會痛！有這種痛覺應該不是夢吧！？比起對這些，日翔更想親自詢問那聲音是出於什麼理由把自己帶回來，還有他口中的「表現」又是什麼意思，一切都發生得太突然了，讓日翔感到十分困惑。"+"\n"+"不過日翔很快又發現了一件更重要的問題——他沒有帶課表！剛剛趕著出門只把手機、錢包跟家裡鑰匙塞進書包就出門了，他太久沒有上課的經驗，自然是忘記了課表這回事。日翔的記憶力也沒有好到能夠記得好幾年前大一第一堂課在哪間教室上課。怎麼辦，只能問曉光了。"))
                list_talk.append(TextSendMessage(text="「呃……請問妳知道第一堂課的教室在哪裡嗎……」日翔轉向曉光不好意思地詢問，希望自己聽起來並不是在隨便找什麼理由搭訕，「我太急著出門，忘記帶課表了……」"+"\n"+"「LM503，企業概論。」曉光連看都不必看，直接回答了日翔的問題。"+"\n"+"果然是學霸，連課表都背起來了。日翔在心裡讚嘆。"))
                list_talk.append(TextSendMessage(text="#6 「LM」指的是哪棟大樓呢？（請以「ＯＯＯ大樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #6答案
    elif event.message.text=="利瑪竇大樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('J'+str(j))
            list.append('K'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖利瑪竇大樓！趕快去「遊戲地圖」看看！"+"\n\n"+"利瑪竇大樓是法管學院的綜合大樓，為了紀念來華傳教耶穌會士利瑪竇神父，以其名諱命名。資管系的商學課程常常被安排在利瑪竇大樓上課。"+"\n"+"「謝謝，幫大忙了！」日翔向曉光道謝。剛剛才在捷運上被曉光道謝，還真是風水輪流轉。"+"\n"+"「沒什麼。」曉光又補充一句：「校網上的選課清單裡也可以看。」"+"\n"+"對了，還有這招！日翔覺得在女神面前只能緊張到手足無措的自己真的是笨死了……怎麼沒辦法跟遊戲一樣存檔再讓他重新來過呢......"))
                list_talk.append(TextSendMessage(text="一路上日翔很認真地在思考「Code/140.136」讓他回到過去的這件事，日翔起初是不太願意相信的，畢竟這麼不科學的事一般人一時之間也很難接受，不過到現在日翔自己現在也不太確定了......毫無頭緒也只能認命走一步算一步了。"+"\n"+"日翔本來就不是擅長一心多用的人，加上現在一下子又有那麼多事情需要他去思考，導致他開門時沒有注意到環境而和走出來的同學撞個滿懷。"+"\n"+"「呃！對不......起......？」日翔趕緊為了自己的不留神向對方道歉。定睛一看來人不得了，他撞上的竟然是班上的第二個學霸馬宇桓！現在是怎樣？回到學校一開始就接連遇上兩個最強也太刺激了吧？"+"\n"+"馬宇桓在日翔的記憶中總是一副趾高氣昂、不可高攀的樣子，和同為學霸卻不張揚的曉光形成鮮明的對比。日翔還記得宇桓在學校總是處處針對著自己，日翔自己也不是很明白到底哪裡惹到宇桓，明明自己總是在被當掉的邊緣遊走，並不是在意成績的宇桓需要堤防的對象啊......不過還好宇桓「現在」並沒有找他麻煩，只是瞪日翔一眼便皺著眉頭走過去了。"+"\n"+"日翔算晚才進教室，好位置早早就被人挑走了，曉光也在不知不覺間挑好位置開始看書了。日翔正苦惱要坐哪，眼角不經意瞄到角落第一排位置正有個一頭金髮的男同學正趴在桌上睡覺。這不是他的好兄弟——葉司晨嗎！日翔差點笑了出來，也只有司晨這種少根筋的人才會在開學第一天坐在這麼顯眼的位置睡覺了。"+"\n"+"葉司晨是日翔在大學間結交的拜把兄弟，總喜歡幫人取奇奇怪怪的綽號。司晨大咧咧、不拘小節的個性讓日翔相處起來很輕鬆，雖然有時候司晨做事不太可靠，但司晨很講義氣，總是無條件地支持著日翔，日翔很慶幸自己能交到這麼好的兄弟。"+"\n"+"日翔才剛選定好司晨旁邊的位置坐下就打鐘了，「同學，要上課了。」見司晨還沒有起來的意思，日翔便順手推了推司晨。"+"\n"+"「嗚喔！？」聽見要上課了的司晨驚坐起，「謝謝你啊，你人真好！我叫葉司晨，你咧？」司晨給了日翔一個大大的笑容並伸出手。"+"\n"+"「游日翔，請多指教了！」日翔回握道，日翔很確定自己在這一次也能和司晨成為好朋友。"))
                list_talk.append(TextSendMessage(text="早上的課很快地結束了，日翔和司晨兩人一邊聊著天一邊下樓準備去吃午餐。在風華廣場的聲音吸引了兩人的注意。"+"\n"+"「喂喂！那邊在做什麼啊？超熱鬧的！」司晨興奮地瞪大雙眼。要是這裡是漫畫世界，司晨的眼睛裡應該會冒出星星吧。"+"\n"+"「選在開學舉辦，那這應該就是......」"))
                list_talk.append(TextSendMessage(text="#7 請問每年的9月，在風華廣場會舉辦什麼活動？"+"\n"+"（Ａ）社團博覽會"+"\n"+"（Ｂ）星光路跑"+"\n"+"（Ｃ）巧克力傳情"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#7',
                    template=ButtonsTemplate(
                        title='#7',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='社團博覽會'
                            ),
                            MessageAction(
                                label='B',
                                text='星光路跑'
                            ),
                            MessageAction(
                                label='C',
                                text='巧克力傳情'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #7答案
    elif event.message.text=="社團博覽會":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('K'+str(j))
            list.append('L'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「原來是社團招生啊！我們去看看！」司晨頗有興致地拉著日翔晃了一整圈，在發現沒有籃球社後顯得有些失望。"+"\n"+"「那......加入系籃怎麼樣？」日翔提議，在過去日翔和司晨也都有加入系籃，兩人因為同樣的興趣變得要好起來。「對了，在12月也有體育競賽喔，學校會舉辦......」"))
                list_talk.append(TextSendMessage(text="#8 請問每年的12月，學校會舉辦什麼活動？"+"\n"+"（Ａ）煙火大會"+"\n"+"（Ｂ）課堂加退選"+"\n"+"（Ｃ）校慶運動會"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#8',
                    template=ButtonsTemplate(
                        title='#8',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='煙火大會'
                            ),
                            MessageAction(
                                label='B',
                                text='課堂加退選'
                            ),
                            MessageAction(
                                label='C',
                                text='校慶運動會'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #8答案
    elif event.message.text=="校慶運動會":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('L'+str(j))
            list.append('M'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="一提起體育話題，司晨精神都來了，開始喋喋不休地和日翔討論最近的賽事，彷彿和早上趴在桌上睡著的是不同人。司晨十分好動這點還是和日翔記憶中的一模一樣，日翔總是覺得司晨是在面試體育系的時候走錯教室。"+"\n"+"「咕嚕咕嚕──」尷尬的聲音讓兩人同時沉默了下來。"+"\n"+"「呃......抱歉抱歉，我拖太久了我自己都餓了，哈哈。」司晨尷尬地對日翔笑了笑。"+"\n"+"「那我們就吃飽一點，去外面吃吧。」日翔提議，「外面的小巷子聽說有很多好吃的喔。」"))
                list_talk.append(TextSendMessage(text="#9 學校外面藏有很多美食的小巷叫？（請輸入「ＯＯＯ巷」回答，ＯＯＯ為半形數字。） "))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        
    #9答案
    elif event.message.text=="514巷":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('M'+str(j))
            list.append('N'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「好啊！走了走了！早八的課我早餐根本來不及吃都要餓死啦！」一聽見有美食可以吃的司晨立刻舉雙手贊成日翔的提議，「不過阿日你怎麼知道這麼多啊？」"+"\n"+"「哦......我事先查過了啊，哈哈～」日翔含糊地帶過話題，說自己從未來回來的估計誰也不會信，還會被當成瘋子吧！？"+"\n"+"「嘿、那我大學就要靠你罩了，兄弟～」兩人邊打鬧著邊前往514巷。"))
                list_talk.append(TextSendMessage(text="開學最輕鬆的第一個禮拜很快就過去了，日翔漸漸接受起自己回到過去的事實，當然也沒忘記那個聲音要他在學校好好表現。說也奇怪，從那天以後他再也沒有聽到過那個聲音，日翔也無從詢問「好好表現」具體來說要做什麼才能達到標準。即使如此，日翔已經決定他這次要好好把握機會充實自己，不能像以前一樣摸魚度日才在空後悔。"+"\n"+"除了教授指定的書籍以外，日翔決定去多買幾本當參考。一聽見日翔要去書局，司晨立刻表示不奉陪，他才不想去書局這種讓人窒息的地方。"+"\n"+"…...反正你遲早也是要去買指定教科書的，怎麼可能不進書局，日翔默默吐槽。"+"\n"+"記得聖言樓地下室有一間書局？先去那邊看看好了。"))
                list_talk.append(TextSendMessage(text="#10 聖言樓地下室的書局叫？"+"\n"+"（Ａ）金石堂書局"+"\n"+"（Ｂ）敦煌書局"+"\n"+"（Ｃ）誠品書局"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#10',
                    template=ButtonsTemplate(
                        title='#10',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='金石堂書局'
                            ),
                            MessageAction(
                                label='B',
                                text='敦煌書局'
                            ),
                            MessageAction(
                                label='C',
                                text='誠品書局'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))    
    #10答案
    elif event.message.text=="敦煌書局":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('N'+str(j))
            list.append('O'+str(j))
            list.append('B'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(2))
                worksheet.update(list[4],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="書局的冷氣吹散了外頭九月悶熱的暑氣。日翔隨意地在書架間瀏覽，他記得以前只在原子筆沒水才進來過少少幾次，他一直都沒注意到書局旁邊還有「每一杯咖啡」這間咖啡廳？比起外面的書局，校內的書局還是顯得要小很多，日翔很快就挑好了幾本。準備去結帳時，日翔看見了走進來的曉光，而曉光也正好發現了自己。"+"\n"+"小、曉光怎麼在這裡！？雖然喜歡看書的曉光出現在書局也不是很意外。"+"\n"+"「你在選書嗎？」"+"\n"+"「咦？啊啊、對......」曉光主動向自己說話讓日翔又驚又喜。"+"\n"+"不過曉光似乎沒有發現日翔的異樣，她的目光落在日翔捧著的書上，「那個......這些書怎麼了嗎？」查覺到曉光的視線，日翔小心翼翼地出聲詢問。"+"\n"+"曉光搖搖頭，「這兩本是一樣的書，只是封面不一樣。」"+"\n"+"「！？真的耶！」日翔翻起內容才發現裡面的內容寫的一樣，只是順序不一樣罷了。可惡！怎麼有這種無良作者，害日翔差一點花了冤枉錢。「差點花錢買下去了......謝謝妳啊，又被妳幫助了。」日翔努力的擺出笑容掩飾面對曉光的緊張。"+"\n"+"「話說，」日翔一面將書放回書架一面向曉光搭話，「妳剛剛明明連內容都沒看卻知道這兩本是一樣的，難不成妳看過了嗎？」"+"\n"+"「嗯，稍微看過。」稍微看過卻連內容都清楚嗎？日翔笑了笑，不過他不打算將這句話說出口。"+"\n"+"「那妳應該很喜歡看書了？之前看妳都在讀書。」"+"\n"+"「……。」"+"\n"+"「我沒有別的意思！就只是剛好看到！真的不是偷窺！」日翔慌張地解釋，不料聽起來卻像此地無銀三百兩的狡辯。"+"\n"+"「很喜歡。」曉光的嘴角揚起了一個淺淺的弧度，要不是日翔和曉光距離得近，日翔可能會漏看難得出現在曉光臉上的笑容。"+"\n"+"「這、這樣啊。」奇怪？剛才有這麼熱嗎？或許是看見喜歡的人意外的笑容，或許是不曾和曉光講過這麼多話，或許是兩者皆有，日翔感覺自己的臉就像熟透的番茄，而方才還很涼爽的地下室現在就像個大蒸籠，悶得日翔喘不過氣。"+"\n\n"+"解鎖童話書！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="「好——難——」司晨趴在桌上大聲嚷嚷，顯然已經放棄理解螢幕上一行行的程式碼。「怎麼不用中文寫程式一定要用英文啊！」"+"\n"+"「哈哈......系上挑的Python已經算簡單了......」日翔想起過去司晨也這麼跟他抱怨過，以前日翔還跟著附和過呢，不過對於回到過去的日翔來說，現在教的東西對他來說只是一小塊蛋糕。"+"\n"+"「欸欸？所以說還有更難的？騙人的吧......」想到還要面對更加困難的程式語言直接讓司晨失去了夢想。"+"\n"+"「不、不過！其實寫程式運用的邏輯幾乎都是相同的！只要理解這些，其他程式語言阿司也能很快學會的！」見司晨因為自己的話顯得更萎靡了，日翔趕緊出聲安慰。「這樣吧，阿司你哪裡不懂，我都教你！」"+"\n"+"「！阿日！你真是我的救星！」司晨感激地握住了日翔的手。「其實是這些......」"))
                list_talk.append(TextSendMessage(text="#11 python程式碼如下，請問輸出結果為？"+"\n"+"（Ａ）1234"+"\n"+"（Ｂ）0123"+"\n"+"（Ｃ）123"))
                list.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/5YXBG8.png', preview_image_url='https://upload.cc/i1/2022/03/25/5YXBG8.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#11',
                    template=ButtonsTemplate(
                        title='#11',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='1234'
                            ),
                            MessageAction(
                                label='B',
                                text='0123'
                            ),
                            MessageAction(
                                label='C',
                                text='123'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #11答案
    elif event.message.text=="1234":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('O'+str(j))
            list.append('P'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#12 以下語法為Python結構中的？"+"\n"+"（Ａ）array"+"\n"+"（Ｂ）dictionary"+"\n"+"（Ｃ）tuple"))
                list.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/8MeqCO.png', preview_image_url='https://upload.cc/i1/2022/03/25/8MeqCO.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#12',
                    template=ButtonsTemplate(
                        title='#12',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='array'
                            ),
                            MessageAction(
                                label='B',
                                text='dictionary'
                            ),
                            MessageAction(
                                label='C',
                                text='tuple'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #12答案
    elif event.message.text=="dictionary":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('P'+str(j))
            list.append('Q'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「阿日！好厲害！你根本是天才！」司晨看著日翔完成的一題題程式碼驚呼道。"+"\n"+"「不不，天才什麼的......」司晨的誇讚讓日翔有些心虛，日翔當然是不可能告訴司晨其實他已經學過了。"+"\n"+"「既然是天才，想必再困難的題目也難不倒你吧？」冰冷的聲音在兩人背後響起，兩人轉過頭一看發現竟是宇桓。"+"\n"+"「你是誰啊？」查覺到來者不善的司晨先發制人問道。"+"\n"+"宇桓瞥了司晨一眼，「我並不是在跟你說話，我找的是這位『天才』同學。」宇桓語帶嘲諷的強調「天才」兩個字。"+"\n"+"「哼...不過挑戰者先自報門號才符合禮節吧？」宇桓推了推眼鏡繼續說，「我叫宇桓，跟你同班。」"+"\n"+"「呃、宇桓同學？你是不是搞錯什麼......」如果可以，日翔還真不想接受宇桓的「挑戰」。話又說回來，這次還是被宇桓給盯上了嗎？自己到底是哪裡惹到宇桓了呢......"+"\n"+"「搞錯？我可是清清楚楚的聽見這個笨蛋叫你天才。」宇桓像是怕日翔聽不懂一樣一字一字緩緩地說，「怎麼了？該不會是害怕了？」"+"\n"+"「你這人從剛剛就一直瞧不起人啊！」被宇桓直罵的司晨晨憤憤地指著宇桓，「阿日怎麼可能會輸給你！不管你要出幾題阿日都會解開的！」"+"\n"+"「就當你是接受了。」宇桓一臉計畫通地笑了，語氣也不容許日翔拒絕。"+"\n"+"中了宇桓的圈套啊......宇桓想必是針對司晨容易被挑釁這點出手的。看來不解開宇桓的難題，宇桓是不會罷休了。"))
                list_talk.append(TextSendMessage(text="#13 請問下圖最後會出現什麼結果？（請以「Ｏ」回答，Ｏ為半形數字。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/10/J106XE.png', preview_image_url='https://upload.cc/i1/2022/03/10/J106XE.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #13答案
    elif event.message.text=="5050":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('Q'+str(j))
            list.append('R'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#14 下列以Python語法撰寫出的程式碼最後輸出結果為？（請以「x=Ｏ」回答，Ｏ數量不代表實際答案字數。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/uHLoSw.png', preview_image_url='https://upload.cc/i1/2022/03/25/uHLoSw.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #14答案
    elif event.message.text=="x=2500":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('R'+str(j))
            list.append('S'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「哈哈哈阿日你看到宇桓的表情了嗎？說什麼『還在意料內』我看他根本就是被嚇傻了，哈哈哈！」司晨從離開教室後從沒停止過大笑，彷彿是自己解開了宇桓的難題，日翔終於忍不住反手朝司晨的後腦打了一巴掌。"+"\n"+"「好痛！阿日你幹嘛！？變笨了怎麼辦！」司晨吃了痛驚呼道。"+"\n"+"「已經很……咳嗯，我是說，阿司你也長點心眼，被宇桓算計了也不知道！下次你自己回答！」"+"\n"+"「對不起啦阿日！誰叫他一臉欠揍還說我笨嘛！我聽同學說過傳說中的『輔大三寶』，我請你吃阿日你就消氣吧？」司晨趕緊討好地說，「我記得有......」"))
                list_talk.append(TextSendMessage(text="#15 傳說中的「輔大三寶」分別是哪三寶？"+"\n"+"（Ａ）小木屋鬆餅、食科冰淇淋、比臉大雞排"+"\n"+"（Ｂ）巧瑋鬆餅、食科冰淇淋、大菠蘿麵包"+"\n"+"（Ｃ）小木屋鬆餅、食科冰淇淋、大菠蘿麵包"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#15',
                    template=ButtonsTemplate(
                        title='#15',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='小木屋鬆餅、食科冰淇淋、比臉大雞排'
                            ),
                            MessageAction(
                                label='B',
                                text='巧瑋鬆餅、食科冰淇淋、大菠蘿麵包'
                            ),
                            MessageAction(
                                label='C',
                                text='小木屋鬆餅、食科冰淇淋、大菠蘿麵包'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #15答案
    elif event.message.text=="巧瑋鬆餅、食科冰淇淋、大菠蘿麵包":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('S'+str(j))
            list.append('T'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(2))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「對了！我請你吃鬆餅！阿日你就原諒我啦！」日翔看著友人拼命討好自己的樣子，氣也消了大半，該不會這就是有個需要人照顧的弟弟的感覺？"+"\n"+"「好啦，你要說話算話喔！」"+"\n"+"「嘿嘿～當然了！說謊的人要吞一千根針！」見日翔終於氣消，司晨才鬆一口氣恢復了平常傻呼呼的笑容。"))
                list_talk.append(TextSendMessage(text="兩人有說有笑地來到心園，心園位於信義和平宿舍的地下室，因此第一次去不注意環境的話很可能會錯過。心園除了有輔大三寶之一的鬆餅外，也提供便宜的果汁、餐點，甚至還有雜貨店等，因此被眾多學生評價為CP值最高的學餐。"+"\n"+"為了解開宇桓的難題花了一些時間，所幸今天教授提早下課，因此兩人來到心園時還沒有什麼人。當他們來到鬆餅店前，他們發現了曉光站在招牌前，似乎還在猶豫要點什麼。"+"\n"+"「曉光？你也來買鬆餅嗎？」自從上次在書局跟曉光講話後，日翔和曉光講話已經不會那麼緊張了，甚至在課堂上見面時還會和對方打聲招呼。"+"\n"+"「嗯。還在想要點什麼。」"+"\n"+"「哈哈、畢竟菜單很多選擇，連鹹的口味也有。」日翔想起第一次買鬆餅時，也因為五花八門的口味而思考了很久要買什麼。"+"\n"+"在徵得曉光同意一起點餐後，日翔幫自己點了玉米蔬菜、司晨的蜂蜜奶油以及曉光的鮮奶油。"+"\n"+"「阿司你的加上我的95元，曉光的……怎麼了嗎？」日翔察覺到曉光似乎有些慌張。"+"\n"+"「……沒有足夠的零錢……只有大鈔……」天要塌下來了嗎？還是今天的太陽是從西邊出來的？居然能在有生之年看見曉光出亂子的時候……不對啦！到底在想什麼啊？"+"\n"+"「這樣啊……那不用給我了。」看見曉光臉上堆滿疑惑，日翔繼續解釋，「呃、我的意思是，上次妳不是在書局幫了我嗎？當成那次的回禮好了。」"+"\n"+"曉光正想說什麼，一旁的司晨插嘴：「欸——阿日要請客喔？那我也要！」"+"\n"+"「反了吧阿司！你剛才才說過要請我吧！」"+"\n"+"幸好最後曉光同意了日翔這次的請客，還順帶一起請了司晨。（雖然應該是因為不太好意思和店家直接換大鈔吧，日翔想。）要是曉光拒絕了，日翔可能會尷尬得想立刻逃離現場。日翔本來以為自己的請客發言會表現得很帥，沒想到居然那麼羞恥……跟喜歡的人說話真難啊……"+"\n\n"+"解鎖遊Ｏ王卡！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="時間很快地過去，讓大家最頭痛的期中考也悄悄地來了。幸好日翔還保有過去的記憶，重理解一次課程上的問題對他來說並不困難，甚至還有一點餘韻應付宇桓時不時拋過來的刁難及幫助司晨在課業上的問題。"+"\n"+"請完成以下題目安全度過期中考："))
                list_talk.append(TextSendMessage(text="#16 y=(5x+6)^10，則y'=？"+"\n"+"（Ａ）10*(5x+6)^9"+"\n"+"（Ｂ）50*(5x+6)^9"+"\n"+"（Ｃ）50x+60"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#16',
                    template=ButtonsTemplate(
                        title='#16',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='10*(5x+6)^9'
                            ),
                            MessageAction(
                                label='B',
                                text='50*(5x+6)^9'
                            ),
                            MessageAction(
                                label='C',
                                text='50x+60'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))


    elif event.message.text=="遊戲規則":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="本遊戲是採用回答問題的遊玩方式進行闖關！！"+"\n"+"玩家回答出遊戲內關卡的問題，透過回答問題一步步解鎖劇情✨"+"\n"+"若是問題回答不出來時可以參考下面網站裡的解題技巧喔٩( 'ω' )و "+"\n"+"玩家從個人檔案中觀看目前選擇視角、已解鎖物件，想重新體驗遊戲或選擇不同視角可以輸入「重置遊戲」喔✨"+"\n\n"+"最後祝各位玩家遊玩愉快🥳"))
    elif event.message.text=="人物介紹":
        carousel_template_message = TemplateSendMessage(
            alt_text='人物介紹',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/30/K9D6Xw.jpg?fbclid=IwAR3TXV-o2OBUFuPpOursWi-w4pik7hG__iqpSahR59P7CcBaeb76ZvWKQPM',
                        title='游日翔',
                        text='心思細膩的青年',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='日翔角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/30/dRcCSl.jpg?fbclid=IwAR0LgBlXQ2LP-Ag99jBXJALWmbv2zF-DUX9BXp6dTEGn494AIAUKrxOr6q4',
                        title='何曉光',
                        text='研精靜慮的才女',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='曉光角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/03/8rgJCv.png',
                        title='葉司晨',
                        text='陽光朝氣的笨蛋',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='司晨角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/15/yvIkxV.png',
                        title='林真澄',
                        text='塔羅占卜的能手',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='真澄角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/03/UvGMpX.png',
                        title='馬宇恒',
                        text='自視甚高的學霸',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='宇恒角色資料'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    elif event.message.text=="日翔角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="誤打誤撞考上輔大資管系的普通學生日翔，在學間遇到自己的真命天女——曉光，卻因為成績差而不敢進一步追求。內心思緒豐富喜歡吐槽，且觀察力十分敏銳，總能注意到一些小細節。稱呼死黨司晨為「阿司」。"))
    elif event.message.text=="曉光角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以在校成績第一繁星進入輔大資管系，一有空閒就會拿書出來閱讀。平時都擺著一張撲克臉，讓人難以親近的樣子。除了與好友真澄的關係比較親密之外，鮮少看到她與其他人有互動。但若吃到學校的食科冰，臉上便會洋溢出幸福的笑容。家裡養了一隻叫德魯貝的貓。"))
    elif event.message.text=="司晨角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="日翔的死黨。和日翔一起去打籃球、吃飯、上課，雖然總是冒冒失失的，但一直都把朋友擺在第一位，偶爾會顯得可靠。喜歡幫人取奇怪的綽號，稱呼日翔為「阿日」。"))
    elif event.message.text=="宇恒角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="擅長讀書跟coding，總是與曉光角逐班上的一二名。宇桓也喜歡同為學霸的曉光，為了不讓日翔靠近曉光，常常提出問題刁難日翔。出手闊綽，家裡似乎很有錢，把領到的書卷獎當零頭。"))
    elif event.message.text=="真澄角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="曉光在通識課程中認識的甲班同學，對任何人最初都抱有警戒心，熟識後會發現真澄只是不知如何開口向他人表達關心。對自我要求很高，課程總是排得很滿，因此常常衝堂改修乙班的課。"))
    
    elif event.message.text=="個人檔案":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            #玩家名稱
            user_id = event.source.user_id
            profile = line_bot_api.get_profile(user_id)         
            #從exccel取學分
            x=len(userid_list)
            list=[]
            for i in range(x):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            #建築、物件、視角
            list.append('B'+str(j))
            list.append('C'+str(j))
            list.append('D'+str(j))
            #找關卡代號為1
            for i in range(4,len(worksheet.row_values(j))):
                if worksheet.row_values(j)[i]=="1":
                    ques=str(i-3)
            #還沒選擇視角
            if worksheet.acell(list[2]).value=="0":
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='選擇視角',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://upload.cc/i1/2022/03/30/K9D6Xw.jpg?fbclid=IwAR3TXV-o2OBUFuPpOursWi-w4pik7hG__iqpSahR59P7CcBaeb76ZvWKQPM',
                                action=MessageTemplateAction(
                                    label='日翔',
                                    text='以日翔的視角進行遊戲'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://upload.cc/i1/2022/03/30/dRcCSl.jpg?fbclid=IwAR0LgBlXQ2LP-Ag99jBXJALWmbv2zF-DUX9BXp6dTEGn494AIAUKrxOr6q4',
                                action=MessageTemplateAction(
                                    label='曉光',
                                    text='以曉光的視角進行遊戲'
                                )
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token,image_carousel_template_message)
            #日向視角
            elif worksheet.acell(list[2]).value=="1":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【"+worksheet.acell(list[1]).value+"/8】"))
            #小光視角
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="玩家選擇視角：小曉"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【"+worksheet.acell(list[1]).value+"/8】"))   
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒開始遊戲喔，請輸入「開始遊戲」建立個人檔案。"))

    elif event.message.text=="重置遊戲":
        userid_list=worksheet.col_values(1)
        #已寫入ID
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            worksheet.delete_row(j)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已重置遊戲，請輸入「開始遊戲」。"))
        #未寫入ID
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立開始遊戲喔，請輸入「開始遊戲」建立個人檔案。"))
    elif event.message.text=="遊戲地圖":
        carousel_template_message = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message2 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message3 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message4 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://mapio.net/images-p/84019119.jpg',
                        title='進修部',
                        text='成功解鎖進修部！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message5 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://mapio.net/images-p/84019119.jpg',
                        title='進修部',
                        text='成功解鎖進修部！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/sqlb3OC.jpeg',
                        title='伯達樓',
                        text='成功解鎖伯達樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='伯達樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message6 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/6/68/FJU_SSMG01.jpg',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://mapio.net/images-p/84019119.jpg',
                        title='進修部',
                        text='成功解鎖進修部！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/sqlb3OC.jpeg',
                        title='伯達樓',
                        text='成功解鎖伯達樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='伯達樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ppt.cc/f3IHdx@.jpg',
                        title='濟時樓',
                        text='成功解鎖濟時樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='濟時樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message7 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/6/68/FJU_SSMG01.jpg',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://mapio.net/images-p/84019119.jpg',
                        title='進修部',
                        text='成功解鎖進修部！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/sqlb3OC.jpeg',
                        title='伯達樓',
                        text='成功解鎖伯達樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='伯達樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ppt.cc/f3IHdx@.jpg',
                        title='濟時樓',
                        text='成功解鎖濟時樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='濟時樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/dx980Kw.jpeg',
                        title='中美堂',
                        text='成功解鎖中美堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='中美堂介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message8 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photox.pchome.com.tw/s13/moni101/112/135200602386/',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://pic.pimg.tw/fjumyblog/4a128e07da7c5_wn.jpg',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/FJU_Religion03.jpg/800px-FJU_Religion03.jpg',
                        title='淨心堂',
                        text='成功解鎖淨心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='淨心堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://mapio.net/images-p/84019119.jpg',
                        title='進修部',
                        text='成功解鎖進修部！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/sqlb3OC.jpeg',
                        title='伯達樓',
                        text='成功解鎖伯達樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='伯達樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ppt.cc/f3IHdx@.jpg',
                        title='濟時樓',
                        text='成功解鎖濟時樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='濟時樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/dx980Kw.jpeg',
                        title='中美堂',
                        text='成功解鎖中美堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='中美堂介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://fastly.4sqi.net/img/general/784x588/43402781_EW7mtusxKDYOM_Og5v3k7sFac_UPy0JeNmwAnTUQWgw.jpg',
                        title='野聲樓',
                        text='成功解鎖野聲樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='野聲樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        #施工中
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('B'+str(j))
            rep_arr=[]
            if worksheet.acell(list[0]).value=="0":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【0/8】"))
                rep_arr.append(TextSendMessage(text="還沒解鎖任何建築！趕快去回答問題解鎖吧！"))
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="1":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【1/8】"))
                rep_arr.append(carousel_template_message)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="2":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【2/8】"))
                rep_arr.append(carousel_template_message2)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="3":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【3/8】"))
                rep_arr.append(carousel_template_message3)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="4":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【4/8】"))
                rep_arr.append(carousel_template_message4)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="5":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【5/8】"))
                rep_arr.append(carousel_template_message5)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="6":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【6/8】"))
                rep_arr.append(carousel_template_message6)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            elif worksheet.acell(list[0]).value=="7":
                rep_arr.append(TextSendMessage("建築物解鎖進度：【7/8】"))
                rep_arr.append(carousel_template_message7)
                line_bot_api.reply_message(event.reply_token,rep_arr)
            else:
                rep_arr.append(TextSendMessage("建築物解鎖進度：【8/8】"))
                rep_arr.append(carousel_template_message8)
                line_bot_api.reply_message(event.reply_token,rep_arr)   
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))
    elif event.message.text=="利瑪竇大樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="利瑪竇大樓為法管學院綜合大樓，呈現「T」字形，於1986年落成，為紀念來華傳教的耶穌會會是利瑪竇神父，特意以其姓名命名，在利瑪竇大樓的前庭、後廳大理石地板，還鑲嵌著輔仁校訓「真善美聖」的拉丁文。利瑪竇為天主教在中國傳教的開拓者之一，除了傳播天主教福音之外，他還結交許多中國官員，教導天文、數學、地理等西方科學知識，因而獲得「泰西儒士」的尊稱。《坤輿萬國全圖》則是利瑪竇為中國所製作的世界地圖，問世後不久即被傳入日本，對於亞洲地理學的發展產生重要影響。"))
    elif event.message.text=="中美堂介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="中美堂是學校體育館，屬於大型活動的集會場所，由聖言會會士、德國人林慎白總建築師，及我國專家陳濯、李實鐸、沈大魁、趙楓等四位合作規劃而成，象徵古羅馬競技精神的圓形建築，遠看狀似北平天壇，取前總統蔣中正以及前董事長蔣宋美齡名字各一字，簡稱中美堂。"))
    elif event.message.text=="聖言樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="代號SF，主要科系為電子系與資工系，而資管系的資料結構、網路設計課程安排在此棟建築物授課。地下室具有敦煌書局，內部除了各大科系的教科書、文具以外，還具備蘋果專區和餐廳，相當便利。"))
    elif event.message.text=="靜心堂介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="淨心堂位於外語學院跟法管學院之間，圓環的旁邊喔。於民國66年落成，整體外觀為白色，乃前任校長羅光總主教選定的顏色，代表純潔肅穆莊嚴。在建築風格上非常特別，結合了科學、藝術、宗教等等，可以在外觀上找到字母Α和字母Ω。"))
    elif event.message.text=="野聲樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="野聲樓為輔大的行政中心，所有行政辦公室都設置在此處，包含校長室秘書室、人事室、會計室、會議室、註冊組、教務處、課務組、軍訓室、公共事務室、生活輔導組、出納組，谷欣廳⋯⋯等等；此外，在野聲樓四樓設有中國天主教文物館、校史館、于斌樞機紀念館，可供民眾預約參觀，以便更了解輔仁大學的歷史背景。「野聲」取自輔大第一任校長于斌樞機主教的字號，源於聖經中聖洗者若翰曠「野」的呼「聲」，有趣的是，在野聲樓外頭也豎立著于斌樞機主教的雕像，和野聲樓相映對照，透過此空間規劃間接說明輔大創建的校史。"))
    elif event.message.text=="濟時樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="濟時樓圖書總館館舍總面積約3500坪，閱覽席位1062席、全館無線網路(SSID FJU)、學習共享空間與檢索查詢之電腦設備92組、研究小間28間、團體討論室7間。二樓為圖書館入口、借閱櫃台、參考服務區、資訊檢索區、指定參考書區、新書展示區、學習共享空間、寫作中心及閱報區；三樓為現期期刊區、學位論文區及參考書區；四樓為期刊室（含合訂本報紙）；五至七樓為中西文書庫；八樓為辦公室。"))
    elif event.message.text=="伯達樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="代號BS，所屬科系為社會科學系、法律學系，資管系的資料庫管理和作業系統課程也在此授課。建築意義：愛護真理、保護青年的張伯達神父（1905-1951致命殉道），他常說：現代青年該具有團結、合作、謙虛、仁恕、急公、好義等社會道德，還要有創造力。這樣，一旦跨出校門，不但能夠適應社會，在社會中生存，更能領導社會，改造社會，做社會中堅份子。"))
    elif event.message.text=="進修部大樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輔大進修部的前身是輔大夜間部，自民國五十八年成立迄今已五十餘年。秉持天主教的辦學理念與宗旨，以全人教育為目標；秉持真、善、美、聖的校訓，提供一個終生學習的環境，為社會國家造就許多人才。"+"\n"+"本部下轄8個學系及10個學士學位學程，致力培養學生具備廣博的知識及精進的專業能力，並培育學生具有人文素養、人本情懷、人際溝通與思惟判斷能力之完備的社會人。"))
    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)