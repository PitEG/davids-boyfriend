import re
import asyncio

import mpv
import pytube
import discord

from pytube import Playlist
from pytube import YouTube
from pytube import extract

from discord.player import AudioSource
from discord.ext import commands

# create bot
bot = commands.Bot(command_prefix='!david')

# create mpv player
m = mpv.Context()
m.set_option('vid','no')
m.initialize()

# playlist
playlist = []

class Song:
    def __init__(self, url, title, duration):
        self.url = url
        self.title = title
        self.duration = duration

    def __repr__(self):
        return f'{self.title} - {self.duration}s'

def add_song(url):
    yt = YouTube(url)
    playlist.append(Song(yt.watch_url, yt.title, yt.length))
    pass

def add_playlist(url):
    pl = Playlist(url)
    songs = pl.video_urls
    for s in songs:
        add_song(s)

def play():
    if len(playlist) < 1: return
    m.command('loadfile',playlist[0].url,'append-play',
            'o','test',
            'of','nut',
            'oac','pcm_s16le',
            )


# bot commands
@bot.command(name='add')
async def command_add(ctx, *args):
    print("COMMAND: !davidadd")
    print("arg: ", args[0])
    url = args[0]
    is_playlist = re.search('list',url)
    print("playlist: ", is_playlist)
    if is_playlist is None: # it's probably a video url
        add_song(url)
        pass
    else: # it's probably a playlist url
        add_playlist(url)
        pass 
    print(playlist)
    pass

@bot.command(name='play')
async def command_play(ctx):
    # join voice channel
    voice_channel = ctx.message.author.voice.channel
    voice_client = ctx.guild.voice_client
    if (not voice_client):
        print('joining voice chat')
        voice_client = await voice_channel.connect()
        print('joined voice chat')

    # stream audio with mpv
    play()
    pass

@bot.command(name='pause')
async def command_pause(ctx):
    # pause stream from mpv
    pass

@bot.command(name='next')
async def command_next(ctx):
    # remove the first thing in playlist
    # play next song
    pass

@bot.command(name='clear')
async def command_clear(ctx):
    # stop playing
    # clear playlist
    pass

@bot.command(name='leave')
async def command_leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

@bot.command(name='list')
async def command_list(ctx):
    def format_time(secs : int):
        return f'{secs//60}:{secs%60}';

    def check_valid_page(page_num):
        page_num -= 1
        first_entry = page_num * 10 # 10 entries per page
        if first_entry >= len(playlist):
            return False
        else:
            return True

    def create_page(page_num : Song):
        page_num -= 1
        first_entry = page_num * 10 # 10 entries per page
        entries = playlist[first_entry:first_entry+10]
        page = ""
        for e in entries:
            first_entry += 1
            page += f'{first_entry}. {e.title} | {format_time(e.duration)}s\n';
        return page

    curr_page = 1
    color = 0xff8888

    init_page = "no music atm" if not check_valid_page(1) else create_page(1)
    embed = discord.Embed(title="Title", description=f'{init_page}', color=color)
    message = await ctx.send(embed = embed)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    while True:
        try:
            reaction,user = await bot.wait_for("reaction_add", timeout=10)

            # check reaction
            if str(reaction.emoji) == "▶️":
                curr_page = curr_page+1 if check_valid_page(curr_page+1) else curr_page
            if str(reaction.emoji) == "◀️":
                curr_page = curr_page-1 if check_valid_page(curr_page-1) else curr_page

            # display appropriate page
            if check_valid_page(curr_page):
                embed = discord.Embed(title="Title", description=f'{create_page(curr_page)}', color=color)
                description = create_page(curr_page)
                embed = discord.Embed(title="Title", description=description, color=color)
                await message.edit(embed = embed)
            await message.remove_reaction(reaction, user)
            pass
        except asyncio.TimeoutError:
            await message.delete()
            print("list timed out and deleted")
            break

# read token
print('reading token...')
token_file = open('TOKEN.txt','r')
token = token_file.readline()
token_file.close()
print('token read!')

# start bot 
print('starting bot!')
bot.run(token)
