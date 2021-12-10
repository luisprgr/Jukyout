Jukyout
========================

Similar to the Jukeboxes in the 90s, allow users to create a shared playlist of songs from YouTube to be played in a Raspberry Pi using VLC

## Raspberry Pi Compatibility:

This project has been tested on the following Raspberry Pi Boards: 

* Raspberry Pi Zero W 1.1

## Requirements:

* VLC with the latest youtube.lua from their repository


```shell
sudo rm /usr/lib/arm-linux-gnueabihf/vlc/lua/playlist/youtube.luac

curl -LJO https://raw.github.com/videolan/vlc/master/share/lua/playlist/youtube.lua

sudo cp youtube.lua /usr/lib/arm-linux-gnueabihf/vlc/lua/playlist/youtube.luac 
```

* Flask

* BeautifulSoup

* Pexpect

* Requests

```shell
pip3 install flask beautifulsoup4 pexpect requests
```

## Use

The project is executed with: 

```shell
python3 jukebox.py
```
In the project folder