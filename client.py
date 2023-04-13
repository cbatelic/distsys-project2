import aiohttp
import asyncio
from aiohttp import web
import pandas as pd


routes = web.RouteTableDef()

clientID =  []
for i in range(10000):
    clientID.append(i)
    
df = pd.read_json("fakeData.json", lines=True, nrows=50000)

division = len(df) / len(clientID)
print("division", int(division))


contentList = list(df.loc[:, 'content'])
clientDict = {elem:[] for elem in clientID}

for index,elem in clientDict.items():
    numberOfRowsToTake = index*division
    numberOfRowsTill = numberOfRowsToTake + division
    for x in range(len(contentList)):        
        elem.append(contentList[int(numberOfRowsToTake):int(numberOfRowsTill)])
        break
    
for index,List in clientDict.items():
    total = 0
    for elem in List:
        for elementOfList in elem:
            total += len(elementOfList)
    ave_size = float(total) / float(division)
    print("Client:",index, "average", ave_size)
    

async def next():
    tasks = []
    
    try: 
        async with aiohttp.ClientSession() as session:
            for index,element in clientDict.items():
                tasks.append(asyncio.create_task(session.get("http://localhost:2000/", json = {"cli": index, "codes": element})))
            res = await asyncio.gather(*tasks)
            res = [await x.json() for x in res]
            print(res)
            return res
    except (aiohttp.ClientError, asyncio.TimeoutError):
        await asyncio.sleep(5)
        return await next()

asyncio.get_event_loop().run_until_complete(next())           