import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

MAKS_STICKERPACK = "crypto_maks_by_fStikBot"

# Fill all stickerpack IDs you want to prefetch here. You must fetch every used sticker pack
STICKER_PACKS_ID = [
    MAKS_STICKERPACK,
]

KEYWORD_RULES = [
    {
        "keywords": ['ласос', 'lasos', 'losos', 'лосос'],
        "id": "lasos",
        "file": "./assets/lasos.jpg",
    },
    {
        "keywords": ['макс', 'max'],
        "id": "max",
        "file": "./assets/maks.jpg",
        "stickerpack_id": MAKS_STICKERPACK,
    },
    {
        "keywords": ['сосыр'],
        "id": "sosyr",
        "file": "./assets/sosyr.jpg",
    },
    {
        "keywords": ['сос', 'sos'],
        "id": "lasos",
        "file": "./assets/lasos.jpg"
    },
]
