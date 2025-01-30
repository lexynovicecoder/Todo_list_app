import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

payload_data = {
    "sub": "6031957",
    "name": "Alexandra",
    "admin": True
}

token = jwt.encode(payload=payload_data, key=JWT_SECRET_KEY, algorithm="HS256")
print(token)
