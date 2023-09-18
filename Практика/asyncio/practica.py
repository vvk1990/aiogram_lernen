import asyncio

async def send_time(sec):
    await asyncio.sleep(sec)
    print(f'прошло {sec} секунд')

async def main():
    task_1 = asyncio.create_task(send_time(2))# различные обьекты карутины!!
    task_2 = asyncio.create_task(send_time(5))
    await task_1
    await task_2


asyncio.run(main())