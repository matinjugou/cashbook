from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings
import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine(settings.database_address, pool_recycle=1801)
db = sessionmaker(bind=engine)
