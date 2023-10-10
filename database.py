from sqlalchemy.orm import sessionmaker

from models import Base
from dotenv import load_dotenv
import os


from sqlalchemy import create_engine

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}", echo=True)
Base.metadata.create_all(engine)

connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
