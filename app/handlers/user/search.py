from aiogram import Router
from aiogram.types import Message

from app.search import Search
from app.keyboards.inline import module_keyboard

import html

router = Router()

@router.message()
async def search_module(message: Message, api):
    query = message.text

    if len(query) < 2:
        return await message.answer("Very short search query, try it differently")

    if len(message.text) > 100:
        return await message.answer("Very long search query, try it differently")

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
            contents.append({"id": module["id"], "content": command["command"]})
            contents.append({"id": module["id"], "content": command["description"]})

    searcher = Search(query)
    result = searcher.search_module(contents)

    module_id = result[0]

    if module_id == 0:
        await message.answer("❌ <b>Модуль не найден!</b>")

    else:
        module_info = await api.get_module_by_id(module_id)

        dev_username = module_info["developer"]
        name = module_info["name"]
        description = module_info["description"]
        # link = f"https://limoka.vsecoder.dev/api/module/{dev_username}/{name}.py"

        commands = []

        command_template = "<code>.{command}</code> - <i>{description}</i>"

        for command in module_info["commands"]:
            commands.append(
                command_template.format(
                    command=command['command'],
                    description=command["description"]
                )
            )

        commands_text = '\n'.join(commands)

        await api.look_module(message.from_user.id, module_id)

        await message.answer(
            f"🔎 Best guess for <code>{html.escape(query)}</code>"
            "\n"
            f"\n🧩 <b>Module <code>{html.escape(name)}</code> by {dev_username}</b>"
            f"\nℹ️ <i>{description}</i>"
            f"\n🔽 <b>Downloads:</b> {len(module_info['downloads'])}"
            f"\n👀 <b>Views:</b> {len(module_info['looks'])}"
            f"\n\n{commands_text}",
            reply_markup=module_keyboard(module_id),
            disable_web_page_preview=True,
        )
