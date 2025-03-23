import os
import pytz
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.commands import start, help_command, leaderboard
from bot.handlers import handle_message, handle_callback
from bot.scheduler import setup_scheduler
from database.operations import init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
    
    # Create a scheduler with explicit timezone
    scheduler = AsyncIOScheduler(timezone="UTC")
    
    # Create the Application with the custom scheduler
    application_builder = Application.builder().token(TOKEN)
    # Disable the default job queue to prevent automatic creation
    application_builder._job_queue = None
    app = application_builder.build()
    
    # Manually create and attach job queue with our scheduler
    from telegram.ext import JobQueue
    job_queue = JobQueue()
    job_queue.scheduler = scheduler
    job_queue = app.job_queue  # ✅ CORRECT! Get the job queue from 'app'

    #app.job_queue = job_queue
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard))

    from bot.handlers import about_command, faq_command
    app.add_handler(CommandHandler("about", about_command))  # ✅ Fix for /about
    app.add_handler(CommandHandler("faq", faq_command))      # ✅ Fix for /faq

    from bot.handlers import announce
    app.add_handler(CommandHandler("announce", announce))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    from bot.commands import sentiment_command
    app.add_handler(CommandHandler("sentiment", sentiment_command))

    
    # Register callback query handler
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Set up scheduled tasks
    #setup_scheduler(app)
    await setup_scheduler(app)  # ✅ Correct

    
    # Start the scheduler
    scheduler.start()
    
    # Start the bot
    logger.info("🤖 Bot started! Press Ctrl+C to stop.")
    await app.run_polling()

"""
if __name__ == "__main__":
    import asyncio
    #asyncio.run(main())  # Run the bot using asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())  # ✅ Safe way to run inside an existing loop
    #asyncio.get_event_loop().run_until_complete(main())  # ✅ Safe way to run inside an existing loop
"""
if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())  # ✅ Standard execution
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()  # ✅ Only apply if needed
        asyncio.run(main())