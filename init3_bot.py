from telethon import TelegramClient, events, sync, Button
import os
from dotenv import load_dotenv
load_dotenv()
import logging
import emoji
import asyncio


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



@client.on(events.NewMessage(pattern='/start'))
async def questions(event):
    await event.respond('Hello! Talking to you from Telethon')

@client.on(events.NewMessage(pattern='(?i)hi|hello'))
async def handler(event):
    print(event)
    async with event.client.conversation(event.chat) as conv:
      await conv.send_message('Hey!, what is your favorite emoji?!')
      
      # Try to get emoji response many times until we get a qualifying emoji or user confirms this is really what they want as their favorite
      while True:
        response = await conv.get_response()
        print('response',response)
        await asyncio.sleep(1)

        _foundemoji = False
        for em in emoji.UNICODE_EMOJI['en']:
          if em in response.message:
            _foundemoji = True
            break # break out of this for loop

        if _foundemoji:
            print('found emoji in string',response)
            await conv.send_message('thanks!')
            break # break out of while loop
        else:
          await conv.send_message(f'Are you sure this "{response.message}" is your emoji?', buttons=[ [Button.inline('yes'), Button.inline('no')] ] )
          print('event2',event)
          print('chat2',event.chat)
          print('chatid2',event.chat.id)

          response = await conv.wait_event(events.CallbackQuery(chats= event.chat.id ))
          print('response2',response)

          if response.data == b'yes':
            await conv.send_message('ok!')
            break
          else:
            await conv.send_message('ok, so what is your *actual* favorite emoji?')

        await asyncio.sleep(1)

        print(response)
      

@client.on(events.CallbackQuery)
async def clicked(event):
    await event.edit(f'Thank you for clicking {event.data}!')

@client.on(events.NewMessage(pattern='(?i)test'))
async def test(event):
  await client.send_message(event.chat, 'A single button, with "clk1" as data', buttons=Button.inline('Click me', b'clk1'))
  
  # await event.reply('A single button, with "clk1" as data', buttons=Button.inline('Click me', b'clk1'))

  await client.send_message(event.chat, 'Pick one from this grid', buttons=[
      [Button.inline('Left'), Button.inline('Right')],
      [Button.url('Check this site!', 'https://lonamiwebs.github.io')]
  ])

@client.on(events.NewMessage(pattern=r"(?:\u263a|\U0001f645)"))
async def get_emoji(event):  
  print('Emoji',event.message)

client.run_until_disconnected()
