import re
import atexit
import pexpect
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, Response, make_response

jukebox = Flask("")

data_jukebox = {"id": [], "name": [], "link": []}

# VLC instance to play the videos
vlc = pexpect.spawn("vlc --intf=lua --no-video --vout=none")
vlc.expect(">")


@atexit.register
def fin():
    vlc.close()
    print("exiting")


def name_link_youtube(link):
    """getting the name of the youtube video from the twitter card"""

    headers = {
        "user_agent": (
            "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 "
            "(KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    yt_inf = requests.get(link, headers=headers)
    soup = BeautifulSoup(yt_inf.text, "lxml")
    return soup.find("head").find(attrs={"name": "twitter:title"})["content"]


def youtube_link_clean(link):
    """
    gets the id from the video url, deleting other parts
    (like playlist, time, etc). This function also makes sure that the
    url is valid
    """

    r = re.compile(r"watch\?v=+[a-zA-Z0-9_-]{11}").search(link)
    if r:
        return "https://www.youtube.com/" + r.group()
    else:
        r2 = re.compile(r"youtu.be\/+[a-zA-Z0-9_-]{11}").search(link)
        if r2:
            return "https://www.youtube.com/watch?v=" + r2.group().replace(
                "youtu.be/", ""
            )
        else:
            return None


@jukebox.route("/")
def index():
    """index controller"""
    return render_template(
        "index.html",
        data=zip(
            data_jukebox["id"],
            data_jukebox["name"],
            data_jukebox["link"]
        ),
    )


@jukebox.route("/addlink", methods=["POST"])
def addlink():
    """post controller of the addlink function"""
    link = youtube_link_clean(request.form["link"])
    if link:
        id_item = 1
        # if there was already videos in the list
        if len(data_jukebox["id"]) > 0:
            # the id of the video to be added will be equal
            # to the id of the last video plus one
            id_item = (
                data_jukebox["id"][-1] + 1
            )
        data_jukebox["id"].append(id_item)
        data_jukebox["name"].append(name_link_youtube(link))
        data_jukebox["link"].append(link)
        # sends this command to the vlc instance
        enqueue_command = "enqueue " + link
        vlc.sendline(enqueue_command)
        vlc.expect(">")
        return Response(status=200)
    else:
        return Response(status=400)


# the following functions sends commands to the vlc instance


@jukebox.route("/play")
def play():
    vlc.sendline("play")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/pause")
def pause():
    vlc.sendline("pause")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/stop")
def stop():
    vlc.sendline("stop")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/vol_more")
def vol_up():
    vlc.sendline("volup 1")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/vol_less")
def vol_down():
    vlc.sendline("voldown 1")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/next")
def next():
    vlc.sendline("next")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/prev")
def prev():
    vlc.sendline("prev")
    vlc.expect(">")
    return Response(status=200)


@jukebox.route("/time")
def get_time():
    """gets how much time has passed from the video"""
    vlc.sendline("get_time")
    vlc.expect(">")
    video_info = vlc.before.decode("utf-8", "ignore")
    video_time = video_info.partition("get_time")[-1].strip()
    response = make_response(video_time, 200)
    response.mime_type = "text/plain"
    return response


@jukebox.route("/title")
def get_title():
    """gets the title of the video"""
    vlc.sendline("get_title")
    vlc.expect(">")
    video_info = vlc.before.decode("utf-8", "ignore")
    video_title = video_info.partition("get_title")[-1].strip()
    response = make_response(video_title, 200)
    response.mime_type = "text/plain"
    return response


@jukebox.route("/length")
def get_length():
    """gets the length of the video"""
    vlc.sendline("get_length")
    vlc.expect(">")
    video_info = vlc.before.decode("utf-8", "ignore")
    video_length = video_info.partition("get_length")[-1].strip()
    response = make_response(video_length, 200)
    response.mime_type = "text/plain"
    return response


# starts the flask server
jukebox.run(host="0.0.0.0", port=8080)
