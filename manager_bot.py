from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from github_api import update_file
from settings import BOT_TOKEN, TARGET_REPO, TARGET_PATH

pending_file = None

async def start(update, context):
    await update.message.reply_text(
        "سلام عارف! اسم فایل رو با /edit بفرست.\nمثال:\n/edit main.py"
    )

async def edit_cmd(update, context):
    global pending_file
    args = update.message.text.split()

    if len(args) < 2:
        return await update.message.reply_text("فرمت درست:\n/edit filename.py")

    pending_file = args[1]
    await update.message.reply_text(
        f"اوکی! حالا کد جدید فایل {pending_file} رو بفرست.\nکل کد رو در یک پیام بفرست."
    )

async def receive_code(update, context):
    global pending_file
    if not pending_file:
        return await update.message.reply_text("اول باید اسم فایل رو با /edit بفرستی.")

    new_code = update.message.text
    full_path = TARGET_PATH + pending_file

    ok = update_file(TARGET_REPO, full_path, new_code)
    pending_file = None

    if ok:
        await update.message.reply_text("✅ فایل آپدیت شد. Railway الان داره ربات B رو Deploy می‌کنه.")
    else:
        await update.message.reply_text("❌ خطا در آپدیت فایل. مسیر یا توکن رو چک کن.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("edit", edit_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_code))

print("ربات مدیر روشن شد.")
app.run_polling()
