# -*- coding: cp936 -*-
import urllib2
import time
import os
import re
def filepath():  #�õ�����Ҫ����ϵͳʱ����ص��ļ�����������ֵ����Ϊstr
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
def makedr(title,path): #��path·���´�����Ϊtitle���ļ��У����ҷ��ظ��ļ��е�·��������ֵ����str
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path
def getFile(addr,path):  #�洢��֪��ҳ·�����ļ����洢������path��λ�ã��ļ���Ϊ���������ֲ���
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
    while stopTime-startTime>=60:#����ѭ������
        startTime=time.time()
        jsNameNum=0  #�������������ڲ�js���ļ�����Ϊ�˷��㣬�ڲ���js�洢��Ϊ����0-n
        cssNameNum=0
        title = filepath()
        htmlPath='D:\\tmp\\backup\\'
        makedr('backup','D:\\tmp\\')#�ڱ���D���½�tmp�ļ��У������½�backup�ļ���
        new_htmlPath=makedr(title,htmlPath)#��D:\tmp\backup\�½���ϵͳʱ����ص��ļ���
        f=urllib2.urlopen('http://m.sohu.com')
        buf=f.read()
        out = open('%s\\souhu.html'%new_htmlPath,'w')#�洢html
        out.write(buf)
        out.close()
        addrjs=re.findall('\<script.*?\<\/script>',buf,re.S)#ƥ��js
        while addrjs!=[]:
            jsPath=makedr('js',new_htmlPath)#�½�js�ļ���
            singleJs=addrjs.pop()#����list�����һ��
            singleJs1=re.findall('http.*?\.js',singleJs)#��֤�Ƿ���.js��β��js
            if singleJs1!=[]:  #�ж����� js�ļ�����ҳ·����֪
                singleJs1=''.join(singleJs1)
                getFile(singleJs1,jsPath)
            else:   #���ڲ���js
                jsNameNum+=1
                ####����jsҪ�洢�Ĳ���
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
        addrcss=re.findall('\<style.*?\<\/style>',buf,re.S)# css�Ĵ洢ԭ���js��ȫһ��������׸��
        while addrcss!=[]:
            cssPath=makedr('css',new_htmlPath)
            singleCss=addrcss.pop()
            addrCss1=re.findall('http.*?\.js',singleCss)
            if addrCss1!=[]:
                aaddrCss1=''.join(addrCss1)
                getFile(addrCss1,cssPath)
            else:
                cssNameNum+=1
                ####����csҪ�洢�Ĳ���
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
        addrcss2=re.findall('http.*css',buf)#Ϊ��ƥ���ڲ���ʽ��
        cssPath=makedr('css',new_htmlPath)
        for n in addrcss2:
            getFile(n,cssPath)
        addrImg=re.findall('http:\/\/.*?\.jpg|http:\/\/.*?\.png',buf)#ƥ��ͼƬ
        imagePath=makedr('images',new_htmlPath)
        for i in addrImg:
            getFile(i,imagePath)
    stopTime=time.time()


   
        
