import logging
import os
from datetime import datetime

def setup_logger():
    # ログディレクトリの作成
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # ログファイル名に日時を含める
    log_file = os.path.join(log_dir, f'link_checker_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    # ロガーの設定
    logger = logging.getLogger('link_checker')
    logger.setLevel(logging.INFO)

    # ファイルハンドラ
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # フォーマッタ
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ハンドラの追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger