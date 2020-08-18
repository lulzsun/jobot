# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from fbchat import Client
from fbchat.models import *
import requests
#import cleverbotfree.cbfree
import time
import random
import json

# global vars
botAdmin_id = "<admin id>"
generalRecords = {}
poopRecords = {}
pointsRecords = {}

# random react event
nextEvent = time.time()
eventPrize = 0
eventId = 69

# trivia react event
triviaAnswer = 0
triviaPrize = 0
triviaId = 69

#cb = cleverbotfree.cbfree.Cleverbot()

def init():
    # Save the session
    with open('session.json', 'w') as f:
        json.dump(client.getSession(), f)

    thread_id = "518314794987940"
    thread_type = ThreadType.GROUP
    readRecords("general_records.txt", generalRecords)
    readRecords("poop_records.txt", poopRecords)
    readRecords("points_records.txt", pointsRecords)

    client.listen()

def readRecords(filename, record):
    print("Reading from " + filename + "...")
    file = open(filename,'r')

    for line in file:
        line = line.rstrip() # remove \n
        record[line.split('=')[0]] = line.split('=')[1]

    file.close()

def saveRecords(filename, record):
    print("Saving to " + filename + "...")
    file = open(filename,'w')
    newRecord = []

    for x, y in record.items():
        newRecord.append(x + '=' + y + '\n')
    
    file.writelines(newRecord) 
    file.close()

def whoAsked(message_object):
    keywords = ["i'm ", "i am", "i ", "im ", " me ", "i'll ", "my "]
    containsKeyword = any(ele in message_object.text.lower() for ele in keywords)
    if containsKeyword == True:
        if random.randrange(6) == 0:
            client.send(Message(text="ok but who asked?"), thread_id=thread_id, thread_type=thread_type)

def poopLeaderboard(message_object, uid):
    # create user's poop count
    if message_object.author not in poopRecords : # no records exist
        poopRecords[message_object.author] = "0" + "," + "0"
        
    # display poop leaderboard
    leaderboard = ""
    countRecord = {}

    for x, y in poopRecords.items():
        countRecord[x] = int(y.split(',')[0])

    sorted_countRecord = sorted(countRecord.items(), key=lambda x: x[1], reverse=True)
    
    leaderboard += ("POOP LEADERBOARD:\n")
    num = 1
    for i in sorted_countRecord: #print the top three
        leaderboard += "#" + str(num)
        leaderboard += " " + client.fetchUserInfo(i[0])[i[0]].first_name
        #leaderboard += " " + str(client.fetchUserInfo(i[0])[i[0]].last_name)[0] + "."
        leaderboard += " " + poopRecords[i[0]].split(',')[0] + "\n"
        num += 1
        if num == 4:
            break

    # add to user's poop count
    poops = int(poopRecords[message_object.author].split(',')[0])+1
    timestamp = float(poopRecords[message_object.author].split(',')[1]) 

    if timestamp+21600 > time.time():
        leaderboard += "...\n"
        leaderboard += "You had a poo recently (6hr cd), so it wont be counted.\n"
    else:
        leaderboard += "...\n"
        leaderboard += "Your poo has been recorded.\n"
        poopRecords[message_object.author] = str(poops) + "," + str(time.time())
        saveRecords("poop_records.txt", poopRecords)

    num = 1
    for i in sorted_countRecord:
        if i[0] == uid: #print the sender's place
            leaderboard += "#" + str(num)
            leaderboard += " " + client.fetchUserInfo(i[0])[i[0]].first_name
            #leaderboard += " " + str(client.fetchUserInfo(i[0])[i[0]].last_name)[0] + "."
            leaderboard += " " + poopRecords[i[0]].split(',')[0] + "\n"
            break
        num += 1

    client.send(Message(text=leaderboard), thread_id=thread_id, thread_type=thread_type)

