# Books to Scrape — Web Scraper

A Python web scraper for [books.toscrape.com](https://books.toscrape.com/) that navigates through all pages, visits each book's detail page, extracts the required fields, and stores the results in JSON format.


## Folder Structure

```
proshore/
├── scrape.py            # Main scraper script
├── books.json           # Output JSON file with scraped book data
├── terminal_output.png  # Screenshot of scraper output
└── README.md
```

## Libraries Used

- **requests** — Sends HTTP requests to fetch catalogue and book detail pages.
- **beautifulsoup4** — Parses HTML and extracts book data using tags and CSS classes.
- **lxml** — Fast HTML parser backend for BeautifulSoup.
- **json** (built-in) — Writes the scraped data to `books.json`.
- **datetime** (built-in) — Adds the current date to each record.

## Pagination

Page numbers are not hardcoded. The scraper starts from page 1 and checks for a "next" button on each page. If the button exists, it moves to the next page. If not, scraping stops.

## Output Format

Data is saved as JSON in `books.json`.

## How to Run

```bash
pip install requests beautifulsoup4 lxml
python scrape.py
```
