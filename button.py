import asyncio
import logging
import re
from aiohttp import web
import aiohttp_jinja2
import jinja2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor
from environs import Env

BOT_TOKEN = "token"

ENDPOINT = "https://example.com/"

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
    # Ask the user for a link and button title
    await msg.reply("Please enter a link and a button title (e.g., Link Title|http://example.com):")

@dp.message_handler(lambda message: '|' in message.text)
async def process_link(message: types.Message):
    # Split the user's input into title and link
    parts = message.text.split('|')
    
    if len(parts) != 2:
        await message.reply("Please enter both a button title and a link separated by '|' (e.g., Link Title|http://example.com).")
        return

    title, link = parts

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=title, web_app=types.WebAppInfo(url=link))]
    ])
    await message.reply("Here's your customized web app button:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.TEXT, is_forwarded=True)
async def handle_forwarded_message(msg: types.Message):
    # Extract the forwarded message text and link (if any)
    forwarded_text = msg.text
    forwarded_link = None

    if forwarded_text:
        # Check if there is a link in the forwarded text
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', forwarded_text)
        if links:
            forwarded_link = links[0]

    if forwarded_link:
        # Extract the title from the original message, if provided
        title = msg.caption if msg.caption else "Make Payment Here 🥰"
        
        # Create a button with the title and link
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=title, web_app=types.WebAppInfo(url=forwarded_link))]
        ])

        # Reply with the original forwarded message and the web app button
        await msg.reply(forwarded_text, reply_markup=keyboard)
    else:
        await msg.reply("Sorry, I couldn't find a link in the forwarded message.")

def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == "__main__":
    main()
