import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

def load_path():
    file_path = f"./data/yt_data_{date.today()}.json"

    try:
        logger.info("Processing file: YT_data{date.today()}")

        with open(file_path,'r',encoding='utf-8') as raw_data:
            data = json.load(raw_data)
            logger.info("File loaded successfully")
            
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid Json in the file: {file_path}")
        raise