def pointsLeaderboard(message_object, uid):
    # create user's points count
    if message_object.author not in pointsRecords : # no records exist
        pointsRecords[message_object.author] = "0"
        
    # display points leaderboard
    leaderboard = ""
    countRecord = {}

    for x, y in pointsRecords.items():
        countRecord[x] = int(y.split(',')[0])

    sorted_countRecord = sorted(countRecord.items(), key=lambda x: x[1], reverse=True)
    
    leaderboard += ("QBUCKS LEADERBOARD:\n")
    num = 1
    for i in sorted_countRecord: #print the top three
        leaderboard += "#" + str(num)
        leaderboard += " " + client.fetchUserInfo(i[0])[i[0]].first_name
        #leaderboard += " " + str(client.fetchUserInfo(i[0])[i[0]].last_name)[0] + "."
        leaderboard += " $" + pointsRecords[i[0]].split(',')[0] + "\n"
        num += 1
        if num == 4:
            break

    leaderboard += "...\n"

    num = 1
    for i in sorted_countRecord:
        if i[0] == uid: #print the sender's place
            leaderboard += "#" + str(num)
            leaderboard += " " + client.fetchUserInfo(i[0])[i[0]].first_name
            #leaderboard += " " + str(client.fetchUserInfo(i[0])[i[0]].last_name)[0] + "."
            leaderboard += " $" + pointsRecords[i[0]].split(',')[0] + "\n"
            break
        num += 1

    client.send(Message(text=leaderboard), thread_id=thread_id, thread_type=thread_type)

def addPoints(amount, uid):
    # create user's points count
    if uid not in pointsRecords : # no records exist
        pointsRecords[uid] = "0"

    points = int(pointsRecords[uid].split(',')[0])+int(amount)
    pointsRecords[uid] = str(points)
    saveRecords("points_records.txt", pointsRecords)

def createTrivia(category = None):
    global triviaPrize, triviaAnswer
    triviaPrize = random.randrange(60)
    message = ""
    if category == None:
        r = requests.get('https://opentdb.com/api.php?amount=1')
    elif "anime" in category:
        r = requests.get('https://opentdb.com/api.php?amount=1&category=31')
    elif "videogame" in category:
        r = requests.get('https://opentdb.com/api.php?amount=1&category=15')
    elif "sport" in category:
        r = requests.get('https://opentdb.com/api.php?amount=1&category=21')
    else: 
        r = requests.get('https://opentdb.com/api.php?amount=1')
    result = r.json()["results"][0]

    message += result["question"].replace("&quot;", "\"").replace("&#039;", "'") + "\n" + "\n"

    shuffledAnswers = result["incorrect_answers"]
    shuffledAnswers.append(result["correct_answer"])
    random.shuffle(shuffledAnswers)

    index = 0
    reactList = ["👍", "👎", "❤", "😆"]
    for answer in shuffledAnswers: 
        if answer == result["correct_answer"]:
            triviaAnswer = reactList[index]
        message += reactList[index] + " " + answer.replace("&quot;", "\"").replace("&#039;", "'") + "\n"
        index += 1

    print(result["type"], result["question"], triviaAnswer, shuffledAnswers)
    return client.send(Message(text=message), thread_id=thread_id, thread_type=thread_type)

