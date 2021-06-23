from telethon import TelegramClient, events, sync
import os
from dotenv import load_dotenv
load_dotenv()
import logging
import emoji

level=logging.ERROR     # will only show errors that you didn't handle

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# get the api key from the env file
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
Bot_TOKEN = os.getenv("API_KEY")

print(Bot_TOKEN)

#creating Client
client = TelegramClient('NewSession', API_ID, API_HASH)
client.start(bot_token=Bot_TOKEN)

#get the client info
# print(client.get_me().stringify())



# @client.on(events.NewMessage(pattern='/start'))
# async def questions(event):
#     await event.respond('Hello! Talking to you from Telethon')

chat="@test2GossipPartnerBot" 

@client.on(events.NewMessage(pattern='(?i)hi|hello'))
async def handler(event):
    # await event.respond('Hey!, what is your favorite emoji?!')
     # Good
    # chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    # <you> denotes outgoing messages you sent
    # <usr> denotes incoming response messages
    async with event.client.conversation(chat) as conv:
        # <you> Hi!
        await conv.send_message(event.chat_id,'Hey!, what is your favorite emoji?!')

        # <usr> Hello!
        hello = await conv.get_response(0)

        # <you> Please tell me your name
        await conv.send_message(event.chat_id,'Please tell me your name')

        # <usr> ?
        name = await conv.get_response(0).raw_text

        while not any(x.isalpha() for x in name):
            # <you> Your name didn't have any letters! Try again
            await conv.send_message(event.chat_id,"Your name didn't have any letters! Try again")

            # <usr> Human
            name = await conv.get_response(0)
        print("response", name)
            

    # <you> Thanks Human!
    await conv.send_message(event.chat_id,'Thanks {}!'.format(name))
    
    


# @client.on(events.NewMessage(pattern=r"(?:\u263a|\U0001f645)"))
# async def get_emoji(event):  
#   print(event.message)

client.run_until_disconnected()



