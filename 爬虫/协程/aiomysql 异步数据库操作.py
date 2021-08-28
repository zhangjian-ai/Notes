import aiomysql
import logging
import asyncio
import traceback

logging.basicConfig(level='INFO')
logger = logging.getLogger('aio_mysql')


class AsyncMysql:
    """
    异步数据库操作
    """
    async def initPool(self):
        try:
            logger.info("init mysql connection pool ...")
            __pool = await aiomysql.create_pool(
                minsize=5,
                maxsize=20,
                host='121.4.47.229',
                port=3306,
                user='tp_admin',
                password='tp_123456',
                db='test_plat',
                autocommit=True  # 自动提交模式
            )
            self.pool = __pool
            logger.info("async mysql connected!!")
        except:
            # exc_info = True 表示将记录或者打印捕获到的异常信息
            logger.error('connection error ...', exc_info=True)

    async def getCursor(self):
        conn = await self.pool.acquire()
        # aiomysql.DictCursor 这样cursor查询到的每一条结果将被封装成字典
        # 默认情况下每条数据将是元组
        cur = await conn.cursor(aiomysql.DictCursor)

        return conn, cur

    async def query(self, sql, param=None):
        """
        查询操作
        :param sql: sql语句
        :param param: 参数
        :return:
        """
        conn, cur = await self.getCursor()
        try:
            await cur.execute(sql, param)
            return await cur.fetchall()
        except:
            # traceback 主要作用是打印详细的异常信息，且不会中断程序执行
            # print_exc 默认情况下将异常信息打印到控制台，也可以配置file参数输出到文件
            # format_exc 将异常信息以字符串的方式返回，方便记录到日志
            # traceback.print_exc()
            logger.error(traceback.format_exc())
        finally:
            if cur:
                await cur.close()
            # 释放链接到链接池
            await self.pool.release(conn)

    async def execute(self, sql, param=None):
        """
        增删改 操作
        :param sql: sql语句
        :param param: 参数
        :return:
        """
        conn, cur = await self.getCursor()
        try:
            await cur.execute(sql, param)
            if cur.rowcount == 0:
                return False
            else:
                return True
        except:
            logger.error(traceback.format_exc())
        finally:
            if cur:
                await cur.close()
            # 释放链接到链接池
            await self.pool.release(conn)


if __name__ == '__main__':
    sql = "select * from tp_users where id = %s"
    param = [1, 2]

    amysql = AsyncMysql()

    # 同一个对象中的协程对象必须运行在同一个循环事件中，所以这里用asyncio.run()很不方便
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amysql.initPool())
    tasks = [amysql.query(sql, param=x) for x in param]

    # 返回值done是包含多个成功执行的task对象的集合，每个task对象里面包含了当前task的状态，执行结果等信息
    # - done() 方法查看状态
    # - result() 方法查看执行结果,包装在列表里面
    # pending 是一个包含执行失败的任务对象的集合
    done, pending = loop.run_until_complete(asyncio.wait(tasks))

    for task in done:
        print(task.result()[0])

    # 如果是执行运行的协程对象，则可以直接拿到函数返回值
    res = loop.run_until_complete(amysql.query('select * from tp_users'))
    print(res)



