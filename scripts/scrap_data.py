
import nest_asyncio
import telethon
from telethon.sync import TelegramClient
import os # Import os module
import asyncio # Import asyncio

nest_asyncio.apply()

# **Ensure you have a valid API ID and API hash from my.telegram.org**
API_ID = 20070625  # Replace with your API ID (as an integer)
API_HASH = 'e575003ddfb16cf5a391ed2322e37f6b'  # Replace with your API hash

# Define session file path 
session_file = 'my_session.session'

# Check if the session file exists and delete it if it does
if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Removed existing session file: {session_file}")
    
# Create a Telegram client outside the loop
# to avoid creating multiple sessions
client = TelegramClient(session_file, API_ID, API_HASH)

# Explicitly connect the client and handle potential errors
# Replace 'your_phone_number' with your actual phone number 
# in international format (e.g., '+15551234567')
phone_number = 'your_phone_number'  

try:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number) 
        print('Enter the code sent to your number: ')
        code = input()
        client.sign_in(phone_number, code)
    print("Client connected successfully!")
except telethon.errors.rpcerrorlist.PhoneNumberInvalidError:
    print("Invalid phone number. Please check your phone number.")
except Exception as e:
    print(f"An error occurred during connection: {e}")

# Define the channels to scrape
channels = [
    'DoctorsET',
    'Chemed Telegram Channel',
    'lobelia4cosmetics',
    'yetenaweg',
    'EAHCI'
]

# Define the functions to scrape data from each channel
def scrape_channel(channel):
    async def inner():
        try:
            # Ensure client is connected before making requests
            if not client.is_connected():
                await client.connect() 
            channel_entity = await client.get_entity(channel)
            messages = await client.get_messages(channel_entity, limit=100)
            return messages
        except telethon.errors.rpcerrorlist.UsernameNotOccupiedError:
            print(f"Channel '{channel}' not found.")
            return []  # Return an empty list if the channel is not found
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return []

    return inner

# Scrape data from each channel and store it in a database
# (Assuming you have 'db' and 'db.session' defined)
async def main(): # Define an async function to run the scraping logic
  async with client: # Use 'async with' for asynchronous context management
      for channel in channels:
          result = await scrape_channel(channel)() # Await the result of the scrape_channel function
          for message in result:
              # Store the message in a database (replace with your actual database logic)
              # db.session.add(message) 
              print(message) # Replace with your database logic
          # db.session.commit()

# Run the main function using asyncio.run
asyncio.run(main())