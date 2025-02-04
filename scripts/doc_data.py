# Install the necessary package first


import nest_asyncio
from telethon.sync import TelegramClient
import os
import asyncio
import logging
import telethon  # Import telethon here for exception handling
import csv  # Import CSV module for saving data

# Apply nest_asyncio for compatibility with Jupyter notebooks and other async environments
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)  # Change logging level as needed

# **Ensure you have a valid API ID and API hash from my.telegram.org**
API_ID = 20070625  # Replace with your API ID (as an integer)
API_HASH = 'e575003ddfb16cf5a391ed2322e37f6b'  # Replace with your API hash

# Define session file path
session_file = 'my_session.session'

# Check if the session file exists and delete it if it does
if os.path.exists(session_file):
    os.remove(session_file)
    logging.info(f"Removed existing session file: {session_file}")

# Create a Telegram client outside the loop to avoid creating multiple sessions
client = TelegramClient(session_file, API_ID, API_HASH)

# Explicitly connect the client and handle potential errors
# Replace 'your_phone_number' with your actual phone number
phone_number = 'your_phone_number'  # Update placeholder to your actual phone number

try:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        logging.info('Enter the code sent to your number: ')
        code = input()
        client.sign_in(phone_number, code)
    logging.info("Client connected successfully!")
except telethon.errors.rpcerrorlist.PhoneNumberInvalidError:
    logging.error("Invalid phone number. Please check your phone number.")
except Exception as e:
    logging.error(f"An error occurred during connection: {e}")

# Define the channels to scrape
channels = [
    'DoctorsET',
    'Chemed123',  # Corrected channel name, removed spaces
    'lobelia4cosmetics',
    'yetenaweg',
    'EAHCI'
]

# Define the functions to scrape data from each channel
async def scrape_channel(channel):
    try:
        # Ensure client is connected before making requests
        if not client.is_connected():
            await client.connect()

        channel_entity = await client.get_entity(channel)
        messages = await client.get_messages(channel_entity, limit=400)  # Adjust limit as needed
        return messages
    except telethon.errors.rpcerrorlist.UsernameInvalidError:  # telethon is now accessible
        logging.warning(f"Channel '{channel}' not found.")
        return []
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        return []

# Function to save data to CSV
def save_to_csv(data, filename):
    if not data:
        logging.info("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    logging.info(f"Data saved to {filename}")

# Main async function to execute scraping logic
async def main():
    all_data = []
    async with client:  # Use 'async with' for asynchronous context management
        for channel in channels:
            result = await scrape_channel(channel)
            for message in result:
                # Extract relevant data from the message
                message_data = {
                    'channel': channel,
                    'message_id': message.id,
                    'text': message.text or "",  # Handle NoneType
                    'date': message.date.strftime("%Y-%m-%d %H:%M:%S") if message.date else "",
                    'views': message.views or "",
                    'media_type': type(message.media).__name__ if message.media else ""
                }
                all_data.append(message_data)
                logging.info(f"Scraped message: {message.text} from channel: {channel}")

    # Save all data to CSV after scraping all channels
    save_to_csv(all_data, 'telegram_scraped_data.csv')

# Run the main function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())