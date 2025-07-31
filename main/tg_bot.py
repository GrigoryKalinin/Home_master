import telegram
import logging


logging.basicConfig(level=logging.INFO)

async def send_tg_message(token, chat_id, message, parse_mode='Markdown'):
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
        logging.info(f'Соощбшение "{message}" отправлено в чат {chat_id}')
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')
        raise
