import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from typing import List
from .product import Product


class WebScraper:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, base_url: str, headers: dict = None, delay: float = 2):
        self.base_url = base_url
        self.headers = headers or self.DEFAULT_HEADERS
        self.delay = delay

    def get_total_pages(self) -> int:
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            page_links = soup.select("a.pagination-item-link")
            if not page_links:
                return 1

            page_numbers = []
            for link in page_links:
                try:
                    num = int(link["href"].split("/page/")[1].strip("/"))
                    page_numbers.append(num)
                except (IndexError, ValueError):
                    span = link.find("span", class_="pagination-item-span")
                    if span and span.text.isdigit():
                        page_numbers.append(int(span.text))

            return max(page_numbers) if page_numbers else 1
        except Exception as e:
            print(f"Error getting page count: {e}")
            return 1

    def scrape_product(self, product_element) -> Product:
        try:
            name = product_element.find("h3", class_="kw-details-title").get_text(
                strip=True
            )
            product = Product(name=name, url=product_element["href"])

            price_container = product_element.find("span", class_="price")
            if price_container:
                if price_container.find("del"):
                    product.original_price = price_container.find("del").get_text(
                        strip=True
                    )
                if price_container.find("span", class_="woocommerce-Price-amount"):
                    product.discounted_price = price_container.find(
                        "span", class_="woocommerce-Price-amount"
                    ).get_text(strip=True)
                if price_container.find("ins"):
                    product.monthly_payment = price_container.find("ins").get_text(
                        strip=True
                    )

            return product
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None

    def scrape_page(self, page_url: str) -> List[Product]:
        try:
            response = requests.get(page_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_elements = soup.find_all("a", class_="woocommerce-LoopProduct-link")
            return [
                self.scrape_product(p)
                for p in product_elements
                if self.scrape_product(p)
            ]
        except Exception as e:
            print(f"Error scraping page {page_url}: {e}")
            return []

    def scrape_all_pages(self, max_pages: int = None) -> List[Product]:
        total_pages = self.get_total_pages()
        if max_pages:
            total_pages = min(total_pages, max_pages)

        all_products = []
        for page in range(1, total_pages + 1):
            page_url = self.base_url.replace("/page/1/", f"/page/{page}/")
            print(f"Scraping page {page}/{total_pages}...")

            products = self.scrape_page(page_url)
            all_products.extend(products)

            if page < total_pages:
                time.sleep(self.delay)

        return all_products
