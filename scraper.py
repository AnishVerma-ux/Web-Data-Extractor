
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 5

OUTPUT_FILE = Path(__file__).parent / "sample_dataset.csv"


def extract_books():
    books = []
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}page-{page}.html"

        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Could not fetch page {page}: {error}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        book_cards = soup.select("article.product_pod")

        if not book_cards:
            print(f"No books found on page {page}.")
            continue

        for book in book_cards:
            title_element = book.select_one("h3 a")
            price_element = book.select_one(".price_color")
            availability_element = book.select_one(".availability")
            rating_element = book.select_one("p.star-rating")

            if not all([
                title_element,
                price_element,
                availability_element,
                rating_element
            ]):
                print(f"Skipped incomplete record on page {page}.")
                continue

            title = title_element.get("title", "").strip()
            price_text = price_element.get_text(strip=True)
            availability = availability_element.get_text(strip=True)
            rating_classes = rating_element.get("class", [])

            try:
                price = float(
                    price_text.replace("£", "").replace("Â", "")
                )
            except ValueError:
                print(f"Skipped invalid price for: {title}")
                continue

            rating = next(
                (item for item in rating_classes
                 if item in ["One", "Two", "Three", "Four", "Five"]),
                None
            )

            if not title or rating is None:
                print("Skipped record with invalid title or rating.")
                continue

            books.append({
                "Title": title,
                "Price_GBP": price,
                "Availability": availability,
                "Rating": rating
            })

        print(f"Page {page}: processed {len(book_cards)} books")

    session.close()

    df = pd.DataFrame(books)

    if df.empty:
        print("No data extracted. CSV was not updated.")
        return

    before = len(df)
    df = df.drop_duplicates(subset=["Title"])
    duplicates_removed = before - len(df)

    df["Price_GBP"] = pd.to_numeric(
        df["Price_GBP"], errors="coerce"
    )
    df = df.dropna(
        subset=["Title", "Price_GBP", "Availability", "Rating"]
    )

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\n--- Data Quality Report ---")
    print(f"Valid unique books: {len(df)}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Missing values remaining: {int(df.isna().sum().sum())}")
    print(f"Average price: £{df['Price_GBP'].mean():.2f}")
    print(f"CSV saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_books()
