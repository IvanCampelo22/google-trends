from sqlalchemy import Integer, String, Column, UUID
from database.conn import Base
import uuid

class RelatedEntitiesTop(Base):
    __tablename__ = 'RelatedEtitiesTop'
    __table_args__ = {'schema': 'google_trends'}


    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    param = Column(String, nullable=True)
    initial_date = Column(String, nullable=True)
    region = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    entities = Column(String, nullable=True)
    value = Column(String, nullable=True)


class RelatedEntitiesRising(Base):
    __tablename__ = 'RelatedEtitiesRising'
    __table_args__ = {'schema': 'google_trends'}


    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    param = Column(String, nullable=True)
    initial_date = Column(String, nullable=True)
    region = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    entities = Column(String, nullable=True)
    value = Column(String, nullable=True)