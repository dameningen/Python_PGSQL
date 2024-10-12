"""
メール送信処理
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import logging.config


# ロガーの取得
logger = logging.getLogger(__name__)


class MailSend:
    """メール送信処理クラス"""

    def __init__(self, mail_config):
        self.server = mail_config["Mail"]["server"]
        self.port = mail_config["Mail"]["port"]
        self.user = mail_config["Mail"]["user"]
        self.password = mail_config["Mail"]["password"]
        self.from_addr = mail_config["Mail"]["from"]
        self.to_addr = mail_config["Mail"]["to"]

    # メールを送信する関数
    def send_email(self, subject, body, attachment_path):
        """メール送信処理

        Args:
            subject (str): _description_
            body (str): _description_
            attachment_path (str): _description_
        """
        # メールの設定
        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["To"] = self.to_addr
        msg["Subject"] = subject

        # メール本文
        msg.attach(MIMEText(body, "plain"))

        # 添付ファイルの設定
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f"attachment; filename={attachment_path}"
                )
                msg.attach(part)
        except Exception as e:
            logger.error("Error attaching file: %s", e)

        # メール送信
        # TODO 一旦コメントアウト
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.from_addr, self.password)
                server.sendmail(self.from_addr, self.to_addr, msg.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
