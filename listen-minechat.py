import asyncio
from datetime import datetime

import aiofiles


async def main():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5000)

    async with aiofiles.open('chat_history.txt', mode='a') as f:
        while True:
            data = await reader.readline()
            if not data:
                break

            await f.write(f'[{datetime.now().strftime("%d.%m.%Y %H:%M")}] {data.decode()}')
        writer.close()
    await writer.wait_closed()

asyncio.run(main())
