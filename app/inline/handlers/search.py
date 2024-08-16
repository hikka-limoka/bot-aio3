from aiogram import Router
from aiogram.types import InlineQuery

from app.inline.articles.search import get_modules

from app.api import LimokaAPI
from app.search import Search

router = Router()


@router.inline_query()
async def module_query(inline_query: InlineQuery):
    print("a")
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
    search = Search(inline_query.from_user)
    modules_matched = await search.search_module(contents)

    results = await get_modules(modules_matched)

    
    await inline_query.answer(
        results=results,
        cache_time=0,
        is_personal=True,
    )

