from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.api import LimokaAPI


async def get_modules(modules: list):
    results = []

    api = LimokaAPI()
    
    for module in modules:
        info = await api.get_module_by_id(module)

        dev_username = info["developer"]
        name = info["name"]
        link = f"https://limoka.vsecoder.dev/api/module/{dev_username}/{name}.py"
        results.append(
            InlineQueryResultArticle(
                id="modules",
                title=f"<b>{info['name']}</b>",
                description=f"<i>{info['description']}</i>",
                input_message_content=InputTextMessageContent(
                    message_text=
                    f"\n🔗 <b>Link:</b> <code>{link}</code>"
                ),
            )
        )

        return results
