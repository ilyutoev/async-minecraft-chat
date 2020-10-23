# Скрипты для работы с чатом

Скрипт подключается к чат серверу minechat.dvmn.org, позволяет сохранить историю сообщений, зарегистрироваться и отправлять свои сообщения.


## Как установить

Для работы микросервиса нужен Python версии не ниже 3.6.

```bash
pip install -r requirements.txt
```

## Как запустить скрипт для сохранения истории переписки

Скрипт сохраняет в файл все сообщения и чата о майнкрафте.

```bash
python listen-minechat.py
```

Скрипт поддерживает настройку через аргументы командной строки и переменные окружения:
 
- хост сервера (`--host` или `MINECHAT_SERVER_HOST`)
- порт сервер (`--port` или `MINECHAT_SERVER_PORT`)
- путь к файлу (`--history` или `MINECHAT_FILE_PATH`)

## Как запустить скрипт для отправки сообщений

Скрипт позволяет отправить сообщение в чат, а также авторизоваться в нем и зарегистрировать нового пользователя.

```bash
python write-minechat.py
```

Скрипт поддерживает настройку через аргументы командной строки и переменные окружения:
 
- хост сервера (`--host` или `MINECHAT_SERVER_HOST`)
- порт сервер (`--port` или `MINECHAT_SERVER_PORT`)
- токен пользователя (`--token` или `MINECHAT_TOKEN`)
- имя пользователя (`--username` или `MINECHAT_USERNAME`)
- текст сообщения (`--message` или `MINECHAT_MESSAGE`)
