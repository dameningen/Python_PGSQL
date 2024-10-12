import pandas as pd
import logging
import traceback


# ロガーの取得
logger = logging.getLogger(__name__)

class OutputExcel:
    def __init__(self):
        logger.debug('OutputExcel')

    # Excelファイルを作成する関数
    def save_dataframe_to_excel(self, df, file_path):
        """DataFrameのデータをExcelファイルに出力する。

        Args:
            df (_type_): _description_
            file_path (_type_): _description_
        """        
        try:
            for index, row in df.iterrows():
                logger.debug('%s, %s, %s, %s, %s, %s, ', row['date'], row['all_comment'], row['mt_comment'], row['mt_comment_per'], row['ai_comment'], row['ai_comment_per'])
                logger.debug('======')

            df.to_excel(file_path, index=False, engine='openpyxl')
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f"Error saving to Excel: {e}")
