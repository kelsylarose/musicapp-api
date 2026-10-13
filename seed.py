from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)


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


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Song).count() > 0:
            print("BD já contém músicas. Nada a fazer.")
            return
        for s in SONGS:
            db.add(models.Song(**s))
        db.commit()
        print(f"✅ {len(SONGS)} músicas inseridas na base de dados.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()