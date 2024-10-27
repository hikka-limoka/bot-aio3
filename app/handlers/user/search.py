from aiogram import Router
from aiogram.types import Message

from app.search import Search
from app.keyboards.inline import module_keyboard

import html

router = Router()

@router.message()
async def search_module(message: Message, api):
    query = message.text

    if query.startswith("#"):
        query = query[1:]

        command, module_id = query.split("\n", 1)[0].split(":", 1)

        if not module_id.isdigit():
            return

        module_id = int(module_id)

        if command == "confirm":
            await api.download_module(message.from_user.id, module_id)
            await message.answer("✅ <b>Module installed!</b>")

        if command == "look":
            await api.look_module(message.from_user.id, module_id)

        return await message.delete()

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
        for func in module["commands"]:
            for command, description in func.items():
                contents.append({"id": module["id"], "content": command})
                contents.append({"id": module["id"], "content": description})

    searcher = Search(query)
    try:
        result = searcher.search_module(contents)
    except IndexError:
        return await message.answer("Very short search query, try it differently")

    if not result:
        return await message.answer("❌ <b>Module not found!</b>")

    module_id = result[0]

    if module_id == 0:
        await message.answer("❌ <b>Module not found!</b>")

    else:
        module_info = await api.get_module_by_id(module_id)

        dev_username = module_info["developer"]
        name = module_info["name"]

        commands = []

        command_template = "<code>.{command}</code> - <i>{description}</i>"

        for func in module_info["commands"]:
            for command, description in func.items():
                commands.append(
                    command_template.format(
                        command=html.escape(command),
                        description=(
                            html.escape(description)
                            if description
                            else "No description"
                        ),
                    )
                )

        commands_text = '\n'.join(commands)

        description = module_info["description"] if description else "No description"

        await message.answer(
            f"🔎 Best guess for <code>{html.escape(query)}</code>"
            "\n"
            f"\n🧩 <b>Module <code>{html.escape(name)}</code> by {dev_username}</b>"
            f"\nℹ️ <i>{html.escape(description)}</i>"
            f"\n\n{commands_text}",
            reply_markup=module_keyboard(module_id),
            disable_web_page_preview=True,
        )
