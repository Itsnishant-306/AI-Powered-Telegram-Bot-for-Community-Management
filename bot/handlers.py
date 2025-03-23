# bot/handlers.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from ai.nlp_processor import get_ai_response
from database.operations import increment_user_points, save_message
from utils.helpers import chunk_text

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle the user message."""
    message_text = update.message.text
    user_id = update.effective_user.id
    
    # Save the message to database
    save_message(user_id, message_text)
    
    # Increment user points for engagementa
    increment_user_points(user_id)
    
    # Get AI-powered response
    response = await get_ai_response(message_text, user_id)
    
    # Save the bot's response
    save_message(user_id, response, is_bot=True)

    """from ai.nlp_processor import analyze_sentiment
    sentiment = await analyze_sentiment(message_text)
    if sentiment == "negative":
        await update.message.reply_text("Sounds negative! What happened?")
    elif sentiment == "positive":
        await update.message.reply_text("Sounds positive! 😊 That's great to hear!")
    else: 
        await update.message.reply_text("Umm, Okay!")"""

    
    # Handle long responses by chunking them
    chunks = chunk_text(response)
    for chunk in chunks:
        await update.message.reply_text(chunk)

async def handle_callback(update: Update, context: CallbackContext) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'about':
        await query.edit_message_text(
            'Systemic Altruism is a community focused on creating positive impact '
            'through systematic approaches to charitable giving and social good.'
        )
    elif query.data == 'faq':
        keyboard = [
            [InlineKeyboardButton("How to join?", callback_data='join_faq')],
            [InlineKeyboardButton("What do we do?", callback_data='activities_faq')],
            [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('Frequently Asked Questions:', reply_markup=reply_markup)
    elif query.data == 'join':
        await query.edit_message_text(
            'Great! To join our community, please fill out this form: [link to form]\n'
            'After submission, an admin will review and approve your request.'
        )
    elif query.data == 'join_faq':
        await query.edit_message_text(
            'To join Systemic Altruism, start by using the /start command and then '
            'click on the "Join Community" button. You\'ll be guided through the process.\n\n'
            'Back to [FAQ](callback_data=faq)'
        )
    elif query.data == 'activities_faq':
        await query.edit_message_text(
            'Systemic Altruism organizes events, discussions, and initiatives focused on '
            'effective altruism and systematic approaches to social good.\n\n'
            'Back to [FAQ](callback_data=faq)'
        )
    elif query.data == 'main_menu':
        keyboard = [
            [
                InlineKeyboardButton("About Us", callback_data='about'),
                InlineKeyboardButton("FAQ", callback_data='faq'),
            ],
            [InlineKeyboardButton("Join Community", callback_data='join')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            'Welcome to Systemic Altruism Community Bot. How can I help you today?',
            reply_markup=reply_markup
        )

async def faq_command(update: Update, context: CallbackContext) -> None:
    """Send FAQ info when user types /faq."""
    keyboard = [
        [InlineKeyboardButton("How to join?", callback_data='join_faq')],
        [InlineKeyboardButton("What do we do?", callback_data='activities_faq')],
        [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Frequently Asked Questions:", reply_markup=reply_markup)

async def about_command(update: Update, context: CallbackContext) -> None:
    """Send About info when user types /about."""
    await update.message.reply_text(
        "Systemic Altruism is a community focused on creating positive impact "
        "through systematic approaches to charitable giving and social good."
    )

from telegram import Chat
from database.operations import get_all_users  # Fetch users from Firebase

ADMIN_IDS = [5750325083]  # Add your Telegram user ID here

async def announce(update: Update, context: CallbackContext):
    """Admin command to send announcements to all users."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You are not authorized to send announcements.")
        return

    announcement = ' '.join(context.args)
    if not announcement:
        await update.message.reply_text("Usage: /announce <Attention guys! I am happy to announce that, our community is rapidly growing.>")
        return

    users = await get_all_users()  # Fetch all users from Firebase
    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=f"📢 Announcement: {announcement}")
        except Exception as e:
            print(f"⚠️ Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("✅ Announcement sent!")


from database.operations import get_leaderboard
def leaderboard(update: Update, context: CallbackContext):
    """Show top active users."""
    top_users = get_leaderboard()
    update.message.reply_text(f"🏆 Leaderboard:\n{top_users}")
