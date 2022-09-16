# david's boyfriend
david's boyfriend is a discord bot for playing music on discord servers

# setup
Depends on `python mpv`, `pytube`, `discordpy` and `PyNaCl`. To install the dependencies with `pip`, run:

`pip install python-mpv pytube discordpy PyNaCl`.

Also, it depends on ffmpeg and mpv so you need to install that with your package manager. For example:

on ubuntu
`apt-get ffmpeg mpv`

on arch
`pacman -S ffmpeg mpv`

Need to get a token from discord developer portal and place it in a single line file called TOKEN.txt from the same directory the python script was run in.

To enable that audio is streamed properly, make sure to run

`mkfifo david`

in the directory that the script is run in

