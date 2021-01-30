"""
Wikipedia bot
"""

import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse, GroupSearchResponse
import kik_unofficial.datatypes.peers as peers
import requests
import sepApi.sepapi
from sepApi.sepapi import SepEntry
from random import seed
import random
import wikiengine
import re
import plotter
import os
import time
from bs4 import BeautifulSoup
import nltk
import groups as group
import datetime
from wtapi import WiktionarySearch


username = 'borgean'
password = 'borgean'
floodcont = ('#debatemarket')
tocnumbers=[]
seed(1)
wikinum=0
wikiresult=''
roster= ['mboyt']
boldnums=['𝟭', '𝟮', '𝟯', '𝟰', '𝟱', '𝟲', '𝟳', '𝟴', '𝟵'] 
lastResponse=['','','']
imagelist=[]
flag=True
messagelist=[]
messages=[]
nouns = []
groups = []
users=[]
mentions = open("mentions","r")
for mention in mentions:
    users.append(mention.split(" "))
mentions.close()

for line in open("groupdb","r"):
    if line.startswith("_"):
        name, hash, jid = line.split(" ")
        name = name[1:]
        jid = jid[:-1]
        groups.append(group.Group(name,jid,hash))
    else:
        usr, body, date = line.split(" ", 2)
        date=date[:-1]
        groups[len(groups)-1].newMsg(body, usr, date)

def main():
    bot = EchoBot()

def clean(x):
	string = x
	search = re.search("<[^>]*>", string)
	if search:
		if search.span()[0]==0:
			string=string[search.span()[1]:]
			#print(string)
			return clean(string)
		else:
			string=string[:search.span()[0]]+string[search.span()[1]:]
			#print(string)
			return clean(string)
	else:
		return string

def arrTranslate(arr):
    for x in range(len(arr)-1):
        arr[x]=arr[x+1]
def msgTwist(message):
    newmsg=''
    flag=1
    if message!='':
        for letter in message:
            if flag:
                newmsg+=letter.lower()
                flag=0
            else:
                newmsg+=letter.upper()
                flag=1
    else:
        for letter in messagelist[8]:
            if flag:
                newmsg+=letter.lower()
                flag=0
            else:
                newmsg+=letter.upper()
                flag=1
    return newmsg
class EchoBot(KikClientCallback):

    def __init__(self):
        self.client = KikClient(self, username, password)
    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()
    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        if chat_message.body == "Unflood":
            flag = False
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))
        print("[+] Replaying.")
