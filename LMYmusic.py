#coding=utf-8
import requests
import json
import re
import os
from urllib import request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
def getjson(jsontext):
    rejson=json.loads(re.findall(r"^\w+\((.*)\)$", jsontext)[0])
    return rejson

def getMusicList(word):
    #word="演员"
    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=58294319880195336&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w="+word+"&g_tk=5381&jsonpCallback=MusicJsonCallback10263594486078043&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    t=requests.get(url,headers=headers)
    t.encoding=t.apparent_encoding
    #print(t.encoding)#utf-8
    a=t.text
    musiclist=json.loads(re.findall(r"^\w+\((.*)\)$",a)[0])
    #print(musiclist)
    return musiclist
#获取songmid
def getSongmid(MusicList):
    mysongmid = []
    musicName=[]
    singerName=[]
    MusicListdata=MusicList.get("data")
    MusicListSong=MusicListdata.get("song")
    MusicListList=MusicListSong.get("list")
    for i in MusicListList:
        # print(i.get("file").get("strMediaMid"))
        # print(i.get("name"))
        # print(i["singer"][0].get("name"))
        mysongmid.append(i.get("file").get("strMediaMid"))
        musicName.append(i.get("name"))
        singerName.append(i["singer"][0].get("name"))
    return mysongmid,musicName,singerName
def getVkey(songmid):
    musicURL=[]
    for i in songmid:
        url="https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=678733985&jsonpCallback=MusicJsonCallback8015407264426806&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback8015407264426806&songmid={}&filename=C100{}.m4a&guid=1674273789".format(i,i)
        #print(url)
        vkeydict = requests.get(url, headers=headers)
        vkeydata = getjson(vkeydict.text)
        vkeyitems = vkeydata.get("data").get("items")
        for i in vkeyitems:
            # print(i.get("songmid"))
            # print(i.get("filename"))
            # print(i.get("vkey"))
            musciurl = "http://streamoc.music.tc.qq.com/{filename}?guid=0&uin=0&fromtag=53&vkey={vkey}".format(
                filename=i.get("filename"), vkey=i.get("vkey"))
            #print("歌曲链接为:" + musciurl)
            musicURL.append(musciurl)
    return musicURL
def downloadMusic(musicName):
    music = getMusicList(musicName)
    songmid,musicName,singerName= getSongmid(music)
    lista = getVkey(songmid)
    for link in range(3):
        #print(link)
        filename = os.getcwd()+musicName[link]+"-"+singerName[link]+".m4a"
        # request.urlretrieve(lista[link], filename)
        print(lista[link])
downloadMusic("演员")
