"""
PostgreSQL操作用の処理
"""

from sqlalchemy import create_engine, text
import pandas as pd
import os
import re
import logging
import logging.config
import json
import traceback
import configparser
from typing import List

# ロガーの取得
logger = logging.getLogger(__name__)


class PgsqlCli:
    """PostgreSQL操作用クラス"""

    def __init__(self, con_config):
        self.host = con_config["Database"]["host"]
        self.port = con_config["Database"]["port"]
        self.name = con_config["Database"]["name"]
        self.user = con_config["Database"]["user"]
        self.password = con_config["Database"]["password"]

    def get_query_from_file(self, file_path: str) -> str:
        """SQL クエリを外部ファイルから読み込み、返却する。
        Args:
            file_path (str): SQL定義ファイル

        Returns:
            str: SQLクエリ
        """
        with open(file_path, "r", encoding="utf-8") as file:
            line = file.read()
        query = re.sub("-- .*\\n", "", line)
        return query

    # データベースからデータを抽出する関数
    def fetch_data_from_postgresql(self, query: str):
        try:
            connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
            engine = create_engine(connection_string)
            # SQLクエリの実行
            with engine.connect() as connection:
                df = pd.read_sql(
                    query,
                    connection,
                    params={
                        "start_date_param": "2024-09-01",
                        "end_date_param": "2024-09-01",
                    },
                )
            connection.close()
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    # Excelファイルを作成する関数
    def save_dataframe_to_excel(self, df, file_path):
        try:
            for index, row in df.iterrows():
                print(index)
                print(
                    row["date"],
                    row["all_comment"],
                    row["mt_comment"],
                    row["mt_comment_per"],
                    row["ai_comment"],
                    row["ai_comment_per"],
                )
                # print(row['comment_id'])
                print("======")

            # logger.info('df.comment_id:%s', df.at[0,'comment_id'])
            df.to_excel(file_path, index=False, engine="openpyxl")
        except Exception as e:
            print(traceback.format_exc())
            print(f"Error saving to Excel: {e}")


# ログ設定の読み込み
def setup_logging(default_path="logging_config.json", default_level=logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == "__main__":
    #setup_logging()
    config = configparser.ConfigParser()
    config.read("config.ini")

    pgsql_cli = PgsqlCli(config)
    query = pgsql_cli.get_query_from_file("query.sql")
    df = pgsql_cli.fetch_data_from_postgresql(query)
    logger.info(f"df:{df}")
