# bot/scheduler.py
from datetime import time
from telegram.ext import CallbackContext
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.operations import get_active_users
import random

async def send_motivation(context: CallbackContext):
    """Send a daily motivational message to all users."""
    messages = [
        "🌟 Keep pushing forward!",
        "🚀 The best time to start is now.",
        "🔥 Believe in yourself!",
        "💡 Every day is a new opportunity."
    ]
    from database.operations import get_all_users
    users = get_all_users()
    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=random.choice(messages))
        except Exception as e:
            print(f"⚠️ Error sending motivation: {e}")

"""def setup_scheduler(app):
    #Schedule daily tasks.
    job_queue = app.job_queue
    #job_queue.run_daily(send_motivation, time=time(9, 0))  # Sends at 9 AM daily
    job_queue.run_daily(lambda context: context.job_queue.run_once(send_motivation, when=0), time=time(9, 0))"""


async def send_daily_update(context: CallbackContext):
    """Send daily updates to community members."""
    bot = context.bot
    active_users = get_active_users()
    
    message = (
        "🌟 Daily Update from Systemic Altruism 🌟\n\n"
        "Here's what's happening in our community today:\n"
        "• New discussion on effective giving\n"
        "• Upcoming webinar this Friday\n"
        "• New resources added to our library\n\n"
        "Stay engaged and keep making a difference!"
    )
    
    """for user_id in active_users:
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")"""
    for user in active_users:
        try:
            chat_id = int(user['user_id'])  # ✅ Convert to int to avoid errors
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"⚠️ Failed to send message to {user}: {e}")

async def setup_scheduler(app):
    """Set up scheduled tasks."""
    scheduler = AsyncIOScheduler()

     # Schedule daily motivation at 9 AM
    #scheduler.add_job(send_motivation, trigger=CronTrigger(hour=1, minute=28), id="daily_motivation", args=[app])
    scheduler.add_job(send_motivation, trigger=CronTrigger(hour=1, minute=48), id="daily_motivation", kwargs={"context": app})

    
    # Schedule daily updates at 9 AM
    #scheduler.add_job(send_daily_update, trigger=CronTrigger(hour=1, minute=28), id='daily_update', args=[app])
    scheduler.add_job(send_daily_update, trigger=CronTrigger(hour=1, minute=49), id='daily_update', kwargs={"context": app})


    scheduler.start()
    
    """# Schedule daily updates at 9 AM
    scheduler.add_job(
        send_daily_update, 
        trigger=CronTrigger(hour=9, minute=0), 
        id='daily_update',
        args=[app]  # ✅ CORRECT

    )
    
    scheduler.start()"""
