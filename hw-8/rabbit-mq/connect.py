from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

db_uri = os.environ["DB_URI"]

connect(host=db_uri)
