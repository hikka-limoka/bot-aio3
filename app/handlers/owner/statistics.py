from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.is_owner import IsOwner

from app.api import LimokaAPI

router = Router()




@router.message(IsOwner(is_owner=True), Command(commands=["stats"]))
async def stats_handler(message: Message):

    api = LimokaAPI()

    count = await api.get_users_count()

    await message.answer(
        f"📊 <b>Количество пользователей бота -</b> <code>{count}</code>"
    )
