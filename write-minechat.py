import asyncio
import os


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5050)
CHAT_HASH = 'c11a9f9e-f36f-11ea-8c47-0242ac110002'


async def main():
    reader, writer = await asyncio.open_connection(DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)

    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode()
        if 'Enter your personal hash' in message:
            writer.write(f'{CHAT_HASH}\n'.encode())
            await writer.drain()
        else:
            writer.write('Hello\n\n'.encode())
            await writer.drain()
            break

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
