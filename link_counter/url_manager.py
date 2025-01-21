import csv

class UrlManager:
    def __init__(self):
        self.url_rows = []
        self.search_links = []

    def load_urls_from_csv(self, csv_path: str) -> None:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.url_rows = [row for row in reader]

    def load_search_links_from_txt(self, txt_path: str) -> None:
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.search_links = [line.strip() for line in f if line.strip()]

    def get_url_rows(self) -> list:
        return self.url_rows

    def get_search_links(self) -> list:
        return self.search_links

    def save_results_to_csv(self, rows: list, output_path: str) -> None:
        if not rows:
            return
        fieldnames = list(rows[0].keys())
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)