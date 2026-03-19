from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🔍 Search ID", callback_data='search')],
        [InlineKeyboardButton("📢 Report Scammer", callback_data='report')],
        [InlineKeyboardButton("✅ Trusted Sellers", callback_data='sellers')],
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_menu():
    keyboard = [
        [InlineKeyboardButton("➕ Add Scammer", callback_data='add_scam')],
        [InlineKeyboardButton("➕ Add Seller", callback_data='add_sell')],
    ]
    return InlineKeyboardMarkup(keyboard)
