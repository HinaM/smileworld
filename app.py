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
            #初始值設定到E
            for i in range(1,len(list)):
                worksheet.update(list[i],int(0))
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
                list.append(TextSendMessage(text='#1 檔案只有短短幾行程式碼，請問該輸入什麼才能執行此函式，讓結果非None呢？（請輸入半形英文字母）'))
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
                list=[]
                list.append(ImageSendMessage(original_content_url='https://i.imgur.com/2cCaBmx.jpeg', preview_image_url='https://i.imgur.com/2cCaBmx.jpeg'))
                list.append(TextSendMessage(text="今天是曉光大學的同學會，然而曉光只是待在家裡，懷裡還抱著一隻她從小飼養到大的貓咪。「唉，早知道那時候就多交一些朋友了。」生性害羞的曉光，不太擅長社交，所以在大學四年根本沒認識什麼人就畢業了，曉光常常為此感到後悔，但是曉光只能繼續按著手上的遙控器，尋找有趣的節目。"+"\n"+"此時，曉光的手指停了下來，目光停留在一則新聞報導上。"+"\n"+"「根據星象專家的判斷，今日有高機率能在天空中看到流星，請民眾多留意。」"+"\n"+"「德魯貝，你聽，有流星耶，說不定等一下我們就能看到流星喔。」曉光對著懷中的貓咪興奮地說道。"+"\n"+"突然，有一道流星劃破天際，出現在曉光的窗外，「有流星！」曉光抱著懷中的德魯貝，快步地走向窗邊。眼看流星越來越大、越來越大，正當曉光感到吃驚時，流星發出刺眼的光芒。曉光的耳邊響起不知名的聲音：「你想重來一次大學生活嗎？」"+"\n"+"什麼意思？雖然曉光半信半疑，可是可以回到過去，也就是回到18歲的我，可以再重溫一次大學生活，交到很多朋友，感覺不賴，曉光決定試試看，答應了這道聲音。"+"\n"+"那道聲音說：「有這麼簡單就能回到過去嗎？先回答我這個問題——『Code/140.136』，答對了馬上就讓你回去。」"+"\n"+"一下說回到過去，一下子說要解題目，我是不是不該答應啊？可是對我也沒什麼損失。"+"\n"+"「什麼題目？」曉光問道。"))
                list.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/06/q4DPkj.png', preview_image_url='https://upload.cc/i1/2022/03/06/q4DPkj.png'))
                list.append(TextSendMessage(text='#1 題目只有短短幾行程式碼，請問該輸入什麼才能執行此函式，讓結果非None呢？（請輸入半形英文字母）'))
                line_bot_api.reply_message(event.reply_token,list)
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
            #ID已寫入、日向視角、Q1=0
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="0":
                worksheet.update(list[1],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="執行程式後，日翔的螢幕發出了一道刺眼的閃光，幾乎讓日翔睜不開眼睛。日翔隱約聽見一個聲音在耳邊說著：「嘻嘻，這樣人情就還清了，剩下的就看你在學校的表現了。」聲音一落下，刺眼的光就消失了，日翔才緩緩地睜開眼睛。"+"\n"+"「剛剛那是什麼！？」日翔不記得自己欠過誰人情呀？過了一會，日翔才發現自己站在老家的房間裡，連房裡的擺設都跟以前一模一樣，難道自己真的回到過去了嗎？"+"\n"+"「日翔！你怎麼還在房間裡！大學不是今天開學嗎，難道你想第一天上學就遲到嗎？」呃！連媽媽的聲音都跟以前一樣，話說回來剛剛的聲音好像提到了學校？總之先去學校看看吧，搞不好能找到有關那個聲音的線索？"))
                list_talk.append(TextSendMessage(text="#2 要出發去學校了，輔大的地址是？（請以「ＯＯ市ＯＯ區ＯＯ路ＯＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="0":
                worksheet.update(list[1],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="回答完問題後，曉光的身體發出了一道刺眼的閃光，曉光錯愕地睜大雙眼，只能在刺眼的光芒中看到一抹模糊的微笑，還聽見一個聲音在耳邊說著：「嘻嘻，這樣人情就還清了，剩下的就看你在學校的表現了。」聲音一落下，那道光就消失了，曉光才緩緩地睜開眼睛。"+"\n"+"「我是誰？我還活著嗎？這裡是哪裡？剛剛那是！？」過了一會，曉光才發現自己站在老家的房間裡，連房裡的擺設都跟以前一模一樣，難道自己真的回到過去了嗎？"+"\n"+"「曉光！你怎麼還在房間裡！大學不是今天開學嗎，難道你想第一天上學就遲到嗎？」 母親大聲喊著催促曉光。"+"\n"+"「什麼？學校？我真的回來了嗎？」曉光慌張的看著自己的身體，摸著自己的臉。"+"\n"+"「也就是說…我現在是大學一年級新生了？ 糟糕，那就不能在這裡磨磨蹭蹭了，要趕快出門了。是說那道聲音有提到人情？我怎麼一點印象都沒有。不管了，先去學校再說。」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔將上課需要的東西塞進書包匆匆出門了，從日翔老家前往輔大最方便的交通工具就是捷運了，不僅不像公車可能會遇上塞車，在開通環狀線後學生搭捷運所需通勤時間大幅縮短，甚至設有以輔大命名的捷運站直達校門口。"))
                list_talk.append(TextSendMessage(text="#3 請問離校園最近的捷運出口爲？（請以「Ｏ號」回答。Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="1":
                worksheet.update(list[1],int(2))
                list_talk=[]
                list_talk.append(TextSendMessage(text="曉光匆匆忙忙地出門，根本無暇整理自己的包包。曉光只好把學生證，連同手機拿在手上。"+"\n"+"「唔…還是一樣多人呢。」很久沒搭車的曉光，早就忘了從龍山寺搭到新埔這段路程有多麼辛苦，尤其是身材嬌小的曉光總是找不到能呼吸新鮮空氣的地方，這點讓曉光總是到學校前，臉上就略顯疲態。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="2":
                worksheet.update(list[1],int(3))
                list_talk=[]
                list_talk.append(TextSendMessage(text="還好學生證裡還有足夠錢可以讓日翔坐車，日翔倚靠在車門邊沿途欣賞環狀線行經的景色。此刻的他正感到無比放鬆，同樣是在交通巔峰通勤，但日翔現在不必時刻煩惱公司那惱人的報表、業績考核，如果現在發生的一切都是夢的話，拜託讓他多享受一下再醒吧。"+"\n"+"捷運放慢速度進了站，因為是轉乘站的關係，在這站上下車的人數比較多，在一陣推擠後車門終於關上了。捷運再次啟動，這時車廂內傳來的小小聲的驚呼讓日翔的目光從窗外回到車廂，日翔注意到腳邊不知何時出現了一張卡，上頭熟悉的圖案讓日翔一眼認出是輔大的學生證。"+"\n"+"日翔將學生證撿了起來，順便看了一眼學生證上頭的學生資訊，想看看到底是哪個冒失鬼遺落了學生證。經歷過一次大學生活的日翔知道學生證對輔大學生的重要性，學生證不僅可以作為悠遊卡使用，有些教授在期中期末考也會要求學生出示學生證以辨認學生身分。"+"\n"+"學生證上是一張青澀的女孩子的照片，總覺得看起來很熟悉......？往下瞧竟然也是資訊管理系，開學第一天就遇到同系的人嗎？還真巧啊，日翔莞爾。不過看見對方的姓名欄時日翔愣住了，白底黑字清清楚楚地寫著「何曉光」三個字。"+"\n"+"何曉光——在過去和日翔同班，不僅是個大學霸，還是系上的系花，更重要的是！曉光還是日翔單戀了整整四年的女神，不過日翔在過去因為成績太差而不敢高攀曉光。曉光總是安安靜靜地坐在位置上看書，給人一種「可遠觀不可褻玩焉」的感覺，曉光無論是舉手投足間的優雅，還是不冷不熱的語調都讓日翔很是喜歡。"+"\n"+"曉光的學生證掉落在這裡表示曉光也在這班車上嗎！？日翔朝車廂內望去，果不其然發現了正四處張望尋找遺落的學生證的曉光，日翔其實很猶豫到底要不要跟曉光搭話，但少了學生證曉光也出不了站。既然神都給他和曉光說上話的機會了，他又何嘗不把握呢？"))
                list_talk.append(TextSendMessage(text="「妳在找這個吧？」日翔做足了心理準備朝曉光遞出學生證。"+"\n"+"「對......謝謝你。」曉光驚訝地道謝接過。"+"\n"+"「不會。」沒想到能有被曉光道謝一天，日翔在心裡默默感謝那個神秘聲音，「我剛剛看了妳的學生證發現我們同一班呢。我叫游日翔，請多指教啦。」和曉光說上話讓日翔心裡感覺輕飄飄的。"))
                list_talk.append(TextSendMessage(text="#4 曉光的學號是「408402132」，請問曉光是民國幾年入學、甲班還是乙班、座號幾號呢？（請以「ＯＯ年、Ｏ班、ＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="2":
                worksheet.update(list[1],int(3))
                list_talk=[]
                list_talk.append(TextSendMessage(text="因為輔大在橘線上，曉光得要搭乘藍線轉乘黃線、再從黃線轉乘橘線，這繁瑣的轉乘順序，住在台北的曉光早就習慣了。而當捷運快要接近新埔站時，捷運放慢速度，因為是轉乘站的關係，捷運站突然變成車水馬龍的場景，前前後後陸陸續續有人上車和下車，都市人換車的速度，彷彿光陰被快轉了好幾倍。"+"\n"+"「好想趕快到學校。」來來往往被通勤的人擠來擠去的曉光，心中只有這個想法，但是曉光沒想到的是，當捷運突然啟動時，她一不留神的沒握緊好手上的學生證，而學生證劃出華麗的拋物線掉在地上。"+"\n"+"「啊！糟糕！」曉光驚呼一聲，只見學生證掉在一個男子身邊。曉光趕緊平衡好自己的身體，想要向前撿起學生證。但早在這之前，那名男子已經拿起她的學生證。"+"\n"+"「得快點拿回來才行。」曉光略顯緊張，如果學生證被撿走的話，不但要重新申辦新的學生證，還有可能被別人隨便使用，後果不堪設想，得快點跟那名男子要回學生證。"+"\n"+"「不好意思。那個…」怕打擾到其他人，曉光發出細小孱弱的聲音，試圖與那名男子搭話。"+"\n"+"而當那名男子轉過身來，曉光馬上認出來他是誰。"))
                list_talk.append(TextSendMessage(text="「妳在找這個吧？」那名男子遞出學生證。"+"\n"+"「對......謝謝你。」因為太驚訝而來不及和那名男子打招呼的曉光，一眼就認出來他是和曉光同班的游日翔。"+"\n"+"原來我們一直都是搭同一條捷運上學嗎？這個問題瞬間閃過曉光的腦海。大概是曉光通勤的時候都在看書沒注意到吧，曉光用這個理由說服自己。"+"\n"+"「不會。」日翔回答。"+"\n"+"「我剛剛看了妳的學生證發現我們同一班呢。我叫游日翔，請多指教啦。」日翔爽朗的伸出手，想跟曉光握手。"+"\n"+"既然他都幫我拿回學生證了，那握個手應該沒關係吧。曉光也伸出手回握。"+"\n"+"曉光仔細端倪了日翔的手，原來男生的手都這麼大嗎，跟自己的手比起來可說是天壤之別。"+"\n"+"「怎麼了嗎？」日翔對著遲疑的曉光問道。"+"\n"+"「呃不，沒什麼，也請你多多指教，日翔同學。」 曉光總是一不留神就陷入自己的小劇場。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="3":
                worksheet.update(list[1],int(4))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="3":
                worksheet.update(list[1],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="做完簡單自我介紹後，兩人幾乎是沒有什麼更進一步的對話了。一來是曉光本來就不太擅長主動找人說話，二來因為不知道兩人的共同交集是什麼，曉光也找不到話題可以先開口。明白到這兩點的曉光，認為暫時不需要有更多的互動，拿出書來準備開始閱讀。"+"\n"+"好不容易終於到了輔大站，日翔和曉光兩人像是約好一樣從出車廂維持著日翔在前曉光在後跟著，反正兩人目的本來就是一樣的。回到了母校輔大，曉光從遠處就能看得見的白色三面水泥柱，代表三個教會團體共同復校同心協力的精神。上面大大的寫著輔大的中英文全名。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="4":
                worksheet.update(list[1],int(5))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔從畢業後就沒有再回來學校看過了，他甚至不清楚學校是否在他畢業以後有沒有改建過。走進校園，不僅建築物、銅像甚至是一草一木都和日翔記憶中一模一樣……日翔偷偷捏了自己一把，會痛！有這種痛覺應該不是夢吧！？比起對這些，日翔更想親自詢問那聲音是出於什麼理由把自己帶回來，還有他口中的「表現」又是什麼意思，一切都發生得太突然了，讓日翔感到十分困惑。"+"\n"+"不過日翔很快又發現了一件更重要的問題——他沒有帶課表！剛剛趕著出門只把手機、錢包跟家裡鑰匙塞進書包就出門了，他太久沒有上課的經驗，自然是忘記了課表這回事。日翔的記憶力也沒有好到能夠記得好幾年前大一第一堂課在哪間教室上課。怎麼辦，只能問曉光了。"))
                list_talk.append(TextSendMessage(text="「呃……請問妳知道第一堂課的教室在哪裡嗎……」日翔轉向曉光不好意思地詢問，希望自己聽起來並不是在隨便找什麼理由搭訕，「我太急著出門，忘記帶課表了……」"+"\n"+"「LM503，企業概論。」曉光連看都不必看，直接回答了日翔的問題。"+"\n"+"果然是學霸，連課表都背起來了。日翔在心裡讚嘆。"))
                list_talk.append(TextSendMessage(text="#6 「LM」指的是哪棟大樓呢？（請以「ＯＯＯ大樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="4":
                worksheet.update(list[1],int(5))
                list_talk=[]
                list_talk.append(TextSendMessage(text="曉光從畢業後就沒有再回來學校看過了，她甚至不清楚學校是否在他畢業以後有沒有改建過。走進校園，不僅建築物、銅像甚至是一草一木都和曉光記憶中一模一樣……"+"\n"+"「一點都沒變呢。」不知道是慶幸還是感嘆的曉光，至今還是不敢相信自己又回來了母校。"+"\n"+"「第一堂課在哪裡呢？」一向都是學霸的曉光，即便遇到這種事情也是能不慌不忙的在課業上，曉光拿出手機打開手機的APP查看課表，表定第一堂課的教室在LM503。"+"\n"+"此時身旁的日翔不曉得在慌張什麼，緊張的動作大到連曉光想不注意到也很難。"))
                list_talk.append(TextSendMessage(text="「我太趕著出門，忘記帶課表了，你知道第一堂課的教室在哪裡嗎？」日翔似乎很不好意思地問道。"+"\n"+"「LM503，企業概論。」"+"\n"+"「在校網上的選課清單裡也可以看，日翔同學你也可以用用。」 曉光將自己手機畫面顯示給日翔看。"+"\n"+"「原來如此，謝啦。」"))
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="5":
                worksheet.update(list[1],int(6))
                worksheet.update(list[2],int(1))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="5":
                worksheet.update(list[1],int(6))
                worksheet.update(list[2],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖利瑪竇大樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="「怎麼那麼吵啊…」曉光咕噥著，原本正專心看書的曉光，抬頭往門口方向一看，日翔好像撞到了一個人。而日翔撞到的那個人是據說是個資優生，以優異的成繁星進來的馬宇桓，但趾高氣昂的態度讓人感到相當不愉快，總之還是不要跟這個人扯上關係比較好，曉光想。"+"\n"+"「不過話說回來，帶我回來的那道光提到的『好好表現』，究竟是什麼呢？」曉光陷入沉思，特地帶人回到過去，一定有所目的，但是就憑這句話還沒辦法聯想到任何關聯性。"+"\n"+"「看來這四年可不平靜啊。」像是法官定案的樣子，從早上不小心掉落自己的學生證，到眼前這些大吵大鬧的光景，一切的一切都不是做夢。"+"\n"+"鐘聲響起，為這場總長四年的大學生活揭開第一幕。"))
                list_talk.append(TextSendMessage(text="早上的課很快地結束了，一向獨來獨往的曉光總是在午餐時刻找個寧靜的地方休息，但是一如往常的休息場所，卻充滿著喧囂。「開始了嗎？」熙來攘往的風華廣場正在舉辦活動。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="6":
                worksheet.update(list[1],int(7))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="6":
                worksheet.update(list[1],int(7))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「是社團招生啊。」一向是學霸的曉光，不是很想要花時間在其他多餘的娛樂上，但是聽說學校有「愛狗社」，熱愛動物的曉光，回想起小時候養貓的過程，實在是令人懷念啊。"+"\n"+"然而愛狗社的旁邊剛好是運動社團，曉光聽到熟悉的聲音：「那......加入系籃怎麼樣？」「對了，在12月學校會舉辦......」。曉光說道：「又遇到他們兩個啊…他們說12月有活動？是什麼活動啊？」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="7":
                worksheet.update(list[1],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="一提起體育話題，司晨精神都來了，開始喋喋不休地和日翔討論最近的賽事，彷彿和早上趴在桌上睡著的是不同人。司晨十分好動這點還是和日翔記憶中的一模一樣，日翔總是覺得司晨是在面試體育系的時候走錯教室。"+"\n"+"「咕嚕咕嚕──」尷尬的聲音讓兩人同時沉默了下來。"+"\n"+"「呃......抱歉抱歉，我拖太久了我自己都餓了，哈哈。」司晨尷尬地對日翔笑了笑。"+"\n"+"「那我們就吃飽一點，去外面吃吧。」日翔提議，「外面的小巷子聽說有很多好吃的喔。」"))
                list_talk.append(TextSendMessage(text="#9 學校外面藏有很多美食的小巷叫？（請輸入「ＯＯＯ巷」回答，ＯＯＯ為半形數字。） "))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="7":
                worksheet.update(list[1],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「體育競賽？我沒什麼興趣。」對於把學業能力點滿，社交能力和體育能力卻低到谷底的曉光來說，體育競賽的確是相當不適合她的活動。「不如舉辦個浪浪募款活動，我一定會參加。」曉光嘴角微微上揚，想必是在心裡模擬募款活動的光景吧。"+"\n"+"既然平常的休息場所變得一點也不平靜，很少離開學校吃飯的曉光，拿出手機裡的課表看了看。「嗯…下午剛好沒有課，不如我就去外面吃吧，這還是我第一次去學校外吃飯。」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="8":
                worksheet.update(list[1],int(9))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="8":
                worksheet.update(list[1],int(9))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「還蠻好吃的，下次也來這邊吃吧。」吃了一間叫做歐姆先生的咖哩飯店，感到相當滿足的曉光，心想學校外面明明也有不輸給校內的美食，卻像個籠中鳥不願出學校，未免也太畫地自限了吧。"))
                list_talk.append(TextSendMessage(text="開學最輕鬆的第一個禮拜很快就過去了，曉光漸漸接受起自己回到過去的事實，當然也沒忘記那個聲音要她在學校好好表現。說也奇怪，從那天以後他再也沒有聽到過那個聲音、在學校也尋不到任何線索，曉光也無從詢問「好好表現」具體來說要做什麼才能達到標準。即使如此，曉光仍按著她的生活步調，按部就班的完成每天必做的事情。"+"\n"+"「開學就一定要買書啊。」 以前都是班上的總務統一購買書籍，如今因為疫情的關係，只好自己去採購教科書。聖言樓樓下有一個書局，曉光以前在空堂時都會前往選購、瀏覽書籍。"))
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="9":
                worksheet.update(list[1],int(10))
                worksheet.update(list[2],int(2))
                worksheet.update(list[3],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖聖言樓！趕快去「遊戲地圖」看看！"+"\n\n"+"書局的冷氣吹散了外頭九月悶熱的暑氣。日翔隨意地在書架間瀏覽，他記得以前只在原子筆沒水才進來過少少幾次，他一直都沒注意到書局旁邊還有「每一杯咖啡」這間咖啡廳？比起外面的書局，校內的書局還是顯得要小很多，日翔很快就挑好了幾本。準備去結帳時，日翔看見了走進來的曉光，而曉光也正好發現了自己。"+"\n"+"小、曉光怎麼在這裡！？雖然喜歡看書的曉光出現在書局也不是很意外。"+"\n"+"「你在選書嗎？」"+"\n"+"「咦？啊啊、對......」曉光主動向自己說話讓日翔又驚又喜。"+"\n"+"不過曉光似乎沒有發現日翔的異樣，她的目光落在日翔捧著的書上，「那個......這些書怎麼了嗎？」查覺到曉光的視線，日翔小心翼翼地出聲詢問。"+"\n"+"曉光搖搖頭，「這兩本是一樣的書，只是封面不一樣。」"+"\n"+"「！？真的耶！」日翔翻起內容才發現裡面的內容寫的一樣，只是順序不一樣罷了。可惡！怎麼有這種無良作者，害日翔差一點花了冤枉錢。「差點花錢買下去了......謝謝妳啊，又被妳幫助了。」日翔努力的擺出笑容掩飾面對曉光的緊張。"+"\n"+"「話說，」日翔一面將書放回書架一面向曉光搭話，「妳剛剛明明連內容都沒看卻知道這兩本是一樣的，難不成妳看過了嗎？」"+"\n"+"「嗯，稍微看過。」稍微看過卻連內容都清楚嗎？日翔笑了笑，不過他不打算將這句話說出口。"+"\n"+"「那妳應該很喜歡看書了？之前看妳都在讀書。」"+"\n"+"「……。」"+"\n"+"「我沒有別的意思！就只是剛好看到！真的不是偷窺！」日翔慌張地解釋，不料聽起來卻像此地無銀三百兩的狡辯。"+"\n"+"「很喜歡。」曉光的嘴角揚起了一個淺淺的弧度，要不是日翔和曉光距離得近，日翔可能會漏看難得出現在曉光臉上的笑容。"+"\n"+"「這、這樣啊。」奇怪？剛才有這麼熱嗎？或許是看見喜歡的人意外的笑容，或許是不曾和曉光講過這麼多話，或許是兩者皆有，日翔感覺自己的臉就像熟透的番茄，而方才還很涼爽的地下室現在就像個大蒸籠，悶得日翔喘不過氣。"+"\n\n"+"解鎖童話書！趕快去「個人檔案」看看！"))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="9":
                worksheet.update(list[1],int(10))
                worksheet.update(list[2],int(2))
                worksheet.update(list[3],int(1))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖聖言樓！趕快去「遊戲地圖」看看！"+"\n\n"+"剛踏進去店門口的一瞬間，書局的冷氣讓身上的暑氣馬上就消散了。「真好，看來找到一個好地方了。」正踩著雀躍的小碎步走進門口不到幾秒鐘，日翔正好站在她的前方。"+"\n"+"「天啊，好糗喔，他該不會都看到了吧？怎麼辦，要跟他講話嗎？遇到不打招呼很失禮的，可是…」曉光躊躇了一會兒，發現雙方都站在門口也不是辦法，曉光撇開心裡的那些種種疑惑，鼓起勇氣問了這位站在面前高大的男生。"+"\n"+"「你在選書嗎？」曉光低聲問道，手指著日翔懷裡的書。「咦？啊啊、對......」日翔支支吾吾地回答，曉光對他的反應一點也不在意，反而盯著日翔捧著的書上，「那個......這些書怎麼了嗎？」查覺到曉光的視線，日翔小心翼翼地出聲詢問。"+"\n"+"「這兩本是一樣的書，只是封面不一樣。」曉光搖搖頭。"+"\n"+"「！？真的耶！」日翔翻起內容才發現裡面的內容寫的一樣，只是順序不一樣。"+"\n"+"「謝謝妳啊，差點花錢買下去了......對了，我是跟妳同班的日翔。」日翔努力的擺出笑容掩飾面對曉光的緊張。"+"\n"+"「話說，」日翔一面將書放回書架一面向曉光搭話，「妳剛剛明明連內容都沒看卻知道這兩本是一樣的，難不成妳看過了嗎？」"+"\n"+"「嗯，稍微看過。」講看過好幾次似乎有點太誇張了，講稍微看過就好，曉光這麼是這麼想的，不過確實，熱愛閱讀的曉光，的確是把很多書都讀得滾瓜爛熟。"+"\n"+"「那妳應該很喜歡看書了？之前看妳都在讀書。」"+"\n"+"「……。」"+"\n"+"「我沒有別的意思！就只是剛好看到！真的不是偷窺！」日翔慌張地解釋。這個人緊張的樣子怎麼那麼滑稽，曉光暗自想道。雖然迷迷糊糊的，但是感覺是個不錯的人，曉光認為可以多多觀察這個人。"+"\n"+"「很喜歡。」曉光的嘴角揚起了一個淺淺的弧度。意外認識到了一個有趣的人。"+"\n\n"+"解鎖童話書！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="「來，同學們，試著解解看這幾題。」"+"\n"+"聽到老師這麼說，多數同學接二連三地發出嘆息聲，看來多數同學都不太喜歡寫程式呢，曉光思考著。雖然沒有到喜歡，但也沒有到討厭程式的曉光，回想起過去的光景。"+"\n"+"「這次程式比賽的冠軍是：何曉光同學，恭喜你。」"+"\n"+"面對台下此起彼落的掌聲，曉光戰戰兢兢地走上台上領獎，帶著略顯尷尬的表情，從評審手上領了獎狀。曉光不擅長應付這個場景，連走到台下別人向前跟她祝賀時，曉光也只是快步地離開他們。"+"\n"+"「要是能再勇敢一點就好了，為什麼這麼害怕人呢？」曉光搖了搖頭，不再回想過去。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="10":
                worksheet.update(list[1],int(11))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="10":
                worksheet.update(list[1],int(11))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="11":
                worksheet.update(list[1],int(12))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「阿日！好厲害！你根本是天才！」司晨看著日翔完成的一題題程式碼驚呼道。"+"\n"+"「不不，天才什麼的......」司晨的誇讚讓日翔有些心虛，日翔當然是不可能告訴司晨其實他已經學過了。"+"\n"+"「既然是天才，想必再困難的題目也難不倒你吧？」冰冷的聲音在兩人背後響起，兩人轉過頭一看發現竟是宇桓。"+"\n"+"「你是誰啊？」查覺到來者不善的司晨先發制人問道。"+"\n"+"宇桓瞥了司晨一眼，「我並不是在跟你說話，我找的是這位『天才』同學。」宇桓語帶嘲諷的強調「天才」兩個字。"+"\n"+"「哼...不過挑戰者先自報門號才符合禮節吧？」宇桓推了推眼鏡繼續說，「我叫宇桓，跟你同班。」"+"\n"+"「呃、宇桓同學？你是不是搞錯什麼......」如果可以，日翔還真不想接受宇桓的「挑戰」。話又說回來，這次還是被宇桓給盯上了嗎？自己到底是哪裡惹到宇桓了呢......"+"\n"+"「搞錯？我可是清清楚楚的聽見這個笨蛋叫你天才。」宇桓像是怕日翔聽不懂一樣一字一字緩緩地說，「怎麼了？該不會是害怕了？」"+"\n"+"「你這人從剛剛就一直瞧不起人啊！」被宇桓直罵的司晨晨憤憤地指著宇桓，「阿日怎麼可能會輸給你！不管你要出幾題阿日都會解開的！」"+"\n"+"「就當你是接受了。」宇桓一臉計畫通地笑了，語氣也不容許日翔拒絕。"+"\n"+"中了宇桓的圈套啊......宇桓想必是針對司晨容易被挑釁這點出手的。看來不解開宇桓的難題，宇桓是不會罷休了。"))
                list_talk.append(TextSendMessage(text="#13 請問下圖最後會出現什麼結果？（請以「Ｏ」回答，Ｏ為半形數字。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/10/J106XE.png', preview_image_url='https://upload.cc/i1/2022/03/10/J106XE.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="11":
                worksheet.update(list[1],int(12))
                list_talk=[]
                list_talk.append(TextSendMessage(text="才沒幾分鐘，曉光已經把老師指定要做的習題練習完了，而曉光正打算繼續寫程式時，突然眼角餘光看到了一個身影，是比較瘦長型的身材。「我聽說你…曾經也是知名高中的榜首吧？」聽到這個口氣，就知道來著不善，曉光只好停下手邊的事情，馬宇桓？怎麼會突然和我搭話呢？?我需要搭理他嗎？ 曉光一臉疑惑的看著這名不速之客。「忘了自我介紹，我曾經是數理資優班的，以優異的成績特殊選才進來輔大的『馬宇桓』，請多指教。」"+"\n"+"「真麻煩，遇到一個棘手的人。」曉光不滿的呢喃，「我是何曉光，請問有什麼事情嗎？」"+"\n"+"「也沒什麼啦，只是想問看看你有沒有興趣解這題程式，這可是很知名的迷宮問題喔，我想你應該聽過吧？」"+"\n"+"竟然第一次見面就下馬威，真是討厭的人，曉光默默的在內心留下這個評語。此時曉光的腦袋開始以高倍率的速度運轉。要是我沒有回答他的問題，感覺他會更加小看我，既然都報上自己過去的經歷，想必是很在意學歷的人，唉…這世界上還真的是什麼人都有呢。曉光左思右想，說道：「我有聽過，也知道怎麼解釋這題。」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="12":
                worksheet.update(list[1],int(13))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#14 下列以Python語法撰寫出的程式碼最後輸出結果為？（請以「x=Ｏ」回答，Ｏ數量不代表實際答案字數。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/uHLoSw.png', preview_image_url='https://upload.cc/i1/2022/03/25/uHLoSw.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="12":
                worksheet.update(list[1],int(13))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="13":
                worksheet.update(list[1],int(14))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="13":
                worksheet.update(list[1],int(14))
                list_talk=[]
                list_talk.append(TextSendMessage(text="只見曉光以飛快的速度打著程式碼，三兩下就達成宇桓的要求，這點讓宇桓目瞪口呆。"+"\n"+"「還有其他問題嗎？」 你真的干擾到我的讀書進度了，當然曉光沒有說出口，只是內心這麼覺得。"+"\n"+"宇桓露出一臉尷尬的表情，說道：「哎呀，沒想到你那麼厲害，果然名不虛傳，沒了，我問完了，下次我會再拿其他題目來『請教』你。」語畢，宇桓轉身快步離開。「這個人完全是日翔同學的翻版呢…連謝謝都沒說，下次他再來找我，我是不是要裝作沒看到？」曉光長嘆一口氣，無奈的聳了聳肩。"+"\n"+"解了無數道題目的曉光，身心俱疲之下決定去吃點東西，但是曉光不太想出去校門，「對了！現在就是好時機，就去吃那個傳說中的『輔大三寶』好了。」曉光一手手掌張開，一手拳頭敲了一下掌心，像是在蓋章一樣，對這個臨時想到的提案感到相當滿意。"))
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
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="14":
                worksheet.update(list[1],int(15))
                worksheet.update(list[2],int(2))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="14":
                worksheet.update(list[1],int(15))
                worksheet.update(list[2],int(2))
                list_talk=[]
                list_talk.append(TextSendMessage(text="據說吃甜點能促進大腦思考，這是曉光從書上學到的，因此曉光很喜歡吃甜食。聽到輔大有地方賣鬆餅，二話不說就來到輔大的「心園餐廳」。心園位於信義和平宿舍的地下室，因此第一次去不注意環境的話很可能會錯過。心園除了有輔大三寶之一的鬆餅外，也提供便宜的果汁、餐點，甚至還有雜貨店等，因此被眾多學生評價為CP值最高的學餐。"))
                list_talk.append(TextSendMessage(text="「要點什麼好呢？」曉光從上到下、從左到右，巡視著菜單上的一行一句。此時突然有個聲音打斷了她的思考迴路。"+"\n"+"「曉光？你也來買鬆餅嗎？」曉光不用看到對方，就能知道是誰在和她說話。"+"\n"+"「嗯。還在想要點什麼，那日翔同學你想要點什麼？」曉光說完這句後，才轉過身子看著日翔。"+"\n"+"「哈哈、畢竟菜單很多選擇，連鹹的口味也有。」日翔說起他第一次買鬆餅時，也因為五花八門的口味而思考了很久要買什麼。曉光能想像日翔站在店門口，埋頭苦思的樣子，光是想像這個光景，就覺得挺有趣的，曉光小聲地笑了一聲。"+"\n"+"「怎麼了？有什麼好笑的？」日翔歪著一邊的腦袋，疑惑的看著曉光。「沒..沒什麼啦」曉光為了不要把話題轉向自己身上，趕緊又接了下一句，「對了，要不要一起點餐？」當曉光說出這句話時，曉光感覺用了她畢生以來所有的勇氣。"+"\n"+"「當然好啊。」日翔爽快的答應曉光，但日翔似乎沒發現曉光的緊張。曉光聽到日翔幫他自己點了玉米蔬菜，幫他旁邊的司晨點了蜂蜜奶油，還有她的鮮奶油。"+"\n"+"「太好了，我期待已久的鬆餅。」曉光正準備從錢包裡找出零錢準備付款，但卻怎麼也找不到零錢。"+"\n"+"「阿司你的加上我的95元，曉光的……怎麼了嗎？」日翔問道，一向冷靜的曉光，這時卻亂了分寸。"+"\n"+"「……沒有足夠的零錢……只有大鈔……」要趕快把大鈔換成小鈔才行。正當曉光這麼想時，日翔竟然說出曉光意想不到的話：「這樣啊……那不用給我了。」曉光嚇了一跳，曉光從來也沒有想過會有這樣子的答覆，為什麼要對我這麼好？曉光臉上堆滿疑惑。"+"\n"+"日翔繼續解釋，「呃、我的意思是，上次妳不是幫了我嗎？當成那次的回禮好了。」上次？是說書局那一次嗎？原來他還記得，我還以為對他來說是不重要的小事情。曉光原先認為日翔是個迷糊的人，可是他卻把別人的事情牢牢記著。「看來跟想像中的有所誤差呢。得修正對他的印象才行。」"+"\n"+"在日翔和司晨正在小倆口鬥嘴時，曉光在一旁更正她的評價。「下一次換我請他好了，如果有遇到他的話。」曉光點了點頭，握起手心說著：「一定要更努力才行，一掃以前怯弱的我。」"+"\n\n"+"解鎖遊O王卡！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="時間很快地過去，讓大家最頭痛的期中考也悄悄地來了。幸好曉光還保有過去的記憶，重理解一次課程上的問題對她來說並不困難。請完成以下題目安全度過期中考："))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="15":
                worksheet.update(list[1],int(16))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="15":
                worksheet.update(list[1],int(16))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="16":
                worksheet.update(list[1],int(17))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="16":
                worksheet.update(list[1],int(17))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="17":
                worksheet.update(list[1],int(18))
                list_talk=[]
                list_talk.append(TextSendMessage(text="期中考的分數公布下來後，日翔考了一個不錯的分數，司晨也在日翔的幫（洩）助（題）下安全地擦邊通過了期中考。"+"\n"+"「阿日！你看！我活到現在第一次考這麼高欸！」司晨興奮地將考卷舉到日翔面前，「阿日你怎麼猜題都猜得那麼準啊！」"+"\n"+"「就、剛好從學長姐那邊拿到考古題啦～」"+"\n"+"「真好啊！那我期末也靠你罩了啊！」"+"\n"+"日翔有時很慶幸還好司晨並不會過問那麼多，他可不擅長撒謊啊！"+"\n"+"「曉光呢？考得怎麼樣？」日翔轉頭詢問坐在兩人後面的曉光，但其實日翔不需要問也知道結果了，曉光可是提高班上平均分數的大學霸啊。"+"\n"+"「還行。」曉光給了日翔一個模稜兩可的回答，不過日翔聽得出曉光語氣裡的透露了一絲喜悅，看來考試的結果也讓曉光很滿意呢。"))
                list_talk.append(TextSendMessage(text="在輔大大學入門課程中，為了讓學生更加了解校園環境，學校會安排學生參觀校史室跟淨心堂這兩項活動。"))
                list_talk.append(TextSendMessage(text="#19 校史館在哪一棟建築的二樓呢？（請以「ＯＯ樓二樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="17":
                worksheet.update(list[1],int(18))
                list_talk=[]
                list_talk.append(TextSendMessage(text="期中考的分數公布下來後，曉光一如往常的發揮原本的實力，考了讓其他人望塵莫及的分數。當老師念到曉光的名字與分數時，只見班上發出一陣一陣大小聲不間斷的驚呼聲，但曉光早就已經習慣這種氛圍。當曉光從前方遞回老師手上的考卷以後，剛坐到座位上時，坐在前方的日翔轉過頭來說：「曉光妳很強欸，你看我才考這樣而已。」 日翔指了一指手上的考卷，雖然跟曉光的分數差了一大截，但是日翔本人看起來一點也不介意，反而還傻呼呼地笑著。"+"\n"+"「沒什麼，基本實力而已。」從原本不太敢跟人互動曉光，到現在能夠和日翔說上話，曉光認為自己進步了很多。「有不會的再來問我吧。」"+"\n"+"「可以嗎？謝謝妳了！」期中考就在兩人的約定下落幕了。"))
                list_talk.append(TextSendMessage(text="在輔大大學入門課程中，為了讓學生更加了解校園環境，學校會安排學生參觀校史室跟淨心堂這兩項活動。"))
                list_talk.append(TextSendMessage(text="「曉光！」這時候找曉光搭話的不是日翔，而是與曉光上同一堂課的「林真澄」。"+"\n"+"「真澄同學？你也選了我們班的大學入門嗎？」真澄是隔壁班的同學，有一次修同一堂通識課偶然認識的，她常常把課程排得很滿，因為衝堂的關係，改修曉光班上的課。曉光回想起當初也沒有和真澄同學講過太多話，這次要多認識看看真澄。"+"\n"+"「對啊，要是都能照我所想的選課就好，偏偏學校設了一大堆選課規則，超級麻煩的。」看來她又把課表填滿了，真厲害。"+"\n"+"「真澄還是一樣修很多課呢。」曉光佩服地說。"+"\n"+"「雖然修了很多課，但是樣樣不精。」真澄無奈地說，「倒是我聽說曉光微積分期中考考得不錯喔。」"+"\n"+"「咦？妳從哪裡聽到的？」"+"\n"+"「秘密！」真澄俏皮地眨了眨眼。"+"\n"+"真澄應該沒有和她修同一堂微積分，那她是怎麼知道她考的很好這件事？是有人走漏風聲嗎？但這件事有這麼值得和別人四處八卦嗎？還是是真澄自己觀察到的？要是是這樣，真澄的觀察力還真是敏銳。"+"\n"+"「先不說這個了，先聽導覽吧。」真澄不等曉光的回答，快步走向導覽員。「還真是強勢的一個人，我也趕快跟上吧。」曉光也加緊腳步，走向導覽員旁邊聆聽導覽。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="18":
                worksheet.update(list[1],int(19))
                list_talk=[]
                list_talk.append(TextSendMessage(text="校史室位於野聲樓二樓，就像一座位於輔大的小型博物館，存放著從開校以來到現今所保存的各種珍貴文物。校史室不僅只是展示，更是保存、傳承下發生在輔大的故事。"))
                list_talk.append(TextSendMessage(text="#20 在大學入門課程中，導師會帶學生去什麼地方傾聽神父的禱告呢？（請以「ＯＯＯ」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="18":
                worksheet.update(list[1],int(19))
                list_talk=[]
                list_talk.append(TextSendMessage(text="校史室位於野聲樓二樓，就像一座位於輔大的小型博物館，存放著從開校以來到現今所保存的各種珍貴文物。校史室不僅只是展示，更是保存、傳承下發生在輔大的故事。"))
                list_talk.append(TextSendMessage(text="#20 在大學入門課程中，導師會帶學生去什麼地方傾聽神父的禱告呢？（請以「ＯＯＯ」回答。）"))
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
            list.append('E'+str(j))
            list.append('C'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="19":
                worksheet.update(list[1],int(20))
                worksheet.update(list[2],int(3))
                worksheet.update(list[3],int(3))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖淨心堂！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="眾所皆知輔大是天主教大學，當然少不了大型教堂，淨心堂開放也開放讓非天主教教徒進入禱告，走在輔大校園內也可以看見一些神父及修女。此外，除了淨心堂，輔大校內也設有淨心室讓同學進入沉澱心靈。淨心堂和日翔以往在電視影集上看到的教堂不太一樣，淨心堂的座位六個一排呈半圓狀，可以容納至少一個班級以上的學生數量，和日翔印象中的兩個一排的教堂有所不同。"+"\n"+"無論是從窗戶照進來的和煦陽光，還是神父溫厚的聲音都讓人感到十分舒適，甚至讓日翔的眼皮越發沉重。日翔揉了揉眼睛想驅散睡意，卻發現隔壁的司晨已經開始有一下沒一下地點頭打起瞌睡了。在抵抗了一會，日翔最終也敵不過睡魔緩緩閉上雙眼——"+"\n"+"再次睜開雙眼，日翔看見的是一張空白的圖畫紙，還有一隻小手正握著蠟筆努力的在白紙上畫著什麼。從這個視角看來，自己應該是變成了小手的主人，日翔試著移動身體卻只是徒勞，小手的主人目前似乎不打算做塗鴉以外的事。"+"\n"+"不知過了多久，日翔的視線終於從圖畫紙上移開，他看見一個面容模糊的小孩子正常自己走來。日翔可以感覺到他的嘴巴正一開一闔的，似乎在跟那孩子說些什麼？不過他們的聲音卻傳不進日翔的耳裡，好像隔得好遠好遠......"+"\n"+"「——日！阿日！」司晨的呼喚聲讓日翔從睡夢中驚醒過來。"+"\n"+"「欸、欸？我睡著了嗎！？」日翔記得自己只是想閉目養神一下子的。"+"\n"+"「睡得可熟啦！你看你還流口水！」司晨指了指日翔的嘴角。"+"\n"+"「口水！？」日翔連忙伸向司晨指示的地方，卻沒有預想中濕滑的觸感。"+"\n"+"「噗、哈哈哈騙你的啦！」見日翔上當後司晨憋不住放聲笑了出來，日翔則給了後者一個大白眼。"+"\n"+"日後日翔回憶起那個沒頭沒尾的夢，竟有種說不出的熟悉感，好像從很久很久以前就認識了那個面容模糊的孩子......"))
                list_talk.append(TextSendMessage(text="解鎖圖畫！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="#21 日翔下一節課在進修部上課，請問以下哪個課程最可能在進修部大樓上課呢？"+"\n"+"（Ａ）微積分"+"\n"+"（Ｂ）會計"+"\n"+"（Ｃ）通識"+"\n"+"（Ｄ）統計學"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#21',
                    template=ButtonsTemplate(
                        title='#21',
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="19":
                worksheet.update(list[1],int(20))
                worksheet.update(list[2],int(3))
                worksheet.update(list[3],int(3))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖淨心堂！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="眾所皆知輔大是天主教大學，當然少不了大型教堂，淨心堂開放也開放讓非天主教教徒進入禱告，走在輔大校園內也可以看見一些神父及修女。此外，除了淨心堂，輔大校內也設有淨心室讓同學進入沉澱心靈。"+"\n"+"曉光和真澄正位於淨心堂之中，跟著班級的所有人聆聽神父的一言一語。雖然兩人在天主教大學就讀，但並沒有相關的宗教信仰，於是這對他們而言這是頗為新鮮的體驗。二樓的聖堂整體打造為扇形的格局，據說，這擁有「教友將歸向天主」的意義。"+"\n"+"雖然曉光並不是天主教徒，但仍舊認為宗教的言語多少給人溫暖人心的力量，或許這便是教徒們會選擇跟隨神明的原因吧，她默默地想。"+"\n"+"突然間，她想起在很久以前自己似乎也感受過這樣柔和的、宛如午後坐擁薄雲的陽光——腦海裡和誰牽著手的模糊影像閃過了一瞬，緊接著是小時候的她將一張稚氣的圖畫送給了誰的畫面……可除此之外，曉光卻什麼都想不起來。"+"\n"+"算了，應該不是很重要的事情吧。曉光決定不再去想，並隨著神父的指示闔上雙眼聆聽禱告詞。"))
                list_talk.append(TextSendMessage(text="解鎖圖畫！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="#21 曉光下一節課在進修部上課，請問以下哪個課程最可能在進修部大樓上課呢？"+"\n"+"（Ａ）微積分"+"\n"+"（Ｂ）會計"+"\n"+"（Ｃ）通識"+"\n"+"（Ｄ）統計學"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#21',
                    template=ButtonsTemplate(
                        title='#21',
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="20":
                worksheet.update(list[1],int(21))
                worksheet.update(list[2],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖進修部！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="日翔其實很喜歡通識課程，除了系上排除課程外，在通識課可以學到各領域的知識。日翔這次很幸運地選上了過去在DCard上大家都很推薦卻一直沒有選上的課程，不過......"+"\n"+"「太慢了！」日翔才找到位置坐下，立刻遭到宇桓的斥責。沒錯，籤王日翔，雖然選上了喜歡的課，但他沒料到宇桓也選了同一門課，甚至連分組報告也和宇桓同一組。"+"\n"+"「根本還沒開始上課啊......」日翔小聲地抱怨。"+"\n"+"一開始在通識教室裡看見宇桓時，日翔差那麼一點點🌌🤏想直接退選出去了，但學校規定："))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="20":
                worksheet.update(list[1],int(21))
                worksheet.update(list[2],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖進修部！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="「曉光，下一堂課剛好是通識課，我們就一起去吧。」曉光答應了真澄的邀約。"+"\n"+"「對了，曉光你還修了什麼通識課？我還修了有關古物鑑賞的課程，因為我最喜歡寶石和研究各式各樣的卡牌。」真澄自顧自地說了起來。"+"\n"+"「真澄，這是什麼領域的課啊？」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="21":
                worksheet.update(list[1],int(22))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="21":
                worksheet.update(list[1],int(22))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「當然是藝術與人文啦，我聽說學校規定三個領域的課都要選滿兩堂課，其中一堂還要跟歷史有關係，為什麼不都全部是藝術人文就好？啊啊，學校也規定太多了。」真澄無奈的抱怨著。"+"\n"+"「這也是沒有辦法的事情。學習其他知識也沒有壞處。」曉光也不能改變學校，只好這樣安慰真澄。"+"\n"+"「是說，曉光，要不要我幫你算算看你未來的運勢。」"+"\n"+"「咦？」真澄話題轉變得十分突然，讓曉光一時之間反應不過來。"+"\n"+"「別這麼緊張，放輕鬆，我就用我這典藏已久的塔羅牌幫你算看看。」只見真澄從書包裡拿出一副閃亮亮的卡牌，卡牌的樣式是各種國王與皇后戴著珍貴的寶石的照片，雖然曉光對占卜並無涉獵，但從對卡牌的保護看得出真澄有多喜歡這些卡片。"+"\n"+"「這可是我最喜歡的牌喔，你看看這些耀眼的寶石，像極了女人一生的生命。還有……咳嗯，扯太遠了，抱歉我太興奮了，你想要算什麼呢？」"+"\n"+"曉光左思右想，面對這麼多突如其來的怪事，還是算算未來的命運好了，看看能不能順利度過這次的大學生活。"+"\n"+"「那幫我算算看大學四年過得怎麼樣好了。」"+"\n"+"「沒問題。」真澄將她手中的塔羅牌攤在桌上，要求曉光指出一張牌。"+"\n"+" 如果想得越多感覺越干擾結果，這時候就隨著心走吧。曉光不假思索的指了一張牌。"))
                list_talk.append(TextSendMessage(text="「我看看啊，這張牌是太陽，這張牌的涵義是說：『將會有一道光指引你，走向正確的道路，朝著那道光勇敢前進吧。』」"+"\n"+"光？怎麼又是光？原本是流星，現在又是太陽。曉光陷入了沉思，流星和太陽會指引她走向什麼樣的道路呢？"+"\n"+"「怎麼了，曉光？是不是覺得我的占卜準到讓你目瞪口呆啊。」"+"\n"+"「呃不，沒什麼事情，謝謝你幫我占卜。」"+"\n"+"雖然占卜本來就不一定會成真，但還是相信看看好了，至少對我沒什麼損失。"+"\n"+"鐘聲一響，兩人回到各自的座位上開始準備上課。"))
                list_talk.append(TextSendMessage(text="一連下好幾周的雨終於放晴了，班代在班群宣布今天體育課在籃球場上打球，曉光對於這個消息不是很高興。"+"\n"+"「還真是不想運動。」曉光噘著嘴說著，通堂體育課曉光只會待在陰涼處，觀察附近的動植物，只有偶爾被老師叫到的時候才會意思意思的活動一下。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="22":
                worksheet.update(list[1],int(23))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="22":
                worksheet.update(list[1],int(23))
                list_talk=[]
                list_talk.append(TextSendMessage(text="在輔大體育課都是0學分，且大一二都為必修課程。對某些主張「大學生就是要軟爛！」的人來說體育課非常麻煩，恨不得能翹就盡量翹，但是曉光想到翹課會影響她的體育點名成績，想一想還是不翹課的好。"+"\n"+"不像曉光在高中體育課那樣，老師會強迫大家動起來，在大學，體育課教授比較睜一隻眼閉一隻眼，只要完成指定活動就可以在旁邊休息或自由活動。"+"\n"+"「還真是熱血啊，那些男生。」曉光看著場上的日翔與司晨，揮灑著淋漓的汗水。剛下完雨的球場地板還殘留著一個個大小水坑，然而曉光還看到司晨不小心跌進水坑裡面，只好趕緊撇開視線，雖然對司晨很不好意思，曉光還是不小心笑了出來。"))
                list_talk.append(TextSendMessage(text="刺眼的陽光讓曉光想起的真澄幫她占卜的結果，「指引我的一道光啊…究竟在何方呢？」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="23":
                worksheet.update(list[1],int(24))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="23":
                worksheet.update(list[1],int(24))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="24":
                worksheet.update(list[1],int(25))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="24":
                worksheet.update(list[1],int(25))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="25":
                worksheet.update(list[1],int(26))
                list_talk=[]
                list_talk.append(TextSendMessage(text="早早完成考試的日翔交了卷走出考場，最後一科剛好是許多學生眼中最「硬核」的考科，因此像日翔一樣提早交卷的學生只有少少幾人，大多不是對自己很有信心，就是早已放棄打算明年再重修。"+"\n"+"時間已經來到六月底，距離日翔回到過去也快要過了一年。在這一年間，日翔找不到任何關於那個神祕聲音的線索，但他並沒有忘記自己在出社會後滿滿的後悔感，也沒有忘記執行「Code/140.136」時想重回大學把握時光的決心。日翔認真地度過每一天，雖然不知道有沒有符合神秘聲音對他的期待，但日翔認為這是報答他最好的方式了。"+"\n"+"天空的湛藍讓日翔想起了曉光那寶石般閃耀的雙眸，「如果我能變成更好的人，曉光會不會注意到我呢......」日翔用只有自己能聽到的聲音低喃道。"))
                list_talk.append(TextSendMessage(text="解鎖大二劇情"))
                list_talk.append(TextSendMessage(text="日翔睜開雙眼，只見自己竟然置身於一團迷霧之中，他將自己的雙臂前伸，卻沒能清楚看見自己的手，這大概就是｢伸手不見五指｣吧，日翔迷迷糊糊地想。比起這個，這到底是什麼地方？雖然對這裡完全感到陌生，但卻一點都不令人感到害怕。"+"\n"+"「呼啊——好久不見啦。」頓時，整個空間傳來熟悉的聲音，日翔甚至都沒有整理好思緒就被他給驚乍住了；而且，聽起來他甚至在慵慵懶懶地打著呵欠？"+"\n"+"日翔對這個聲音十分印象深刻，畢竟，去年帶他回到大一生活的那個「Code/140.136」回傳的瞬間，也聽到了與他別無二致的聲音。不僅如此，日翔隱隱約約感受到，這位就是這個迷霧空間的主人。"))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="25":
                worksheet.update(list[1],int(26))
                list_talk=[]
                list_talk.append(TextSendMessage(text="期末考終於結束了，曉光背起背包正要離開時，突然聽見一個聲音在她耳邊呢喃著，「回到過去了，好不好玩啊？」曉光抬起頭來，想要找出聲音的來源，卻怎麼樣都找不到。「是錯覺嗎？」曉光沒有多想，一如往常地踏上回家的路程。"+"\n"+"悄然夜晚，萬物進入夢鄉。正準備入睡的曉光站在窗邊，望向星光熠熠的天空。已經一年了，仍沒有想出那聲音告訴她的好好表現是什麼意思，曉光愁眉不展的歎了一口氣，「究竟要做什麼呢…？」這個問題一直存在曉光的心中。搖了搖頭，蓋上棉被的曉光，決定將這個問題拋開。"))
                list_talk.append(TextSendMessage(text="解鎖大二劇情"))
                list_talk.append(TextSendMessage(text="「呼啊——好久不見啦。」"+"\n"+"「誰？是誰在說話？這裡是哪裡？」"+"\n"+"「這裡是你的夢，至於我是誰，哼哼哼，大膽刁民竟然敢問本皇的尊名，我才不告訴你。」"+"\n"+"曉光對這個聲音十分印象深刻，畢竟之前才聽到相似的聲音，曉光當時還沒意會到聲音的主人是誰，但是能在夢裡和她對話，唯一想到的可能性就是那道光，沒有錯，就是那道光之中的聲音。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=ButtonsTemplate(
                        title='？？',
                        text='你到底是誰？為什麼要讓我回到大學生活？',
                        actions=[
                            MessageAction(
                                label='？？',
                                text='你到底是誰？為什麼要讓我回到大學生活？'
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、AE=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="26":
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

    elif event.message.text=="你到底是誰？為什麼要讓我回到大學生活？":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、AE=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="26":
                list_talk=[]
                list_talk.append(TextSendMessage(text="滿腔的疑問終究淹沒了曉光，她忍不住向聲音詢問。"+"\n"+"「你的表現比我想像中的好嘛。不過還是不夠，你還需要…」沒有搭理她的疑問，只是自顧自的講起話來，讓曉光一頭霧水。「你猜猜，我是來找你做什麼的？」"+"\n"+"曉光總覺得這個不明的聲音別有居心。她認為必須要趁現在趕快問清楚那傢伙的目的：「應該不是來跟我閒話家常的吧？」"+"\n"+"「答、對啦——！我只是來看看你過得怎麼樣而已。怎麼樣，大學生活好玩嗎？」對面給出了令人傻眼的回答。"+"\n"+"「你究竟有什麼目的？特地帶我回到過去又是為了什麼？」曉光向聲音問道。"+"\n"+"「總而言之，能像你一樣得到重返大學生活的機會的人『幾乎』是沒有的……這次啊，你得好好把握……」不明的聲音並沒有打算和曉光多說，整個夢境便已經隨著逐漸模糊的聲音消逝而去。"))
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="26":
                worksheet.update(list[2],int(5))
                list_talk=[]
                list_talk.append(TextSendMessage(text="待到日翔重新拾起話語權時，他卻已經回到了柔軟的床上——伴隨手機鬧鐘叮鈴鈴地鬧騰，他意識到剛才與迷霧的對話僅不過是一場夢。"+"\n"+"日翔關閉擾人的鬧鐘，思考道：那場「夢境」清晰得不得了，和真實在眼前發生過的事情沒兩樣。剛剛所經歷的夢真的是一場夢嗎？……不過，能重返大學生活本身，就已經是件不科學的事情了，日翔更傾向於將這場「夢境」視作真正發生過的事情。"+"\n"+"他拍拍臉頰振作自己，今天是開始上課的日子——重新升上大二的上課日。秉持著「好好把握」的理念，他並不想在第一天就遲到。"))
                list_talk.append(TextSendMessage(text="解鎖伯達樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="開學的第一堂課是在伯達樓。伯達樓也是資管系學生常常前往的大樓。除了有資管系的機房之外，系學會也在這裡。另外也有BS440等新型教室，採光優良、設備新穎。除了有大大的白板跟投影螢幕外，甚至還有足夠的充座可以提供給每個學生使用筆電、平板等，無須擔心充電問題。"+"\n"+"過了不知道多久，這堂課終於結束了，日翔拎起背包，正打算去514巷覓食。他習慣性地偷偷看了一眼他打從幾年前就有些在意的曉光，雖然平常都看不太出她的感情起伏，但日翔隱隱約約注意到，她的動作比平常要更輕巧，而且似乎盯著手上的一張兌換券。記得曉光上次填寫教學評量，好像抽中了食科冰淇淋的兌換券……"))
                list_talk.append(TextSendMessage(text="#27 經典輔大美食：食科冰淇淋最接近哪個學餐？（請以「Ｏ園」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="26":
                worksheet.update(list[2],int(5))
                list_talk=[]
                list_talk.append(TextSendMessage(text="回過神來，曉光猛然睜開雙眼，眼前只有熟悉的天花板，伴隨手機鬧鐘分秒不差、無從寬待的鈴鈴作響，她意識到剛才與不明的聲音的對話不僅僅只是一場夢。"+"\n"+"曉光關閉鬧鐘，仔細回想起剛剛那場「夢境」，曉光很快就明白到，這不是在開玩笑，也不是整人節目，所有事情都無法合理解釋。"+"\n"+"「難道是…外星人？書上說的超科學力量？」 曉光噗哧一笑，「怎麼可能嘛。」總之，暫時是想不出理由去說明現況，但是曉光相信那場夢絕對有所含意。"+"\n"+"轉眼間就來到開學，「既然還想不到能回去的方法，只好繼續加油吧，何曉光，你一定可以的。」曉光鼓舞自己，並背起上學用的包包準備出門。"))
                list_talk.append(TextSendMessage(text="解鎖伯達樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="開學的第一堂課是在伯達樓。伯達樓也是資管系學生常常前往的大樓。除了有資管系的機房之外，系學會也在這裡。另外也有BS440等新型教室，採光優良、設備新穎。除了有大大的白板跟投影螢幕外，甚至還有足夠的充座可以提供給每個學生使用筆電、平板等，無須擔心充電問題。"+"\n"+"「終於結束了。」外表看似沒有情緒起伏的曉光，實際上內心非常雀躍。「今天就是那一天了！」曉光打開書包，拿出一張紙，小心翼翼地放在桌上擺整齊，雙手合十拜了拜。"+"\n"+"「還以為抽不到呢，沒想到真的抽中我了，我猜一定是回到過去後運氣增加了。」曉光得意的點了點頭。原來曉光抽到的是輔大食科冰淇淋的兌換卷，只要填寫教學評量就有機率抽中，但據說抽中的人微乎其微，所以這次曉光能抽到這張稀有的兌換券，就連曉光自己也不可置信。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="26":
                worksheet.update(list[1],int(27))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="26":
                worksheet.update(list[1],int(27))
                list_talk=[]
                list_talk.append(TextSendMessage(text="正當曉光準備拎著背包前往食科冰淇淋區兌換冰淇淋時，一個熟悉的聲音叫住她。"+"\n"+"「曉光！你抽到冰淇淋券了？真幸運！」這個熟悉的聲音說道。"+"\n"+"「謝謝你，我只是順手填了教學評量。」曉光抬起頭來回應聲音的來源。和她搭話的人是日翔，剛開學的時候就偶然遇上的班上同學，蠻有禮貌的一個人，常常會跟曉光搭話，燦爛的笑容總是讓曉光不知所措。"+"\n"+"正當日翔和曉光邊聊天邊往教室門口走去，正巧遇到大搖大擺晃進教室的司晨，他很自然地插話道：「剛剛是不是有人提到食科冰？我也要去吃！」"+"\n"+"司晨是日翔的朋友，他們總是形影不離，只要有日翔的地方就會有司晨。"+"\n"+"「遲到了卻還那麼厚臉皮，真是不可思議。」出乎曉光意料，司晨不但沒有感覺到羞愧，反而笑嘻嘻地說著。"+"\n"+"「這是在誇我嗎？謝謝你呀曉光、嘿嘿。」這個人還真是粗線條啊，曉光暗自給了司晨一條評語。"+"\n"+"「阿司啊，正常人會覺得這是在誇獎嗎？」日翔敲了敲司晨的腦袋瓜。"+"\n"+"「哎，又沒關係第一周是加退選吧，也不點名啊！大好時光當然要去吃早餐嘛。」說完這句話的司晨，也拍了拍日翔的背，像是在回敬一樣。"+"\n"+"於是，一行人以兩人聊天一人吐槽的模式邊走邊聊，一邊走下博達樓的樓梯，這時，司晨看看班群的機測通過名單，苦惱道：「哎、我上兩次機測都只有對一題，這樣真的可以畢業嗎？」"+"\n"+"日翔用詫異的眼神看看司晨：「你不知道嗎？機測其實不一定要一次通過，只要……」"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="27":
                worksheet.update(list[1],int(28))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="27":
                worksheet.update(list[1],int(28))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「原來只要累計三題、再去選修我們系上的程式語言課程就可以算是通過機測了嘛！那就好，我這次再答對一題就可以不用再考了！」司晨露出了像是「賺爛了」的眼神，就好似撥雲見日一般，剛剛懊惱的樣子早已煙消雲散。"+"\n"+"如果能一次過當然是最好的，除了曉光、日翔、宇桓，還有其他少數同學以外，多數同學都還沒通過測驗，看來系上的機測蠻有鑑別度的。"+"\n"+"「怎麼了，曉光，你不是早就通過測驗了？」日翔看著曉光問道。"+"\n"+"「不，沒什麼，聽到司晨同學不用再考試，也覺得挺開心的。」"+"\n"+"「對吧對吧，阿日，這是多麼值得慶祝的一件事啊。」司晨蹦蹦又跳跳的說著。"+"\n"+"「嗯？你們看，風華廣場今天這麼熱鬧，是不是有什麼好玩的！」正在興奮情緒中的司晨，手指了指豐華廣場的方向。"+"\n"+"曉光看他像大一新生一樣興奮，依然維持著淡然的樣子默默開口：「那個，是課指組舉辦的……」"))
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
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="28":
                worksheet.update(list[1],int(29))
                worksheet.update(list[2],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「啊——我想起來了，原來又到了社團博覽會的季節，時間過得真快。」司晨撓撓頭，似乎終於回想起來去年剛開學的時候也有社博這回事。"+"\n"+"「你居然忘記了，前一年的社博我們是一起參加的吧？去年明明我們都有意願加入系籃，你現在就給我忘了？」日翔失笑，這些年跟司晨相處他很明白他直率過了頭的腦袋，總是讓人有種他能考上資管系真是奇蹟的感覺。"+"\n"+"對日翔而言，他已經和司晨一起逛熱鬧的風華廣場好多次了。不過他可以確定，這一年的社博一定比過往更加獨特，因為無論參加與否，他所喜歡的曉光這次就在旁邊。日翔不經意地將視線撇向曉光——就這麼巧，她也正好往這邊看了過來。"+"\n"+"「……嗯、怎麼了？」曉光注意到了剛剛的注視。冰藍的眸子裡仍然讀不出表情，這也是身為高嶺之花她最獨特的地方，日翔盯著她的眼睛，思緒竟然發散了起來。"+"\n"+"下一刻，日翔才回過神來急急忙忙回應曉光的疑問：「啊沒、沒什麼！只是有點好奇曉光會不會參加社團而已。」"+"\n"+"跟著下課的人流走著走著，食科冰淇淋的招牌映入三人的眼簾。"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/07/a6V5BY.png', preview_image_url='https://upload.cc/i1/2022/03/07/a6V5BY.png'))
                list_talk.append(TextSendMessage(text="「星期三會有特殊口味，可惜今天是星期一。」曉光打開玻璃門自言自語；雖然一言一語中沒有透露出什麼特殊訊息，但日翔能感覺到曉光的心情似乎很好。"+"\n"+"食科冰的店面乾淨整潔、澄黃色的牆面跟木質的地板櫃檯都十分有溫馨的感覺。聽說食科冰的配方是由以前的學長姊留下的，無論在什麼時候，輔大都可以吃到這種回憶裡的好味道。日翔一直認為，這裡應該是校園內數一數二讓人放鬆的地方。"+"\n"+"曉光兌換完香草口味的冰淇淋後，日翔和司晨也都各購買了一支冰淇淋，三人坐在窗邊的位置上邊吃邊聊天。日翔的心思仍然停在曉光身上，好像都沒有注意到手上綜合冰淇淋的一角已經開始化掉了——不知為何，曉光喜歡香草口味的霜淇淋這事對他而言並不是一件令自己意外的事情？明明以前都沒有和曉光吃過冰淇淋吧。"+"\n"+"「喂——阿日，你的冰都弄到手上啦！！阿日！」"+"\n"+"突然，有熟悉的聲音打斷了進入沉思狀態的日翔，他近乎是顫得跳了起來看了看，原來是早就把冰淇淋吃完了的司晨。"+"\n"+"「你今天怎麼搞的，居然一直在出神，不是讓曉光看笑話了嗎？」司晨趁著還在好友尚在半恍神的狀態中，趁機調侃了一番。"+"\n"+"「嗯？日翔捨不得吃那麼好吃的冰所以開始發呆，應該是很正常的吧。」被點名的曉光咬下酥脆的甜筒輕快地反駁。很明顯的，曉光一吃冰淇淋心情就好了一大截。"+"\n"+"司晨說得沒錯，他竟然就開始自顧自地出神了起來，這無疑是稍微浪費了難得和曉光同行的機會。可曉光說的話也並沒有什麼問題，畢竟食科冰是真的很好吃——唯一錯的地方在於，發呆的原因分明是那個比食科冰更加美好的女孩。"+"\n\n"+"解鎖冰淇淋券！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="某天統計課的下課時間，日翔發現自己犯了很大的錯誤。"+"\n"+"「啊……！！」"+"\n"+"「怎麼啦阿日？」聽到日翔那讓人聯想到世界名畫「吶喊」的慘叫聲，在一旁玩手機遊戲的司晨撇過頭來看他。"+"\n"+"日翔突然開始搖起了司晨的肩膀：「今天統計要小考啊，我沒有帶計算機欸！完蛋了！」"+"\n"+"「……對喔！那要不要現在去敦煌買？」"+"\n"+"「這樣會不會太浪費錢了啊，工程計算機一台不便宜吧……而且我覺得應該也沒有人會多帶一台。」雖然日翔馬上就反駁了自己的好友，但是他仍然掏出了自己的錢包看看有沒有帶足夠的錢買計算機。"+"\n"+"這時，一道格外清澈的女聲打斷了兩人的對話：「……聽說我們系學會可以借計算機。」"+"\n"+"是看見他們吵吵鬧鬧於是忍不住提議的曉光。"+"\n"+"「「欸？真的嗎！？」」宛如重見天日的兩位粗心大意的傻子對曉光投以感激的目光。"))
                list_talk.append(TextSendMessage(text="#30 資管系系學會目前位在哪一個大樓？（請以「ＯＯ樓」回答）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="28":
                worksheet.update(list[1],int(29))
                worksheet.update(list[2],int(4))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「啊——我想起來了，原來又到了社團博覽會的季節，時間過得真快。」司晨撓撓頭，似乎終於回想起來去年剛開學的時候也有社博這回事。"+"\n"+"「你居然忘記了，前一年的社博我們是一起參加的吧？去年明明我們都有意願加入系籃，你現在就給我忘了？」日翔失笑地說著。"+"\n"+"司晨同學真的沒問題嗎？曉光疑惑的看著司晨，同樣的，曉光發現日翔也正疑惑的看著司晨。"+"\n"+"正當曉光正在觀察日翔看著司晨的表情，日翔猛然轉了頭，剛好與曉光四目交接。什麼？現在是什麼情形？ 怎麼那麼剛好日翔轉過頭來。"+"\n"+"「……嗯、怎麼了？」曉光試圖安頓好剛剛混亂的情緒，眼神略帶漂移的問了這句話。"+"\n"+"只見日翔沒有馬上回答曉光的問題，慢了一拍才急急忙忙回應曉光的疑問：「啊沒、沒什麼！只是有點好奇曉光會不會參加社團而已。」"+"\n"+"他剛剛在想事情嗎？原來他也有想事情想到出神的時候，跟我好像。曉光發現到日翔一個有趣的特色，嘴角微微的上揚。"+"\n"+"跟著下課的人流走著走著，食科冰淇淋的招牌映入三人的眼簾。"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/07/a6V5BY.png', preview_image_url='https://upload.cc/i1/2022/03/07/a6V5BY.png'))
                list_talk.append(TextSendMessage(text="「星期三會有特殊口味，可惜今天是星期一。」曉光打開玻璃門自言自語。曉光不僅對書上的一行一句記得相當熟悉，連食科冰淇淋的口味也瞭若指掌，畢竟是自己最喜歡的冰淇淋，曉光當然上食科冰的粉絲專頁好好研究了一番。"+"\n"+"「你很喜歡冰淇淋嗎？」日翔問道。"+"\n"+"面對這突如其來的問題，使得曉光耳根發紅。曉光總覺得自己隱瞞得很好，日翔又是怎麼發現的？曉光不禁欽佩日翔過人的觀察力。"+"\n"+"「非、非常喜歡。」緊張到結結巴巴的曉光顯得更加慌張。"+"\n"+"「哈哈哈，原來曉光也會喜歡冰淇淋嗎？挺可愛的。」日翔說。"+"\n"+"他剛剛是說可愛嗎？曉光低下頭去，試圖利用冰淇淋的沁涼消除內心的熱氣。"+"\n"+"食科冰的店面乾淨整潔、澄黃色的牆面跟木質的地板櫃檯都十分有溫馨的感覺。聽說食科冰的配方是由以前的學長姊留下的，無論在什麼時候，輔大都可以吃到這種回憶裡的好味道。"+"\n"+"曉光兌換完香草口味的冰淇淋後，日翔和司晨也都各購買了一支冰淇淋，三人坐在窗邊的位置上邊吃邊聊天。突然，司晨大叫一聲，讓曉光嚇了一跳。"+"\n"+"「喂——阿日，你的冰都弄到手上啦！！阿日！」只見日翔近乎顫得跳了起來看了看手上融了一半的冰淇淋。今天的日翔是怎麼了？怎麼一副魂不守舍的樣子。"+"\n"+"「沒事吧？日翔。」曉光有股熟悉的感覺，彷彿這句話常常聽到，曉光恍然大悟，之前都是日翔對著曉光說，沒想到這次立場反過來了。"+"\n"+"「你今天怎麼搞的，居然一直在出神，不是讓曉光看笑話了嗎？」司晨趁著還在好友尚在半恍神的狀態中，趁機調侃了一番。"+"\n"+"「嗯？日翔捨不得吃那麼好吃的冰淇淋，所以開始發呆，應該是很正常的吧。」被點名的曉光咬下酥脆的甜筒輕快地反駁。"+"\n"+"這麼好吃的冰淇淋，任誰都沒辦法抵擋它的美好，曉光深信不疑。"+"\n"+"「如果能在曆法上新增一個冰淇淋的節日那該有多好。」要是真的有冰淇淋的節日，曉光真想吃遍所有品牌的冰淇淋。"+"\n\n"+"解鎖冰淇淋券！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="某天統計課的下課時間，曉光一如往常的看著書。"+"\n"+"「……大二都過了快一半了。」曉光無奈的自言自語道。自從大二開學聽到那道光的聲音後，就再也沒聽到了，這讓曉光相當焦慮。"+"\n"+"「那道光一直強調的：好好表現，一定別有居心，是不是還沒達成阿？」對曉光來說，這次重來的大學生活已經讓從來不說話、不社交的曉光，踏出嶄新的一步了，不禁開始懷疑起是不是什麼地方出了錯。"+"\n"+"突然，一陣喧囂打斷曉光的思考。"+"\n"+"「今天統計要小考啊，我沒有帶計算機欸！完蛋了！」"+"\n"+"「……對喔！那要不要現在去敦煌買？」"+"\n"+"「這樣會不會太浪費錢了啊，工程計算機一台不便宜吧……而且我覺得應該也沒有人會多帶一台。」"+"\n"+"嗯……又是那日翔跟司晨兩人組合啊，忘了帶計算機的確是很緊張的事情，但也用不著讓全班都知道吧，曉光苦笑。上次吃鬆餅的時候，也是他們請我的，這次換我幫助他們吧。曉光站了起來，走向他們。"+"\n"+"「……聽說我們系學會可以借計算機。」曉光平淡的口吻與剛剛大吵大鬧的兩人形成強烈對比。"+"\n"+"「「欸？真的嗎！？」」宛如重見天日的兩位粗心大意的傻子對曉光投以感激的目光，曉光只好用手指比了比外面表示趕快去借吧。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="29":
                worksheet.update(list[1],int(30))
                list_talk=[]
                list_talk.append(TextSendMessage(text="又過了幾個禮拜，終於，考試又要鄰近了——打算抱佛腳的日翔心想，根據他的經驗，在家看書他一點也不會認真，總是讀了一兩行又跑去滑滑手機敲敲鍵盤、整理書櫃打掃房間、甚至出奇地自告奮勇跑去幫媽媽跑腿。畢竟再怎麼擁有上一次大學生活的經歷，有些東西就是考完就會順便忘記的。於是他決定在學校圖書館讀書。而他心想，現在跟曉光也逐漸熟識了起來，如果有機會也可以向他問問題。"))
                list_talk.append(TextSendMessage(text="#31 請問本校擁有最多層樓的圖書館是哪一個？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="29":
                worksheet.update(list[1],int(30))
                list_talk=[]
                list_talk.append(TextSendMessage(text="又過了幾個禮拜，終於，考試又要鄰近了——曉光總是不急不徐的安排好讀書計畫，以及吃飯與休息時間，仿佛一天的每一分每一秒都掌握在她的手上。而對於喜歡安靜場所的曉光而言，圖書館是再適合不過的地方，也因此，曉光把輔大的所有圖書館的開館與閉館記得一清二楚。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="30":
                worksheet.update(list[1],int(31))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="30":
                worksheet.update(list[1],int(31))
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="31":
                worksheet.update(list[1],int(32))
                worksheet.update(list[2],int(6))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖濟時樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="日翔這幾天讀得急急忙忙，但靠著過去大學生活的記憶，總算把所有的課程內容讀完了，甚至還比以前要讀得更好——甚至還可以跟曉光討論一些比較艱難的題目，或者是拯救必修快要掛掉的司晨。他們三人後來還借濟時樓的討論室，在課後一起惡補。而且，其中的幾天還遇上同樣跑來濟時樓讀書的宇桓！沒想到，那個學霸也在這裡讀書啊，這是以前日翔都不知道的。"+"\n"+"現在，是該要驗收讀書的成果了。"))
                list_talk.append(TextSendMessage(text="#33 班上 1-10 號的同學身高分別為 178、160、155、182、169、160、164、158、175、160，請分別輸入這十位同學的算術平均數、中位數與眾數。（請以「Ｏ、Ｏ、Ｏ」回答，若Ｏ有小數點為四捨五入至第一位半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="31":
                worksheet.update(list[1],int(32))
                worksheet.update(list[2],int(6))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖濟時樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="期中考逼近，曉光平時都保持著課前預習、課後複習的好習慣，加上課堂教的又是曉光已經掌握的知識，因此曉光早早就準備好令大家頭疼的期中考試了。不過，跟以往獨自念書不同，這次日翔和司晨也會來詢問自己一些不明白的問題，為此三人還專門去濟時樓借了討論室開讀書會。甚至遇上了同來濟時樓念書的馬宇桓，雖說他為人高傲，不過也是很努力在讀書上呢。"+"\n"+"現在，是該要驗收讀書的成果了。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="32":
                worksheet.update(list[1],int(33))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#34 有一資料庫用來記錄學生分數如下圖，下列有一塗黑語法，該填上什麼可以由小到大輸出A班學生姓名與成績？"+"\n"+"◼ name,score ◼ database_score ◼ class_id=1 ◼ score ◼"+"\n"+"（Ａ）SELECT/FROM/WHERE/ORDER BY/ASC"+"\n"+"（Ｂ）SELECT/FROM/WHERE/GROUP BY/DESC"+"\n"+"（Ｃ）SELECT/FROM/WHEN/ORDER BY/DESC"+"\n"+"（Ｄ）SELECT/FROM/WHEN/GROUP BY/ASC"))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="32":
                worksheet.update(list[1],int(33))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#34 有一資料庫用來記錄學生分數如下圖，下列有一塗黑語法，該填上什麼可以由小到大輸出A班學生姓名與成績？"+"\n"+"◼ name,score ◼ database_score ◼ class_id=1 ◼ score ◼"+"\n"+"（Ａ）SELECT/FROM/WHERE/ORDER BY/ASC"+"\n"+"（Ｂ）SELECT/FROM/WHERE/GROUP BY/DESC"+"\n"+"（Ｃ）SELECT/FROM/WHEN/ORDER BY/DESC"+"\n"+"（Ｄ）SELECT/FROM/WHEN/GROUP BY/ASC"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="33":
                worksheet.update(list[1],int(34))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#35 又該如何輸出全班總分及平均並重新命名表格欄位？（請以半形英文大寫「ＯＯＯ/ＯＯ/ＯＯＯ/ＯＯ」回答。）"+"\n"+"SELECT ◼(score) ◼ 總分, ◼(score) ◼ 平均 FROM database_score"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fxIoAx@.png', preview_image_url='https://ppt.cc/fxIoAx@.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="33":
                worksheet.update(list[1],int(34))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="34":
                worksheet.update(list[1],int(35))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="34":
                worksheet.update(list[1],int(35))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="35":
                worksheet.update(list[1],int(36))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="35":
                worksheet.update(list[1],int(36))
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
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="36":
                worksheet.update(list[1],int(37))
                worksheet.update(list[2],int(6))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="36":
                worksheet.update(list[1],int(37))
                worksheet.update(list[2],int(6))
                list_talk=[]
                list_talk.append(TextSendMessage(text="總算是到了大二的學期中末，班代已經在班群開始提醒各組要尋找好專題組員了。"+"\n"+"「要找誰呢……」雖然曉光認為她一個人就可以做好整個專題——這應該是曉光不太想主動找組員的推託之詞；不過，在她還沒回到過去之前其實就是一個人攬下了整個大三專題的工作。而這其實是看在曉光過人的才能而特地給的優待，否則一般來說，專題的規則上是不能一個人一組的。"+"\n"+"「難道這就是轉捩點嗎？」曉光沉思。"+"\n"+"「不過……」曉光眨了眨眼回想過去獨自完成專題的經歷，雖說事情都獨自包攬下來的效率很高，但仍是有些疲勞，而且她都下定決心要邁出步伐前進了！"+"\n"+"「這次要找他們當組員嗎？」曉光有些猶豫，要是他們已經找好組員不就尷尬了嗎。"+"\n"+"這時曉光發現日翔和司晨就站在教室外面，兩個人嘀嘀咕咕的不知道討論什麼，隱隱約約還聽見自己的名字。"+"\n"+"曉光決定主動上前攀談，「……日翔？你們在討論什——」。"+"\n"+"「曉光！你現在專題已經有組了嗎？」日翔詢問。嗯？我剛好也是來問這個問題。"+"\n"+"「哎、哎、還沒有……」"+"\n"+"「那……要不要和我們一組？」日翔伸出大拇指，將大拇指指向自己和司晨，向曉光示意目前有兩個組員。"+"\n"+"「好啊。」 很快就找到組員的曉光，總覺得卸下一個重擔，內心十分慶幸有認識日翔和司晨這兩個人。"))
                list_talk.append(TextSendMessage(text="曉光回到座位上，正準備預習等一下上課的內容。此時，眼角餘光稍微撇到原本只有日翔和司晨的兩人，旁邊多了一個宇桓。"+"\n"+"只見宇桓和日翔他們正在溝通中，曉光心想要不要再次去加入他們的話題。隔了沒多久，曉光聽到自己的手機發出輕快的提醒聲音，下意識地打開手機一看。"+"\n"+"「好像不需要了。」曉光看到專題的群組裡多了一個人，不用說也知道，宇桓也加入了他們的專題小組。宇桓雖態度高傲了一點，但平時做事很認真，對成績也很要求，曉光記得他在機測五題全過，一定可以成為專題的一大助力。"+"\n"+"「曉光～你專題找到人了嗎？」真澄把臉湊過來詢問曉光，真澄突然的行為讓曉光嚇了一跳。"+"\n"+"「目前有我、日翔、司晨和宇桓同學喔。」曉光一字一句回答道。"+"\n"+"「嘿～～？這麼多人啊，曉光很受歡迎喔。」真澄笑瞇瞇的說著，曉光總覺得她應該不是特別來稱讚她才和她說話。"+"\n"+"「那這樣的話你們不是就少一個人？那加上我就剛好五個人啦，就這麼說定了。」真澄也不管曉光是不是答應與否，就擅自把自己算入他們的一份子。"+"\n"+"「唔……還是得問看看其他人才行。」正當曉光想要打開群組詢問其他組員的意見時，發現真澄在旁邊竊笑著。"+"\n"+"曉光不解真澄臉上的笑意，直到她仔細一看上面的組員欄位。欸？！什麼時候多了一個人。"+"\n"+"「我早就跟日翔同學說好啦，只是想看看你的反應。」真澄比出一個勝利V手勢，「有我這個強力助手進來，一定能派上用場的！」"+"\n"+"就這樣專題組員在短時間內迅速的湊齊了。"))
                list_talk.append(TextSendMessage(text="過了幾周，眾人在團體討論室專題主題。由於專題或多或少牽涉到畢業、或者職涯發展的話題，司晨便突然開口：「哎，已經要到申請雙主修的時間了。我在想要不要申請雙主修。」"+"\n"+"「真的假的，阿司，你居然想要雙主修！」日翔嘴巴張得大大的。"+"\n"+"沒問題嗎？雙主修的門檻很高的。曉光雖然沒有參與話題，卻在心中留下了這個問題。"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="37":
                worksheet.update(list[1],int(38))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「我突然想要雙修體育系啊！」司晨看到日翔那麼驚訝也顯得有些意外。"+"\n"+"「一般日間部不能用雙主修的方式申請體育系，而且雙主修這件事應該要好好提早規劃的。」看到日常犯傻的司晨，曉光忍不住吐槽。"+"\n"+"「哎、是這樣啊，那算啦。」"+"\n"+"「……」宇桓選擇沉默，他傻眼地把落到鼻樑下方的眼鏡往上推，似乎想喝一口遺忘汁把這段白癡的對話忘掉——他原先是心想日翔跟曉光這兩人肯定是專題的有力隊友，絕對能襯得上自己才加入他們的，至於司晨……宇桓對他的評價是，原來這世界上真的有那麼蠢的人，大開眼界。"))
                list_talk.append(TextSendMessage(text="專題五人組在六月的某天為了要討論專題的主題，順便讀期末考而決定約在學校附近的餐廳見面——更重要的是家財萬貫的宇桓決定請所有人吃一頓！"+"\n"+"宇桓的預算近乎是個無底洞，無論司晨在群組提出多麼離譜的建議——無論是學餐還是吃到飽，大家的金主同學幾乎都是回應：「你們選，我都行」；不過，基於虧欠心理，大家自然不會想佔盡宇桓的便宜，最後一行人還是決定在一個大家都沒課的下午去吃輔大附近的貓中途餐廳「吃。貓」。"+"\n"+"只不過計劃趕不上變化，五個人都有空的時間也就那麼一個下午，卻偏偏在當天午後來了場突襲式的傾盆大雨。已經到站的日翔、曉光跟司晨在捷運輔大站的入口屋簷下看著LINE群的訊息，得知了宇桓跟真澄因為選修課延後所以會晚到的消息。"))
                list_talk.append(TextSendMessage(text="「欸欸欸你們知道嗎，聽說學校淹水了餒！！」司晨把限動展示給日翔跟曉光看，一臉就是對學校淹水的狀況備感興趣的樣子。"+"\n"+"「阿司，你要去參觀就自己去，『這次』我不想陪你啦。」日翔想到過去的自己選擇陪著司晨去看那個傳說中的湖，最後那個傻子居然拉著自己在學校裡泛舟……那次經驗實在是瘋狂到在日翔畢業後偶爾還會夢到，很是驚悚。不過雖然日翔這麼說，但這「我不陪你」的話也僅僅是開個玩笑而已，畢竟等等就要去吃貓餐廳，再傻也不會有人真的跑進學校吧……"))
                list_talk.append(TextSendMessage(text="#39 輔大水樂園開張！傳說每當暴雨強襲，校園內就會出現一面湖，曾有學長帶著橡皮艇「到此一划」，請問應該到哪裡朝聖奇景？（請以「ＯＯＯ」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="37":
                worksheet.update(list[1],int(38))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「我突然想要雙修體育系啊！」司晨看到日翔那麼驚訝也顯得有些意外。"+"\n"+"唔……看來是該有人點醒他呢。曉光環顧四周。宇桓根本沒有在理他們的對談，專心的看著電腦。真澄則是正在看著有關寶石的雜誌。"+"\n"+"「一般日間部不能用雙主修的方式申請體育系，而且雙主修這件事應該要好好提早規劃的。」看來只有自己了，曉光開口提醒。"+"\n"+"「哎、是這樣啊，那算啦。」"+"\n"+"「……」宇桓選擇沉默，他傻眼地把落到鼻樑下方的眼鏡往上推，似乎想喝一口遺忘汁把這段白癡的對話忘掉——"+"\n"+"真澄似乎對雙主修沒有任何想法，也是，真澄總是把課修的很滿，也無暇顧慮雙主修，因此真澄從頭到尾沒有任何應答。"+"\n"+"這樣真的沒問題嗎？曉光對這個氣氛不知道該如何是好。"))
                list_talk.append(TextSendMessage(text="專題五人組在六月的某天為了要討論專題的主題，順便讀期末考而決定約在學校附近的餐廳見面——更重要的是家財萬貫的宇桓決定請所有人吃一頓！"+"\n"+"宇桓的預算近乎是個無底洞，無論司晨在群組提出多麼離譜的建議——無論是學餐還是吃到飽，大家的金主同學幾乎都是回應：「你們選，我都行」；不過，基於虧欠心理，大家自然不會想佔盡宇桓的便宜，最後一行人還是決定在一個大家都沒課的下午去吃輔大附近的貓中途餐廳「吃。貓」。"+"\n"+"只不過計劃趕不上變化，五個人都有空的時間也就那麼一個下午，卻偏偏在當天午後來了場突襲式的傾盆大雨。已經到站的日翔、曉光跟司晨在捷運輔大站的入口屋簷下看著LINE群的訊息，得知了宇桓跟真澄因為選修課延後所以會晚到的消息。"))
                list_talk.append(TextSendMessage(text="「欸欸欸你們知道嗎，聽說學校淹水了餒！！」司晨把限動展示給日翔跟曉光看，一臉就是對學校淹水的狀況備感興趣的樣子。就算大學生活反覆重來，輔大會淹水這件事依舊沒變。對淹水早已司晨空見慣的曉光，覺得沒什麼稀奇的。"+"\n"+"「阿司，你要去參觀就自己去，『這次』我不想陪你啦。」聞言，日翔與司晨的興奮不同，倒是冷靜地向自己的好友推辭。"+"\n"+"……「這次」？ 曉光聽到了關鍵字，眉頭便以微不可見的程度蹙了起來。他們是常常一起跑去玩水嗎？等等，不對。曉光陷入了沉思之中——在「上一次」的記憶之中，這兩個人曾經因為在輔大泛舟而被記者採訪過。"+"\n"+"「你真的不跟好兄弟一起去嗎？比起我……你居然更重視妹子，嗚嗚嗚，真是太過分了……」邀約失敗的司晨乾脆開始假哭。"+"\n"+"「喂，你啊……我們不是還在群組約好要一起讀書嗎？大雨把你沖失憶啦？」日翔似乎看出了司晨的意圖，便輕輕敲了一下他的頭，難得認真地向他講道理。"+"\n"+"比起貓餐廳，司晨似乎還是對雨水氾濫的輔大更有興趣，因此便丟下一句話就一溜菸地跑了：「嘿嘿、沒有啦我還記得。總之我看看就回來嗷！晚點再去找你們吃下午茶！」"+"\n"+"默默在一旁聽完兩人的對話的曉光總感覺日翔提到的「這次」這個關鍵字有些蹊蹺，有「這次」就代表在某時某刻存在過一個「上次」。然而在她的記憶之中，去年輔大並沒有淹水。那麼這樣令人感到有些違和的詞語又是怎麼來的？"+"\n"+"還是只是我想太多了，真的只是單純兩人常常一起去玩水？還是不要對這種事這麼敏感好了。曉光心想。"))
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
            list.append('E'+str(j))
            list.append('B'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="38":
                worksheet.update(list[1],int(39))
                worksheet.update(list[2],int(7))
                worksheet.update(list[3],int(7))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖中美堂！趕快去「遊戲地圖」看看！"+"\n\n"+"中美堂是一座大型的圓形建築，類似羅馬競技場。通常是重大集會跟室內體育競賽的選擇地，新生們的開學典禮一般會選擇在這裡舉辦所謂的「叩門禮」。只不過如果遇上了大雨……就會變成傳說中輔大水樂園的鎮園之寶「中美湖」……"+"\n"+"「好啊那我看看就回來！晚點再去找你們吃下午茶！」"+"\n"+"「喂、阿司，我只是開玩笑的！阿司！！」日翔開口大喊，司晨的身影卻早已消失在重重雨簾之中。"+"\n"+"「哇……司晨連傘也不帶就往學校去了。」曉光竟然也忍不住感嘆。"+"\n"+"雖然對他的莽撞感到無言，但日翔對司晨的決定確實是有些感謝之情，因為這樣一來他便得到了第一次名正言順和曉光獨處的機會——即使很可能只有一下下。雖然不知道司晨是不是在幫自己製造機會，但日翔決定以這樣的角度默默感謝他。"+"\n"+"日翔的心情和此時的暴雨呈反比的高興了起來：「曉光，我們先去『吃。貓』等他們吧。」"+"\n"+"「吃。貓」是在北部貓餐廳之中較為著名的一間，據說裡面的人類店長跟貓咪店長都很好，同時也是貓咪的中途之家，許多喜歡貓咪的輔大人都會前去一探究竟。"+"\n"+"日翔和曉光已經提早和人類店長支會總共有五個人要前來用餐，於是他們倆便坐到事先安排好的五人空位桌，由於宇桓和真澄剛剛傳訊息過來表示他們已經下課了，待會就到，於是日翔跟曉光打算等隊友們都差不多到齊了再點餐，至於司晨……他能平安就好。"+"\n"+"畢竟傾盆大雨實在是如倒瀉般止不住，於是到達吃貓的兩人其實也是有些狼狽的——就算是一人撐一把傘，也難以避免身上稍微被淋濕的命運。而因為雨水的緣故，日翔揹筆電跟課本用的背包和手腿無依倖免。嗯……都這樣了還吹著冷氣實在有點討厭啊，曉光她還好嗎？他留意了一下身旁曉光的狀況，她似乎也因為自己的東西淋濕了而懊惱著。"+"\n"+"日翔突然想到，他應該有放一條毛巾在書包裡——起初只是因為對這個「暴雨的今天」有所預防，說白了就是為了要避免司晨真的拉自己去泛舟才帶著的……現在居然可以派上用場，老實說日翔也十分意外。"+"\n"+"他把潔白的毛巾拿出來瞧了瞧。嗯，幸好雨水並沒有波及到它。"+"\n"+"「曉光，這個給妳，如果感冒了就糟糕了。」日翔把自己帶著的乾淨毛巾遞給曉光。"+"\n"+"「欸？啊……謝謝你，我還懊惱要怎麼辦呢。」曉光在接過毛巾之後還細心地確認了一下毛巾的狀況，便用來擦拭濕得很是不舒服的腿腳。"+"\n"+"「不客氣。」他笑著回應完曉光。隨後，日翔的餘光瞄到了她肩膀上的……灰色動物毛？考慮到曉光手機殼印著一隻灰色胖貓，他便好奇地詢問：「曉光，你家裡有養貓嗎？」"+"\n"+"「對，是一隻叫做『德魯貝』的米克斯，小學的時候領養的。」曉光似乎有些驚訝日翔猜中了家裡有養貓，難得地將平淡以外的神情表露在外：「沒想到日翔你可以辨認得出來這是貓毛。」"+"\n"+"「沒有啦，只是我瞎猜的。因為這讓我想到我在小時候也有養過一陣子的貓咪，只要家裡有養動物，毛總是會滿天飛……而且我們也還沒跟這裡的貓咪互動吧。」日翔對於自己的直覺也感到有些驚喜，而他現在才想到，好像也有可能是養灰色的其他動物。"+"\n"+"「這樣呀……我的貓咪以前也是流落街頭，當時是在一間中途之家收養牠的。」一提到自家的貓咪，一邊擦拭書包的她心情就好了起來。"+"\n"+"「啊、如果你會冷的話這個也可以給你，我是不怕冷的那種……雖然只是短袖襯衫，希望可以讓妳好一點。」日翔見到她的臉色似乎還是有些不好，便決定脫下了自己的外套給曉光。"+"\n"+"曉光似乎顯得有些驚喜，也接下了日翔的外套：「不用這麼費心啦……但還是謝謝你。」"))
                list_talk.append(TextSendMessage(text="「哎唷——聊得很開心嘛。」一個聲音打破了兩人的對話。曉光抬頭一看，是自己的好友真澄，她一邊調侃一邊順勢坐到了曉光的對面。"+"\n"+"「你們可以先吃啊，難道是怕我不來付帳嗎？」跟在後頭的宇桓語氣仍然尖銳，但在場的所有人都並不是很在意，畢竟他是金主爸爸，他說得都對。"+"\n"+"眾人你一言我一語地開始聊了起來，並且開始點起了餐。日翔點了一份「隨便」跟一杯「隨便」順便幫目前不在場的司晨點了一份「吃不完的脆薯」、曉光點了一盤雞米花跟一杯葡萄汁、真澄點了「綜合梅優格」、金主宇桓意思意思地點了杯馬來西亞白咖啡，在滿滿都是貓的氛圍裡過了好是愜意的下午。"+"\n"+"至於當初說好討論的期末考跟專題……在貓餐廳怎麼可能討論得起來啊。"+"\n\n"+"解鎖糖果紙！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="期末考在即，大二的時光也即將過去了。不知不覺第二次的大學生活也過了快要一半——日翔想起了那個希望自己好好努力的聲音，他確實感受到，這一次的大學生活因為他的積極而有諸多改變。不知道那位讓自己回到過去的「高位生命體」，是否也在某個地方注視著他呢……"))
                list_talk.append(TextSendMessage(text='#40 在html語法中，要如何輸出此空格效果？（請以半形小寫「<input type="Ｏ">」回答，Ｏ數不代表答案正確字數。）'))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fX1Pix@.png', preview_image_url='https://ppt.cc/fX1Pix@.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="38":
                worksheet.update(list[1],int(39))
                worksheet.update(list[2],int(7))
                worksheet.update(list[3],int(7))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖中美堂！趕快去「遊戲地圖」看看！"+"\n\n"+"中美堂是一座大型的圓形建築，類似羅馬競技場。通常是重大集會跟室內體育競賽的選擇地，新生們的開學典禮一般會選擇在這裡舉辦所謂的「叩門禮」。只不過如果遇上了大雨……就會變成傳說中輔大水樂園的鎮園之寶「中美湖」……"+"\n"+"「好啊那我看看就回來！晚點再去找你們吃下午茶！」"+"\n"+"「喂、阿司，我只是開玩笑的！阿司！！」日翔開口大喊，司晨的身影卻早已消失在重重雨簾之中。"+"\n"+"「哇……司晨連傘也不帶就往學校去了。」曉光竟然也忍不住感嘆。"+"\n"+"這兩個人忘東忘西這點還真像呢，這就是物以類聚嗎？曉光想起當初見到日翔的時候，日翔也沒有帶課表就衝出家門。"+"\n"+"「曉光，我們先去『吃。貓』等他們吧。」 日翔的語氣略帶興奮地說道。"+"\n"+"「吃。貓」是在北部貓餐廳之中較為著名的一間，據說裡面的人類店長跟貓咪店長都很好，同時也是貓咪的中途之家，許多喜歡貓咪的輔大人都會前去一探究竟。"+"\n"+"日翔和曉光已經提早和人類店長支會總共有五個人要前來用餐，於是他們倆便坐到事先安排好的五人空位桌，由於宇桓和真澄剛剛傳訊息過來表示他們已經下課了，待會就到，於是日翔跟曉光打算等隊友們都差不多到齊了再點餐，至於司晨……他能平安就好。"+"\n"+"「吃。貓」的貓咪們讓曉光想起了家裡那隻嬌生慣養的天皇貓咪——德魯貝，店內專門給貓咪們設置的小物品讓曉光想起自己似乎有些時間沒有幫德魯貝添購新玩具了，曉光拿出手機，看看有關寵物的商品。不過要買什麼好呢，牠這麼挑，買了新玩具只顧著玩附贈的紙箱，不是某牌的貓罐頭連動都不動。"+"\n"+"還是來看看有沒有衣服吧。曉光最喜歡有關貓咪的服飾，今天的她穿著粉色的日系上衣，下半身是小巧可愛的皺摺裙，搭配耐穿好看的帆布鞋，頭上還戴著貓咪造型的髮夾，這對曉光可說是基本標配。"+"\n"+"當曉光將視線全集中在自己的手機螢幕上時，曉光突然感到一陣寒意。"+"\n"+"「好冷，沒有想到今天會下雨。」曉光邊發抖、邊懊惱的說著。"+"\n"+"是不是該先點一些熱飲來喝呢？可是人都還沒來耶……曉光在心中盤算，但瞬間又打消了念頭。"+"\n"+"突然，在旁邊的日翔拿出一個潔白的毛巾，遞給曉光。"+"\n"+"「曉光，這個給妳，如果感冒了就糟糕了。」日翔把自己帶著的乾淨毛巾遞給曉光。"+"\n"+"「欸？啊……謝謝你，我還懊惱要怎麼辦呢。」曉光在接過毛巾之後還細心地確認了一下毛巾的狀況，便用來擦拭濕得很是不舒服的腿腳。"+"\n"+"「不客氣。」日翔笑著回應曉光。"+"\n"+"由於日翔暖心的舉動，將曉光身上的寒意一掃而空。曉光內心十分感謝日翔，也欣賞他這個舉動，甚至感受到心臟跳的比平常快。"+"\n"+"奇怪，我是怎麼了。從來沒談過戀愛的曉光，不曉得自己是怎麼了，但是她看著日翔的笑臉，彷彿一顆耀眼的寶石般，吸引著她的目光。"+"\n"+"「曉光，你家裡有養貓嗎？」 這個問題讓曉光的焦點再度回到現實，曉光慢了一拍才回答。"+"\n"+"「對，是一隻叫做『德魯貝』的米克斯，小學的時候領養的。」"+"\n"+"他是怎麼知道我家裡有養貓？曉光提出這個疑惑，並在腦海尋找答案。而當曉光的目光移動到自己身上時，才發現到身上的貓毛忘記清除。"+"\n"+"「沒想到日翔你可以辨認得出來這是貓毛。」曉光找到了解答，大概是日翔發現自己身上的貓毛才這麼提問的。"+"\n"+"「沒有啦，只是我瞎猜的。因為這讓我想到我在小時候也有養過一陣子的貓咪，只要家裡有養動物，毛總是會滿天飛……而且我們也還沒跟這裡的貓咪互動吧。」只見日翔揮著手表示否定。"+"\n"+"「這樣呀……我的貓咪以前也是流落街頭，當時是在一間中途之家收養牠的。」一提到自家的貓咪，一邊擦拭書包的曉光心情就好了起來。"+"\n"+"「啊、如果你會冷的話這個也可以給你，我是不怕冷的那種……雖然只是短袖襯衫，希望可以讓妳好一點。」日翔說完這句話時，已經脫下了自己的外套，伸出手來遞給曉光。"+"\n"+"「不用這麼費心啦……但還是謝謝你。」曉光似乎顯得有些驚喜，也接下了日翔的外套。"+"\n"+"真是個好人，日翔貼心的舉動讓曉光內心暖暖的。"))
                list_talk.append(TextSendMessage(text="「哎唷——聊得很開心嘛。」一個聲音打破了兩人的對話。曉光抬頭一看，是自己的好友真澄，她一邊調侃一邊順勢坐到了曉光的對面。"+"\n"+"「你們可以先吃啊，難道是怕我不來付帳嗎？」跟在後頭的宇桓語氣仍然尖銳，但在場的所有人都並不是很在意，畢竟他是金主爸爸，他說得都對。"+"\n"+"眾人你一言我一語地開始聊了起來，並且開始點起了餐。日翔點了一份「隨便」跟一杯「隨便」順便幫目前不在場的司晨點了一份「吃不完的脆薯」、曉光點了一盤雞米花跟一杯葡萄汁、真澄點了「綜合梅優格」、金主宇桓意思意思地點了杯馬來西亞白咖啡，在滿滿都是貓的氛圍裡過了好是愜意的下午。"+"\n"+"至於當初說好討論的期末考跟專題……在貓餐廳怎麼可能討論得起來啊。"+"\n\n"+"解鎖糖果紙！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="期末考在即，大二的時光也即將過去了。不知不覺第二次的大學生活也過了快要一半——曉光想起了那個希望自己好好努力的聲音，她確實感受到，這一次的大學生活因為他的積極而有諸多改變。不知道那位讓自己回到過去的「那道光」，是否也在某個地方注視著她呢……"))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="39":
                worksheet.update(list[1],int(40))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="39":
                worksheet.update(list[1],int(40))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="40":
                worksheet.update(list[1],int(41))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="40":
                worksheet.update(list[1],int(41))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="41":
                worksheet.update(list[1],int(42))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="41":
                worksheet.update(list[1],int(42))
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="42":
                worksheet.update(list[1],int(43))
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
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="42":
                worksheet.update(list[1],int(43))
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
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="43":
                worksheet.update(list[1],int(44))
                worksheet.update(list[2],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖紀念幣！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="解鎖大三劇情"))
                list_talk.append(TextSendMessage(text="人類的記憶總是在不斷累積，也會在不知不覺間遺忘對大腦而言不重要的事物。"+"\n"+"開學的前一天夜裡，日翔躺在床上努力回憶著過去的種種。他發現：幼時的記憶他似乎也記不得多少了。至於為何要開始回憶過去，是因為他愈發感覺自己似乎遺忘了某個重要的事情。每次和曉光相處的時候，他總能在腦海之中勾勒出幼時見到過的物件，而日翔幼時的玩伴和曉光的身影好像可以重疊在一起——無論是喜歡看書、點了葡萄汁、還是著迷於霜淇淋等等。"+"\n"+"日翔能夠記得的幼時記憶不多，但他還是能隱隱約約感受到，她倆似乎相似過了頭。可是最關鍵的那位小女孩的名字，他卻忘得一乾二淨。"))
                carousel_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                title='選項',
                                text='偏偏忘了這麼重要的事……',
                                actions=[
                                    MessageAction(
                                        label='選擇',
                                        text='偏偏忘了這麼重要的事……'
                                    )
                                ]
                            ),
                            CarouselColumn(
                                title='選項',
                                text='頭好痛……',
                                actions=[
                                    MessageAction(
                                        label='選擇',
                                        text='頭好痛……'
                                    )
                                ]
                            )
                        ]
                    )
                )
                list_talk.append(carousel_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="43":
                worksheet.update(list[1],int(44))
                worksheet.update(list[2],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖紀念幣！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="解鎖大三劇情"))
                list_talk.append(TextSendMessage(text="夜深人靜，曉光複習完今日上課的內容，洗了澡，開始整理房間。沒想到整理到書櫃時，突然從最上層掉下一個有點舊的盒子，從上面佈滿灰塵的狀況看來似乎被遺忘很久了，曉光對此盒子並沒有印象，它的出現讓曉光十分疑惑。"+"\n"+"「奇怪，這些東西是什麼？」 曉光開啟盒子端詳起裡面的物品，有信封、圖畫、還有……戰鬥紙牌？看著這些毫無關聯的物品，曉光並沒有想出個所以然。「應該不會有人特地把東西寄放在我這裡吧？」"+"\n"+"「……總覺得忘了什麼。」雖然跟日翔相處的時候，看到一些事物，隱隱約約會有股「被電到的感覺」，為什麼是日翔呢？可是其他人就沒有相似的感覺，難道這些東西和日翔有關？曉光不敢妄下斷論，但是也不想否定這個問題。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='是什麼呢……想不起來。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text="是什麼呢……想不起來。"
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
    elif event.message.text=="偏偏忘了這麼重要的事……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="44":
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
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="44":
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
    elif event.message.text=="是什麼呢……想不起來。":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="44":
                list_talk=[]
                list_talk.append(TextSendMessage(text="「謎題又增加了。」曉光放棄思考，決定停止手邊的事情，準備上床睡覺。"+"\n"+"「我該問日翔嗎？」 曉光詢問自己，但是瞬間又打消了念頭，「總不能拿這些東西問他：『日翔你記得這些東西嗎？』」"+"\n"+"「又不是在訊問犯人，感覺好奇怪。」曉光將自己蜷縮在棉被中。"+"\n"+" 還是睡覺吧，曉光清光腦中正在運作的這些想法，按下腦中的關機鍵，進入夢鄉。"))
                list_talk.append(TextSendMessage(text="大學三年級才剛開始，就可以看到班上少了很多人，沒有硬性規定學生一定要上學的大學生活就是這麼優閒自在，有些人甚至一整個學期只會考試當周看到，對曉光而言已經是見怪不怪的日常了。"+"\n"+"也因為升上三年級，課不像一二年級還來的多，因此曉光比以往多出了許多空閒時間。"+"\n"+"這點，她的朋友真澄也一樣。"+"\n"+"「曉光！要不要趁著空堂出去玩啊。」曉光看著手機的簡訊，來信者是真澄。"+"\n"+"「好啊，要去哪裡呢？」曉光飛快的按著手機的按鍵回覆真澄。"+"\n"+"「根據我近期算塔羅的結果，禮拜三去博物館會有好事發生。」可能沒在上課吧，真澄回覆的速度也很快。"+"\n"+"塔羅也可以算這個嗎……？曉光疑惑，不過怕牴觸了她的專業，曉光並沒有將疑問送出。"+"\n"+"「禮拜三我有空。」"+"\n"+"「那就說定了喔，禮拜三早上十點在博物館的門口見，遲到的人要吞一一一一千千千根針喔。」這則訊息除了文字以外，還附加很多星星。"+"\n"+"不是說謊的人才要吞一千根針嗎？對真澄來說大概講錯也無所謂吧。"+"\n"+"到了禮拜三，兩人依照約定準時赴約。"+"\n"+"「曉光光，你好準時到。」看起來非常興奮的真澄說。"+"\n"+"「你也是。」無意間接受特別綽號的曉光，依舊平淡的回答。"+"\n"+"「那我們趕快進去吧。」真澄拉著曉光的手，催促著曉光進去。"+"\n"+"真是的。曉光雖然無奈，但她不討厭真澄這個樣子。"))
                list_talk.append(TextSendMessage(text="一進到博物館，各國稀奇古怪的珍寶盡收在眼底，有來自中國古代的兵馬俑，有埃及的木乃伊，有冰原時期的長毛象標本，還有真澄最喜歡的寶石。"+"\n"+"隨著導覽員的介紹，彷彿自己已經周遊列國般，遊覽各地風景名勝。"+"\n"+"「哇哇哇，這裡真的好棒喔。」不斷發出驚呼聲的真澄，似乎非常喜歡博物館。"+"\n"+"「小聲一點，還在導覽呢。」曉光把手指放在自己嘴巴正中間，告示著真澄要把音量放小。"+"\n"+"「唔，對不起嘛，我太開心了。」真澄也將手放在自己的嘴唇上，把手從左邊移動到右邊，像是把嘴巴拉上拉鍊一樣。"+"\n"+"不過，能看到真澄這麼開心的樣子，還是頭一次呢。曉光當初認為真澄是一個難以親近的人，但是隨著認識的時間越久，才發現真澄只是不知如何開口向他人表達自己的感受，曉光在真澄身上看到自己的影子。"+"\n"+"結束了早上的導覽，曉光和真澄決定在博物館裡面附設的餐廳享用她們的午餐。"+"\n"+"「這盤義大利麵也太好吃了吧。」真澄一手摸著自己的臉，另一手手上的叉子還捲著麵條，感覺非常陶醉的樣子。"+"\n"+"「我的披薩也很好吃，要不要吃吃看。」曉光把手上的披薩遞給真澄。"+"\n"+"「喔喔喔，披薩也很好吃，口感跟學校附近的那間披薩店差不多。」真澄附和曉光的說法。"+"\n"+"「學校附近有披薩店？」曉光不管再怎麼努力思考學校周遭的店家也想不起來。"+"\n"+"「啊，有一段距離啦，因為我以前課比較多，來不及去學校外面買，所以我都叫外送。」"+"\n"+"「原來如此。」從來沒訂過外送的曉光，點了點頭，表示理解。"))
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
    
    #45答案
    elif event.message.text=="正門和後門":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="44":
                worksheet.update(list[1],int(45))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔跟司晨花了好一段時間物色餐廳和菜色。"+"\n"+"現在他們已經挑選好餐點了，剩下的就是等待下課時間了。"+"\n"+"「那等等你去後門拿餐，我先去空教室找位置。」日翔開始打起了吃飯時間的策略。"+"\n"+"「好啊！哈哈，不瞞你說我已經開始肚子餓啦……」"+"\n"+"對了，雖然司晨不太可靠，但是應該可以問問他對「似曾相識的女孩」的想法吧，幸好今天沒有約曉光吃午餐。"+"\n"+"下課後，日翔坐在LM405的某個座位上等待司晨把餐點拿來教室，他無趣地看著手機中SNS朋友們發的限動，但卻像走馬看花一般，看得並不上心。簡單地說來，日翔仍舊無法忘懷那些逐漸被自己拾起的回憶，他仍然在乎那個人究竟是不是曉光。糖果紙、紀念幣、童話書、冰淇淋券……他必須承認，這些物品在他腦海內很是鮮明，像是在提醒他必須好好重視一樣。"+"\n"+"突然間LINE跳出了視窗強制打斷日翔思慮出了神的狀態，他定睛一看，原來是司晨傳訊息過來的通知：「欸欸！！！」「oO卐籃球master🍃司晨卍Oo 傳送了照片」"+"\n"+"嗯？……該不會是這個傻子取餐出了什麼事吧，沒帶錢或者是拿不動餐點之類的……日翔飛速點開LINE確認訊息。"+"\n"+"沒想到這傢伙傳的是一張鳥照片……「大笨鳥」的照片。"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fZdZax@.jpg', preview_image_url='https://ppt.cc/fZdZax@.jpg'))
                list_talk.append(TextSendMessage(text="「欸X，阿日這個笨笨的是什麼鳥啊，嗚呼！！可以養嗎？欸阿日這可以養嗎？」司晨傳了一張表達興奮的貼圖。"+"\n"+"而日翔則是回敬了一張傻眼的貼圖，接著輸入：「這叫阿司鳥，學校不是很多嗎？你現在才注意到喔。」"+"\n"+"過沒幾秒鐘，司晨便又傳來了訊息：「我以為那是雕像結果他會動？？？？」「真假跟我同名，酷欸」「不對我怎麼覺得你在損我？！？！！」"+"\n"+"劈哩啪啦地傳了三則訊息後，又緊接著貼了哭哭的動態貼圖。"+"\n"+"日翔嘆出一口氣，無奈笑了出來：「你居然會注意到我在損你？好啦，其實他叫……」"))
                list_talk.append(TextSendMessage(text="#46 輔大內有許多咖啡色的「大笨鳥」，請問他的正名是？（請以「ＯＯＯＯ」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="44":
                worksheet.update(list[1],int(45))
                list_talk=[]
                list_talk.append(TextSendMessage(text="吃飽飯後，兩人參觀博物館裡面的鳥類特別展覽。"+"\n"+"「曉光你看這個，是金剛鸚鵡耶，毛色好漂亮，好像我喜歡的寶石一樣有好多色彩。」真澄指著金剛鸚鵡的模型說著。"+"\n"+"「真的耶，我喜歡那個紅色。」"+"\n"+"「還有你看看這個，是孔雀，孔雀的毛色也好漂亮。」真澄假裝自己是孔雀，把雙手張開，像是孔雀開屏一樣。"+"\n"+"真澄好像喜歡毛色很多色的鳥類呢。曉光觀察真澄的眼神，毛色比較多樣的鳥類，真澄的雙眼就會盯著很久，但是像是禿鷹或是烏鴉等偏黑色系的鳥類，真澄連看都沒看。"+"\n"+"「喔喔喔，這個是。」真澄又指著一隻鳥。"+"\n"+"曉光的目光隨著真澄手指的方向看。「是大笨鳥呢，學校很常看到。」"+"\n"+"「哈哈哈，大家都說牠是大笨鳥，但是我看很少人知道牠的名字吧。」真澄笑著說道。"))
                list_talk.append(TextSendMessage(text="#46 輔大內有許多咖啡色的「大笨鳥」，請問他的正名是？（請以「ＯＯＯＯ」回答。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://ppt.cc/fZdZax@.jpg', preview_image_url='https://ppt.cc/fZdZax@.jpg'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #46答案
    elif event.message.text=="黑冠麻鷺":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="45":
                worksheet.update(list[1],int(46))
                list_talk=[]
                list_talk.append(TextSendMessage(text="接著，日翔就沒有看到司晨再傳訊息過來，他估摸一下時間，大概是他快要到教室來了。"+"\n"+"果不其然，他馬上就聽到了推開門的聲音，甚至聽見有人喃喃：「黑冠麻鷺黑冠麻鷺……」"+"\n"+"「嗨。為什麼你要一直講黑冠麻鷺啊？」日翔傻眼地看著進門的司晨。"+"\n"+"「久等啦。我想說以後如果想偷損討厭的教授，我就可以說他是黑冠麻鷺。」"+"\n"+"別把腦子用在這種地方好嗎——這話尚未說出口，日翔就被司晨手邊打開來的餐點吸引了注意力。他們最後其實並沒有選擇高價的餐點，只是叫了附近聽說評價不錯的小火鍋來吃而已。"+"\n"+"日翔被來自司晨桌上的香氣吸引，忍不住評價：「哇噻，這家的麻辣鍋好香哦！」"+"\n"+"司晨一邊興奮的回應，一邊把日翔的餐點從塑膠袋拿出來，自顧自地幫忙掀開蓋子：「嘿嘿，對吧。不過阿日你的起司牛奶鍋感覺也不錯啊，我夾你的豬血糕走囉。」"+"\n"+"日翔點點頭同意司晨擅自把豬血糕夾走的行為，然後把自己的起司牛奶鍋推到眼前，他把連起來的竹筷子拆開，猶豫著是否要開口提起關於兒時回憶的事情……雖然不是什麼大事，但他仍然不知道要怎麼和自己最好的朋友開口。"+"\n"+"躊躇了幾秒後，他還是帶著試探語氣地問道：「欸阿司……我可以問你一個問題嗎？」"+"\n"+"「好啊，怎麼啦？」司晨一邊咬著牛奶起司味的豬血糕一邊回應。他好像注意到了日翔的語氣變化，於是他也收起平時語氣裡帶點嘻皮笑臉的感覺，要不是他還一邊吃東西，可能會覺得他突然變得正經了起來。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='有沒有可能我以前其實見過曉光，只是我忘了？',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='有沒有可能我以前其實見過曉光，只是我忘了？'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="45":
                worksheet.update(list[1],int(46))
                list_talk=[]
                list_talk.append(TextSendMessage(text="其實我也是到現在才知道叫做黑冠麻鷺呢。增廣見聞的曉光，點了點頭。"+"\n"+"時間隨著兩人閱覽各式各樣的鳥類，導覽也漸漸到了尾聲。"+"\n"+"「導覽即將結束摟，最後提醒大家，如果喜歡鳥類的話，想買點東西回家，可以到旁邊的紀念品專區，裡面有關於鳥類的周邊商品，或是可以到這裡來，這裡有各式各樣的鳥類印章，蓋在這邊的手冊上，紀念自己到此一遊喔。」導覽員拿著麥克風大聲說著。"+"\n"+"「曉光曉光，既然都來了，我們就去蓋印章吧。」真澄像個小孩一樣，拉著曉光的衣袖，示意著曉光往剛剛導覽員說的方向行動。"+"\n"+"「好，我也想收集博物館的印章呢。」語畢，兩人走向放著手冊和蓋章的桌子旁邊準備蓋章。"))
                list_talk.append(TextSendMessage(text="小光打開手冊，翻到最後一頁。"+"\n"+"「為什麼要翻到最後一頁？」真澄問道。"+"\n"+"「對耶，下意識就…」 曉光也沒有察覺道自己做這件事的理由，手自然的就翻到最後一頁。"+"\n"+"「等等！曉光！你看。」真澄驚訝的斷句，讓曉光的視線指向真澄手指的地方。"+"\n"+"「！？」曉光驚訝到說不出話來，因為在她眼前的是，蓋著大笨鳥的印章下方寫著「曉光和日翔到此一遊:D」這句話，上面還有兩人的簽名。"+"\n"+"「曉光，你早就跟日翔同學來過了嗎？」真澄直視著曉光的雙眼。"+"\n"+"「欸？沒有，我是第一次來這間博物館啊。」曉光拼命的搖了搖頭。"+"\n"+"「那…怎麼會？」真澄也不知道發生什麼事情，只是留下這個問題給曉光，而那也是曉光內心的問題。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='有沒有可能我以前其實見過日翔，只是我忘了？',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='有沒有可能我以前其實見過日翔，只是我忘了？'
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
    
    #46答案
    elif event.message.text=="有沒有可能我以前其實見過曉光，只是我忘了？":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="46":
                list_talk=[]
                list_talk.append(TextSendMessage(text="「有啊……欸欸欸欸、以前你就認識你的真命天女曉光了嗎？！」司晨簌簌地吃著泡在麻辣鍋裡頭變得通紅的王子麵，而他的話才說到一半，吸食麵體的聲音就停了下來，換來的是王子麵咕咚的掉落跟傻瓜青年震驚的呼喊！"+"\n"+"「不是啦不是啦，我還沒確定啊！」而且你喊這麼大聲幹嘛……日翔沒好氣的吐槽。"+"\n"+"「可是我想到了以前幼稚園的時候，有個跟她相像的女孩……」日翔似乎是鬆了一口氣，果然最好的朋友是很值得傾聽的對象。他開始娓娓道來。"+"\n"+"包括突然回憶起的物件、以及幼稚園遠去的記憶，全部對他信賴的朋友悉數道出。"+"\n"+"「哦……是這樣啊……沒想到阿日也會變成黑冠麻鷺，哈哈哈哈哈。」聽完好友的秘密之後，司晨的手抵住下巴思考了一兩秒，接著又恢復一如既往的開朗，笑著調侃朋友。"+"\n"+"「？？？？？？」不要馬上就吐槽我！日翔在內心小抱怨。"+"\n"+"「直接去問曉光啊，講出來！」司晨看到好友困惑的樣子，爽快地講出自己的建議。"+"\n"+"他果然是希望我打直球。日翔很不意外，但他並不像司晨那樣直來直往的：「可是如果搞錯就很尷尬了吧？」"+"\n"+"「要不然，你剛剛說跟曉光相處就會想起很多『酷東西』對吧？那要不要試著跟她更多地相處，然後再下定論？」司晨戳起了一顆熱騰騰的麻辣魚丸，放到日翔碗裡。"+"\n"+"「你說得對。不能馬上解決的話就不能焦急。」日翔笑了，把司晨遞過來的魚丸夾起來咬了一口。麻香鮮辣卻不失原先魚漿的甜，這樣的好味道讓日翔的心情也好了起來。"+"\n"+"「哈哈，無論如何我葉司晨都會支持你的啦！兄弟你放心好了！」此刻的司晨顯得特別可靠。"+"\n"+"不過……跟曉光多多相處呀，除了專題討論跟上課這種正事之外，我有機會邀請曉光去玩嗎？日翔思考著。"))
                list_talk.append(TextSendMessage(text="兩人吃完也收拾完小火鍋的殘骸後，日翔突然想起自己還有重要的事情，那就是——他還沒有把加選單送回系辦！他目前已經確定沒有要退選的課程，剛剛的那堂課也成功加簽上了，他早有決定要先把加選單的事情在今天之內解決掉。於是，他把這件事告訴在一旁因為吃太辣而瘋狂灌水的司晨。"+"\n"+"「窩剛好耶、要去找扳刀斯，哪阿香，今天就、先降八啊啊……」我剛好也要去找班導師，那阿日，今天就先這樣吧。司晨的聲音變得有點搞笑，宛如剛剛可靠的樣子都是假的。"+"\n"+"誰叫你偏要把湯喝掉。日翔看他可憐，便放棄吐槽：「你做了什麼啊，還要去找班導師？」"+"\n"+"「煤油哇，窩很喜憨跟他勞天，今天要去、找他勞宗沒湖的依溫嗯嗯……」沒有啊，我很喜歡跟他聊天，今天要去找他聊中美湖的軼聞。"+"\n"+"日翔在腦內花了大約一秒鐘翻譯，才搞懂司晨在說些甚麼。"+"\n"+"「靠、你太扯了……好吧那我先走囉，你多喝點水，回宿舍最好吃顆胃藥，不舒服要去輔大醫院。」日翔像個媽媽一樣提點自己的好友。這傢伙舌頭都這樣了，居然還頑強打算找導師聊天，這就是直來直往向前衝的人嗎……不管是喜歡跟導師聊天還是即使舌頭遭殃還要聊個天再走都很離譜，日翔邊感嘆邊抄起手機，揹好書包後就離開了教室。"))
                list_talk.append(TextSendMessage(text="#47 請問資管系辦公室位於哪裏？（請以英文代號「ＯＯ」回答，ＯＯ為半形英文字母。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #46答案
    elif event.message.text=="有沒有可能我以前其實見過日翔，只是我忘了？":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="46":
                list_talk=[]
                list_talk.append(TextSendMessage(text="「這樣啊…不如…」話還沒說完，真澄又拿出她隨身攜帶的塔羅牌。"+"\n"+"有沒有見過日翔也可以用塔羅算嗎…？曉光已經不清楚塔羅牌的用途了。"+"\n"+"「那，幫我抽出一張牌吧。」真澄指示曉光指出一張牌。"+"\n"+"「好。」和之前占卜一樣，曉光想也沒想的用手指點出一張牌。"+"\n"+"「這個嘛…」真澄看著曉光的牌，眉頭微微一皺。"+"\n"+"「怎麼樣？」平時平淡的曉光，此時心急如焚。"+"\n"+"「你的懷疑是正確的，的確是有見過面喔，而且是你們年紀都很小的時候。」真澄回答道。"+"\n"+"「小時候…？」還沒講完話的曉光，突然像是想到了什麼，腦海中快速的閃過一個聲音。"))
                list_talk.append(TextSendMessage(text="「下次再來參觀博物館吧，曉光。」"))
                list_talk.append(TextSendMessage(text="不是真澄在說話，也不是那道光，更別說日翔沒有在現場，但是曉光確實想起這個聲音。"+"\n"+"「怎麼…」此時曉光的思緒紊亂。"+"\n"+"「曉光你還好嗎？你的臉色很難看耶，要不要先回家休息呢？」 真澄看起來很擔心的樣子。"+"\n"+"「嗯，那我先回家了，明天學校見。」曉光向真澄揮了揮手告別。"+"\n"+"「好，回家路上小心。」真澄也向曉光揮了揮手。"))
                list_talk.append(TextSendMessage(text="「今天究竟是怎麼一回事？」因為過度回想的關係，頭腦隱隱作痛，所以曉光決定提早上床。"+"\n"+"「那些東西果然跟日翔有關。」曉光看了看那些特別擺在一旁的物品。"+"\n"+"「可是…為什麼？」悄然無聲的房間，並沒有回應她的問題。"+"\n"+"「再想下去也不是辦法，還是想想明天要做什麼好了。」試圖把今天所想的事物拋開，拿出手機紀錄明天要做的事情。"+"\n"+"「我看看，首先要去辦公室找秘書，接著要去找導師，還要去一趟診所。」曉光飛快地按下手機上的按鍵。"))
                list_talk.append(TextSendMessage(text="#47 請問資管系辦公室位於哪裏？（請以英文代號「ＯＯ」回答，ＯＯ為半形英文字母。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #47答案
    elif event.message.text=="LM":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="46":
                worksheet.update(list[1],int(47))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#48 請問班導師的辦公室在哪裡？（請以「ＯＯＯ大樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="46":
                worksheet.update(list[1],int(47))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#48 請問班導師的辦公室在哪裡？（請以「ＯＯＯ大樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #48答案
    elif event.message.text=="羅耀拉大樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="47":
                worksheet.update(list[1],int(48))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#49 請問輔仁大學醫院附設診所在哪一棟建築裡？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="47":
                worksheet.update(list[1],int(48))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#49 請問輔仁大學醫院附設診所在哪一棟建築裡？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #49答案
    elif event.message.text=="國璽樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="48":
                worksheet.update(list[1],int(49))
                list_talk=[]
                list_talk.append(TextSendMessage(text="幾週後的下午，日翔準備要去濟時樓找專題開發用的程式語言教學書。這次他們選定的主題要自己學全新的程式語言，是一款他出社會後剛好沒有接觸過的語言。畢竟他實在不想拖曉光等人的後腿，於是他打算先惡補一下。"+"\n"+"輔仁大學圖書館的館藏豐富。截至2021年7月31日的統計為止，光是實體藏書合計就有147.8萬冊，若是算上可提供學生使用的電子書籍292.2萬冊就更驚人了！只要是想找學術用資料，先來圖書館跑一趟可以省下不少買書的錢，日翔這麼認為。"+"\n"+"日翔已經在昨天晚上利用輔大圖書館的館藏查詢功能找好想看的藏書號了，因此只要依照書號跟濟時樓的樓層分類做比較，就可以找到想看的書。通常一本書可以借一個月，日翔覺得借閱的時間非常充足。"+"\n"+"他正置身於一個個佇立的書架叢，認真端詳每一本書的書脊跟書號：「嗯、糟糕……到底在哪裡呢？」"+"\n"+"每一本程式教學書都跟磚塊一樣又厚又重，而且樣子都長得差不多，實在是比想像中難找到網路上都推薦的那一本。正當日翔想放棄，打算隨便抓一本回去的時候——他便在視覺的一角看到了他想借的書，同樣的書籍有三本，而且全部都放在一起。"+"\n"+"找到了！……等等，旁邊居然有人要拿那本書？日翔看到了一隻纖白的手似乎因為搆不到上方的那本程式書而正奮力地向上伸展著。"+"\n"+"至於那隻手的主人……日翔仔細一看，竟然是正在取書的曉光！她似乎差一點就夠得著那些書籍了，可輔大圖書館的書架高度對日翔來說，就算放在書架的最上面也可以輕鬆拿到。日翔思索了一下，便在內心感謝了一下父母生給自己的身高優勢。"+"\n"+"接著，日翔連墊腳尖都沒有就輕而易舉地取了兩本下來，然後將其中一本遞給曉光：「來，給妳吧。」"+"\n"+"面對曉光顯得有些驚喜的樣子，日翔有些得意的回應：「我們借好書之後，去外面聊吧。」"))
                list_talk.append(TextSendMessage(text="#50 以下何者不是輔大正確的「圖書館-館藏種類」配對？"+"\n"+"（Ａ）公博樓圖書館-人文、藝術、歷史、哲學"+"\n"+"（Ｂ）國璽樓圖書館-公共衛生、心理學、食品營養"+"\n"+"（Ｃ）濟時樓圖書總館-資訊、法律、教育"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#50',
                    template=ButtonsTemplate(
                        title='#50',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="公博樓圖書館-人文、藝術、歷史、哲學"
                            ),
                            MessageAction(
                                label='B',
                                text="國璽樓圖書館-公共衛生、心理學、食品營養"
                            ),
                            MessageAction(
                                label='C',
                                text="濟時樓圖書總館-資訊、法律、教育"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="48":
                worksheet.update(list[1],int(49))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「這樣就沒問題了，來睡覺吧。」曉光闔上手機，把房間的電燈關掉，準備入眠。"+"\n"+"春季的夜晚，涼涼的微風吹拂著，花兒隨著風搖曳，風中飄散著淡淡的花香。"+"\n"+"「看來你好像想起什麼。」早已進入夢鄉的曉光，並沒有聽到這句話。"))
                list_talk.append(TextSendMessage(text="獲得充足睡眠的曉光，擺脫昨日的疲態，整頓好心情準備好上學。"+"\n"+"昨日安排好的事情，在今日早上井然有序的辦好了，面對這些丈二摸不著金剛，宛如童話故事才會出現的劇情，曉光仍不慌不忙的處理事情，這就是曉光厲害的地方。"+"\n"+"「事情都辦好了阿，那下午就去一趟圖書館吧。」對於圖書館常客的曉光，經常瀏覽圖書館的消息，而根據圖書館最新的消息，在今日下午會引進一些新書，曉光決定去一探究竟。"+"\n"+"輔仁大學圖書館的館藏豐富。截至2021年7月31日的統計為止，光是實體藏書合計就有147.8萬冊，若是算上可提供學生使用的電子書籍292.2萬冊就更驚人了！只要是想找學術用資料，先來圖書館跑一趟可以省下不少買書的錢。"))
                list_talk.append(TextSendMessage(text="「我看看喔。」面對這些比曉光高上兩倍的新書架，曉光需要抬起頭來一本本找尋自己喜歡的書籍。"+"\n"+"找尋一段時間後，曉光的眼神緊盯著一本書，那是有關於程式的書籍，但是這本書位於書架的高處，身材嬌小的曉光無論怎麼伸手都拿不到。"+"\n"+"「怎麼辦才好？是不是該拿凳子，或是請人來拿呢？」"+"\n"+"突然，曉光看到那本書正被另外一隻手取走。"+"\n"+"「那個…」想出聲制止那隻手的曉光，因為緊張而沒注意到自己的音量。"+"\n"+"「來，給妳吧。」只見那隻手的主人把手上的書遞給曉光。"+"\n"+"曉光顯得有些驚喜，因為這隻手的主人正是日翔。"+"\n"+"「我們借好書之後，去外面聊吧。」而注意到曉光剛剛出聲音量過大，稍微吸引到一些人側目的日翔，提出這個建議。"+"\n"+"曉光點了點頭，答應日翔的邀約。"))
                list_talk.append(TextSendMessage(text="#50 以下何者不是輔大正確的「圖書館-館藏種類」配對？"+"\n"+"（Ａ）公博樓圖書館-人文、藝術、歷史、哲學"+"\n"+"（Ｂ）國璽樓圖書館-公共衛生、心理學、食品營養"+"\n"+"（Ｃ）濟時樓圖書總館-資訊、法律、教育"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#50',
                    template=ButtonsTemplate(
                        title='#50',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="公博樓圖書館-人文、藝術、歷史、哲學"
                            ),
                            MessageAction(
                                label='B',
                                text="國璽樓圖書館-公共衛生、心理學、食品營養"
                            ),
                            MessageAction(
                                label='C',
                                text="濟時樓圖書總館-資訊、法律、教育"
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

    #50答案
    elif event.message.text=="國璽樓圖書館-公共衛生、心理學、食品營養":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="49":
                worksheet.update(list[1],int(50))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#51 接續上題多媒體視聽區位於校內ＯＯ樓圖書館。（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="49":
                worksheet.update(list[1],int(50))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#51 接續上題多媒體視聽區位於校內ＯＯ樓圖書館。（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #51答案
    elif event.message.text=="公博樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="50":
                worksheet.update(list[1],int(51))
                list_talk=[]
                list_talk.append(TextSendMessage(text="借完書後，兩人坐在濟時樓外面的長椅閒聊，在鬱鬱蔥蔥的大樹下，即使是偏熱的天氣也能在樹蔭下享受到涼爽的滋味。"+"\n"+"「謝謝你。」曉光拈起了落在自己裙子上的綠葉把玩，一邊對日翔表達感謝。"+"\n"+"「不會啦，沒想到可以在借書的時候看到妳。」難得可以幫助到曉光，日翔的心情也好了起來，臉上也明顯地維持著真心的笑意。"+"\n"+"曉光看了看身旁的人臉上的表情，也帶著微笑回應：「沒想到日翔選書的品味跟我越來越近了。」"+"\n"+"沒想到今天能再見到她的笑臉，而且這是在誇我嗎……！在喜歡的人面前總是容易顯得反常，日翔焦急了起來：「哎、沒有啦，只是有先爬文而已！」"+"\n"+"只是和曉光對視而已我就這麼害臊，希望她沒有注意到自己的臉已經開始發熱了……日翔內心很是慌亂地想。"+"\n"+"「這個作者的教學很清楚，除了全彩印製之外，練習題目難度也剛剛好，重點是還附上了答案跟小建議，初學者容易錯的地方也會特別標記起來。要是我想買教學書，都會首先考慮他的著作。」好像是突然提到感興趣的話題，曉光的話好像就變多了一些，語速好像也變快了一點。"+"\n"+"聞言，日翔便感嘆：「曉光對這個真瞭解啊，大一的時候也是有妳在我才知道我差點買了一樣的書。」"+"\n"+"聽到了誇獎自己的話，曉光倒是表現得很謙虛：「只是剛好記得而已……而且，日翔你剛剛也幫助了我。」"+"\n"+"如果是阿司被我這樣誇的話，一定是洋洋得意的樣子吧……日翔把她跟自己的好友進行了一番殘酷的比對，得出了這兩人果然差距很大的結論。"))
                list_talk.append(TextSendMessage(text="突然，曉光停止把玩葉子的動作並緊緊地將它握進掌心，像是做了什麼覺悟一般。她努力正視著日翔那對琥珀色的雙眼：「唔……對了，日翔，下禮拜三有空嗎？」"+"\n"+"面對突來的問題，日翔感到驚訝，並輕輕點了點頭。"+"\n"+"雖然表面上只有點頭而已，但實際上日翔已經是受到了晴天霹靂——曉光她，居然主動問別人有沒有空，該不會是想要約我去讀書會之類的吧，而且在我決定好約她之前，她居然是主動先邀請的那個……即使是讀書會，也是讓人很期待的事情啊……"+"\n"+"曉光自然沒有發現日翔腦內的風暴，她繼續開口：「要不要來我家？」"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='？？？？！',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='？？？？！'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="50":
                worksheet.update(list[1],int(51))
                list_talk=[]
                list_talk.append(TextSendMessage(text="借完書後，兩人坐在濟時樓外面的長椅閒聊，在鬱鬱蔥蔥的大樹下，即使是偏熱的天氣也能在樹蔭下享受到涼爽的滋味。可曉光一點都感受不到什麼涼爽，畢竟她身邊可是那個過去似乎與他有所交集的男孩……而且，她自己現在也對日翔抱持著不明的好感。"+"\n"+"「……謝謝你。」曉光把玩起了落在自己裙子上的綠葉試圖冷靜下來，嘴上也不忘對日翔表達感謝。"+"\n"+"經常處於被動方的曉光其實早早就在想要不要主動約日翔看看了；前些日子在博物館看見了簽名，自那之後，她便更想嘗試慢慢地拉近日翔跟自己的關係了。說不定會因為更多的相處，回憶起更多記憶呢？"+"\n"+"曉光實在是很想趁著這次聊天的機會，乾脆邀請日翔在下周三沒課的時候一起研究專題。可她還沒有下定決心。"+"\n"+"「不會啦，沒想到可以在借書的時候看到妳。」日翔笑著回應。"+"\n"+"「沒想到日翔選書的品味跟我越來越近了。」他笑起來真好看啊，好像都要比陽光都炫目了……曉光緊張的心情依舊沒有散去，但也依舊不自覺地露出笑容。"+"\n"+"在這樣既緊張又心動的狀態下還能好好隱藏情緒聊天，應該是何曉光原先就很是聰明的緣故。"))
                list_talk.append(TextSendMessage(text="「哎、沒有啦，只是有先爬文而已！」日翔受到了誇獎後似乎顯得有些慌張，不過曉光仍然在整理自己的情緒，於是並沒有注意到這件事。"+"\n"+"「這個作者的教學很清楚，除了全彩印製之外，練習題目難度也剛剛好，重點是還附上了答案跟小建議，初學者容易錯的地方也會特別標記起來。要是我想買教學書，都會首先考慮他的著作。」曉光早早就足了功課，滔滔不絕的向日翔介紹這本書的優點。"+"\n"+"「曉光對這個真瞭解啊，大一的時候也是有妳在我才知道我差點買了一樣的書。」日翔感嘆。"+"\n"+"「只是剛好記得而已……而且，日翔你剛剛也幫助了我。」不太會表達感謝的曉光，在說出這句話後，趕緊低下頭轉移焦點，但曉光的內心是十分感謝日翔。"+"\n"+"——是啊，日翔他剛剛也幫助了我。如果不趁這次機會邀請，下一次機會還要等到什麼時候呢？如果僅僅在這裡猶豫不決，那不是和過去的自己一樣了嗎？曉光已經有過了一次後悔，她不想在第二次的大學生活之中，在此時此刻又功虧一簣。"))
                list_talk.append(TextSendMessage(text="她將葉子握進掌心，自己的命運將要由自己決定啊。"+"\n"+"「唔……對了，日翔，下禮拜三有空嗎？」曉光努力正視著日翔那對琥珀色的雙眼。"+"\n"+"面對突來的問題，日翔露出驚訝的表情，但還是輕輕點了點頭。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='要不要來我家？',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='要不要來我家？'
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
    elif event.message.text=="？？？？！":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="對日翔來說，她的攻勢可謂一波未平一波又起。不會吧！第一次被喜歡的女生邀請就是去家裡……他畢生都還沒有去過異性朋友的家裡……頂多就是以前去過男同學的家裡有遇到別人家的姊姊而已。日翔馬上就羞得要燒焦了，他結結巴巴地回應：「等等、這、會不會太突然……」"+"\n"+"「我記得真澄也沒課，如果可以的話幫我問問司晨跟宇桓吧。需要長時間開發專題的話家裡還是比圖書館方便，也可以一起討論期中考。」"+"\n"+"原來是大家一起去啊，而且是做專題……沒想到是要去曉光家裡做正事中的正事。日翔的內心因為想到專題的壓力而失落了一瞬，但也僅僅有一瞬——畢竟他可是第一次有機會去喜歡的女生家裡啊。"+"\n"+"接著，日翔連別人的行程都沒確定，就擅自替其他組員答應了邀請：「當然可以！他們都有空！」"+"\n"+"也幸好這份擅自決定的魯莽沒有害了他，日翔後來私下知會司晨跟宇桓的時候，他們都沒有拒絕下周三的聚會。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交集',
                        text='A⋂B',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='A⋂B'
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
    elif event.message.text=="要不要來我家？":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="曉光終於鼓起勇氣開口邀請日翔。不過她似乎還沒有意識到「邀請日翔去自己家」究竟有什麼不妥。畢竟對內向不愛出門曉光而言，家裡便是她最好最棒的避風港，去哪裡都沒有在家的愜意。"+"\n"+"不過，這還是曉光第一次主動約日翔，於是並不打算只約他一個人。她打算邀請專題組的所有人一起研究專題，順便讀期中考——她事前已經考慮過，做專題這事除了邀約上的「合理性」之外，多一些其他的人在場，尤其是好友真澄，也會讓她不那麼緊張……"+"\n"+"「欸、等等、這、會不會太突然……！？」畢竟只有問了「要不要來我家」，不知道曉光計畫全貌的日翔迅速地緊張了起來。"+"\n"+"「我記得真澄也沒課，如果可以的話幫我問問司晨跟宇桓吧。需要長時間開發專題的話家裡還是比圖書館方便，也可以一起討論期中考。」當曉光提起其他人的名字時，能看到日翔的表情些微的改變，不過她並沒有仔細探究原因。"+"\n"+"「當然可以！他們都有空！」日翔格外爽朗地回應。"+"\n"+"欸，他們原來都有空嗎？曉光當然不太清楚司晨跟宇桓的行程是怎麼樣的，不過既然日翔清楚就好，那麼這次的邀請就是成功了。對於自己勇敢道出心意的第一步，曉光對此頗為滿意。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交集',
                        text='A⋂B',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='A⋂B'
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
    elif event.message.text=="A⋂B":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/V3ojX1A.jpg', preview_image_url='https://i.imgur.com/V3ojX1A.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-1',
                        text='繼續看主線故事-1',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-1'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/V3ojX1A.jpg', preview_image_url='https://i.imgur.com/V3ojX1A.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-1',
                        text='繼續看主線故事-1',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-1'
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
    elif event.message.text=="繼續看主線故事-1":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="終於到了眾人約定前往曉光家的時間，專題組一行人已經來到了曉光家門口。曉光首先走在最前頭開完了鎖，司晨便搶先步伐跑進了別人家裡。"+"\n"+"可能是一進門就可以看見玄關跟大大的客廳，還有採光良好的落地窗跟分布於客廳的木製貓爬架的緣故，司晨居然像小學生遠足一樣興奮地跑來跑去：「好耶！這裡好大喔！！」"+"\n"+"曉光安靜地瞄了一眼窩在紙箱裡休息的灰色胖貓，提醒道：「不要用跑的，德魯貝會嚇到。」"+"\n"+"似乎是因為被主人點名，德魯貝對著剛剛還在亂跑的司晨發出了意義不明的貓叫聲。有一瞬間，司晨好像覺得德魯貝的眼神像是在看笨蛋一樣，但願只是個錯覺。"+"\n"+"日翔看了一眼紙箱中的貓咪，心想那隻「德魯貝」跟曉光手機殼上面的貓果然一模一樣，只是體積好像比想像中的大很多。他好奇地走向貓咪打算多觀察一下他，並隨口提起了問題：「哇，曉光，你現在只跟德魯貝住嗎？」"+"\n"+"話說回來，這隻貓還真胖啊，在曉光家裡過得這麼好嗎？"+"\n"+"曉光確認好所有人都進到家中後鎖上了門，回應：「我媽今天剛好出差不在。」"+"\n"+"不知為何，日翔竟然覺得這隻貓讓自己感到格外的熟悉，但明明應該是第一次見到德魯貝才對——他困惑地想，這種「似曾相識的熟悉感」好像之前在哪裡經歷過了一回，但是他突然想不起來到底是什麼時候的事情，有可能是錯覺吧。"+"\n"+"下一刻，德魯貝便擅自跳進了眼前人類的懷裡，嚇得日翔差點沒接住牠。"+"\n"+"「哇！好重！」日翔感嘆，不過還是很欣然地抱住了對自己毫無戒心的大貓咪。"+"\n"+"「看來德魯貝很喜歡你。」曉光並沒有制止德魯貝跟日翔的互動，也沒有反對其他人在自己家裡參觀的行為，而是一邊打開冰箱拿出招待客人的飲品和點心。"+"\n"+"「所以妳才讓我們到妳家啊，雖然之前就猜想可能很大，但沒想到這麼氣派。」真澄已經擅自坐到了客廳的沙發上，或許是因為足夠熟稔，認為曉光不會介意別人碰東西，於是她沒有經過詢問就直接抱起了一旁貓咪圖案的小靠枕。"+"\n"+"「普普通通吧。」用托盤端著五杯飲料的曉光和坐在沙發上看手機的宇桓不約而同地回應真澄，只不過態度很明顯是一個謙虛一個高傲。"+"\n"+"「這是葡萄汁，」曉光像個服務生一樣熟練地把五盞玻璃杯裝的葡萄汁一一放在乾淨的桌子上：「冰箱裡還有我昨天去亞O克買的北海道生乳捲，等等要是討論累了可以一起吃。」"+"\n"+"「日翔！！快點過來，我們要開始討論囉！」在沙發旁邊席地而坐的司晨朝著還在跟德魯貝玩的日翔大喊。"+"\n"+"「小聲一點，德魯貝會嚇到。」曉光再次出聲提醒，很明顯是在平靜中多了些無奈的語氣。"+"\n"+"日翔的內心仍然帶著說不出口的困惑——我跟那隻貓真有那麼熟嗎？但看看現狀，應該也沒有人可以回答這個奇怪的問題，他只得抱著不想離開懷裡的貓咪走向桌子旁：「啊、好，我馬上過來。」"))
                list_talk.append(TextSendMessage(text="終於討論得告一段落，眾人也結束了期中考的讀書會——因為大三的必修課跟理論課都不多，所以讀書時間自然是結束得比想像中要快。宇桓已經幫所有人叫了晚餐的外送，於是所有人便決定吃個晚餐再散會。"+"\n"+"「噯、日翔，大好機會啊！臉書通知寫說曉光的生日就快到了！要不要約她出去玩？」司晨趁著曉光到廚房洗吃蛋糕用的碗盤時，偷偷對日翔建議了一番。"+"\n"+"「說得也是……不過我對於要去哪邊玩實在沒什麼頭緒。」日翔的頭垂了下來，很是懊惱的樣子。"+"\n"+"剛剛還放鬆到開始躺在沙發上看手機的真澄似乎是聽見有意思的話題而坐了起來：「想對我家曉光做什麼？我就知道你肯定對她有意思……」"+"\n"+"「咳，日翔，我真的一點都不介意，只是想提醒你別約她去太需要跑跑跳跳的地方，她體力不是很好。」雖然說了「不介意」但日翔總覺得真澄的話裡明顯帶了醋意，也帶了點「真澄我可比你了解曉光」的較勁意味。"+"\n"+"哇……這就是女生跟女生的交情嗎。日翔稍有不解地默默感嘆。不過自己有表現出來喜歡曉光嗎？日翔對此提出疑問：「哎？有這麼明顯嗎？」"+"\n"+"「畢竟曉光是系花，男生對她有意思不奇怪吧。而且再怎麼說，這麼明顯應該也只有曉光本人沒有看出來了。」真澄擺擺手，表現出好像不是第一次應付這種狀況的樣子。"+"\n"+"宇桓只是點頭表示同意真澄的說法，倒是不知道他心裡在想些什麼。"+"\n"+"「找個放學過後短時間在學校附近轉轉的地方，應該不錯吧……」日翔單手抵著下巴思索了起來。他並沒有想要第一次邀約就挑戰和曉光玩一整天，還是先以短時間又輕鬆的邀約為主吧。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交換',
                        text='向陽融化之冰',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='向陽融化之冰'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="終於到了眾人約定前往曉光家的時間，專題組一行人已經來到了曉光家門口。曉光首先走在最前頭開完了鎖，司晨便搶先步伐跑進了別人家裡。"+"\n"+"可能是一進門就可以看見玄關跟大大的客廳，還有採光良好的落地窗跟分布於客廳的木製貓爬架的緣故，司晨居然像小學生遠足一樣興奮地跑來跑去：「好耶！這裡好大喔！！」"+"\n"+"「小聲一點，德魯貝會嚇到。」曉光安靜地瞄了一眼窩在紙箱裡休息的灰色胖貓提醒道，似乎是因為被主人點名，德魯貝對著剛剛還在亂跑的司晨發出了意義不明的貓叫聲。"+"\n"+"隨即，一旁的日翔看到德魯貝的樣子，提出了一個問題。"+"\n"+"「哇，曉光，你現在只跟德魯貝住嗎？」"+"\n"+"「我媽今天剛好出差不在。」曉光確認好所有人都進到家中後鎖上了門，回應日翔的問題。"+"\n"+"下一刻，德魯貝便擅自跳進了眼前人類的懷裡，嚇得日翔差點沒接住牠。"+"\n"+"「哇！好重！」日翔感嘆，卻看起來相當熟練地抱著德魯貝。"+"\n"+"「看來德魯貝很喜歡你。」曉光並沒有制止德魯貝跟日翔的互動，也沒有反對其他人在自己家裡參觀的行為，而是一邊打開冰箱拿出招待客人的飲品和點心。"+"\n"+"「所以妳才讓我們到妳家啊，雖然之前就猜想可能很大，但沒想到這麼氣派。」真澄已經擅自坐到了客廳的沙發上，抱起了一旁貓咪圖案的小靠枕。"+"\n"+"「普普通通吧。」用托盤端著五杯飲料的曉光和坐在沙發上看手機的宇桓不約而同地回應真澄，只不過態度很明顯是一個謙虛一個高傲。"))
                list_talk.append(TextSendMessage(text="「這是葡萄汁，」曉光像個服務生一樣熟練地把五盞玻璃杯裝的葡萄汁一一放在乾淨的桌子上：「冰箱裡還有我昨天去亞O克買的北海道生乳捲，等等要是討論累了可以一起吃。」"+"\n"+"司晨、宇桓和真澄接二連三的點頭道謝，唯獨日翔還在不遠處的一旁和德魯貝嘻鬧。"+"\n"+"「日翔！！快點過來，我們要開始討論囉！」在沙發旁邊席地而坐的司晨朝著還在跟德魯貝玩的日翔大喊。"+"\n"+"「小聲一點，德魯貝會嚇到。」曉光再次出聲提醒，很明顯是在平靜中多了些無奈的語氣。"+"\n"+"「啊、好，我馬上過來。」聽見呼喚聲的日翔，抱著德魯貝回應道。"))
                list_talk.append(TextSendMessage(text="終於討論得告一段落，眾人也結束了期中考的讀書會——因為大三的必修課跟理論課都不多，所以讀書時間自然是結束得比想像中要快。宇桓已經幫所有人叫了晚餐的外送，於是所有人便決定吃個晚餐再散會。"+"\n"+"曉光決定先收拾好方才吃蛋糕用的碗盤待會才有空間吃晚餐，大夥表示想幫忙不過曉光婉拒了，畢竟來者是客，讓客人幫忙收拾太不好意思了。曉光洗著碗回想今日讀書兼專題討論會的場景，不斷提出無厘頭提案的司晨、憤怒斥責的宇桓、擔任和事佬的日翔、在旁邊看好戲的真澄，吵吵鬧鬧的……可是，也不壞。若是以往的自己，可能也沒有想到會有邀請朋友回家作客的一天，每每看見三五成群作伴、感情很好的同學，說不羨慕也是騙人的，曉光打從心底感謝那聲音讓自己回到過去，讓她能勇敢向前。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交換',
                        text='向陽融化之冰',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='向陽融化之冰'
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
    elif event.message.text=="向陽融化之冰":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/ixtqZOa.jpg', preview_image_url='https://i.imgur.com/ixtqZOa.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-2',
                        text='繼續看主線故事-2',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-2'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/ixtqZOa.jpg', preview_image_url='https://i.imgur.com/ixtqZOa.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-2',
                        text='繼續看主線故事-2',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-2'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #??
    elif event.message.text=="繼續看主線故事-2":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="時間飛逝，期中考在即。曉光的生日在期中考之後——必須要跨越這道牆，才能夠到達和曉光一起玩的美好時光。當然，日翔並沒有忘記他必須在課業上全力以赴的理念。為了不再次變成那個沒有選擇只能待在某公司賣肝的社畜日翔，也得努力備考才行。"))
                list_talk.append(TextSendMessage(text="#52 有一空堆疊（Stack），依序做push(a)、push(b)、push(c)、pop、push(d)、push(e)、pop後，由下往上的資料依序是？（填寫範例如下，請依序輸入半形小寫「ＯＯＯ」回答。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/02/3oDCXx.png', preview_image_url='https://upload.cc/i1/2022/04/02/3oDCXx.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                list_talk=[]
                list_talk.append(TextSendMessage(text="時間飛逝，期中考在即，而曉光的生日也跟著接近了。不過，為了保持好成績，就算是生日也得先擱在一邊，專心面對高山一樣的參考書，才能解決即將來臨的期中考！"))
                list_talk.append(TextSendMessage(text="#52 有一空堆疊（Stack），依序做push(a)、push(b)、push(c)、pop、push(d)、push(e)、pop後，由下往上的資料依序是？（填寫範例如下，請依序輸入半形小寫「ＯＯＯ」回答。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/02/3oDCXx.png', preview_image_url='https://upload.cc/i1/2022/04/02/3oDCXx.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #52答案
    elif event.message.text=="abd":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="51":
                worksheet.update(list[1],int(52))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#53 小志畢業後可以選擇就業或繼續攻讀研究所。如果小志選擇上研究所，他的學費總共是42000元，生活費31000元，書本費2300元。若他選擇就業，他的薪水是25000元，生活費13000元。小志選擇上研究所的成本總共是？（請以「Ｏ元」回答，Ｏ數量不代表答案正確字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="51":
                worksheet.update(list[1],int(52))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#53 小志畢業後可以選擇就業或繼續攻讀研究所。如果小志選擇上研究所，他的學費總共是42000元，生活費31000元，書本費2300元。若他選擇就業，他的薪水是25000元，生活費13000元。小志選擇上研究所的成本總共是？（請以「Ｏ元」回答，Ｏ數量不代表答案正確字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #53答案
    elif event.message.text=="108000元":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="52":
                worksheet.update(list[1],int(53))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#54 下列何者記憶體管理方法有內部碎裂（Internal Fragmentation）問題？"+"\n"+"（Ａ）分頁（Page）"+"\n"+"（Ｂ）連續性（Contiguous）"+"\n"+"（Ｃ）分段（Segment）"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#54',
                    template=ButtonsTemplate(
                        title='#54',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="分頁（Page）"
                            ),
                            MessageAction(
                                label='B',
                                text="連續性（Contiguous）"
                            ),
                            MessageAction(
                                label='C',
                                text="分段（Segment）"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="52":
                worksheet.update(list[1],int(53))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#54 下列何者記憶體管理方法有內部碎裂（Internal Fragmentation）問題？"+"\n"+"（Ａ）分頁（Page）"+"\n"+"（Ｂ）連續性（Contiguous）"+"\n"+"（Ｃ）分段（Segment）"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#54',
                    template=ButtonsTemplate(
                        title='#54',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="分頁（Page）"
                            ),
                            MessageAction(
                                label='B',
                                text="連續性（Contiguous）"
                            ),
                            MessageAction(
                                label='C',
                                text="分段（Segment）"
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
    
    #54答案
    elif event.message.text=="分頁（Page）":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="53":
                worksheet.update(list[1],int(54))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#55 發生死結（Deadlock）的條件有幾個？（請輸入「Ｏ個」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="53":
                worksheet.update(list[1],int(54))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#55 發生死結（Deadlock）的條件有幾個？（請輸入「Ｏ個」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #55答案
    elif event.message.text=="4個":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="54":
                worksheet.update(list[1],int(55))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#56 請判斷下列程式碼，包含main()一共會產生多少process？（請輸入「Ｏ個process」，Ｏ為半形數字。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/02/r8NibS.png', preview_image_url='https://upload.cc/i1/2022/04/02/r8NibS.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="54":
                worksheet.update(list[1],int(55))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#56 請判斷下列程式碼，包含main()一共會產生多少process？（請輸入「Ｏ個process」，Ｏ為半形數字。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/02/r8NibS.png', preview_image_url='https://upload.cc/i1/2022/04/02/r8NibS.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #56答案
    elif event.message.text=="8個process":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="55":
                worksheet.update(list[1],int(56))
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔突然覺得，他或許是一個會在關鍵時刻成為縮頭烏龜的人。"+"\n"+"距離曉光的生日已經剩下僅僅一周了，他卻沒有下定決心要怎麼樣好好約曉光才行——他確實是有考慮過要不要在LINE上面約曉光就好，可是又怕會不會太突然……光是在這件事上，日翔就猶豫了許久。"+"\n"+"日翔坐在輔園的椅子上咬著插在珍珠紅茶上頭的吸管：「哎。怎麼辦才好啊——」"+"\n"+"今天司晨沒課，怎麼偏偏在這煩惱的時刻少了平常最熱鬧的人啊，如果他在的話或許還能跟我討論，或者讓我分分心的……日翔自顧自地喃喃道。"+"\n"+"突然，有一道人影直截了當地到了日翔面前，甚至在日翔反應過來前就理所當然地坐在了他的對面：「你一個人在這煩惱沒用的。」"+"\n"+"日翔一聽到那個傲骨嶙嶙的聲音時，就已經確定了這個人究竟是何方神聖：「啊、……宇、宇桓？你今天也有課嗎？」"+"\n"+"沒想到宇桓會在這個時候來輔園……日翔頗為震驚。不過，宇桓並沒有打算要理會日翔的疑問，倒是單刀直入地切入主題：「這麼煩惱的話你大可去找諮詢。」"))
                list_talk.append(TextSendMessage(text="#57 請問要是心情鬱悶，想找個人談談的話，可以到哪裡諮詢呢？"+"\n"+"（Ａ）在籃球場吶喊"+"\n"+"（Ｂ）去全聯福利中心買買買解悶"+"\n"+"（Ｃ）去學生輔導中心詢問"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#57',
                    template=ButtonsTemplate(
                        title='#57',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="在籃球場吶喊"
                            ),
                            MessageAction(
                                label='B',
                                text="去全聯福利中心買買買解悶"
                            ),
                            MessageAction(
                                label='C',
                                text="去學生輔導中心詢問"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="55":
                worksheet.update(list[1],int(56))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「終於結束了。」 剛考完試的曉光決定要吃冰淇淋犒賞自己。"+"\n"+"曉光找了一個空曠的地方，坐在長椅上好好享用冰淇淋。"+"\n"+"「考完是考完了，但好像還沒辦法放鬆下來。」"+"\n"+"至今為止，曉光未解的謎團越來越多了。首先是那莫名其妙帶她回來的那道光，家裡出現自己沒有印象的物品，看到博物館與日翔的筆跡，這些種種讓她摸不著頭緒。"+"\n"+"而一想到日翔的曉光，心跳得特別快。"+"\n"+"「該怎麼辦才好…」曉光也不知道該跟誰提起這件事，說自己突然又重新過了大學生活，任誰都不會相信。"+"\n"+"「要不要去諮詢看看呢？」"))
                list_talk.append(TextSendMessage(text="#57 請問要是心情鬱悶，想找個人談談的話，可以到哪裡諮詢呢？"+"\n"+"（Ａ）在籃球場吶喊"+"\n"+"（Ｂ）去全聯福利中心買買買解悶"+"\n"+"（Ｃ）去學生輔導中心詢問"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#57',
                    template=ButtonsTemplate(
                        title='#57',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="在籃球場吶喊"
                            ),
                            MessageAction(
                                label='B',
                                text="去全聯福利中心買買買解悶"
                            ),
                            MessageAction(
                                label='C',
                                text="去學生輔導中心詢問"
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

    #57答案
    elif event.message.text=="去學生輔導中心詢問":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="56":
                worksheet.update(list[1],int(57))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「學校原來就有諮詢的資源啊……不過我想這次還是一個人解決就好，謝謝你。」日翔從來不曉得學校居然有專門的諮商服務，而且除了許多老師都會協助進行個人輔導以外，居然還有團體輔導。如果以後真的有需要的話，那或許他也會考慮去諮商看看吧。日翔想到了畢業之後去外面找個諮商就花了他不少錢，瞬間感覺到了學校的良心。"+"\n"+"「游日翔。」宇桓嚴肅地喊住日翔的全名，他再次不顧話題地開口：「你再繼續猶豫不決的，我就要出手了。」"+"\n"+"日翔直覺性地感受到，這或許是對自己的宣戰。他有些驚訝：「欸？欸？難道，你也對曉光……」"+"\n"+"還等不到宇桓的回應，他便頭也不回的離開了。日翔想到之前去曉光家的時候，真澄也提到「男生們對曉光有意思」完全不奇怪……甚至從最當初想起，宇桓想加入專題組，或許就是因為曉光吧……雖說如此，但日翔不知為何地感覺宇桓可能是在鼓勵自己，沒想到這個人比想像中還要好。"+"\n"+"或許也是因為這一樁突來的衝擊，日翔決定現在就傳LINE邀請曉光，他點進了那個熟悉的灰色貓咪頭貼：「曉光，下禮拜11月24日是你的生日吧？要一起出去玩嗎？」"+"\n"+"對方很快就回了一個貓咪問號的貼圖，接著回應：「和大家一起？」"+"\n"+"日翔見到曉光秒回便緊張地嚥了下口水——平常都沒什麼傳訊息的機會，現在一交流就是要邀請他兩個人約會……真叫人害羞的。"+"\n"+"他敲了敲鍵盤，趕緊回應或許還在等待自己回覆的曉光：「我們兩個人就好。」"))
                list_talk.append(TextSendMessage(text="終於盼到了曉光生日的那一天，日翔甚至緊張得整晚都沒有睡好……整個晚上日翔幾乎都在思考自己要預備些什麼話題、穿什麼衣服、或者該怎麼打理自己的髮型。"+"\n"+"也因為整晚幾乎沒睡好，日翔甚至比預計時間早起了整整一小時。雖然提出邀請的是自己，但也壓根沒想到自己真會有和曉光約會的一天。"+"\n"+"他們今天要一起去IKEA新莊店逛逛，除了可以添購一些家中小物之外，日翔聽說IKEA還被鄉民譽為「被家具耽誤的餐廳」，他早就想去一探究竟了。此外，曉光也表示想要買一隻鯊鯊回家，於是兩人一拍即合，便馬上決定了要在這裡相聚。"+"\n"+"想到了跟那個「Code/140.136」的約定，日翔再度燃起了鬥志。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='我今天絕對要全力以赴。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='我今天絕對要全力以赴。'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="56":
                worksheet.update(list[1],int(57))
                list_talk=[]
                list_talk.append(TextSendMessage(text="一個熟悉的聲音傳來。曉光猛然抬起頭來尋找聲音的來源。"+"\n"+"「是我啦，你的知心好友真澄。」真澄比出勝利手勢，順勢坐到曉光旁邊。"+"\n"+"真澄是什麼時候來的？也許是心中的大石頭還沒有放下，曉光並沒有發現真澄的靠近。"+"\n"+"「是不是在煩惱日翔的事情啊？」真澄一語就說出了曉光心中所想。"+"\n"+"「咦咦...？你怎麼會知道？」一聽見關鍵字，曉光緊張得連講話都顫抖了起來。雖然曉光知道真澄一向直覺很準，但她怎麼會知道呢？難不成又是塔羅牌告訴她的？"+"\n"+"「哎呀，你全部都寫在臉上了啊。」真澄笑嘻嘻地戳了戳曉光因為種種疑惑而皺緊的眉頭，好似在示意曉光放輕鬆一點。"+"\n"+"「才沒有......」 曉光不滿的噘起嘴來。"+"\n"+"「瞧你緊張的樣子。」真澄笑道，她總是看不膩曉光臉上的表情變化。「好啦！不鬧妳了！在妳生日那幾天說不定會發生好事讓煩惱都會迎刃而解喔！」"+"\n"+"「咦...？」曉光不解真澄語中藏有的訊息。"+"\n"+"「我以這張上面印有翡翠寶石的塔羅牌發誓！」真澄從書包裡亮出她提到的牌，神祕地告訴曉光，「妳到時候就會知道了！」"))
                list_talk.append(TextSendMessage(text="幾天後曉收到了來自日翔的訊息：「曉光，下禮拜11月24日是你的生日吧？要一起出去玩嗎？」"+"\n"+"「和大家一起？」曉光點了一個貓咪問號的貼圖做回應。"+"\n"+"「我們兩個人就好。」"+"\n"+"我們兩個…一起…看到這句話的曉光，內心掀起無數波瀾，腦袋的思緒又再度錯亂。這難道就是真澄說的「好事」嗎？曉光只要一想像和日翔單獨在一起的景象，就會害羞地想找個洞跳進去。"+"\n"+"「好。」 曉光決定要告別以往怯懦的自己，下定決心答應了日翔的邀約。"+"\n"+"他們最後決定要一起去IKEA新莊店逛逛，除了可以添購一些家中小物之外，日翔聽說IKEA還被鄉民譽為「被家具耽誤的餐廳」，他早就想去一探究竟了。此外，曉光也表示想要買一隻鯊鯊回家，於是兩人一拍即合，便馬上決定了要在這裡相聚。"))
                list_talk.append(TextSendMessage(text="赴約前一晚曉光幾乎是將衣櫃裡的衣服一套套翻出來思考了很久，第一次和日翔單獨出門讓曉光十分緊張，她謹慎仔細地搭配衣服，甚至還想找母親借用化妝品上點妝，可不能讓人覺得自己隨隨便便地就出門了。"+"\n"+"隔天曉光起了個大早，甚至比自己的鬧鐘還要早醒過來。曉光最後選擇了米色的燈籠袖襯衫洋裝，外頭再加了一件棕色馬甲背心，再搭配了一只側背的貓咪小包。曉光站在鏡子面前再三確認服裝儀容。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='加油！',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='加油！'
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
    elif event.message.text=="我今天絕對要全力以赴。":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="57":
                list_talk=[]
                list_talk.append(TextSendMessage(text="日翔抵達IKEA建築內的時候，曉光已經在裡面等了——可實際上，日翔是提早了20分鐘到達約定地點的。曉光會提得這麼早到，實際上有些超乎他的意料，畢竟他本來就因為早起而打算提早到達等待曉光，順便在空閒的時間做好和曉光約會的心理準備。"+"\n"+"可現在一切計畫都被打亂了！沒想到曉光也是習慣早到的人……得要靠臨場反應了。"+"\n"+"「曉光！你好早到啊！」日翔往曉光的方向奔去，朝她大幅度地揮了揮手。"+"\n"+"「不會……只是剛好早起了些。倒是日翔你氣色好像不太好。」"+"\n"+"「沒、沒有啊，應該是你的錯覺吧。」"+"\n"+"日翔突然有一個大膽的猜想：曉光會不會跟自己一樣，其實半夜都沒睡好覺啊！但日翔其實並沒有特別去留意曉光的神氣，反倒是被她的服裝所吸引——她的女神打扮得並不是太華麗、也不是太簡約，她身穿一襲米色的燈籠袖襯衫洋裝，外頭再加了一件棕色馬甲背心，再搭配了一只側背的貓咪小包。曉光本身就看起來就是乾淨氣質，這套服裝在所謂氣質之上又更增添了些復古文青的風味，同時因為肩上的貓咪包包而不顯得過於成熟。"+"\n"+"「妳今天的穿著真好看啊。」日翔看著看著，決定坦率地對曉光的穿著表示讚賞。"+"\n"+"「欸、」曉光似乎是因為被肯定而露出了有些欣喜的樣子，她問道：「真的嗎？」"+"\n"+"「我不會騙你啦。走吧。」語畢，日翔決定豁出去，決定就這樣直接拉著她的手走往賣場裡頭。不過因為有些緊張，日翔並沒有看見被突然牽起了手而滿臉通紅的曉光。"+"\n"+"在兩人視線的角落，似乎有另外一組人馬正在觀察他們……"+"\n"+"「哇、這兩個人的進展比想像中快啊。」"+"\n"+"「對啊對啊！好興奮！……呃，真澄？你怎麼在這裡？」"+"\n"+"「司晨，你也來湊熱鬧啊，那你等等一定要給我小聲點，別被他們發現了。」"))
                list_talk.append(TextSendMessage(text="「啊、我是不是……不該擅自拉著妳的手的？抱歉！」兩人總算從門口一路搭手扶梯到了賣場內，可日翔這才意識到自己是不是不該擅自就牽別人的手，應該要徵得對方的同意才對。"+"\n"+"曉光並沒有忽視日翔的道歉，可她回答得極其小聲，卻還是被日翔一字不差地聽見了：「……沒關係，我不在意。」"+"\n"+"正當日翔打算放開手時，才發現曉光似乎沒有放開的意思。曉光是不是想要就這樣手牽著手一起逛呢？日翔因為完全沒有料想到這樣的展開而大腦一片空白，但他當然沒有就這樣甩開曉光，而是再次握好了曉光的手心。"+"\n"+"日翔突然發現，跟曉光手牽手感覺居然令人倍感溫暖、且十分熟稔。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交心',
                        text='與 ░░░ 的約定',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='與 ░░░ 的約定'
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
    elif event.message.text=="加油！":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="57":
                list_talk=[]
                list_talk.append(TextSendMessage(text="曉光雙手握拳替自己打氣。"+"\n"+"「德魯貝你也要幫我加油喔。」即將出門的曉光摸了摸家中愛貓的毛髮，而德魯貝發出「呼魯魯」的聲響，似乎非常享受。"+"\n"+"習慣早到的曉光提早二十分鐘抵達指定的地點，在此同時，她也看到日翔朝她揮著手奔來：「曉光！你好早到啊！」"+"\n"+"「不會……只是剛好早起了些。」待日翔近了些曉光才注意到日翔臉上似乎有些疲倦於是出聲關心道，「倒是日翔你氣色好像不太好。」"+"\n"+"「沒、沒有啊，應該是你的錯覺吧。」嗯……既然本人都這麼說了，曉光也沒有繼續追問下去。"+"\n"+"「妳今天的穿著真好看啊。」日翔看了看曉光的衣著，沒有一絲猶豫就說出這句話。"+"\n"+"「欸、真的嗎？」"+"\n"+"「我不會騙你啦。走吧。」曉光的手被日翔牽了起來。"))
                list_talk.append(TextSendMessage(text="「？？？！！」曉光沒有料到日翔這突如其來的舉動，曉光感覺自己好像發燒一樣臉紅得不像話，曉光還是第一次跟異性牽手，而且還是跟日翔……曉光的手被日翔溫暖的掌心包覆住，她並不覺得排斥，反倒還希望日翔不要放開……"+"\n"+"而在兩人視線的角落，似乎有另外一組人馬正在觀察他們……"+"\n"+"「哇、這兩個人的進展比想像中快啊。」"+"\n"+"「對啊對啊！好興奮！……呃，真澄？你怎麼在這裡？」"+"\n"+"「司晨，你也來湊熱鬧啊，那你等等一定要給我小聲點，別被他們發現了。」"))
                list_talk.append(TextSendMessage(text="「啊、我是不是……不該擅自拉著妳的手的？抱歉！」兩人從門口一路搭手扶梯到了賣場內，日翔才發現他一直牽著曉光的手。"+"\n"+"「…沒關係。」 曉光小聲地說，「我不在意。」"+"\n"+"正當日翔打算放開手時，曉光卻握緊了手，不願意放開。"+"\n"+"這樣很好。曉光沒有說出這句話，但是日翔彷彿能知道曉光的想法，再次握好小光的手心。"+"\n"+"曉光突然發現，跟日翔手牽手感覺居然令人倍感溫暖、且十分熟稔。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='解鎖記憶碎片',
                    template=ButtonsTemplate(
                        title='交心',
                        text='與 ░░░ 的約定',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='與 ░░░ 的約定'
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
    elif event.message.text=="與 ░░░ 的約定":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="57":
                worksheet.update(list[2],int(9))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖照片！趕快去「個人檔案」看看！"))
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/1sdS8xa.jpg', preview_image_url='https://i.imgur.com/1sdS8xa.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-3',
                        text='繼續看主線故事-3',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-3'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="57":
                worksheet.update(list[2],int(9))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖照片！趕快去「個人檔案」看看！"))
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/1sdS8xa.jpg', preview_image_url='https://i.imgur.com/1sdS8xa.jpg'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='繼續看主線故事',
                    template=ButtonsTemplate(
                        title='繼續看主線故事-3',
                        text='繼續看主線故事-3',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='繼續看主線故事-3'
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
    elif event.message.text=="繼續看主線故事-3":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="57":
                list_talk=[]
                list_talk.append(TextSendMessage(text="兩人就這樣慢悠悠地逛了幾乎整個賣場，曉光很中意大鯊鯊玩偶「BLÅHAJ」於是抱了一隻，日翔也打算買一隻，便也拿在手上。"+"\n"+"當然，手也還是牽得緊緊的。他們似乎是已經習慣了對方手心的溫度，更或者是有了什麼不約而同的默契，誰都不願意放開手；畢竟就如日翔所推測的，只要與曉光相處，就會回憶起更多童年的點點滴滴——他甚至想起了與他一起度過幼兒園時期的女孩就是曉光。"+"\n"+"日翔覺得現在就是問曉光的大好時機，此時不問更待何時！更何況曉光也不像是會主動開口詢問的人，他便主動出擊：「那個……」"+"\n"+"「那個……」旁邊的女孩異口同聲。"+"\n"+"沒想到跟曉光同時開了口，日翔對這個意料之外的默契感到有些驚訝。而一旁的曉光似乎也嚇到了，她連忙回應：「沒事、你先講。」"+"\n"+"似乎是因為接下來要談的事情藏在心中很久了。日翔的語氣變得鄭重了起來：「我有一件很重要的事情要問你。」"+"\n"+"「……我剛剛也想起來了。」曉光連日翔的問題都沒有聽，似乎判斷出了他究竟想要說些什麼。她露出了淺淺的微笑，那笑起來的模樣讓人聯想到清甜的蘋果汁。"+"\n"+"日翔看著她的笑臉，似乎也知道了她究竟要講些什麼：「曉光，難道妳是說……妳也跟我一樣想起了那個約定？」"+"\n"+"或許是因為回憶起了相同的場景，日翔跟曉光格外地有著對話的默契，不用把話說得清楚就可以了解對方想表達的東西。"+"\n"+"「嗯，那個人就是你。」曉光的語氣卻是少見地篤定。"+"\n"+"「沒想到我們到現在才真正地相認啊……對不起，我應該要早些想起來的。」日翔的這話是和曉光道歉，也是和多年前尚未回到大學生活的那個自己道歉，他實在不曉得自己會那麼遲鈍，居然和曉光同班了那麼久都沒發現她就是記憶中的孩子。"+"\n"+"突然，有個熟悉的聲音打破了兩人的對話：「哇X！真假！！！！」"+"\n"+"日翔轉頭一看，竟然是司晨躲在柱子後面大喊大叫……或許是因為聽到了他們所有的對話？而從位置判斷的話可以猜測，本來他應該是躲藏起來的，所以一個腦袋瓜才從柱子旁邊路露了出來。……躲藏得並不是很好啊，這個笨蛋。日翔心想。"+"\n"+"「白癡，司晨你太大聲了！！」接著，日翔和曉光聽到了另一個熟悉的聲音對著司晨進行告誡。"+"\n"+"兩人毅然決然往聲音的方向走近，當然是看見了露出尷尬神情的司晨跟真澄。"))
                list_talk.append(TextSendMessage(text="或許是因為感到害臊，日翔和曉光的手已經放開來了，曉光的雙手緊緊抱著鯊鯊一語不發，似乎是對於被兩個朋友「關切」（雖然很明顯這只是單純的跟蹤而不是關切）而有些難為情的緣故。"+"\n"+"「就是，實在是太擔心了才來看看啊，阿日你前陣子不還是很猶豫不決嗎？」司晨好像沒有對偷窺兩人約會表達歉意的意思，至少依他的神情看來，應該是真的很擔心他摯友的狀況。"+"\n"+"「是這樣沒錯……」日翔無言，但其實也頗為習慣了。這個人做出傻事好像也不是第一次了。"+"\n"+"「今天也是我的生日，有人搶了我跟曉光相處的好時光才過來關心一下。」真澄跟著解釋了自己的動機，但不知為何日翔總感覺她似乎不打算澄清什麼。"+"\n"+"日翔忍不住對真澄吐槽：「等等，不是我的錯吧！」"+"\n"+"「噗、」聽見他們的對話，原先感到害羞的曉光終究還是笑了出來，更是：「好意外，真澄跟司晨居然都跟過來了。」"+"\n"+"而原先日翔跟曉光兩人預定的午餐時刻自然是演變成了四個人一起在瑞典餐廳吃飯，日翔表示他要順便請客慶祝一下現場兩位女生的生日。"+"\n"+"日翔對此的心得是：肉丸很好吃！他同意IKEA是一間被家具耽誤的餐廳，可面對司晨瘋狂催促和曉光快點交往的事情，又是另一個故事了。"))
                list_talk.append(TextSendMessage(text="雖然也感受到了曉光對自己的好感，但日翔顧慮到了專題發表的壓力，於是他還沒有跟曉光告白。他打算要等到時機成熟，大家都放下了壓力之後再明確地告訴曉光自己的心意。日翔注意到自己在和曉光的第一次約會過後和她的距離也近了許多。他很感謝司晨給自己的建議，也很感謝宇桓給自己激將了一番……當然，更是感謝那個「Code/140.136」給了自己重來一次的機會，不然這輩子想要和曉光再次有接觸，幾乎是不太可能了吧。"+"\n"+"日翔和司晨剛剛結束了今天的最後一堂課，正要離開校園。"+"\n"+"「欸、欸、糟糕、阿日！」走往捷運站的路上，司晨突然毫無預警地慘叫了一聲，成功引來了周圍所有人的注目禮。"+"\n"+"日翔感到有些尷尬，但見到司晨的臉色慘白，還是有些感到緊張：「怎麼了？」"+"\n"+"仔細一看，司晨似乎正在一邊翻找自己的書包跟錢包，焦急得不行：「我的學生證不見了，怎麼辦！我以後要怎麼回家啊嗚嗚嗚嗚……」"+"\n"+"「唉。我跟你說，學生證要是找不到的話，其實……」"))
                list_talk.append(TextSendMessage(text="#58 請問學生如果學生有學務上的問題該去哪裏處理？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="57":
                list_talk=[]
                list_talk.append(TextSendMessage(text="兩人就這樣慢悠悠地逛了幾乎整個賣場，曉光很中意大鯊鯊玩偶「BLÅHAJ」於是抱了一隻，日翔也打算買一隻，便也拿在手上。"+"\n"+"當然，手也還是牽得緊緊的。他們似乎是已經習慣了對方手心的溫度，更或者是有了什麼不約而同的默契，誰都不願意放開手；手心的溫度，讓曉光想起來，這不是第一次牽起異性的手，而是在幼兒園時期，也是跟他一起，沒錯，跟日翔一起。"+"\n"+"「那個……」想起來這段過往的曉光，試圖開口詢問。"+"\n"+"沒想到跟日翔同時開了口，曉光對這個意料之外的默契感到有些驚訝。而一旁的日翔似乎也嚇到了，曉光連忙回應：「沒事、你先講。」"+"\n"+"「我有一件很重要的事情要問你。」似乎是因為接下來要談的事情藏在心中很久了，日翔的語氣變得鄭重了起來。"+"\n"+"「……我剛剛也想起來了。」曉光連日翔的問題都不必聽，因為她已經知道日翔想要說什麼，曉光露出了淺淺的微笑。"+"\n"+"「曉光，難道妳是說……妳也跟我一樣想起了那個約定？」日翔看著她的笑臉，似乎也知道了曉光究竟要講些什麼。"+"\n"+"或許是因為回憶起了相同的景物，日翔跟曉光格外地有著對話的默契，不用把話說得清楚就可以了解對方想表達的東西。"+"\n"+"「嗯，那個人就是你。」曉光的語氣少見地篤定。"+"\n"+"「沒想到我們到現在才真正地相認啊……對不起，我應該要早些想起來的。」日翔的和曉光道歉。"+"\n"+"曉光搖搖頭讓日翔不要道歉。曉光其實想問日翔搬家後過得好不好、想跟日翔說她想起了盒子裡所有跟他有關的回憶、想告訴日翔她終於又見到他了、想告訴日翔要是自己能早點想起來就好了……可曉光最後還是說不出口，她有太多太多話想跟日翔說。"+"\n"+"突然，有個熟悉的聲音打破了兩人的對話：「哇X！真假！！！！」"+"\n"+"兩人轉頭一看，竟然發現司晨躲在柱子後面，或許是因為聽到了他們的對話，驚訝的叫出聲來。"+"\n"+"「白癡，司晨你太大聲了！！」接著，日翔和曉光聽到了另一個熟悉的聲音對著司晨進行告誡。"+"\n"+"兩人毅然決然往聲音的方向走近，當然是看見了露出尷尬神情的司晨跟真澄。"))
                list_talk.append(TextSendMessage(text="或許是因為感到害臊，日翔和曉光的手已經放開來了，曉光的雙手緊緊抱著鯊鯊一語不發，似乎是對於被兩個朋友「關切」（雖然很明顯這只是單純的跟蹤而不是關切）而有些難為情的緣故。"+"\n"+"「就是，實在是太擔心了才來看看啊，阿日你前陣子不還是很猶豫不決嗎？」司晨好像沒有對偷窺兩人約會表達歉意的意思，至少依他的神情看來，應該是真的很擔心摯友的狀況。"+"\n"+"「是這樣沒錯……」日翔看起來相當無奈。"+"\n"+"「今天也是我的生日，有人搶了我跟曉光相處的好時光才過來關心一下。」真澄跟著解釋了自己的動機，但不知為何日翔總感覺她似乎不打算澄清什麼。"+"\n"+"「等等，不是我的錯吧！」日翔忍不住對真澄吐槽。"+"\n"+"「噗、好意外，真澄跟司晨居然都跟過來了。」終於平復心情的曉光笑了出來。"+"\n"+"而原先日翔跟曉光兩人預定的午餐時刻自然是演變成了四個人一起在瑞典餐廳吃飯，日翔表示他要順便請客慶祝一下現場兩位女生的生日。"+"\n"+"今天真的很開心。想起了以前的種種回憶，買到了喜歡的鯊魚布偶，也吃到IKEA的香草冰淇淋。不過面對司晨瘋狂催促和曉光快點交往的事情，又是另一個故事了。"))
                list_talk.append(TextSendMessage(text="眼看專題發表的時間將近，曉光先把其他想法拋在腦後，想要努力打好這場仗。"+"\n"+"「糟糕，差點就忘記這件事。」曉光敲了敲自己的腦袋。"+"\n"+"最近發生太多事情，著實的讓小光感受到充實的大學生活，比起第一次度過的大學生活來說，還來的忙碌許多，但曉光卻十分感謝「Code/140.136」給了自己重來一次的機會，不然這輩子想要和日翔再次有接觸，幾乎是不可能。"+"\n"+"剛下課的曉光，決定趕快去辦理獎學金。"))
                list_talk.append(TextSendMessage(text="#58 請問學生如果學生有學務上的問題該去哪裏處理？（請以「ＯＯ樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #58答案
    elif event.message.text=="野聲樓":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            list.append('B'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="57":
                worksheet.update(list[1],int(58))
                worksheet.update(list[2],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖野聲樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="「原來是這樣……阿日你對學校真的很熟欸，像我都不知道野聲樓在幹嘛。」司晨一邊翻找錢包的動作緩了下來，似乎是鬆了一口氣。"+"\n"+"哈哈，我猜你甚至不知道野聲樓的聲不是野生的「生」，而是聲音的「聲」……日翔內心默默吐槽自己的朋友。"))
                list_talk.append(TextSendMessage(text="「資管系ＸＸ周年運動會」的公告一發布在班群，司晨就馬上興奮地告知坐在隔壁的日翔。沒想到專題發表在即，居然還會有系上的活動！日翔心想，幸好小組的專題已經準備得差不多了，多參加個師生運動會絕對是綽綽有餘的，他想趁著這次機會，再多多表現自己在籃球場上馳騁的英姿。"+"\n"+"據說這次的師生運動會在中美堂舉辦，那應該不會再有大一時司晨發生的窘況——為了耍帥反而摔了一跤了吧。"+"\n"+"「這次我不會搶你風頭，一旦有給你表現的就交給你啊！給曉光看看你帥氣的樣子！」司晨搭上了日翔的肩膀，好像在往他身上加持一些勇氣。"+"\n"+"「哇靠……阿司，你這麼講義氣真好。」日翔想到以前的司晨也是這麼挺朋友，突然發自內心地感嘆有這位朋友真好。"+"\n"+"不過，司晨本人倒是很快就因為這樣的讚賞得意了起來：「哎？嘿嘿，謝謝誇獎。反之，你要好好表現啊，不要辜負我給你的機會！」"+"\n"+"日翔是很習慣他的反應了，拍拍他的肩膀笑道：「哈哈，當然啦。」"+"\n"+"這時，坐在前頭的曉光回過頭來詢問：「你們在聊資管系的師生運動會嗎？」"+"\n"+"「對啊，之後的籃球比賽你會來看嗎？」日翔順勢向她提出了邀請。他發現，自從那次發現彼此就是對方的兒時玩伴之後，曉光就變得比以往更加開朗了起來。"+"\n"+"「嗯。我想去幫你加油。」曉光笑著回應。"+"\n"+"「好期待那天的到來啊！」司晨看著好哥們跟喜歡的女生互動也不禁動容了起來。他心想，說不定他也有機會在師生運動會找到一個喜歡的小仙女呢？"))
                list_talk.append(TextSendMessage(text="#59 輔大資管系學會想要租借中美堂場地舉辦師生運動會，請問應該到哪個單位租借場地呢？"+"\n"+"（Ａ）心園"+"\n"+"（Ｂ）宜真宜善學苑"+"\n"+"（Ｃ）舊醫學大樓一樓右側"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#59',
                    template=ButtonsTemplate(
                        title='#59',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="心園"
                            ),
                            MessageAction(
                                label='B',
                                text="宜真宜善學苑"
                            ),
                            MessageAction(
                                label='C',
                                text="舊醫學大樓一樓右側"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="57":
                worksheet.update(list[1],int(58))
                worksheet.update(list[2],int(8))
                list_talk=[]
                list_talk.append(TextSendMessage(text="解鎖野聲樓！趕快去「遊戲地圖」看看！"))
                list_talk.append(TextSendMessage(text="「資管系ＸＸ周年運動會」的公告一發布在班群，司晨就馬上興奮地告知坐在隔壁的日翔。"+"\n"+"而坐在他們兩人前面的曉光，聽得見他們兩人的對話。"+"\n"+"「這次我不會搶你風頭，一旦有給你表現的就交給你啊！給曉光看看你帥氣的樣子！」司晨搭上了日翔的肩膀，好像在往他身上加持一些勇氣。"+"\n"+"「哇靠……阿司，你這麼講義氣真好。」"+"\n"+"「哎？嘿嘿，謝謝誇獎。反之，你要好好表現啊，不要辜負我給你的機會！」司晨本人倒是很快就因為這樣的讚賞得意了起來。"+"\n"+"「哈哈，當然啦。」日翔是很習慣他的反應了，拍拍他的肩膀笑道。"))
                list_talk.append(TextSendMessage(text="「你們在聊資管系的師生運動會嗎？」 聽到自己名字被提起的曉光，回過頭來詢問。"+"\n"+"「對啊，之後的籃球比賽你會來看嗎？」日翔順勢向她提出了邀請。"+"\n"+"「嗯。我想去幫你加油。」曉光笑著回應，自從那次發現彼此就是對方的兒時玩伴之後，曉光就變得比以往更加開朗了起來。"+"\n"+"「好期待那天的到來啊！說不定他也有機會在師生運動會找到一個喜歡的小仙女呢？」司晨看著好哥們跟喜歡的女生互動也不禁動容了起來。"))
                list_talk.append(TextSendMessage(text="#59 輔大資管系學會想要租借中美堂場地舉辦師生運動會，請問應該到哪個單位租借場地呢？"+"\n"+"（Ａ）心園"+"\n"+"（Ｂ）宜真宜善學苑"+"\n"+"（Ｃ）舊醫學大樓一樓右側"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#59',
                    template=ButtonsTemplate(
                        title='#59',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="心園"
                            ),
                            MessageAction(
                                label='B',
                                text="宜真宜善學苑"
                            ),
                            MessageAction(
                                label='C',
                                text="舊醫學大樓一樓右側"
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

    #59答案
    elif event.message.text=="舊醫學大樓一樓右側":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="58":
                worksheet.update(list[1],int(59))
                list_talk=[]
                list_talk.append(TextSendMessage(text="專題發表的時刻終於到了！五人組對於這次的專題內容十分有信心。但信心歸信心，發表時刻終究還是有所考驗的。趕緊動用所學，度過專題大魔王吧！"+"\n"+"日翔已經決定好結束這次專題就要向曉光表達心意了，可不能在這個時候漏氣呀。"))
                list_talk.append(TextSendMessage(text="#60 CPU排班演算法中，效能最佳的是？"+"\n"+"（Ａ）FIFO法則"+"\n"+"（Ｂ）SJF法則"+"\n"+"（Ｃ）RR法則"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#60',
                    template=ButtonsTemplate(
                        title='#60',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="FIFO法則"
                            ),
                            MessageAction(
                                label='B',
                                text="SJF法則"
                            ),
                            MessageAction(
                                label='C',
                                text="RR法則"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="58":
                worksheet.update(list[1],int(59))
                list_talk=[]
                list_talk.append(TextSendMessage(text="專題發表的時刻終於到了！五人組對於這次的專題內容十分有信心。但信心歸信心，發表時刻終究還是有所考驗的。趕緊動用所學，度過專題大魔王吧！"))
                list_talk.append(TextSendMessage(text="#60 CPU排班演算法中，效能最佳的是？"+"\n"+"（Ａ）FIFO法則"+"\n"+"（Ｂ）SJF法則"+"\n"+"（Ｃ）RR法則"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#60',
                    template=ButtonsTemplate(
                        title='#60',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="FIFO法則"
                            ),
                            MessageAction(
                                label='B',
                                text="SJF法則"
                            ),
                            MessageAction(
                                label='C',
                                text="RR法則"
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

    #60答案
    elif event.message.text=="SJF法則":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="59":
                worksheet.update(list[1],int(60))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#61 某IP採用IPv4，且網路為占24bit，請問可用的主機數量有多少？（請以「Ｏ」回答，Ｏ數量不代表正確答案字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="59":
                worksheet.update(list[1],int(60))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#61 某IP採用IPv4，且網路為占24bit，請問可用的主機數量有多少？（請以「Ｏ」回答，Ｏ數量不代表正確答案字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #61答案
    elif event.message.text=="254":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="60":
                worksheet.update(list[1],int(61))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#62 IPv6採用多少位元來表示IP位置？"+"\n"+"（Ａ）32"+"\n"+"（Ｂ）64"+"\n"+"（Ｃ）128"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#62',
                    template=ButtonsTemplate(
                        title='#62',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="32"
                            ),
                            MessageAction(
                                label='B',
                                text="64"
                            ),
                            MessageAction(
                                label='C',
                                text="128"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="60":
                worksheet.update(list[1],int(61))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#62 IPv6採用多少位元來表示IP位置？"+"\n"+"（Ａ）32"+"\n"+"（Ｂ）64"+"\n"+"（Ｃ）128"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#62',
                    template=ButtonsTemplate(
                        title='#62',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="32"
                            ),
                            MessageAction(
                                label='B',
                                text="64"
                            ),
                            MessageAction(
                                label='C',
                                text="128"
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

    #62答案
    elif event.message.text=="128":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="61":
                worksheet.update(list[1],int(62))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#63 網頁資料URL的英文全名是？"+"\n"+"（Ａ）Uniform Resource Locator"+"\n"+"（Ｂ）Used Return Link"+"\n"+"（Ｃ）Unknow Rank Location"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#63',
                    template=ButtonsTemplate(
                        title='#63',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="Uniform Resource Locator"
                            ),
                            MessageAction(
                                label='B',
                                text="Used Return Link"
                            ),
                            MessageAction(
                                label='C',
                                text="Unknow Rank Location"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="61":
                worksheet.update(list[1],int(62))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#63 網頁資料URL的英文全名是？"+"\n"+"（Ａ）Uniform Resource Locator"+"\n"+"（Ｂ）Used Return Link"+"\n"+"（Ｃ）Unknow Rank Location"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#63',
                    template=ButtonsTemplate(
                        title='#63',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="Uniform Resource Locator"
                            ),
                            MessageAction(
                                label='B',
                                text="Used Return Link"
                            ),
                            MessageAction(
                                label='C',
                                text="Unknow Rank Location"
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

    #63答案
    elif event.message.text=="Uniform Resource Locator":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="62":
                worksheet.update(list[1],int(63))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#64 有一二進位數1100 1101 0011，轉十進位是？（請以「Ｏ」回答，Ｏ數量不代表正確答案字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="62":
                worksheet.update(list[1],int(63))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#64 有一二進位數1100 1101 0011，轉十進位是？（請以「Ｏ」回答，Ｏ數量不代表正確答案字數。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #64答案
    elif event.message.text=="3283":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            list.append('C'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="63":
                worksheet.update(list[1],int(64))
                worksheet.update(list[2],int(10))
                list_talk=[]
                list_talk.append(TextSendMessage(text="呼——日翔長吐了一口氣，他面對著手機，在七夕的前一天對著手機螢幕敲敲打打，他打算在七夕的零時零分準時送出對曉光的告白。雖然總感覺只是以訊息來告白似乎太不盛大了，可日翔卻心想，他總該給自己一些退路……要是曉光拒絕自己呢？那就真的太尷尬了。"+"\n"+"「曉光，關於這件事我想了很久。打從大一看到妳的時候，我就因為妳出眾的外貌而對妳抱持著好印象，也因為妳聰明伶俐對你產生了好感，妳偶爾顯出笨拙的那一面也顯得可愛，總是令我的心產生悸動。」"+"\n"+"嗚哇，感覺有點肉麻……看著由自己撰寫出的一字一句，日翔的臉都不自覺地發燙了起來，可他沒有打算要進行更多的修飾，只是坦然地與曉光分享那個真正的自己。他繼續寫下：「我想或許不只是大一吧，我的心意從很久很久以前，從我們尚未了解所謂的『喜歡』就開始發芽了。只不過我竟然忘記了在搬家前與妳共處的美好時光——若不是我們之間再次產生了交集，或許我一輩子都沒有機會和妳相認、或和妳並肩而行了。」"+"\n"+"日翔話中的意思是，要是沒有「code/140.136」送我回到了大一，我在大學生活與妳的牽連就單單僅有同班而已，而畢業後就會面臨永遠的分道揚鑣。這些話日翔沒有打出來，畢竟他也不知道該怎麼解釋這不科學的事情。"+"\n"+"最後，他以一句真摯的邀請收尾：「妳願意讓我以新的身分進行彌補嗎？」"+"\n"+"最後，在日期更替的那一刻，日翔跟曉光的關係如日翔所願地發生了好的改變。"+"\n"+"不知為何，在看到曉光的回覆後，日翔的眼眶有些發熱。"+"\n\n"+"解鎖信紙！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="解鎖大四劇情"+"\n\n"+"日翔喜歡貓是從小時候開始的。還記得在尚未搬家的時候，幼小的他就曾經在路邊救過一隻虛弱的小野貓。日翔的印象頗為深刻，那是一個下課後的傍晚，他跟媽媽一起在一棵大樹旁發現了一隻虛弱瘦小的灰色幼貓。"+"\n"+"「哇，媽媽……他好像很虛弱的樣子。」小日翔蹲在歸家的路上看著倒在路上的小傢伙，很是擔憂的樣子。畢竟這可是實實在在的一個小生命，再怎麼說，日翔也無法接受就這樣忽視牠就離開現場。"+"\n"+"而日翔的媽媽也見到了這一幕，她馬上就想到了一個好主意，便向自己的孩子提議：「日翔，我們把他送到獸醫去吧。」"+"\n"+"做這樣的決定的原因有二：一來是這對孩子也是一個生命教育的機會，二來是她也並不想眼睜睜看著小貓受苦。"+"\n"+"在動物醫院裡，醫生很有耐心地替小貓進行檢查。確認沒有外傷且後，便先跟日翔媽媽說好這隻流浪貓支付的費用醫院並不會幫忙給付。而日翔媽媽趁勢告訴日翔，流浪動物沒有跟人類依樣的健保，而醫生的檢查用品也都要花不少錢，動物醫院自然沒有辦法做自行吸收成本的免費服務。要是在路邊看到受傷的小動物卻沒有錢，是不能貿然送到動物醫院的。"+"\n"+"日翔媽媽同意支付費用後，醫生判斷這隻小貓似乎只是餓昏了而已，於是醫生便選擇幫忙補充營養，並在兩人離開醫院之前告知兩人這隻貓很可能是跟媽媽走散了。如果沒有打算要飼養的話，原地放生的存活率也不高。"+"\n"+"於是，這個小傢伙便在日翔家待了一段時間，畢竟家裡沒有預計要養貓，所以日翔的媽媽是一邊詢問有沒有好友可以收留，一邊照顧小貓的。"+"\n"+"自然，有愛心的日翔也出了不少心力，所以日漸恢復的小貓也與他很是親密，只要日翔一回家，小貓便會反常地像狗狗一樣，主動迎接這位拯救了自己的孩子。不過，這樣的日子並不長，小貓僅是在這裡居住了一個禮拜，就因為日翔媽媽找到可以收養的中途之家而離開了家中。"))
                list_talk.append(TextSendMessage(text="開學的前一天下午，日翔跟曉光兩個人坐在新莊運動公園的草地上談天：「有沒有可能，妳家的德魯貝就是我以前養過的小貓啊？牠剛好也是灰色的耶。」"+"\n"+"日翔開口完便想到之前去曉光家的時候抱著德魯貝的重量，和小時候遇到的貓完全是兩回事，想了想便開始吐槽自己剛剛說的話：「哈哈，可是德魯貝這麼胖，應該不可能吧？」"+"\n"+"確實除了毛色以外，無論身形還是大小都無法對小時候那隻貓跟德魯貝進行聯想……可惜日翔並沒有給他的小貓拍照，他也並沒有問媽媽那隻貓最後怎麼樣了。"+"\n"+"「哎、德魯貝只是毛蓬鬆了一點，而且又不愛運動……唔，好像真的有點胖……」曉光本來似乎想認真地反駁，但後來又越說越小聲。"+"\n"+"「我們可以幫牠制定一個減重計畫呀。」德魯貝好像是曉光小學的時候領養的，年紀也真的不小了……日翔想到德魯貝的健康問題，對此進行了提議。"+"\n"+"「說得也是……要不先從減少零食開始好了。」"+"\n"+"日翔和曉光的交往也過了兩三個月的時間，兩個人早就熟悉了起來，日翔可以感覺到曉光和自己的關係日漸親密，這對他而言是一件很幸福的事情——彼此之間雖然還是很慢熱，但直到今天也已經是無話不談的程度了。"))
                list_talk.append(TextSendMessage(text="日翔睜開雙眼，只見自己竟然置身於一團迷霧之中……等等，又是這個謎霧？日翔很快地就回憶起了兩年前也進入過這個夢境！無庸置疑，這絕對是那個「Code/140.136」所製造的。"+"\n"+"「『藉著對知識真理的追求，修德行善的用心，欣賞宇宙萬物之美，以體會人生至聖之境』。……日翔你果然做得比我想像中的更加優秀啊——哎唷唷唷，真不愧是我看中的人。」似乎是發現日翔已經意識到這裡是什麼地方，那神秘的個體便逕自跟日翔搭話。"+"\n"+"不知道為什麼，總覺得第一段話聽起來跟背誦課文一樣平淡又毫無感情，而且那段話似乎就是輔大「真善美聖」的校訓……突然講這個要幹嘛？日翔總覺得，每次進來這個空間都會聽到一些莫名其妙的話。"+"\n"+"「大學生活已經快要結束了吧，你還是不能告訴我為什麼要帶我到過去嗎？」不如再問他一次看看吧。日翔乾脆豁出去了。"+"\n"+"「你很快就會知道啦。日翔你已經越來越接近真相囉，太棒了！」他似乎又不打算正面回應。但可以知道的是應該有接觸到真相的那一天，這句話總歸還是有點資訊量的……日翔心想。"+"\n"+"「你是在棒什麼啦……」日翔面對這奇怪的個體，再次壓抑不住內心的吐槽魂。"+"\n"+"「這還用說嗎？因為我們是互惠互利的關係嘛……接下來你只要好好期待就好……」迷霧的聲音逐漸模糊，整個空間也逐漸不穩了起來。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=ButtonsTemplate(
                        title='？？',
                        text='你該不會又要擅自離開了吧……',
                        actions=[
                            MessageAction(
                                label='？？',
                                text='你該不會又要擅自離開了吧……'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="63":
                worksheet.update(list[1],int(64))
                worksheet.update(list[2],int(10))
                list_talk=[]
                list_talk.append(TextSendMessage(text="明日就是七夕了，而七夕前一晚的曉光，剛洗完澡頭髮仍濕淋淋的，穿著粉色貓咪圖案的睡衣，肩上還掛著毛巾。曉光到冰箱拿了一瓶沁涼的果汁牛奶，還有一個小紅豆麵包，準備好好享用。"+"\n"+"此時，曉光的手機收到了一則訊息。"+"\n"+"「是誰啊？這麼晚了。」曉光打開手機，目光停留在寄件人的名字。「日翔？怎麼了嗎？」"+"\n"+"曉光點開日翔的訊息，上面寫著：「曉光，關於這件事我想了很久。打從大一看到妳的時候，我就因為妳出眾的外貌而對妳抱持著好印象…」"+"\n"+"看到一半的曉光，瞬間明白這封信的目的。"+"\n"+"是…情書？！曉光驚呼了一聲，她能感受到手正在顫抖，心跳加速。曉光緊張地拿起最近買的IKEA鯊魚，緊緊抱在懷裡。"+"\n"+"曉光內心激動不已，遲遲不敢往下看訊息。而正當曉光猶豫該怎麼辦時，身邊的德魯貝突然慵懶地叫了一聲。"+"\n"+"「德魯貝，你在幫我加油嗎？」 曉光摸了一下德魯貝。"+"\n"+"「喵嗚。」不曉得是聽得懂人話的德魯貝，還是剛好只是又想發出叫聲。"+"\n"+"「嗯，我會把它看完。」曉光把懷裡的鯊魚放在沙發上，拿起剛剛放在桌上的手機，做了個深呼吸。"+"\n"+"後來，曉光一字不漏的將這些字看完了，又再度吸了一口氣，把手機放在一旁，將已經不那麼冰涼的果汁和麵包握在手上。不同於剛剛的曉光，心情很快就平復下來，開始思考要怎麼回應日翔的「告白」。"+"\n"+"曉光回想起從認識日翔的那刻，無論曉光面對任何困難，日翔總是一直幫助曉光，在曉光最寂寞的時候，也一直陪伴著曉光，而臉上的笑容總能融化曉光冰冷的外在。曉光很感激日翔的所做所為，也覺得日翔是個貼心、溫柔善良的男孩子。"+"\n"+"而如今又回到大學生活，想起以前的回憶，也不斷受到日翔的照顧，曉光認為是時候該回覆日翔的心意了。"+"\n"+"曉光把手上的果汁和麵包飲用完，收拾一下，打開了手機，開始慢慢的按下手機上的按鍵。"+"\n\n"+"「謝謝你，日翔，你的心意我確實收到了。一直以來受到你的幫忙，不論是小時候，你陪伴了常常一個人，感到寂寞的我，帶著我到處去遊玩。我一直都記得。還有一次你帶著我去吃冰淇淋，我的臉上沾到冰淇淋了，你拿出手帕幫我擦拭嘴角，我很喜歡你這些貼心的舉動。"+"\n"+"直到現在大學了，你依舊在一旁默默的幫助我，剛開學的時候你撿起我的學生證，臉上的笑容，如同你的名字，像太陽一樣溫暖我的心。不過還是像以前一樣，對課業不太擅長呢，但是從大一到現在的你，已經進步了很多了喔。還有一起吃著鬆餅、冰淇淋的時候，真的很快樂。到現在大三開始做專題，你在吃貓餐廳遞給我毛巾好讓我擦拭身體，在圖書館幫我拿書本，我也都記得。而最近我們一起去IKEA，你牽起我的手，當時我的心跳真的跳得好快。"+"\n"+"不知道該怎麼答謝你，也很感謝你對我做的這些。"+"\n"+"如果不嫌棄的話，希望你可以一直在我身邊。"+"\n"+"我答應你。」"+"\n\n"+"曉光重頭看了一次自己寫的字，確定都沒問題以後，按下發送。"+"\n"+"轉眼間，這個輪迴的大學生活即將邁入最後一年，曉光不禁感嘆時光飛逝。"+"\n"+"原本一片混亂的腦袋，似乎找到了自己的地圖，原本被迷霧壟罩的路程，隨著一道曙光開闢了道路，曉光已經不再對未來感到迷惘。"+"\n"+"「但，究竟是誰呢？」還是不理解是什麼人大費周章讓她回顧一次大學生活，也不清楚這樣能帶給那個人什麼好處。"+"\n"+"不過，曉光仍然想再見那個人一次面，想當面向他道謝。"+"\n"+"「感謝您帶我回來。」曉光面對家中的窗外，雙手合十道謝以後，隨即轉身回到房間裡。"+"\n"+"而正當曉光轉身的瞬間，夜幕中再度劃過一顆流星。"+"\n\n"+"解鎖信紙！趕快去「個人檔案」看看！"))
                list_talk.append(TextSendMessage(text="家貓德魯貝是在小學的時候，曉光從貓咪中途之家收養而來的。當時，年幼的曉光與母親相依為命，母親又常常因為工作的關係會晚回家，因此曉光常常一個人在家裡。"+"\n"+"為了不讓曉光感到寂寞，也知道曉光喜歡動物，於是有一天…"+"\n"+"「曉光，明天媽媽帶你去一個地方好不好？」"+"\n"+"很久沒跟媽媽出門玩的曉光，聽到媽媽這麼說，高興的猛點頭。"+"\n"+"「那太好了，你要好好期待喔。」母親摸了摸曉光的頭，臉上帶著慈祥的笑容。"+"\n"+"隔一天，曉光和媽媽到了貓咪中途之家，裡面有很多曉光最喜歡的貓咪。"+"\n"+"「媽媽你看，有好多貓咪喔。」曉光拉著母親的衣角，興奮的說著。"+"\n"+"「曉光，你很喜歡貓咪對吧？」"+"\n"+"「對呀！特別是這一隻，小小的好可愛。」曉光手指著玻璃櫥櫃後面一隻灰色小貓。"+"\n"+"「這隻貓咪之前被一個家庭餵養了一個禮拜，有帶給獸醫檢查過，健康方面都什麼問題，如果你們喜歡的話，可以領養牠喔。」中途之家的人員告訴曉光母女。"+"\n"+"「欸…這樣啊，那曉光你覺得呢？」母親問道。"+"\n"+"「真的嗎媽媽？這隻貓咪會跟我們一起回家嗎？」曉光看著母親的雙眼。"+"\n"+"「是真的喔，那我們就帶這隻貓咪回家吧。」嘴角微微上揚、眼睛瞇成上弦月的母親，是曉光最喜歡的笑容。"+"\n"+"於是曉光和母親帶著這隻灰色貓咪回家，並取名為德魯貝，而德魯貝的名字由來，是出自於曉光最喜歡的卡通「月光美少女戰士」裡面，女主角飼養的貓咪的名字。"+"\n"+"自從那天以後，受到天皇等級般照顧的德魯貝，與曉光感情密切，形影不離。"))
                list_talk.append(TextSendMessage(text="開學的前一天下午，日翔跟曉光兩個人坐在新莊運動公園的草地上談天：「有沒有可能，妳家的德魯貝就是我以前養過的小貓啊？牠剛好也是灰色的耶。」"+"\n"+"對了，日翔之前說過家裡有養過貓。"+"\n"+"「哈哈，可是德魯貝這麼胖，應該不可能吧？」日翔摸摸頭笑了笑。"+"\n"+"「哎、德魯貝只是毛蓬鬆了一點，而且又不愛運動……唔，好像真的有點胖……」曉光本來似乎想認真地反駁，但後來又越說越小聲。"+"\n"+"「我們可以幫牠制定一個減重計畫呀。」日翔想到德魯貝的健康問題，對此進行了提議。"+"\n"+"「說得也是……要不先從減少零食開始好了。」曉光附和道。"+"\n"+"日翔和曉光的交往也過了兩三個月的時間，兩個人早就熟悉了起來，日翔可以感覺到曉光和自己的關係日漸親密，這對他而言是一件很幸福的事情——彼此之間雖然還是很慢熱，但直到今天也已經是無話不談的程度了。"))
                list_talk.append(TextSendMessage(text="曉光睜開雙眼，突然就被一道刺眼的光芒照射著……又是這道光？曉光很快地就回憶起了兩年前也看過這道光！無庸置疑，這絕對是那個「Code/140.136」所製造的。"+"\n"+"「『藉著對知識真理的追求，修德行善的用心，欣賞宇宙萬物之美，以體會人生至聖之境』。……曉光你果然做得比我想像中的更加優秀啊——哎唷唷唷，真不愧是我看中的人。」似乎是發現曉光已經意識到這裡是什麼地方，那神秘的個體便逕自曉光搭話。"+"\n"+"曉光總看不透聲音的主人內心所想，突然講起輔大「真善美聖」的校訓想告訴她什麼呢？且曉光對於他口中所說「看中的人」也十分在意。"+"\n"+"「……大學生活也快結束了，你還是不願告訴我你的身分嗎？」曉光詢問道。"+"\n"+"「妳很快就會知道啦，曉光妳已經越來越接近真相囉！」聲音告訴曉光，果然從他口中直接套出真相的機率是微乎其微，不過曉光還是從這句話裡得知了一定的資訊。"+"\n"+"「唔……也就是說，總有一天你會告訴我真相嗎？」曉光再次向聲音問道。"+"\n"+"「接下來你只要好好期待就好……」聲音仍不打算交代清楚，隨著聲音聽起來越來越模糊，曉光知道他又要離開了，可是她還有很多問題想問……"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='？？',
                    template=ButtonsTemplate(
                        title='？？',
                        text='等、等等……',
                        actions=[
                            MessageAction(
                                label='？？',
                                text='等、等等……'
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
    
    #64答案
    elif event.message.text=="你該不會又要擅自離開了吧……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="64":
                list_talk=[]
                list_talk.append(TextSendMessage(text="待到日翔恢復意識時，又是躺回了柔軟的床上。那傢伙果然跟上次一樣，擅自進入人家夢境又擅自離開了。他今天倒不是被鬧鐘所叫醒，因為已經大四的日翔安排的課程不多，今天也只有下午有一堂必修課而已。"+"\n"+"看來對話又莫名其妙結束了嗎，算了，至少有從那傢伙身上獲得一些消息……日翔迅速地從床上坐起，深刻地思考道。"+"\n"+"雖然是知道了終會有抵達真實的一天，但所謂的「互惠互利」或者「接近真相」，日翔還是一點頭緒都沒有……"))
                list_talk.append(TextSendMessage(text="「……你現在都沒有去考多益？真的假的？」一進教室，日翔便聽到宇桓震驚又帶點責備意味的聲音。"+"\n"+"司晨好像沒有注意到對方傻眼的語氣，他像是閒聊一樣輕鬆地接話：「對啊對啊，所以我要參加管院的自學方案……聽說跟高中一樣會考雜誌，希望不會太難。」"+"\n"+"早已通過多益畢業門檻的真澄嘆氣：「唉，幸好管院有規劃自學方案，你才可以有準時畢業的機會。」"+"\n"+"「我上上學期多益也考過門檻了，阿司你要加油啊。」日翔一邊往眾人的方向走去一邊揮揮手，真澄等人看到日翔進教室，便也揮手和他打招呼。"+"\n"+"「什、什麼！你原來通過了嗎，阿日，你居然背著我偷偷來……」司晨的語氣像是朋友背叛了自己一樣悽慘。"+"\n"+"「你不要說這麼招人誤會的話啦！」什麼背著你偷偷來，我又沒有做什麼不該做的事情，也沒有背叛自己的兄弟啊……日翔感到好笑，無奈的心想。"+"\n"+"司晨頭垂了下來對日翔進行了一番解釋，語氣中帶了點難過：「因為我真的沒想到阿日會去考多益啊！！還以為你會跟我一起參加自學方案……」"))
                list_talk.append(TextSendMessage(text="#65 請問本系英文畢業門檻多益成績為多少分以上？（請以「Ｏ分」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #64答案
    elif event.message.text=="等、等等……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="64":
                list_talk=[]
                list_talk.append(TextSendMessage(text="待到曉光恢復意識時，和之前一樣躺在柔軟的床上。那道光無論是出現還是消失，都毫無徵兆，彷彿擁有自己的意志。曉光在床邊坐著，思考著剛剛的對話。"+"\n"+"「至少知道一點線索了。」曉光增加了信心，她握緊了自己的手掌心放在胸前。"))
                list_talk.append(TextSendMessage(text="「我昨天收到多益的通知書了！一次就考過了！」真澄將手機裡的多益證書秀給大家看，「大三為了寫專題少修了一點課，還好我們做得很快才有時間念多益。」"+"\n"+"「真澄，恭喜妳。」曉光說，宇桓也點點頭表示祝賀。"+"\n"+"「哎、你們都考過啦？我都還沒考呢！」司晨驚訝地說。"+"\n"+"「……你現在都沒有去考多益？真的假的？」宇桓大聲地說，在教室內引起一些人的注目。"+"\n"+"「對啊對啊，所以我要參加管院的自學方案……聽說跟高中一樣會考雜誌，希望不會太難。」司晨好像沒有注意到對方傻眼的語氣，他像是閒聊一樣輕鬆地接話。"+"\n"+"「唉，幸好管院有規劃自學方案，你才可以有準時畢業的機會。」早已通過多益畢業門檻的真澄嘆氣。"+"\n"+"「我上上學期多益也考過門檻了，阿司你要加油啊。」晚來的日翔似乎也在教室外聽見了宇桓的驚呼，一進教室就加入了多益的話題。"+"\n"+"「什、什麼！你原來通過了嗎，阿日，你居然背著我偷偷來……」司晨的語氣像是朋友背叛了自己一樣悽慘。"+"\n"+"「你不要說這麼招人誤會的話啦！」"+"\n"+"「因為我真的沒想到阿日會去考多益啊！！還以為你會跟我一起參加自學方案……」司晨頭垂了下來對日翔進行了一番解釋，語氣中帶了點難過。"))
                list_talk.append(TextSendMessage(text="#65 請問本系英文畢業門檻多益成績為多少分以上？（請以「Ｏ分」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #65答案
    elif event.message.text=="750分":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="64":
                worksheet.update(list[1],int(65))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「沒事啦阿司，你一定可以度過的。」知道司晨實在不擅長英文，於是日翔還是拍拍司晨的肩膀表達安慰。"+"\n"+"宇桓看到他這麼難過，也只好跟著拉下臉安慰剛剛被自己大聲斥責的人：「畢竟你工讀也挺忙的，不能準備多益也並不是很意外。」"+"\n"+"輔大資管系不只有承認TOEIC750分以上這個標準，尚可以選擇考取iBT TOEFL成績71分以上、IELTS成績6.0以上或全民英檢中高級複試通過等等，這些測驗只要到達了標準都會承認通過英文畢業門檻。但如果沒有辦法通過這些門檻，管院也有為大四生準備8次英語自學方案的測驗，顧及英文程度比較差的同學，而這些測驗的內容跟時間都會公告在自學方案的粉絲專頁。"))
                list_talk.append(TextSendMessage(text="開學已經過了數周，日翔還是沒有什麼「接近真相」的感覺，他已經開始懷疑是不是要到畢業當天才能知道那個「Code/140.136」製作者的動機了。"+"\n"+"今天是星期二下午三點三十五分，日翔跟曉光坐在教室的一角等待上課時間的來臨。而曉光正在一邊準備她升學所需要的甄試資料，日翔比起以往的偷看，反倒是更加光明正大地注視著他的戀人。"+"\n"+"注意到隔壁的視線，曉光眼睛仍然盯著螢幕對筆電敲敲打打，一邊對身旁的人詢問：「怎麼了，日翔？」"+"\n"+"「沒事，只是覺得妳……嗯，果然是會考研的類型。」只是覺得妳認真起來的樣子我果然好喜歡……這種話好像還是太肉麻了，即使已經和曉光是交往關係，日翔還是對於內心話稍微難以啟齒。"+"\n"+"曉光似乎對日翔的反應不是太意外，便反過來詢問：「畢竟讀書還算是我的專長……唔、日翔以後不升學的話，是要參加產業實習？」"+"\n"+"日翔想到某個往年都有開實習名額夢想公司，便坦率地回答：「我想是這樣的吧……」"+"\n"+"畢竟再怎麼說，他還是想進福利好一點又可以發揮目前所學，還不會日以繼夜爆肝的夢想公司啊！"+"\n"+"「阿——日——午安安——呼、呼……」一個熟悉的人影不知是走還是爬的急急進了教室。"+"\n"+"「阿司，你怎麼這麼累？｣日翔再度看看時間，已經是三點三十九分了，上課時間都要到了，司晨才走進教室。"+"\n"+"「我剛剛，在進修部啦。」司晨一手撐著桌子，氣喘吁吁地回應。"+"\n"+"「上二外有點晚下課，想說、教授會點名就、趕著過來……電梯人太多搭不上……」二外指的是第二外語。在大一的英語必修過了之後，也可以在這個語言資源豐富的學校修習各式各樣的語言，提升自身的競爭力。"+"\n"+"「司晨，喝點水會比較好。」曉光看跑樓梯上來的司晨這麼喘，便關心了他一下。"+"\n"+"噹噹——噹——噹——聽見上課時間到了，司晨便趕緊坐在日翔和曉光的旁邊，然後開始對自己灌水。日翔看著他心裡便想，他這樣邊工讀邊忙課業也是真的很辛苦，不知道他的學分修得怎麼樣了……可自己又不能替他修學分，頂多也只能在課業上多多幫忙了。"))
                list_talk.append(TextSendMessage(text="#66 請問輔仁大學資訊管理系畢業所需的學分為何？（請以「Ｏ分」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="64":
                worksheet.update(list[1],int(65))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「沒事啦阿司，你一定可以度過的。」知道司晨實在不擅長英文，於是日翔還是拍拍司晨的肩膀表達安慰。"+"\n"+"「畢竟你工讀也挺忙的，不能準備多益也並不是很意外。」宇桓看到他這麼難過，也只好跟著拉下臉安慰剛剛被自己大聲斥責的人。"+"\n"+"輔大資管系不只有承認TOEIC750分以上這個標準，尚可以選擇考取iBT TOEFL成績71分以上、IELTS成績6.0以上或全民英檢中高級複試通過等等，這些測驗只要到達了標準都會承認通過英文畢業門檻。但如果沒有辦法通過這些門檻，管院也有為大四生準備8次英語自學方案的測驗，顧及英文程度比較差的同學，而這些測驗的內容跟時間都會公告在自學方案的粉絲專頁。"))
                list_talk.append(TextSendMessage(text="開學已經過了數周，那道光依舊還是沒有出現，曉光已經開始懷疑是不是要到畢業當天才能知道那個「Code/140.136」的真相。"+"\n"+"今天是星期二下午三點三十五分，日翔跟曉光坐在教室的一角等待上課時間的來臨，而曉光正在一邊準備她升學所需要的甄試資料的時候，突然發覺身旁的日翔正在看著他。"+"\n"+"「怎麼了，日翔？」注意到隔壁的視線，曉光眼睛仍然盯著螢幕對筆電敲敲打打，一邊對身旁的人詢問。"+"\n"+"「沒事，只是覺得妳……嗯，果然是會考研的類型。」日翔說。"+"\n"+"「畢竟讀書還算是我的專長……唔、日翔以後不升學的話，是要參加產業實習？」曉光詢問。"+"\n"+"「我想是這樣的吧……」日翔提起往年都有開實習名額夢想公司，便坦率地回答。"))
                list_talk.append(TextSendMessage(text="「阿——日——午安安——呼、呼……」一個熟悉的人影不知是走還是爬的急急進了教室，打斷兩個人的對話。"+"\n"+"「阿司，你怎麼這麼累？｣日翔再度看看時間，已經是三點三十九分了。"+"\n"+"「我剛剛，在進修部啦。」司晨一手撐著桌子，氣喘吁吁地回應。"+"\n"+"「上二外有點晚下課，想說、教授會點名就、趕著過來……電梯人太多搭不上……」二外指的是第二外語。在大一的英語必修過了之後，也可以在這個語言資源豐富的學校修習各式各樣的語言，提升自身的競爭力。"+"\n"+"「司晨，喝點水會比較好。」曉光看跑樓梯上來的司晨這麼喘，便關心了他一下。"+"\n"+"噹噹——噹——噹——聽見上課時間到了，司晨便趕緊坐在日翔和曉光的旁邊，然後開始對自己灌水。司晨邊工讀邊念書真辛苦，不知道他的學分修得怎麼樣了……"))
                list_talk.append(TextSendMessage(text="#66 請問輔仁大學資訊管理系畢業所需的學分為何？（請以「Ｏ分」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #66答案
    elif event.message.text=="128分":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="65":
                worksheet.update(list[1],int(66))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#67 以下那些課程是輔大的校定必修課程？"+"\n"+"（Ａ）大學入門、人生哲學、專業倫理"+"\n"+"（Ｂ）體育、國文、外國語文"+"\n"+"（Ｃ）人文與藝術、自然與科技、社會科學三個領域通識（包含歷史與文化學群）"+"\n"+"（Ｄ）以上皆是必修課程"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#67',
                    template=ButtonsTemplate(
                        title='#67',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="大學入門、人生哲學、專業倫理"
                            ),
                            MessageAction(
                                label='B',
                                text="體育、國文、外國語文"
                            ),
                            MessageAction(
                                label='C',
                                text="人文與藝術、自然與科技、社會科學三個領域通識（包含歷史與文化學群）"
                            ),
                            MessageAction(
                                label='D',
                                text="以上皆是必修課程"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="65":
                worksheet.update(list[1],int(66))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#67 以下那些課程是輔大的校定必修課程？"+"\n"+"（Ａ）大學入門、人生哲學、專業倫理"+"\n"+"（Ｂ）體育、國文、外國語文"+"\n"+"（Ｃ）人文與藝術、自然與科技、社會科學三個領域通識（包含歷史與文化學群）"+"\n"+"（Ｄ）以上皆是必修課程"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#67',
                    template=ButtonsTemplate(
                        title='#67',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="大學入門、人生哲學、專業倫理"
                            ),
                            MessageAction(
                                label='B',
                                text="體育、國文、外國語文"
                            ),
                            MessageAction(
                                label='C',
                                text="人文與藝術、自然與科技、社會科學三個領域通識（包含歷史與文化學群）"
                            ),
                            MessageAction(
                                label='D',
                                text="以上皆是必修課程"
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
    
    #67答案
    elif event.message.text=="以上皆是必修課程":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="66":
                worksheet.update(list[1],int(67))
                list_talk=[]
                list_talk.append(TextSendMessage(text="總而言之，為了安慰又忙又累的司晨，日翔擅自在下課後表示他要請司晨喝個飲料。"+"\n"+"「我也幫司晨出錢。」曉光提議。"+"\n"+"「欸欸！真的不用啦，而且我也有薪水啊。」司晨看著兩位對自己這麼好的同學，連忙進行推辭。不過下一秒便又後悔了：「那不然你們請我711就好啦，嘿嘿，我要順便去取個貨。」"+"\n"+"日翔一邊收書包，一邊無所謂的思考道：對了，學校這麼多便利商店，他甚至都沒有好好研究過店名……"))
                list_talk.append(TextSendMessage(text="#68 進修部旁邊7-11門市的名稱為？"+"\n"+"（Ａ）進修門市"+"\n"+"（Ｂ）輔大門市"+"\n"+"（Ｃ）輔進門市"+"\n"+"（Ｄ）輔明門市"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#68',
                    template=ButtonsTemplate(
                        title='#68',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="進修門市"
                            ),
                            MessageAction(
                                label='B',
                                text="輔大門市"
                            ),
                            MessageAction(
                                label='C',
                                text="輔進門市"
                            ),
                            MessageAction(
                                label='D',
                                text="輔明門市"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="66":
                worksheet.update(list[1],int(67))
                list_talk=[]
                list_talk.append(TextSendMessage(text="為了安慰又忙又累的司晨，日翔擅自在下課後表示他要請司晨喝個飲料。"+"\n"+"「我也幫司晨出錢。」曉光提議。"+"\n"+"「欸欸！真的不用啦，而且我也有薪水啊。」司晨看著兩位對自己這麼好的同學，連忙進行推辭。不過下一秒便又後悔了：「那不然你們請我711就好啦，嘿嘿，我要順便去取個貨。」"+"\n"+"曉光一邊收書包，一邊思考著：對了，學校這麼多便利商店，她甚至都沒有好好研究過店名……"))
                list_talk.append(TextSendMessage(text="#68 進修部旁邊7-11門市的名稱為？"+"\n"+"（Ａ）進修門市"+"\n"+"（Ｂ）輔大門市"+"\n"+"（Ｃ）輔進門市"+"\n"+"（Ｄ）輔明門市"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#68',
                    template=ButtonsTemplate(
                        title='#68',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="進修門市"
                            ),
                            MessageAction(
                                label='B',
                                text="輔大門市"
                            ),
                            MessageAction(
                                label='C',
                                text="輔進門市"
                            ),
                            MessageAction(
                                label='D',
                                text="輔明門市"
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

    #68答案
    elif event.message.text=="輔進門市":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="67":
                worksheet.update(list[1],int(68))
                list_talk=[]
                list_talk.append(TextSendMessage(text="取完貨、日翔和曉光也幫司晨付活益比O多的錢之後，三人走在離開學校的路上。"+"\n"+"日翔也替自己跟曉光結帳了兩瓶果汁。他旋開寶特瓶罐子，開始關心自己好友的狀況：「啊對了，司晨你以後有想做什麼嗎？」"+"\n"+"「欸？我沒講過嗎，經理跟我談好啦，因為我工作很認真，畢業之後工讀要幫我轉正欸！」"+"\n"+"雖然以過去的「經驗」來說，日翔早就知道這個時期的司晨已經給未來做好打算了——他當時也很意外，這個最粗心傻氣的摯友，居然是最先找到出路的。資管系畢業之後也有一些學生會去做與資管無關的工作，司晨就是其中一位。"+"\n"+"「沒想到你是我們之中最先計畫好未來的人。」日翔除了打從心底佩服他以外，也盡力表現出很意外的樣子。"+"\n"+"曉光似乎是想到了自己的升學準備進度，語氣也認真了起來：「好厲害。那我也得努力一點才行了。」"+"\n"+"日翔點點頭同意曉光所說的話，不只是曉光而已，他這個經過回歸的人也不可以就這樣敗給司晨了。"))
                list_talk.append(TextSendMessage(text="今天是日翔期待已久的實習說明會，說明通常會在導師時間統一舉辦。在這一天，會有許多企業會過來介紹徵才條件與福利等等，對有意參加產業實習的同學們無疑是十分重要的一天。除了不打算升學的日翔以外，同樣想參加實習的真澄和單純前來陪同的曉光也都過來了。"+"\n"+"每一年會參加輔大資管系產業實習計畫的企業都不一樣，不過日翔畢竟使用了code/140.136，於是他多少知道台上的企業大概有哪些。自然，這三年多重來的時間裡，日翔也為此做好了準備，除了在院必修的部分不怠慢之外，也把系上的程式語言課程給全修了！"+"\n"+"他很有信心這樣充實的大學生活，可以為他迎來一個更好的未來。"+"\n"+"他看著台上正好輪到了自己想去的企業之一，主動詢問坐在旁邊的真澄：「噯，真澄你覺得這家怎麼樣？」"+"\n"+"真澄思索了一下，表示他還想聽聽接下來其他企業的福利如何再決定：「我再想想吧，畢竟這很可能會是畢業後的第一份工作嘛。」"+"\n"+"「說得也是……」聽到這裡，日翔突然有感而發——他的大學生活明明已經是經歷了第二次，卻總對時光的飛逝感到措手不急，四年的時間很快又很慢，如今，所有人又將要啟程，隨著自己所定下的命運而飛往不同的方向。"+"\n"+"曉光似乎注意到了日翔心境上的變化，便小聲地對他傳達心情：「即使前程相異，我也會在你身邊……守護我們的約定。」"+"\n"+"日翔似乎因為見到了曉光感性的一面而有些動容。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='當然，因為我們已經約好了。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='當然，因為我們已經約好了。'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="67":
                worksheet.update(list[1],int(68))
                list_talk=[]
                list_talk.append(TextSendMessage(text="取完貨、日翔和曉光也幫司晨付活益比O多的錢之後，三人走在離開學校的路上。"+"\n"+"日翔也替自己跟曉光結帳了兩瓶果汁。他旋開寶特瓶罐子，開始關心自己好友的狀況：「啊對了，司晨你以後有想做什麼嗎？」"+"\n"+"「欸？我沒講過嗎，經理跟我談好啦，因為我工作很認真，畢業之後工讀要幫我轉正欸！」"+"\n"+"其實曉光早已知道這件事情，畢竟她可是從未來來的人，不過曉光還是很佩服司晨的努力，累積了許多的工作經驗，也存了一筆錢，未來這些資源都會變成他前進的助力，這點已經贏過大半數的大學生了。"+"\n"+"「沒想到你是我們之中最先計畫好未來的人。」日翔發出讚嘆的語氣。"+"\n"+"「真厲害。那我也得努力一點才行了。」曉光想想過去的自己，的確也是從畢業後考試、升學，之後憑著碩士學歷去找到適合自己的工作，這一步步走來的確也是不輕鬆。"+"\n"+"日翔點點頭同意曉光所說的話。"))
                list_talk.append(TextSendMessage(text="今天是實習說明會，說明通常會在導師時間統一舉辦。在這一天，會有許多企業會過來介紹徵才條件與福利等等，對有意參加產業實習的同學們無疑是十分重要的一天。除了不打算升學的日翔以外，同樣想參加實習的真澄和單純前來陪同的曉光也都過來了。"+"\n"+"「噯，真澄你覺得這家怎麼樣？」日翔主動詢問坐在旁邊的真澄。"+"\n"+"「我再想想吧，畢竟這很可能會是畢業後的第一份工作嘛。」真澄思索了一下，表示他還想聽聽接下來其他企業的福利如何再決定。"+"\n"+"「說得也是……」"+"\n"+"看來他們也都各自決定好未來的方向了，曉光看著正在討論的兩人想道。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='即使前程相異，我也會在你身邊……守護我們的約定。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='即使前程相異，我也會在你身邊……守護我們的約定。'
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
    elif event.message.text=="即使前程相異，我也會在你身邊……守護我們的約定。":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="68":
                list_talk=[]
                list_talk.append(TextSendMessage(text="曉光似乎注意到了日翔苦惱的樣子，便小聲地對他傳達心情。"+"\n"+"「當然，因為我們已經約好了。」日翔似乎因為見到了曉光感性的一面而有些動容，將自己的手放在曉光的手上。"+"\n"+"「哎哎你們不要擅自在那邊貼貼好不好！我以後當然也會跟親愛的曉光……還有日翔你繼續聯絡啊！我們的友情可沒那麼脆弱，更何況又還沒畢業。」坐在旁邊的真澄自然見證了一切，沒好氣的看著他們兩個偷偷放閃。"+"\n"+"「沒錯，真澄說得好。」"+"\n"+"曉光很慶幸自己能遇到這些好朋友，友誼的可貴渲染了曉光的大學生活，變得豐富又多彩。"))
                list_talk.append(TextSendMessage(text="過了幾天，曉光邀約日翔到她家讀書。放學後，他們便一路從學校走回小光的家裡，而當曉光打開家裡的大門，便見到媽媽坐在客廳的沙發上悠閒地跟窩在她腿上的德魯貝玩。她回過頭來說道：「曉光啊，這就是妳說的那位游日翔嗎？」"+"\n"+"「嗯，等等我們要在家裡讀書。」"+"\n"+"「伯母您好，我是游日翔。今天來您們家叨擾了。」日翔見到曉光媽媽，便有禮貌地向她自我介紹，並把書包裡要給曉光家的一袋禮盒拿出來。"+"\n"+"「其實日翔你不用特意準備禮物的……」曉光現在才知道日翔帶了禮物來，感到很驚訝。"+"\n"+"「別這麼說嘛，如果一直都空手來訪，我也會很不好意思。」日翔回應。"+"\n"+"其實今天日翔到曉光家來並不是單純地到對方家來玩，而是要準備將至的期中考……以及一些有關於實習用的履歷資料，曉光則是除了期中考之外，也需要對升學進行準備。"+"\n"+"曉光的房間在二樓，非常的寬敞，還有一大張足夠提供兩三個人念書的桌子，這對家裡有養貓咪的貓皇，可說是再適合不過的空間。"+"\n"+"日翔坐在書桌旁，把書包裡的幾本參考書拿出來。曉光發現這些都是她喜歡的作者出版的書籍。"+"\n"+"曉光很是驚喜，她把不知為何跟著過來的德魯貝抱到自己腿上：「哇……我也正好想要找他的書來看，謝謝你。」接著，她便像想到了甚麼重要的事情而將德魯貝交給日翔，並站起了身：「……對了，我下樓去拿冰好的葡萄汁過來。」"+"\n"+"「話說曉光妳真的很喜歡葡萄口味的東西啊。」日翔接過德魯貝，大概是想起了小時候的她也最喜歡吃葡萄口味的糖果。"+"\n"+"「喵……」到日翔懷裡的灰色胖貓似乎沒有不適應的樣子，反而撒嬌了起來。"+"\n"+"德魯貝還是那麼喜歡日翔呢。通常德魯貝對外人都擺出一股高傲的態度，但是面對日翔卻變成一隻溫馴的貓咪，如此大的反差讓曉光覺得很稀奇。"+"\n"+"「唔、畢竟酸酸甜甜的很好吃。」曉光看了看德魯貝和日翔，回答日翔。"+"\n"+"說完，曉光去樓下端了兩杯葡萄汁上了樓。"+"\n"+"「我記得妳上次……也是請我們喝葡萄汁對吧？」日翔想起上次來曉光家討論專題的事情。"+"\n"+"「對阿，你還記得。」曉光認為日翔總是把小事情記得很清楚。"+"\n"+"「話說，我都還不知道日翔你喜歡什麼飲料呢。」曉光問道。"+"\n"+"「大概就是葡萄汁？」日翔拿著自己背包上的籃球吊飾跟德魯貝玩了起來，一邊思索道：「其實我沒有什麼特別的愛好啦。要說的話……」"+"\n"+"「嗯、妳喜歡的我就喜歡？」日翔抬起頭來，露出了泛紅的臉頰和好看的微笑。"+"\n"+"「哎、……在說什麼啦！」 聽到日翔這麼說，耳根子也紅了起來。即使他們交往了一段時間，曉光還是還沒習慣這種促不及防的撩妹行為。"))
                list_talk.append(TextSendMessage(text="天氣漸漸冷了下來。傍晚的下課時分，真澄裹著一層厚厚的外套看著陰鬱的教室外頭，對與天氣呈現反差的風華廣場感到有些意外。"+"\n"+"「曉光，你看那裡。」真澄指著風華廣場的方向。"+"\n"+"曉光順著真澄手指的方向看過去。"+"\n"+"「是星光路跑阿。」說到星光路跑，這可是曉光最懷念的活動，可以看到無論是學生、老師、還是小朋友，在校園內開開心心跑步的樣子。"+"\n"+"「嘿…原來如此，我通常都下午就離開學校了，所以不知道星光路跑舉行的日子。」"))
                list_talk.append(TextSendMessage(text="#69 輔大的每年幾月會舉辦星光路跑？（請以「Ｏ月」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #??
    elif event.message.text=="當然，因為我們已經約好了。":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="68":
                list_talk=[]
                list_talk.append(TextSendMessage(text="他自然不敢在說明會的現場太大動作地直接跟曉光做些什麼，僅僅是覆上了她放在桌子的雙手。"+"\n"+"「哎哎你們不要擅自在那邊貼貼好不好！我以後當然也會跟親愛的曉光……還有日翔你繼續聯絡啊！我們的友情可沒那麼脆弱，更何況又還沒畢業。」坐在旁邊的真澄自然見證了一切，沒好氣的看著他們兩個偷偷放閃。"+"\n"+"「沒錯，真澄說得好。」"+"\n"+"聽到這些話，日翔突然有些感到釋懷——現在已經和過去的自己不同了，他身邊還有著很多可靠的朋友，更何況在資訊發達的現在，想要隨時約出來都不是很困難的事情。"+"\n"+"話說回來，曉光有一個那麼喜歡她的朋友，也真的是很難得啊。日翔不忘在心裡吐槽一下。"))
                list_talk.append(TextSendMessage(text="曉光打開家裡的大門，便見到媽媽坐在客廳的沙發上悠閒地跟窩在她腿上的德魯貝玩。她回過頭來說道：「曉光啊，這就是妳說的那位游日翔嗎？」"+"\n"+"聽到自己被點名，曉光便回應：「嗯，等等我們想要在家裡讀書。」"+"\n"+"日翔見到曉光媽媽，便有禮貌地向她自我介紹，並把書包裡要給曉光家的一袋禮盒拿出來：「伯母您好，我是游日翔。今天來您們家叨擾了。」"+"\n"+"沒想到今天會見到曉光媽媽，幸好有準備了家裡附近有名的紅豆大福當禮物……日翔對自己出門臨時去買一盒甜點的決定感到慶幸。"+"\n"+"曉光現在才知道日翔帶了禮物來，她感到很是驚訝：「其實日翔你不用特意準備禮物的……」"+"\n"+"「別這麼說嘛，如果一直都空手來訪，我也會很不好意思。」日翔回應。"+"\n"+"希望這次能夠給伯母帶點好印象。"+"\n"+"其實今天日翔到曉光家來並不是單純地到對方家來玩，而是要準備將至的期中考……以及一些有關於實習用的履歷資料，曉光則是除了期中考之外，也需要對升學進行準備；於是乎，雖然說是到了喜歡的女生家裡，卻還是在讀書而已。不過對日翔而言，能和曉光在一起已經是很開心的事情了。"+"\n"+"曉光的房間在二樓，裡面是比日翔想像中的要寬敞——而且還有一大張足夠提供兩三個人念書的桌子，要日翔去找一個恰當的形容的話，這大概已經跟自己家的客廳差不多大了。"+"\n"+"日翔坐在書桌旁，把書包裡的幾本參考書拿出來。他記得曉光在大三的時候好像說過自己喜歡這個人寫的書，於是便提早從濟時樓借了出來。雖然一口氣揹兩本同樣的厚重參考書過來是有點重，不過對他而言也並不是件難事：「我想之後會用到這幾本書，就先借過來了。」"+"\n"+"曉光很是驚喜，她把不知為何跟著過來的德魯貝抱到自己腿上：「哇……我也正好想要找他的書來看，謝謝你。」接著，她便像想到了甚麼重要的事情而將德魯貝交給日翔，並站起了身：「……對了，我下樓去拿冰好的葡萄汁過來。」"+"\n"+"「話說曉光妳真的很喜歡葡萄口味的東西啊。」日翔接過德魯貝，想起了小時候的她也最喜歡吃葡萄口味的糖果。"+"\n"+"「喵……」到日翔懷裡的灰色胖貓似乎沒有不適應的樣子，反而撒嬌了起來。日翔覺得這隻貓似乎和自己有說不出來的熟悉感……不禁開始想，該不會這隻貓真的是以前短暫照顧過的那隻瘦小的貓咪吧。如果真的是牠，那命運也實在太過於奇妙了。"+"\n"+"「唔、畢竟酸酸甜甜的很好吃。」"+"\n"+"「我記得妳上次……也是請我們喝葡萄汁對吧？」日翔感受到，在不知不覺間，她心中的曉光也從難以接近的女神這樣片面的形象之中變得逐漸鮮明起來，葡萄汁、霜淇淋、參考書、幼時一起編織的夢，以及她手心的溫度。"+"\n"+"曉光很快就端著兩杯葡萄汁上了樓：「說來，我都還不知道日翔你喜歡什麼飲料呢。」"+"\n"+"「大概是，葡萄汁？」日翔拿著自己背包上的籃球吊飾跟德魯貝玩了起來，一邊思索道：「其實我沒有什麼特別的愛好啦。要說的話……」"+"\n"+"日翔抬起頭來，露出了泛紅的臉頰和好看的微笑：「嗯、妳喜歡的我就喜歡？」"+"\n"+"「哎、……在說什麼啦！」"))
                list_talk.append(TextSendMessage(text="天氣漸漸冷了下來。傍晚的下課時分，司晨裹著一層厚厚的外套看著陰鬱的教室外頭，對與天氣呈現反差的風華廣場感到有些意外：「感覺今天教室外面特別熱鬧哎？」"+"\n"+"日翔看著窗外再看了看手機的日期，理所當然地回答自己的好兄弟：「是星光路跑吧？我還以為阿司你一定記得欸，今天不就是了嗎？！」"+"\n"+"「沒、沒有啊，我當然沒忘記！我只是想考考阿日你而已，哈哈哈哈哈哈！」司晨不知為何慌慌張張地回應。"+"\n"+"其實你不用掩飾也沒關係啊，畢竟也不是第一次犯傻了……日翔心想，跟你相處那麼久我早就習慣啦。"))
                list_talk.append(TextSendMessage(text="#69 輔大的每年幾月會舉辦星光路跑？（請以「Ｏ月」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    #69答案
    elif event.message.text=="12月":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="68":
                worksheet.update(list[1],int(69))
                list_talk=[]
                list_talk.append(TextSendMessage(text="「對欸，今天是聖誕節前一個禮拜！那下禮拜不就放假嗎！那天我一定要好好的享受一下！」"+"\n"+"眾所皆知，輔仁大學和其他大學不同的就是——輔大是天主教大學，而到了聖誕節，自然會給學生放一天假！除了聖誕節以外，輔大的教師節也是放假的。因為假期比其他學校要多，也有許多校友戲稱輔仁大學是「放假大學 Fang Jia University」。"+"\n"+"約略在11月底，學校就會在外頭布置華麗的大聖誕樹與聖誕燈飾，並且會在12月的每個晚上都點亮，這樣美麗的聖誕景色總是深得輔大人的心。"+"\n"+"「你聖誕節那天不用上班喔？」"+"\n"+"「不用啊，倒是阿日你都不約你女朋友出去？」司晨似乎是在計畫自己的聖誕節，心情顯得很是愉快。"+"\n"+"「我今天其實已經約她了啦，還在想要怎麼把你打發走呢。」聽聞好朋友居然反過來關心自己，日翔便用調侃的語氣說道。"+"\n"+"「嗚嗚……阿日，你好壞，一交女朋友……就想把我踢走！！」司晨還配合的開始假哭，可下一刻就馬上把那個假掰的語氣收回了，他坦蕩地拍拍日翔的肩膀：「好啦開玩笑的，這種事情你早說嘛，那我先走啦！」"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/28/ZmAdvH.png', preview_image_url='https://upload.cc/i1/2022/03/28/ZmAdvH.png'))
                list_talk.append(TextSendMessage(text="畢竟接近冬至，晚上五點半的天色自然是黯淡了下來，可輔仁大學的聖誕節的燈飾使得本該孤寂的夜晚十分絢爛，宛如地面的點點星光。日翔跟曉光手牽手漫步在校園中，要先好好欣賞聖誕燈再出學校約會。"+"\n"+"「對了曉光，我跟你說我的實習錄取了！妳那邊怎麼樣？」日翔對於自己的前程早早塵埃落定感到開心。"+"\n"+"「準備得差不多了，還要等過些日子報名。」曉光打算考取其他學校的碩士班，成績優異的她早就已經把升學要考試的東西讀得很是完備，幾乎只差在筆試跟面試的部分了。"+"\n"+"「曉光真厲害啊……」日翔不由得喃喃自語，畢竟對方實在是很會讀書，也很擅長計劃自己的升學考試。就算日翔有code/140.136的加持，使得自己在班上的成績也頗為優異，但他還是明白自己本身並不是一塊擅長讀書的料。"+"\n"+"曉光的回應還是一如既往的謙虛：「別這麼說，我也只是讀得比別人要多次而已。」"+"\n"+"兩人穿梭於繁華的造型燈飾之中，靜靜地欣賞輔仁大學聖誕節的景色。日翔感覺曉光並不是那麼愛聊天的類型，於是他選擇與她一同見證這個熱鬧的夜晚。"+"\n"+"兩人已經走到了校門口附近。日翔感覺，對比自己還算有溫度的手來說，曉光的手即使被自己牽了這麼久還是顯得冰冷。他想，他應該可以買杯熱拿鐵來給曉光一些溫暖。"+"\n"+"「曉光，妳要喝熱拿鐵嗎？我去買。」"+"\n"+"「謝謝你，可是……不用麻煩你了。」"+"\n"+"「沒事，妳冷到了就糟糕了。我去買給妳吧？」"))
                list_talk.append(TextSendMessage(text="#70 請問靠近學校出口，在郵局旁邊的賣場為何？"+"\n"+"（Ａ）好市多"+"\n"+"（Ｂ）IKEA"+"\n"+"（Ｃ）全聯福利中心"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#70',
                    template=ButtonsTemplate(
                        title='#70',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="好市多"
                            ),
                            MessageAction(
                                label='B',
                                text="IKEA"
                            ),
                            MessageAction(
                                label='C',
                                text="全聯福利中心"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="68":
                worksheet.update(list[1],int(69))
                list_talk=[]
                list_talk.append(TextSendMessage(text="輔仁大學和其他大學不同的就是——輔大是天主教大學，而到了聖誕節，自然會給學生放一天假！除了聖誕節以外，輔大的教師節也是放假的。因為假期比其他學校要多，也有許多校友戲稱輔仁大學是「放假大學 Fang Jia University」。"+"\n"+"約略在11月底，學校就會在外頭布置華麗的大聖誕樹與聖誕燈飾，並且會在12月的每個晚上都點亮，這樣美麗的聖誕景色總是深得輔大人的心。"+"\n"+"「話說，聖誕節有什麼計畫阿？」真澄的微笑裡感覺有其他意思。"+"\n"+"「哎呀，是不是已經被日翔約走了阿？」真澄早就知道問題的答案，卻還是想看看曉光的反應。"+"\n"+"「嗯…」 曉光害羞的點點頭。"+"\n"+"「你喔，什麼時候才要把時間留給我啊。」真澄戳了戳曉光的臉頰。"+"\n"+"「對不起嘛，下次一定會約你。」曉光愧歉的說著。"+"\n"+"「我們說好了喔。」真澄伸出自己的手指，示意著要與曉光打勾勾。"+"\n"+"曉光覺得真澄有時候還挺可愛的，於是曉光面帶微笑地也伸出手指勾住真澄的手指。"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/28/ZmAdvH.png', preview_image_url='https://upload.cc/i1/2022/03/28/ZmAdvH.png'))
                list_talk.append(TextSendMessage(text="畢竟接近冬至，晚上五點半的天色自然是黯淡了下來，可輔仁大學的聖誕節的燈飾使得本該孤寂的夜晚十分絢爛，宛如地面的點點星光。日翔跟曉光手牽手漫步在校園中，要先好好欣賞聖誕燈再出學校約會。"+"\n"+"「對了曉光，我跟你說我的實習錄取了！妳那邊怎麼樣？」日翔開心的說著。"+"\n"+"「準備得差不多了，還要等過些日子報名。」曉光打算考取其他學校的碩士班，成績優異的她早就已經把升學要考試的東西讀得很是完備，幾乎只差在筆試跟面試的部分了。"+"\n"+"「曉光真厲害啊……」日翔喃喃自語道。"+"\n"+"「別這麼說，我也只是讀得比別人要多次而已。」沒錯，曉光以前為了準備升學考早就將考科背熟了，這次回來才能這麼快準備好。"+"\n"+"兩人穿梭於繁華的造型燈飾之中，靜靜地欣賞輔仁大學聖誕節的景色。兩人並沒有多說什麼話，只是靜靜地一同見證這個熱鬧的夜晚。"+"\n"+"「曉光，妳要喝熱拿鐵嗎？我去買。」兩人已經走到了校門口附近，發覺曉光的手些微冰冷的日翔提出這個建議。"+"\n"+"「謝謝你，可是……不用麻煩你了。」"+"\n"+"「沒事，妳冷到了就糟糕了。我去買給妳吧？」"))
                list_talk.append(TextSendMessage(text="#70 請問靠近學校出口，在郵局旁邊的賣場為何？"+"\n"+"（Ａ）好市多"+"\n"+"（Ｂ）IKEA"+"\n"+"（Ｃ）全聯福利中心"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#70',
                    template=ButtonsTemplate(
                        title='#70',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="好市多"
                            ),
                            MessageAction(
                                label='B',
                                text="IKEA"
                            ),
                            MessageAction(
                                label='C',
                                text="全聯福利中心"
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

    #70答案
    elif event.message.text=="全聯福利中心":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="69":
                worksheet.update(list[1],int(70))
                list_talk=[]
                list_talk.append(TextSendMessage(text="考試又要到來，這已經是日翔大學生活的第N次測驗了，想必他也已經習慣了吧。"+"\n"+"如今距離真相也越來越接近，或許在不久之後，我們就將會接觸到一切的源頭。"))
                list_talk.append(TextSendMessage(text="#71 請問19.20行輸出的結果分別是？"+"\n"+"（Ａ）true, false"+"\n"+"（Ｂ）null, null"+"\n"+"（Ｃ）1, 0"+"\n"+"（Ｄ）false,  true"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/04/VNuXJc.png', preview_image_url='https://upload.cc/i1/2022/04/04/VNuXJc.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#71',
                    template=ButtonsTemplate(
                        title='#71',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="true, false"
                            ),
                            MessageAction(
                                label='B',
                                text="null, null"
                            ),
                            MessageAction(
                                label='C',
                                text="1, 0"
                            ),
                            MessageAction(
                                label='C',
                                text="false,  true"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="69":
                worksheet.update(list[1],int(70))
                list_talk=[]
                list_talk.append(TextSendMessage(text="過完聖誕節，迎接全新的年份，同時也是準備期中考的時候。"+"\n"+"如今距離真相也越來越接近，或許在不久之後，將會接觸到一切的源頭。"))
                list_talk.append(TextSendMessage(text="#71 請問19.20行輸出的結果分別是？"+"\n"+"（Ａ）true, false"+"\n"+"（Ｂ）null, null"+"\n"+"（Ｃ）1, 0"+"\n"+"（Ｄ）false,  true"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/04/VNuXJc.png', preview_image_url='https://upload.cc/i1/2022/04/04/VNuXJc.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#71',
                    template=ButtonsTemplate(
                        title='#71',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="true, false"
                            ),
                            MessageAction(
                                label='B',
                                text="null, null"
                            ),
                            MessageAction(
                                label='C',
                                text="1, 0"
                            ),
                            MessageAction(
                                label='C',
                                text="false,  true"
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

    #71答案
    elif event.message.text=="true, false":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="70":
                worksheet.update(list[1],int(71))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#72 請問以下JS程式碼可以alert出hello嗎？"+"\n"+"（Ａ）可以"+"\n"+"（Ｂ）不行"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/04/hj1QrD.png', preview_image_url='https://upload.cc/i1/2022/04/04/hj1QrD.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#72',
                    template=ButtonsTemplate(
                        title='#72',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="可以"
                            ),
                            MessageAction(
                                label='B',
                                text="不行"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="70":
                worksheet.update(list[1],int(71))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#72 請問以下JS程式碼可以alert出hello嗎？"+"\n"+"（Ａ）可以"+"\n"+"（Ｂ）不行"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/04/04/hj1QrD.png', preview_image_url='https://upload.cc/i1/2022/04/04/hj1QrD.png'))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#72',
                    template=ButtonsTemplate(
                        title='#72',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="可以"
                            ),
                            MessageAction(
                                label='B',
                                text="不行"
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

    #72答案
    elif event.message.text=="不行":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="71":
                worksheet.update(list[1],int(72))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#73 下列哪一個是十進位數 100 的二進位值？"+"\n"+"（Ａ）10110100"+"\n"+"（Ｂ）1100100"+"\n"+"（Ｃ）110010"+"\n"+"（Ｄ）1010000"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#73',
                    template=ButtonsTemplate(
                        title='#73',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="10110100"
                            ),
                            MessageAction(
                                label='B',
                                text="1100100"
                            ),
                            MessageAction(
                                label='C',
                                text="110010"
                            ),
                            MessageAction(
                                label='D',
                                text="1010000"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="71":
                worksheet.update(list[1],int(72))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#73 下列哪一個是十進位數 100 的二進位值？"+"\n"+"（Ａ）10110100"+"\n"+"（Ｂ）1100100"+"\n"+"（Ｃ）110010"+"\n"+"（Ｄ）1010000"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#73',
                    template=ButtonsTemplate(
                        title='#73',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="10110100"
                            ),
                            MessageAction(
                                label='B',
                                text="1100100"
                            ),
                            MessageAction(
                                label='C',
                                text="110010"
                            ),
                            MessageAction(
                                label='D',
                                text="1010000"
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

    #73答案
    elif event.message.text=="1100100":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="72":
                worksheet.update(list[1],int(73))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#74 下列哪一個不是和網頁設計有關的程式語言？"+"\n"+"（Ａ）HTML"+"\n"+"（Ｂ）JavaScript"+"\n"+"（Ｃ）CSS"+"\n"+"（Ｄ）JQuery"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#74',
                    template=ButtonsTemplate(
                        title='#74',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="HTML"
                            ),
                            MessageAction(
                                label='B',
                                text="JavaScript"
                            ),
                            MessageAction(
                                label='C',
                                text="CSS"
                            ),
                            MessageAction(
                                label='D',
                                text="JQuery"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="72":
                worksheet.update(list[1],int(73))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#74 下列哪一個不是和網頁設計有關的程式語言？"+"\n"+"（Ａ）HTML"+"\n"+"（Ｂ）JavaScript"+"\n"+"（Ｃ）CSS"+"\n"+"（Ｄ）JQuery"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#74',
                    template=ButtonsTemplate(
                        title='#74',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="HTML"
                            ),
                            MessageAction(
                                label='B',
                                text="JavaScript"
                            ),
                            MessageAction(
                                label='C',
                                text="CSS"
                            ),
                            MessageAction(
                                label='D',
                                text="JQuery"
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

    #74答案
    elif event.message.text=="HTML":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="73":
                worksheet.update(list[1],int(74))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#75 剛上大學的小華想要找一份打工，目前有四份工作曉華正在猶豫，分別是補習班 14000 元、餐廳 17000 元、飲料店 16000 元和便利商店 20000元，在僅考慮薪水不考慮其他因素的情況下，小華選擇到飲料店工作的機會成本是多少？（請以「Ｏ元」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="73":
                worksheet.update(list[1],int(74))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#75 剛上大學的小華想要找一份打工，目前有四份工作曉華正在猶豫，分別是補習班 14000 元、餐廳 17000 元、飲料店 16000 元和便利商店 20000元，在僅考慮薪水不考慮其他因素的情況下，小華選擇到飲料店工作的機會成本是多少？（請以「Ｏ元」回答，Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
    
    #75答案
    elif event.message.text=="20000元":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="74":
                worksheet.update(list[1],int(75))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#76 有關於GDP與GNP，下列何者正確？"+"\n"+"（Ａ）GDP是以國民為計算標準"+"\n"+"（Ｂ）GNP的全名為國民生產毛額"+"\n"+"（Ｃ）GNP是以國家為計算標準"+"\n"+"（Ｄ）GDP的全名為國民生產總額"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#76',
                    template=ButtonsTemplate(
                        title='#76',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="GDP是以國民為計算標準"
                            ),
                            MessageAction(
                                label='B',
                                text="GNP的全名為國民生產毛額"
                            ),
                            MessageAction(
                                label='C',
                                text="GNP是以國家為計算標準"
                            ),
                            MessageAction(
                                label='D',
                                text="GDP的全名為國民生產總額"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="74":
                worksheet.update(list[1],int(75))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#76 有關於GDP與GNP，下列何者正確？"+"\n"+"（Ａ）GDP是以國民為計算標準"+"\n"+"（Ｂ）GNP的全名為國民生產毛額"+"\n"+"（Ｃ）GNP是以國家為計算標準"+"\n"+"（Ｄ）GDP的全名為國民生產總額"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#76',
                    template=ButtonsTemplate(
                        title='#76',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="GDP是以國民為計算標準"
                            ),
                            MessageAction(
                                label='B',
                                text="GNP的全名為國民生產毛額"
                            ),
                            MessageAction(
                                label='C',
                                text="GNP是以國家為計算標準"
                            ),
                            MessageAction(
                                label='D',
                                text="GDP的全名為國民生產總額"
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

    #76答案
    elif event.message.text=="GNP的全名為國民生產毛額":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="75":
                worksheet.update(list[1],int(76))
                list_talk=[]
                list_talk.append(TextSendMessage(text="很快的季節到了春天，除了下學期來臨以外，更是碩士班放榜的季節！為了關心曉光跟宇桓的錄取狀況，五人組決定來個相聚歡。因為日翔等人畢業了之後就很難再隨時回到學校，於是一行人在討論之中，本來是打算吃學餐的……"))
                list_talk.append(TextSendMessage(text="#77 下列哪個不是學餐？"+"\n"+"（Ａ）理園"+"\n"+"（Ｂ）法園"+"\n"+"（Ｃ）仁園"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#77',
                    template=ButtonsTemplate(
                        title='#77',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="理園"
                            ),
                            MessageAction(
                                label='B',
                                text="法園"
                            ),
                            MessageAction(
                                label='C',
                                text="仁園"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="75":
                worksheet.update(list[1],int(76))
                list_talk=[]
                list_talk.append(TextSendMessage(text="很快的季節到了春天，除了下學期來臨以外，更是碩士班放榜的季節！為了關心曉光跟宇桓的錄取狀況，五人組決定來個相聚歡。因為日翔等人畢業了之後就很難再隨時回到學校，於是一行人在討論之中，本來是打算吃學餐的……"))
                list_talk.append(TextSendMessage(text="#77 下列哪個不是學餐？"+"\n"+"（Ａ）理園"+"\n"+"（Ｂ）法園"+"\n"+"（Ｃ）仁園"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#77',
                    template=ButtonsTemplate(
                        title='#77',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="理園"
                            ),
                            MessageAction(
                                label='B',
                                text="法園"
                            ),
                            MessageAction(
                                label='C',
                                text="仁園"
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

    #77答案
    elif event.message.text=="法園":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="76":
                worksheet.update(list[1],int(77))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#78 輔大「五」學餐為？"+"\n"+"（Ａ）輔園、文園、心園、仁園、理園"+"\n"+"（Ｂ）一園、兩園、三園、四園、五園"+"\n"+"（Ｃ）動物園、植物園、伊甸園、公園、球好園"+"\n"+"（Ｄ）日園、美園、歐園、澳園、港園"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#79',
                    template=ButtonsTemplate(
                        title='#78',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="輔園、文園、心園、仁園、理園"
                            ),
                            MessageAction(
                                label='B',
                                text="一園、兩園、三園、四園、五園"
                            ),
                            MessageAction(
                                label='C',
                                text="動物園、植物園、伊甸園、公園、球好園"
                            ),
                            MessageAction(
                                label='D',
                                text="日園、美園、歐園、澳園、港園"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="76":
                worksheet.update(list[1],int(77))
                list_talk=[]
                list_talk.append(TextSendMessage(text="#78 輔大「五」學餐為？"+"\n"+"（Ａ）輔園、文園、心園、仁園、理園"+"\n"+"（Ｂ）一園、兩園、三園、四園、五園"+"\n"+"（Ｃ）動物園、植物園、伊甸園、公園、球好園"+"\n"+"（Ｄ）日園、美園、歐園、澳園、港園"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#79',
                    template=ButtonsTemplate(
                        title='#78',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="輔園、文園、心園、仁園、理園"
                            ),
                            MessageAction(
                                label='B',
                                text="一園、兩園、三園、四園、五園"
                            ),
                            MessageAction(
                                label='C',
                                text="動物園、植物園、伊甸園、公園、球好園"
                            ),
                            MessageAction(
                                label='D',
                                text="日園、美園、歐園、澳園、港園"
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
    elif event.message.text=="輔園、文園、心園、仁園、理園":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="77":
                worksheet.update(list[1],int(78))
                list_talk=[]
                list_talk.append(TextSendMessage(text="最後，還是得歸功於宇桓一如既往「你們選，我都行」的大氣，再加上真的是快要畢業了，這次除了曉光之外，眾人都沒有直接阻止司晨隨便亂選各式各樣吃到飽餐廳的行為。LINE聊天群組裡，幾個人決定聚餐地點的樣子很是熱鬧："+"\n"+"「欸欸不然我們去吃晶華酒店那個很酷的頂級bafet好不好！！！！！！」"+"\n"+"「@oO卐籃球master🍃司晨卍Oo  哇靠那個吃晚餐超貴欸，還有那個是buffet你拼錯了」"+"\n"+"「@日翔☀ 普通價位而已吧？還行，看你們。｣"+"\n"+"「靠，你家到底是多有錢啊……」"+"\n"+"「司晨，這樣麻煩宇桓不好 @oO卐籃球master🍃司晨卍Oo」"+"\n"+"「還是曉光溫柔」"+"\n"+"「還是我家最親愛的曉光溫柔」"+"\n"+"「@真澄_Kotsu 不是你家的😡」"+"\n"+"「@日翔☀ 唷你學會吃醋啦😊😊」"))
                list_talk.append(TextSendMessage(text="結果大家還是為了顧及宇桓的錢包，依舊決定去吃一波「吃。貓」。而這次相約總算沒有擾人的雨天了，五人自然是坐了一個大桌，他們正一起討論要點些什麼。"+"\n"+"「上次你幫我點那個是什麼啊，CP值超高的欸！！」畢竟上次沒有第一時間就參與，司晨是第一次看到吃貓的菜單，似乎對於裡面豐富的品項感到新奇。"+"\n"+"「哦，那個是『吃不完的脆薯』，你要的話這次自己點。」日翔對那個盯著菜單雙眼發光的摯友感到很不意外。"+"\n"+"「不知道那個叫做『心痛』的飲料到底是什麼……」日翔本來又想點點看「隨便」——也就是店家真的隨機準備的飲料（可能會出現菜單沒有的東西），卻看到了菜單角落有一個叫做心痛的特別飲料。"+"\n"+"「應該是開水。因為要價100元的開水很讓人心痛？」曉光似乎也很好奇，她對此進行了一番合理的推測。"+"\n"+"「……我先說清楚，不要點那種東西，要點自己付錢。」聽聞要價100元「心痛」的真相，金錢觀特別大氣的宇桓也對他們制止了一番。"))
                list_talk.append(TextSendMessage(text="很快的眾人就點好了餐，大家都各點了一些自己感興趣的食物。日翔仍舊給自己點了一杯「隨便」，而曉光還是老樣子點了葡萄汁，日翔對此感到頗為有趣。"+"\n"+"「所以宇桓曉光，你們的升學情形怎麼樣啊？」司晨啃著脆薯發問。"+"\n"+"「當然是錄取了。」「我也錄取了。」兩人不約而同地回答。"+"\n"+"哇……不愧是兩個學霸，競爭這麼激烈的升學對他們而言跟喝水一樣。日翔在內心默默佩服……他們都成功考上國立大學的研究所了，真厲害。"+"\n"+"不過對日翔而言，如果要升學他應該會比較傾向考慮資管系的五年一貫方案：若是申請通過，就可以在大三就獲得碩士的修課資格，並在大四後一年就得到學位。既省下整整一年的學費又可以提早出去闖盪，十分划算。"+"\n"+"「這樣看來大家都找到自己出路了。」日翔對於包括自己在內的所有人都有著不錯的未來，內心又是一陣感慨。"+"\n"+"真澄也對此有感而發，帶了些悲傷的情緒：「不過，以後我們就不會坐在教室裡一起上課了。」"+"\n"+"曉光見到自己的好友有些難過，連忙安慰道：「真澄，你上次才說『我們的友情可沒那麼脆弱』。以後我們可以隨時再相約。」"+"\n"+"「是這樣沒錯……可是，總不可能這麼容易就喬出大家都有空的時間吧，況且大家以後都要各奔東西了，甚至也可能有人之後都不在北部工作，像我就是這樣。」真澄難得地道出自己的內心話。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='……',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='……'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="77":
                worksheet.update(list[1],int(78))
                list_talk=[]
                list_talk.append(TextSendMessage(text="最後，還是得歸功於宇桓一如既往「你們選，我都行」的大氣，再加上真的是快要畢業了，這次除了曉光之外，眾人都沒有直接阻止司晨隨便亂選各式各樣吃到飽餐廳的行為。LINE聊天群組裡，幾個人決定聚餐地點的樣子很是熱鬧："+"\n"+"「欸欸不然我們去吃晶華酒店那個很酷的頂級bafet好不好！！！！！！」"+"\n"+"「@oO卐籃球master🍃司晨卍Oo  哇靠那個吃晚餐超貴欸，還有那個是buffet你拼錯了」"+"\n"+"「@日翔☀ 普通價位而已吧？還行，看你們。｣"+"\n"+"「靠，你家到底是多有錢啊……」"+"\n"+"「司晨，這樣麻煩宇桓不好 @oO卐籃球master🍃司晨卍Oo」"+"\n"+"「還是曉光溫柔」"+"\n"+"「還是我家最親愛的曉光溫柔」"+"\n"+"「@真澄_Kotsu 不是你家的😡」"+"\n"+"「@日翔☀ 唷你學會吃醋啦😊😊」"))
                list_talk.append(TextSendMessage(text="結果大家還是為了顧及宇桓的錢包，依舊決定去吃一波「吃。貓」。而這次相約總算沒有擾人的雨天了，五人自然是坐了一個大桌，他們正一起討論要點些什麼。"+"\n"+"「上次你幫我點那個是什麼啊，CP值超高的欸！！」畢竟上次沒有第一時間就參與，司晨是第一次看到吃貓的菜單，似乎對於裡面豐富的品項感到新奇。"+"\n"+"「哦，那個是『吃不完的脆薯』，你要的話這次自己點。」與司晨興奮的口氣比起來，日翔只是平淡的說著。"+"\n"+"「不知道那個叫做『心痛』的飲料到底是什麼……」日翔本來又想點點看「隨便」——也就是店家真的隨機準備的飲料（可能會出現菜單沒有的東西），卻看到了菜單角落有一個叫做心痛的特別飲料。"+"\n"+"「應該是開水。因為要價100元的開水很讓人心痛？」曉光似乎也很好奇，她對此進行了一番合理的推測。"+"\n"+"「……我先說清楚，不要點那種東西，要點自己付錢。」聽聞要價100元「心痛」的真相，金錢觀特別大氣的宇桓也對他們制止了一番。"))
                list_talk.append(TextSendMessage(text="很快的眾人就點好了餐，大家都各點了一些自己感興趣的食物。日翔仍舊給自己點了一杯「隨便」，而曉光還是老樣子點了葡萄汁，曉光無法抵擋葡萄汁的誘惑。"+"\n"+"「所以宇桓曉光，你們的升學情形怎麼樣啊？」司晨啃著脆薯發問。"+"\n"+"「當然是錄取了。」「我也錄取了。」兩人不約而同地回答。"+"\n"+"原來宇桓也錄取了。身為角逐班上前兩名的兩個學霸，曉光也很肯定宇桓的實力。"+"\n"+"「這樣看來大家都找到自己出路了。」日翔對於包括自己在內的所有人都有著不錯的未來，內心又是一陣感慨。"+"\n"+"「不過，以後我們就不會坐在教室裡一起上課了。」真澄也對此有感而發，帶了些悲傷的情緒。"+"\n"+"「真澄，你上次才說『我們的友情可沒那麼脆弱』。以後我們可以隨時再相約。」曉光見到自己的好友有些難過，連忙安慰道。"+"\n"+"「是這樣沒錯……可是，總不可能這麼容易就喬出大家都有空的時間吧，況且大家以後都要各奔東西了，甚至也可能有人之後都不在北部工作，像我就是這樣。」真澄難得地道出自己的內心話。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='……',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='……'
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
    elif event.message.text=="……":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="78":
                list_talk=[]
                list_talk.append(TextSendMessage(text="於是沉默一陣，真澄說的也並非沒有道理。"+"\n"+"想到了有人說大學是「最後的青春」，一生只有一次的珍貴年華。時間是即使緊握也無法使其回頭的一種概念，這使得時間軌跡中的例外之一的日翔對於第二次的大學生活十分珍惜。即使有了第二次，日翔也認為誰也不能讓青春像乘坐心儀的遊樂設施般反覆重來。"+"\n"+"「哎，那就趁現在製造更多更多的回憶不就好了嗎？坐在這難過有什麼用！快點快點，我們來玩遊戲！看誰可以最先讓貓咪主動靠過來摸摸！最後一名要幫大家各買一杯心痛！」司晨看到大家沉默了起來，便站起身來提議自己的想法，而且還真的跑去找店員買了貓咪肉乾要餵食貓咪店員。"+"\n"+"「哈哈，好啊，那我也不能認輸了！」「唔、我也想買一條肉乾。」「有趣。」"+"\n"+"真澄見到大家興致勃勃的，心情便恢復了不少——她想，這樣的時光一定能化作每個人心裡最璀璨的寶石。"))
                list_talk.append(TextSendMessage(text="為了參加畢業典禮上午的「畢業生校園巡禮」，日翔早早就搭上了捷運。這對日翔來說，已經是第二次的輔仁大學畢業典禮，大學時光短短四年將要在今天結束，從明天開始，他又要變回社會人士了——不過，當然是以進入不同的公司，以不同的身分馳騁於社會上，而且還與自己重要的青梅竹馬相認，成為了情侶。日翔坐在靠窗的座位上托著腮幫子觀覽窗外的風景，他心想，這樣的結束對他而言實在比想像中的好太多太多了。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='畢業典禮即將開始，你已經搭上了去往輔仁大學的捷運。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='參加畢業典禮'
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="78":
                list_talk=[]
                list_talk.append(TextSendMessage(text="於是沉默一陣，真澄說的也並非沒有道理。"+"\n"+"曉光想到了有人說大學是「最後的青春」，一生只有一次的珍貴年華。時間是即使緊握也無法使其回頭的一種概念，即使像自己那樣有了第二次，曉光也認為誰也不能讓青春像乘坐心儀的遊樂設施般反覆重來。"+"\n"+"「哎，那就趁現在製造更多更多的回憶不就好了嗎？坐在這難過有什麼用！快點快點，我們來玩遊戲！看誰可以最先讓貓咪主動靠過來摸摸！最後一名要幫大家各買一杯心痛！」司晨看到大家沉默了起來，便站起身來提議自己的想法，而且還真的跑去找店員買了貓咪肉乾要餵食貓咪店員。"+"\n"+"「哈哈，好啊，那我也不能認輸了！」「唔、我也想買一條肉乾。」「有趣。」"+"\n"+"真澄見到大家興致勃勃的，心情便恢復了不少——她想，這樣的時光一定能化作每個人心裡最璀璨的寶石。"))
                list_talk.append(TextSendMessage(text="為了參加畢業典禮上午的「畢業生校園巡禮」，曉光早早就出了門。這對曉光來說，已經是第二次的輔仁大學畢業典禮，大學時光短短四年將要在今天結束，從明天開始，又再度回到畢業後的生活，曉光不禁感慨時光飛逝，但是曉光認為自己已經度過了一個難忘的大學回憶，是原本想像不到的。"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='選項',
                    template=ButtonsTemplate(
                        title='選項',
                        text='畢業典禮即將開始，你已經搭上了去往輔仁大學的捷運。',
                        actions=[
                            MessageAction(
                                label='選擇',
                                text='參加畢業典禮'
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
    elif event.message.text=="參加畢業典禮":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="78":
                list_talk=[]
                list_talk.append(TextSendMessage(text="「日翔、日翔。」沉浸在思緒之中的日翔突然被熟悉的聲音打斷。"+"\n"+"日翔回頭一看，曉光不知何時就站在了自己身旁——他又抬抬頭確認車廂的跑馬燈，果然是到了環狀線跟板南線轉乘的新埔民生站，看來曉光也才剛剛上車。"+"\n"+"可能是因為出門的時段有些不太一樣，日翔平常幾乎不會和曉光搭上同一班車。他一邊收回發散的思緒，一邊回應：「欸，曉光？好巧啊。」"+"\n"+"只見曉光將手送過來，似乎是要交給自己什麼東西：「你的東西掉了哦。」"+"\n"+"「啊…‥」他看了看曉光打算交給他的東西，這不正是剛剛還躺在自己口袋的學生證嗎？到底什麼時候滑下來了……日翔有些納悶，但不打算就這件事思索下去，因為他正好想起了大一開學那天，他們的相遇就是因為撿到了對方的學生證，就算那天沒有和曉光說到什麼話，他仍然對於和曉光重新接觸的那一天印象深刻；仔細想起來，都還像是前一刻才發生一樣。"+"\n"+"曉光見到日翔旁邊還有空位，便就順勢坐了下來：「大一開學的時候，也是你幫我找到學生證的，好巧。」"+"\n"+"「嘿嘿、我也在想一樣的事情。或許學生證就是一種我們的緣分吧？俗話說萬事起頭難？」日翔開始回味起了那一天的情景，當時撿到曉光學生證的震驚似乎還留存在腦海之中。"+"\n"+"「我想，」曉光也跟著笑了起來：「我們的『起頭』也可能是那天科博館看展，你怕我落單而主動找我的那一天。」"+"\n"+"「如果以小說來形容的話就像是『序章』一樣重要的東西吧，如果沒有發生的話，會不會我們到現在都還是普通同學呢？」現在自己確實也很慶幸那天有決定要牽她的手，日翔心想，或許那次的決定真的造就出了蝴蝶效應，使得兩人的命運出現改變。雖然也托了code/140.136的福，但他仍舊認為小時候的回憶是至關重要的。"+"\n"+"「嗯……或許吧。有些事現在看來就跟奇蹟一樣。」曉光也同意了日翔的話。"+"\n"+"於是，兩人不同於初次相見一般在上學路途中無話可講，反而是肩並著肩、有說有笑的前行，變成了無話不談的關係。"))
                list_talk.append(TextSendMessage(text="校園巡禮結束後，就是大四生的畢業典禮了。"+"\n"+"所有大四生都像開學典禮一樣，每個人都在中美堂穿著學士服，領受天主以及師長們對所有輔仁學士即將啟程的祝福。在畢業典禮的氛圍渲染之下，也有不少珍愛大學生活的畢業生在中美堂裡面哭了出來。"+"\n"+"在畢業典禮結束後，日翔跟曉光兩人一同走出中美堂。中美堂外面人很多，除了畢業的社團發表之外，當然也有許多前來參加畢業典禮的家長。正當日翔感嘆著這熱鬧的情景或許是最後一次見到了，便看到自己的好友司晨裝作哭哭啼啼的樣子，一邊大喊大叫跑了過來：「阿日！！阿日！你要開心，你要幸福，好不好？ 開心啊，幸福！！！」"+"\n"+"「什麼鬼……你這次又玩什麼梗了？」日翔傻眼，就算要畢業了他還是不放過任何一次耍笨的機會。"+"\n"+"「沒有啦哈哈，只是昨天看的一部電影有個女生甩掉男生的時候那個男生說的話，我就模仿了一下啊。」司晨一邊打哈哈裝傻，這才注意到他的浮誇行為再度引起了周圍所有人的注意。"+"\n"+"「哈哈哈哈，哎你這四年倒是一點都沒變啊。」日翔對此很是欣慰，司晨從大一到大四都是自己最好的朋友，以某種程度來說，他也陪伴了自己八年的時間啊。"+"\n"+"「唉唷，說是這麼說，但是我對兄弟你的祝福可是真心的！以後我們就不能一直在一起玩啦，我們彼此在不同地方也要加油啊。」司晨很是真心地對日翔表達祝福之意。"+"\n"+"真澄似乎是從一旁看到了剛才的鬧劇，於是湊上來說道：「我剛剛還想這裡怎麼這麼吵，原來是你啊司晨。」"+"\n"+"「是啊，剛剛還想找你們的，多虧葉司晨一直都這麼吵，傳LINE都免了。」宇桓跟在後頭附議。"+"\n"+"司晨聽見這兩人對自己的吐槽，倒是不滿地開始抗議：「欸X不是啊，林真澄馬宇桓你們什麼意思啦！」"+"\n"+"「只是覺得很可惜以後都聽不到你那麼吵了。」宇桓難得對司晨的蠢行為有了正面的反應。"+"\n"+"「是啊，多虧你多吵了這會，好讓我能夠記得清楚一些。」真澄也沒有嫌棄司晨，倒是不忘對他吐槽一口。"+"\n"+"「我能夠交到你們這些朋友，真的很開心。」曉光看著一群人的樣子，很是欣慰地表達自己的想法——這些朋友或許不可靠，但確實增添了大學生活的樂趣。"+"\n"+"「大學生活沒有浪費真是太好了。」日翔同意曉光的說法。"+"\n"+"「對了，那個誰不是一直說想吃晶華栢麗廳嗎，我剛好晚上有訂位，姑且給我們五個人當畢業餐。」宇桓看中了話題結束的間隔，突然告知在場的所有人他打算圓圓某個白癡的夢。"+"\n"+"「哇……真的假的啊宇桓！？晚上的吃到飽不是超貴嗎？」聽到關鍵字，日翔的雙眼也誠實地發亮了起來。"+"\n"+"宇桓面對日翔跟司晨閃亮亮的眼神，似乎有些應對不來：「沒差多少吧。咳、總之，要聊可以晚上見。」語畢，宇桓便頭也不回的走了。"+"\n"+"真澄對此也忍不住評價：「……宇桓他是真的很罩，我真的對他刮目相看了。」"+"\n"+"「做專題的時候也很厲害，再難的工作都可以很快搞定。」曉光似乎也對宇桓的為人有所認可。"))
                list_talk.append(TextSendMessage(text="眾人約好晚上相見之後便離開了學校，唯獨留下了日翔和曉光兩個人。"+"\n"+"正當他們打算離開校園時，有一道身影攔住了他們的去路：「等一下等一下！別走，我找你們找很久啊。」"+"\n"+"「「欸？」」兩人異口同聲地發出困惑的聲音。"+"\n"+"接著，日翔馬上就辨認出了那傢伙的聲音，他根本就是那個熟悉迷霧，那個「Code/140.136」！"+"\n"+"可他們面前並不是一個人，而是一隻貓咪——準確來說，是名為德魯貝的灰色的大胖貓，正在對兩人說話。"+"\n"+"「德魯貝？！你、你……為什麼？！」曉光少見地顯露出驚恐的神色，似乎是對於感到驚訝……再怎麼說，畢竟那可是一隻會說話的貓咪。"+"\n"+"「你……你就是那傢伙嗎？！」日翔也同樣震驚，他想都沒想過，那個讓自己回到大學生活的始作俑者，居然是那隻住在曉光家裡的貓！貓為什麼會寫程式、為什麼那個程式有奇怪的力量、貓咪講話會不會被研究動物的人抓走……這些奇怪的問題全都湧上了日翔的心頭。"+"\n"+"「只有使用『Code/140.136』的人才可以聽見我的聲音，這樣說你們明白嗎？」貓咪的嘴巴沒有張開卻發出了聲音。玻璃珠一般的雙眼盯著兩人，語氣很是愜意。"+"\n"+"使用「Code/140.136」的人？難怪我聽得見他的聲音……不對，這麼說曉光她剛剛也聽見貓咪說話了吧，難道曉光也是使用了那個程式嗎？正當日翔內心有著這樣的疑問而下意識看向曉光時，發現她也是以那樣疑惑的神情看著自己。"+"\n"+"「原來是這樣……」曉光似乎也理解了情形，她的表情逐漸冷靜了下來。"+"\n"+"「唔，程式碼的使用者不只有一人其實也不讓人意外就是了……」日翔對曉光也是使用者這件事也下了結論，可內心還是處於震驚的狀態。"+"\n"+"他們長達四年都沒有發現對方也是Code/140.136的使用者啊……"+"\n"+"「可能也不只有你們，但其他『真善美聖妖精』怎樣幫助你們這些小孩我是不清楚啦。唉，不說這個，你們知道我一隻貓混入捷運裡躲著站務員，再轉乘過來輔大有多辛苦嗎？」德魯貝好像很懊惱地舔了舔自己亂掉的毛。"+"\n"+"可惜兩人好像對德魯貝的訴苦不太買帳。日翔和曉光分別還是提出了與德魯貝辛辛苦苦來輔大無關的問題：「真善美聖妖精是什麼啊？」「為什麼要讓我們回到過去？」"+"\n"+"「欸不是你們怎麼這樣……好啦好啦我一個個回答，這是你們德魯貝的熱心售後服務喔。」德魯貝乖乖坐了下來，在原地打了個呵欠。"+"\n"+"「我先問你們一個問題好了。」"))
                list_talk.append(TextSendMessage(text="#79 「140.136」是屬於哪裡的網域？"+"\n"+"（Ａ）台灣大學"+"\n"+"（Ｂ）新北市政府"+"\n"+"（Ｃ）輔仁大學"+"\n"+"（Ｄ）輔仁大學資訊管理學系"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#79',
                    template=ButtonsTemplate(
                        title='#79',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="台灣大學"
                            ),
                            MessageAction(
                                label='B',
                                text="新北市政府"
                            ),
                            MessageAction(
                                label='C',
                                text="輔仁大學"
                            ),
                            MessageAction(
                                label='D',
                                text="輔仁大學資訊管理學系"
                            )
                        ]
                    )
                )
                list_talk.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="78":
                list_talk=[]
                list_talk.append(TextSendMessage(text="搭上捷運的曉光，偶然間看到日翔的身影，要在同一時間搭上同樣的捷運，實在是運氣很好。"+"\n"+"「日翔、日翔。」曉光出聲打招呼，可是日翔卻在思考什麼而沒有回應。"+"\n"+"只見日翔突然身體震了一下，慢了一拍才看到曉光。"+"\n"+"「欸，曉光？好巧啊。」 回過神的日翔說出這句話。"+"\n"+"「你的東西掉了哦。」只見曉光將手送過來，將某個東西歸還給日向。"+"\n"+"「啊…‥」日翔面露尷尬，原來是他的學生證掉了。而曉光正好想起了大一開學那天，他們的相遇就是因為撿到了對方的學生證，就算那天沒有和日翔說到什麼話，她仍然對於和日翔重新接觸的那一天印象深刻；仔細想起來，都還像是前一刻才發生一樣。"+"\n"+"「大一開學的時候，也是你幫我找到學生證的，好巧。」曉光見到日翔旁邊還有空位，便就順勢坐了下來。"+"\n"+"「嘿嘿、我也在想一樣的事情。或許學生證就是一種我們的緣分吧？俗話說萬事起頭難？」日翔開始回味起了那一天的情景，當時撿到曉光學生證的震驚似乎還留存在腦海之中。"+"\n"+"「我想，」曉光也跟著笑了起來：「我們的『起頭』也可能是那天科博館看展，你怕我落單而主動找我的那一天。」"+"\n"+"「如果以小說來形容的話就像是『序章』一樣重要的東西吧，如果沒有發生的話，會不會我們到現在都還是普通同學呢？」日翔感慨的說著。"+"\n"+"「嗯……或許吧。『有些事』現在看來就跟奇蹟一樣。」曉光也同意了日翔的話。"+"\n"+"於是，兩人不同於初次相見一般在上學路途中無話可講，反而是肩並著肩、有說有笑的前行，變成了無話不談的關係。"))
                list_talk.append(TextSendMessage(text="校園巡禮結束後，就是大四生的畢業典禮了。所有大四生都像開學典禮一樣，每個人都在中美堂穿著學士服，領受天主以及師長們對所有輔仁學士即將啟程的祝福。在畢業典禮的氛圍渲染之下，也有不少珍愛大學生活的畢業生在中美堂裡面哭了出來。"+"\n"+"在畢業典禮結束後，日翔跟曉光兩人一同走出中美堂。中美堂外面人很多，除了畢業的社團發表之外，當然也有許多前來參加畢業典禮的家長。正當曉光看著這熱鬧的情景，心中充滿著五味雜陳的心情，司晨裝作哭哭啼啼的樣子，一邊大喊大叫跑了過來：「阿日！！阿日！你要開心，你要幸福，好不好？ 開心啊，幸福！！！」"+"\n"+"「什麼鬼……你這次又玩什麼梗了？」日翔傻眼。"+"\n"+"「沒有啦哈哈，只是昨天看的一部電影有個女生甩掉男生的時候那個男生說的話，我就模仿了一下啊。」司晨一邊打哈哈裝傻，這才注意到他的浮誇行為再度引起了周圍所有人的注意。"+"\n"+"「哈哈哈哈，哎你這四年倒是一點都沒變啊。」"+"\n"+"「唉唷，說是這麼說，但是我對兄弟你的祝福可是真心的！以後我們就不能一直在一起玩啦，我們彼此在不同地方也要加油啊。」司晨很是真心地對日翔表達祝福之意。"+"\n"+"以後就聽不到他們打打鬧鬧的聲音，也是挺可惜的。曉光看著兩人相聲般的行為想道。"+"\n"+"真澄似乎是從一旁看到了剛才的鬧劇，於是湊上來說道：「我剛剛還想這裡怎麼這麼吵，原來是你啊司晨。」"+"\n"+"「是啊，剛剛還想找你們的，多虧葉司晨一直都這麼吵，傳LINE都免了。」宇桓跟在後頭附議。"+"\n"+"司晨聽見這兩人對自己的吐槽，倒是不滿地開始抗議：「欸X不是啊，林真澄馬宇桓你們什麼意思啦！」"+"\n"+"「只是覺得很可惜以後都聽不到你那麼吵了。」宇桓難得對司晨的蠢行為有了正面的反應。"+"\n"+"「是啊，多虧你多吵了這會，好讓我能夠記得清楚一些。」真澄也沒有嫌棄司晨，倒是不忘對他吐槽一口。"+"\n"+" 「我能夠交到你們這些朋友，真的很開心。」 曉光看著一群人的樣子，很是坦率地表達自己的想法——這些朋友或許不可靠，但確實增添了大學生活的樂趣。"+"\n"+"「大學生活沒有浪費真是太好了。」日翔同意曉光的說法。"+"\n"+"「對了，那個誰不是一直說想吃晶華栢麗廳嗎，我剛好晚上有訂位，姑且給我們五個人當畢業餐。」宇桓看中了話題結束的間隔，突然告知在場的所有人他打算圓圓司晨的夢。"+"\n"+"「哇……真的假的啊宇桓！？晚上的吃到飽不是超貴嗎？」聽到關鍵字，日翔的雙眼也誠實地發亮了起來。"+"\n"+"宇桓面對日翔跟司晨閃亮亮的眼神，似乎有些應對不來：「沒差多少吧。咳、總之，要聊可以晚上見。」語畢，宇桓便頭也不回的走了。"+"\n"+"真澄對此也忍不住評價：「……宇桓他是真的很罩，我真的對他刮目相看了。」"+"\n"+"「做專題的時候也很厲害，再難的工作都可以很快搞定。」曉光似乎也對宇桓的為人有所認可。"))
                list_talk.append(TextSendMessage(text="眾人約好晚上相見之後便離開了學校，唯獨留下了日翔和曉光兩個人。"+"\n"+"正當他們打算離開校園時，有一道身影攔住了他們的去路：「等一下等一下！別走，我找你們找很久啊。」"+"\n"+"「「欸？」」兩人異口同聲地發出困惑的聲音。"+"\n"+"接著，小光馬上就辨認出了那傢伙的聲音，是那道光，那個奇怪的「Code/140.136」！"+"\n"+"可是在他們面前並不是一個人，而是一隻貓咪——準確來說，竟然是曉光家那隻灰色胖貓咪德魯貝。"+"\n"+"「德魯貝？！你、你……為什麼？！」曉光少見地顯露出驚恐的神色，似乎是對於感到驚訝……再怎麼說，畢竟那可是一隻會說話的貓咪。"+"\n"+"「你……你就是那傢伙嗎？！」日翔也同樣震驚，不震驚才奇怪，任誰都沒看過貓咪會說話，貓為什麼會寫程式、為什麼那個程式有奇怪的力量、貓咪講話會不會被研究動物的人抓走……這些問題不斷地浮出在兩人的腦海中。"+"\n"+"「只有使用『Code/140.136』的人才可以聽見我的聲音，這樣說你們明白嗎？」貓咪的嘴巴沒有張開卻發出了聲音。玻璃珠一般的雙眼盯著兩人，語氣很是愜意。"+"\n"+"曉光其實也沒有想過這個可能性，只是真的太天馬行空了，曉光並沒有太仔細的去思考，只是覺得自己想出「那道光就是德魯貝」的想法感到相當天真。"+"\n"+"「原來是這樣……」曉光表情逐漸冷靜了下來。"+"\n"+"「唔，程式碼的使用者不只有一人其實也不讓人意外就是了……」日翔對曉光也是使用者這件事也下了結論，可內心還是處於震驚的狀態。"+"\n"+"他們長達四年都沒有發現對方也是Code/140.136的使用者啊……"+"\n"+"「可能也不只有你們，但其他『真善美聖妖精』怎樣幫助你們這些小孩我是不清楚啦。唉，不說這個，你們知道我一隻貓混入捷運裡躲著站務員，再轉乘過來輔大有多辛苦嗎？」德魯貝好像很懊惱地舔了舔自己亂掉的毛。"+"\n"+"可惜兩人好像對德魯貝的訴苦不太買帳。日翔和曉光分別還是提出了與德魯貝辛辛苦苦來輔大無關的問題：「真善美聖妖精是什麼啊？」「為什麼要讓我們回到過去？」"+"\n"+"「欸不是你們怎麼這樣……好啦好啦我一個個回答，這是你們德魯貝的熱心售後服務喔。」德魯貝乖乖坐了下來，在原地打了個呵欠。"+"\n"+"「我先問你們一個問題好了。」"))
                list_talk.append(TextSendMessage(text="#79 「140.136」是屬於哪裡的網域？"+"\n"+"（Ａ）台灣大學"+"\n"+"（Ｂ）新北市政府"+"\n"+"（Ｃ）輔仁大學"+"\n"+"（Ｄ）輔仁大學資訊管理學系"))
                buttons_template_message = TemplateSendMessage(
                    alt_text='#79',
                    template=ButtonsTemplate(
                        title='#79',
                        text='請選出正確答案',
                        actions=[
                            MessageAction(
                                label='A',
                                text="台灣大學"
                            ),
                            MessageAction(
                                label='B',
                                text="新北市政府"
                            ),
                            MessageAction(
                                label='C',
                                text="輔仁大學"
                            ),
                            MessageAction(
                                label='D',
                                text="輔仁大學資訊管理學系"
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
    elif event.message.text=="輔仁大學":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入、日向視角、Q2=1
            if worksheet.acell(list[0]).value=="1" and worksheet.acell(list[1]).value=="78":
                worksheet.update(list[1],int(79))
                list_talk=[]
                list_talk.append(TextSendMessage(text="德魯貝很滿意地點了點頭，便開始耐心地說明：「真善美聖妖精是輔大的妖精，是什麼不太重要，總之它只是一個種族名稱。日翔，我應該跟你說我們是互惠互利吧？我想你之前就對我是不是小時候你撿到的貓咪有所猜測了，我的回答是：『沒錯，就是我』。至於曉光，妳是我的主人，我也對妳有所感恩。至於除了『感恩』之外要讓你們回歸大一的理由還有一個——很簡單，我是來掙罐罐的。」"+"\n"+"曉光對他的「另一個理由」深感疑惑：「掙罐罐？」"+"\n"+"只見德魯貝輕鬆地回答：「沒錯，如果日翔跟曉光以後真的結婚，那我的未來就是由兩位善心的孩子飼養我啦，你看你看，人類供奉貓咪美好的高級罐罐，這樣的生活豈不是很棒嗎！」"+"\n"+"日翔對德魯貝有意撮和兩人的話語很是意外……自己能追到曉光居然有一隻貓的功勞，但此刻似乎也只能吐槽一番：「什麼鬼啊……就因為這種原因嗎？」"+"\n"+"「我就說了是互惠互利。至少你們確實得到了改變未來的機會吧？你們不是都對當初畢業後自己的樣子感到懊惱嗎，我可是知道的。」貓咪發出了很是自豪的聲音。"+"\n"+"日翔和曉光看了看彼此，想到了能夠回想起兒時回憶也是因為這隻貓咪給了兩人回到過去的機會，似乎也很同意德魯貝說的話。"+"\n"+"「說來，我真的得對回到過去這件事上感謝你啊。」"+"\n"+"「嗯，謝謝你，德魯貝。」"+"\n"+"「真是的，我也不想由別人之手掙罐罐的。我跟你們說啊，要不是我沒手指，不然依照我這個能讓你們回到過去的能力來coding，我一定是年薪百萬，不，千萬的工程師。……不過，你們確實讓我很自豪，兩人比起上次都有著不小的改變啊。」德魯貝開始逕自多嘴了起來：「你們都擁有兩次大學生活的機會，但對一般人而言這樣的青春只會有僅僅一次，過了就沒了！舉凡讀書、交朋友、找伴侶、社團還是實習、或是尋找未來，都沒有例外。我想你們經過了這次，應該就十分明白了吧？"+"\n"+"無論什麼時候，即使畢業了、走出了校園，都要做為堅強的輔仁學子，不要虛度自己的人生。」"))
                list_talk.append(TextSendMessage(text="兩人攢緊了彼此的手，像是以這樣的動作向未來的日子道出無聲的誓約——珍惜當下、珍惜你我身邊的美好，陽光或許高掛在遙遠的天空，也或許早就在肩側默默閃耀，等待誰去擁抱。"+"\n"+"他們之間，還有千千萬萬的未來等待著綻放。"))
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/i8xodQ8.jpg', preview_image_url='https://i.imgur.com/i8xodQ8.jpg'))
                list_talk.append(TextSendMessage(text="「那為什麼要今天才告訴我們真相啊？」"+"\n"+"「儀式感啊，你們不覺得畢業典禮再一次公開很刺激嗎？」"+"\n"+"「喂，……你果然很我行我素啊德魯貝。」")) 
                list_talk.append(TextSendMessage(text="恭喜玩家完成遊戲🥳"+"\n"+"想從曉光視角觀看故事請輸入「重置遊戲」重新選擇視角！"+"\n"+"遊玩上有任何問題或想回饋給我們的意見請點選選單「聯絡管理員」告訴我們！再次感謝玩家的遊玩～"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value=="2" and worksheet.acell(list[1]).value=="78":
                worksheet.update(list[1],int(79))
                list_talk=[]
                list_talk.append(TextSendMessage(text="德魯貝很滿意地點了點頭，便開始耐心地說明：「真善美聖妖精是輔大的妖精，是什麼不太重要，總之它只是一個種族名稱。日翔，我應該跟你說我們是互惠互利吧？我想你之前就對我是不是小時候你撿到的貓咪有所猜測了，我的回答是：『沒錯，就是我』。至於曉光，妳是我的主人，我也對妳有所感恩。至於除了『感恩』之外要讓你們回歸大一的理由還有一個——很簡單，我是來掙罐罐的。」"+"\n"+"「掙罐罐？」曉光對他的「另一個理由」深感疑惑。"+"\n"+"只見德魯貝輕鬆地回答：「沒錯，如果日翔跟曉光以後真的結婚，那我的未來就是由兩位善心的孩子飼養我啦，你看你看，人類供奉貓咪美好的高級罐罐，這樣的生活豈不是很棒嗎！」"+"\n"+"日翔對德魯貝有意撮和兩人的話語很是意外……但是此刻似乎也只能吐槽一番：「什麼鬼啊……就因為這種原因嗎？」"+"\n"+"「我就說了是互惠互利。至少你們確實得到了改變未來的機會吧？你們不是都對當初畢業後自己的樣子感到懊惱嗎，我可是知道的。」貓咪發出了很是自豪的聲音。"+"\n"+"日翔和曉光看了看彼此，想到了能夠回想起兒時回憶也是因為這隻貓咪給了兩人回到過去的機會，似乎也很同意德魯貝說的話。"+"\n"+"「說來，我真的得對回到過去這件事上感謝你啊。」"+"\n"+"「嗯，謝謝你，德魯貝。」"+"\n"+"「真是的，我也不想由別人之手掙罐罐的。我跟你們說啊，要不是我沒手指，不然依照我這個能讓你們回到過去的能力來coding，我一定是年薪百萬，不，千萬的工程師。……不過，你們確實讓我很自豪，兩人比起上次都有著不小的改變啊。」德魯貝開始逕自多嘴了起來：「你們都擁有兩次大學生活的機會，但對一般人而言這樣的青春只會有僅僅一次，過了就沒了！舉凡讀書、交朋友、找伴侶、社團還是實習、或是尋找未來，都沒有例外。我想你們經過了這次，應該就十分明白了吧？"+"\n"+"無論什麼時候，即使畢業了、走出了校園，都要做為堅強的輔仁學子，不要虛度自己的人生。」"))
                list_talk.append(TextSendMessage(text="兩人攢緊了彼此的手，像是以這樣的動作向未來的日子道出無聲的誓約——珍惜當下、珍惜你我身邊的美好，陽光或許高掛在遙遠的天空，也或許早就在肩側默默閃耀，等待誰去擁抱。"+"\n"+"他們之間，還有千千萬萬的未來等待著綻放。"))
                list_talk.append(ImageSendMessage(original_content_url='https://i.imgur.com/i8xodQ8.jpg', preview_image_url='https://i.imgur.com/i8xodQ8.jpg'))
                list_talk.append(TextSendMessage(text="「那為什麼要今天才告訴我們真相啊？」"+"\n"+"「儀式感啊，你們不覺得畢業典禮再一次公開很刺激嗎？」"+"\n"+"「喂，……你果然很我行我素啊德魯貝。」")) 
                list_talk.append(TextSendMessage(text="恭喜玩家完成遊戲🥳"+"\n"+"想從日翔視角觀看故事請輸入「重置遊戲」重新選擇視角！"+"\n"+"遊玩上有任何問題或想回饋給我們的意見請點選選單「聯絡管理員」告訴我們！再次感謝玩家的遊玩～"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

    elif event.message.text=="遊戲規則":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您有一封來自Code/140.136的遊戲須知❗️✉️"+"\n"+"本遊戲採回答問題的方式進行闖關，玩家將透過回答題目一步步解鎖故事劇情和新關卡✨"+"\n"+"我們提供以下工具幫助您破解關卡👊🏻"+"\n"+"工具1️⃣-遊戲地圖：校園建築物大揭密！點擊查看解鎖進度🏫"+"\n"+"工具2️⃣-個人檔案：在玩家個人檔案中可查看目前選擇的遊戲視角、已解鎖的記憶物件數。"+"\n"+"工具3️⃣-關卡提示：我們鼓勵玩家動腦破解題目，但真的卡關時還是可以參考提示網站🧐"+"\n"+"工具4️⃣-遊戲規則：忘記遊戲規則的玩家，可再次點擊查看！"+"\n"+"工具5️⃣-人物介紹：關於劇情角色的所有秘密，快來認識他們吧~"+"\n"+"工具6️⃣-聯絡管理員：有任何疑問與狀況，歡迎聯繫開發團隊，將有專人為您解答🗣"+"\n"+"工具7️⃣-現在題目：忘記或遺失題目請輸入「現在題目」，可以查看現在的關卡喔🤝"+"\n"+"最後！玩家若想重新體驗遊戲或選擇不同視角可以輸入「重置遊戲」喔✨"+"\n"+"祝各位玩家遊玩愉快🥳"))
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
            list.append('E'+str(j))
            ques=str(int(worksheet.acell(list[3]).value)+1)
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
            #日向視角&物件9
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="9":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【9/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/bncQTAE.png',
                                action=MessageTemplateAction(
                                    label='照片介紹',
                                    text='照片介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件10
            elif worksheet.acell(list[2]).value=="1" and worksheet.acell(list[1]).value=="10":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：日翔"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【10/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/bncQTAE.png',
                                action=MessageTemplateAction(
                                    label='照片介紹',
                                    text='照片介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/IkA7fXf.png',
                                action=MessageTemplateAction(
                                    label='信紙介紹',
                                    text='信紙介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #小光視角&物件0
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="0":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【0/10】"))
                list_talk.append(TextSendMessage(text="還沒解鎖物件喔！趕快去過關解鎖吧！"))
                line_bot_api.reply_message(event.reply_token, list_talk)
            #日向視角&物件1
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【1/10】"))
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
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="2":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【2/10】"))
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
            #曉光視角&物件3
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="3":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【3/10】"))
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
            #曉光視角&物件4
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="4":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【4/10】"))
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
            #曉光視角&物件5
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="5":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【5/10】"))
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
            #曉光視角&物件6
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="6":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【6/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
            #曉光視角&物件7
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="7":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【7/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
            #曉光視角&物件8
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="8":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【8/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
            #曉光視角&物件9
            elif worksheet.acell(list[2]).value=="2" and worksheet.acell(list[1]).value=="9":
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【9/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/bncQTAE.png',
                                action=MessageTemplateAction(
                                    label='照片介紹',
                                    text='照片介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
            #曉光視角&物件10
            else:
                list_talk=[]
                list_talk.append(TextSendMessage(text="玩家選擇視角：曉光"+"\n"+"目前關卡：#"+ques+"\n"+"解鎖物件數：【10/10】"))
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
                                image_url='https://i.imgur.com/cpu3ksv.png',
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
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/bncQTAE.png',
                                action=MessageTemplateAction(
                                    label='照片介紹',
                                    text='照片介紹'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url='https://i.imgur.com/IkA7fXf.png',
                                action=MessageTemplateAction(
                                    label='信紙介紹',
                                    text='信紙介紹'
                                )
                            )
                        ]
                    )
                )
                list_talk.append(image_carousel_template_message)
                line_bot_api.reply_message(event.reply_token, list_talk)
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
    elif event.message.text=="照片介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="一張略有泛黃的相片，夕暉之下的窗邊有著一個男孩跟一個女孩的背影，仔細一看可以發現他們在勾勾手，像是在做著什麼約定。考慮到場景是幼稚園，應該是由老師拍攝下來的。"))
    elif event.message.text=="信紙介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收在日翔家裡的斑駁信紙。由於保存了一段時間，上頭的字有些模糊，不過可以看得出內容是某位女孩在過去向某位男孩的告白。"))

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
    elif event.message.text=="現在題目":
        userid_list=worksheet.col_values(1)
        #ID已寫入
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('D'+str(j))
            list.append('E'+str(j))
            #ID已寫入且未選擇視角
            if worksheet.acell(list[0]).value=="0":
                list_talk=[]
                list_talk.append(TextSendMessage("還沒選遊戲擇視角，請選擇"))
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
            #ID已寫入
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="0":
                list_talk=[]
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/06/q4DPkj.png', preview_image_url='https://upload.cc/i1/2022/03/06/q4DPkj.png'))
                list_talk.append(TextSendMessage("#1 檔案只有短短幾行程式碼，請問該輸入什麼才能執行此函式，讓結果非None呢？（請輸入半形英文字母）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="1":
                list_talk=[]
                list_talk.append(TextSendMessage("#2 要出發去學校了，輔大的地址是？（請以「ＯＯ市ＯＯ區ＯＯ路ＯＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="2":
                list_talk=[]
                list_talk.append(TextSendMessage("#3 請問離校園最近的捷運出口爲？（請以「Ｏ號」回答。Ｏ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="3":
                list_talk=[]
                list_talk.append(TextSendMessage("#4 曉光的學號是「408402132」，請問曉光是民國幾年入學、甲班還是乙班、座號幾號呢？（請以「ＯＯ年、Ｏ班、ＯＯ號」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="4":
                list_talk=[]
                list_talk.append(TextSendMessage("#5 輔大英文全名是？"+"\n"+"（Ａ）Fu Jen Catholic University"+"\n"+"（Ｂ）Fu Jen Christian University"+"\n"+"（Ｃ）Fang Jia University"))
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="5":
                list_talk=[]
                list_talk.append(TextSendMessage("#6 「LM」指的是哪棟大樓呢？（請以「ＯＯＯ大樓」回答。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="6":
                list_talk=[]
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="7":
                list_talk=[]
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="8":
                list_talk=[]
                list_talk.append(TextSendMessage("#9 學校外面藏有很多美食的小巷叫？（請輸入「ＯＯＯ巷」回答，ＯＯＯ為半形數字。）"))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="9":
                list_talk=[]
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="10":
                list_talk=[]
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="11":
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="12":
                list_talk=[]
                list_talk.append(TextSendMessage(text="#13 請問下圖最後會出現什麼結果？（請以「Ｏ」回答，Ｏ為半形數字。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/10/J106XE.png', preview_image_url='https://upload.cc/i1/2022/03/10/J106XE.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="13":
                list_talk=[]
                list_talk.append(TextSendMessage(text="#14 下列以Python語法撰寫出的程式碼最後輸出結果為？（請以「x=Ｏ」回答，Ｏ數量不代表實際答案字數。）"))
                list_talk.append(ImageSendMessage(original_content_url='https://upload.cc/i1/2022/03/25/uHLoSw.png', preview_image_url='https://upload.cc/i1/2022/03/25/uHLoSw.png'))
                line_bot_api.reply_message(event.reply_token,list_talk)
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="14":
                list_talk=[]
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
            elif worksheet.acell(list[0]).value!="0" and worksheet.acell(list[1]).value=="15":
                list_talk=[]
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
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))
    elif event.message.text=="DDD":
        list_talk=[]
        buttons_template_message = TemplateSendMessage(
            alt_text='臭甲',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/neBOLvG_d.webp?maxwidth=640&shape=thumb&fidelity=medium',
                title='恭喜！',
                text='你找到臭甲財富密碼，請問要花費購買宇桓DLC嗎？',
                actions=[
                    MessageAction(
                        label='讓我看宇日',
                        text='讓我看宇日'
                    ),
                    MessageAction(
                        label='等一等，不可以',
                        text='等一等，不可以'
                    )
                ]
            )
        )
        list_talk.append(buttons_template_message)
        line_bot_api.reply_message(event.reply_token,list_talk)
    elif event.message.text=="JÄTTESTOR":
        list_talk=[]
        buttons_template_message = TemplateSendMessage(
            alt_text='臭甲',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2022/03/08/Baezmv.jpg',
                title='恭喜！',
                text='你找到臭甲財富密碼，請問要花費購買司晨DLC嗎？',
                actions=[
                    MessageAction(
                        label='讓我看司日',
                        text='讓我看司日'
                    ),
                    MessageAction(
                        label='等一等，不可以',
                        text='等一等，不可以'
                    )
                ]
            )
        )
        list_talk.append(buttons_template_message)
        line_bot_api.reply_message(event.reply_token,list_talk)
    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)