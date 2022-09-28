import motor.motor_asyncio
from models.user import User

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.melody_generator
collection_user = database.users
collection_melodies = database.melodies