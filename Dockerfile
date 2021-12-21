FROM debian:stretch-slim

RUN apt update && apt install --no-install-recommends -y python3 python3-pip python3-setuptools python3-wheel python3-lxml vlc-nox
RUN rm /usr/lib/arm-linux-gnueabi/vlc/lua/playlist/youtube.luac 

ADD https://raw.github.com/videolan/vlc/master/share/lua/playlist/youtube.lua /usr/lib/arm-linux-gnueabi/vlc/lua/playlist/youtube.luac

RUN chmod 644 /usr/lib/arm-linux-gnueabi/vlc/lua/playlist/youtube.luac
RUN useradd -m jukebox -G audio

USER jukebox

ENV PULSE_SERVER=unix:/home/jukebox/pulse/socket

COPY . /home/jukebox/jukebox-py/

WORKDIR /home/jukebox/jukebox-py/

RUN pip3 install -r requirements.txt

CMD python3 jukebox.py

EXPOSE 8080