#self.client.send_chat_message(chat_message.from_jid, "You said \"" + chat_message.body + "\"!")
    def on_message_delivered(self, response: chatting.IncomingMessageDeliveredEvent):
        #print("[+] Chat message with ID {} is delivered.".format(response.message_id))
        pass
    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        #print("[+] Human has read the message with ID {}.".format(response.message_id))
        pass
    def on_group_search_response(self, response: GroupSearchResponse):
        print(response)

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        global lastResponse
        global messagelist
        #if chat_message.body.lower() == "members":
        #    msg=''
        #    for member in [x.jid == chat_message.group.jid for x in groups].members:
        #        msg += member+"\n"
        #    self.client.send_chat_message(chat_message.group_jid, msg[:-1])
        if chat_message.body.lower() == "groups":
            msg=''
            for grp in groups:
                msg += grp.ht+"\n"
            self.client.send_chat_message(chat_message.group_jid, msg[:-1])
        if chat_message.body.lower().startswith("ety "):
            query = chat_message.body[4:]
            ws = WiktionarySearch(query)
            if (ws.existe()):
                self.client.send_chat_message(chat_message.group_jid, ws.getEty())
            else:
                self.client.send_chat_message(chat_message.group_jid, "no")
        if chat_message.body.lower().startswith("group "):
            name, hashtag = chat_message.body[6:].split(" ")
            jid = chat_message.group_jid
            groups.append(group.Group(name, jid, hashtag))
        if chat_message.group_jid in [x.jid for x in groups]:
            g1 = list(filter(lambda x: x.jid == chat_message.group_jid, groups))[0]
            self.client.request_info_of_users(chat_message.from_jid)
            while lastResponse[0] != 'peerinfo':
                pass
            now = datetime.datetime.now()
            g1.newMsg(chat_message.body.replace(" ", "_"), lastResponse[1].split("(")[0][:-1].replace(" ", "_"), str(now.day)+"/"+str(now.month)+"/"+str(now.year)+" "+str(now.hour)+":"+str(now.minute))
            lastResponse=['','','']
            file = open("groupdb", "w")
            for gp in groups:
                file.write("_"+gp.name+" "+gp.ht+" "+gp.jid+"\n")
                for message in gp.messages:
                    file.write(message[0]+" "+"\""+message[1]+"\""+" "+message[2]+"\n")
            file.close()
        if chat_message.body.lower() == "messages":
            self.client.send_chat_message(chat_message.group_jid, str(list(filter(lambda x: x.jid == chat_message.group_jid, groups))[0].messages))
        # mention set
        if chat_message.body.lower().startswith("assign "):
            name, username = chat_message.body[7:].split(' ',1)
            if not ' ' in username:
                users.append([name,username])
                self.client.send_chat_message(chat_message.group_jid, "Assigned @"+name+" to "+username)
                mentions = open("mentions", "a")
                mentions.write(name+" "+username+"\n")
                mentions.close()
            else:
                self.client.send_chat_message(chat_message.group_jid, "Incorrect input.")
        # mention detector
        if "@" in chat_message.body:
            if len(chat_message.body[chat_message.body.find("@"):].split(" ")) == 1:
                mention = chat_message.body[chat_message.body.find("@")+1:]
            else:
                mention = chat_message.body[chat_message.body.find("@")+1:].split(" ")[0]
            if mention in [x[0] for x in users]:
                mentionusr = users[users.index(list(filter(lambda x: x[0]==mention, users))[0])][1]
                if mentionusr[-1] == "\n":
                    mentionusr = mentionusr[:-1]
                #self.client.send_chat_message(chat_message.group_jid, "detected a mention")
                self.client.request_info_of_users(chat_message.from_jid)
                while lastResponse[0] != 'peerinfo':
                    pass
                self.client.send_chat_message(self.client.get_jid(mentionusr), lastResponse[1].split("(")[0]+"in "+str(list(filter(lambda x: x.jid == chat_message.group_jid, groups))[0].name)+":\n"+"\""+chat_message.body+"\"")
                lastResponse = ['','']
            else:
                self.client.send_chat_message(chat_message.group_jid, "@"+mention+" not assigned.")
        if chat_message.body.lower().startswith("msgs "):
            if len(chat_message.body.split(" ")) == 2:
                self.client.send_chat_message(chat_message.group_jid, "You requested the list of occurences of the word "+chat_message.body.split(" ")[1])
            if len(chat_message.body.split(" ")) == 3:
                self.client.send_chat_message(chat_message.group_jid, "You requested the list of messages by "+chat_message.body.split(" ")[1]+" with the word "+chat_message.body.split(" ")[2])
                #messgs = list(filter(lambda x: x.jid == chat_message.group_jid, groups))[0].messages
        # topic detector
        for noun in open("nouns", "r"):
            for word in nltk.word_tokenize(chat_message.body.lower()):
                if noun[:-1] == word or nouns[:-1] == word:
                    print(word+" is a noun.")
                    if word in [x[1] for x in nouns]:
                        nouns[nouns.index(list(filter(lambda x: x[1]==word, nouns))[0])][0] += 1
                    else:
                        nouns.append([1, word]) 
        if chat_message.body.lower() == "topic":
            self.client.send_chat_message(chat_message.group_jid, str(nouns[nouns.index(list(filter(lambda x: x[0] == max([x[0] for x in nouns]), nouns))[0])]))
            
        if chat_message.body.lower() == "nouns":
            nounsstr=''
            for noun in nouns:
                nounsstr+=noun[1] + ": "+ str(noun[0])+"\n"
            self.client.send_chat_message(chat_message.group_jid, nounsstr)
        if len(messagelist) <= 10:
            messagelist.append(chat_message.body)
        else:
            arrTranslate(messagelist)
            messagelist[9] = chat_message.body
        print(chat_message.from_jid+" says: "+chat_message.body)
        #for verb in open("verbsList", "r"):
        #    if " "+verb[:-1]+" " in chat_message.body.lower():
        #        print(verb[:-1]+" is a verb.")
        if chat_message.body.lower().startswith("who up"):
            self.client.send_chat_message(chat_message.group_jid,  msgTwist(chat_message.body))
        if chat_message.body.lower() == "dum":
            newmsg = msgTwist('')
            self.client.send_chat_message(chat_message.group_jid, newmsg)
        if chat_message.body.lower() == "test":
            self.client.send_chat_message(chat_message.group_jid, "working")
            self.client.send_chat_message(chat_message.group_jid, chat_message.group_jid)
        if chat_message.body.startswith('jid'):
            self.client.send_chat_message(chat_message.group_jid, self.client.get_jid(chat_message.body[3:]))
        if chat_message.body.startswith("Request"):
            self.client.request_info_of_users(chat_message.body[7:])
        if chat_message.body.startswith("Clean"):
            for _ in range(int(chat_message.body[5:])):
                self.client.send_chat_message(chat_message.group_jid, cleanStr)
        if chat_message.body=="Quit":
            self.client.send_chat_message(chat_message.group_jid, "leaving then")
            self.client.leave_group(chat_message.group_jid)
