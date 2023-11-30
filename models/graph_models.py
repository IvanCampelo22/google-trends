from sqlalchemy import Integer, String, Column
from database.conn import Base

class Graphic(Base):
    __tablename__ = 'Graphic'
    __table_args__ = {'schema': 'google_trends'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    date = Column(String, nullable=True)
    hour = Column(String, nullable=True)
    value = Column(String, nullable=True)