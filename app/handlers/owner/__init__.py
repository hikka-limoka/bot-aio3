from aiogram import Router



def get_owner_router() -> Router:
    from . import stuff
    from . import moderate

    router = Router()
    router.include_router(moderate.router)
    router.include_router(stuff.router)

    return router