# maths function plotter
        if chat_message.body.startswith("Plot "):
            self.client.send_chat_message(chat_message.group_jid, "Plotting " + chat_message.body[5:])
            plotter.plot(chat_message.body[5:])
            self.client.send_chat_image(chat_message.group_jid, "temporaryplot.png")
            os.remove("temporaryplot.png")
            os.remove("temporaryplot_send.png")    
# wolfram engine
        if chat_message.body.startswith("Wolf "):
            self.client.send_chat_message(chat_message.group_jid, "WolframAlpha not supported yet")
#image storer
        if chat_message.body.lower().startswith("store as "):
            global imagelist
            if "." in chat_message.body:
                name = chat_message.body[9:chat_message.body.find(".")]
                filename = name.lower()+chat_message.body[chat_message.body.find("."):]
            else:
                name = chat_message.body[9:]
                filename = name.lower()+".jpeg"
            imageurl = imagelist[len(imagelist)-1]
            image = open("images/"+filename, "wb")
            image.write(requests.get(imageurl).content)
            image.close()
            storelog = open("images/storelog.txt", "r+")
            storelog.write(name+" "+"images/"+filename+"\n")
            storelog.close()
            self.client.send_chat_message(chat_message.group_jid, "Stored image as "+name)
            
        if chat_message.body.lower() == "imagelist":
            head="images/storelog.txt\n\n"
            body='' 
            for line in open("images/storelog.txt"):
                body += str(line)
            self.client.send_chat_message(chat_message.group_jid, head+body )
#image retriever
        for line in open("images/storelog.txt"):
            if chat_message.body.lower() == line.split(" ",1)[0].lower():
                self.client.send_chat_image(chat_message.group_jid, line.split(" ",1)[1][:-1])
                os.remove(line.split(" ",1)[0]+"_send.jpg")
        if chat_message.body.lower() == "wiki":
            self.client.send_chat_message(chat_message.group_jid, "The 'Wiki' prefix interfaces Kik with Wikipedia\n\nCommands:\nWiki [query]\nRegular search, returns first paragraph.\n\nWiki [query] toc\nReturns table of contents, select a section with their number.\n\nWiki [query] \"[string]\"\nReturns list of occurrences. say 'Next' to browse it.")
