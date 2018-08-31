import asyncio
import aiohttp

host = "http://example.com"
urls_todo = list(map(lambda x: "/{0}".format(x), range(1, 10)))
print(urls_todo)

loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop = loop) as session:
        async with session.get(url) as  response:
            response = await response.read()
            response = b'' +response
            print("resp:{0}\n{1}".format(url,response.decode("utf-8")))
            return response

if __name__ == "__main__":
    import  time
    start = time.time()
    tasks = [fetch(host+url) for url in urls_todo]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)
