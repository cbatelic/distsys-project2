import asyncio
from aiohttp import web
import random

routes = web.RouteTableDef()

@routes.get("/")
async def countW(req):
    try:
        await asyncio.sleep(random.uniform(0.1, 0.3))

        data = await req.json()
        count = []
        for i in data["codes"]:
            print(len(i.split()))
            count.append(len(i.split()))
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return web.json_response({"w": "9","count": count}, status=200)
    except Exception as e:
        return web.json_response({"error":e}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=1009)