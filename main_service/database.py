from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


#todo: can be converted to env variable via os.environ.get('DB_URL')
connection_url = 'postgresql://omermunk:1234@db-sql:5432/my_store_db'
engine = create_engine(connection_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
