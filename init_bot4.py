from telethon import TelegramClient, client, events, sync, Button
import os
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()

level = logging.ERROR


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("API_KEY")


client = TelegramClient("New", API_ID, API_HASH)

print("The bot is runnng..!!")
@client.on(events.NewMessage)
async def my_event_handler(event):
  if "hello" in event.raw_text:
    await event.reply("Hi!")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event):
  if event.is_reply:
    replied = await event.get_reply_message()
    print('replied', replied)
    sender = replied.sender
    await client.download_profile_photo(sender)
    await event.respond('saved your photo {}'.format(sender.username))

@client.on(events.NewMessage(pattern=r'(?i).*heck'))
async def handler(event):
  await event.delete()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
