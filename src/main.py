"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(
        f"\nUser profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("\nTop recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']}  ({song['genre']}/{song['mood']})")
        print(f"   Score: {score:.2f} / 5.00")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
