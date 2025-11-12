import streamlit as st
import requests
import random
import os

# ========== Load API keys from Streamlit secrets ==========
TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
GOOGLE_BOOKS_API_KEY = st.secrets.get("GOOGLE_BOOKS_API_KEY", "")

# ========== Streamlit Page Setup ==========
st.set_page_config(page_title="Book & Movie Recommender", page_icon="🎬", layout="centered")

st.markdown(
    """
    <style>
    .recommend-box {
        background-color: #4a4e69;
        color: white;
        padding: 14px;
        margin-top: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ========== Header ==========
st.title("🎬📚 Book & Movie Recommender")
st.write("Get personalized movie and book suggestions — powered by UX + Python + Streamlit 💜")

# ========== User Selection ==========
choice = st.radio("What do you want recommendations for?", ["Movies", "Books"], horizontal=True)

# ========== MOVIES ==========
if choice == "Movies":
    st.subheader("🎞️ Movie Recommendations")

    genre = st.selectbox("Select a genre:", [
        "Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Sci-Fi", "Thriller", "Animation"
    ])

    min_year, max_year = st.slider("Select release year range:", 1930, 2025, (2000, 2025))

    if st.button("🎲 Recommend Movies"):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre}&language=en-US&sort_by=popularity.desc&primary_release_date.gte={min_year}-01-01&primary_release_date.lte={max_year}-12-31"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                movies = random.sample(data.get("results", []), k=min(5, len(data["results"])))
                st.success(f"🎬 Movie suggestions in {genre} ({min_year}-{max_year}):")
                for movie in movies:
                    name = movie.get("title", "Unknown Title")
                    year = movie.get("release_date", "Unknown Year")[:4]
                    rating = movie.get("vote_average", "N/A")
                    runtime = movie.get("runtime", "N/A")
                    st.markdown(f"<div class='recommend-box'>{name} ({year}) ⭐ {rating}</div>", unsafe_allow_html=True)
            else:
                st.error("❌ Error fetching movies. Please check your API key or try again later.")
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

# ========== BOOKS ==========
else:
    st.subheader("📚 Book Recommendations")

    genre = st.selectbox("Choose a genre:", [
        "Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Adventure", "Biography"
    ])
    count = st.slider("How many results?", 5, 20, 10)

    if st.button("🎲 Recommend Books"):
        st.write("Fetching books... please wait.")
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={count}&key={GOOGLE_BOOKS_API_KEY}"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                books = response.json().get("items", [])
                if books:
                    st.success(f"✨ Books in {genre}:")
                    for b in books:
                        title = b["volumeInfo"].get("title", "Unknown Title")
                        authors = ", ".join(b["volumeInfo"].get("authors", ["Unknown Author"]))
                        st.markdown(f"<div class='recommend-box'>{title} — {authors}</div>", unsafe_allow_html=True)
                else:
                    st.warning("No books found. Try another genre.")
            else:
                raise Exception("API returned error")
        except Exception:
            # ========== FALLBACK MODE ==========
            st.warning("⚠️ Google Books API unavailable — showing local suggestions instead.")

            fallback_books = {
                "Fantasy": ["Harry Potter", "The Hobbit", "Percy Jackson", "Game of Thrones", "Eragon"],
                "Science Fiction": ["Dune", "Neuromancer", "Snow Crash", "Ender's Game", "The Martian"],
                "Mystery": ["Sherlock Holmes", "Gone Girl", "The Girl with the Dragon Tattoo", "Big Little Lies", "In the Woods"],
                "Romance": ["Pride and Prejudice", "Me Before You", "The Notebook", "Outlander", "Twilight"],
                "Horror": ["It", "The Shining", "Dracula", "Frankenstein", "Bird Box"],
                "Adventure": ["Treasure Island", "The Lost World", "Life of Pi", "Around the World in 80 Days", "Jurassic Park"],
                "Biography": ["Steve Jobs", "Becoming", "Educated", "The Diary of a Young Girl", "Long Walk to Freedom"]
            }

            st.success(f"✨ Offline {genre} book suggestions:")
            for title in random.sample(fallback_books.get(genre, []), k=5):
                st.markdown(f"<div class='recommend-box'>{title}</div>", unsafe_allow_html=True)

# ========== Footer ==========
st.markdown("---")
st.markdown("<center>Designed by Parsa | UX + Python + Streamlit 💜</center>", unsafe_allow_html=True)
