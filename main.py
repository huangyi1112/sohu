# -*- coding: cp936 -*-
import urllib2
import time
import os
import re
def filepath():  #得到所需要的与系统时间相关的文件夹名，返回值类型为str
    now = time.localtime()
    year=str(now.tm_year)
    mon=now.tm_mon
    if mon<10:
        mon=''.join(['0',str(mon)])
    else:
        mon=str(mon)
    day=now.tm_mday
    if day<10:
        day=''.join(['0',str(day)])
    else:
        day=str(day)
    hour=now.tm_hour
    if hour<10:
        hour=''.join(['0',str(hour)])
    else:
        hour=str(hour)
    mmin=now.tm_min
    if mmin<10:
        mmin=''.join(['0',str(mmin)])
    else:
        mmin=str(mmin)
    dirname=''.join([year,mon,day,hour,mmin])
    return dirname
def makedr(title,path): #在path路径下创建名为title的文件夹，并且返回该文件夹的路径，返回值类型str
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path
def getFile(addr,path):  #存储已知网页路径的文件，存储到本地path的位置，文件名为本来的名字不变
    u = urllib2.urlopen(addr)
    data = u.read()
    splitPath = addr.split('/')
    fName = splitPath.pop()
    f = open('%s\\%s'%(path,fName), 'wb')
    f.write(data)
    f.close()
startTime=time.time()
stopTime=time.time()+60
while True:
    while stopTime-startTime>=60:#设置循环条件
        startTime=time.time()
        jsNameNum=0  #后面用来保存内部js的文件名，为了方便，内部的js存储名为整数0-n
        cssNameNum=0
        title = filepath()
        htmlPath='D:\\tmp\\backup\\'
        makedr('backup','D:\\tmp\\')#在本地D盘新建tmp文件夹，里面新建backup文件夹
        new_htmlPath=makedr(title,htmlPath)#在D:\tmp\backup\新建与系统时间相关的文件夹
        f=urllib2.urlopen('http://m.sohu.com')
        buf=f.read()
        out = open('%s\\souhu.html'%new_htmlPath,'w')#存储html
        out.write(buf)
        out.close()
        addrjs=re.findall('\<script.*?\<\/script>',buf,re.S)#匹配js
        while addrjs!=[]:
            jsPath=makedr('js',new_htmlPath)#新建js文件夹
            singleJs=addrjs.pop()#弹出list的最后一个
            singleJs1=re.findall('http.*?\.js',singleJs)#验证是否是.js结尾的js
            if singleJs1!=[]:  #判断条件 js文件的网页路径已知
                singleJs1=''.join(singleJs1)
                getFile(singleJs1,jsPath)
            else:   #是内部的js
                jsNameNum+=1
                ####整出js要存储的部分
                singleJs=singleJs.split('</script>')
                singleJs.pop()
                singleJs=''.join(singleJs)
                singleJs=singleJs.split('<script type="text/javascript">')
                singleJs.pop(0)
                singleJs=''.join(singleJs)
                jsName=str(jsNameNum)+'.js'
                f = open('%s\\%s'%(jsPath,jsName), 'wb')
                f.write(singleJs)
                f.close()
                ###
        addrcss=re.findall('\<style.*?\<\/style>',buf,re.S)# css的存储原理和js完全一样，不再赘述
        while addrcss!=[]:
            cssPath=makedr('css',new_htmlPath)
            singleCss=addrcss.pop()
            addrCss1=re.findall('http.*?\.js',singleCss)
            if addrCss1!=[]:
                aaddrCss1=''.join(addrCss1)
                getFile(addrCss1,cssPath)
            else:
                cssNameNum+=1
                ####整出cs要存储的部分
                singleCss=singleCss.split('</style>')
                singleCss.pop()
                singleCss=''.join(singleCss)
                singleCss=singleCss.split('<style type="text/css">')
                singleCss.pop(0)
                singleCss=''.join(singleCss)
                cssName=str(cssNameNum)+'.css'
                f = open('%s\\%s'%(cssPath,cssName), 'wb')
                f.write(singleCss)
                f.close()
        addrcss2=re.findall('http.*css',buf)#为了匹配内部样式表
        cssPath=makedr('css',new_htmlPath)
        for n in addrcss2:
            getFile(n,cssPath)
        addrImg=re.findall('http:\/\/.*?\.jpg|http:\/\/.*?\.png',buf)#匹配图片
        imagePath=makedr('images',new_htmlPath)
        for i in addrImg:
            getFile(i,imagePath)
    stopTime=time.time()


   
        
