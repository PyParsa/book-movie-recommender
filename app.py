# app.py   (یا همان فایل قبلی‌ات)
import streamlit as st
import json, random

st.set_page_config(page_title="Book & Movie Recommender", page_icon="🎬", layout="centered")

# --- Theme state ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# --- THEME COLORS ---
def theme():
    if st.session_state.dark_mode:
        return {"bg":"#1E1E26","card":"#2E2E36","text":"#F2E9E4","border":"#9A8C98"}
    return {"bg":"#F2E9E4","card":"#FFFFFF","text":"#22223B","border":"#4A4E69"}

C = theme()

# --- CSS ---
st.markdown(f"""
<style>
  .main {{ background:{C['bg']}; color:{C['text']}; font-family: 'Inter', sans-serif; }}
  .stButton>button {{ background:#4A4E69; color:white; border:none; border-radius:10px; padding:10px 18px; font-weight:600; }}
  .stButton>button:hover {{ background:#9A8C98; color:{C['bg']}; }}
  .card {{
    background:{C['card']}; color:{C['text']}; border:2px solid {C['border']};
    border-radius:12px; padding:12px; margin-top:10px; text-align:center; font-weight:600;
    transition:all .25s ease;
  }}
  .card:hover {{ transform:scale(1.02); background:{("#38384B" if st.session_state.dark_mode else "#E9E4EF")}; }}
</style>
""", unsafe_allow_html=True)

# --- HEADER + TOGGLE ---
c1, c2 = st.columns([6,1])
with c1:
    st.title("🎬 Book & Movie Recommender")
    st.caption("Find something new to watch or read 🎲")
with c2:
    if st.button("🌙" if st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode

# --- LOAD DATA (from generator.py outputs) ---
@st.cache_data
def load_data():
    with open("synthetic_movies.json","r",encoding="utf-8") as fm:
        movies = json.load(fm)
    with open("synthetic_books.json","r",encoding="utf-8") as fb:
        books = json.load(fb)
    return {"movies": movies, "books": books}

data = load_data()

# --- INPUTS ---
choice = st.radio("What do you feel like exploring?", ["🎥 Movies", "📚 Books"], horizontal=True)
category = "movies" if "Movies" in choice else "books"

genres = list(data[category].keys())
genre = st.selectbox(f"Select a {category[:-1]} genre:", genres)

# Year range (1930–2025)
year_min, year_max = st.slider("Filter by year range:", 1930, 2025, (1990, 2020))
# Optional month filter (Any → 1..12)
month = st.selectbox("Filter by month (optional):", ["Any"] + list(range(1,13)))

# --- ACTION ---
if st.button("🎲 Recommend Me!"):
    items = data[category][genre]

    # فیلتر سال/ماه
    filtered = [
        it for it in items
        if year_min <= it["year"] <= year_max and (month == "Any" or it["month"] == month)
    ]

    if not filtered:
        st.warning("No items match your filters — showing similar picks.")
        filtered = items

    # تعداد خروجی: تا 5 مورد
    k = min(5, len(filtered))
    recs = random.sample(filtered, k=k)

    st.success(f"✨ {choice.strip()} suggestions in {genre} ({year_min}-{year_max}" +
               ("" if month == "Any" else f", month {month}") + "):")
    for it in recs:
        title, y, m, rating, length = it["title"], it["year"], it["month"], it["rating"], it["meta"]["length"]
        extra = f"{'min' if category=='movies' else 'pages'}"
        st.markdown(f"<div class='card'>{title} &nbsp;({y}/{m:02d}) • ⭐ {rating} • {length} {extra}</div>",
                    unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{C['border']}; font-size:14px;'>Designed by Parsa | UX + Python + Streamlit 💜</p>",
    unsafe_allow_html=True
)
