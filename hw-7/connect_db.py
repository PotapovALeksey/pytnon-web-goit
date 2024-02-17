from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mynotes.sqlite")
Session = sessionmaker(bind=engine)
session = Session()