###############################################################################################################################################
#sep api
        if chat_message.body.lower() == "sep":
            self.client.send_chat_message(chat_message.group_jid, "The 'sep' command interfaces Kik with the Stanford Encyclopedia of Philosophy\n\nCommands:\n\nSep [query]\nTries to find entry, if it doesn't it returns first 5 related results..\n\nSep s [query]\nReturns 5 first search results.")
        if chat_message.body.lower().startswith("sep "):                            # main sep
            output = ''
            if chat_message.body.lower().startswith("sep s "):                                      # sep search
                sep = SepEntry(chat_message.body[6:])
                output = 'First 5 results:\n\n'
                sep.setSearchList()
                for result in sep.searchList:
                    output += boldnums[result[0]-1]+". "+result[1]+"\n"
                print(sep.searchList)
                output = output[:-1]
                self.client.send_chat_message(chat_message.group_jid, output)
                lastResponse = ['sepList', sep, 5, sep.searchList, round(time.time())]
            else:                                                                                   # sep normal
                sep = SepEntry(chat_message.body[4:])
                if sep.setArticleSoup():
                    self.client.send_chat_message(chat_message.group_jid, sep.getFirstParagraph(1))
                    lastResponse = ['sepArt', sep, len(sep.toc), sep.toc, round(time.time())]
                else:
                    self.client.send_chat_message(chat_message.group_jid, "Didn't find an entry for "+sep.name+ ", related results:")
                    for result in sep.searchList:
                        output += boldnums[result[0]-1]+". "+result[1]+"\n"
                    output = output[:-1]
                    self.client.send_chat_message(chat_message.group_jid, output)
                    lastResponse = ['sepList', sep, 5, sep.searchList, round(time.time())]
                                                                                                    # interaction
        if lastResponse[0] == "sepList" and round(time.time())-lastResponse[4] < 90:                    # search, sepList interaction
            for num in range(5):
                if chat_message.body == str(num+1):
                    entry = lastResponse[3][num][2]
                    sep = SepEntry(entry)
                    sep.setArticleSoup()
                    self.client.send_chat_message(chat_message.group_jid, sep.getFirstParagraph(1))
                    lastResponse = ['sepArt', sep, len(sep.toc), sep.toc, round(time.time())]
        
        if lastResponse[0] == 'sepArt' and round(time.time())-lastResponse[4] < 90:                     # article, toc interaction
            if chat_message.body.lower() == "toc":                                                          #toc request
                self.client.send_chat_message(chat_message.group_jid, "You requested the table of contents for "+lastResponse[1].name)
                print(lastResponse[3])
                body = ''
                for section in lastResponse[3]:
                    body += section[1] + section[2] +"\n"
                self.client.send_chat_message(chat_message.group_jid, body)
                lastResponse = ['sepToc', lastResponse[1], lastResponse[2], lastResponse[3], round(time.time())]
        if lastResponse[0] == 'sepToc' and round(time.time())-lastResponse[4] < 90:
            for section in lastResponse[3]:                                                                 #toc select
                if chat_message.body == str(section[1][0]):
                    self.client.send_chat_message(chat_message.group_jid, "You selected "+section[2])
                    self.client.send_chat_message(chat_message.group_jid, str(lastResponse[1].getSection(int(chat_message.body))))
                    



                    
#########################################################################################################################################################

