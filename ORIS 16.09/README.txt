Формат сообщения
[COMMAND: 4 байта][LENGTH: 4 байта][PAYLOAD: LENGTH байт]

COMMAND имя команды, ровно 4 символа (ASCII)
LENGTH длина payload, big-endian unsigned int (struct.pack("!I", ...))
PAYLOAD данные в UTF-8
Максимальный размер payload 10 МБ

Команды
JOIN войти в чат под именем
TEXT отправить сообщение всем
LIST список пользователей онлайн
QUIT выйти из чата
ERRO ответ сервера об ошибке
