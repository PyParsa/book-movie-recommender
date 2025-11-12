import streamlit as st
import random

# ----------- DATASET WITH YEARS -----------
data = {
    "movies": {
        "Action": [
            ("John Wick", 2014), ("Mad Max: Fury Road", 2015), ("Die Hard", 1988), ("Gladiator", 2000),
            ("Mission Impossible", 1996), ("The Dark Knight", 2008),
            ("The Terminator", 1984), ("Lethal Weapon", 1987), ("Speed", 1994), ("Edge of Tomorrow", 2014)
        ],
        "Comedy": [
            ("The Mask", 1994), ("Superbad", 2007), ("The Hangover", 2009), ("Step Brothers", 2008),
            ("Home Alone", 1990), ("Ted", 2012), ("21 Jump Street", 2012), ("Crazy Rich Asians", 2018)
        ],
        "Drama": [
            ("The Shawshank Redemption", 1994), ("Forrest Gump", 1994), ("The Green Mile", 1999),
            ("Fight Club", 1999), ("A Beautiful Mind", 2001), ("The Pursuit of Happyness", 2006),
            ("The Godfather", 1972), ("Good Will Hunting", 1997)
        ],
        "Sci-Fi": [
            ("Interstellar", 2014), ("Inception", 2010), ("The Matrix", 1999),
            ("Blade Runner 2049", 2017), ("Arrival", 2016), ("Ex Machina", 2014),
            ("Star Wars: A New Hope", 1977), ("The Empire Strikes Back", 1980)
        ],
        "Thriller": [
            ("Se7en", 1995), ("Gone Girl", 2014), ("Shutter Island", 2010),
            ("Parasite", 2019), ("Prisoners", 2013), ("Zodiac", 2007),
            ("Psycho", 1960), ("The Silence of the Lambs", 1991)
        ]
    },
    "books": {
        "Fantasy": [
            ("Harry Potter", 1997), ("The Hobbit", 1937), ("Percy Jackson", 2005),
            ("Game of Thrones", 1996), ("The Name of the Wind", 2007), ("Mistborn", 2006)
        ],
        "Mystery": [
            ("Sherlock Holmes", 1892), ("Gone Girl", 2012), ("The Girl with the Dragon Tattoo", 2005),
            ("Big Little Lies", 2014), ("And Then There Were None", 1939), ("In the Woods", 2007)
        ],
        "Romance": [
            ("Pride and Prejudice", 1813), ("Me Before You", 2012), ("The Notebook", 1996),
            ("Twilight", 2005), ("Outlander", 1991), ("The Time Traveler’s Wife", 2003)
        ],
        "Self-Help": [
            ("Atomic Habits", 2018), ("Deep Work", 2016),
            ("The 7 Habits of Highly Effective People", 1989),
            ("Think and Grow Rich", 1937), ("The Power of Now", 1997), ("Can’t Hurt Me", 2018)
        ],
        "Sci-Fi": [
            ("Dune", 1965), ("Neuromancer", 1984), ("Ender’s Game", 1985),
            ("Ready Player One", 2011), ("The Martian", 2014), ("Snow Crash", 1992)
        ]
    }
}

# ----------- CONFIG -----------
st.set_page_config(page_title="Book & Movie Recommender", page_icon="🎬", layout="centered")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Theme toggle
col1, col2 = st.columns([6, 1])
with col1:
    st.title("🎬 Book & Movie Recommender")
    st.caption("Find something new to watch or read 🎲")
with col2:
    if st.button("🌙" if st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode

# Theme colors
if st.session_state.dark_mode:
    bg_color = "#1E1E26"
    card_color = "#2E2E36"
    text_color = "#F2E9E4"
    box_border = "#9A8C98"
else:
    bg_color = "#F2E9E4"
    card_color = "#FFFFFF"
    text_color = "#22223B"
    box_border = "#4A4E69"

# Custom CSS
st.markdown(f"""
    <style>
        .main {{
            background-color: {bg_color};
            color: {text_color};
            font-family: 'Inter', sans-serif;
        }}
        .stButton>button {{
            background-color: #4A4E69;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            background-color: #9A8C98;
            color: {bg_color};
        }}
        .recommend-box {{
            background-color: {card_color};
            color: {text_color};
            border: 2px solid {box_border};
            border-radius: 12px;
            padding: 12px;
            margin-top: 10px;
            text-align: center;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .recommend-box:hover {{
            transform: scale(1.02);
            background-color: {("#38384B" if st.session_state.dark_mode else "#E9E4EF")};
        }}
    </style>
""", unsafe_allow_html=True)

# ----------- USER INPUTS -----------
choice = st.radio("What do you feel like exploring?", ["🎥 Movies", "📚 Books"], horizontal=True)

# Dynamic genre list
category = "movies" if "Movies" in choice else "books"
genres = list(data[category].keys())
genre = st.selectbox(f"Select a {category[:-1]} genre:", genres)

# Year filter – limited to realistic range
year_input = st.number_input("Filter by year (optional):", min_value=1930, max_value=2025, step=1)

# ----------- LOGIC -----------
if st.button("🎲 Recommend Me!"):
    items = data[category][genre]
    filtered = [(title, year) for title, year in items if year == year_input]
    if year_input and filtered:
        recs = random.sample(filtered, k=min(2, len(filtered)))
        st.success(f"✨ {choice.strip()} suggestions from {year_input}:")
    elif year_input and not filtered:
        recs = random.sample(items, k=2)
        st.warning(f"No {category[:-1]}s found from {year_input}. Showing similar ones.")
    else:
        recs = random.sample(items, k=2)
        st.success(f"✨ {choice.strip()} suggestions in {genre} (any year):")

    for r, y in recs:
        st.markdown(f"<div class='recommend-box'>{r} ({y})</div>", unsafe_allow_html=True)

# ----------- FOOTER -----------
st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{box_border}; font-size:14px;'>Designed by Parsa | UX + Python + Streamlit 💜</p>",
    unsafe_allow_html=True
)
