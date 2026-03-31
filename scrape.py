from bs4 import BeautifulSoup
import requests
import json
from datetime import date


def scrape_books():
    base_url = "https://books.toscrape.com/catalogue/"
    books = []
    page = 1

    while True:
        url = f"{base_url}page-{page}.html"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "lxml")

        # each book on the current page
        for article in soup.find_all("article", class_="product_pod"):
            try:
                link = article.find("h3").find("a")["href"]
                abs_url = base_url + link  
            except Exception:
                continue

            # Book detail page
            inside_response = requests.get(abs_url)
            if inside_response.status_code != 200:
                continue
            inside_soup = BeautifulSoup(inside_response.text, "lxml")

            product = inside_soup.find("article", class_="product_page")
            if not product:
                continue

            # Required fields
            try:
                name = product.find("h1").text
            except Exception:
                name = None

            try:
                price = product.find("p", class_="price_color").text
            except Exception:
                price = None

            try:
                availability = product.find("p", class_="instock availability").text.strip()
            except Exception:
                availability = None

            try:
                rating = product.find("p", class_="star-rating")["class"][1]
            except Exception:
                rating = None

            try:
                description = product.find("div", id="product_description").find_next_sibling("p").text
            except Exception:
                description = None

            rows = product.find("table", class_="table table-striped").find_all("tr")
            try:
                upc = rows[0].find("td").text
            except Exception:
                upc = None

            try:
                tax = rows[4].find("td").text
            except Exception:
                tax = None

            book = {
                "name": name,
                "url": abs_url,
                "scrape_date": str(date.today()),
                "description": description,
                "price": price,
                "tax": tax,
                "availability": availability,
                "upc": upc,
                "rating": rating,
            }
            books.append(book)

        # next page 
        next_btn = soup.find("li", class_="next")
        if next_btn:
            page += 1
        else:
            break  # No more pages

        print(f"Page {page - 1} done — {len(books)} books so far")

    return books


if __name__ == "__main__":
    results = scrape_books()

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nScraped {len(results)} books → books.json")





        

