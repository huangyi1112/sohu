# -*- coding: cp936 -*-
import urllib2,time,os,re,sys,getopt,string
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

def webGrab(buf,path,mode):#��buf��mode�Ĵ洢ģʽ�洢�ڱ���path��
    out = open(path,mode)
    out.write(buf)
    out.close()
    
def makedr(title,path): #��path·���´�����Ϊtitle���ļ��У����ҷ��ظ��ļ��е�·��������ֵ����str
    new_path = os.path.join(path, title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    return new_path

def makeFolder(htmlPath): #�½���ʱ����ص��ļ���
    title = filepath()
    new_htmlPath=makedr(title,htmlPath)#��\tmp\backup\�½���ϵͳʱ����ص��ļ���
    return new_htmlPath
def getFile(addr,path):  #�洢��֪��ҳ·�����ļ����洢������path��λ�ã��ļ���Ϊ���������ֲ���
    splitPath = addr.split('/')
    fName = splitPath.pop()
    f=urllib2.urlopen(addr)
    buf=f.read()
    webGrab(buf,'%s\\%s'%(path,fName),'wb')
    
def CodeOut(startLabel,endLabel,fileNum,fileContent,fileSuffix,path):#ȡ����Ӧ��ǩ�ڵĴ���
    fileContent=fileContent.split(startLabel)
    fileContent.pop(0)
    fileContent=''.join(fileContent)
    fileContent=fileContent.split(endLabel)
    fileContent.pop()
    fileContent=''.join(fileContent)
    fileName=str(fileNum)+fileSuffix
    webGrab(fileContent,'%s\\%s'%(path,fileName),'wb')#�������
    
def jsCode(new_htmlPath,buf):#ץȡjs�ĺ���
    addrjs=re.findall('<script.*?</script>',buf,re.S)
    while addrjs!=[]:
        jsPath=makedr('js',new_htmlPath)#�½�js�ļ���
        singleJs=addrjs.pop()#����list�����һ��
        singleJs1=re.findall('http.*?\.js',singleJs)#��֤�Ƿ���.js��β��js
        if singleJs1!=[]:  #�ж����� js�ļ�����ҳ·����֪
            singleJs1=''.join(singleJs1)
            getFile(singleJs1,jsPath)
        else:   #���ڲ���js
            global jsNameNum
            jsNameNum+=1
            CodeOut('<script type="text/javascript">','</script>',jsNameNum,singleJs,'.js',jsPath)

def cssCode(new_htmlPath,buf):#ץȡcss�ĺ���
    addrcss=re.findall('<style.*?</style>',buf,re.S)# �ⲿ��ʽ��
    global cssNameNum
    while addrcss!=[]:
        cssPath=makedr('css',new_htmlPath)
        singleCss=addrcss.pop()
        cssNameNum+=1
        CodeOut('<style type="text/css">','</style>',cssNameNum,singleCss,'.css',cssPath)
    addrcss2=re.findall('http.*?\.css',buf)#Ϊ��ƥ���ڲ���ʽ��
    if addrcss2!=[]:
        cssPath=makedr('css',new_htmlPath)
    for n in addrcss2:
        getFile(n,cssPath)
    addrcss3=re.findall(r'style=".*?"',buf,re.S)#Ϊ��ƥ��������ʽ
    addrcss3=list(set(addrcss3))#ɾ���ظ�����ʽ
    while addrcss3!=[]:
        cssPath=makedr('css',new_htmlPath)
        singleCss3=addrcss3.pop()
        cssNameNum+=1
        CodeOut('style=\"','\"',cssNameNum,singleCss3,'.css',cssPath)

def imagefile(new_htmlPath,buf):#ץȡͼƬ�ĺ���
    addrImg=re.findall('http://.*?\.jpe?g|http://.*?\.png',buf)#ƥ��ͼƬ
    addrImg=list(set(addrImg))
    imagePath=makedr('images',new_htmlPath)
    for i in addrImg:
        getFile(i,imagePath)


opts,args=getopt.getopt(sys.argv[1:],'hd:u:o:')#���������в���
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
    while stopTime-startTime>=period:#����ѭ������
        startTime=time.time()
        jsNameNum=0  #�������������ڲ�js���ļ�����Ϊ�˷��㣬�ڲ���js�洢��Ϊ����0-n
        cssNameNum=0
        f=urllib2.urlopen(htmlUrl)
        buf=f.read()#ץȡ�ֻ��Ѻ�����ҳ
        new_htmlPath=makeFolder(htmlPath)#�½���ʱ����ص��ļ��У�����·��
        webGrab(buf,'%s\\souhu.html'%new_htmlPath,'w')#�洢html
        jsCode(new_htmlPath,buf)#�洢js
        cssCode(new_htmlPath,buf)#�洢css
        imagefile(new_htmlPath,buf)#�洢ͼƬ
    stopTime=time.time()


   
        
