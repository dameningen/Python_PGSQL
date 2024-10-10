'''
pip install elasticsearch
'''
import re
from elasticsearch import Elasticsearch
import random
from datetime import datetime, timedelta
import string

# Elasticsearchの接続設定
es = es = Elasticsearch("http://localhost:9200")

# Apacheログファイルのパス
log_file_path = 'test_input/apache_log.log'  # ここを実際のログファイルのパスに変更してください

# Apacheのアクセスログのパターン
log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<date>.+?)\] "(?P<request>.+?)" (?P<status>\d{3}) (?P<size>\d+|-)'

# サンプルのIPアドレスとHTTPメソッド
ip_addresses = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
http_methods = ['GET', 'POST', 'PUT', 'DELETE']
status_codes = [200, 404, 500]

def main():
    # ログファイルを読み込み、各行を解析してElasticsearchに登録
    with open(log_file_path) as log_file:
        for line in log_file:
            match = re.match(log_pattern, line)
            if match:
                log_entry = match.groupdict()
                # Elasticsearchにデータを登録
                es.index(index='apache_logs', document=log_entry)

    # 取得するインデックス名
    index_name = 'apache_logs'

    # データを取得するクエリを設定
    query = {
        "query": {
            "match_all": {}  # すべてのドキュメントを取得するクエリ
        }
    }

    # データを取得
    response = es.search(index=index_name, body=query)

    # 結果を表示
    for hit in response['hits']['hits']:
        print(hit['_source'])  # ドキュメントの内容を表示


    print("ログの登録が完了しました。")


# サンプルデータの生成
def generate_log_entry():
    ip = random.choice(ip_addresses)
    random_str = generate_random_string(10)
    method = random.choice(http_methods)
    path = f"/{random_str}/{random.randint(1, 100)}"
    status = random.choice(status_codes)
    timestamp = datetime.now() - timedelta(days=random.randint(0, 10))
    return f"{ip} - - [{timestamp.strftime('%d/%b/%Y:%H:%M:%S')} +0000] \"{method} {path} HTTP/1.1\" {status}"


def generate_random_string(length):
    # 使用する文字のセット（英字と数字）
    characters = string.ascii_letters + string.digits
    # ランダムな文字列を生成
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def write_random_log():
    # ログエントリの数と出力ファイルの指定
    num_entries = 100000  # 生成するログエントリの数
    output_file = 'test_input/apache_log.log'

    # サンプルログをファイルに出力
    with open(output_file, 'w') as file:
        for _ in range(num_entries):
            # num_entries行のサンプルログを生成
            file.write(generate_log_entry() + '\n')

if __name__ == '__main__':
    main()

