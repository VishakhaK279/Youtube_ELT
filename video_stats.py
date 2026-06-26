import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'MrBeast'
maxResults = 50

def get_Playlist_id():

    try:
            url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

            response = requests.get(url)

            response.raise_for_status()

            #print(response)

            data = response.json()

            #print(json.dumps(data,indent=4))

            channle_items = data['items'][0]

            channel_playlistId = channle_items['contentDetails']['relatedPlaylists']['uploads']

            print(channel_playlistId)

            return channel_playlistId
    
    except requests.exceptions.RequestException as e:
          raise e


def get_video_ids(playlist_id):
    
    video_ids = []

    pageToken = None

    baseUrl = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}'

    try:
        while True:
            url = baseUrl
            if pageToken:
                url += f'&pageToken={pageToken}'

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data['items']:
                video_ids.append(item['contentDetails']['videoId'])

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e  


def extract_video_data(video_id):
    extracted_data = []

    def batch_list(video_lst, batch_size):
        for start in range(0, len(video_lst), batch_size):
            yield video_lst[start:start + batch_size]

    try:
        for batch in batch_list(video_id, 50):
            video_ids = ','.join(batch)

            url = (
                f'https://youtube.googleapis.com/youtube/v3/videos?'
                f'part=snippet,statistics&id={video_ids}&key={API_KEY}'
            )

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                content_details = item.get('contentDetails')
                duration = content_details.get('duration') if content_details else None
                statistics = item['statistics']

            video_data = {
                "video_id": video_id,
                "title":snippet['title'],
                "publishedAt": snippet['publishedAt'],
                "duration": duration,
                "viewCount": statistics.get('viewCount', None),
                "likeCount": statistics.get('likeCount', None),
                "commentCount": statistics.get('commentCount', None)
            }

            extracted_data.append(video_data)

        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e


if __name__=="__main__":
    playlist_id = get_Playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    print(json.dumps(video_data[:3], indent=2))

