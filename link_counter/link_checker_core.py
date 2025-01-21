# link_checker/link_checker_core.py
import time
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urljoin
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger('link_checker')

class LinkChecker:
    def __init__(self, request_interval: float, timeout: int, user_agent: str):
        self.request_interval = request_interval
        self.timeout = timeout
        self.user_agent = user_agent
        self.session = self._init_session()
        self.driver = None

    def _init_session(self):
        s = requests.Session()
        s.headers.update({'User-Agent': self.user_agent})
        # リトライの設定やプロキシ設定を追加したいならここで
        return s

    def _init_selenium(self):
        """Seleniumドライバーの初期化"""
        if not self.driver:
            options = Options()
            options.add_argument('--headless')  # ヘッドレスモード
            options.add_argument('--no-sandbox')  # Linux環境で必要
            options.add_argument('--disable-dev-shm-usage')  # メモリ制限回避
            options.add_argument(f'user-agent={self.user_agent}')

            try:
                self.driver = webdriver.Chrome(options=options)
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {str(e)}")
                print("Please make sure Chrome and ChromeDriver are properly installed")
                raise

    def _get_page_content(self, url: str, search_config: dict) -> tuple:
        """通常のリクエストまたはSeleniumでページを取得"""
        try:
            if search_config.get('use_selenium', False):
                try:
                    if not self.driver:
                        self._init_selenium()

                    logger.info(f"Using Selenium to fetch: {url}")
                    self.driver.get(url)
                    # JavaScript実行待機
                    wait_time = search_config.get('selenium_wait', 3)
                    print(f"Waiting {wait_time} seconds for JavaScript...")
                    time.sleep(wait_time)

                    if self.driver.page_source:
                        return 200, self.driver.page_source
                    return 0, "Empty page source"
                except Exception as e:
                    logger.error(f"Selenium error for {url}: {str(e)}")
                    print("Falling back to regular request...")
                    # Seleniumが失敗した場合は通常のリクエストを試みる
                    resp = self.session.get(url, timeout=self.timeout)
                    return resp.status_code, resp.text
            else:
                resp = self.session.get(url, timeout=self.timeout)
                return resp.status_code, resp.text
        except Exception as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return 0, str(e)

    def check_links_in_page(self, url: str, search_links: list, search_config: dict = {
            'mode': 'tag_attr',
            'tags': {'a': 'href'},
            'resolve_relative_urls': True,
            'use_selenium': False,
            'selenium_wait': 3
        }) -> dict:
        print(f"\nChecking URL: {url}")
        self.search_config = search_config
        result = {}
        try:
            status_code, page_content = self._get_page_content(url, search_config)
            print(f"Status code: {status_code}")
            if status_code != 200:
                print(f"Error response for {url}")
                for link in search_links:
                    result[link] = 0
                result['error'] = f"Status Code: {status_code}"
                return result

            soup = BeautifulSoup(page_content, 'html.parser')

            if search_config['mode'] == 'tag_attr':
                print("Using tag attribute mode")
                # タグと属性による検索
                found_links = []
                for tag, attr in search_config['tags'].items():
                    elements = soup.find_all(tag)
                    found_links.extend([elem.get(attr) for elem in elements if elem.get(attr)])

                # URLからパラメータを除去し、必要に応じて相対パスを解決
                found_links = [self._normalize_url(link, url) for link in found_links if link]
                search_links_normalized = [self._normalize_url(link) for link in search_links]

                c = Counter(found_links)
                for link, normalized_link in zip(search_links, search_links_normalized):
                    result[link] = c[normalized_link]
            else:
                print("Using text search mode")
                # テキスト検索モード
                page_text = str(soup).lower()
                for link in search_links:
                    if link.startswith('/'):
                        # 相対パスの場合
                        base_link = self._normalize_url(link, url)
                        pattern = re.escape(base_link)
                    else:
                        # 通常のテキストまたはURL
                        pattern = re.escape(link.lower())
                    result[link] = len(re.findall(pattern, page_text))
                print(f"Page text length: {len(page_text)}")
                for link in search_links:
                    count = result[link]
                    print(f"Found {count} occurrences of '{link}'")

        except Exception as e:
            for link in search_links:
                result[link] = 0
            result['error'] = str(e)

        return result

    def _normalize_url(self, url: str, base_url: str = None) -> str:
        """URLからクエリパラメータを除去し、必要に応じて相対パスを解決"""
        if base_url and self.search_config.get('resolve_relative_urls', True):
            if not url.startswith(('http://', 'https://', '//')):
                url = urljoin(base_url, url)
        return url.split('?')[0].split('#')[0]

    def run(self, url_rows: list, search_links: list, search_config: dict = None) -> list:
        for row in url_rows:
            url = row.get('url')
            if not url:
                continue
            page_result = self.check_links_in_page(url, search_links, search_config)
            for link in search_links:
                if 'error' in page_result:
                    row[f'count_{link}'] = 'error'
                else:
                    row[f'count_{link}'] = page_result[link]
        return url_rows

    def __del__(self):
        """デストラクタでSeleniumドライバーを終了"""
        if self.driver:
            self.driver.quit()
