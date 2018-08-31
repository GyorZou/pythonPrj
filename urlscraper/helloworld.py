import asyncio
import time

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()

rs = loop.run_until_complete(coroutine)
print('Task ret: ', rs)
# print('Task ret: ', coroutine.result())
print('TIME: ', now() - start)