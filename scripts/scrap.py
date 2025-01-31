

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import logging
import os
import asyncio  # Import asyncio
import nest_asyncio # Import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = '20070625'
API_HASH = 'e575003ddfb16cf5a391ed2322e37f6b'
CHANNELS = ['DoctorsET', 'Chemed', 'lobelia4cosmetics', 'yetenaweg', 'EAHCI']
IMAGE_DIR = 'downloaded_images'
os.makedirs(IMAGE_DIR, exist_ok=True)

async def main():  # Define an async function
    # Use a unique session name to avoid conflicts.
    # If the session file doesn't exist, it will be created.
    # If it exists, it will be reused.
    async with TelegramClient('my_unique_session_name', API_ID, API_HASH) as client:  
        for channel in CHANNELS:
            try:
                async for message in client.iter_messages(channel):  # Use async for
                    # Extract text data
                    text_data = {
                        'message_id': message.id,
                        'date': message.date,
                        'text': message.text,
                        'channel': channel
                    }
                    # Save text data to PostgreSQL raw table (see schema below)

                    # Download images for specific channels
                    if channel in ['Chemed', 'lobelia4cosmetics'] and isinstance(message.media, MessageMediaPhoto):
                        image_path = os.path.join(IMAGE_DIR, f'{channel}_{message.id}.jpg')
                        await client.download_media(message.media, file=image_path)  # Use await
                        logger.info(f"Downloaded image: {image_path}")

            except Exception as e:
                logger.error(f"Error in {channel}: {e}")

if __name__ == "__main__":  # Ensure main() is only called when the script is run directly
    asyncio.run(main())  # Run the async function