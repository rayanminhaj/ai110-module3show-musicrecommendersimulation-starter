# 🎧 Model Card - VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

## 2. Intended Use

This system is designed to recommend 3 to 5 songs from a small catalog based on a user’s preferred genre, mood, and music-vibe features such as energy, valence, danceability, and acousticness. It is meant for classroom exploration and learning, not for real-world deployment.

The system assumes that a person’s music taste can be partly represented by a few features and that songs with similar attributes are more likely to match the user’s preferences.

## 3. How It Works

This recommender is a content-based system. It does not look at other users or use collaborative filtering. Instead, it compares one user profile against the features of every song in the dataset.

Each song includes:
- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness

The user profile stores:
- preferred genre
- preferred mood
- target energy
- target valence
- target danceability
- whether the user likes acoustic music
- a ranking mode

The model gives songs points for matching the user. A genre match adds a large bonus. A mood match also adds points. For numeric features like energy, valence, and danceability, the system rewards songs whose values are closer to the user’s target. It also adds either an acoustic or non-acoustic bonus depending on the user. After that, songs are sorted by score.

I also added two improvements:
1. **Multiple ranking modes** so the model can be genre-first, balanced, or energy-focused.
2. **A diversity penalty** so the final top results do not repeat the same artist or genre too much.

## 4. Data

The catalog contains **18 songs** in `data/songs.csv`.

The dataset includes genres such as:
- pop
- lofi
- rock
- ambient
- jazz
- synthwave
- indie pop
- electropop
- acoustic

The moods include:
- happy
- chill
- intense
- relaxed
- moody
- focused
- calm
- angry
- sad

I expanded the starter dataset to include more variety across genre, mood, and energy levels. Even so, the dataset is still very small and represents only a narrow slice of musical taste.

## 5. Strengths

This recommender works well when the user has a fairly clear preference pattern. For example:

- high-energy pop listeners receive upbeat and danceable songs
- chill lofi listeners receive low-energy and acoustic tracks
- intense rock listeners receive high-energy songs with stronger genre alignment

One strength of the system is transparency. Because the scoring is rule-based, it is easy to explain why a song appeared in the results. That makes the recommender more understandable than a black-box model.

## 6. Limitations and Bias

This system has several important limitations.

First, the catalog is tiny, so the recommendations are heavily limited by what songs are available. If there are only a few rock or acoustic songs, users with those preferences will get weaker variety.

Second, the model only looks at structured features. It does not know anything about lyrics, language, artist popularity, culture, nostalgia, or personal memories, even though those matter a lot in real music taste.

Third, the scoring system may still create a filter bubble. Even with a diversity penalty, a strong genre preference can dominate the rankings. That means the model may keep giving very similar songs instead of occasionally surfacing a surprising but good match.

Fourth, the dataset itself may be biased. If more upbeat songs are included than sad or experimental songs, users with those less represented tastes will not be served equally well.

If a system like this were used in a real product, it could unfairly favor certain genres, artists, or listening styles simply because of how the data and weights were chosen.

## 7. Evaluation

I evaluated the recommender using multiple user profiles:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Edge Case / Conflicting Taste

I checked whether the top recommendations matched what I would expect from the profile. I also compared how the outputs changed when I used different ranking modes.

The results mostly matched intuition for clear profiles. The Chill Lofi profile moved low-energy and acoustic songs upward, while the Deep Intense Rock profile pushed high-energy rock tracks to the top. The most surprising behavior came from the conflicting profile. Because the profile combined lofi, sadness, high energy, and acoustic preference, the system returned partial matches rather than something that truly felt correct. That showed me that simple recommenders can break down when user intent is complex.

I also used tests from `tests/test_recommender.py` to verify that:
- recommended songs are sorted sensibly
- explanation strings are not empty

## 8. Future Work

If I continued this project, I would improve it in these ways:

1. Add more song features, such as popularity, release decade, or detailed mood tags.
2. Increase dataset size so the system can serve more user tastes fairly.
3. Improve diversity logic so the system actively balances novelty, genre variety, and artist variety.
4. Add support for multiple users or playlist-level recommendations.
5. Make the explanations more human-friendly, such as “recommended because it matches your chill low-energy vibe.”

## 9. Personal Reflection

The biggest thing I learned is that recommendation systems are really about turning human taste into numbers. Even a simple scoring rule can feel like intelligence when the chosen features match what a person cares about.

What surprised me most was how quickly bias appears. A tiny dataset and a strong weight on one feature can completely change what rises to the top. This project made me think more critically about real music apps. Even when they feel personalized, they still depend on feature choices, data coverage, and ranking decisions made by people.