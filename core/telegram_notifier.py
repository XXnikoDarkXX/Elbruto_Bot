import os
from dotenv import load_dotenv
import re
from telegram import Bot
from telegram.constants import ParseMode

# Cargar .env solo si existe
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def escape_markdown_v2(text: str) -> str:
    if not isinstance(text, str):
        return str(text)
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

class TelegramNotifier:
    def __init__(self):
        pass

    async def enviar_mensaje(self, texto):
        bot = Bot(TOKEN)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode=ParseMode.MARKDOWN_V2)
            print(f"Mensaje enviado a {CHAT_ID}")
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
