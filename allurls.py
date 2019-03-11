import bs4 as bs
import urllib2
from threading import Thread
from Queue import Queue
import gzip
import ssl
concurrent = 1200
s=1
def doWork():
    while True:
        url = q.get()
        urlstatus = getStatus(url)
        q.task_done()

def getStatus(myurl):
    context = ssl._create_unverified_context()
    files=myurl.replace(".", "_")
    files=files[8:]
    filename=files+".zip"
    print(filename)
    try:
        source = urllib2.urlopen(myurl,context=context,timeout=2).read()
        source=str(source)
        print(source)
        with gzip.open(filename, 'wb') as f:
            f.write(source)
    except:
        t=open("fail.txt","a+")
        t.write(myurl)
        t.write('\n')
        t.close() 

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    with open("a.txt") as infile:
        for line in infile:
            lin="https://"+line
            q.put(lin.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
