import urllib2
import time
import os
import re
def filepath():
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
def makedr(title,path):
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path
def getFile(addr,path):
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
    while stopTime-startTime>=60:
        startTime=time.time()
        title = filepath()
        htmlPath='D:\\tmp\\backup\\'
        makedr('backup','D:\\tmp\\')
        new_htmlPath=makedr(title,htmlPath)
        print
        f=urllib2.urlopen('http://m.sohu.com')
        buf=f.read()
        out = open('%s\\souhu.html'%new_htmlPath,'w')
        out.write(buf)
        out.close()
        addrjs=re.findall('http.*js',buf)
        jsPath=makedr('js',new_htmlPath)
        for m in addrjs:
            getFile(m,jsPath)
        addrcss=re.findall('http.*css',buf)
        cssPath=makedr('css',new_htmlPath)
        for n in addrcss:
            getFile(n,cssPath)
        addrImg=re.findall('http:\/\/.*?\.jpg|http:\/\/.*?\.png',buf)
        imagePath=makedr('images',new_htmlPath)
        for i in addrImg:
            getFile(i,imagePath)
    stopTime=time.time()


   
        
