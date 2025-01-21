# Link Counter

URLリスト内の各ページから、指定されたリンクの出現回数をカウントするツールです。タグの属性（href, srcなど）またはテキストとしての出現回数を検索できます。

## 機能

- 複数のURLに対して一括で検索
- 複数の検索対象リンクに対応
- 2つの検索モード
  - タグ属性検索（a:href, link:href, script:src, img:srcなど）
  - テキスト検索（ページ内の文字列として検索）
- 柔軟なURL解決
  - 相対パスの自動解決（設定可能）
  - URLパラメータを無視したマッチング
- 設定ファイルによる柔軟な設定
- CSV形式での結果出力

## インストール

必要なパッケージを一括インストール：

```bash
pip install -r requirements.txt
```

Seleniumを使用する場合は、以下の追加設定が必要です：

### Linux環境の場合
```bash
# 必要なパッケージのインストール
sudo apt-get update
sudo apt-get install -y unzip

# Google Chromeのインストール
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# ChromeDriverのインストール
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
wget -N "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION.0.6834.83/linux64/chromedriver-linux64.zip"
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```
### Windows環境の場合
1. [Google Chrome](https://www.google.com/chrome/)をインストール
2. Chromeのバージョンを確認（設定 > Chromeについて）
3. 対応する[ChromeDriver](https://sites.google.com/chromium.org/driver/)をダウンロード
4. ChromeDriverをPATHの通ったディレクトリに配置

## 使用方法

### 基本的な使い方

```bash
python main.py
```

### 入力ファイル形式

#### URLリスト（CSV）
```csv
url,name
https://example.com,Example Site
https://example.org,Another Site
```

#### 検索リンク（TXT）
```text
https://target1.com
https://target2.com
```

### 設定ファイル（config.ini）

```ini
[request]
interval = 1.0
max_retries = 3
timeout = 10

[connection]
user_agent = LinkCheckerBot/1.0

[files]
output_csv_file = results.csv
input_urls_file = test_urls.csv
input_links_file = test_links.txt

[search]
# 検索モード: tag_attr（タグ属性）または text（テキスト検索）
mode = tag_attr
# タグ属性モード時のみ使用。カンマ区切りで検索対象のタグを指定
tags = a:href,link:href,script:src,img:src
# 相対パスをURLに解決するか  あまりうまく機能していないのでfalseを推奨
resolve_relative_urls = false
```

### 出力形式（CSV）

```csv
url,name,count_https://target1.com,count_https://target2.com,error
https://example.com,Example Site,5,2,
https://example.org,Another Site,3,1,
```

### 出力結果について

**免責事項**: 本ツールの出力結果の正確性について、いかなる保証も行いません。
結果はあくまで参考値としてご利用ください。

- カウント結果は以下の要因により実際のページ内容と異なる場合があります：
  - JavaScriptによる動的なコンテンツ生成
  - ページのレンダリングタイミング
  - アクセス制限やレート制限
  - ネットワークの状態
- 対象ウェブサイトの利用規約やロボット規約を必ず確認し、遵守してください
- エラー時は該当URLのカウントが`error`と表示されます
- 詳細なエラー情報は`logs`ディレクトリ内のログファイルを参照してください

## エラーハンドリング

- ネットワークエラーや無効なURLの場合、errorカラムにエラーメッセージが記録されます
- タイムアウトや接続エラーの場合、該当URLの検索結果は0としてカウントされます

## 制限事項

- JavaScriptで動的に生成されるコンテンツは`use_selenium = true`の設定で取得可能
- リクエスト間隔（interval）を適切に設定し、対象サーバーに負荷をかけないよう注意してください

## ライセンス

MIT License
