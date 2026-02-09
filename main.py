import asyncio
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Register Now", url="https://t.me/devdevelopers_07")],
            [types.InlineKeyboardButton(text="Customer Support", url="https://t.me/devdevelopers_07")],
            [types.InlineKeyboardButton(text="Join us on Telegram", url="https://t.me/devdevelopers_07")],
        ]
    )

    await message.answer_photo(
        photo="https://i.ibb.co/CpSM6QJ0/images-1.jpg",
        caption="<b>WELCOME TO AVIATORX OFFICIAL</b>\n\nClick below 👇",
        reply_markup=keyboard
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
