from sqlalchemy import Integer, String, Column, UUID
from database.conn import Base
import uuid

class Graphic(Base):
    __tablename__ = 'Graphic'
    __table_args__ = {'schema': 'google_trends'}

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=True)
    date = Column(String, nullable=True)
    hour = Column(String, nullable=True)
    value = Column(String, nullable=True)