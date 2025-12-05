import html
import logging
import random
import re
import traceback
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ReplyParameters, FSInputFile

from config import BOT_TOKEN, KEYWORD_RULES, STICKER_PACKS_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

prefetched_stickerpacks = {}


async def fetch_stickers():
    global prefetched_stickerpacks

    for stickerpack_id in STICKER_PACKS_ID:
        try:
            sticker_set = await bot.get_sticker_set(stickerpack_id)
            sticker_ids = [sticker.file_id for sticker in sticker_set.stickers]

            prefetched_stickerpacks[stickerpack_id] = sticker_ids

            logging.info("Fetched %d stickers from %s", len(prefetched_stickerpacks), stickerpack_id)
        except Exception as e:
            logging.exception("Error fetching sticker set '%s'", stickerpack_id)


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
    message_text = message.text or ""

    for message_rule in KEYWORD_RULES:
        for keyword in message_rule["keywords"]:
            keyword_found_in_message = re.search(re.escape(keyword), message_text, re.IGNORECASE)
            if keyword_found_in_message:
                found = keyword_found_in_message.group(0)
                position = keyword_found_in_message.start()
                file_path = module_file_path(message_rule["file"])
                stickerpack_id = message_rule.get("stickerpack_id", None)

                # Send sticker if available. If no -> send image.

                if stickerpack_id:
                    found_safe = html.escape(found)
                    send_sticker = random.choice([True, False])
                    if send_sticker:
                        sticker = random.choice(prefetched_stickerpacks[stickerpack_id])
                        try:
                            await bot.send_sticker(
                                chat_id=message.chat.id,
                                sticker=sticker,
                                reply_parameters=ReplyParameters(
                                    message_id=message.message_id,
                                    quote=found_safe,
                                    quote_position=len(message_text[:position]),
                                ),
                            )
                            return
                        except Exception:
                            logging.exception("Failed to send sticker, sending image instead")

                await safe_send_photo(
                    chat_id=message.chat.id,
                    path=file_path,
                    message_id=message.message_id,
                    found=found,
                    position=position,
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
