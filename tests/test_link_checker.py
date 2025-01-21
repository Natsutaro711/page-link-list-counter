import pytest
from link_counter.link_checker_core import LinkChecker
from link_counter.config_loader import ConfigLoader

@pytest.fixture
def config():
    return ConfigLoader('tests/test_config.ini')

@pytest.fixture
def checker():
    return LinkChecker(
        request_interval=0.1,  # テスト用に短く
        timeout=5,
        user_agent='TestBot/1.0'
    )

def test_check_links_in_page_text_mode(checker):
    """テキストモードでの検索テスト"""
    url = "https://example.com"
    search_links = ["example", "test"]
    config = {
        'mode': 'text',
        'tags': {},
        'resolve_relative_urls': False,
        'use_selenium': False
    }

    # モックのHTMLコンテンツ
    checker._get_page_content = lambda u, c: (200, """
        <html>
            <body>
                <p>This is an example page</p>
                <p>Another test example</p>
            </body>
        </html>
    """)

    result = checker.check_links_in_page(url, search_links, config)
    assert result['example'] == 2
    assert result['test'] == 1

def test_check_links_in_page_tag_mode(checker):
    """タグ属性モードでの検索テスト"""
    url = "https://example.com"
    search_links = ["/page1.html", "/page2.html"]
    config = {
        'mode': 'tag_attr',
        'tags': {'a': 'href'},
        'resolve_relative_urls': False,
        'use_selenium': False
    }

    # モックのHTMLコンテンツ
    checker._get_page_content = lambda u, c: (200, """
        <html>
            <body>
                <a href="/page1.html">Link 1</a>
                <a href="/page2.html">Link 2</a>
                <a href="/page1.html">Link 3</a>
            </body>
        </html>
    """)

    result = checker.check_links_in_page(url, search_links, config)
    assert result['/page1.html'] == 2
    assert result['/page2.html'] == 1

def test_error_handling(checker):
    """エラーハンドリングのテスト"""
    url = "https://nonexistent.example.com"
    search_links = ["test"]
    config = {'mode': 'text'}

    # エラーを発生させるモック
    checker._get_page_content = lambda u, c: (404, "Not Found")

    result = checker.check_links_in_page(url, search_links, config)
    assert result['test'] == 0
    assert 'error' in result