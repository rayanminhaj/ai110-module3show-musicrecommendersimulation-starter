"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendation_table(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    print("=" * 110)
    print(f"{profile_name}")
    print(f"Preferences: {user_prefs}")
    print("-" * 110)
    print(f"{'Title':<24} {'Artist':<18} {'Genre':<12} {'Mood':<10} {'Score':<8} Explanation")
    print("-" * 110)

    for song, score, explanation in recommendations:
        short_explanation = explanation[:55] + "..." if len(explanation) > 58 else explanation
        print(
            f"{song['title']:<24} {song['artist']:<18} {song['genre']:<12} "
            f"{song['mood']:<10} {score:<8.2f} {short_explanation}"
        )

    print("=" * 110)
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    profiles = {
        "Profile 1 - High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.85,
            "danceability": 0.85,
            "likes_acoustic": False,
            "mode": "balanced",
        },
        "Profile 2 - Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.60,
            "danceability": 0.55,
            "likes_acoustic": True,
            "mode": "genre_first",
        },
        "Profile 3 - Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.45,
            "danceability": 0.60,
            "likes_acoustic": False,
            "mode": "energy_focused",
        },
        "Profile 4 - Edge Case / Conflicting Taste": {
            "genre": "lofi",
            "mood": "sad",
            "energy": 0.90,
            "valence": 0.30,
            "danceability": 0.40,
            "likes_acoustic": True,
            "mode": "balanced",
        },
    }

    for profile_name, prefs in profiles.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendation_table(profile_name, prefs, recommendations)


if __name__ == "__main__":
    main()