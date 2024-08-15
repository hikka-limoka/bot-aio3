from aiogram import Router
from aiogram.types import Message

from app.search import Search
from app.api import LimokaAPI

router = Router()

@router.message()
async def search_module(message: Message):

    if message.text not in ["/stats", "/start"]:
        query = message.text

        api = LimokaAPI()

        modules = await api.get_all_modules()

        contents = []

        for module in modules:
            contents.append(
                {
                    "id": module["id"], 
                    "content": module["name"],
                }
            )

        for module in modules:
            contents.append(
                {
                    "id": module["id"], 
                    "content": module["description"],
                }
            )

        for module in modules:
            for command in module["commands"]:
                contents.append(
                    {
                        "id": module["id"],
                        "content": command["command"]
                    }
                )
                contents.append(
                    {
                        "id": module["id"],
                        "content": command["description"]
                    }
                )

        searcher = Search(query)
        result = searcher.search_module(contents)

        module_id = result

        if module_id == 0:
            await message.answer("❌ <b>Модуль не найден!</b>")

        else:
            module_info = await api.get_module_by_id(module_id)

            dev_username = module_info["developer"]
            name = module_info["name"]
            description = module_info["description"]
            commands = module_info["commands"]

            commands = []

            command_template = ".{command} - {description}"

            for command in commands:
                command_template.format(
                    command=command["command"],
                    description=description["description"]
                )

            commands_text = '\n'.join(commands)

            await message.answer(
                f"🔎 Best guess for <code>{query}</code>"
                "\n"
                f"\n🧩 <b>Module <code>{name}</code> by {dev_username}</b>"
                f"\nℹ️ <i>{description}</i>"
                "\n"
                f"\n{commands_text}"
            )