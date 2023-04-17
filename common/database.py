from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db_engine = create_engine('mysql+pymysql://root:admin@127.0.0.1/library_system', echo=False, pool_size=100)
db_session = Session(db_engine)
