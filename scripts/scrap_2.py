import asyncio
from telethon.sync import TelegramClient
import csv
import nest_asyncio
import os

# Telegram API credentials
API_ID = 20070625
API_HASH = 'e575003ddfb16cf5a391ed2322e37f6b'
SESSION_NAME = 'my_session'

# Channels to scrape
CHANNELS = [
    'DoctorsET',
    'Chemed123',
    'lobelia4cosmetics',
    'yetenaweg',
    'EAHCI'
]

# Apply nest_asyncio to enable running within existing event loop
nest_asyncio.apply()

# Define session file path
session_file = f'{SESSION_NAME}.session'

# Check if the session file exists and delete it if it does
if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Removed existing session file: {session_file}")

# Scrape data from Telegram channels
async def scrape_telegram_channels(): # Define as async function
    # Create the TelegramClient outside the loop
    client = TelegramClient(session_file, API_ID, API_HASH)
    await client.start() # Use await for asynchronous operations

    try:
        for channel in CHANNELS:
            print(f"Scraping {channel}...")
            messages = await client.get_messages(channel, limit=500)  # Use await to get messages
            with open(f'{channel}_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'text', 'date', 'views', 'media_type'])
                for message in messages:
                    writer.writerow([
                        message.id,
                        message.text,
                        message.date,
                        message.views,
                        type(message.media).__name__ if message.media else None
                    ])
    finally:
        await client.disconnect() # Use await for disconnect, ensure it happens even if errors occur


# Run the asynchronous function using asyncio.run
asyncio.run(scrape_telegram_channels())