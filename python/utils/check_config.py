import os
from dotenv import load_dotenv

load_dotenv()

print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))

password = os.getenv("DB_PASSWORD")

if password:
    print("DB_PASSWORD: Loaded")
else:
    print("DB_PASSWORD: NOT LOADED")