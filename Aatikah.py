import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN  # Ingiza token kutoka config.py

# Kuweka log level kwenye INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Handler ya amri ya /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tuma ujumbe wakati amri ya /start inapotolewa."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Habari #Marafiki tuko hapa kujifunza na kufanya majaribio ya Code au Msimbo")

# Handler ya ujumbe ili kurudia ujumbe
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rudia ujumbe wa mtumiaji."""
    await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=update.effective_chat.id, message_id=update.message.id)

# Handler ya makosa
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" ilisababisha kosa "%s"', update, context.error)

# Kazi kuu ya kuanzisha na kuendesha bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.ALL & filters.ChatType.PRIVATE, echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
