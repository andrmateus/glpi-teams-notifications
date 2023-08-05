from db.sqlite_engine import Session, engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer)
    office = Column(String(255))
    expired_notified = Column(Boolean, default=False)
    less_than_30m_notified = Column(Boolean, default=False)
    less_than_1h_notified = Column(Boolean, default=False)
    less_than_2h_notified = Column(Boolean, default=False)


# Create the table in the database
Base.metadata.create_all(engine)
