from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator


# Kutafsiri ujumbe kwenda Kiswahili
translator = Translator()




# Define the /tr command handler
def tr_command(update, context):
    try:
        message = update.message.reply_to_message
        if message:
            text = message.text
            caption = message.caption

            if text:
                translated_text = translator.translate(text, src='auto', dest='sw').text
                update.message.reply_text(f"{translated_text}", disable_web_page_preview=True)

            if message.photo:
                file_id = message.photo[-1].file_id
                caption = message.caption

                translated_caption = translator.translate(caption, src='auto', dest='sw').text if caption else None
                update.message.reply_photo(photo=file_id, caption=translated_caption)

            elif message.video:
                file_id = message.video.file_id
                caption = message.caption

                translated_caption = translator.translate(caption, src='auto', dest='sw').text if caption else None
                update.message.reply_video(video=file_id, caption=translated_caption)


            elif message.document:
                file_id = message.document.file_id
                caption = message.caption

                translated_caption = translator.translate(caption, src='auto', dest='sw').text if caption else None
                update.message.reply_document(document=file_id, caption=translated_caption)

            elif message.audio:
                file_id = message.audio.file_id
                caption = message.caption

                translated_caption = translator.translate(caption, src='auto', dest='sw').text if caption else None
                update.message.reply_audio(audio=file_id, caption=translated_caption)
    except Exception as e:
        print(f"Error occurred: {e}")
        # Unaweza kufanya kitu kingine hapa kama vile kutuma taarifa ya hitilafu kwenye mtandao wako au kurekebisha tatizo kwa njia fulani.
        return

# Function to handle unknown commands
def unknown(update: Update, context):
    update.message.reply_text("Samahani, siwezi kuelewa amri hiyo.")


# Tafsiri ujumbe wa maandishi
def tr_text(update, context):
    # Pata ujumbe kutoka kwa mtumiaji
    message = update.message.text

    # Tathmini ikiwa ujumbe ni amri
    if message.startswith('/'):
        return  # Rudi bila kufanya chochote ikiwa ni amri

    # Tathmini lugha ya ujumbe
    detected_language = translator.detect(message).lang

    # Ikiwa lugha iliyotambuliwa ni Kiswahili, rudisha ujumbe bila kufanya tafsiri
    if detected_language == 'sw' or detected_language == 'und':
        return

    # Tafsiri ujumbe kwenda Kiswahili
    translation = translator.translate(message, dest='sw')
    translation_text = translation.text.replace("Mwenyezi Mungu", "Allah") # Badilisha neno "Mwenyezi Mungu" na "Allah"

    # Ikiwa ujumbe wa mtumiaji ni sawa na tafsiri, rudisha bila kufanya chochote
    if message == translation_text:
        return

    # Jibu na tafsiri
    return update.message.reply_text(translation_text, disable_web_page_preview=True)



# Tafsiri picha au video na tuma
def tr_picha_video(update, context):
    caption = update.message.caption

    # Ikiwa hakuna maelezo (caption), rudi kutoka kwenye mbinu
    if not caption:
        return

    # Tathmini lugha ya maelezo (caption)
    detected_language = translator.detect(caption).lang

    # Ikiwa lugha iliyotambuliwa ni Kiswahili, rudisha bila kufanya tafsiri
    if detected_language == 'sw' or detected_language == 'und':
        return

    # Tafsiri maelezo kutoka lugha ya awali kwenda Kiswahili
    translation = translator.translate(caption, dest='sw')
    translation_text = translation.text.replace("Mwenyezi Mungu", "Allah")  # Badilisha neno "Mwenyezi Mungu" na "Allah"

    # Badilisha maelezo ya awali na yale yaliyotafsiriwa
    update.message.caption = translation_text
    if caption == translation_text:
        return

    # Tuma tena picha au video na maelezo yaliyobadilishwa
    if update.message.photo:
        for photo in update.message.photo:
            return update.message.reply_photo(photo=photo.file_id, caption=translation_text)


    if update.message.video:
        return update.message.reply_video(video=update.message.video.file_id, caption=translation_text)


    if update.message.animation:
        return update.message.reply_animation(animation=update.message.animation.file_id, caption=translation_text)



