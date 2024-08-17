from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.inline import start

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, api):
    uid = message.from_user.id

    if not await api.get_user(uid):
        await api.create_user(uid)

    await message.answer_photo(
        "https://raw.githubusercontent.com/hikka-limoka/stuff/main/banners/start.png",
        "🍾 Modules are now in one place with easy searching!"
        "\n"
        "\n🔎 Start searching:",
        reply_markup=start(),
    )
