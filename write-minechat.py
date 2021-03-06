import asyncio
import os
import logging
import json
import argparse

from connection_helper import open_connection


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5050)
DEFAULT_TOKEN = os.getenv('MINECHAT_TOKEN')
DEFAULT_USERNAME = os.getenv('MINECHAT_USERNAME')

logger = logging.getLogger(__name__)


def get_arguments():
    """Получаем аргументы командной строки, переданные скрипту."""
    parser = argparse.ArgumentParser(description='Script save minechat messages to file.')
    parser.add_argument('--host', type=str, default=DEFAULT_SERVER_HOST, help='Minechat server host.')
    parser.add_argument('--port', type=int, default=DEFAULT_SERVER_PORT, help='Minechat server port.')
    parser.add_argument('--token', type=str, default=DEFAULT_TOKEN, help="User token.")
    parser.add_argument('--username', type=str, default=DEFAULT_USERNAME, help="Username for registration.")
    parser.add_argument('--message', type=str, help="Sending message.", required=True)
    return parser.parse_args()


async def authorise(writer, reader, token):
    """Функция для авторизации пользователя по токену."""

    await submit_message(writer, token)

    # Получаем сообщение и проверяем верно ли авторизовались
    received_message = await read_json_message_and_deserialize(reader)

    return bool(received_message)


async def register(writer, reader, username):
    """Регистрируем нового пользователя и возвращем токен."""
    # Получаем строку о вводе логина нового пользователя
    await read_message_str(reader)

    # Регистрируем нового пользователя
    await submit_message(writer, username)

    # Получаем сообщение и сохранем хеш
    received_message = await read_json_message_and_deserialize(reader)

    token = received_message.get('account_hash')
    print(f'Ваш новый токен: {token}')


async def submit_message(writer, message):
    """Отправялем сообщение в чат"""
    message = message.replace("\n", "\\n")
    sent_message = f'{message}\n'
    logger.debug(sent_message)
    writer.write(sent_message.encode())
    await writer.drain()


async def read_message_str(reader):
    """Читаем сообщение из чата и возвращаем строковое представление."""
    data = await reader.readline()
    received_message = data.decode()
    logger.debug(received_message)
    return data


async def read_json_message_and_deserialize(reader):
    """Читаем сообщение в json формате и десереализуем."""
    received_message_str = await read_message_str(reader)
    return json.loads(received_message_str)


async def main():
    logger.setLevel(logging.DEBUG)

    args = get_arguments()

    if all((args.username, args.token, args.message)):
        print('Необходимо передать в скрипт токен (или имя пользователя) и сообщение.')
        return

    async with open_connection(args.host, args.port) as (reader, writer):
        # Получаем первое сообщение из чата
        await read_message_str(reader)

        # Авторизуемся
        is_authorised = False
        if args.token:
            is_authorised = await authorise(writer, reader, args.token)

        # Регистрируем нового пользователя, если не удалось авторизоваться и передано имя пользователя
        if not is_authorised and args.username:
            if not args.token:
                # Отправляем пустую строку вместо токена
                await submit_message(writer, '')
            await register(writer, reader, args.username)

            # Вычитываем строку о вводе нового сообщения
            await read_message_str(reader)

            is_authorised = True

        if not is_authorised:
            print('Для отправки сообщения необходимо авторизоваться: '
                  'передать валидный токен или зарегистрировать нового пользователя.')

        # Отправляем сообщение
        if is_authorised and args.message:
            await submit_message(writer, args.message)


if __name__ == '__main__':
    asyncio.run(main())
