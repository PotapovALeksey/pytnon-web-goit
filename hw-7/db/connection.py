from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db/school")
Session = sessionmaker(bind=engine)
session = Session()
