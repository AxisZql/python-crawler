import urllib.request
from fake_useragent import UserAgent
import time
import urllib.error
import http.cookiejar
import socket
from bs4 import BeautifulSoup

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'https://www.invshen.net'
}

# 网站的图片必须是在自己的网址链接打开才可以下载

headers['User-Agent']=UserAgent().random

headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)

# 设置cookie
cjar=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))

opener.addheaders=headall

base_url='https://www.invshen.net'

base_album_url='https://www.invshen.net/girl/27942/album/'



urllib.request.install_opener(opener)

def getallMini(base_album_url,base_url):
    # global 
    bs='https://www.invshen.net/girl/27942/album/'
    allalbum=[]
    try:
        # 获取四个相册页面的所有图集链接
        for i in range(1,2):
            print(i)
            wei='%d'%(i)+'.html'
            base_album_url=bs+wei
            data_text=urllib.request.urlopen(base_album_url)
            time.sleep(1)
            try:
                data_text=data_text.read()
            except:
                print("READ TIME OUT")
            bsObj=BeautifulSoup(data_text,"html.parser")
            for imglink in bsObj.findAll("a",{"class":"igalleryli_link"}):
                imglink=imglink['href']
                imglink=base_url+imglink
                allalbum.append(imglink)
        return allalbum
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
        if isinstance(e.reason,socket.timeout):
            print("TIME OUT")


#下载图片的函数
def img_download(cur_page):
    global img_num
    global page_num
    global tuji_num
    try:
        data_text=urllib.request.urlopen(cur_page,timeout=10)
        try:
            data_text=data_text.read()
        except:
            print('READ TIME OUT')
        print('-----------------第%d页下载开始--------------'%(page_num))
        bsObj=BeautifulSoup(data_text,"html.parser")
        for child in bsObj.find("ul",{"id":"hgallery"}).children:
            # print(child['src'])
            try:
                data=urllib.request.urlopen(child['src'],timeout=10)
                try:
                    data=data.read()
                    # 因为该网站不支持直接用图片链接下载，所以先打开图片链接在把图片保存
                    file=open('youpath'+'.jpg','wb')
                    file.write(data)
                    file.close()
                    print('下载第%d'%(img_num)+"张图片完毕！")
                    img_num=img_num+1
                except:
                    print("READ TIME OUT!")
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                if isinstance(e.reason,socket.timeout):
                    print("TIME OUT")
    
        i=1
        nextPage=''
        for next in bsObj.find("div",{"id":"pages"}).findAll("a",{"class":"a1"}):
            if i==2:
                # print(next['href'])
                nextPage=next['href']            
            else:
                i=i+1
        return nextPage
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        if isinstance(e.reason,socket.timeout):
            print("TIME OUT")


# 获取所有图集链接
allalbum=getallMini(base_album_url,base_url)

for album in allalbum:
    print(album)

allalbum=[
'https://www.invshen.net/g/35602/',
'https://www.invshen.net/g/35503/',

]
# 图片编号
img_num=1

tuji_num=0

AllPageLinks=[]
for cur_page in allalbum:
    flag=1
    # 加入第一页的网址
    AllPageLinks.append(cur_page)
    
    print('------------------第%d'%(tuji_num)+'图集开始下载----------------------')
    tuji_num=tuji_num+1
    # 当前页码
    page_num=1
    # 下载完每一页的图片
    while flag==1:
        nextPage=img_download(cur_page)
        page_num=page_num+1
        cur_page=base_url+nextPage
        if cur_page not in AllPageLinks:
            AllPageLinks.append(cur_page)
        else:
            flag=0
