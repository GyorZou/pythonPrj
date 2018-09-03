import asyncio
import aiohttp
import ssl

host = "http://www.futunn.com/quote/stock-news?m=hk&code="
urls_todo = list(map(lambda x: str(x).zfill(5), range(1, 1000)))
print(urls_todo)

loop = asyncio.get_event_loop()

context = ssl._create_unverified_context()




async def fetch(url):
    print("fetching",url)

    async with aiohttp.ClientSession(loop = loop) as session:

        try:
            async with session.get(url, verify_ssl=False) as  response:
                response = await response.read()
                response = b'' + response
                # print("resp:{0}\n{1}".format(url,response.decode("utf-8")))
                return response
        except Exception:
            pass

async def bound_fetch(sem,url):
    async with sem:
        await fetch(url)


if __name__ == "__main__":
    import  time
    start = time.time()
    sem = asyncio.Semaphore(100)
    #tasks = [fetch(host+url) for url in urls_todo]
    tasks = [bound_fetch(sem,host + url) for url in urls_todo]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)
