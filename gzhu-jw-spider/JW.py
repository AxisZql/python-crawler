import urllib.parse
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.error
import socket
import time
import copy
from lxml import etree  #导入可以将html转换为xpath可识别的类型
import json



url = {
    "login": "https://cas.gzhu.edu.cn/cas_server/login?service=http://jwxt.gzhu.edu.cn/sso/lyiotlogin",#用这个url登陆会直接到教务系统
    "course":"http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su=default",
    # 引入两个course是为了防止第一个不行,打开这两个网站得到的是json数据，xnm表示学年，xqm表示学期，1表示第一学期，12表示第二学期
    "_course":"http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151&su=default&xnm=2020&xqm=12",
    "course":"http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508&su=default&xnm=2020&xqm=12"    
}


headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'utf-8',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
'Referer':'https://cas.gzhu.edu.cn/cas_server/login'
}

headers['User-Agent']=UserAgent().random

headall=[]

for key,value in headers.items():
    item=(key,value)
    headall.append(item)

# 设置cookie
cjar=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))

opener.addheaders=headall

urllib.request.install_opener(opener)

#获取提交数据
def get_post_data(url):
    try:
        html=urllib.request.urlopen(url)
        try:
            html=html.read()
        except:
            print("READ TIMEOUT")
        bsObj=BeautifulSoup(html,"html.parser")
    
        #找到验证码参数
        lt=bsObj.find('input',attrs={'name':'lt'})['value']
        execution=bsObj.find('input',attrs={'name':'execution'})['value']
        _eventId=bsObj.find('input',attrs={'name':'_eventId'})['value']
        submit=bsObj.find('input',attrs={'name':"submit"})['value']
        warn=bsObj.find('input',attrs={'name':'warn'})['value']
    
        #下载验证码图片
        pic=urllib.request.urlretrieve('https://cas.gzhu.edu.cn/cas_server/captcha.jsp','ver_pic5.png')
 
        #构造需要post的参数表
        data={'username':'username',
              'password':'password',
              'captcha':'',
              'warn':'',
              'lt':'',
              'execution':'',
              '_eventId':'',
              'submit':''}
    
        #构造登陆的post参数
        # data['username']=input('请输入学号')
        # data['password']=input('请输入密码')
        data['captcha']=input('请输入验证码')
        data['warn']=warn
        data['lt']=lt
        data['execution']=execution
        data['_eventId']=_eventId
        data['submit']=submit
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
            if isinstance(e.reason,socket.timeout):
                print("TIME OUT")
        if hasattr(e,"reason"):
            print(e.reason)
            if isinstance(e.reason,socket.timeout):
                print("TIME OUT")
        

postdata=get_post_data(url['login'])
postdata=urllib.parse.urlencode(postdata).encode('utf-8')
print(postdata)

r=urllib.request.urlopen(url['login'],postdata)
r=r.read()
file=open('./HTML页面/教务系统页面.html','wb')
file.write(r)
file.close()

# time.sleep(10)
res=urllib.request.urlopen(url['_course'])

res=res.read()
js=json.loads(res)




kbList=js['kbList']
Course=[]
for kb in kbList:
    course={
    'kcmc':'',#课程名称 
    'jcor':'',#节次 1-2
    'qsj':'',#课程起始节
    'jsj':'',#课程结束节
    # 'qsz':'',#课程起始周
    # 'jsz':'',#课程结束周
    'cdmc':'',#上课地点
    'kcxszc':'',#格式为 理论：32
    'xm':'',#教师名称
    'zxs':'',#总学时
    'xf':'',#学分
    'zcmc':'',#教师职称
    'xqjmc':'',#星期一
    'd_or_s':'no',#表示单周或者双周才上课,默认为no
    }
    course['kcmc']=kb['kcmc']
    course['jcor']=kb['jcor']

    x=kb['jcor'].split('-')
    course['qsj']=int(x[0])
    course['jsj']=int(x[1])

    course['cdmc']=kb['cdmc']
    course['kcxszc']=kb['kcxszc']
    course['xm']=kb['xm']
    
    try:
        # 周数连续的情况
        dpos=kb['zcd'].index('-')
        y=kb['zcd'].split('-')
        q=list(y[1])
        if q[-2]=='双':
            course['d_or_s']='s'
        elif q[-2]=='单':
            course['d_or_s']='d'
        pos=q.index('周')
        y[1]=y[1][:pos]
        course['qsz']=int(y[0])
        course['jsz']=int(y[1])
    except:
        try:
            # 周数离散的情况
            gpos=kb['zcd'].index(',')
            y=kb['zcd'].split(',')
            i=0
            for ly in y:
                pos=ly.index('周')
                ly=int(ly[:pos])
                y[i]=ly
                i+=1
            j=0
            for ly in y:
                course['z'+str(j)]=ly
                j+=1
            # 记录离散的周数一共有多少个
            course['ls_num']=j
        except:
            # 只有一周的情况
            pos=kb['zcd'].index('周')
            y=kb['zcd']
            y=y[:pos]
            course['z0']=int(y)
            course['ls_num']=1

    

    course['zxs']=kb['zxs']
    course['xf']=kb['xf']
    try:
       course['zcmc']=kb['zcmc']
    except:
        course['zcmc']='未知'
    course['xqjmc']=kb['xqjmc']


    Course.append(course)


sjkList=js['sjkList']
Sjk=[]
for sj in sjkList:
    sjCourse={
    'jsxm':'',#教师姓名
    'kcmc':'',#操作系统课程设计@陶文正,王艳(共2周)/17-18周
    'qsjsz':'',#17-18周
    }
    sjCourse['jsxm']=sj['jsxm']
    sjCourse['kcmc']=sj['sjkcgs']
    sjCourse['qsjsz']=sj['qsjsz']
    Sjk.append(sjCourse)



file=open('./HTML页面/课表页面.html','wb')
file.write(res)
file.close()










