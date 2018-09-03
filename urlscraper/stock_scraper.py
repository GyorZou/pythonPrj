import asyncio
import aiohttp
import ssl


loop = asyncio.get_event_loop()

async def fetch(url):
   # print("fetching",url)

    async with aiohttp.ClientSession(loop = loop) as session:

        try:
            async with session.get(url, verify_ssl=False) as  response:
                response = await response.read()
                response = b'' + response
                # print("resp:{0}\n{1}".format(url,response.decode("utf-8")))
                return response
        except Exception:
            pass

async def bound_fetch(sem,url,analyse_func = None,holder = None):
    async with sem:
       resp = await fetch(url)

       if analyse_func:
           result = analyse_func(resp)
           if result:
               if isinstance(holder,list):
                   holder.append(result)
       elif analyse_func:
           holder.append(resp)






def scrape_urls(urls,analyse_func = None,holder=None):
    sem = asyncio.Semaphore(100)
    # tasks = [fetch(host+url) for url in urls_todo]

    tasks = [bound_fetch(sem, url,holder=holder,analyse_func=analyse_func) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))

if __name__ == "__main__":
    import  time
    start = time.time()
    # sem = asyncio.Semaphore(100)
    # #tasks = [fetch(host+url) for url in urls_todo]
    # tasks = [bound_fetch(sem,host + url) for url in urls_todo]
    # loop.run_until_complete(asyncio.gather(*tasks))
    scrape_urls()
    print(time.time() - start)