class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if message_object.author != client.uid: # IF NOT THE BOT
            if whoAsked(message_object):
                return
            elif "kyle" in message_object.text.lower():
                client.send(Message(text="🧀", emoji_size=EmojiSize.LARGE), thread_id=thread_id, thread_type=thread_type)
                return
            elif [ele for ele in ["dog", "dawg"] if(ele in message_object.text.lower())]:
                client.sendLocalImage(
                    "1Rzqi6G.jpg",
                    message=Message(text=""),
                    thread_id=thread_id,
                    thread_type=thread_type,
                )
                return
            # elif "jobot" in message_object.text.lower():
            #     client.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
            #     response = cb.single_exchange(message_object.text.lower().replace("jobot", "cleverbot"))
            #     client.send(Message(text=response.replace("Cleverbot", "Jobot").replace("cleverbot", "Jobot")), thread_id=thread_id, thread_type=thread_type)
            #     client.setTypingStatus(TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)
            #     return
            elif message_object.text.startswith("!"): 
                commandStr = message_object.text[1:]
                args = commandStr.split(" ")

                if args[0] in ["qbucks", "qbuck", "qb", "money", "cash"]:
                    if(len(args) == 1):
                        pointsLeaderboard(message_object, author_id)
                    else:
                        user = client.searchForUsers(args[1])[0]
                        pointsLeaderboard(message_object, user.uid)
                elif args[0] == "roulette":
                    client.send(Message(text="Firing in 3"), thread_id=thread_id, thread_type=thread_type)
                    time.sleep(1)
                    client.send(Message(text="2"), thread_id=thread_id, thread_type=thread_type)
                    time.sleep(1)
                    client.send(Message(text="1"), thread_id=thread_id, thread_type=thread_type)
                    time.sleep(1)

                    if random.randrange(6) == 0:
                        addPoints(int(pointsRecords[author_id])*-1, author_id)
                        client.send(Message(text="💀💨🔫"), thread_id=thread_id, thread_type=thread_type)
                        deathMsg = client.fetchUserInfo(author_id)[author_id].first_name + " died playing russian roulette."
                        client.send(Message(text=deathMsg), thread_id=thread_id, thread_type=thread_type)
                        if botAdmin_id == author_id:
                            self.removeUserFromGroup(author_id, thread_id=thread_id)
                    else:
                        addPoints(15, author_id)
                        client.send(Message(text="😳🔫"), thread_id=thread_id, thread_type=thread_type)
                elif args[0] in ["poop", "flush", "crap"]:
                    if(len(args) == 1):
                        poopLeaderboard(message_object, author_id)
                    else:
                        user = client.searchForUsers(args[1])[0]
                        poopLeaderboard(message_object, user.uid)
                elif args[0] == "trivia":
                    global triviaId
                    if(len(args) == 1):
                        triviaId = createTrivia()
                    else:
                        triviaId = createTrivia(args[1].lower())
                elif args[0] == "help":
                    client.send(Message(text="!help yourself"), thread_id=thread_id, thread_type=thread_type)
                else:
                    client.send(Message(text="This command does not exist"), thread_id=thread_id, thread_type=thread_type)
        pass
    def onReactionAdded(self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs):
        global eventId, triviaId, triviaAnswer

        # Answering random event
        if eventId == mid and reaction == MessageReaction.HEART:
            rewardMsg = str(client.fetchUserInfo(author_id)[author_id].first_name) + " has redeemed " + str(eventPrize) + " qbucks."
            addPoints(eventPrize, author_id)
            client.send(Message(text=rewardMsg), thread_id=thread_id, thread_type=thread_type)
            eventId = 0

        # Answering trivia
        if triviaId == mid and reaction.value == triviaAnswer:
            rewardMsg = str(client.fetchUserInfo(author_id)[author_id].first_name) + " has redeemed " + str(triviaPrize) + " qbucks."
            addPoints(triviaPrize, author_id)
            client.send(Message(text=rewardMsg), thread_id=thread_id, thread_type=thread_type)
            triviaId = 0
        elif triviaId == mid and reaction.value != triviaAnswer:
            loseMsg = str(client.fetchUserInfo(author_id)[author_id].first_name) + " has failed the trivia question!\nCorrect answer is: " + triviaAnswer
            if int(pointsRecords[author_id]) - 20 < 0:
                addPoints(int(pointsRecords[author_id])*-1, author_id)
            else:
                addPoints(-20, author_id)
            client.send(Message(text=loseMsg), thread_id=thread_id, thread_type=thread_type)
            triviaId = 0
        pass
    def onMessageSeen(self, seen_by, thread_id, thread_type, seen_ts, ts, metadata, msg, **kwargs):
        global nextEvent, eventPrize, eventId
        if nextEvent < time.time():
            hour = random.randrange(4)
            eventPrize = random.randrange(40)
            nextEvent = time.time()+(hour*3600)
            eventId = client.send(Message(text="First one to heart react to this message gets " + str(eventPrize) + " qbucks."), thread_id=thread_id, thread_type=thread_type)
        pass

cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

# Attempt a login with the session, and if it fails, just use the email & password
client = CustomClient("<email>", "<password>", session_cookies=cookies)

# ... Do stuff with the client here
thread_id = "<id>"
thread_type = ThreadType.GROUP
init()

# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)