from pydantic import BaseModel


class SongBase(BaseModel):
    title: str
    artist: str
    artwork: str
    url: str
    duration: int = 0


class SongCreate(SongBase):
    pass


class SongOut(SongBase):
    id: int
    is_favorite: bool

    class Config:
        from_attributes = True