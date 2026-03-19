import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from database import init_db, search_scammer, add_scammer
from keyboards import main_menu, admin_menu
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# States for conversation
SEARCHING, REPORTING = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_db() # Ensure tables exist
    await update.message.reply_text("🛡️ **BGMI Trust Bot**\nSelect an option:", 
                                   reply_markup=main_menu(), parse_mode='Markdown')
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Admin Tools:", reply_markup=admin_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'search':
        await query.message.reply_text("🔍 Send the **BGMI Character ID** to check:")
        return SEARCHING
    elif query.data == 'report':
        await query.message.reply_text("📢 Send ID and Proof link like this:\n`ID - Reason - ProofLink`")
        return REPORTING

async def process_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    result = search_scammer(user_input)
    
    if result:
        await update.message.reply_text(f"❌ **SCAMMER FOUND!**\n\n🆔 ID: {result[0]}\n⚠️ Reason: {result[1]}\n🔗 Proof: {result[2]}", parse_mode='Markdown')
    else:
        await update.message.reply_text("✅ No records found. Always use a middleman!")
    return ConversationHandler.END

async def process_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only Admin can add to DB in this basic pro version
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only Admins can submit reports currently.")
        return ConversationHandler.END
    
    data = update.message.text.split(" - ")
    if len(data) == 3:
        add_scammer(data[0], data[1], data[2], str(update.effective_user.id))
        await update.message.reply_text("✅ Scammer added to Blacklist!")
    else:
        await update.message.reply_text("❌ Wrong format! Use: ID - Reason - Link")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_buttons)],
        states={
            SEARCHING: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search)],
            REPORTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_report)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
