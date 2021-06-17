import telebot
import os
from dotenv import load_dotenv
load_dotenv()

# get the api key from the env file
API_KEY = os.getenv("API_KEY")


if len(API_KEY)<20:
    raise Exception(f'Invalid TOKEN: {API_KEY}')

#initiate the bot instance 
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, 'Howdy, how are you doing?')

@bot.message_handler(func=lambda message:True)
def echo_all(message):
  bot.reply_to(message, message.text)


#to start the bot
bot.polling()