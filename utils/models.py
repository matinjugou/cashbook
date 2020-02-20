from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime, Date, Text, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Cashbook(Base):
    __tablename__ = 'cashbook'

    id = Column(String(32), nullable=False, primary_key=True)
    title = Column(String(1024), nullable=False, default='')
    content = Column(String(4096), nullable=False, default='')
    template = Column(String(4096), nullable=False, default='平桥乡')
    area = Column(String(4096), nullable=False, default='平桥乡')
    accounting_date = Column(Date, nullable=False, default=datetime.now())
