# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**: a simple music recommender that matches songs to your vibe.

---

## 2. Intended Use  

**Goal:** given one user's taste, suggest the 5 songs from a small catalog that fit it best, and explain why each one was picked.

**What it assumes about the user:**
- They can describe their taste with one favorite genre, one mood, a target energy level (0 to 1), and whether they like acoustic music.
- Their taste doesn't change. The system has no memory of past listening.

**Intended use:**
- Classroom exploration of how recommenders turn data into rankings.
- Experimenting with weights and seeing how the results change.

**Not intended for:**
- Real users or a real music app. The catalog is 18 made-up songs.
- Judging what music is "good". A high score only means the song matches the labels the user picked.
- Users whose taste spans several genres or moods. The system only accepts one of each.

---

## 3. How the Model Works  

VibeMatch gives every song in the catalog points, then shows the 5 songs with the most points.

**How a song earns points (5 points max):**
- **Same genre as the user wants:** +2 points. Genre counts most because it's the strongest sign of someone's taste.
- **Same mood:** +1 point.
- **Energy close to what the user wants:** up to +1.5 points. A perfect match gets all 1.5, and the further off the song is, the fewer points it gets. Being too intense loses points just like being too quiet does.
- **Acoustic sound that fits the user:** +0.5 points. Acoustic songs get it if the user likes acoustic music; electronic-sounding songs get it if they don't.

**Picking the winners:** sort all songs from most to fewest points and keep the top 5. If two songs tie, the one with closer energy wins.

Every recommendation comes with its reasons, like "genre match: pop (+2.0)", so you can see exactly where the points came from.

**Changes from the starter code:** the starter returned the first 5 songs in the file with no scoring. I added CSV loading, the scoring rules, the ranking, readable explanations, a test run with six user profiles, and case-insensitive matching for genre and mood.

---

## 4. Data  

- **Size:** 18 songs. The starter had 10, and I added 8 to cover more genres and moods.
- **Genres (15):** lofi (3 songs), pop (2), and one song each of rock, ambient, jazz, synthwave, indie pop, hip-hop, country, r&b, metal, classical, blues, edm and reggae.
- **Moods (14):** chill (3), happy (2), intense (2), and one song each of relaxed, moody, focused, confident, nostalgic, romantic, angry, melancholic, sad, energetic and uplifting.
- **Features per song:** genre, mood, energy, tempo, valence (how happy it sounds), danceability and acousticness. The numeric features are from 0 to 1, except tempo, which is in BPM.

**Limits:**
- Most genres and moods have only one song, so many users have only 1 or 2 exact matches.
- Energy, tempo, danceability and acousticness are closely linked in this data. Loud songs are almost always fast, danceable and electronic.
- There are no high-energy acoustic songs and very few sad or dark songs.
- The songs are made up, and the labels reflect one person's judgment.
- It has no lyrics, language, release year or artist popularity.

---

## 5. Strengths  

- **Users whose taste the catalog covers well.** The Chill Lofi profile got all three lofi songs first, then an ambient chill song, then a quiet jazz song, which is exactly what I'd pick by hand.
- **Opposite tastes get opposite lists.** The lofi fan and the rock fan had zero songs in common.
- **The best match always wins.** For every normal profile, the song that matched everything scored 4.96 or higher and ranked first.
- **Unknown genres still work.** A k-pop fan got no genre points but still received happy, mid-energy songs, because the mood and energy rules kept working.
- **Explanations are honest.** Each result lists exactly where its points came from, so it's easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

**Weakness: once the few genre and mood matches are used up, the system turns into an "energy-only" recommender.** Most genres and moods in the 18-song catalog appear only once, so a user usually matches 1–3 songs, and the rest of the top 5 is ranked almost entirely by how close each song's energy is to the target. In my "sad but high-energy" test, the system found the one blues/sad song and then filled the list with Storm Runner, Gym Hero and Bassline Fever. These are intense and upbeat, the opposite of sad, but they had the right energy. The same thing makes Gym Hero show up in 4 of my 6 test profiles, because its energy (0.93) is close to anyone who asks for high energy. Users with less common tastes, like sad, acoustic or k-pop listeners, get worse recommendations than pop, lofi or rock fans, simply because the catalog has fewer songs that fit them.

