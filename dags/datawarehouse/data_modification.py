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

        conn.commit()
        logger.info(f"Inserted row with video_id: {row['video_id']} into {schema}.{table}")

    except Exception as e:
        logger.error(f"Error inserting row with video_id: {row['video_id']} into {schema}.{table}: {e}")
        conn.rollback()
        raise e 
    

def update_rows(cur,conn,schema,row):
    try:
        if schema == 'staging':

            video_id = "video_id"
            upload_date = "publishedAt"
            video_title = "title"
            video_views = "viewCount"
            likes_count = "likeCount"
            comments_count = "commentCount"
        else :
            video_id = "Video_ID"
            upload_date = "Upload_date"
            video_title = "Video_title"
            video_views = "Video_Views"
            likes_count = "Likes_Count"
            comments_count = "Comments_Count"

        cur.execute(f"""UPDATE {schema}.{table}
                        SET "Video_title" = %(video_title)s,
                            "Upload_date" = %(upload_date)s,
                            "Duration" = %(duration)s,
                            "Video_Views" = %(video_views)s,
                            "Likes_Count" = %(likes_count)s,
                            "Comments_Count" = %(comments_count)s
                        WHERE "Video_ID" = %(video_id)s and upload_date = %(upload_date)s
                    """,row
                    )
        conn.commit()

        logger.info(f"Updated row with video_id: {row['video_id']} in {schema}.{table}")

    except Exception as e:
            logger.error(f"Error updating row with video_id: {row['video_id']} in {schema}.{table}: {e}")
            conn.rollback()
            raise e
    
    def delete_rows(cur,conn,schema,row):
        try:
            ids_to_delete = f"""({','.join(f"'{id}'" for id in ids_to_delete)})"""

            cur.execute(f"""DELETE FROM {schema}.{table}
                            WHERE "Video_ID" IN {ids_to_delete}
                        """)
            conn.commit()
            logger.info(f"Deleted rows with video_ids: {ids_to_delete} from {schema}.{table}")

        except Exception as e:
            logger.error(f"Error deleting rows with video_ids: {ids_to_delete} from {schema}.{table}: {e}")
            conn.rollback()
            raise e           
        
                                           
                

        