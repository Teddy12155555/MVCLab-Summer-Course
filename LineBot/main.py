from fastapi import FastAPI, Request, Response
from typing import Optional
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = FastAPI()

CHANNEL_ACCESS_TOKEN = 'asFNhw2Th+xWFsOxcaJ7MhL+Et9OKoAQKnsjgtEbevVkS0u4E2fXRavGJl6cCYEWmydyPPfWO4v75zus0ft3H1mx/ngBFrit5qw2848xYGBT/OH8ZG/bEIFNLU4VBMqbt/Q7lS/hmIQmKzZydO09pwdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'c31eff1a497b39443fefeb349c826638'
CHANNEL_ID = 'U9074d7f0b8a8f845592e778a48b73a17'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) # Add your line 
handler = WebhookHandler(CHANNEL_SECRET) # Add your line developer channel secret key

line_bot_api.push_message(CHANNEL_ID, TextSendMessage(text='You Can Start Now'))

@app.get('/hello')
def hello_word():
    return {"hello" : "world"}

@app.post('/message')
async def hello_word(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    
    try:
      handler.handle(body.decode('UTF-8'), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        if event.message.text == 'hello' : 
            sendMessage(event,"hello, here you are")
        else:
            echo(event)
    
def echo(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
        
def sendMessage(event,message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))