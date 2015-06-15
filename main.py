import urllib2
import time
import os
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
path ='D:\\tmp\\backup\\'
title = dirname
new_path = os.path.join(path, title)
if not os.path.isdir(new_path):
    os.makedirs(new_path)
f=urllib2.urlopen(' http://m.sohu.com ')
buf=f.read()
out = open('%s\\souhu.html'%new_path,'w')
out.write(buf)
out.close()
