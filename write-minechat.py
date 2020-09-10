import asyncio
import os
import logging


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5050)
CHAT_HASH = 'c11a9f9e-f36f-11ea-8c47-0242ac110002'

logging.basicConfig(level=logging.DEBUG)


async def main():

    reader, writer = await asyncio.open_connection(DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)

    while True:
        data = await reader.readline()
        if not data:
            break
        received_message = data.decode()
        logging.debug(received_message)

        if 'Enter your personal hash' in received_message:
            sent_message = f'{CHAT_HASH}\n'
            logging.debug(sent_message)
            writer.write(sent_message.encode())
            await writer.drain()
        else:
            sent_message = 'Hello\n\n'
            logging.debug(sent_message)
            writer.write(sent_message.encode())
            await writer.drain()
            break

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
