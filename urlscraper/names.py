import aiomysql
import asyncio

class SqlUtils():
    number = 1
    print("xxx")
    def __init__(self):
        print("initing")
    def help(self):
        print("htlping")
        pass

SqlUtils.help("")
async def sql(loop):
    try:
        pool = await aiomysql.create_pool(user="root", password="123", db="ewj", loop=loop)
    except BaseException as e:
        print("some error :",e)
        return

    async with pool.acquire() as conn:
        cur = await conn.cursor()
        sql = "select name from user where name=?"
        sql = sql.replace("?","%s")

        r = await cur.execute(sql,args=("zjp") or ())
        rs = await  cur.fetchall()

        print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(sql(loop))
