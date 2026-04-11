import os
from dotenv import load_dotenv

load_dotenv()

print(f"CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"CLOUDINARY_API_SECRET: {'***' if os.getenv('CLOUDINARY_API_SECRET') else 'None'}")
