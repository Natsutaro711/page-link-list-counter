import configparser

class ConfigLoader:
    def __init__(self, config_path: str = 'config.ini'):
        self._config = configparser.ConfigParser()
        self._config.read(config_path, encoding='utf-8')

    @property
    def request_interval(self) -> float:
        return self._config.getfloat('request', 'interval', fallback=1.0)

    @property
    def max_retries(self) -> int:
        return self._config.getint('request', 'max_retries', fallback=3)

    @property
    def timeout(self) -> int:
        return self._config.getint('request', 'timeout', fallback=10)

    @property
    def user_agent(self) -> str:
        return self._config.get('connection', 'user_agent', fallback='LinkCheckerBot/1.0')

    @property
    def output_csv_file(self) -> str:
        return self._config.get('files', 'output_csv_file', fallback='results.csv')

    @property
    def input_urls_file(self) -> str:
        return self._config.get('files', 'input_urls_file', fallback='test_urls.csv')

    @property
    def input_links_file(self) -> str:
        return self._config.get('files', 'input_links_file', fallback='test_links.txt')

    @property
    def search_config(self) -> dict:
        mode = self._config.get('search', 'mode', fallback='tag_attr')
        tags_str = self._config.get('search', 'tags', fallback='a:href')
        resolve_relative = self._config.getboolean('search', 'resolve_relative_urls', fallback=True)
        use_selenium = self._config.getboolean('search', 'use_selenium', fallback=False)
        selenium_wait = self._config.getfloat('search', 'selenium_wait', fallback=3.0)

        # タグ設定の解析
        tags = {}
        if mode == 'tag_attr':
            for tag_pair in tags_str.split(','):
                tag, attr = tag_pair.strip().split(':')
                tags[tag] = attr

        return {
            'mode': mode,
            'tags': tags,
            'resolve_relative_urls': resolve_relative,
            'use_selenium': use_selenium,
            'selenium_wait': selenium_wait
        }