from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_Playlist_id, get_video_ids, extract_video_data,save_to_json

#Define local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

# Define default arguments for the DAG
default_args={
    "owner": "airflow",
    "depends_on_past": False,   
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "vishakhakokate2@gmail.com",
    #"retries": 1,
    #"retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(minutes=60),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz),
    #"end_date": datetime(2026, 12, 31, tzinfo=local_tz),
}

with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="A DAG to extract YouTube video data and save it to a JSON file",
    schedule_interval="0 14 * * *",  # Run daily at 14:00
    catchup=False,  # Do not perform backfill
) as dag:

    playlist_id = get_Playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extracted_data)

    playlist_id >> video_ids >> extracted_data >> save_to_json_task



