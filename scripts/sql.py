from sqlalchemy import create_engine

# Replace these variables with your own information
username = 'postgres'
password = 'Malede@191919'
hostname = 'localhost'  # or your database server
database = 'kara'
port = '5432'  # default PostgreSQL port

# Create a SQLAlchemy engine
DATABASE_URL = f'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'
engine = create_engine(DATABASE_URL)

# Connect to the database
with engine.connect() as connection:
    print("Connection successful!")

    # Execute SQL queries
    # result = connection.execute("SELECT * FROM your_table;")
    # for row in result:
    #     print(row)