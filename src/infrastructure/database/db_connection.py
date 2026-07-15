from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import Settings


class DataBaseSession:

 """
 DataBaseSession module arranges SQLAlchemy Engine settings and
 manages database (in this project it's SQLite) connection sessions
 """

 def __init__(self):
  self.engine = create_engine(Settings.DATABASE_URL, echo = False) #gets the database_url from config/settings
  self.Session = sessionmaker(bind = self.engine)

 def get_session(self):
  return self.Session()

 # def close_session(self):
 #  self.session.close()

 #session.commit(), session.close(), session.rollback()