#wikipedia engine
        if chat_message.body.lower().startswith("wiki "):
            lastResponse
            global foundlist
            foundlist=[]
            global tocnumbers, toctexts, toc, soup, contents, req
            if "toc" in chat_message.body:
                req = chat_message.body[5:chat_message.body.find("toc")-1]
                contents, soup, toctexts, tocnumbers, toc, found = wikiengine.run(req)
            elif "\"" in chat_message.body:
                req = chat_message.body[5:chat_message.body.find("\"")-1]
                contents, soup, toctexts, tocnumbers, toc, found=wikiengine.run(req)
            else:
                req = chat_message.body[5:]
                contents, soup, toctexts, tocnumbers, toc, found=wikiengine.run(req)
            result=''
            # Format output
            if found:
                header = "Table of contents:\n"
            else:
                header = "'" + req + "' may refer to:\n"
            
            # indentation
            maxlen=0
            indentnum=0
            tabnum=0
            largest='^.'
            numhier=['^.$',]
            for x in tocnumbers:
                if len(x)>maxlen:
                    maxlen=len(x)
            indentnum = round(maxlen/2)
            for i in range(indentnum):
                largest += '\..'
                numhier.append(largest+'$')
            ################################################
            if found:
                for x in toc:
                    for i in numhier:
                        if re.match(i, x):
                            tabnum=round((round(len(i))-3)/3)
                            result+='\t'*tabnum + "(" + str(x) +")" + str(toc[x]) + "\n"
                result=result[:-1]
            else:
                if toc!=[]:
                    for x in range(len(contents)):
                        if x<len(contents)-1:
                            result+= str(contents[x+1][1]) + "\n"
                            for i in range(len(contents[x+1])):
                                if x+1<=len(contents[x+1]):
                                    result+='\t' + '(' + str(i+1) + ')' + clean(contents[x+1][2]) + '\n'
                    result=result[:-1]
                else:
                    print("No toc")
            ################################################
            if "toc" in chat_message.body and found:
                self.client.send_chat_message(chat_message.group_jid, header+result)
            elif "\"" in chat_message.body:
                searchstring = chat_message.body[chat_message.body.find("\"")+1:-1]
                for x in contents:
                    if searchstring.lower() in x[2].lower():
                        foundlist.append("..."+ x[2][x[2].lower().find(searchstring.lower())-150:x[2].lower().find(searchstring.lower())+150] +"...")
                self.client.send_chat_message(chat_message.group_jid,"Found '"+searchstring+"' "+str(len(foundlist))+" times.")
                self.client.send_chat_message(chat_message.group_jid, "First occurence (radius: 150):\n\n"+"'"+clean(foundlist[0])+"'")
                lastResponse = ['foundlist', [0,len(foundlist)], foundlist, round(time.time())]
                print(lastResponse)

            elif found:
                self.client.send_chat_message(chat_message.group_jid, contents[0])
            else:
                self.client.send_chat_message(chat_message.group_jid, header+result)
        if chat_message.body == "Next":
            if round(time.time())-lastResponse[3] < 90:
                if (lastResponse[0] == "paragraph"):
                    self.client.send_chat_message(chat_mesage.grop_jid, lastResponse[2][lastResponse[1]+1])
                    lastResponse[1]=lastResponse[1]+1
            if round(time.time())-lastResponse[3] < 90:
                if (lastResponse[0] == "foundlist"):
                        if (lastResponse[1][0]+1 < lastResponse[1][1]):
                            self.client.send_chat_message(chat_message.group_jid, clean(lastResponse[2][lastResponse[1][0]+1]))
                            lastResponse = ['foundlist', [lastResponse[1][0]+1, len(foundlist)], foundlist, round(time.time())]
                        else:
                            self.client.send_chat_message(chat_message.group_jid, "That's it.")

        if tocnumbers:
            for x in tocnumbers:
                if chat_message.body == x:
                    #self.client.send_chat_message(chat_message.group_jid, str(toctexts[tocnumbers.index(x)]))
                    for j in range(len(contents)):
                        if j+1<=len(contents):
                            if contents[j+1][0] == x:
                                try:
                                    self.client.send_chat_message(chat_message.group_jid, clean(contents[j+1][2]))
                                except:
                                    self.client.send_chat_message(chat_message.group_jid, "That paragraph is too long, maybe later.")
                if toctexts[tocnumbers.index(x)] in chat_message.body:
                    self.client.send_chat_message(chat_message.group_jid, str(toctexts[tocnumbers.index(x)]))
#################################
    def on_is_typing_event_received(self, response: chatting.IncomingIsTypingEvent):
        print("[+] {} is now {}typing.".format(response.from_jid, "not " if not response.is_typing else ""))
        
    def on_group_is_typing_event_received(self, response: chatting.IncomingGroupIsTypingEvent):
        print("[+] {} is now {}typing in group {}".format(response.from_jid, "not " if not response.is_typing else "",
                                                          response.group_jid))

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))
        for member in response.peer:
            roster += str(member)

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        #print("[+] Friend attribution request from " + response.referrer_jid)
        pass
    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        global imagelist
        print("[+] Image message was received from {}".format(image_message.from_jid))
        print(image_message.image_url)
        if len(imagelist)>=10:
            imagelist=[]
            imagelist.append(image_message.image_url)
        else:
            imagelist.append(image_message.image_url)
    def on_peer_info_received(self, response: PeersInfoResponse):
        global lastResponse
        print("[+] Peer info: " + str(response.users[0]))
        lastResponse = ['peerinfo', str(response.users[0])]

    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        print("[+] Status message in {}: {}".format(response.group_jid, response.status))

    def on_group_receipts_received(self, response: chatting.IncomingGroupReceiptsEvent):
        #print("[+] Received receipts in group {}: {}".format(response.group_jid, ",".join(response.receipt_ids)))
        pass

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        print("[+] Status message from {}: {}".format(response.from_jid, response.status))

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()

cleanStr = " \n \n "*200
