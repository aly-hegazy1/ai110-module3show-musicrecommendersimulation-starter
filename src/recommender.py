import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.5
ACOUSTIC_POINTS = 0.5

INT_FIELDS = {"id"}
FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for a UserProfile, best first."""
        by_id = {song.id: song for song in self.songs}
        song_dicts = [asdict(song) for song in self.songs]
        ranked = recommend_songs(profile_to_prefs(user), song_dicts, k)
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why a song fits a UserProfile."""
        score, reasons = score_song(profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dict used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in INT_FIELDS:
                row[field] = int(row[field])
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    # Reward closeness to the target energy, not higher or lower energy
    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = ENERGY_POINTS * (1 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})"
        )

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        acoustic = song["acousticness"]
        if likes_acoustic and acoustic >= 0.6:
            score += ACOUSTIC_POINTS
            reasons.append(f"acoustic sound ({acoustic:.2f}) (+{ACOUSTIC_POINTS:.1f})")
        elif not likes_acoustic and acoustic <= 0.4:
            score += ACOUSTIC_POINTS
            reasons.append(f"non-acoustic sound ({acoustic:.2f}) (+{ACOUSTIC_POINTS:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    target_energy = user_prefs.get("energy", 0.5)
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Highest score first; ties go to the song closest to the target energy
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy)),
    )
    return ranked[:k]
