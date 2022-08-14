import os
import re
import json
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv() # Load your local environment variables

# Pokedex Link
pokemons_link = 'https://pokemondb.net/pokedex/all'
# Get all info from link (html)
doc = PyQuery(url=pokemons_link).find('td').find('span').children()
# Create My_pokedex Images Dict
pokemons_imgs = dict()
# For filter the empty image from link
empty_img_url = 'https://img.pokemondb.net/s.png'
# Add each pokemon img url into dict
for poke in doc:
    poke = PyQuery(poke)
    # Filter empty img
    if not re.match(poke.attr('data-src'), empty_img_url):
        poke_url = poke.attr('data-src') # Attribute['data-src'] value
        poke_name = str(poke_url).split('/')[-1][:-4].lower() # Get lower case of a pokemon name & filter .png behind
        # Save a pokemon's img info
        pokemons_imgs[poke_name] = poke_url

app = FastAPI()

CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

'''
For first testing, you can comment the code below after you check your linebot can send you the message below
'''
CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID
# My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='Welcome to my pokedex !')) # Push a testing message

@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and 
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# Events for message reply
my_event = ['#getpokemon', '#mypokemon', '#addpokemon', '#delpokemon', '#help']
# My pokemon datas
my_pokemons = dict()
poke_file = 'my_pokemons.json'
# Load local json file if exist
if os.path.exists(poke_file):
    with open(poke_file, 'r') as f:
        my_pokemons = json.load(f)

# All message events are handling at here !
@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    ''' Basic Message Reply
    message = TextSendMessage(text= event.message.text)
    My_LineBotAPI.reply_message(
        event.reply_token,
        message
    )
    '''
    recieve_message = str(event.message.text).split(' ')
    case_ = recieve_message[0].lower().strip()
    # Case 1: get pokemon
    if re.match(my_event[0], case_):
        pokename = recieve_message[1].lower().strip()
        if pokename in pokemons_imgs.keys():
            url = pokemons_imgs[pokename]
            # Return image
            My_LineBotAPI.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
            )
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text='Pokemon not found in pokedex !')
            )
    # Case 2: show my pokemons (if existed)
    elif re.match(my_event[1], case_):
        if len(my_pokemons):
            message = 'Here is your pokemons :\n'
            for idx, pokename in enumerate(my_pokemons.keys(), 1):
                # Send Poke name
                message += str(idx) + ': ' + pokename + '\n'
            # LineBot Reply Message can only send up to 5, otherwise you will see an error in console
            # LineBot event reply_token can only be used once !
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text=message)
            )
        else:
            My_LineBotAPI.push_message(
                event.reply_token,
                TextSendMessage(text='You don\'t have any pokemon')
            )
    # Case 3: add a pokemon into my pokedex
    elif re.match(my_event[2], case_):
        pokename = recieve_message[1].lower().strip()
        if pokename in pokemons_imgs.keys():
            if pokename in my_pokemons.keys():
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'You have already add {pokename} into your pokedex !')
                )
            else:
                # Add a new pokemon into my pokedex
                my_pokemons[pokename] = pokemons_imgs[pokename]
                with open(poke_file, 'w') as f:
                    json.dump(my_pokemons, f, indent=4)
                # Reply successful message
                My_LineBotAPI.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'Successful add {pokename} into your pokedex !')
                )
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text=f'Pokemon "{pokename}" not found in global pokedex !')
            )
    # Case 3: Delete a pokemon from my pokedex
    elif re.match(my_event[3], case_):
        pokename = recieve_message[1].lower().strip()
        if pokename in my_pokemons.keys():
            # Remove an existed pokemon in my pokedex
            my_pokemons.pop(pokename)
            with open(poke_file, 'w') as f:
                json.dump(my_pokemons, f, indent=4)
            # Reply successful message
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text=f'Successful delete {pokename} from your pokedex !')
            )
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text=f'Pokemon "{pokename}" not found in your pokedex !')
            )
    # Help command for listing all commands to user
    elif re.match(my_event[4], case_):
        command_describtion = 'Commands:\n\
        #getpokemon <pokemon\'s name>\n\t-->Show this pokemon\'s name & Image for you if existed !\n\
        #mypokemon\n\t-->List all pokemons in your pokedex if existed !\n\
        #addpokemon <pokemon\'s name>\n\t-->Add a pokemon from global pokedex into your pokedex if existed !\n\
        #delpokemon <pokemon\'s name>\n\t-->Delete a pokemon from your pokedex if existed !\n'
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(text=command_describtion)
        )
    else:
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(text='Welcome to my pokedex ! Enter "#help" for commands !')
        )
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)