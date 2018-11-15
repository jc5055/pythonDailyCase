#!/usr/bin/python
import time,asyncio,aiohttp,requests

url = 'https://www.baidu.com/'

async  def hello(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async  with session.get(url) as response:
                print(time.time())
                return  await response.read()

async  def run():
    semphore = asyncio.Semaphore(10)
    to_get = [hello(url.format(), semphore) for _ in range(100)]

    await  asyncio.wait(to_get)





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()