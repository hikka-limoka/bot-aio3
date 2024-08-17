from aiogram import Router
from aiogram.types import InlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.api import LimokaAPI
from app.search import Search

import random

router = Router()


@router.inline_query()
async def module_query(inline_query: InlineQuery):
    if inline_query.query:
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

        search = Search(inline_query.query)
        modules_matched = search.search_module(contents)

        results = []

        if type(modules_matched) is int and modules_matched == 0:
            return InlineQueryResultArticle(
                    id="404",
                    title="<b>Not found</b>",
                    description="<i>Not found</i>",
                    input_message_content=InputTextMessageContent(
                        message_text=
                        "Not found"
                    ),
                )

        for module in modules_matched:
            info = await api.get_module_by_id(module)
            print(info)

            dev_username = info["developer"]
            name = info["name"]
            link = f"https://limoka.vsecoder.dev/api/module/{dev_username}/{name}.py"
            results.append(InlineQueryResultArticle(
                    id=f"{random.randint(1,10000000000000000)}",
                    title=f"{info['name']}",
                    description=f"{info['description']}",
                    input_message_content=InputTextMessageContent(
                        message_text=
                        f"\n🔗 <b>Link:</b> <code>{link}</code>"
                    ),
                )
            )
            
            await inline_query.answer(
                results=results,
                cache_time=30,
                is_personal=True,
            )
