# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
# from bs4 import soup
#获取网页源代码
def pageCode(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url,headers = headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print e.reason
    else:
        content = response.read()
    return content

#获取页面个数
def pageNum(url):
    content = pageCode(url)
    fin = r'<span class="PageMore"'
    if re.findall(fin,content):
        page = content.find(r'PageMore')
        title = content.find(r'title=',page)
        end = content.find(r'">',title)
        num = int(content[title+7:end])
        #print num
    else:
         fin = r'class="PageLink"'
         pages = re.findall(fin,content)
         num = len(pages)+1
         #print num
    return num

#获取各页面链接保存到next_page
def pageLink(url,num,c):
    next_page = []
    i = 2
    next_page.append(url)
    while i<num+1:
        if c==1:
            next_page_url = url+'p'+str(i)
        elif c==2:
            next_page_url = url+'?pageno='+str(i)
        else:
            next_page_url = url+'?pg='+str(i)
        next_page.append(next_page_url)
        i = i+1
    # for con in next_page:
    #     print con
    return next_page

#获取页面中具体景点的链接
def shopLink(next_page):
    jump=[] #jump中储存了所有景点的链接
    for page in next_page:
        content = pageCode(page)
        rex = r'/shop/[0-9]+"  >'
        lists = re.findall(rex, content)
        for list in lists:
            list = list.replace('"  >','')
            #print list
            jump.append('https://www.dianping.com'+list)
    return jump
    # for con in jump:
    #     print con

#定位到全部点评，返回全部点评对应的url
def showAll(url):
    url = url+'/review_more'
    return url

#创建目录
def createFolder(num):
    i = 0
    while i<num:
        os.mkdir('C:\Users\lenovo\PycharmProjects\comments\%s'%(i))
        i = i+1

#下载页面中的全部分享图片
def download(url,j,i):
    # pho储存所有图片链接
    # pageurl储存所有更多图片页面的链接
    pageurl = []
    # 查找所有图片链接（包括重复项）
    content = pageCode(url)
    fin1 = r'img src="(http://.*?\.jpg)" panel'
    pho = re.findall(fin1,content)
    # 进入更多图片页面，获取各链接
    more = r'<li class="more"><a target="_blank"  href="(/shop/[0-9]+/photos/album/[0-9]+)"'
    mo = re.findall(more,content)
    for mor in mo:
        pageurl.append("https://www.dianping.com"+mor)
    for page in pageurl:
        # 获取各页面具体链接
        pg = pageLink(page,pageNum(page),3)
        # 获取各页面的代码
        for pglink in pg:
            content = pageCode(pglink)
            fin3 = r'src="(http://.*?\.jpg)" title'
            pho3 = re.findall(fin3,content)
            for phot in pho3:
                pho.append(phot)
    photo = list(set(pho))
    for picurl in photo:
        print picurl
        urllib.urlretrieve(picurl,'C:\Users\lenovo\PycharmProjects\comments\%s\%s.jpg'%(j,i))
        i = i+1
        print "downloading picture:"+str(i)
    return i

#url需改进为能够根据不同类别自动生成
url = 'https://www.dianping.com/search/category/8/35/r39'     #武侯区
con = pageCode(url)
num = pageNum(url)                                                    #shop页面数
pagelink = pageLink(url,num,1)                                        #有shop的页面链接
shop = shopLink(pagelink)                                             #武侯区所有shop链接
shopNum = len(shop)                                                   #shop个数
print 'shopNum:'+str(shopNum)
createFolder(shopNum)

# 下载logo
m = 0
shoplogo = r'data-src="(http://.*?\.jpg)"'
print "start downloading the logos!"
for pl in pagelink:
    con = pageCode(pl)
    logolink = re.findall(shoplogo,con)
    for logo in logolink:
        print logo
        urllib.urlretrieve(logo,'C:\Users\lenovo\PycharmProjects\comments\%s\%s.jpg'%(m,0))
        m = m+1
        print "finished"

j = 0
for u in shop:
    sh = 0
    pic = 1
    print "shop:"+str(sh)
    num = pageNum(showAll(u))                                         #得到每个shop对应的全部点评页面数目
    page = pageLink(showAll(u),num,2)                                 #所有点评页面的url
    for p in page:
        pic = download(p,sh,pic)                                                   #下载点评页面上的所有图片
        print pic
    sh = sh+1