import mpv
import asyncio

m = mpv.MPV(vid='no',o='david',of='nut',oac='pcm_s16le')

print('first play')
m.play('https://www.youtube.com/watch?v=F4_D07Y3oNk')
m.wait_for_playback()
@m.on_key_press('s')
def play():
    m.play('https://www.youtube.com/watch?v=F4_D07Y3oNk')
    m.wait_for_playback()

print('second play')
m.play('https://www.youtube.com/watch?v=F4_D07Y3oNk')
m.wait_for_playback()

