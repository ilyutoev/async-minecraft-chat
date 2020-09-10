import asyncio
import os
import logging
import json


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5050)
CHAT_HASH = 'c11a9f9e-f36f-11ea-8c47-0242ac110002'

logging.basicConfig(level=logging.DEBUG)


async def authorise(writer, reader, token):
    """Функция для авторизации пользователя по токену."""

    await submit_message(writer, token)

    # Получаем сообщение и проверяем верно ли авторизовались
    received_message_json = await read_message_json(reader)

    if received_message_json is None:
        print('Неизвестный токен.')
        return False
    return True


async def register(writer, reader):
    """Регистрируем нового пользователя и возаращем токен"""
    # Получаем строку о вводе логина нового пользователя
    data = await reader.readline()
    logging.debug(data.decode())

    # Регистрируем нового пользователя
    await submit_message(writer, 'User')

    # Получаем сообщение и сохранем хеш
    received_message_json = await read_message_json(reader)

    token = received_message_json.get('account_hash')
    print(f'Ваш новый токен: {token}')

    # Вычитываем строку о вводе нового сообщения
    await read_message_str(reader)


async def submit_message(writer, message):
    """Отправялем сообщение в чат"""
    message = message.replace("\n", "\\n")
    sent_message = f'{message}\n'
    logging.debug(sent_message)
    writer.write(sent_message.encode())
    await writer.drain()


async def read_message_str(reader):
    """Читаем сообщение из чата и возвращаем строковое представление."""
    data = await reader.readline()
    received_message = data.decode()
    logging.debug(received_message)
    return data


async def read_message_json(reader):
    """Читаем сообщение и возвращаем json."""
    received_message_str = await read_message_str(reader)
    return json.loads(received_message_str)


async def main():
    reader, writer = await asyncio.open_connection(DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)

    # Получаем первое сообщение из чата
    await read_message_str(reader)

    is_authorise = await authorise(writer, reader, CHAT_HASH)

    if is_authorise is False:
        await register(writer, reader)

    await submit_message(writer, 'Hello\n')

    await submit_message(writer, 'Test')

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
