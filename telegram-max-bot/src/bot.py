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
    print(message)
    keywords = ['макс', 'max']
    text_lower = message.text.lower()
    found = None
    for kw in keywords:
        if kw in text_lower:
            found = True
            break
    if found:
        if sticker_file_ids:
            sticker = random.choice(sticker_file_ids)
            bot.send_sticker(
                message.chat.id,
                sticker,
                reply_to_message_id=message.message_id
            )
        else:
            bot.send_message(message.chat.id, "Sticker pack not found or empty.", reply_to_message_id=message.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)