from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import users_col

app = Client("beyblade_pre_register", api_id=27548865, api_hash="db07e06a5eb288c706d4df697b71ab61",
             bot_token="7391978734:AAFX5BrojPJeL2cH0JGdwfCpztatqD6nXXg ")

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id

    user = users_col.find_one({"_id": user_id})
    if user and user.get("pre_registered"):
        return await message.reply_text("✅ You are already Pre-Registered! 🚀")

    await message.reply_text(
        "**🛠️ This bot is under Pre-Registration.**\n\n"
        "🎮 Version 1 launching soon...\n"
        "Click below to pre-register and claim exclusive rewards when we launch!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Pre-Register", callback_data="preregister")]
        ])
    )

@app.on_callback_query(filters.regex("preregister"))
async def preregister_handler(client, query: CallbackQuery):
    user_id = query.from_user.id

    # Check again to avoid double registration
    user = users_col.find_one({"_id": user_id})
    if user and user.get("pre_registered"):
        await query.answer("Already pre-registered!", show_alert=True)
        return

    users_col.update_one(
        {"_id": user_id},
        {"$set": {"pre_registered": True}},
        upsert=True
    )

    await query.message.edit_text(
        "✅ You are now **Pre-Registered**!\n\n"
        "🎁 You’ll receive exclusive in-game rewards once we go live.\nStay tuned!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/YourChannel")]
        ])
    )
