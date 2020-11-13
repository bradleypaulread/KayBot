import os
import subprocess
import tempfile
from random import choice
from random import randint
from typing import Dict
from urllib.parse import quote

import requests
from discord import Client
from discord import File
from discord.ext import commands
from dotenv import load_dotenv
from isodate import Duration
from isodate import parse_duration

KAY_ID = 'UCeKWgImK1RAD9IGjWZqxmIw'

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_TOKEN = os.getenv('YOUTUBE_TOKEN')

client = Client()

bot = commands.Bot(command_prefix='!', case_insensitive=True)


def make_request(query_args: Dict[str, str]) -> str:
    args = []
    for k, v in query_args.items():
        if isinstance(v, list):
            args.append(k + '=' + '&'.join([quote(_v) for _v in v]))
        else:
            args.append(k + '=' + quote(v))
    return "?" + '&'.join(args)


@bot.event
async def on_ready():
    print(f'{bot.user.name} connected!')


@bot.command(name='ping', help='Ping the bot.')
async def ping(ctx):
    upper = ctx.message.content[1::].isupper()
    msg = 'pong!'
    if upper:
        msg = msg.upper()
    await ctx.send(msg)


@bot.command(name='pic', help='Force KayBot to look at disgusting food and share pics of it.')
async def post_pic(ctx):
    title, vid_id = get_random_video()
    time = get_random_time_secs(vid_id)
    ts = secs_to_timestamp(time)

    with tempfile.TemporaryDirectory() as tmpdir:
        screenshot = get_screenshot(time, vid_id, str(tmpdir))
        image = File(screenshot)
        await ctx.send(f'`{title} ({ts})`', file=image)


def get_random_video() -> str:
    reqs = make_request({
        'part': 'contentDetails',
        'id': KAY_ID,
        'key': YOUTUBE_TOKEN,
    })

    url = 'https://youtube.googleapis.com/youtube/v3/channels' + reqs

    response = requests.get(url=url).json()
    details, = response['items']
    uploads_id = details['contentDetails']['relatedPlaylists']['uploads']

    reqs = {
        'part': ['snippet', 'contentDetails', 'status'],
        'playlistId': uploads_id,
        'key': YOUTUBE_TOKEN,
        'maxResults': '50',
        'pageToken': '',
    }

    videos = []
    while True:
        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems' + make_request(reqs)
        response = requests.get(url=url).json()
        items = response['items']
        if not items:
            break
        videos += [(vid['snippet']['title'], vid['snippet']['resourceId']['videoId']) for vid in items]
        next_page = response['nextPageToken'] if 'nextPageToken' in response else ''
        if not next_page:
            break
        reqs['pageToken'] = next_page

    return choice(videos)


def get_random_time_secs(video_id: str) -> Duration:
    req = {
        'id': video_id,
        'part': 'contentDetails',
        'key': YOUTUBE_TOKEN,
    }

    video_details = requests.get(url='https://www.googleapis.com/youtube/v3/videos' + make_request(req)).json()
    time = parse_duration(video_details['items'][0]['contentDetails']['duration'])
    return randint(1, time.total_seconds())


def secs_to_timestamp(total_secs: int) -> str:
    mins, secs = total_secs // 60, total_secs % 60

    if mins < 10:
        mins = "0" + str(mins)
    if secs < 10:
        secs = "0" + str(secs)

    return f'{mins}:{secs}'


def get_screenshot(time_secs: int, video_id: str, tmpdir: str) -> str:
    ts = secs_to_timestamp(time_secs)
    cmd1 = f'ffmpeg -ss "{ts}" -i'
    youtube_dl_cmd = f'$(youtube-dl -f 22 --get-url "https://www.youtube.com/watch?v={video_id}")'
    cmd2 = f'-vframes 1 -q:v 2 "{tmpdir}/out.png"'

    cmd = cmd1.split(' ')
    cmd.append(youtube_dl_cmd)
    cmd += cmd2.split(' ')
    subprocess.run(' '.join(cmd), shell=True)

    return f'{tmpdir}/out.png'


def main():
    print(f'Connecting bot...')
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
