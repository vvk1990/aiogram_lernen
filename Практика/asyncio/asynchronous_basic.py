import asyncio

async def send_hello():
    sec = 0
    while sec != 15:
        await asyncio.sleep(1)
        sec += 1
        if sec%3 != 0:
            print(f'Прошло {sec} секунд')

async def send_bye():
    sec = 0
    while sec != 15:
        await asyncio.sleep(3)
        sec += 3
        print('Прошло 3 секунды')


async def rune():
    task_1 = asyncio.create_task(send_hello())
    task_2 = asyncio.create_task(send_bye())
    await task_1
    await task_2

asyncio.run(rune())
