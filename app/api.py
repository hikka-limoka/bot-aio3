import aiohttp

class LimokaAPI:
    def __init__(self, token):
        self.token = token

    async def get_all_modules(self) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://limoka.vsecoder.dev/api/module/all') as response:
                # A necessary crutch, because the server 
                # returns a list, but aiohttp gives only json
                return [await response.json()][0] 
            
    async def get_module_by_id(self, id) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://limoka.vsecoder.dev/api/module/{id}') as response:
                return await response.json()
            
    async def get_module_raw(self, developer, module_name) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://limoka.vsecoder.dev/api/module/{developer}/{module_name}') as response:
                return {"content": response.content(), "name": f"{module_name}.py"}
            
    async def get_users_count(self) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://limoka.vsecoder.dev/api/user/count') as response:
                data = await response.json()
                return data["count"]
            
    async def get_user(self, userid: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://limoka.vsecoder.dev/api/user/{user_id}?tg_id=' + userid) as response:
                data = await response.json()
                if data.get("error"):
                    return False
                else:
                    return True
                
    async def create_user(self, userid: str) -> dict:
        headers = {"token": self.token}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post('https://limoka.vsecoder.dev/api/user/?telegram_id=' + userid) as response:
                return userid