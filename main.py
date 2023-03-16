import requests
import time
import json
import random
from threading import Thread
print("Please input the filename without the ending (.bp)")
filename = input("> ") + ".bp"
f = open(filename, "r")
fileall = f.read()
f.close()
project = []
fileln = fileall.split('\n')
for line in fileln:
    linelist = line.split(' ')
    if linelist[0] == "LOG":
        if linelist[1] == "TEXT":
            prtext = line.split(' ', 2)
            print("[LOG] " + prtext[2])
    if linelist[0] == "IFIN":
        prtext = line.split(';', 1)
        iftext = prtext[0].split(' ', 1)[1]
        saytext = prtext[1]
        project.append({"type":"ifin", "iftext":iftext, "saytext":saytext})
ignored =[]
ops = ["tjc472"]
#Loading config
f = open("config.json", "r")
jason = json.loads(f.read())
f.close()
debugon = "false"
ops = jason["ops"]
ignored = jason["banned"]
usrname = jason["username"]
accID = jason["accountid"]
passwrd = jason["password"]
levelID = jason["levelID"]
commentfetch = 3
debugon = jason["debug"]
ids = []
alreadyrun = False
lastsaid = ""

print("Configurated ")
def debugmsg(text):
    print(f"[Debug] {text}")
if debugon.lower() == "true":
    debugmsg("Debug mode enabled. Press ctrl + c for more options.")
def debug():
    global debugon
    debugshon = True
    print("\n[Debug] type 'return' to return to normal program function 'help' for help.")
    while debugshon:
        debugsh = input("[Debug] $ ").lower()
        if debugsh == "return":
            debugshon = False
        elif debugsh == "help":
            debugmsg("return, debug")
        elif debugsh == "debug":
            inp = input("[Debug] Turn debug mode on/off > ").lower()
            if inp == "on":
                debugon = "true"
            elif inp == "off":
                debugon = "false"
            else:
                debugmsg("Not a valid option! exiting function!")
while True:
    try:
        print("Connecting...")
        ids = []
        url = 'http://localhost/postComment'
        def say(text):
            global lastsaid
            x = requests.post(url, data={"username":usrname,"accountID":accID,"password":passwrd,"levelID":levelID,"percent":"0","comment":text})
            print(text)
            lastsaid = text
        url = 'http://localhost/postComment'
        while True:
            comments=requests.get("http://localhost/api/comments/"+levelID+"?count=3") # annoying issue, please dont make this very high.
            comments=json.loads((comments.text))
            jason["banned"] = ignored
            jason["ops"] = ops
            fi = open("config.json","w")
            fi.write(str(jason).replace("'",'"'))
            fi.close()
            for comment in range(0,3): #adjust this or it will crash
                comment1=dict(comments[comment])["content"]
                comment2=dict(comments[comment])
                #Debug testing
                if debugon.lower() == "true":
                    try:
                        comment1 = input("[Debug] Message > ")
                        comment2["ID"] = random.randint(1,100000)
                    except:
                        debug()
                if not comment2["ID"] in ids:
                    if not comment2["username"].lower() in ignored:
                        ids.append(comment2["ID"])
                        print(comment2["username"]+": "+comment1)
                        file = open("log.txt", "a")
                        file.write("\n"+comment2["username"]+": "+comment1)
                        file.close()
                        arguments = comment1.split(' ', 1)
                        for cmd in project:
                            if cmd["type"] == "ifin":
                                if cmd["iftext"].lower() in comment1.lower() and not comment2["username"]==usrname:
                                    say(cmd["saytext"].format(comment2["username"], random.randint(1,100)))
                        #if "/help" in comment1.lower() and not comment2["username"]==usrname:
                        #    say("@"+comment2["username"]+" Commands: /furry /ai /cool /yesorno /say /oplist /banlist /stats /help")
                        #    print("command /help")
            if not debugon.lower() ==  "true":
                time.sleep(2) # Make the bot check every 2 seconds instead, You shouldnt be ratelimited.
    except:
        try:
            print("Press Ctrl + C in 5 seconds for menu")
            time.sleep(5)
        except:
            sel = input("[Menu] 'exit' to exit, 'shell' for debug shell > ").lower()
            if sel == "exit":
                break
            elif sel == "shell":
                debug()
            else:
                print("[Menu] Invalid selection! Returning!")
print("Saving New Config...")
try:
    fi = open("config.json","w")
    fi.write(str(jason).replace("'",'"'))
    fi.close()
    print("Success!")
except:
    print("Failed!")