Other limitations:
- **Exact text matching:** "indie pop" gets no credit for being close to "pop". (Capitalization used to break matching too; that's now fixed, see Evaluation.)
- **Ignored features:** valence, tempo and danceability are not scored, so the system can't tell a calm happy song from a calm sad one.
- **Energy outweighs acousticness:** a user who likes acoustic music but wants high energy gets loud electronic songs, since energy is worth up to 1.5 points and acousticness only 0.5. The catalog also has no high-energy acoustic songs.

---

## 7. Evaluation  

### Profiles tested

The full terminal output for each profile is in the README's [Experiments](README.md#experiments-you-tried) section.

| Profile | genre / mood / energy / likes acoustic | Why I tested it |
|---|---|---|
| High-Energy Pop | pop / happy / 0.85 / no | Normal user, the default case |
| Chill Lofi | lofi / chill / 0.35 / yes | Normal user at the opposite end |
| Deep Intense Rock | rock / intense / 0.92 / no | Normal user with only one exact match in the catalog |
| Sad but High-Energy | blues / sad / 0.9 / yes | Edge case: the only blues/sad song is quiet, so the preferences conflict |
| Unknown Genre | k-pop / happy / 0.7 / no | Edge case: a genre that isn't in the catalog |
| Capitalized Input | Pop / Happy / 0.85 / no | Edge case: the same as High-Energy Pop, just capitalized |

### Did the results feel right?

For the three normal profiles, yes, especially at the top. Chill Lofi was the best: all three lofi songs first, then the ambient chill song, then a quiet jazz song. That is exactly the playlist I'd make by hand. The rock fan getting Storm Runner first also feels right.

### Why "Gym Hero" keeps showing up for Happy Pop fans

Gym Hero is labeled "pop", so it earns the biggest prize in the scoring, 2 points for matching the genre. It is also very high-energy (0.93), close to the 0.85 the user asked for, and not acoustic, so it collects almost every other point too. The only thing it misses is the mood: it's "intense", not "happy". But mood is worth only 1 point, half as much as genre, so Gym Hero (3.88) still beats Rooftop Lights (2.87). Rooftop Lights *is* happy, but it's labeled "indie pop", and the system treats "indie pop" as a completely different word from "pop". To a person, Rooftop Lights is the better fit for "happy pop". To the scoring rules, Gym Hero is "pop" and Rooftop Lights is not.

Sunrise City ranks first for that user because it is the only song that wins every category: pop (+2.0), happy (+1.0), energy 0.82 vs. a 0.85 target (+1.46) and non-acoustic (+0.5), for 4.96 out of 5.

### What surprised me

- **Capital letters break everything.** Typing "Pop" and "Happy" instead of "pop" and "happy" made every genre and mood match fail. Sunrise City's score fell from 4.96 to 1.96, and Storm Runner, a rock song, jumped to #2. A real app needs to lowercase input before comparing, so I fixed this after the evaluation. Matching now ignores case, and this profile gives the same results as High-Energy Pop.
- **An unknown genre is handled better than a typo.** The k-pop user still got happy songs first, because the mood match still worked. The capitalized user got no credit at all.
- **Doubling energy and halving genre barely changed anything.** In this catalog, pop and rock songs are also the high-energy ones, so the two weights push in the same direction. The rankings stayed almost identical, so the change made results different in score but not more accurate.
- **"Likes acoustic" can be completely overruled.** The sad, high-energy user said they like acoustic music, but 3 of their top 5 songs have acousticness of 0.10 or lower.

### Comparing profiles, pair by pair

These comparisons are from the first run, before the capitalization fix.

- **High-Energy Pop vs. Chill Lofi:** no songs in common. Pop gets loud, non-acoustic songs; lofi gets quiet, acoustic ones. This makes sense: the two profiles disagree on every feature.
- **High-Energy Pop vs. Deep Intense Rock:** they share Gym Hero, Storm Runner and Sunrise City. Both want high energy and no acoustics, so they draw from the same group of loud songs. Only the genre and mood bonuses decide which one is first. Gym Hero lands on both lists because it's pop (good for the pop fan) and intense (good for the rock fan).
- **High-Energy Pop vs. Sad but High-Energy:** after the sad user's one blues song, their list looks like the pop fan's list (Storm Runner, Gym Hero). With nothing else sad in the catalog, energy takes over, so a sad listener ends up with the same loud songs as a happy one. It makes sense mathematically but not musically.
- **High-Energy Pop vs. Unknown Genre (k-pop):** both get the two "happy" songs on top, but for k-pop, Rooftop Lights beats Sunrise City because its energy (0.76) is closer to the 0.7 target. This shows the genre bonus is the only reason Sunrise City wins for the pop fan.
- **High-Energy Pop vs. Capitalized Input:** they asked for the same thing, but the capitalized version lost all genre and mood points, so the list is ordered by energy alone and Storm Runner (rock) moves up to #2. This wasn't valid output; it was a bug in how text was compared, which is now fixed.
- **Chill Lofi vs. Deep Intense Rock:** completely opposite lists, which is the right result for opposite tastes. Energy and acousticness push them to opposite ends of the catalog.
- **Chill Lofi vs. Sad but High-Energy:** both said they like acoustic music. The lofi user's list is all acoustic, but the sad user's list (after #1) is mostly not. The lofi user's energy target agrees with their acoustic taste, while the sad user's target (0.9) fights it, and energy is worth three times as much.
- **Chill Lofi vs. Unknown Genre (k-pop):** no overlap. K-pop wants mid-high energy and no acoustics, which is the opposite of lofi, so this is expected.
- **Chill Lofi vs. Capitalized Input:** no overlap. Even with its genre and mood matches broken, the capitalized profile still wants high energy, so it never reaches the quiet songs. Energy alone keeps the two apart.
- **Deep Intense Rock vs. Sad but High-Energy:** after #1, the lists are nearly the same (Storm Runner, Gym Hero, Bassline Fever). Both ask for about 0.9 energy, and the sad user's mood matches nothing else, so they effectively get the rock fan's playlist.
- **Deep Intense Rock vs. Unknown Genre (k-pop):** the rock fan gets intense songs and the k-pop fan gets happy songs. With genre out of the picture for k-pop, mood is what separates them, and it works.
- **Deep Intense Rock vs. Capitalized Input:** the capitalized list (Sunrise City, Storm Runner, Concrete Verses, Gym Hero, Rooftop Lights) looks like a generic "loud songs" list, close to the bottom half of the rock list. This is what the system gives when nothing matches except energy.
- **Sad but High-Energy vs. Unknown Genre (k-pop):** both are users the catalog serves poorly. The sad user has one perfect match and then filler; the k-pop user has no genre match but two good mood matches. Neither scores above 4.22, while every normal profile's top song scores 4.96 or higher.
- **Sad but High-Energy vs. Capitalized Input:** both show the "energy-only" fallback. Once nothing else matches, the same high-energy songs (Storm Runner, Gym Hero) appear.
- **Unknown Genre (k-pop) vs. Capitalized Input:** the k-pop user still gets happy songs first because "happy" matched. The capitalized user typed "Happy" and got nothing. A genre the system has never heard of is handled better than a capital letter.

---

## 8. Future Work  

1. **Smarter text matching.** Capitalization is already handled. Next would be partial credit for related genres and moods (pop ≈ indie pop, rock ≈ metal, chill ≈ relaxed, sad ≈ melancholic).
2. **Score valence.** Let users choose a "happiness" level, so a sad listener stops getting upbeat rock just because the energy is right.
3. **Add variety to the top 5.** Limit it to one song per artist, and save a slot for a song outside the user's favorite genre so results aren't always the same.
4. **Allow more complex tastes.** Accept several favorite genres or moods with different weights, and grow the catalog so every genre has more than one song.

---

## 9. Personal Reflection  

**Biggest learning moment:** finding that the weights matter less than the data. I expected that doubling the energy weight and halving the genre weight would shuffle the rankings, but almost nothing moved. In this catalog, genre and energy point the same way, since pop and rock are also the loud songs. It showed me that a recommender is only as good as the variety in its catalog: with one sad song, no weight setting can build a good sad playlist.

**How AI tools helped, and when I double-checked:** the AI assistant helped me analyze the dataset, generate new songs, write the scoring code, and suggest edge-case profiles I wouldn't have thought of, like capitalized input, which turned out to reveal a real bug that I then fixed. But its work still needed checking. Running the program showed that the starter import in `main.py` broke with `python -m src.main`. A couple of its written claims were also slightly off and had to be corrected against the real numbers, like saying a genre match outweighs mood and energy combined (it's 2.0 vs. 2.5, so it doesn't). I learned to check claims against the actual terminal output instead of trusting the explanation.

**What surprised me:** how much four simple rules "feel" like a real recommendation. The Chill Lofi list looked like a playlist a person would make, and the reasons made it feel thoughtful. But the same rules confidently gave a sad listener upbeat gym music. The system has no idea what a song sounds like; it just adds up points. A real app might be making the same kinds of mistakes, just with better data hiding them.

**What I'd try next:** add a few simulated users with listening histories and try collaborative filtering ("people who liked this also liked…"), then compare it to this content-based version, especially for new songs nobody has played yet.
