import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== CONFIG ==================
BOT_TOKEN = "8567155226:AAHPR41Y9VIT8sGFHjj1n3b4vXswTOMOyLs"
ADMIN_ID = 8273671529   # 👈 apni Telegram numeric ID

VIDEO_URL = "https://t.me/clashbatttles/44"   # tutorial video (same for all)
WELCOME_IMAGE = "https://i.imgur.com/9ZQZQZB.jpg"  # optional image

REGISTER_LINK = "https://coreversions"
CHANNEL_LINK = "https://t.me/coreversions"
# ============================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ================== BUTTONS ==================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("📝 Register Now", url=REGISTER_LINK),
        InlineKeyboardButton("🎮 How to Play", callback_data="how_play"),
        InlineKeyboardButton("💰 How to Deposit", callback_data="how_deposit"),
        InlineKeyboardButton("🏧 How to Withdraw", callback_data="how_withdraw"),
        InlineKeyboardButton("🧑‍💻 Customer Support", callback_data="support"),
        InlineKeyboardButton("📢 Join Telegram", url=CHANNEL_LINK),
    )
    return kb


# ================== /START ==================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer_photo(
        photo=WELCOME_IMAGE,
        caption=(
            "<b>WELCOME TO AVIATOR X OFFICIAL ✈️</b>\n\n"
            "Please choose an option below 👇"
        ),
        reply_markup=main_menu()
    )


# ================== TUTORIAL VIDEO ==================
@dp.callback_query_handler(lambda c: c.data in ["how_play", "how_deposit", "how_withdraw"])
async def tutorial(call: types.CallbackQuery):
    titles = {
        "how_play": "🎮 How to Play",
        "how_deposit": "💰 How to Deposit",
        "how_withdraw": "🏧 How to Withdraw",
    }

    await call.message.answer_video(
        video=VIDEO_URL,
        caption=f"<b>{titles[call.data]}</b>\n\nStep by step tutorial 👆"
    )
    await call.answer()


# ================== SUPPORT BUTTON ==================
@dp.callback_query_handler(lambda c: c.data == "support")
async def support(call: types.CallbackQuery):
    await call.message.answer(
        "🧑‍💻 <b>Customer Support</b>\n\n"
        "Please type your message.\n"
        "Admin will reply here through the bot."
    )
    await call.answer()


# ================== USER → ADMIN ==================
@dp.message_handler(lambda m: m.from_user.id != ADMIN_ID)
async def user_to_admin(message: types.Message):
    text = (
        f"📩 <b>User Message</b>\n\n"
        f"👤 Name: {message.from_user.full_name}\n"
        f"🆔 UserID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.reply("✅ Your message has been sent to admin.")


# ================== ADMIN → USER (RELAY) ==================
@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.reply_to_message)
async def admin_to_user(message: types.Message):
    try:
        # admin jis message par reply kar raha hai, usme se user id nikalo
        for line in message.reply_to_message.text.splitlines():
            if line.startswith("🆔 UserID:"):
                user_id = int(line.replace("🆔 UserID:", "").strip())
                break

        # admin ka reply USER ko bhejo (bot ke through)
        await bot.send_message(
            user_id,
            f"🧑‍💻 <b>Admin Reply</b>\n\n{message.text}"
        )

        # ❌ admin chat me koi extra message nahi
    except:
        pass


# ================== RUN ==================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
