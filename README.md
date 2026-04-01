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

## Scraping Approach — Nested Two-Level Strategy

The scraper uses a nested loop design rather than scraping everything from a single page level.

### Why nested scraping?

The catalogue listing pages (`/catalogue/page-{n}.html`) only show **partial information** for each book — a truncated title, price, and star rating. Critical fields like full title, UPC, tax, description, and availability are only available on each book's **individual detail page**. Scraping just the listing pages would give incomplete data, so visiting every book's detail page is necessary.

### How URL construction works

Instead of following full absolute URLs, the scraper extracts only the **relative `href`** from each book's `<h3><a>` tag on the listing page (e.g., `a-light-in-the-attic_1000/index.html`). It then constructs the absolute URL by prepending the known `base_url`:

```
base_url = "https://books.toscrape.com/catalogue/"
relative  = "a-light-in-the-attic_1000/index.html"       ← extracted from listing
absolute  = base_url + relative                            ← constructed
```

This works because every book detail page lives under `/catalogue/`, so the relative paths from the listing page map directly to full URLs when joined with the base. This avoids needing to parse or resolve complex URL structures — just a simple string concatenation produces the correct detail page URL every time.

### The flow

1. **Outer loop** — paginate through catalogue pages (`page-1.html`, `page-2.html`, ...) using the "next" button to know when to stop.
2. **Inner loop** — for each of the 20 books on a catalogue page, extract the relative link, construct the full URL, fetch the detail page, and pull all required fields from it.

This two-level approach keeps the listing page parsing minimal (just grab the link) while the detail page parsing handles the heavy lifting of extracting all nine fields.

## Pagination

Page numbers are not hardcoded. The scraper starts from page 1 and checks for a "next" button on each page. If the button exists, it moves to the next page. If not, scraping stops.

## Output Format

Data is saved as JSON in `books.json`.

## How to Run

```bash
pip install requests beautifulsoup4 lxml
python scrape.py
```
