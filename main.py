import csv
from core.scraper import WebScraper
from utils.config import Config
from utils.logger import Logger


def main():
    logger = Logger.setup_logger()
    config = Config.get_user_config()

    scraper = WebScraper(base_url=config["base_url"], delay=config["delay"])

    print("\nStarting scraping process...")
    products = scraper.scrape_all_pages(max_pages=config["max_pages"])

    with open(config["output_file"], "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Product Name",
                "Original Price",
                "Discounted Price",
                "Monthly Payment",
                "Product URL",
            ]
        )

        for product in products:
            writer.writerow(
                [
                    product.name,
                    product.original_price,
                    product.discounted_price,
                    product.monthly_payment,
                    product.url,
                ]
            )

    print(
        f"\nScraping complete! Saved {len(products)} products to {config['output_file']}"
    )


if __name__ == "__main__":
    main()
