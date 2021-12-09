from flask import Flask, render_template, request, Response, make_response
from bs4 import BeautifulSoup
import pexpect
import requests
import atexit
import re

jukebox = Flask("")


data_jukebox = {"id": [], "name": [], "link": []}

vlc = pexpect.spawn("vlc")  
vlc.expect('>')

@atexit.register
def fin():
    vlc.close()
    print("exiting")

def name_link_youtube(link): 
    headers = {"user_agent":"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",}
    yt_inf = requests.get(link, headers=headers)
    soup = BeautifulSoup(yt_inf.text, 'lxml')
    return soup.find('head').find(attrs={"name":"twitter:title"})['content']
    
def youtube_link_clean(link):
    r = re.compile(r"watch\?v=+[a-zA-Z0-9_-]{11}").search(link)
    if r:
        return "https://www.youtube.com/" + r.group()
    else:
        r2 = re.compile(r"youtu.be\/+[a-zA-Z0-9_-]{11}").search(link)
        if r2:
            return "https://www.youtube.com/watch?v=" + r2.group().replace("youtu.be/","")
        else:
            return None


@jukebox.route("/")
def index():
    return render_template("index.html", data=zip(data_jukebox["id"],data_jukebox["name"],data_jukebox["link"]))

@jukebox.route("/addlink", methods=["POST"])
def addlink():
    link = youtube_link_clean(request.form["link"])
    if link:
        id_item = 1
        if len(data_jukebox['id']) > 0: 
            id_item = data_jukebox['id'][-1] + 1
        data_jukebox["id"].append(id_item)
        data_jukebox["name"].append(name_link_youtube(link))
        data_jukebox["link"].append(link)
        l = "enqueue " + link 
        vlc.sendline(l)
        vlc.expect('>')
        return Response(status=200)
    else:
        return Response(status=400) 

@jukebox.route("/play")
def play():
    vlc.sendline("play")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/pause")
def pause():
    vlc.sendline("pause")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/stop")
def stop():
    vlc.sendline("stop")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/vol_more")
def vol_up():
    vlc.sendline("volup 1")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/vol_less")
def vol_down():
    vlc.sendline("voldown 1")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/next")
def next():
    vlc.sendline("next")
    vlc.expect('>')
    return Response(status=200)

@jukebox.route("/prev")
def prev():
    vlc.sendline("prev")
    vlc.expect('>')
    return Response(status=200)


@jukebox.route("/time")
def get_time():
    vlc.sendline("get_time")
    vlc.expect('>')
    tempt = vlc.before.decode('utf-8', 'ignore').partition("get_time")[-1].strip()
    response = make_response(tempt, 200)
    response.mime_type = "text/plain"
    return response

@jukebox.route("/title")
def get_title():
    vlc.sendline("get_title")
    vlc.expect('>')
    tempt = vlc.before.decode('utf-8', 'ignore').partition("get_title")[-1].strip()
    response = make_response(tempt, 200)
    response.mime_type = "text/plain"
    return response

@jukebox.route("/length")
def get_length():
    vlc.sendline("get_length")
    vlc.expect('>')
    tempt = vlc.before.decode('utf-8', 'ignore').partition("get_length")[-1].strip()
    response = make_response(tempt, 200)
    response.mime_type = "text/plain"
    return response

jukebox.run(host="0.0.0.0", port=8080)



