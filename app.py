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

    elif event.message.text=="微笑世界":
        reply_arr=[]
        reply_arr.append(TextSendMessage("決帶笑") )
        reply_arr.append(TextSendMessage("デュエルで、笑顔を"))
        line_bot_api.reply_message(event.reply_token, reply_arr)
    
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
                                title='猜謎決鬥',
                                text='哪張卡片是遊矢的王牌',
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
                                        label='時讀、星讀魔術師',
                                        text='時讀、星讀魔術師'
                                    )
                                ]
                            )
                        )
                    )
    elif event.message.text=="動作卡":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="對ㄌ"))
    elif event.message.text=="EM族":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯ㄌ"))
    elif event.message.text=="時讀、星讀魔術師":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯ㄌ"))
    
    elif event.message.text=="表格":
        user_id=event.source.user_id
        worksheet.update('A2', user_id)

    elif event.message.text=="人物介紹":
        carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://wiki.komica.org/images/thumb/d/d1/Img18353.jpg/400px-Img18353.jpg',
                title='張日向',
                text='m',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu3',
                text='description3',
                actions=[
                    PostbackAction(
                        label='postback3',
                        display_text='postback text3',
                        data='action=buy&itemid=3'
                    ),
                    MessageAction(
                        label='message3',
                        text='message text3'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback4',
                        display_text='postback text4',
                        data='action=buy&itemid=4'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    )
                ]
            )
        ]
    )
)
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    elif event.message.text=="開始遊戲":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            #
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經開始遊戲，要重置嗎"))
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

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
        

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)