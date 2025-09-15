import logging
import random
import re
from pathlib import Path
import traceback
import html

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Router
from aiogram.types import ReplyParameters, FSInputFile

from config import BOT_TOKEN, STICKER_PACK_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

sticker_file_ids = []
async def fetch_stickers():
    global sticker_file_ids
    try:
        sticker_set = await bot.get_sticker_set(STICKER_PACK_ID)
        sticker_file_ids = [sticker.file_id for sticker in sticker_set.stickers]
        logging.info("Fetched %d stickers from %s", len(sticker_file_ids), STICKER_PACK_ID)
    except Exception as e:
        logging.exception("Error fetching sticker set '%s'", STICKER_PACK_ID)


KEYWORDS_LASOS = ['ласос', 'lasos', 'losos', 'лосос']
KEYWORDS_MAX = ['макс', 'max']
KEYWORDS_SOSAL = ['сос', 'sos']
KEYWORDS_SOSYR = ['сосыр']


def module_file_path(filename: str) -> Path:
    """Return absolute Path relative to this module file."""
    return Path(__file__).resolve().parent / filename


async def safe_send_photo(chat_id: int, path: Path, message_id: int, found: str, position: int):
    """Send photo by path using FSInputFile and escape user-provided strings for HTML parse mode."""
    found_safe = html.escape(found)
    try:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        photo = FSInputFile(str(path))
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            reply_parameters=ReplyParameters(
                message_id=message_id,
                quote=found_safe,
                quote_position=len(found_safe) if position is None else len(found_safe)
            ),
        )
    except Exception as e:
        logging.exception("Failed to send photo %s", path)
        await bot.send_message(
            chat_id=chat_id,
            text=f"Ошибка при отправке {html.escape(path.name)}: {html.escape(str(e))}",
            reply_parameters=ReplyParameters(
                message_id=message_id,
                quote=found_safe,
                quote_position=len(found_safe) if position is None else len(found_safe),
            ),
        )


@router.message()
async def check_message(message: types.Message):
    text = message.text or ""

    # LASOS
    for kw in KEYWORDS_LASOS:
        match = re.search(re.escape(kw), text, re.IGNORECASE)
        if match:
            found = match.group(0)
            position = match.start()
            lasos_path = module_file_path('lasos.jpg')
            await safe_send_photo(
                chat_id=message.chat.id,
                path=lasos_path,
                message_id=message.message_id,
                found=found,
                position=position,
            )
            return

    # MAX
    for kw in KEYWORDS_MAX:
        match = re.search(re.escape(kw), text, re.IGNORECASE)
        if match:
            found = match.group(0)
            position = match.start()
            found_safe = html.escape(found)
            if sticker_file_ids:
                sticker = random.choice(sticker_file_ids)
                try:
                    await bot.send_sticker(
                        chat_id=message.chat.id,
                        sticker=sticker,
                        reply_parameters=ReplyParameters(
                            message_id=message.message_id,
                            quote=found_safe,
                            quote_position=len(text[:position]),
                        ),
                    )
                except Exception:
                    logging.exception("Failed to send sticker")
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="Ошибка при отправке стикера.",
                        reply_parameters=ReplyParameters(
                            message_id=message.message_id,
                            quote=found_safe,
                            quote_position=len(text[:position]),
                        ),
                    )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Sticker pack not found or empty.",
                    reply_parameters=ReplyParameters(
                        message_id=message.message_id,
                        quote=found_safe,
                        quote_position=len(text[:position]),
                    ),
                )
            return
        
    # SOSYR
    for kw in KEYWORDS_SOSYR:
        match = re.search(re.escape(kw), text, re.IGNORECASE)
        if match:
            found = match.group(0)
            position = match.start()
            sosyr_path = module_file_path('sosyr.jpg')
            await safe_send_photo(
                chat_id=message.chat.id,
                path=sosyr_path,
                message_id=message.message_id,
                found=found,
                position=position,
            )
            return

    # SOSAL
    for kw in KEYWORDS_SOSAL:
        match = re.search(re.escape(kw), text, re.IGNORECASE)
        if match:
            found = match.group(0)
            position = match.start()
            await bot.send_message(
                chat_id=message.chat.id,
                text="lasos",
                reply_parameters=ReplyParameters(
                    message_id=message.message_id,
                    quote=html.escape(found),
                    quote_position=len(text[:position]),
                ),
            )
            return


async def main():
    await fetch_stickers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Shutdown requested')
    except Exception:
        traceback.print_exc()