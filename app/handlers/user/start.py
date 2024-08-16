from app.api import LimokaAPI

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.inline.buttons.start import start

import toml


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    config = toml.load("config.toml")
    uid = message.from_user.id

    api = LimokaAPI(config["limoka"]["token"])

    if not await api.get_user(uid):
        await api.create_user(uid)

    await message.answer_photo(
        "https://github.com/hikka-limoka/stuff/raw/main/banner.png",
        "🍾 Modules are now in one place with easy searching!"
        "\n"
        "\n🤵 Official developers"
        "\n📊 Statistics"
        "\n👩‍⚖️ Up-to-date module updates"
        "\n"
        "\n🔎 Start searching:",
        reply_markup=start()
        
    )
