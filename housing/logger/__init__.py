import logging
from datetime import datetime
import os
from time import asctime

LOG_DIR = "housing_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

os.makedirs(LOG_DIR, exist_ok= True)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    filemode= "w",
    format='[%(asctime)s] %(filename)s:%(lineno)d - %(levelname)s -%(message)s',
    level= logging.INFO
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns

