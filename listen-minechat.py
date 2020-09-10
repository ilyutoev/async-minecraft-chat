import asyncio


async def main():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5000)

    while True:
        data = await reader.readline()
        if not data:
            break
        print(data.decode().strip())

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
