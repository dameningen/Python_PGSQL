from sqlalchemy import create_engine, text
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import re

# PostgreSQL データベースの接続設定
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'dvdrental'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# メール送信設定
SMTP_SERVER = 'smtp.aa'
SMTP_PORT = 587
SMTP_USER = 'a@a'
SMTP_PASSWORD = 'ppp'
FROM_EMAIL = 'a@a'
TO_EMAIL = 'a@a'

# SQL クエリを外部ファイルから読み込む
def load_query_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        query = file.read()
    query = re.sub('^--.*\\n', '', query)
    return query

# データベースからデータを抽出する関数
def fetch_data_from_postgresql(query):
    try:
        connection_string = (
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
        engine = create_engine(connection_string)
        # SQLクエリの実行
        with engine.connect() as connection:
            df = pd.read_sql(query, connection, params={'start_date_param':'2024-09-01', 'end_date_param':'2024-09-01'})
        connection.close()
        #df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Excelファイルを作成する関数
def save_dataframe_to_excel(df, file_path):
    try:
        for index, row in df.iterrows():
            print(index)
            print(row['date'], row['all_comment'], row['mt_comment'], row['mt_comment_per'], row['ai_comment'], row['ai_comment_per'])
            print('======')
        
        df.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as e:
        print(f"Error saving to Excel: {e}")

# メールを送信する関数
def send_email(subject, body, to_email, attachment_path):

    # メールの設定
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    # メール本文
    msg.attach(MIMEText(body, 'plain'))

    # 添付ファイルの設定
    try:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching file: {e}")

    # メール送信
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, SMTP_PASSWORD)
            #server.sendmail(FROM_EMAIL, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    # SQLクエリ
    # query = 'SELECT * FROM comment'
    # 外部 SQL ファイルのパス
    query_file_path = 'query.sql'
    query = load_query_from_file(query_file_path)
    
    # データの取得
    df = fetch_data_from_postgresql(query)
    
    if df is not None:
        # Excelファイルのパス
        excel_file_path = 'data.xlsx'
        
        # データをExcelファイルに保存
        save_dataframe_to_excel(df, excel_file_path)
        print("Excelファイルを保存しました。")
        
        # メールの送信
        send_email(
            subject='Pythonでメール送信テスト',
            body='Excelファイルを添付して送信するテストだよ。',
            to_email=TO_EMAIL,
            attachment_path=excel_file_path
        )
