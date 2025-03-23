# utils/helpers.py
import datetime

def get_current_time():
    """Return the current time in a readable format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_message_for_logging(message, user=None):
    """Format a message for logging purposes."""
    time = get_current_time()
    if user:
        return f"[{time}] {user.first_name} ({user.id}): {message}"
    return f"[{time}] Bot: {message}"

def chunk_text(text, max_length=4096):
    """
    Chunk text into smaller pieces to avoid Telegram's message length limitation.
    Telegram has a 4096 character limit per message.
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        # Find the last space within max_length
        split_point = text[:max_length].rfind(' ')
        if split_point == -1:  # No space found, force split
            split_point = max_length
        
        chunks.append(text[:split_point])
        text = text[split_point:].lstrip()
    
    return chunks