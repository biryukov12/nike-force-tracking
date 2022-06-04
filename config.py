from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Token
BOT_TOKEN = getenv("BOT_TOKEN")

# Heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# webhook settings
WEBHOOK_HOST = f"https://{HEROKU_APP_NAME}.herokuapp.com"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = getenv("PORT", "3000")

# UUIDs for parse
uuids = {
    "men": "0f64ecc7-d624-4e91-b171-b83a03dd8550",
    "unisex": "568f7ffc-ee7f-49ed-98eb-0b94708d6e88",
    "shoes": "16633190-45e5-4810-a068-232ac7aea82c",
    "air_force_1": "8529ff38-7de8-4f69-973c-9fdbfb102ed2",
    "low_top": "abb0cf06-d7c2-41b7-97ba-c6d5ef5f43ed",
    "mid_top": "2797eaa0-4166-486e-96d1-95ad2495b58d",
    "high_top": "97a10d31-545b-46d9-ad76-8b4801dd7766",
    "footwear_size": "5c357820-4cff-37a6-b815-984753484f06",  # 7.5 US
    # 'cold_weather': 'b3552af0-55fc-4196-99d2-6fc8b834b9f6'
}

url_with_uuids = (
    f"https://api.nike.com/cic/browse/v2"
    f"?queryid=filteredProductsWithContext"
    f'&uuids={",".join(uuids.values())}'
    f"&language=ru"
    f"&country=RU"
    f"&channel=NIKE"
)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/95.0.4638.54 Safari/537.36"
}
