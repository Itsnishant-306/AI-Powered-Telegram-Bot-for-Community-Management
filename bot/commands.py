# bot/commands.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
#from database.operations import create_user_if_not_exists, get_leaderboard

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    from database.operations import create_user_if_not_exists, get_leaderboard
    user = update.effective_user
    create_user_if_not_exists(user.id, user.username, user.first_name)
    
    keyboard = [
        [
            InlineKeyboardButton("About Us", callback_data='about'),
            InlineKeyboardButton("FAQ", callback_data='faq'),
        ],
        [InlineKeyboardButton("Join Community", callback_data='join')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f'Hello {user.first_name}! Welcome to Systemic Altruism Community Bot. '
        f'How can I help you today?',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Here are the commands you can use:\n'
        '/start - Start the bot\n'
        '/help - Show this help message\n'
        '/about - Learn about Systemic Altruism\n'
        '/faq - Frequently asked questions\n'
        '/events - Upcoming events'
    )

def about(update: Update, context: CallbackContext) -> None:
    """Send information about Systemic Altruism."""
    update.message.reply_text(
        'Systemic Altruism is a community focused on creating positive impact '
        'through systematic approaches to charitable giving and social good.'
    )

    # Add to bot/commands.py

async def leaderboard(update: Update, context: CallbackContext) -> None:
    """Show the community leaderboard."""
    from database.operations import get_leaderboard
    leaderboard_data = get_leaderboard(10)
    
    message = "🏆 Community Engagement Leaderboard 🏆\n\n"
    for i, user in enumerate(leaderboard_data, 1):
        message += f"{i}. {user['username']}: {user['points']} points\n"
    
    message += "\nKeep engaging to earn more points!"
    await update.message.reply_text(message)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from ai.nlp_processor import analyze_sentiment  # Import your sentiment function

async def sentiment_command(update: Update, context: CallbackContext) -> None:
    """Runs sentiment analysis only when user types /sentiment"""
    if not context.args:  # If no text is provided
        await update.message.reply_text("Please provide a message to analyze.\nUsage: /sentiment Your message here.")
        return
    
    message_text = " ".join(context.args)  # Join the message after the command
    sentiment = await analyze_sentiment(message_text)  # Run sentiment analysis
    
    # Respond based on sentiment
    if sentiment == "negative":
        await update.message.reply_text("Sounds negative! What happened?")
    elif sentiment == "positive":
        await update.message.reply_text("Sounds positive! 😊 That's great to hear!")
    else:
        await update.message.reply_text("Umm, Okay!")