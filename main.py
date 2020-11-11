import os

from discord import Client
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = Client()

bot = commands.Bot(command_prefix='!', case_insensitive=True)


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


def main():
    print('Connecting bot...')
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
