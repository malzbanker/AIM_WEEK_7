import requests
from bs4 import BeautifulSoup
# Import necessary database libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Database setup (replace with your actual database details)
DATABASE_URL = "mysql+pymysql://postgres:postgres@localhost:5432/kara"
# Create an engine
engine = create_engine(DATABASE_URL) # Replace with your database URL
Base = declarative_base()
# Define a model for 'scraped_data'
class ScrapedData(Base):
    __tablename__ = 'scraped_data'
    id = Column(Integer, primary_key=True)
    message_text = Column(String)
    channel_name = Column(String)
    # Add other columns as needed

Base.metadata.create_all(engine)  # Create the table # Create the table if it doesn't exist
Session = sessionmaker(bind=engine)
db = Session() # Create a session object

# Define the URLs of the channels to scrape images from
urls = [
    'https://t.me/Chemed123',
    'https://t.me/lobelia4cosmetics'
]

# Define the function to scrape images from each channel
def scrape_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    return images

# Scrape images from each channel and store them in a database
for url in urls:
    images = scrape_images(url)
    for image in images:
        # Store the image URL in the database
        image_url = image.get('src') # Get the image source URL
        db.add(Image(url=image_url))  # Create an Image instance and add to session
    db.commit()

# Close the session
db.close()