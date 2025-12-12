import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://invest:investpass@127.0.0.1:3306/investtrack")
