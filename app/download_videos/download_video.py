import pytube
from pytube import YouTube
from pytube.helpers import regex_search

import os
import datetime
import json
import sys

def video_id(url: str) -> str:
    """Extract the ``video_id`` from a YouTube url.

    This function supports the following patterns:

    - :samp:`https://youtube.com/watch?v={video_id}`
    - :samp:`https://youtube.com/embed/{video_id}`
    - :samp:`https://youtu.be/{video_id}`

    :param str url:
        A YouTube url containing a video id.
    :rtype: str
    :returns:
        YouTube video id.
    """
    return regex_search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url, group=1)

def get_video_id(video_url):
    yt = YouTube(video_url)
    return video_id(video_url), yt


def download_video(video_url):
    video_id, yt = get_video_id(video_url)

    # Try finding captions to test if video is valid
    caption = yt.captions['en'] or yt.captions.all()[0]
    caption_list = caption.generate_srt_captions().splitlines()

    if os.path.exists('./public/saves/' + video_id):
        return yt, video_id, {}

    video = yt.streams.filter(progressive=True) \
        .order_by('resolution') \
        .desc() \
        .first()

    # video_data = yt.player_config_args.get('player_response').get('videoDetails')
    video_title = yt.title
    video_author = yt.author
    video_length_in_seconds = yt.length
    video_length_formatted = str(datetime.timedelta(seconds=int(video_length_in_seconds)))

    newpath = './public/saves/' + video_id
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    video.download('./public/saves/' + video_id, 'temp')

    meta_data = {'video_id': video_id, 'video_title': video_title, \
                'video_author': video_author, 'video_length': video_length_formatted}

    output_file = 'meta_data.json'
    with open('./public/saves/' + video_id + '/' + output_file, 'w') as f:
        json.dump(meta_data, f)
    return yt, video_id, meta_data

