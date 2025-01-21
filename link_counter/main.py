import csv
from link_counter.config_loader import ConfigLoader
from link_counter.link_checker_core import LinkChecker
from link_counter.logger import setup_logger

def get_csv_headers(results):
    if not results:
        return ['url', 'name', 'error']
    return list(results[0].keys())

def main():
    logger = setup_logger()
    config = ConfigLoader()

    # URLリストの読み込み
    with open(config.input_urls_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        url_rows = list(reader)

    # 検索対象リンクの読み込み
    with open(config.input_links_file, 'r', encoding='utf-8') as f:
        search_links = [line.strip() for line in f if line.strip()]

    # リンクチェッカーの初期化と実行
    checker = LinkChecker(
        request_interval=config.request_interval,
        timeout=config.timeout,
        user_agent=config.user_agent
    )

    results = checker.run(url_rows, search_links, config.search_config)

    # 結果をCSVに出力
    with open(config.output_csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=get_csv_headers(results))
        writer.writeheader()
        writer.writerows(results)