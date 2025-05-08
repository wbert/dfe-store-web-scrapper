class Config:
    @staticmethod
    def get_user_config():
        print("╔════════════════════════════════════╗")
        print("║      WEB SCRAPER CONFIGURATION     ║")
        print("╚════════════════════════════════════╝")

        base_url = input("Enter the first page URL: ").strip()
        output_file = (
            input("Enter output filename (default: products.csv): ").strip()
            or "products.csv"
        )
        delay = float(input("Enter delay between pages in seconds (default: 2): ") or 2)
        max_pages = input(
            "Enter maximum pages to scrape (leave empty for all): "
        ).strip()
        max_pages = int(max_pages) if max_pages else None

        return {
            "base_url": base_url,
            "output_file": f"data/{output_file}",
            "delay": delay,
            "max_pages": max_pages,
        }
