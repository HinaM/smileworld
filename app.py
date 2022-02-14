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
def handle_message(event):
    message=event.message.text
    message=message.encode('utf-8')
    if event.message.text=="識別碼":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))

    elif event.message.text=="榊遊矢":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="お楽しみはこれから"))

    elif event.message.text=="可用關鍵字":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="開始遊戲、榊遊矢、微笑世界、抽卡、微笑宇宙、人物介紹、角色好感度"))

    elif event.message.text=="微笑世界":
        reply_arr=[]
        reply_arr.append(TextSendMessage("決帶笑") )
        reply_arr.append(TextSendMessage("デュエルで、笑顔を"))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="デュエルで、笑顔を"))
    
    elif event.message.text=="名稱":
        user_id = event.source.user_id         
        profile = line_bot_api.get_profile(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=profile.display_name))

    elif event.message.text=="抽卡":
        deck=["黑魔導","E-HERO新宇俠","星塵龍","No.39希望皇霍普","異色眼靈擺龍","解碼語者"]
        draw= random.choice(deck)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=draw))
    
    elif event.message.text=="微笑宇宙":
        line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='猜謎決鬥，只能用手機玩',
                            template=ButtonsTemplate(
                                thumbnail_image_url='https://i.imgur.com/j6THk84.png',
                                title='猜謎決鬥',
                                text='哪些卡片是遊矢的王牌',
                                actions=[
                                    MessageTemplateAction(
                                        label='動作卡',
                                        text='動作卡'
                                    ),
                                    MessageTemplateAction(
                                        label='EM族',
                                        text='EM族'
                                    ),
                                    MessageTemplateAction(
                                        label='異色眼靈擺龍',
                                        text='異色眼靈擺龍'
                                    )
                                ]
                            )
                        )
                    )
    elif event.message.text=="動作卡":
        #reply_arr=[]
        #reply_arr.append(TextSendMessage(text="對ㄌ。"+"\n"+"出身於弱小私塾——日勝塾的日向，決鬥風格以動作娛樂決鬥聞名，擅長尋找散落各處的動作卡。一起長大的凱茹也擅長將動作卡加入牌組思考策略，玉山更是直言「動作決鬥就是我們槍兵的決鬥風格」。"+"\n"+"凱茹好感度+10、玉山好感度+10"))
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackAction(
                        label='postback',
                        display_text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        #reply_arr.append(buttons_template_message)
        line_bot_api.reply_message(event.reply_token,buttons_template_message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="對ㄌ。"+"\n"+"出身於弱小私塾——日勝塾的日向，決鬥風格以動作娛樂決鬥聞名，擅長尋找散落各處的動作卡。一起長大的凱茹也擅長將動作卡加入牌組思考策略，玉山更是直言「動作決鬥就是我們槍兵的決鬥風格」。"+"\n"+"凱茹好感度+10、玉山好感度+10"))
    elif event.message.text=="EM族":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯ㄌ"))
    elif event.message.text=="異色眼靈擺龍":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯ㄌ"))

    elif event.message.text=="人物介紹":
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://dic.nicovideo.jp/oekaki/725601.png',
                        title='張日向',
                        text='男主角',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='張日向'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.komicolle.org/2019-04/15566418114917.jpg',
                        title='何愷茹',
                        text='女主角',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='何愷茹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://5.share.photo.xuite.net/davidyea2006/15c7ae8/19334735/1060636313_x.jpg',
                        title='葉司',
                        text='男主朋友',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='葉司'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ygodl.com/wp-content/uploads/2021/09/5_Moment.jpg',
                        title='馬玉山',
                        text='學霸',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='馬玉山'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    elif event.message.text=="張日向":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="萬年吊車尾的日向，竟誤打誤撞的考上了輔大資管系，還遇到自己的真命天女—愷茹。為了要讓愷茹喜歡上他，日向開始努力讀書，希望有一天能被愷茹看見。"))
    elif event.message.text=="何愷茹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以全校第一的成績進入輔大資管系，無論何時何地都在讀書。平時都擺著一張撲克臉，讓人難以親近的樣子。不過一看到小動物時，臉上總是洋溢著幸福的笑容。"))
    elif event.message.text=="葉司":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="大二才轉學過來的轉學生，是日向的死黨。和日向一起去打籃球、吃飯、上課，雖然偶爾冒冒失失的，但是總是把朋友擺在第一位，常常把「兄弟就是要有福同享、有難同當阿」掛在嘴邊。"))
    elif event.message.text=="馬玉山":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="「萬般皆下品，唯有決鬥高」是他的人生名言，與愷茹角逐班上的一二名。玉山也喜歡日向，為了不讓日向一直靠近愷茹，因此常常提出問題刁難日向。"))

    elif event.message.text=="角色好感度":
        userid_list=worksheet.col_values(1)
        list=[]
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    x=i+1
            list.append('B'+str(x))
            list.append('C'+str(x))
            list.append('D'+str(x))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="凱茹好感度："+worksheet.acell(list[2]).value+"\n"+"司好感度："+worksheet.acell(list[0]).value+"\n"+"玉山好感度："+worksheet.acell(list[1]).value))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒開始遊戲，按下開始遊戲建立個人檔案"))

    elif event.message.text=="開始遊戲":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經開始遊戲，請輸入「進行遊戲」開始遊玩，要重置請輸入「重新開始」"))
        else:
            x=len(userid_list)
            list=[]
            for i in range(65,76):
                list.append(chr(i)+str(x+1))
            #ID
            worksheet.update(list[0],event.source.user_id)
            #初始值設定
            for i in range(1,5):
                worksheet.update(list[i],int(0))
            worksheet.update(list[5],int(1))
            for i in range(6,11):
                worksheet.update(list[i],int(0))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已開始遊戲"))

    elif event.message.text=="重新開始":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            x=len(userid_list)
            list=[]
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    x=i
            for i in range(65,76):
                list.append(chr(i)+str(x+1))
            #初始值設定
            for i in range(1,5):
                worksheet.update(list[i],int(0))
            worksheet.update(list[5],int(1))
            for i in range(6,11):
                worksheet.update(list[i],int(0))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已重置遊戲"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒開始遊戲，按下開始遊戲建立個人檔案"))
    
    #施工中
    elif event.message.text=="進行遊戲":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="。"))    

    else:
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/536263c581f68d6a929bcbcf7191928a.png', preview_image_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/536263c581f68d6a929bcbcf7191928a.png'))
        

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)