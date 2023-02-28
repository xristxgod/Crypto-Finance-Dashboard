from config import settings

TELEGRAM_WEBHOOK_URL = settings.WEBHOOK_URL + '/api/telegram-bot_apps/webhook'

TELEGRAM_CONFIG_DIR = settings.CONFIG_DIR / 'telegram'
