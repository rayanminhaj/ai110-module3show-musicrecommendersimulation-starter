from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple


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
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "mode": "balanced",
        }

        song_dicts = [asdict(song) for song in self.songs]
        ranked = recommend_songs(user_prefs, song_dicts, k=k)

        results: List[Song] = []
        for song_dict, _, _ in ranked:
            results.append(Song(**song_dict))
        return results

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "mode": "balanced",
        }
        score, reasons = score_song(user_prefs, asdict(song))
        return f"{song.title} scored {score:.2f} because " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and converts numeric fields
    into numbers for scoring.
    """
    songs: List[Dict] = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs


def similarity_score(target: float, actual: float) -> float:
    """
    Returns a similarity score from 0.0 to 1.0,
    where closer values score higher.
    """
    return max(0.0, 1.0 - abs(target - actual))


def get_mode_weights(mode: str) -> Dict[str, float]:
    """
    Returns a set of weights for different ranking strategies.
    """
    if mode == "genre_first":
        return {
            "genre": 3.0,
            "mood": 1.5,
            "energy": 2.0,
            "valence": 1.0,
            "danceability": 0.5,
            "acousticness": 1.0,
        }

    if mode == "energy_focused":
        return {
            "genre": 1.5,
            "mood": 1.0,
            "energy": 3.5,
            "valence": 1.0,
            "danceability": 1.0,
            "acousticness": 1.0,
        }

    return {
        "genre": 2.5,
        "mood": 1.5,
        "energy": 2.5,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 1.0,
    }


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Returns:
        (score, reasons)
    """
    mode = user_prefs.get("mode", "balanced")
    weights = get_mode_weights(mode)

    score = 0.0
    reasons: List[str] = []

    preferred_genre = user_prefs.get("genre", "").lower()
    preferred_mood = user_prefs.get("mood", "").lower()

    if preferred_genre and song["genre"].lower() == preferred_genre:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if preferred_mood and song["mood"].lower() == preferred_mood:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    if "energy" in user_prefs:
        energy_points = similarity_score(user_prefs["energy"], song["energy"]) * weights["energy"]
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if "valence" in user_prefs:
        valence_points = similarity_score(user_prefs["valence"], song["valence"]) * weights["valence"]
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    if "danceability" in user_prefs:
        dance_points = similarity_score(
            user_prefs["danceability"], song["danceability"]
        ) * weights["danceability"]
        score += dance_points
        reasons.append(f"danceability similarity (+{dance_points:.2f})")

    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_points = song["acousticness"] * weights["acousticness"]
            score += acoustic_points
            reasons.append(f"acoustic bonus (+{acoustic_points:.2f})")
        else:
            acoustic_points = (1.0 - song["acousticness"]) * weights["acousticness"]
            score += acoustic_points
            reasons.append(f"non-acoustic bonus (+{acoustic_points:.2f})")

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Ranks songs by score and returns the top k.

    Includes a small diversity penalty so the final results
    do not over-repeat the same artist or genre.
    """
    scored_songs: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    scored_songs.sort(
        key=lambda item: (item[1], item[0]["danceability"], item[0]["valence"]),
        reverse=True,
    )

    selected: List[Tuple[Dict, float, List[str]]] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    for song, base_score, reasons in scored_songs:
        penalty = 0.0

        if artist_counts.get(song["artist"], 0) >= 1:
            penalty += 0.75

        if genre_counts.get(song["genre"], 0) >= 1:
            penalty += 0.25 * genre_counts[song["genre"]]

        final_score = round(base_score - penalty, 4)

        final_reasons = reasons[:]
        if penalty > 0:
            final_reasons.append(f"diversity penalty (-{penalty:.2f})")

        selected.append((song, final_score, final_reasons))
        selected.sort(key=lambda item: item[1], reverse=True)
        selected = selected[:k]

        artist_counts = {}
        genre_counts = {}
        for chosen_song, _, _ in selected:
            artist_counts[chosen_song["artist"]] = artist_counts.get(chosen_song["artist"], 0) + 1
            genre_counts[chosen_song["genre"]] = genre_counts.get(chosen_song["genre"], 0) + 1

    final_results: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in selected:
        explanation = ", ".join(reasons)
        final_results.append((song, score, explanation))

    return final_results