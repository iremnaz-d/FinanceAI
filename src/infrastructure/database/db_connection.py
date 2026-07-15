from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import Settings


class DataBaseSession:

 """
 DataBaseSession module arranges SQLAlchemy Engine settings and
 manages database (in this project it's SQLite) connection sessions
 """

 engine = create_engine(Settings.DATABASE_URL, echo = False) #gets the database_url from config/settings
 Session = sessionmaker(bind = engine)
 session = Session()

 def get_session(self):
  return self.session

 def close_session(self):
  self.session.close()

 #session.commit(), session.close(), session.rollback()
