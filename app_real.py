# ==========================================================
# 🎬 Book & Movie Recommender App (Final Hybrid + Proxy)
# Designed by Parsa | UX + Python + Streamlit 💜
# ==========================================================

import os
import re
import random
import requests
import streamlit as st
from dotenv import load_dotenv

# ----------------------------------------------------------
# 🔐 LOAD ENVIRONMENT VARIABLES
# ----------------------------------------------------------
load_dotenv()
PROXY_URL = "https://recommender-proxy-production.up.railway.app"  # ← آدرس سرور Railway تو

# ----------------------------------------------------------
# ⚙️ STREAMLIT CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Real Book & Movie Recommender", page_icon="🎬", layout="centered")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def palette():
    if st.session_state.dark_mode:
        return {"bg":"#1E1E26","card":"#2E2E36","text":"#F2E9E4","border":"#9A8C98"}
    return {"bg":"#F2E9E4","card":"#FFFFFF","text":"#22223B","border":"#4A4E69"}

C = palette()

# ----------------------------------------------------------
# 🎨 CUSTOM CSS STYLING
# ----------------------------------------------------------
st.markdown(f"""
<style>
  .main {{
    background:{C['bg']};
    color:{C['text']};
    font-family: 'Inter', sans-serif;
  }}
  .stButton>button {{
    background:#4A4E69;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 18px;
    font-weight:600;
  }}
  .stButton>button:hover {{
    background:#9A8C98;
    color:{C['bg']};
  }}
  .card {{
    background:{C['card']};
    color:{C['text']};
    border:2px solid {C['border']};
    border-radius:12px;
    padding:12px;
    margin-top:10px;
    text-align:center;
    font-weight:600;
    transition:all .25s ease;
  }}
  .card:hover {{
    transform:scale(1.02);
    background:{("#38384B" if st.session_state.dark_mode else "#E9E4EF")};
  }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🧭 HEADER
# ----------------------------------------------------------
c1, c2 = st.columns([6,1])
with c1:
    st.title("🎬 Real Book & Movie Recommender")
    st.caption("Powered by TMDB & Google Books APIs via Proxy 🌍")
with c2:
    if st.button("🌙" if st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode

# ----------------------------------------------------------
# 🔧 HELPER FUNCTIONS
# ----------------------------------------------------------
@st.cache_data(ttl=60*60)
def get_tmdb_genres():
    """دریافت ژانر فیلم‌ها از طریق Proxy"""
    url = f"{PROXY_URL}/tmdb/discover"
    params = {"endpoint": "genre/movie/list", "language": "en-US"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    genres = data.get("genres", [])
    id_by_name = {g["name"]: g["id"] for g in genres}
    names_sorted = sorted(id_by_name.keys())
    return id_by_name, names_sorted


@st.cache_data(ttl=60*10)
def discover_movies(genre_id: int, year: int, page: int = 1):
    """کشف فیلم‌ها از طریق Proxy"""
    url = f"{PROXY_URL}/tmdb/discover"
    params = {
        "with_genres": genre_id,
        "primary_release_year": year,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": page,
        "include_adult": False,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])


def extract_year(s: str) -> int | None:
    if not s:
        return None
    m = re.match(r"(\d{4})", s)
    return int(m.group(1)) if m else None


@st.cache_data(ttl=60*10)
def search_books_by_subject(subject: str, year: int, max_results: int = 20):
    """جستجوی کتاب از طریق Proxy"""
    url = f"{PROXY_URL}/books/search"
    params = {
        "q": f"subject:{subject}",
        "maxResults": 40,
        "orderBy": "relevance",
        "printType": "books",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    items = r.json().get("items", [])
    results = []
    for it in items:
        info = it.get("volumeInfo", {})
        title = info.get("title") or "Unknown"
        published = extract_year(info.get("publishedDate", ""))
        if published is None or published == year:
            results.append({"title": title, "year": published or "N/A"})
        if len(results) >= max_results:
            break
    return results

# ----------------------------------------------------------
# 🧠 APP LOGIC
# ----------------------------------------------------------
category = st.radio("Choose category:", ["🎥 Movies", "📚 Books"], horizontal=True)
year = st.slider("Select release year:", 1930, 2025, 2020)

if category == "🎥 Movies":
    try:
        id_by_name, names = get_tmdb_genres()
        genre_name = st.selectbox("Movie genre:", names, index=names.index("Action") if "Action" in names else 0)
        top_n = st.selectbox("How many results?", [5, 10, 15], index=1)
        if st.button("🎲 Recommend Movies"):
            with st.spinner("Fetching from TMDB (via Proxy)..."):
                pool = []
                for page in (1, 2, 3):
                    pool += discover_movies(id_by_name[genre_name], year, page)
                if not pool:
                    st.warning("No movies found for this year/genre. Try another filter.")
                else:
                    picks = random.sample(pool, k=min(top_n, len(pool)))
                    st.success(f"{len(picks)} movies for {genre_name} ({year}):")
                    for m in picks:
                        title = m.get("title", "Untitled")
                        y = extract_year(m.get("release_date", "")) or year
                        rating = m.get("vote_average", 0)
                        st.markdown(f"<div class='card'>{title} ({y}) • ⭐ {rating}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error fetching from Proxy/TMDB: {e}")

# ----------------------------------------------------------
# 📚 BOOKS
# ----------------------------------------------------------
else:
    subject = st.selectbox("Book subject:",
        ["Fantasy", "Mystery", "Romance", "Self-Help", "Sci-Fi", "History", "Horror", "Biography"],
        index=0)
    top_n = st.selectbox("How many results?", [5, 10, 15], index=1)
    if st.button("🎲 Recommend Books"):
        with st.spinner("Fetching from Google Books (via Proxy)..."):
            try:
                results = search_books_by_subject(subject, year, max_results=40)
                if not results:
                    raise Exception("No API results")
            except Exception:
                st.warning("⚠️ API unavailable — showing fallback results instead.")
                fallback_books = {
                    "Fantasy": ["Harry Potter", "The Hobbit", "Eragon", "Percy Jackson", "Game of Thrones"],
                    "Mystery": ["Sherlock Holmes", "Gone Girl", "The Girl with the Dragon Tattoo", "Big Little Lies"],
                    "Romance": ["Pride and Prejudice", "The Notebook", "Me Before You", "Outlander"],
                    "Sci-Fi": ["Dune", "The Martian", "Neuromancer", "Snow Crash"],
                    "Horror": ["It", "The Shining", "Dracula", "Frankenstein"],
                    "Biography": ["Steve Jobs", "Becoming", "Educated", "Long Walk to Freedom"],
                }
                results = [{"title": t, "year": "N/A"} for t in fallback_books.get(subject, [])]
            picks = results[:top_n]
            st.success(f"{len(picks)} books for {subject} (around {year}):")
            for b in picks:
                st.markdown(f"<div class='card'>{b['title']} ({b['year']})</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🖤 FOOTER
# ----------------------------------------------------------
st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{C['border']}; font-size:14px;'>Designed by Parsa | UX + Python + Streamlit 💜</p>",
    unsafe_allow_html=True
)
