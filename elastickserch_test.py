'''
pip install elasticsearch
'''
import re
from elasticsearch import Elasticsearch

# Elasticsearchの接続設定
es = es = Elasticsearch("http://localhost:9200")

# Apacheログファイルのパス
log_file_path = 'test_input/access_log.log'  # ここを実際のログファイルのパスに変更してください

# Apacheのアクセスログのパターン
log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<date>.+?)\] "(?P<request>.+?)" (?P<status>\d{3}) (?P<size>\d+|-)'

def main():
    # ログファイルを読み込み、各行を解析してElasticsearchに登録
    with open(log_file_path) as log_file:
        for line in log_file:
            match = re.match(log_pattern, line)
            if match:
                log_entry = match.groupdict()
                # Elasticsearchにデータを登録
                es.index(index='apache_logs', document=log_entry)

    print("ログの登録が完了しました。")

if __name__ == '__main__':
    main()
