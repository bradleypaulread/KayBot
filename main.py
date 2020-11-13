import os
from random import choice
from random import randint
from typing import Dict
from urllib.parse import quote

import requests
from discord import Client
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
    await ctx.send('Success')


def get_random_video_id() -> str:
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

    video_ids = []
    while True:
        url = 'https://youtube.googleapis.com/youtube/v3/playlistItems' + make_request(reqs)
        response = requests.get(url=url).json()
        items = response['items']
        if not items:
            break
        video_ids += [vid['snippet']['resourceId']['videoId'] for vid in items]
        next_page = response['nextPageToken'] if 'nextPageToken' in response else ''
        if not next_page:
            break
        reqs['pageToken'] = next_page

    return choice(video_ids)


def get_random_time_secs(video_id: str) -> Duration:
    req = {
        'id': video_id,
        'part': 'contentDetails',
        'key': YOUTUBE_TOKEN,
    }

    video_details = requests.get(url='https://www.googleapis.com/youtube/v3/videos' + make_request(req)).json()
    time = parse_duration(video_details['items'][0]['contentDetails']['duration'])
    return randint(1, time.total_seconds())


def get_screenshot(time_secs: int, video_id: str):
    ...


def main():
    print(f'Connecting bot...')

    vid_id = get_random_video_id()
    time = get_random_time_secs(vid_id)

    screenshot = get_screenshot(time, vid_id)

    # bot.run(TOKEN)


if __name__ == '__main__':
    main()
