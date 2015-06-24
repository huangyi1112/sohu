# -*- coding: cp936 -*-
import urllib2,time,os,re,sys,getopt,string
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

def webGrab(buf,path,mode):#将buf以mode的存储模式存储在本地path下
    out = open(path,mode)
    out.write(buf)
    out.close()
    
def makedr(title,path): #在path路径下创建名为title的文件夹，并且返回该文件夹的路径，返回值类型str
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path

def makeFolder(htmlPath): #新建与时间相关的文件夹
    title = filepath()
    new_htmlPath=makedr(title,htmlPath)#在\tmp\backup\新建与系统时间相关的文件夹
    return new_htmlPath
def getFile(addr,path):  #存储已知网页路径的文件，存储到本地path的位置，文件名为本来的名字不变
    splitPath = addr.split('/')
    fName = splitPath.pop()
    f=urllib2.urlopen(addr)
    buf=f.read()
    webGrab(buf,'%s\\%s'%(path,fName),'wb')
    
def CodeOut(startLabel,endLabel,fileNum,fileContent,fileSuffix,path):#取出相应标签内的代码
    fileContent=fileContent.split(startLabel)
    fileContent.pop(0)
    fileContent=''.join(fileContent)
    fileContent=fileContent.split(endLabel)
    fileContent.pop()
    fileContent=''.join(fileContent)
    fileName=str(fileNum)+fileSuffix
    webGrab(fileContent,'%s\\%s'%(path,fileName),'wb')#保存代码
    
def jsCode(new_htmlPath,buf):#抓取js的函数
    addrjs=re.findall('<script.*?</script>',buf,re.S)
    while addrjs!=[]:
        jsPath=makedr('js',new_htmlPath)#新建js文件夹
        singleJs=addrjs.pop()#弹出list的最后一个
        singleJs1=re.findall('http.*?\.js',singleJs)#验证是否是.js结尾的js
        if singleJs1!=[]:  #判断条件 js文件的网页路径已知
            singleJs1=''.join(singleJs1)
            getFile(singleJs1,jsPath)
        else:   #是内部的js
            global jsNameNum
            jsNameNum+=1
            CodeOut('<script type="text/javascript">','</script>',jsNameNum,singleJs,'.js',jsPath)

def cssCode(new_htmlPath,buf):#抓取css的函数
    addrcss=re.findall('<style.*?</style>',buf,re.S)# 外部样式表
    global cssNameNum
    while addrcss!=[]:
        cssPath=makedr('css',new_htmlPath)
        singleCss=addrcss.pop()
        cssNameNum+=1
        CodeOut('<style type="text/css">','</style>',cssNameNum,singleCss,'.css',cssPath)
    addrcss2=re.findall('http.*?\.css',buf)#为了匹配内部样式表
    if addrcss2!=[]:
        cssPath=makedr('css',new_htmlPath)
    for n in addrcss2:
        getFile(n,cssPath)
    addrcss3=re.findall(r'style=".*?"',buf,re.S)#为了匹配内联样式
    addrcss3=list(set(addrcss3))#删除重复的样式
    while addrcss3!=[]:
        cssPath=makedr('css',new_htmlPath)
        singleCss3=addrcss3.pop()
        cssNameNum+=1
        CodeOut('style=\"','\"',cssNameNum,singleCss3,'.css',cssPath)

def imagefile(new_htmlPath,buf):#抓取图片的函数
    addrImg=re.findall('http://.*?\.jpe?g|http://.*?\.png',buf)#匹配图片
    addrImg=list(set(addrImg))
    imagePath=makedr('images',new_htmlPath)
    for i in addrImg:
        getFile(i,imagePath)


opts,args=getopt.getopt(sys.argv[1:],'hd:u:o:')#处理命令行参数
for op,value in opts:
    if op=='-d':
        period=string.atoi(value)
    elif op=='-u':
        htmlUrl=value
    elif op=='-o':
        htmlPath=value
startTime=time.time()
stopTime=time.time()+period
while True:
    while stopTime-startTime>=period:#设置循环条件
        startTime=time.time()
        jsNameNum=0  #后面用来保存内部js的文件名，为了方便，内部的js存储名为整数0-n
        cssNameNum=0
        f=urllib2.urlopen(htmlUrl)
        buf=f.read()#抓取手机搜狐的网页
        new_htmlPath=makeFolder(htmlPath)#新建与时间相关的文件夹，返回路径
        webGrab(buf,'%s\\souhu.html'%new_htmlPath,'w')#存储html
        jsCode(new_htmlPath,buf)#存储js
        cssCode(new_htmlPath,buf)#存储css
        imagefile(new_htmlPath,buf)#存储图片
    stopTime=time.time()


   
        
