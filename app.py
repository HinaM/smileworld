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

    elif event.message.text=="決鬥":
        deck=["EM","DD","幻奏","魔玩具","超重武者","魔界劇團","花札衛","捕食植物"]
        draw= random.choice(deck)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=draw))

    elif "微笑宇宙" == event.message.text:
        buttons_template = TemplateSendMessage(
            template=ButtonsTemplate(
                title='猜謎決鬥',
                text='遊矢的王牌卡片是？',
                thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Ftwitter.com%2Fyamataika135%2Fstatus%2F1063268603980480513&psig=AOvVaw1tUuI1Vp5havtKzL4crB9n&ust=1643831963796000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJiq8Lul3_UCFQAAAAAdAAAAABAJ',
                actions=[
                    MessageTemplateAction(
                    label='動作卡',
                    text='動作卡'
                    ),
                    MessageTemplateAction(
                    label='EM族',
                    text='EM族'
                    ),
                    URITemplateAction(
                        label='異色眼靈擺龍',
                        uri='異色眼靈擺龍'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif event.message.text=="動作卡":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="對了"))
    elif event.message.text=="EM族":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯了"))
    elif event.message.text=="異色眼靈擺龍":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="錯了"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)