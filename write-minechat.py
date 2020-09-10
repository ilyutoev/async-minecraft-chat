import asyncio
import os
import logging
import json


DEFAULT_SERVER_HOST = os.getenv('MINECHAT_SERVER_HOST', 'minechat.dvmn.org')
DEFAULT_SERVER_PORT = os.getenv('MINECHAT_SERVER_PORT', 5050)
CHAT_HASH = 'c11a9f9e-f36f-11ea-8c47-0242ac110002'

logging.basicConfig(level=logging.DEBUG)


async def main():

    reader, writer = await asyncio.open_connection(DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)
    data = await reader.readline()

    # Получаем первое сообщение из чата
    received_message = data.decode()
    logging.debug(received_message)

    # Отправляем хеш пользователя
    sent_message = f'{CHAT_HASH}\n'
    logging.debug(sent_message)
    writer.write(sent_message.encode())
    await writer.drain()

    # Получаем сообщение и проверяем верно ли авторизовались
    data = await reader.readline()
    received_message_json = json.loads(data.decode())
    logging.debug(received_message_json)

    if received_message_json is None:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        # Получаем строку о вводе логина нового пользователя
        data = await reader.readline()
        logging.debug(data.decode())

        # Регистрируем нового пользователя
        sent_message = 'User\n'
        logging.debug(sent_message)
        writer.write(sent_message.encode())
        await writer.drain()

        # Получаем сообщение и сохранем хеш
        data = await reader.readline()
        received_message_json = json.loads(data.decode())
        logging.debug(received_message_json)

        new_hash = received_message_json.get('account_hash')
        print(f'Ваш новый токен: {new_hash}')
        return

    # Отправляем сообщение в чат
    sent_message = 'Hello\n\n'
    logging.debug(sent_message)
    writer.write(sent_message.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
