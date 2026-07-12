import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur,conn,schema,row):
    try:
        if schema == 'staging':

            video_id = "video_id"

            cur.execute(f"""INSERT INTO {schema}.{table} 
                        ("Video_ID","Video_title","Upload_date","Duration","Video_Views","Likes_Count","Comments_Count")
                        VALUES (%(video_id)s,%(video_title)s,
                        %(upload_date)s,%(duration)s,%(video_views)s,%(likes_count)s,%(comments_count)s)""",row)
        else:

            video_id = "Video_ID"
            
            cur.execute(f"""INSERT INTO {schema}.{table} 
                        ("Video_ID","Video_title","Upload_date","Duration","Video_Views","Likes_Count","Comments_Count")
                        VALUES (%(video_id)s,%(video_title)s,
                        %(upload_date)s,%(duration)s,%(video_views)s,%(likes_count)s,%(comments_count)s)""",row)

