"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # Edge cases designed to trick the scoring logic
    "Conflicting: Sad but High-Energy": {"genre": "blues", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
    "Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
    "Capitalized Input (Pop/Happy)": {"genre": "Pop", "mood": "Happy", "energy": 0.85, "likes_acoustic": False},
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    print("=" * 60)
    print(f"Profile: {name}")
    print(
        f"genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 60)
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']}  ({song['genre']}/{song['mood']})")
        print(f"   Score: {score:.2f} / 5.00")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print()

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
