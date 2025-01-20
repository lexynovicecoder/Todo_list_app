import os
from dotenv import load_dotenv
load_dotenv()

db_type = os.getenv("DB_TYPE")  # Default to sqlite if not set
db_name = os.getenv("DB_NAME")  # Default to database.db if not set
DATABASE_URL = f"{db_type}:///./database/{db_name}"