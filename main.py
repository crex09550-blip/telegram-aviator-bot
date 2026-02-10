import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== ENV VARIABLES ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = os.getenv("ADMIN_ID")
if not ADMIN_ID:
    raise Exception("ADMIN_ID missing in Railway Variables")
ADMIN_ID = int(ADMIN_ID)

# ================== CONTENT ==================
IMAGE_URL = "https://i.ibb.co/zhfWk6CV/file-00000000116872089ee7bdb49d8c245d.png"

REGISTER_URL = "https://clashbattle.qzz.io"
SUPPORT_URL = "https://t.me/coreversions"
JOIN_TG_URL = "https://t.me/coreversions"

PLAY_VIDEO = "https://t.me/clashbatttles/44"
DEPOSIT_VIDEO = "https://t.me/clashbatttles/44"
WITHDRAW_VIDEO = "https://t.me/clashbatttles/44"

# ================== BOT INIT ==================
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# ================== START ==================
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Register Now", url=REGISTER_URL)],
        [InlineKeyboardButton(text="Customer Support", url=SUPPORT_URL)],
        [InlineKeyboardButton(text="Join us on Telegram", url=JOIN_TG_URL)],
        [InlineKeyboardButton(text="How to Play", callback_data="play")],
        [InlineKeyboardButton(text="How to Deposit", callback_data="deposit")],
        [InlineKeyboardButton(text="How to Withdraw", callback_data="withdraw")]
    ])

    await message.answer_photo(
        photo=IMAGE_URL,
        caption="<b>WELCOME TO AVIATOR X OFFICIAL</b>\n\nAny Problem Send Query to Bot.",
        reply_markup=keyboard
    )

# ================== VIDEO HANDLERS ==================
@dp.callback_query(lambda c: c.data == "play")
async def play_video(call: types.CallbackQuery):
    await call.message.answer_video(
        video=PLAY_VIDEO,
        caption="🎮 <b>How to Play</b>\n\nWatch tutorial 👆"
    )
    await call.answer()

@dp.callback_query(lambda c: c.data == "deposit")
async def deposit_video(call: types.CallbackQuery):
    await call.message.answer_video(
        video=DEPOSIT_VIDEO,
        caption="💰 <b>How to Deposit</b>\n\nStep by step 👆"
    )
    await call.answer()

@dp.callback_query(lambda c: c.data == "withdraw")
async def withdraw_video(call: types.CallbackQuery):
    await call.message.answer_video(
        video=WITHDRAW_VIDEO,
        caption="🏧 <b>How to Withdraw</b>\n\nEasy process 👆"
    )
    await call.answer()

# ================== USER -> ADMIN ==================
@dp.message(lambda m: m.from_user.id != ADMIN_ID)
async def user_to_admin(message: types.Message):
    header = (
        f"📩 <b>User Message</b>\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 UserID: {message.from_user.id}\n\n"
    )

    if message.text:
        await bot.send_message(ADMIN_ID, header + message.text)
    else:
        await bot.send_message(ADMIN_ID, header + "<i>Media message</i>")
        await message.copy_to(ADMIN_ID)

    await message.reply("모 Your message has been sent to admin please wait.")

# ================== ADMIN -> USER (REPLY SYSTEM) ==================
@dp.message(lambda m: m.from_user.id == ADMIN_ID and m.reply_to_message)
async def admin_reply(message: types.Message):
    try:
        lines = message.reply_to_message.text.splitlines()
        user_id = int(
            [l for l in lines if l.startswith("🆔 UserID:")][0]
            .split(":")[1].strip()
        )

        if message.text:
            await bot.send_message(
                user_id,
                f"모 <b>Admin</b>\n\n{message.text}"
            )
        else:
            await message.copy_to(user_id)

    except Exception as e:
        print("Admin reply error:", e)

# ================== MAIN ==================
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
