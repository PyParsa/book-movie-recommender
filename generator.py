# generator.py
import json
from pathlib import Path
from random import randint, uniform

START_YEAR = 1930
END_YEAR = 2025

MOVIE_GENRES = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller"]
BOOK_GENRES  = ["Fantasy", "Mystery", "Romance", "Self-Help", "Sci-Fi"]

def generate_dataset(genres, media_label):
    """
    می‌سازد: dict[str, list[dict]]
    هر آیتم: {title, year, month, genre, rating, meta}
    """
    dataset = {g: [] for g in genres}
    for year in range(START_YEAR, END_YEAR + 1):
        for month in range(1, 13):              # 12 ماه
            for genre in genres:                # 5 ژانر
                for i in range(1, 6):          # 5 مورد در هر ماه/ژانر
                    title = f"{genre} {media_label} {year}-{month:02d} #{i}"
                    item = {
                        "title": title,
                        "year": year,
                        "month": month,
                        "genre": genre,
                        # مقادیر تزئینیِ واقعی‌نما:
                        "rating": round(uniform(5.5, 9.6), 1),
                        "meta": {
                            "id": f"{media_label[:1].upper()}-{year}{month:02d}-{genre[:2].upper()}-{i:02d}",
                            "length": randint(85, 170) if media_label == "Movie" else randint(180, 750)  # دقیقه/صفحه
                        }
                    }
                    dataset[genre].append(item)
    return dataset

def main():
    movies = generate_dataset(MOVIE_GENRES, "Movie")
    books  = generate_dataset(BOOK_GENRES,  "Book")

    out_dir = Path(".")
    (out_dir / "synthetic_movies.json").write_text(
        json.dumps(movies, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "synthetic_books.json").write_text(
        json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("✅ Done. Files written: synthetic_movies.json, synthetic_books.json")

if __name__ == "__main__":
    main()
