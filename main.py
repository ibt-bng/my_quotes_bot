from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import logging

# Enable logging (for debugging)
logging.basicConfig(level=logging.INFO)

# Portfolio Data
PORTFOLIO = {
    "about": "👋 Hi, I'm Alex! A full-stack developer with a passion for creating awesome web apps.",
    "skills": "🛠 Python, JavaScript, React, Django, Docker, PostgreSQL",
    "projects": [
        {"name": "Portfolio Website", "url": "https://yourportfolio.com"},
        {"name": "Task Manager App", "url": "https://github.com/you/taskapp"},
    ],
    "resume_url": "https://yourportfolio.com/resume.pdf",
    "contact": "📧 Email: you@example.com\n📱 Telegram: @yourhandle"
}


# Create the main menu as inline keyboard
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 About", callback_data="about")],
        [InlineKeyboardButton("💼 Projects", callback_data="projects")],
        [InlineKeyboardButton("🧠 Skills", callback_data="skills")],
        [InlineKeyboardButton("📎 Resume", callback_data="resume")],
        [InlineKeyboardButton("📬 Contact", callback_data="contact")],
    ])


# Back to menu button
def back_to_menu_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
    ])


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=get_main_menu())


# Callback handler
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.edit_message_text("Choose an option:", reply_markup=get_main_menu())

    elif data == "about":
        await query.edit_message_text(PORTFOLIO["about"], reply_markup=back_to_menu_button())

    elif data == "projects":
        msg = "💼 Projects:\n"
        for p in PORTFOLIO["projects"]:
            msg += f"🔗 {p['name']}: {p['url']}\n"
        await query.edit_message_text(msg, reply_markup=back_to_menu_button())

    elif data == "skills":
        await query.edit_message_text(PORTFOLIO["skills"], reply_markup=back_to_menu_button())

    elif data == "resume":
        await query.edit_message_text(f"📎 Download my resume:\n{PORTFOLIO['resume_url']}", reply_markup=back_to_menu_button())

    elif data == "contact":
        await query.edit_message_text(PORTFOLIO["contact"], reply_markup=back_to_menu_button())

    else:
        await query.edit_message_text("❓ Unknown option", reply_markup=back_to_menu_button())


# Main runner
def main():
    app = ApplicationBuilder().token("8497518526:AAFWvZm6y2wkKV8kbPyDOR_7YcFhPpkoKuo").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


