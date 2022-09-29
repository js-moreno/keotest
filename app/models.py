from sqlalchemy import Column, Integer, Text

from app.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    array = Column(Text, unique=True)
    result = Column(Integer)