from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db, SessionLocal

# Cria as tabelas automaticamente
models.Base.metadata.create_all(bind=engine)


# ─── Popular a BD com músicas se estiver vazia ────────
def seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(models.Song).count() == 0:
            SONGS = [
                {
                    "title": "Someone Like You (Piano Cover)",
                    "artist": "Scott Bradlee",
                    "artwork": "https://picsum.photos/seed/adele/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                    "duration": 372,
                },
                {
                    "title": "R&B Vibes (Non Copyright)",
                    "artist": "Sajeric",
                    "artwork": "https://picsum.photos/seed/beyonce/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                    "duration": 425,
                },
                {
                    "title": "Roots Rock Reggae (Instrumental)",
                    "artist": "Reggae Tribute Band",
                    "artwork": "https://picsum.photos/seed/marley/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                    "duration": 310,
                },
                {
                    "title": "Shape of You (Acoustic Cover)",
                    "artist": "Acoustic Covers",
                    "artwork": "https://picsum.photos/seed/edsheeran/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
                    "duration": 290,
                },
                {
                    "title": "Viva la Vida (Orchestral)",
                    "artist": "Vitamin String Quartet",
                    "artwork": "https://picsum.photos/seed/coldplay/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
                    "duration": 340,
                },
                {
                    "title": "Levitating (Synthwave Cover)",
                    "artist": "Synthwave Covers",
                    "artwork": "https://picsum.photos/seed/dualipa/400",
                    "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
                    "duration": 305,
                },
            ]
            for s in SONGS:
                db.add(models.Song(**s))
            db.commit()
            print(f"✅ {len(SONGS)} músicas inseridas na base de dados.")
        else:
            print("ℹ️ BD já contém músicas. Nada a fazer.")
    finally:
        db.close()


# Executa o seed ao arrancar
seed_if_empty()


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