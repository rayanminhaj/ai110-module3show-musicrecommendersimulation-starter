# Reflection

## What I Learned

The biggest learning moment for me was realizing that a recommender system does not magically “know” what people want. It only knows the data and rules that I give it. In this project, I had to decide what counted as taste: genre, mood, energy, valence, danceability, and acousticness. Once I chose those features, the recommendations became a direct result of those design choices.

I also learned that input data, user preferences, and ranking logic are three different things. The song data is the raw information. The user profile represents the target taste. The ranking logic is the bridge that turns those into predictions. That distinction helped me understand why recommendation systems can feel smart even when they are still pretty simple underneath.

## How AI Tools Helped

AI tools were useful for brainstorming scoring rules, improving structure, and thinking about experiments and bias. They helped me move faster when designing functions and writing explanations. At the same time, I had to double-check the logic because AI can suggest code that looks fine but does not fully match the rubric or the intended algorithm.

For example, it was important to verify that:
- scores were actually numeric
- explanations matched the score
- the top songs were truly sorted
- the code still passed the starter tests

## What Surprised Me

What surprised me most was that a simple weighted system can already feel like a real recommender. If the profile is clear, the output can look surprisingly believable. At the same time, the system becomes weak very quickly when the user preferences are conflicting or when the dataset is too small.

I also noticed how easy it is to create a filter bubble. If genre matters too much, the system keeps recommending the same kind of songs. That is why I added a small diversity penalty. It made the top results feel less repetitive and more fair.

## If I Extended This Project

If I had more time, I would expand the dataset a lot and add more realistic song features, such as popularity, decade, lyrical themes, or repeated listening behavior. I would also experiment with collaborative filtering so the recommender could use patterns from multiple users instead of relying only on content similarity.

Overall, this project made me think of recommender systems less as “magic AI” and more as a series of design decisions about data, weights, and tradeoffs.