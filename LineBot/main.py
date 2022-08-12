from imp import reload
import os
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = FastAPI()

CHANNEL_TOKEN = os.getenv('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

print(CHANNEL_TOKEN)

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

'''
For first testing, you can comment the code below after you check your linebot can send you the message below
'''
CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID
My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='If you see this, you can start now')) # Push a testing message

@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and 
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# All message events are handling at here !
@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    message = event.message.text
    My_LineBotAPI.reply_message(
        event.reply_token,
        message
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)