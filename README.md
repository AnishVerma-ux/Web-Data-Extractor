# Web Data Extractor

A Python project that extracts book data from a practice website, validates records, and generates a CSV dataset.

## Features
- Extracts data from five pages.
- Collects titles, prices, availability, and ratings.
- Removes duplicate titles.
- Checks missing values.
- Generates a summary report.

## Technologies
- Python
- Requests
- BeautifulSoup4
- Pandas

## How to Run

Install dependencies:

    python -m pip install -r requirements.txt

Run the scraper:

    python scraper.py

Generate the summary:

    python analyze_data.py

## Data Source
https://books.toscrape.com/
