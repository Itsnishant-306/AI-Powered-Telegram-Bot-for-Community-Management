import os
import pytz
from pytz import timezone
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, JobQueue
from bot.commands import start, help_command, leaderboard, sentiment_command
from bot.handlers import handle_message, handle_callback, about_command, faq_command, announce
from bot.scheduler import setup_scheduler
from database.operations import init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Set timezone to UTC
os.environ["TZ"] = "UTC"

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Start the bot."""
    # Initialize database
    init_db()
    
    # Create a scheduler with explicit UTC timezone
    scheduler = AsyncIOScheduler(timezone=timezone("UTC"))

    # Create bot application without passing scheduler
    app = Application.builder().token(TOKEN).build()
    
    # Get and attach job queue
    job_queue = app.job_queue

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("faq", faq_command))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("sentiment", sentiment_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Set up scheduled tasks
    await setup_scheduler(app)

    # Start the scheduler
    scheduler.start()
    
    # Start the bot
    logger.info("🤖 Bot started! Press Ctrl+C to stop.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())  # Standard execution
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()  # Apply only if needed
        asyncio.run(main())
