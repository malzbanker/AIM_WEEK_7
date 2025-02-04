
import nest_asyncio
import os
import csv
import logging
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import asyncio
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials (store in .env)
API_ID = int(os.getenv('API_ID', 20070625))  # Default is test credentials
API_HASH = os.getenv('API_HASH', 'e575003ddfb16cf5a391ed2322e37f6b')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')  # Store in .env as '+251...'

# Database configuration
DB_CONFIG = {
    'dbname': 'kara',
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD'),
    'host': 'localhost'
}

# File paths
CSV_PATH = 'scraped_data.csv'
IMAGE_DIR = 'downloaded_images'
os.makedirs(IMAGE_DIR, exist_ok=True)

# Initialize CSV with headers
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['message_id', 'channel', 'date', 'text', 'image_path'])

def create_db_connection():
    """Create PostgreSQL connection"""
    return psycopg2.connect(**DB_CONFIG)

async def save_to_database(message, channel_name, image_path=None):
    """Save message to PostgreSQL database"""
    conn = create_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO staging.raw_messages 
                (message_id, channel, date, text, image_path)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                message.id,
                channel_name,
                message.date,
                message.text,
                image_path
            ))
        conn.commit()
    except Exception as e:
        logger.error(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

async def download_image(client, message, channel_name):
    """Download and save image from message"""
    try:
        if isinstance(message.media, MessageMediaPhoto):
            image_path = os.path.join(IMAGE_DIR, f'{channel_name}_{message.id}.jpg')
            await client.download_media(message.media, file=image_path)
            logger.info(f"Downloaded image: {image_path}")
            return image_path
    except Exception as e:
        logger.error(f"Image download failed: {e}")
    return None

async def scrape_channel(client, channel_name):
    """Scrape messages from a Telegram channel"""
    try:
        entity = await client.get_entity(channel_name)
        async for message in client.iter_messages(entity, limit=100):
            # Download image for specific channels
            image_path = None
            if channel_name in ['Chemed123', 'lobelia4cosmetics']:
                image_path = await download_image(client, message, channel_name)

            # Save to CSV
            with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    message.id,
                    channel_name,
                    message.date,
                    message.text,
                    image_path
                ])

            # Save to PostgreSQL
            await save_to_database(message, channel_name, image_path)
            
    except Exception as e:
        logger.error(f"Error scraping {channel_name}: {str(e)}")

async def main():
    """Main scraping function"""
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        if not await client.is_user_authorized():
            await client.send_code_request(PHONE_NUMBER)
            await client.sign_in(PHONE_NUMBER, input('Enter code: '))
        
        channels = [
            'DoctorsET',
            'Chemed123',
            'lobelia4cosmetics',
            'yetenaweg',
            'EAHCI'
        ]

        for channel in channels:
            logger.info(f"Scraping channel: {channel}")
            await scrape_channel(client, channel)

if __name__ == '__main__':
    asyncio.run(main())