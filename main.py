from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import users_col  # MongoDB collection (must be motor async)
from datetime import datetime

app = Client(
    "beyblade_pre_register",
    api_id=27548865,
    api_hash="db07e06a5eb288c706d4df697b71ab61",
    bot_token="7391978734:AAHCn_W4UMO_spWacqNBHW96A1c6BpUX3E4"
)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id

    user = await users_col.find_one({"_id": user_id})
    if user and user.get("pre_registered"):
        return await message.reply_text("✅ You are already Pre-Registered! 🚀")

    await message.reply_text(
        "**🛠️ Welcome to BEYBLADE WARS Pre-Registration!**\n\n"
        "🎮 Version 1 launching soon...\n"
        "Click the button below to pre-register and claim exclusive launch rewards!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Pre-Register", callback_data="preregister")]
        ])
    )

@app.on_callback_query(filters.regex("^preregister"))
async def preregister_handler(client, query: CallbackQuery):
    user_id = query.from_user.id

    user = await users_col.find_one({"_id": user_id})
    if user and user.get("pre_registered"):
        await query.answer("✅ Already pre-registered!", show_alert=True)
        return

    await users_col.update_one(
        {"_id": user_id},
        {"$set": {
            "pre_registered": True,
            "name": query.from_user.first_name,
            "username": query.from_user.username,
            "joined_at": datetime.utcnow().isoformat()
        }},
        upsert=True
    )

    await query.message.edit_text(
        "🎉 You are now **Pre-Registered!**\n\n"
        "🎁 You’ll receive exclusive in-game rewards on launch day.\n"
        "📢 Stay updated via our channel!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/Bey_war_updates")]
        ])
    )
    await query.answer("🎯 Registered Successfully!", show_alert=True)

print("BOT STARTED")
app.run()
