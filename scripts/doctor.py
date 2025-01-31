import csv
from telethon import TelegramClient

# Sample data from Telegram scraping
scraped_data = [
    {"message_id": 1, "text": "Medicine available", "channel": "DoctorsET", "date": "2023-10-01"},
    {"message_id": 2, "text": "New clinic opening", "channel": "Chemed", "date": "2023-10-02"}
]

# Save to CSV
with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['message_id', 'text', 'channel', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in scraped_data:
        writer.writerow(row)



        