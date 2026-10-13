from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    artwork = Column(String, nullable=False)
    url = Column(String, nullable=False)
    duration = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)