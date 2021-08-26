import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return '返回值'


# 示例二: await task对象
# task对象: 创建时，立即将协程对象放到事件循环中，帮助实现多协程并发
async def task():
    print("开始创建task")

    # 创建task对象。asyncio.create_task(协程对象) python3.7 之后的方法
    # 低版本用 asyncio.create_future()
    task1 = asyncio.create_task(func(), name="no.1")  # 创建时，可以给任务起别名
    task2 = asyncio.create_task(func())

    task_list = [task1, task2]

    print("task创建完成")

    # timeout 协程最大阻塞时间，None表示无上限，一直等
    # done 是一个集合，包含所有执行完的协程对象和返回值
    # pending 是一个集合，包含所有未执行成功的协程对象
    done, pending = await asyncio.wait(task_list, timeout=None)

    print(done)
    print(list(done)[0].done())
    print(pending)


asyncio.run(task())

task_list = [func(), func()]

# asyncio.wait 可以传入task、future的对象列表，也可以直接传入协程对象列表。传入协程时，自动为协程添加task装饰器
done, pending = asyncio.run(asyncio.wait(task_list))
print(done)
