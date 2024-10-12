"""
PostgreSQLからデータを取得して作成したExcelファイルをメール送信する
"""

import configparser
import json
import logging
import logging.config
import os
import traceback

import pandas as pd

from excel.gen_excel import OutputExcel
from mail.send_mail import MailSend
from pgsql.pgsql import PgsqlCli

# ロガーの取得
logger = logging.getLogger(__name__)


def setup_logging(default_path="conf/logging_config.json", default_level=logging.INFO):
    """ログ設定の読み込み

    Args:
        default_path (str, optional): _description_. Defaults to "logging_config.json".
        default_level (_type_, optional): _description_. Defaults to logging.INFO.
    """
    if os.path.exists(default_path):
        with open(default_path, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == "__main__":
    setup_logging()
    config = configparser.ConfigParser()
    config.read("conf/config.ini")

    # PostgreSQLからデータを取得する
    pgsql_cli = PgsqlCli(config)
    query = pgsql_cli.get_query_from_file("sql/query.sql")
    df = pgsql_cli.fetch_data_from_postgresql(query)
    logger.debug("df:%s", df)

    if df is not None:
        # 取得したデータをExcelファイルに出力する
        excel = OutputExcel()
        excel.save_dataframe_to_excel(df, "data/output/DF出力.xlsx")

        mail = MailSend(config)
        # メールの送信
        mail.send_email(
            subject="Pythonでメール送信テスト",
            body="Excelファイルを添付して送信するテストだよ。",
            attachment_path="data/output/DF出力.xlsx"
        )
