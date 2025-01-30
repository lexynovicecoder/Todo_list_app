from sqlmodel import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL,connect_args=connect_args)


