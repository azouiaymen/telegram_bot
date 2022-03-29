import urllib
import requests
from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters
import os



PORT = int(os.environ.get('PORT', '8443'))

def shortenlink(link):
    key = '256a06f4e8402e13975921ab896ad35c18cc9'
    url = urllib.parse.quote(link)
    name  = ''
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, name))
    return r.json()["url"]["shortLink"]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to URL downloader!\nPlease provide a valid url')


def textHandler(update: Update, context: CallbackContext) -> None:
    user_message = str(update.message.text)

    if update.message.parse_entities(types=MessageEntity.URL):
        update.message.reply_text(text='You sent a valid URL!', quote=True)        
        update.message.reply_text(text=f'Your shotned url is: {shortenlink(user_message)}')
    else :
        update.message.reply_text(text='the url you sent is wrong, please retry !', quote=True)   
        

def main():
    TOKEN = "5134166036:AAHqG6UEKrbs-m9BXC_Pvxc8VvYfivQVXvI"

    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, textHandler, run_async=True))
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://aymen-bot.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()

