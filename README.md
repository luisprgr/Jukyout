Jukyout
========================

Similar to Jukeboxes in the 90s, allow users to create a shared playlist of songs from YouTube to be played in a Raspberry Pi using VLC

## Raspberry Pi Compatibility:

This project has been tested on the following Raspberry Pi Boards: 

* Raspberry Pi Zero W 1.1

## Manual Installation 

### Requirements:

* Flask

* Pexpect

* Requests

* Lxml

* BeautifulSoup

```shell
sudo apt install python3-lxml
pip3 install flask beautifulsoup4 pexpect requests
``` 

* VLC with the latest youtube.lua from their repository

```shell
sudo rm /usr/lib/arm-linux-gnueabihf/vlc/lua/playlist/youtube.luac

curl -LJO https://raw.github.com/videolan/vlc/master/share/lua/playlist/youtube.lua

sudo cp youtube.lua /usr/lib/arm-linux-gnueabihf/vlc/lua/playlist/youtube.luac 

sudo chmod 644 /usr/lib/arm-linux-gnueabihf/vlc/lua/playlist/youtube.luac
```

### Use

The project is executed with: 

```shell
python3 jukebox.py
```
In the project folder

## Installation with Docker

### Requirements 

- Expose the raspberry pi pulseaudio socket to the docker container in `/home/jukebox/pulse/socket`

### installation

```shell
docker run -p 8080:8080 -v /run/user/$UID/pulse/native:/home/jukebox/pulse/socket -d luisprgr/jukyout:latest
```

## License

Licensed under the [GPL-3.0 License](LICENSE) 