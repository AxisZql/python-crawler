import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import time
import socket
import re
import urllib.error
# 第三方随机请求头库，贼好用
import fake_useragent
from fake_useragent import UserAgent
from soupsieve.css_match import RE_WEEK


# 构造必要的请求头
headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    # 这个请求头是默认的
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Referer": "https://zh.numberempire.com/integralcalculator.php",
    "Connection":"keep-alive"
}
def getUrl(Num):
    Tool_url=[
    "https://zh.numberempire.com/integralcalculator.php",#不定积分工具0
    "https://zh.numberempire.com/derivativecalculator.php",#函数求导工具1
    "https://zh.numberempire.com/factoringcalculator.php",#因式分解工具 2
    "https://zh.numberempire.com/definiteintegralcalculator.php",#定积分 3
    "https://zh.numberempire.com/limitcalculator.php",#极限计算器 4
    "https://zh.numberempire.com/simplifyexpression.php"#表达式化简器5
    ]
    return Tool_url[Num]
def getPostType(Num):
    if Num==0:
        postdata={
            "function":"",#表达式
            "var":"",#自变量
            "answers":"",#反爬变量
            "_p1":""#反爬参数
        }
    elif Num==1:
        postdata={
            "function":"",#表达式
            "var":"",#自变量
            "order":"",#求导阶数
            "_p1":""#反爬参数
        }
    elif Num==2:
        postdata={
            "function":"",
            "_p1":""
        }
    elif Num==3:
        postdata={
            "function":"",#表达式
            "var":"",#自变量
            "a":"",#积分左端点
            "b":"",#积分右端点
            "answers":"",#反爬变量
            "_p1":""#反爬参数

        }
    elif Num==4:
        postdata={
            "function":"",#表达式
            "var":"",#自变量
            "val":"",#展开点
            "answers":"",#反爬变量
            "limit_type":"",#极限类型
            "_p1":""#反爬参数
        }
    elif Num==5:
        postdata={
            "function":"",
            "_p1":""
        }
    return postdata    


# 提取出密钥
def getJM(ch):
    pattern=r"process1\('.*'\)"
    ans=re.findall(pattern, ch)
    ans=ans[0]
    pattern2=r"'(.+?)'"
    ans2=re.findall(pattern2, ans)
    ans2=ans2[0]
    return ans2

def get_p1(process1):
    s=0
    # 将每个字符转换为Unicode编码，然后累加最后得到_p1
    for a in process1:
        s+=ord(a)
    return s

def get_postdata(_p1,Num):
    print("---------------------------开始处理--------------------------------")
    if Num==0:
        # 不定积分
        postdata['function']=input("请输入表达式")
        postdata['var']=input("请输入自变量")
    elif Num==1:
        # 函数求导
        postdata['function']=input("请输入表达式")
        postdata['var']=input("请输入自变量")
        postdata['order']=input('请输入求导阶数')
    elif Num==2:
        # 因式分解
        postdata['function']=input("请输入表达式")
    elif Num==3:
        # 定积分
        postdata['function']=input("请输入表达式")
        postdata['var']=input("请输入自变量")
        postdata['a']=input("请输入积分左侧点")
        postdata['b']=input("请输入积分右侧点")
    elif Num==4:
        # 极限计算器
        postdata['function']=input("请输入表达式")
        postdata['var']=input("请输入自变量")
        lmType=['two-sided','plus','minus']
        postdata['val']=input("展开点")
        selectType=input("极限类型：双侧极限 0\t右侧极限 1\t左侧极限2")
        selectType=int(selectType)
        postdata['limit_type']=lmType[selectType]
    elif Num==5:
        # 表达式化简
        postdata['function']=input("请输入表达式")
    postdata['_p1']=_p1


num=input("选择网站")
num=int(num)
or_url=getUrl(num)
postdata=getPostType(num)
print(or_url)
print(postdata)




# 获取随机请求头
headers['User-Agent']=UserAgent().random
headers['Referer']=or_url

# 建立空列表，为了以指定格式存储头信息
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)



# 设置cookie
cjar=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))

# 将指定格式的headers添加上
opener.addheaders=headall
# 将opener安装为全局
urllib.request.install_opener(opener)
try:
    data=urllib.request.urlopen(or_url,timeout=10).read()
    # data=data_t.read()
    
    soup_obj=BeautifulSoup(data,"html.parser")
    
    # 找出body标签中所有script标签
    scriptList=soup_obj.select("body script")
    i=1
    for sc in scriptList:
        if i==7:
            if sc is not None:
                str1=sc.contents[0]
        else:
            i=i+1
    print("----------------欢迎使用不定积分积分计算器----------------")
    process1=getJM(str1)
    print("提取出的数据:"+process1)
    _p1=get_p1(process1)
    print("解密的数据:"+str(_p1))
    
    # 获取提交数据
    get_postdata(_p1,num)
    # 对提交的数据进行编码
    postdata=urllib.parse.urlencode(postdata).encode('utf-8')
    # 构造post请求
    req=urllib.request.Request(or_url,postdata)
    try:
        data_text=opener.open(req,timeout=10).read()
        j=1
        ans_soup=BeautifulSoup(data_text,"html.parser")
        ansScriptList=ans_soup.select("body script")
        for sc in ansScriptList:
            if j==6:
                if sc is not None:
                    result1=sc.contents[0]
                break
            else:
                j=j+1

        file1=open("ans.html","wb")
        file1.write(data_text)
        file1.close()
        bs_ans=BeautifulSoup(data_text,"html.parser")        
        #提取出计算结果盒子中的内容
        js_ans=bs_ans.find("span",attrs={'id':'result1'})
        if js_ans is not None:
            if js_ans.contents is not None:
                if len(js_ans.contents)!=0:
                   js_ans=js_ans.contents[0]
                   print("------------------------------不定积分的结果----------------------------------------")
                   print(js_ans)
                   print("++++++++++++++++++++++++++++++++++MATHML+++++++++++++++++++++++++++++++")
                   print(result1)
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!无法积分!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("**********************************出错了******************************************")
                print("请检查您输入的表达式是否有误")
        else:
            print("请检查您输入的表达式是否有误")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if isinstance(e.reason,socket.timeout):
                print('Time out')
        if hasattr(e,"reason"):
            print(e.reason)
        if isinstance(e.reason,socket.timeout):
                print('Time out')
        # return data_t
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print(e.code)
        if isinstance(e.reason,socket.timeout):
            print('Time out')
    if hasattr(e,"reason"):
        print(e.reason)
        if isinstance(e.reason,socket.timeout):
            print('Time out')

    



