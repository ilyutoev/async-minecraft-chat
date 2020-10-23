import asyncio
from datetime import datetime
import argparse
import os

import aiofiles

from connection_helper import open_connection


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5000)
DEFAULT_FILE_PATH = os.getenv('MINECHAT_FILE_PATH', 'minechat.history')


def get_arguments():
    """Получаем аргументы командной строки, переданные скрипту."""
    parser = argparse.ArgumentParser(description='Script save minechat messages to file.')
    parser.add_argument('--host', type=str, default=DEFAULT_SERVER_HOST, help='Minechat server host.')
    parser.add_argument('--port', type=int, default=DEFAULT_SERVER_PORT, help='Minechat server port.')
    parser.add_argument('--history', type=str, default=DEFAULT_FILE_PATH, help="Path to save minechat history.")
    return parser.parse_args()


async def main():
    args = get_arguments()

    async with open_connection(args.host, args.port) as (reader, writer):
        async with aiofiles.open(args.history, mode='a') as f:
            while True:
                data = await reader.readline()
                if not data:
                    break

                await f.write(f'[{datetime.now().strftime("%d.%m.%Y %H:%M")}] {data.decode()}')
                print(data.decode())

if __name__ == '__main__':
    asyncio.run(main())
