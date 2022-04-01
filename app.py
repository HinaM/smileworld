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
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/5YXBG8.png', preview_image_url='https://upload.cc/i1/2022/03/25/5YXBG8.png'))
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
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/8MeqCO.png', preview_image_url='https://upload.cc/i1/2022/03/25/8MeqCO.png'))
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
    
    #16答案
    elif event.message.text=="10*(5x+6)^9":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('T'+str(j))
            list.append('U'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#17 y=e^(2x)，則y'=？"+"\n"+"（Ａ）2xe^(2x)"+"\n"+"（Ｂ）2e^(2x)"+"\n"+"（Ｃ）2e^x"+"\n"+"（Ｄ）e^x"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#17',
                    template=ButtonsTemplate(
                        title='#17',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='2xe^(2x)'
                            ),
                            MessageAction(
                                label='B',
                                text='2e^(2x)'
                            ),
                            MessageAction(
                                label='C',
                                text='2e^x'
                            ),
                            MessageAction(
                                label='D',
                                text='e^x'
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

    #17答案
    elif event.message.text=="2e^(2x)":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('U'+str(j))
            list.append('V'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#18 下列何者為會計恆等式？"+"\n"+"（Ａ）資產 = 負債 + 權益"+"\n"+"（Ｂ）資產 – 權益 = 存貨"+"\n"+"（Ｃ）資產 = 權益"+"\n"+"（Ｄ）負債 = 權益 – 資產"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#18',
                    template=ButtonsTemplate(
                        title='#18',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='資產 = 負債 + 權益'
                            ),
                            MessageAction(
                                label='B',
                                text='資產 – 權益 = 存貨'
                            ),
                            MessageAction(
                                label='C',
                                text='資產 = 權益'
                            ),
                            MessageAction(
                                label='D',
                                text='負債 = 權益 – 資產'
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

    #18答案
    elif event.message.text=="資產 = 負債 + 權益":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('V'+str(j))
            list.append('W'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="期中考的分數公布下來後，日翔考了一個不錯的分數，司晨也在日翔的幫（洩）助（題）下安全地擦邊通過了期中考。"+"\n"+"「阿日！你看！我活到現在第一次考這麼高欸！」司晨興奮地將考卷舉到日翔面前，「阿日你怎麼猜題都猜得那麼準啊！」"+"\n"+"「就、剛好從學長姐那邊拿到考古題啦～」"+"\n"+"「真好啊！那我期末也靠你罩了啊！」"+"\n"+"日翔有時很慶幸還好司晨並不會過問那麼多，他可不擅長撒謊啊！"+"\n"+"「曉光呢？考得怎麼樣？」日翔轉頭詢問坐在兩人後面的曉光，但其實日翔不需要問也知道結果了，曉光可是提高班上平均分數的大學霸啊。"+"\n"+"「還行。」曉光給了日翔一個模稜兩可的回答，不過日翔聽得出曉光語氣裡的透露了一絲喜悅，看來考試的結果也讓曉光很滿意呢。"))
                list_talk.append(TextSendMessage(text="在輔大大學入門課程中，為了讓學生更加了解校園環境，學校會安排學生參觀校史室跟淨心堂這兩項活動。"))
                list_talk.append(TextSendMessage(text="#19 校史館在哪一棟建築的二樓呢？（請以「ＯＯ樓二樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #19答案
    elif event.message.text=="野聲樓二樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('W'+str(j))
            list.append('X'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="校史室位於野聲樓二樓，就像一座位於輔大的小型博物館，存放著從開校以來到現今所保存的各種珍貴文物。校史室不僅只是展示，更是保存、傳承下發生在輔大的故事。"))
                list_talk.append(TextSendMessage(text="#20 在大學入門課程中，導師會帶學生去什麼地方傾聽神父的禱告呢？"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #20答案
    elif event.message.text=="淨心堂":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('X'+str(j))
            list.append('Y'+str(j))
            list.append('C'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(3))
                worksheet.update(list[4],int(3))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖淨心堂！趕快去「遊戲地圖」看看！"+"\n\n"+"眾所皆知輔大是天主教大學，當然少不了大型教堂，淨心堂開放也開放讓非天主教教徒進入禱告，走在輔大校園內也可以看見一些神父及修女。此外，除了淨心堂，輔大校內也設有淨心室讓同學進入沉澱心靈。淨心堂和日翔以往在電視影集上看到的教堂不太一樣，淨心堂的座位六個一排呈半圓狀，可以容納至少一個班級以上的學生數量，和日翔印象中的兩個一排的教堂有所不同。"+"\n"+"無論是從窗戶照進來的和煦陽光，還是神父溫厚的聲音都讓人感到十分舒適，甚至讓日翔的眼皮越發沉重。日翔揉了揉眼睛想驅散睡意，卻發現隔壁的司晨已經開始有一下沒一下地點頭打起瞌睡了。在抵抗了一會，日翔最終也敵不過睡魔緩緩閉上雙眼——"+"\n"+"再次睜開雙眼，日翔看見的是一張空白的圖畫紙，還有一隻小手正握著蠟筆努力的在白紙上畫著什麼。從這個視角看來，自己應該是變成了小手的主人，日翔試著移動身體卻只是徒勞，小手的主人目前似乎不打算做塗鴉以外的事。"+"\n"+"不知過了多久，日翔的視線終於從圖畫紙上移開，他看見一個面容模糊的小孩子正常自己走來。日翔可以感覺到他的嘴巴正一開一闔的，似乎在跟那孩子說些什麼？不過他們的聲音卻傳不進日翔的耳裡，好像隔得好遠好遠......"+"\n"+"「——日！阿日！」司晨的呼喚聲讓日翔從睡夢中驚醒過來。"+"\n"+"「欸、欸？我睡著了嗎！？」日翔記得自己只是想閉目養神一下子的。"+"\n"+"「睡得可熟啦！你看你還流口水！」司晨指了指日翔的嘴角。"+"\n"+"「口水！？」日翔連忙伸向司晨指示的地方，卻沒有預想中濕滑的觸感。"+"\n"+"「噗、哈哈哈騙你的啦！」見日翔上當後司晨憋不住放聲笑了出來，日翔則給了後者一個大白眼。"+"\n"+"日後日翔回憶起那個沒頭沒尾的夢，竟有種說不出的熟悉感，好像從很久很久以前就認識了那個面容模糊的孩子......"))
                list_talk.append(TextSendMessage(text="解鎖圖畫！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="#21 日翔下一節課在進修部上課，請問以下哪個課程最可能在進修部大樓上課呢？"+"\n"+"（Ａ）微積分"+"\n"+"（Ｂ）會計"+"\n"+"（Ｃ）通識"+"\n"+"（Ｄ）統計學"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#20',
                    template=ButtonsTemplate(
                        title='#20',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='微積分'
                            ),
                            MessageAction(
                                label='B',
                                text='會計'
                            ),
                            MessageAction(
                                label='C',
                                text='通識'
                            ),
                            MessageAction(
                                label='D',
                                text='統計學'
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

    #21答案
    elif event.message.text=="通識":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('Y'+str(j))
            list.append('Z'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖進修部！趕快去「遊戲地圖」看看！"+"\n\n"+"日翔其實很喜歡通識課程，除了系上排除課程外，在通識課可以學到各領域的知識。日翔這次很幸運地選上了過去在DCard上大家都很推薦卻一直沒有選上的課程，不過......"+"\n"+"「太慢了！」日翔才找到位置坐下，立刻遭到宇桓的斥責。沒錯，籤王日翔，雖然選上了喜歡的課，但他沒料到宇桓也選了同一門課，甚至連分組報告也和宇桓同一組。"+"\n"+"「根本還沒開始上課啊......」日翔小聲地抱怨。"+"\n"+"一開始在通識教室裡看見宇桓時，日翔差那麼一點點🌌🤏想直接退選出去了，但學校規定："))
                list_talk.append(TextSendMessage(text="#22 學校規定通識該修滿哪些領域各4學分呢？"+"\n"+"（Ａ）藝術與人文（含歷史）、社會科學、自然與科技"+"\n"+"（Ｂ）資訊與科技、社會正義、宗教與信仰（含歷史）"+"\n"+"（Ｃ）人類與文明（含歷史）、社會科技、自然與變遷"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#22',
                    template=ButtonsTemplate(
                        title='#22',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='藝術與人文（含歷史）、社會科學、自然與科技'
                            ),
                            MessageAction(
                                label='B',
                                text='資訊與科技、社會正義、宗教與信仰（含歷史）'
                            ),
                            MessageAction(
                                label='C',
                                text='人類與文明（含歷史）、社會科技、自然與變遷'
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
    
    #22答案
    elif event.message.text=="藝術與人文（含歷史）、社會科學、自然與科技":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('Z'+str(j))
            list.append('AA'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="學校規定通識課程必須修滿三領域共12學分，有些人會選擇在大一二修完通識，好讓大三以後有更多時間對未來做規劃。日翔並不想拖延到大三大四跟學弟妹搶通識名額，也不想白白錯過難得選上的通識課，只好硬著頭皮留了下來並祈禱宇桓不會發現自己。然而這就是「墨菲定律」嗎？越是不想遇到的狀況都讓日翔遇上了。"+"\n"+"在過去日翔沒有跟宇桓同組過，宇桓總是跟班上那些優秀的同學在一塊。然而在這次分組機會下日翔發現，宇桓雖然很喜歡碎碎念並對他人指手畫腳，不過宇桓其實是神一般的隊友。宇桓總能迅速劃分好工作並完成，對分組報告來說宇桓可說是一大助力，也是因為如此日翔才能在通識課程中輕鬆地完成分組報告。"+"\n"+"「報告呢？該不會沒做吧？」宇桓坐在旁邊環抱雙臂斜眼看著日翔，宇桓這種高高在上的態度讓日翔一度想起前公司晨的慣老闆。自開學以來、應該是說從第一次大學生活到現在，宇桓沒少對日翔尖酸的話語，日翔也已經習慣了。"+"\n"+"「早就做好了。」日翔從書包裡抽出報告交給宇桓過目。"+"\n"+"「普普通通。」宇桓隨意翻過日翔的報告後給了一個評語。"+"\n"+"……普普通通是什麼啊！你是這堂課的教授嗎！？日翔怒不敢言，雖然說因為宇桓的能力讓日翔在通識報告中不需要花費太多心力，但還是希望宇桓能少刁難自己啊！"))
                list_talk.append(TextSendMessage(text="一連下好幾周的雨終於放晴了，日翔覺得雨再下下去自己都要發霉了。好消息是班代在班群宣布今天體育課終於可以到籃球場打球了！日翔都能看到司晨在宿舍聽到消息後歡呼擾人清夢的樣子了。"))
                list_talk.append(TextSendMessage(text="#23 以下關於輔仁大學與體育相關的敘述何者正確？"+"\n"+"（Ａ）大一體育必修0學分"+"\n"+"（Ｂ）大二體育必修4學分"+"\n"+"（Ｃ）校園內有排球場、籃球場和網球場"+"\n"+"（Ｄ）位於積健樓的游泳池總長有25公尺"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#23',
                    template=ButtonsTemplate(
                        title='#23',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='大一體育必修0學分'
                            ),
                            MessageAction(
                                label='B',
                                text='大二體育必修4學分'
                            ),
                            MessageAction(
                                label='C',
                                text='校園內有排球場、籃球場和網球場'
                            ),
                            MessageAction(
                                label='D',
                                text='位於積健樓的游泳池總長有25公尺'
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

    #23答案
    elif event.message.text=="大一體育必修0學分":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AA'+str(j))
            list.append('AB'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="在輔大體育課都是0學分，且大一二都為必修課程。對某些主張「大學生就是要軟爛！」的人來說體育課非常麻煩，恨不得能翹就盡量翹，但對日翔跟司晨來說，體育課就是能讓他們發洩過剩體力最好的時間，兩人總是很期待一周一次的體育課。"+"\n"+"不像日翔在高中體育課那樣，老師會強迫大家動起來，在大學，體育課教授比較睜一隻眼閉一隻眼，只要完成指定活動就可以在旁邊休息或自由活動。"+"\n"+"大概是悶太久了，司晨一聽見可以自由活動就像脫韁野馬般，立刻衝向籃框挑了顆球並揪上日翔和幾個朋友。剛下完雨的球場地板還殘留著一個個大小水坑，要是有一個不注意可能會重心不穩跌倒——就像司晨現在這樣。"+"\n"+"司晨不顧球場的濕滑及教授的提醒，硬是在三分球線上用力蹬起，想帥氣地投籃大顯身手。不過卻因為抓地力不足的關係，司晨在起跳時腳下一滑，雖然勉強保持住身體平衡，投出的球卻不受控制地往其他方向飛去——幸虧站在較遠處盯防的日翔眼急手快，一個箭步上前攔下了亂飛的球，才沒有打到場外的人。"+"\n"+"「沒事吧！？」日翔轉頭詢問。原來在場外休息的是體力欠佳的曉光和她的朋友，隔壁班的林真澄。兩人看起來還是有點驚魂未定的樣子，曉光很快調整好狀態並對日翔擺擺手表示沒事，真澄卻不然，把跑過來道歉的司晨狠狠地數落了一頓。"+"\n"+"不但耍帥失敗，還被訓了一頓的司晨垂頭喪氣地回到球場。眾人見狀，圍上前拍了拍司晨的肩膀，「活該吧你。」「被罵了齁！」「丟臉啊丟臉！」大家異口同聲地接連虧損。"+"\n"+"「喂喂！我還以為你們要安慰我！」司晨不滿地對眾人抱怨道。接連便是難懂的話，什麼「三分球多難投」，什麼「啊我就怕被罵啊」之類，引得眾人都鬨笑起來：球場充滿了快活的空氣。"))
                list_talk.append(TextSendMessage(text="時間過得飛快，期末考很快就到來了。請完成期末考："))
                list_talk.append(TextSendMessage(text="#24 九月一日支付6個房租$12,000採預付租金入帳。假設公司僅於每年年底做調整分錄，則該年年底之調整分錄為："+"\n"+"（Ａ）借：預付房租$8,000，貸：房租費用$8,000"+"\n"+"（Ｂ）借：房租費用$4,000，貸：預付房租$4,000"+"\n"+"（Ｃ）借：房租費用$8,000，貸：預付房租$8,000"+"\n"+"（Ｄ）借：預付房租$4,000，貸：房租費用$4,000"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#24',
                    template=ButtonsTemplate(
                        title='#24',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='借：預付房租$8,000，貸：房租費用$8,000'
                            ),
                            MessageAction(
                                label='B',
                                text='借：房租費用$4,000，貸：預付房租$4,000'
                            ),
                            MessageAction(
                                label='C',
                                text='借：房租費用$8,000，貸：預付房租$8,000'
                            ),
                            MessageAction(
                                label='D',
                                text='借：預付房租$4,000，貸：房租費用$4,000'
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

    #24答案
    elif event.message.text=="借：房租費用$8,000，貸：預付房租$8,000":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AB'+str(j))
            list.append('AC'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#25 公司帳上各科目之正常餘額為：現金$20,000、應收帳款$50,000、備抵壞帳$5,000、設備$600,000、應付帳款$45,000、短期借款$100,000、股本$500,000、保留盈餘$20,000。若發生以現金支付水電費後，則資產總額何者正確："+"\n"+"（Ａ）資產總額$669,000"+"\n"+"（Ｂ）資產總額$146,000"+"\n"+"（Ｃ）資產總額$664,000"+"\n"+"（Ｄ）資產總額$521,000"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#25',
                    template=ButtonsTemplate(
                        title='#25',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='資產總額$669,000'
                            ),
                            MessageAction(
                                label='B',
                                text='資產總額$146,000'
                            ),
                            MessageAction(
                                label='C',
                                text='資產總額$664,000'
                            ),
                            MessageAction(
                                label='D',
                                text='資產總額$521,000'
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

    #25答案
    elif event.message.text=="資產總額$664,000":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AC'+str(j))
            list.append('AD'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#26 在html語法中，以何種語法設定分頁標題？"+"\n"+"（Ａ）<strong>輔大資管系</strong>"+"\n"+"（Ｂ）<p>輔大資管系</p>"+"\n"+"（Ｃ）<title>輔大資管系</title>"+"\n"+"（Ｄ）<h1>輔大資管系</h1>"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fsCzxx@.png', preview_image_url='https://ppt.cc/fsCzxx@.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#26',
                    template=ButtonsTemplate(
                        title='#26',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='<strong>輔大資管系</strong>'
                            ),
                            MessageAction(
                                label='B',
                                text='<p>輔大資管系</p>'
                            ),
                            MessageAction(
                                label='C',
                                text='<title>輔大資管系</title>'
                            ),
                            MessageAction(
                                label='D',
                                text='<h1>輔大資管系</h1>'
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
    
    #26答案
    elif event.message.text=="<title>輔大資管系</title>":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AD'+str(j))
            list.append('AE'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="早早完成考試的日翔交了卷走出考場，最後一科剛好是許多學生眼中最「硬核」的考科，因此像日翔一樣提早交卷的學生只有少少幾人，大多不是對自己很有信心，就是早已放棄打算明年再重修。"+"\n"+"時間已經來到六月底，距離日翔回到過去也快要過了一年。在這一年間，日翔找不到任何關於那個神祕聲音的線索，但他並沒有忘記自己在出社會後滿滿的後悔感，也沒有忘記執行「Code/140.136」時想重回大學把握時光的決心。日翔認真地度過每一天，雖然不知道有沒有符合神秘聲音對他的期待，但日翔認為這是報答他最好的方式了。"+"\n"+"天空的湛藍讓日翔想起了曉光那寶石般閃耀的雙眸，「如果我能變成更好的人，曉光會不會注意到我呢......」日翔用只有自己能聽到的聲音低喃道。"))
                list_talk.append(TextSendMessage(text="解鎖大二劇情"))
                list_talk.append(TextSendMessage(text="日翔睜開雙眼，只見自己竟然置身於一團迷霧之中，他將自己的雙臂前伸，卻沒能清楚看見自己的手，這大概就是｢伸手不見五指｣吧，日翔迷迷糊糊地想。比起這個，這到底是什麼地方？雖然對這裡完全感到陌生，但卻一點都不令人感到害怕。"+"\n"+"「呼啊——好久不見啦。」頓時，整個空間傳來熟悉的聲音，日翔甚至都沒有整理好思緒就被他給驚乍住了；而且，聽起來他甚至在慵慵懶懶地打著呵欠？"+"\n"+"日翔對這個聲音十分印象深刻，畢竟，去年帶他回到大一生活的那個「code140.136」回傳的瞬間，也聽到了與他別無二致的聲音。不僅如此，日翔隱隱約約感受到，這位就是這個迷霧空間的主人。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=ButtonsTemplate(
                        title='？？',
                        text='這裡是哪裡？你到底是誰？為什麼要讓我回到大學生活？',
                        actions=[
                            MessageAction(
                                label='？？',
                                text='這裡是哪裡？你到底是誰？為什麼要讓我回到大學生活？'
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

    #??
    elif event.message.text=="這裡是哪裡？你到底是誰？為什麼要讓我回到大學生活？":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AE'+str(j))
            #ID已寫入、日向視角、AE=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage(text="滿腔的疑問終究淹沒了日翔，他忍不住向這個空間的支配者詢問。"+"\n"+"「你的表現比我想像中的好嘛。」迷霧居然沒有搭理他的疑問，有一瞬間，日翔居然覺得這位陌生的個體似乎太有個性了……"+"\n"+"「你猜猜，我是來找你做什麼的？」"+"\n"+"「我怎麼會知……」正打算回應，可迷霧卻不等待日翔說完，便擅自搶答：「沒有啦，我只是來跟你打招呼，有沒有嚇到？」"+"\n"+"喂、這人……是人嗎？會不會太我行我素了？日翔終於忍不住在內心吐槽。"+"\n"+"不過，感覺上應該不是個壞人。"+"\n"+"謎的聲音似乎真的是來打招呼的，他沒有打算和日翔多說，整個世界便已經隨著逐漸模糊的聲音消逝：「總而言之，能像你一樣得到重返大學生活的機會的人『幾乎』是沒有的……這次啊，你得好好把握……」"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=ButtonsTemplate(
                        title='？？',
                        text='……等等，別走！',
                        actions=[
                            MessageAction(
                                label='？？',
                                text='……等等，別走！'
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

    #??
    elif event.message.text=="……等等，別走！":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AE'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[2],int(5))
                list_talk=[]
                list_talk.append(TextSendMessage(text="待到日翔重新拾起話語權時，他卻已經回到了柔軟的床上——伴隨手機鬧鐘叮鈴鈴地鬧騰，他意識到剛才與迷霧的對話僅不過是一場夢。"+"\n"+"日翔關閉擾人的鬧鐘，思考道：那場「夢境」清晰得不得了，和真實在眼前發生過的事情沒兩樣。剛剛所經歷的夢真的是一場夢嗎？……不過，能重返大學生活本身，就已經是件不科學的事情了，日翔更傾向於將這場「夢境」視作真正發生過的事情。"+"\n"+"他拍拍臉頰振作自己，今天是開始上課的日子——重新升上大二的上課日。秉持著「好好把握」的理念，他並不想在第一天就遲到。"))
                list_talk.append(TextSendMessage(text="解鎖伯達樓！趕快去「遊戲地圖」看看！"+"\n\n"+"開學的第一堂課是在伯達樓。伯達樓也是資管系學生常常前往的大樓。除了有資管系的機房之外，系學會也在這裡。另外也有BS440等新型教室，採光優良、設備新穎。除了有大大的白板跟投影螢幕外，甚至還有足夠的充座可以提供給每個學生使用筆電、平板等，無須擔心充電問題。"+"\n"+"過了不知道多久，這堂課終於結束了，日翔拎起背包，正打算去514巷覓食。他習慣性地偷偷看了一眼他打從幾年前就有些在意的曉光，雖然平常都看不太出她的感情起伏，但日翔隱隱約約注意到，她的動作比平常要更輕巧，而且似乎盯著手上的一張兌換券。記得曉光上次填寫教學評量，好像抽中了食科冰淇淋的兌換券……"))
                list_talk.append(TextSendMessage(text="#27 經典輔大美食：食科冰淇淋最接近哪個學餐？（請以「Ｏ園」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #27答案
    elif event.message.text=="輔園":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AE'+str(j))
            list.append('AF'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="是啊，都已經回到大學生活了，一定要想辦法更加了解曉光才行！她會不會其實很喜歡食科冰淇淋？「好好把握」一詞仍然在他腦中迴盪，他想，他得抓住這次機會才行。"+"\n"+"「曉光！你抽到冰淇淋券了？真幸運！」日翔主動上前搭話。"+"\n"+"「謝謝你……我只是順手填了教學評量。」曉光並沒有外表看起來的難接近，倒是很順口地接續了話題。教學評量是學期末會給同學填寫的各課程教學問卷，為了鼓勵同學作答，通常校方會伴隨舉辦抽獎活動。"+"\n"+"日翔和曉光往教室門口走去，正巧遇到大搖大擺晃進教室的司晨，他很自然地插話道：「剛剛是不是有人提到食科冰？我也要去吃！」"+"\n"+"聞言，曉光便以聽不出來她是在誇還是在罵的語氣平靜地回應：「遲到了卻還那麼厚臉皮，真是不可思議。」"+"\n"+"「這是在誇我嗎？謝謝你呀曉光、嘿嘿。」"+"\n"+"「阿司啊，正常人會覺得這是在誇獎嗎？」"+"\n"+"「哎，又沒關係第一周是加退選吧，也不點名啊！大好時光當然要去吃早餐嘛。」"+"\n"+"於是，一行人以兩人聊天一人吐槽的模式邊走邊聊，一邊走下伯達樓的樓梯，這時，司晨看看班群的機測通過名單，苦惱道：「哎、我上兩次機測都只有對一題，這樣真的可以畢業嗎？」"+"\n"+"日翔用詫異的眼神看看司晨：「你不知道嗎？機測其實不一定要一次通過，只要……」"))
                list_talk.append(TextSendMessage(text="#28 以下哪一位同學通過了輔大資管系的畢業規則「通過程式語言機測」？"+"\n"+"（Ａ）未通過任何一次程式語言機測，在學期間總共累計通過3題機測題目，且修畢一門資管系的程式設計選修課程"+"\n"+"（Ｂ）未通過任何一次程式語言機測，累計通過2題機測題目並修畢完一門資管系的程式設計選修課程之後，再參加一次機測並通過1題"+"\n"+"（Ｃ）未通過任何一次程式語言機測，在學期間總共累計通過5題機測題目"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#28',
                    template=ButtonsTemplate(
                        title='#28',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='未通過任何一次程式語言機測，在學期間總共累計通過3題機測題目，且修畢一門資管系的程式設計選修課程'
                            ),
                            MessageAction(
                                label='B',
                                text='未通過任何一次程式語言機測，累計通過2題機測題目並修畢完一門資管系的程式設計選修課程之後，再參加一次機測並通過1題'
                            ),
                            MessageAction(
                                label='C',
                                text='未通過任何一次程式語言機測，在學期間總共累計通過5題機測題目'
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
    
    #28答案
    elif event.message.text=="未通過任何一次程式語言機測，在學期間總共累計通過3題機測題目，且修畢一門資管系的程式設計選修課程":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AF'+str(j))
            list.append('AG'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「原來只要累計三題、再去選修我們系上的程式語言課程就可以算是通過機測了嘛！那就好，我這次再答對一題就可以不用再考了！」司晨露出了像是「賺爛了」的眼神，就好似撥雲見日一般，剛剛懊惱的樣子早已煙消雲散。"+"\n"+"日翔和曉光還來不及吐槽司晨，他又馬上表現出驚喜的樣子，心情轉換堪比川劇變臉：「嗯？風華廣場今天這麼熱鬧，是不是有什麼好玩的！」"+"\n"+"曉光看他像大一新生一樣興奮，依然維持著淡然的樣子默默開口：「那個，是課指組舉辦的……」"))
                list_talk.append(TextSendMessage(text="#29 位於法籃旁邊的輔仁大學課外活動指導組，簡稱課指組，主要目的是期望透過課外活動之輔導功能，促進學生課業以外之活動延伸與學習。請問以下何者是課指組的承辦業務？"+"\n"+"（Ａ）校慶系列活動、社團博覽會、領才營"+"\n"+"（Ｂ）輔仁大學服務學習種籽志工隊"+"\n"+"（Ｃ）租借中美堂場地"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#29',
                    template=ButtonsTemplate(
                        title='#29',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='校慶系列活動、社團博覽會、領才營'
                            ),
                            MessageAction(
                                label='B',
                                text='輔仁大學服務學習種籽志工隊'
                            ),
                            MessageAction(
                                label='C',
                                text='租借中美堂場'
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

    #29答案
    elif event.message.text=="校慶系列活動、社團博覽會、領才營":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AG'+str(j))
            list.append('AH'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「啊——我想起來了，原來又到了社團博覽會的季節，時間過得真快。」司晨撓撓頭，似乎終於回想起來去年剛開學的時候也有社博這回事。"+"\n"+"「你居然忘記了，前一年的社博我們是一起參加的吧？去年明明我們都有意願加入系籃，你現在就給我忘了？」日翔失笑，這些年跟司晨相處他很明白他直率過了頭的腦袋，總是讓人有種他能考上資管系真是奇蹟的感覺。"+"\n"+"對日翔而言，他已經和司晨一起逛熱鬧的風華廣場好多次了。不過他可以確定，這一年的社博一定比過往更加獨特，因為無論參加與否，他所喜歡的曉光這次就在旁邊。日翔不經意地將視線撇向曉光——就這麼巧，她也正好往這邊看了過來。"+"\n"+"「……嗯、怎麼了？」曉光注意到了剛剛的注視。冰藍的眸子裡仍然讀不出表情，這也是身為高嶺之花她最獨特的地方，日翔盯著她的眼睛，思緒竟然發散了起來。"+"\n"+"下一刻，日翔才回過神來急急忙忙回應曉光的疑問：「啊沒、沒什麼！只是有點好奇曉光會不會參加社團而已。」"+"\n"+"跟著下課的人流走著走著，食科冰淇淋的招牌映入三人的眼簾。"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/07/a6V5BY.png', preview_image_url='https://upload.cc/i1/2022/03/07/a6V5BY.png'))
                list_talk.append(TextSendMessage(text="「星期三會有特殊口味，可惜今天是星期一。」曉光打開玻璃門自言自語；雖然一言一語中沒有透露出什麼特殊訊息，但日翔能感覺到曉光的心情似乎很好。"+"\n"+"食科冰的店面乾淨整潔、澄黃色的牆面跟木質的地板櫃檯都十分有溫馨的感覺。聽說食科冰的配方是由以前的學長姊留下的，無論在什麼時候，輔大都可以吃到這種回憶裡的好味道。日翔一直認為，這裡應該是校園內數一數二讓人放鬆的地方。"+"\n"+"曉光兌換完香草口味的冰淇淋後，日翔和司晨也都各購買了一支冰淇淋，三人坐在窗邊的位置上邊吃邊聊天。日翔的心思仍然停在曉光身上，好像都沒有注意到手上綜合冰淇淋的一角已經開始化掉了——不知為何，曉光喜歡香草口味的霜淇淋這事對他而言並不是一件令自己意外的事情？明明以前都沒有和曉光吃過冰淇淋吧。"+"\n"+"「喂——阿日，你的冰都弄到手上啦！！阿日！」"+"\n"+"突然，有熟悉的聲音打斷了進入沉思狀態的日翔，他近乎是顫得跳了起來看了看，原來是早就把冰淇淋吃完了的司晨。"+"\n"+"「你今天怎麼搞的，居然一直在出神，不是讓曉光看笑話了嗎？」司晨趁著還在好友尚在半恍神的狀態中，趁機調侃了一番。"+"\n"+"「嗯？日翔捨不得吃那麼好吃的冰所以開始發呆，應該是很正常的吧。」被點名的曉光咬下酥脆的甜筒輕快地反駁。很明顯的，曉光一吃冰淇淋心情就好了一大截。"+"\n"+"司晨說得沒錯，他竟然就開始自顧自地出神了起來，這無疑是稍微浪費了難得和曉光同行的機會。可曉光說的話也並沒有什麼問題，畢竟食科冰是真的很好吃——唯一錯的地方在於，發呆的原因分明是那個比食科冰更加美好的女孩。"+"\n\n"+"解鎖冰淇淋券！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="某天統計課的下課時間，日翔發現自己犯了很大的錯誤。"+"\n"+"「啊……！！」"+"\n"+"「怎麼啦阿日？」聽到日翔那讓人聯想到世界名畫「吶喊」的慘叫聲，在一旁玩手機遊戲的司晨撇過頭來看他。"+"\n"+"日翔突然開始搖起了司晨的肩膀：「今天統計要小考啊，我沒有帶計算機欸！完蛋了！」"+"\n"+"「……對喔！那要不要現在去敦煌買？」"+"\n"+"「這樣會不會太浪費錢了啊，工程計算機一台不便宜吧……而且我覺得應該也沒有人會多帶一台。」雖然日翔馬上就反駁了自己的好友，但是他仍然掏出了自己的錢包看看有沒有帶足夠的錢買計算機。"+"\n"+"這時，一道格外清澈的女聲打斷了兩人的對話：「……聽說我們系學會可以借計算機。」"+"\n"+"是看見他們吵吵鬧鬧於是忍不住提議的曉光。"+"\n"+"「「欸？真的嗎！？」」宛如重見天日的兩位粗心大意的傻子對曉光投以感激的目光。"))
                list_talk.append(TextSendMessage(text="#30 資管系系學會目前位在哪一個大樓？（請以「ＯＯ樓」回答）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #30答案
    elif event.message.text=="伯達樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AH'+str(j))
            list.append('AI'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="又過了幾個禮拜，終於，考試又要鄰近了——打算抱佛腳的日翔心想，根據他的經驗，在家看書他一點也不會認真，總是讀了一兩行又跑去滑滑手機敲敲鍵盤、整理書櫃打掃房間、甚至出奇地自告奮勇跑去幫媽媽跑腿。畢竟再怎麼擁有上一次大學生活的經歷，有些東西就是考完就會順便忘記的。於是他決定在學校圖書館讀書。而他心想，現在跟曉光也逐漸熟識了起來，如果有機會也可以向他問問題。"))
                list_talk.append(TextSendMessage(text="#31 請問本校擁有最多層樓的圖書館是哪一個？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #31答案
    elif event.message.text=="濟時樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AI'+str(j))
            list.append('AJ'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#32 請問學校圖書館濟時樓平日幾點開？"+"\n"+"（Ａ）08:00 ~ 23:00"+"\n"+"（Ｂ）08:00 ~ 22:00"+"\n"+"（Ｃ）09:00 ~ 23:00"+"\n"+"（Ｄ）08:30 ~ 22:00"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#32',
                    template=ButtonsTemplate(
                        title='#32',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='08:00 ~ 23:00'
                            ),
                            MessageAction(
                                label='B',
                                text='08:00 ~ 22:00'
                            ),
                            MessageAction(
                                label='C',
                                text='09:00 ~ 23:00'
                            ),
                            MessageAction(
                                label='D',
                                text='08:30 ~ 22:00'
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

    #32答案
    elif event.message.text=="08:00 ~ 22:00":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AJ'+str(j))
            list.append('AK'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(6))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖濟時樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="日翔這幾天讀得急急忙忙，但靠著過去大學生活的記憶，總算把所有的課程內容讀完了，甚至還比以前要讀得更好——甚至還可以跟曉光討論一些比較艱難的題目，或者是拯救必修快要掛掉的司晨。他們三人後來還借濟時樓的討論室，在課後一起惡補。而且，其中的幾天還遇上同樣跑來濟時樓讀書的宇桓！沒想到，那個學霸也在這裡讀書啊，這是以前日翔都不知道的。"+"\n"+"現在，是該要驗收讀書的成果了。"))
                list_talk.append(TextSendMessage(text="#33 班上 1-10 號的同學身高分別為 178、160、155、182、169、160、164、158、175、160，請分別輸入這十位同學的算術平均數、中位數與眾數。（請以「Ｏ、Ｏ、Ｏ」回答，若Ｏ有小數點為四捨五入至第一位半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #33答案
    elif event.message.text=="166.1、164.5、160":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AK'+str(j))
            list.append('AL'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#34 有一資料庫用來記錄學生分數如下圖，下列有一塗黑語法，該填上什麼可以由小到大輸出A班學生姓名與成績？"+"\n"+"◼ name,score ◼ database_score ◼ class_id=1 ◼ score ASC"+"\n"+"（Ａ）SELECT/FROM/WHERE/ORDER BY/ASC"+"\n"+"（Ｂ）SELECT/FROM/WHERE/GROUP BY/DESC"+"\n"+"（Ｃ）SELECT/FROM/WHEN/ORDER BY/DESC"+"\n"+"（Ｄ）SELECT/FROM/WHEN/GROUP BY/ASC"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fxIoAx@.png', preview_image_url='https://ppt.cc/fxIoAx@.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#34',
                    template=ButtonsTemplate(
                        title='#34',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='SELECT/FROM/WHERE/ORDER BY/ASC'
                            ),
                            MessageAction(
                                label='B',
                                text='SELECT/FROM/WHERE/GROUP BY/DESC'
                            ),
                            MessageAction(
                                label='C',
                                text='SELECT/FROM/WHEN/ORDER BY/DESC'
                            ),
                            MessageAction(
                                label='D',
                                text='SELECT/FROM/WHEN/GROUP BY/ASC'
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

    #34答案
    elif event.message.text=="SELECT/FROM/WHERE/ORDER BY/ASC":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AL'+str(j))
            list.append('AM'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#35 又該如何輸出全班總分及平均並重新命名表格欄位？（請以半形英文大寫「ＯＯＯ/ＯＯ/ＯＯＯ/ＯＯ」回答。）"+"\n"+"SELECT ◼(score) ◼ 總分, ◼(score) ◼ 平均 FROM database_score"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fxIoAx@.png', preview_image_url='https://ppt.cc/fxIoAx@.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #35答案
    elif event.message.text=="SUM/AS/AVG/AS":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AM'+str(j))
            list.append('AN'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#36 關聯式資料庫中的key分為很多種，其中主鍵（primary key）和外來鍵（foreign key）兩者的特性為？"+"\n"+"（Ａ）兩者皆可為空"+"\n"+"（Ｂ）兩者皆不可為空"+"\n"+"（Ｃ）主鍵可為空，外來鍵不可"+"\n"+"（Ｄ）外來鍵可為空，主鍵不可"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#36',
                    template=ButtonsTemplate(
                        title='#36',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='兩者皆可為空'
                            ),
                            MessageAction(
                                label='B',
                                text='兩者皆不可為空'
                            ),
                            MessageAction(
                                label='C',
                                text='主鍵可為空，外來鍵不可'
                            ),
                            MessageAction(
                                label='D',
                                text='外來鍵可為空，主鍵不可'
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

    #36答案
    elif event.message.text=="外來鍵可為空，主鍵不可":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AN'+str(j))
            list.append('AO'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#37 下列關於資料庫的選項何者正確？"+"\n"+"（Ａ）主鍵在每個儲存格唯一不可重複"+"\n"+"（Ｂ）外來鍵在每個儲存格唯一不可重複"+"\n"+"（Ｃ）所有儲存格皆不可為Null"+"\n"+"（Ｄ）資料表名稱不可與資料庫名稱重複"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#37',
                    template=ButtonsTemplate(
                        title='#37',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='主鍵在每個儲存格唯一不可重複'
                            ),
                            MessageAction(
                                label='B',
                                text='外來鍵在每個儲存格唯一不可重複'
                            ),
                            MessageAction(
                                label='C',
                                text='所有儲存格皆不可為Null'
                            ),
                            MessageAction(
                                label='D',
                                text='資料表名稱不可與資料庫名稱重複'
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
    
    #37答案
    elif event.message.text=="主鍵在每個儲存格唯一不可重複":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AO'+str(j))
            list.append('AP'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(6))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖信封、卡通主題鉛筆！趕快去「個人檔案」看看！"+"\n\n"+"總算是到了大二的學期中末，班代已經在班群開始提醒各組要尋找好專題組員了。"+"\n"+"於是，在一堂課程的下課休息時間，日翔和司晨兩人站在教室門口一邊喝早餐店奶茶，一邊思考要找哪些組員才好。"+"\n"+"「噯，你不是對曉光有意思嗎，快點去邀請她呀阿日！」司晨一如既往地慫恿日翔豁出去了。"+"\n"+"「等一下你怎麼知道的？算了，因為……我怕會拖曉光的後腿。」在日翔的記憶裡，先前一次大學生活的曉光是和宇桓那種等級的學霸們在一起的，就算日翔這幾次考試都靠著神秘的回歸之力得到不錯的分數，他仍然對自己的程式能力有些缺乏自信。"+"\n"+"「當然是身為你好兄弟的直覺啊！這麼明顯！」"+"\n"+"「……日翔？你們在討論什——」曉光聽到好像有人在叫自己的名字後就從教室裡走出來。看見是熟人之後，便上前問話。"+"\n"+"日翔看見自己的真命天女突然在跟兄弟討論「關鍵問題」的時候出現是差點沒嚇破膽，他甚至都還沒有下定決心啊！不，或許就跟司晨、以及那個神祕的聲音說的一樣。這時候已經不能再猶疑不前。明明已經決定好要在「這一次」的大學時光要全力以赴，不留下遺憾了。"+"\n"+"「曉光！你現在專題已經有組了嗎？」"+"\n"+"「哎、哎、還沒有……」"+"\n"+"「那……要不要和我們一組？」"+"\n"+"上課時間，教授似乎還沒回到教室授課。坐在隔壁的司晨趁機用胳膊碰碰日翔，笑著調侃道：「阿日，看你這麼果斷，你很勇喔！前一秒還說怕拖後腿，下一秒就把曉光邀請進來專題群組了嘛。」"+"\n"+"「哈哈哈……這都要謝謝你鼓勵我。」日翔也沒想到這次豁出去會這麼順利，他心想，或許要歸功於考前那次常常開讀書會，才讓曉光對自己感到更加熟識。"+"\n"+"「喂，聽說你們跟曉光一組啊。」聽起來像是要找麻煩一樣的話語從身後傳來，日翔跟司晨回頭一看，宇桓竟然就直直盯著他倆。"+"\n"+"「呃、沒錯，怎麼了？」日翔承受下了宇桓不知為何顯得咄咄逼人的目光。"+"\n"+"「你們現在還缺人吧，我上次看你們在圖書館讀書挺認真的，我很滿意。」宇桓回應。"+"\n"+"日翔默默想道，沒錯，去圖書館那幾次似乎也有看到他在讀書，原來他也看到我們了嗎？"+"\n"+"「？？？」那個高冷學霸宇桓說賞識我哎這裡是哪裡我是誰，司晨露出了貓咪第一次看到宇宙的震撼表情。"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/08/Baezmv.jpg', preview_image_url='https://upload.cc/i1/2022/03/08/Baezmv.jpg'))
                list_talk.append(TextSendMessage(text="「非要我說得那麼明白？我決定跟你們三個一組，這對你們而言不會是件壞事。」宇桓的嘴角勾起，還沒等日翔和司晨反應過來，竟然就擅自認為自己已經加入專題組別了。"+"\n"+"「哇哦……好、好啊，那你先掃QR扣加群組吧。」呃……雖然感覺宇桓好像很有氣場，但在日翔的印象裡，他的程式在全班是數一數二強的！日翔度過的兩次大一上學期的生活裡，宇桓考機測都只用了一小時就出了考場，而且，成績出爐後居然都是五題全通過。這麼厲害的他一定能成為專題的一大助力。"+"\n"+"過了幾周，眾人在團體討論室專題主題。這時候的專題小組已經湊滿五人，有日翔、曉光、司晨、宇桓、以及曉光她隔壁班的朋友，林真澄。"+"\n"+"由於專題或多或少牽涉到畢業、或者職涯發展的話題，司晨便突然開口：「哎，已經要到申請雙主修的時間了。我在想要不要申請雙主修。」"+"\n"+"「真的假的，阿司，你居然想要雙主修！」日翔嘴巴張得大大的，難道世界線發生了這麼大的變動嗎——司晨居然破天荒地跟以前不同，想要變成雙主修學霸了！？"))
                list_talk.append(TextSendMessage(text="#38 為鼓勵學生多元學習，許多大學都有雙主修、輔修和學分學程的申請，而輔大的申請安排於每學年的下學期 4-6 月，請問以下哪一個是開放申請的時間順序？"+"\n"+"（Ａ）輔系-雙主修-學分學程"+"\n"+"（Ｂ）外雙主修-輔系-學分學程"+"\n"+"（Ｃ）學分學程-雙主修-輔系"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#38',
                    template=ButtonsTemplate(
                        title='#38',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text='輔系-雙主修-學分學程'
                            ),
                            MessageAction(
                                label='B',
                                text='雙主修-輔系-學分學程'
                            ),
                            MessageAction(
                                label='C',
                                text='學分學程-雙主修-輔系'
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
    
    #38答案
    elif event.message.text=="學分學程-雙主修-輔系":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AP'+str(j))
            list.append('AQ'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「我突然想要雙修體育系啊！」司晨看到日翔那麼驚訝也顯得有些意外。"+"\n"+"「一般日間部不能用雙主修的方式申請體育系，而且雙主修這件事應該要好好提早規劃的。」看到日常犯傻的司晨，曉光忍不住吐槽。"+"\n"+"「哎、是這樣啊，那算啦。」"+"\n"+"「……」宇桓選擇沉默，他傻眼地把落到鼻樑下方的眼鏡往上推，似乎想喝一口遺忘汁把這段白癡的對話忘掉——他原先是心想日翔跟曉光這兩人肯定是專題的有力隊友，絕對能襯得上自己才加入他們的，至於司晨……宇桓對他的評價是，原來這世界上真的有那麼蠢的人，大開眼界。"))
                list_talk.append(TextSendMessage(text="專題五人組在六月的某天為了要討論專題的主題，順便讀期末考而決定約在學校附近的餐廳見面——更重要的是家財萬貫的宇桓決定請所有人吃一頓！"+"\n"+"宇桓的預算近乎是個無底洞，無論司晨在群組提出多麼離譜的建議——無論是學餐還是吃到飽，大家的金主同學幾乎都是回應：「你們選，我都行」；不過，基於虧欠心理，大家自然不會想佔盡宇桓的便宜，最後一行人還是決定在一個大家都沒課的下午去吃輔大附近的貓中途餐廳「吃。貓」。"+"\n"+"只不過計劃趕不上變化，五個人都有空的時間也就那麼一個下午，卻偏偏在當天午後來了場突襲式的傾盆大雨。已經到站的日翔、曉光跟司晨在捷運輔大站的入口屋簷下看著LINE群的訊息，得知了宇桓跟真澄因為選修課延後所以會晚到的消息。"+"\n"+"「欸欸欸你們知道嗎，聽說學校淹水了餒！！」司晨把限動展示給日翔跟曉光看，一臉就是對學校淹水的狀況備感興趣的樣子。"+"\n"+"「阿司，你要去參觀就自己去，『這次』我不想陪你啦。」日翔想到過去的自己選擇陪著司晨去看那個傳說中的湖，最後那個傻子居然拉著自己在學校裡泛舟……那次經驗實在是瘋狂到在日翔畢業後偶爾還會夢到，很是驚悚。不過雖然日翔這麼說，但這「我不陪你」的話也僅僅是開個玩笑而已，畢竟等等就要去吃貓餐廳，再傻也不會有人真的跑進學校吧……"))
                list_talk.append(TextSendMessage(text="#39 輔大水樂園開張！傳說每當暴雨強襲，校園內就會出現一面湖，曾有學長帶著橡皮艇「到此一划」，請問應該到哪裡朝聖奇景？（請以「ＯＯＯ」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #39答案
    elif event.message.text=="中美堂":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AQ'+str(j))
            list.append('AR'+str(j))
            list.append('B'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(7))
                worksheet.update(list[4],int(7))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖中美堂！趕快去「遊戲地圖」看看！"+"\n\n"+"中美堂是一座大型的圓形建築，類似羅馬競技場。通常是重大集會跟室內體育競賽的選擇地，新生們的開學典禮一般會選擇在這裡舉辦所謂的「叩門禮」。只不過如果遇上了大雨……就會變成傳說中輔大水樂園的鎮園之寶「中美湖」……"+"\n"+"「好啊那我看看就回來！晚點再去找你們吃下午茶！」"+"\n"+"「喂、阿司，我只是開玩笑的！阿司！！」日翔開口大喊，司晨的身影卻早已消失在重重雨簾之中。"+"\n"+"「哇……司晨連傘也不帶就往學校去了。」曉光竟然也忍不住感嘆。"+"\n"+"雖然對他的莽撞感到無言，但日翔對司晨的決定確實是有些感謝之情，因為這樣一來他便得到了第一次名正言順和曉光獨處的機會——即使很可能只有一下下。雖然不知道司晨是不是在幫自己製造機會，但日翔決定以這樣的角度默默感謝他。"+"\n"+"日翔的心情和此時的暴雨呈反比的高興了起來：「曉光，我們先去『吃。貓』等他們吧。」"+"\n"+"「吃。貓」是在北部貓餐廳之中較為著名的一間，據說裡面的人類店長跟貓咪店長都很好，同時也是貓咪的中途之家，許多喜歡貓咪的輔大人都會前去一探究竟。"+"\n"+"日翔和曉光已經提早和人類店長支會總共有五個人要前來用餐，於是他們倆便坐到事先安排好的五人空位桌，由於宇桓和真澄剛剛傳訊息過來表示他們已經下課了，待會就到，於是日翔跟曉光打算等隊友們都差不多到齊了再點餐，至於司晨……他能平安就好。"+"\n"+"畢竟傾盆大雨實在是如倒瀉般止不住，於是到達吃貓的兩人其實也是有些狼狽的——就算是一人撐一把傘，也難以避免身上稍微被淋濕的命運。而因為雨水的緣故，日翔揹筆電跟課本用的背包和手腿無依倖免。嗯……都這樣了還吹著冷氣實在有點討厭啊，曉光她還好嗎？他留意了一下身旁曉光的狀況，她似乎也因為自己的東西淋濕了而懊惱著。"+"\n"+"日翔突然想到，他應該有放一條毛巾在書包裡——起初只是因為對這個「暴雨的今天」有所預防，說白了就是為了要避免司晨真的拉自己去泛舟才帶著的……現在居然可以派上用場，老實說日翔也十分意外。"+"\n"+"他把潔白的毛巾拿出來瞧了瞧。嗯，幸好雨水並沒有波及到它。"+"\n"+"「曉光，這個給妳，如果感冒了就糟糕了。」日翔把自己帶著的乾淨毛巾遞給曉光。"+"\n"+"「欸？啊……謝謝你，我還懊惱要怎麼辦呢。」曉光在接過毛巾之後還細心地確認了一下毛巾的狀況，便用來擦拭濕得很是不舒服的腿腳。"+"\n"+"「不客氣。」他笑著回應完曉光。隨後，日翔的餘光瞄到了她肩膀上的……灰色動物毛？考慮到曉光手機殼印著一隻灰色胖貓，他便好奇地詢問：「曉光，你家裡有養貓嗎？」"+"\n"+"「對，是一隻叫做『德魯貝』的米克斯，小學的時候領養的。」曉光似乎有些驚訝日翔猜中了家裡有養貓，難得地將平淡以外的神情表露在外：「沒想到日翔你可以辨認得出來這是貓毛。」"+"\n"+"「沒有啦，只是我瞎猜的。因為這讓我想到我在小時候也有養過一陣子的貓咪，只要家裡有養動物，毛總是會滿天飛……而且我們也還沒跟這裡的貓咪互動吧。」日翔對於自己的直覺也感到有些驚喜，而他現在才想到，好像也有可能是養灰色的其他動物。"+"\n"+"「這樣呀……我的貓咪以前也是流落街頭，當時是在一間中途之家收養牠的。」一提到自家的貓咪，一邊擦拭書包的她心情就好了起來。"+"\n"+"「啊、如果你會冷的話這個也可以給你，我是不怕冷的那種……雖然只是短袖襯衫，希望可以讓妳好一點。」日翔見到她的臉色似乎還是有些不好，便決定脫下了自己的外套給曉光。"+"\n"+"曉光似乎顯得有些驚喜，也接下了日翔的外套：「不用這麼費心啦……但還是謝謝你。」"))
                list_talk.append(TextSendMessage(text="「哎唷——聊得很開心嘛。」一個聲音打破了兩人的對話。曉光抬頭一看，是自己的好友真澄，她一邊調侃一邊順勢坐到了曉光的對面。"+"\n"+"「你們可以先吃啊，難道是怕我不來付帳嗎？」跟在後頭的宇桓語氣仍然尖銳，但在場的所有人都並不是很在意，畢竟他是金主爸爸，他說得都對。"+"\n"+"眾人你一言我一語地開始聊了起來，並且開始點起了餐。日翔點了一份「隨便」跟一杯「隨便」順便幫目前不在場的司晨點了一份「吃不完的脆薯」、曉光點了一盤雞米花跟一杯葡萄汁、真澄點了「綜合梅優格」、金主宇桓意思意思地點了杯馬來西亞白咖啡，在滿滿都是貓的氛圍裡過了好是愜意的下午。"+"\n"+"至於當初說好討論的期末考跟專題……在貓餐廳怎麼可能討論得起來啊。"+"\n\n"+"解鎖糖果紙！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="期末考在即，大二的時光也即將過去了。不知不覺第二次的大學生活也過了快要一半——日翔想起了那個希望自己好好努力的聲音，他確實感受到，這一次的大學生活因為他的積極而有諸多改變。不知道那位讓自己回到過去的「高位生命體」，是否也在某個地方注視著他呢……"))
                list_talk.append(TextSendMessage(text='#40 在html語法中，要如何輸出此空格效果？（請以半形小寫「<input type="Ｏ">」回答，Ｏ數不代表答案正確字數。）'))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fX1Pix@.png', preview_image_url='https://ppt.cc/fX1Pix@.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #40答案
    elif event.message.text=="password":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AR'+str(j))
            list.append('AS'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#41 在html語法中，以何種語法設定超連結？"+"\n"+"（Ａ）<a href='網址'>超連結</a>"+"\n"+"（Ｂ）<b href='網址'>超連結</b>"+"\n"+"（Ｃ）<c href='網址'>超連結</c>"+"\n"+"（Ｄ）<d href='網址'>超連結</d>"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#41',
                    template=ButtonsTemplate(
                        title='#41',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="<a href='網址'>超連結</a>"
                            ),
                            MessageAction(
                                label='B',
                                text="<b href='網址'>超連結</b>"
                            ),
                            MessageAction(
                                label='C',
                                text="<c href='網址'>超連結</c>"
                            ),
                            MessageAction(
                                label='D',
                                text="<d href='網址'>超連結</d>"
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

    #41答案
    elif event.message.text=="<a href='網址'>超連結</a>":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AS'+str(j))
            list.append('AT'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#42 在html語法中，需要哪些語法以完成下圖效果？"+"\n"+"（Ａ）ol/il"+"\n"+"（Ｂ）ui/il"+"\n"+"（Ｃ）li/ui"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fRPf1x@.png', preview_image_url='https://ppt.cc/fRPf1x@.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#42',
                    template=ButtonsTemplate(
                        title='#42',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="ol/il"
                            ),
                            MessageAction(
                                label='B',
                                text="ui/il"
                            ),
                            MessageAction(
                                label='C',
                                text="li/ui"
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

    #42答案
    elif event.message.text=="ol/il":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AT'+str(j))
            list.append('AU'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#43 下列關於HTML與CSS的敘述何者錯誤？"+"\n"+"（Ａ）HTML適合用來定義網的內容,CSS適合用來定義網頁的外觀"+"\n"+"（Ｂ）CSS樣式表示由一條一條的樣式規則所組成"+"\n"+"（Ｃ）HTML不會區分英文字母的大小寫"+"\n"+"（Ｄ）CSS不會區分英文字母的大小寫"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#43',
                    template=ButtonsTemplate(
                        title='#43',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="HTML適合用來定義網的內容,CSS適合用來定義網頁的外觀"
                            ),
                            MessageAction(
                                label='B',
                                text="CSS樣式表示由一條一條的樣式規則所組成"
                            ),
                            MessageAction(
                                label='C',
                                text="HTML不會區分英文字母的大小寫"
                            ),
                            MessageAction(
                                label="D",
                                text="CSS不會區分英文字母的大小寫"
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

    #43答案
    elif event.message.text=="CSS不會區分英文字母的大小寫":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AU'+str(j))
            list.append('AV'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#44 佇列（Queue）的特性是？"+"\n"+"（Ａ）後進先出（LIFO）"+"\n"+"（Ｂ）先進先出（FIFO）"+"\n"+"（Ｃ）以上皆可"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#44',
                    template=ButtonsTemplate(
                        title='#44',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="後進先出（LIFO）"
                            ),
                            MessageAction(
                                label='B',
                                text="先進先出（FIFO）"
                            ),
                            MessageAction(
                                label='C',
                                text="以上皆可"
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
    
    #44答案
    elif event.message.text=="先進先出（FIFO）":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AV'+str(j))
            list.append('AW'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                worksheet.update(list[2],int(1))
                worksheet.update(list[3],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖紀念幣！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="解鎖大三劇情"))
                list_talk.append(TextSendMessage(text="人類的記憶總是在不斷累積，也會在不知不覺間遺忘對大腦而言不重要的事物。"+"\n"+"開學的前一天夜裡，日翔躺在床上努力回憶著過去的種種。他發現：幼時的記憶他似乎也記不得多少了。至於為何要開始回憶過去，是因為他愈發感覺自己似乎遺忘了某個重要的事情。每次和曉光相處的時候，他總能在腦海之中勾勒出幼時見到過的物件，而日翔幼時的玩伴和曉光的身影好像可以重疊在一起——無論是喜歡看書、點了葡萄汁、還是著迷於霜淇淋等等。"+"\n"+"日翔能夠記得的幼時記憶不多，但他還是能隱隱約約感受到，她倆似乎相似過了頭。可是最關鍵的那位小女孩的名字，他卻忘得一乾二淨。"))
                carousel_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                title='？？',
                                text='偏偏忘了這麼重要的事……',
                                actions=[
                                    MessageAction(
                                        label='？？',
                                        text='偏偏忘了這麼重要的事……'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                title='？？',
                                text='頭好痛……',
                                actions=[
                                    MessageAction(
                                        label='？？',
                                        text='頭好痛……'
                                    )
                                ]
                            )
                        ]
                    )
                )
                list_talk.append(carousel_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #??
    elif event.message.text=="偏偏忘了這麼重要的事……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AW'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage(text="即使日翔已經回憶到開始頭疼了，還是想不起來，甚至他也無法確定究竟這些記憶是真的，還是因為太喜歡曉光而搞錯了記憶……總不能直接問曉光吧？那也太奇怪了！"+"\n"+"日翔曾經在幼稚園時為了配合父親的公司上下班而全家搬到了新北市，到了新家並轉學到別的幼稚園以後，他就再也沒有回到有那位「兒時玩伴」的城市了，也因此，他對那邊的事情實在印象不深。"+"\n"+"比起研究這個，似乎還是睡覺實在……日翔心想。"+"\n"+"明天又是新的學期了，還是珍惜眼前的大學生活跟曉光本人吧。"))
                list_talk.append(TextSendMessage(text="大三開學第一週第一堂課。"+"\n"+"老屁股們不像小大一那樣乖乖的全員到齊，基本上都是來的人無精打采、不來的人就理直氣壯地窩在家裡睡大頭覺。刻意坐在中後排座位的日翔跟司晨自然也不是太認真，甚至已經開始在打午餐的算盤了。"+"\n"+"「嘿嘿，等下去吃仁園嗎？還是去輔園？我請客啊。」遙遙隔了一個暑假，到了今天才見到兩個多月未見的摯友，司晨顯得精神特別振奮。"+"\n"+"「阿司，說到請客啊，這次你可別想賴帳喔。」日翔震驚，雖然以司晨熱心腸子又講義氣的個性本身來說他並不太意外司晨會打算請客，但他想到大一的時候吃鬆餅最後還是自己請客……這次得讓這傢伙好好請客才行。"+"\n"+"「當然啦兄弟！我跟你說，我在暑假的時候跑去打工欸，前幾天拿到薪水了，當然要跟好朋友分享啊！隨便你叫外送也行！」司晨自信地拍拍胸脯。日翔敏銳地發現，他今天穿來的大學T似乎也是新買的。"+"\n"+"如果上次大學生活的印象沒有錯的話，司晨的確是從大二升大三的暑假開始打工的，因為大三的課開始變少了嘛。日翔看著他嶄新潔白的衣服感嘆。"+"\n"+"「好啊，是你說的，那我就盡情點囉？」日翔點開司晨手機裡的外送app，隨便點了一個很貴的餐廳。"+"\n"+"「噯噯手下留情手下留情，我沒阿桓那麼有錢啦！」面對在購物車裡狂加餐點的日翔，司晨慌張得把手機搶了回去。"))
                list_talk.append(TextSendMessage(text="#45 請問如果要在學校訂外送，之能夠在哪個地方取餐？"+"\n"+"（Ａ）正門"+"\n"+"（Ｂ）後門"+"\n"+"（Ｃ）側門和正門"+"\n"+"（Ｄ）正門和後門"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#45',
                    template=ButtonsTemplate(
                        title='#45',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="正門"
                            ),
                            MessageAction(
                                label='B',
                                text="後門"
                            ),
                            MessageAction(
                                label='C',
                                text="側門和正門"
                            ),
                            MessageAction(
                                label='D',
                                text="正門和後門"
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
    
    #??
    elif event.message.text=="頭好痛……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('AW'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage(text="即使日翔已經回憶到開始頭疼了，還是想不起來，甚至他也無法確定究竟這些記憶是真的，還是因為太喜歡曉光而搞錯了記憶……總不能直接問曉光吧？那也太奇怪了！"+"\n"+"日翔曾經在幼稚園時為了配合父親的公司上下班而全家搬到了新北市，到了新家並轉學到別的幼稚園以後，他就再也沒有回到有那位「兒時玩伴」的城市了，也因此，他對那邊的事情實在印象不深。"+"\n"+"比起研究這個，似乎還是睡覺實在……日翔心想。"+"\n"+"明天又是新的學期了，還是珍惜眼前的大學生活跟曉光本人吧。"))
                list_talk.append(TextSendMessage(text="大三開學第一週第一堂課。"+"\n"+"老屁股們不像小大一那樣乖乖的全員到齊，基本上都是來的人無精打采、不來的人就理直氣壯地窩在家裡睡大頭覺。刻意坐在中後排座位的日翔跟司晨自然也不是太認真，甚至已經開始在打午餐的算盤了。"+"\n"+"「嘿嘿，等下去吃仁園嗎？還是去輔園？我請客啊。」遙遙隔了一個暑假，到了今天才見到兩個多月未見的摯友，司晨顯得精神特別振奮。"+"\n"+"「阿司，說到請客啊，這次你可別想賴帳喔。」日翔震驚，雖然以司晨熱心腸子又講義氣的個性本身來說他並不太意外司晨會打算請客，但他想到大一的時候吃鬆餅最後還是自己請客……這次得讓這傢伙好好請客才行。"+"\n"+"「當然啦兄弟！我跟你說，我在暑假的時候跑去打工欸，前幾天拿到薪水了，當然要跟好朋友分享啊！隨便你叫外送也行！」司晨自信地拍拍胸脯。日翔敏銳地發現，他今天穿來的大學T似乎也是新買的。"+"\n"+"如果上次大學生活的印象沒有錯的話，司晨的確是從大二升大三的暑假開始打工的，因為大三的課開始變少了嘛。日翔看著他嶄新潔白的衣服感嘆。"+"\n"+"「好啊，是你說的，那我就盡情點囉？」日翔點開司晨手機裡的外送app，隨便點了一個很貴的餐廳。"+"\n"+"「噯噯手下留情手下留情，我沒阿桓那麼有錢啦！」面對在購物車裡狂加餐點的日翔，司晨慌張得把手機搶了回去。"))
                list_talk.append(TextSendMessage(text="#45 請問如果要在學校訂外送，之能夠在哪個地方取餐？"+"\n"+"（Ａ）正門"+"\n"+"（Ｂ）後門"+"\n"+"（Ｃ）側門和正門"+"\n"+"（Ｄ）正門和後門"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#45',
                    template=ButtonsTemplate(
                        title='#45',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="正門"
                            ),
                            MessageAction(
                                label='B',
                                text="後門"
                            ),
                            MessageAction(
                                label='C',
                                text="側門和正門"
                            ),
                            MessageAction(
                                label='D',
                                text="正門和後門"
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
            #日向視角&物件0
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="0":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【0/10】"))
                list_talk.append(TextSendMessage(text="還沒解鎖物件喔！趕快去過關解鎖吧！"))
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件1
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【1/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件2
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="2":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【2/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件3
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="3":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【3/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件4
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="4":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【4/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/nKLmcQG.png',
                                action=MessageTemplateAction(
                                    label='冰淇淋券介紹',
                                    text='冰淇淋券介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件5
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="5":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【5/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/nKLmcQG.png',
                                action=MessageTemplateAction(
                                    label='冰淇淋券介紹',
                                    text='冰淇淋券介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/Ep84aDF.png',
                                action=MessageTemplateAction(
                                    label='信封介紹',
                                    text='信封介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件6
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="6":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【6/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/nKLmcQG.png',
                                action=MessageTemplateAction(
                                    label='冰淇淋券介紹',
                                    text='冰淇淋券介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/Ep84aDF.png',
                                action=MessageTemplateAction(
                                    label='信封介紹',
                                    text='信封介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/4MW6lNS.png',
                                action=MessageTemplateAction(
                                    label='卡通主題鉛筆介紹',
                                    text='卡通主題鉛筆介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件7
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="7":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【7/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/nKLmcQG.png',
                                action=MessageTemplateAction(
                                    label='冰淇淋券介紹',
                                    text='冰淇淋券介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/Ep84aDF.png',
                                action=MessageTemplateAction(
                                    label='信封介紹',
                                    text='信封介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/4MW6lNS.png',
                                action=MessageTemplateAction(
                                    label='卡通主題鉛筆介紹',
                                    text='卡通主題鉛筆介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/9TzxQhQ.png',
                                action=MessageTemplateAction(
                                    label='糖果紙介紹',
                                    text='糖果紙介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件8
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="8":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【8/10】"))
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='已解鎖物件',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/2r7tDCN.png',
                                action=MessageTemplateAction(
                                    label='童話書介紹',
                                    text='童話書介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/SAwcrWC.png',
                                action=MessageTemplateAction(
                                    label='遊Ｏ王卡介紹',
                                    text='遊Ｏ王卡介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/hXpbU2C.png',
                                action=MessageTemplateAction(
                                    label='圖畫介紹',
                                    text='圖畫介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/nKLmcQG.png',
                                action=MessageTemplateAction(
                                    label='冰淇淋券介紹',
                                    text='冰淇淋券介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/Ep84aDF.png',
                                action=MessageTemplateAction(
                                    label='信封介紹',
                                    text='信封介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/4MW6lNS.png',
                                action=MessageTemplateAction(
                                    label='卡通主題鉛筆介紹',
                                    text='卡通主題鉛筆介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/9TzxQhQ.png',
                                action=MessageTemplateAction(
                                    label='糖果紙介紹',
                                    text='糖果紙介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/3ruuwRd.png',
                                action=MessageTemplateAction(
                                    label='紀念幣介紹',
                                    text='紀念幣介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #小光視角
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【"+worksheet.acell(list[1]).value+"/8】"))   
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒開始遊戲喔，請輸入「開始遊戲」建立個人檔案。"))
    
    elif event.message.text=="童話書介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="適合學齡前小朋友的讀物，封底被人用油性筆寫上名字，但部分筆墨已脫落而看不出原本的字。被人反反覆覆翻閱過很多遍，看得出其主人對這本童書內容的喜愛。"))
    elif event.message.text=="遊Ｏ王卡介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="一張看起來很有年代感的卡牌，上頭印著魄力十足的怪獸，被好好地保存了起來。"))
    elif event.message.text=="圖畫介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="在？？的房間牆上經過裱框的一張圖畫，以畫風看來明顯出自於孩童之手。稚氣的圖上畫著兩個孩子手牽著手的樣子。"))
    elif event.message.text=="冰淇淋券介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不知道是誰用鉛筆親手畫下的冰淇淋券，沒有實際效用。"+"\n"+"稚氣的中文和注音符號寫著「兔ㄈㄟˋ冰氵其氵木木ㄑㄩㄢˋ」（免費冰淇淋券），在旁邊還用心地畫了兩個小孩跟兩支冰淇淋。從鉛筆痕跡的潮濕狀況來看，應該是有些年歲了。"))
    elif event.message.text=="信封介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="稚嫩的字在信封上寫著「日翔ㄐ攵」。看起來跟那張「冰淇淋券」出自同一人之手。信封裡面沒有任何東西。"))
    elif event.message.text=="卡通主題鉛筆介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經使用過的鉛筆，上面的圖案是一位童年卡通人物，看得出來鉛筆的主人很愛護它。"))
    elif event.message.text=="糖果紙介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="看起來皺巴巴的糖果紙，上面用用黃底紅字印著「Chupa Chups」的字樣，是葡萄口味。從塑膠紙皺褶的壓痕來看，應該是包裝棒棒糖用的。"))
    elif event.message.text=="紀念幣介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="老舊的科博館紀念幣，只要在館內花費50元製作就可以獲得一枚。對重要的人們總是觀察入微的他，似乎想起了某人的鉛筆盒裡也有一枚……"))

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