import asyncio
import logging
from aiohttp import web
import aiohttp_jinja2
import jinja2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor
from environs import Env


BOT_TOKEN = "token"

ENDPOINT = "https://www.google.com/"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.ERROR)

# Placeholder function for web_start
async def web_start(request):
    # Your implementation here
    return web.Response(text="Web Start Placeholder")

# Placeholder function for web_send_message
async def web_send_message(request):
    # Your implementation here
    return web.Response(text="Web Send Message Placeholder")

# Placeholder function for web_check_user_data
async def web_check_user_data(request):
    # Your implementation here
    return web.Response(text="Web Check User Data Placeholder")

app = web.Application()
app.add_routes([web.get('/web-start', web_start),
                web.post('/sendMessage', web_send_message),
                web.post('/checkUserData', web_check_user_data)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('web'), enable_async=True)

async def on_startup(dps: Dispatcher):
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host="0.0.0.0", port=45678))

async def on_shutdown(dps: Dispatcher):
    await dps.storage.close()
    await dps.storage.wait_closed()

@dp.message_handler(CommandStart())
async def cmd_start(msg: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="😎 WEB APP", web_app=types.WebAppInfo(url=f"{ENDPOINT}"))]
    ])
    await msg.reply("TEST WEB APP", reply_markup=keyboard)

def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == "__main__":
    main()
