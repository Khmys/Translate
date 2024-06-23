import logging
import asyncio
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import swtr
from config import TOKEN



# Command handler kwa amri ya /start
def start_command(update, context):
    fname = update.message.chat.first_name
    atxt = f"Karibu {fname}! Tuma ujumbe nitautafsiri kwa Kiswahili.\n\nTuma picha yenye maelezo (caption) na nitaitafsiri caption yake kuwa Kiswahili.\n\nTuma video yenye maelezo (caption) na nitaitafsiri caption yake kuwa Kiswahili.\n\nKwa sasa naweza kufanya tafsiLugha zote kwenda Kiswahili tu.\n\nKwa msaada zaidi, wasiliana na @Huduma."
    update.message.reply_text(atxt)


def tr_command(update, context):
    message = update.message.reply_to_message

    if message:
        text = message.text
        caption = message.caption

        try:
            swtr.tr_command(update, context)
        except Exception as e:
            update.message.reply_text(text="Tafsiri haikufanikiwa. Jaribu tena baadaye.")





# Tafsiri ujumbe wa maandishi
def translate_to_swahili(update, context):
        swtr.tr_text(update, context)



# Tafsiri picha au video na tuma
def translate_and_send(update, context):
    if update.message.caption:
        try:
            swtr.tr_picha_video(update, context)
        except Exception as e:
            update.message.reply_text(text="Tafsiri haikufanikiwa. Tumia Command hii /tr kwa ku, reply message unayotaka kuitranslate.")




def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # Unda Updater na Token yako ya boti
    updater = Updater(TOKEN, use_context=True)

    # Pata kitanzi cha Dispatcher
    dispatcher = updater.dispatcher

    # Unda handler ya amri ya /start
    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)

    translate_handler = CommandHandler('tr', tr_command)

    # Add command handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(translate_handler)


    # Unda handler ya ujumbe wa maandishi
    message_handler = MessageHandler(Filters.text, translate_to_swahili)
    dispatcher.add_handler(message_handler)

    # Unda handler ya picha na video
    media_handler = MessageHandler(Filters.photo | Filters.video, translate_and_send)
    dispatcher.add_handler(media_handler)

    dispatcher.add_handler(MessageHandler(Filters.animation | Filters.document, translate_and_send))

    # Anza boti
    updater.start_polling()

    # Endesha boti hadi kusitishwa
    updater.idle()

if __name__ == '__main__':
    main()
