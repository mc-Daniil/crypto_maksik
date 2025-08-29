import telebot
import random
from config import BOT_TOKEN, STICKER_PACK_ID

bot = telebot.TeleBot(BOT_TOKEN)

# Fetch sticker file_ids from the sticker pack at startup
sticker_file_ids = []
print(f"Trying to fetch sticker set: {STICKER_PACK_ID}")
try:
    sticker_set = bot.get_sticker_set(STICKER_PACK_ID)
    sticker_file_ids = [sticker.file_id for sticker in sticker_set.stickers]
except Exception as e:
    print(f"Error fetching sticker set '{STICKER_PACK_ID}': {e}")
    print("Make sure STICKER_PACK_ID is set to the correct sticker pack name (not a file_id or list).")

@bot.message_handler(func=lambda message: True)
def check_message(message):
    text_lower = message.text.lower()
    
    KEYWORDS_LASOS = ['ласос', 'lasos', 'losos', 'лосось']
    FOUND_LASOS = None
    for kw in KEYWORDS_LASOS:
        if kw in text_lower:
            FOUND_LASOS = True
            break

    KEYWORDS_MAX = ['макс', 'max']
    FOUND_MAX = None
    for kw in KEYWORDS_MAX:
        if kw in text_lower:
            FOUND_MAX = True
            break
    KEYWORDS_SOSAL = ['сос', 'sos']
    FOUND_SOSAL = None
    for kw in KEYWORDS_SOSAL:
        if kw in text_lower:
            FOUND_SOSAL = True
            break
    if FOUND_MAX:
        if sticker_file_ids:
            sticker = random.choice(sticker_file_ids)
            bot.send_sticker(
                message.chat.id,
                sticker,
                reply_to_message_id=message.message_id
            )
        else:
            bot.send_message(message.chat.id, "Sticker pack not found or empty.", reply_to_message_id=message.message_id)
    if FOUND_SOSAL:
        bot.send_message(message.chat.id, "lasos", reply_to_message_id=message.message_id)
    if FOUND_LASOS:
        with open('lasos.jpg', 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                reply_to_message_id=message.message_id
            )


if __name__ == '__main__':
    bot.polling(none_stop=True)
