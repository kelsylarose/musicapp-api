from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Cria as tabelas automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MusicApp API", version="1.0.0")

# Permite que o app Expo (que corre noutro domínio) aceda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # em produção troque por domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Rota de teste ──────────────────────────────────────
@app.get("/")
def read_root():
    return {"message": "MusicApp API funcionando!", "docs": "/docs"}


# ─── Listar todas as músicas ────────────────────────────
@app.get("/songs", response_model=List[schemas.SongOut])
def list_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).all()


# ─── Obter uma música ──────────────────────────────────
@app.get("/songs/{song_id}", response_model=schemas.SongOut)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return song


# ─── Adicionar música ──────────────────────────────────
@app.post("/songs", response_model=schemas.SongOut, status_code=201)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    new_song = models.Song(**song.model_dump())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


# ─── Remover música ────────────────────────────────────
@app.delete("/songs/{song_id}", status_code=204)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    db.delete(song)
    db.commit()
    return None


# ─── Listar favoritos ──────────────────────────────────
@app.get("/favorites", response_model=List[schemas.SongOut])
def list_favorites(db: Session = Depends(get_db)):
    return db.query(models.Song).filter(models.Song.is_favorite == True).all()


# ─── Marcar/desmarcar favorito ─────────────────────────
@app.post("/favorites/{song_id}", response_model=schemas.SongOut)
def toggle_favorite(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    song.is_favorite = not song.is_favorite
    db.commit()
    db.refresh(song)
    return song