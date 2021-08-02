from ..gibooru import Danbooru

async def get_post(dan: Danbooru):
    await dan.get_post()

x = Danbooru()
get_post(x)
