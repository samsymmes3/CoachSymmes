from requests_html import HTMLSession

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8'}

url_kingco2A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137155&depth=25"
url_kingco2A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137155&depth=25&gender=f"
url_kingco4A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137187&depth=25"
url_kingco4A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137187&depth=25&gender=f"

url_state4A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137183"
url_state4A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137183&gender=f"
url_state2A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137150"
url_state2A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137150&gender=f"

url_D32A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137156&depth=20"
url_D32A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137156&depth=20&gender=f"
url_D14A_boys = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137184&depth=20"
url_D14A_girls = "https://www.athletic.net/TrackAndField/Division/Top.aspx?DivID=137184&depth=20&gender=f"

session = HTMLSession()
r = session.request("get",url_kingco4A_girls,headers=hdr)

session2 = HTMLSession()
r2 = session2.request("get",url_D14A_girls,headers=hdr)

athletesIn = 4
athletesToShow = 16

with open("tempOutput.txt", "w") as f:
    f.write(r.text)

schoolName = "Skyline"
isGirls = True
includeRelays = True
isDistricts = False


outputFile = "boysKingcoOutput.html"
teamOutputFile = "boysKingcoTeamOutput.html"
if isGirls:
    outputFile = "girlsKingcoOutput.html"
    teamOutputFile = "girlsKingcoTeamOutput.html"

def ridSpace(a):
    toRet = ""
    for i in range(len(a)):
        if (a[i] >= "a" and a[i] < "z") or (a[i] >= "A" and a[i] <= "Z"):
            toRet = toRet + a[i]
    return toRet

class Team:
    name = ""
    nameNoSpace = ""
    score = 0
    scoreByCategory = []

    def __init__(self, initName):
        self.name = initName
        self.nameNoSpace = ""
        for i in range(len(initName)):
            if (initName[i] >= "a" and initName[i] < "z") or (initName[i] >= "A" and initName[i] <= "Z"):
                self.nameNoSpace = self.nameNoSpace + initName[i]
        self.score = 0
        self.scoreByCategory = [0, 0, 0, 0, 0]

    def addScore(self, num, category):
        self.score += num
        if category == "Sprints":
            self.scoreByCategory[0] += num
        elif category == "Distance":
            self.scoreByCategory[1] += num
        elif category == "Hurdles":
            self.scoreByCategory[2] += num
        elif category == "Throws":
            self.scoreByCategory[3] += num
        elif category == "Jumps":
            self.scoreByCategory[4] += num
        else:
            print("ERROR: Unknown Category")

    def __str__(self):
        return self.name + ": " + str(self.score)

class Event:
    name = ""
    shortHand = ""
    marks = []
    isRelay = False
    isGolfStyle = True
    category = ""

    def __init__(self, initName, initShortHand, initCategory, initIsRelay=False, initIsGolfStyle=True):
        self.name = initName
        self.shortHand = initShortHand
        self.marks = []
        self.isRelay = initIsRelay
        self.isGolfStyle = initIsGolfStyle
        self.category = initCategory

    def __str__(self):
        toRet = self.name + "\n"
        for i in range(len(self.marks)):
            toRet += str(self.marks[i]) + "\n"
        return toRet

class Mark:
    name = ""
    mark = ""
    team = ""

    def __init__(self, initName):
        self.name = initName
        self.mark = ""
        self.team = ""

    def __str__(self):
        temp = ""
        for i in range(len(self.mark)):
            if self.mark[i] == "<":
                break
            temp = temp + self.mark[i]
            if self.mark[i] == ">":
                temp = ""
        self.mark = temp
        return self.name + " - " + self.mark + " - " + self.team;

    def __gt__(self, x):
        markList = []
        markList2 = []
        curNum = ""
        for i in range(len(self.mark)):
            if (self.mark[i] >= "0" and self.mark[i] <= "9") or (self.mark[i] == "."):
                curNum = curNum + self.mark[i]
            else:
                if not (curNum == ""):
                    markList.append(float(curNum))
                curNum = ""
        if not (curNum == ""):
            markList.append(float(curNum))
        curNum = ""
        for i in range(len(x.mark)):
            if (x.mark[i] >= "0" and x.mark[i] <= "9") or (x.mark[i] == "."):
                curNum = curNum + x.mark[i]
            else:
                if not (curNum == ""):
                    markList2.append(float(curNum))
                curNum = ""
        if not (curNum == ""):
            markList2.append(float(curNum))
        if len(markList) > len(markList2):
            return True
        if len(markList) < len(markList2):
            return False
        for i in range(len(markList)):
            if markList[i] > markList2[i]:
                return True
            if markList[i] < markList2[i]:
                return False
        return False

    def __gte__(self, x):
        return not self < x

    def __lte__(self, x):
        return not self > x

    def __lt__(self, x):
        #print(self.mark)
        #print(x.mark)
        markList = []
        markList2 = []
        curNum = ""
        for i in range(len(self.mark)):
            if (self.mark[i] >= "0" and self.mark[i] <= "9") or (self.mark[i] == "."):
                curNum = curNum + self.mark[i]
            else:
                if not (curNum == ""):
                    markList.append(float(curNum))
                curNum = ""
        if not (curNum == ""):
            markList.append(float(curNum))
        curNum = ""
        for i in range(len(x.mark)):
            if (x.mark[i] >= "0" and x.mark[i] <= "9") or (x.mark[i] == "."):
                curNum = curNum + x.mark[i]
            else:
                if not (curNum == ""):
                    markList2.append(float(curNum))
                curNum = ""
        if not (curNum == ""):
            markList2.append(float(curNum))
        #print(markList)
        #print(markList2)
        if len(markList) > len(markList2):
            #print("here1")
            return False
        if len(markList) < len(markList2):
            #print("here2")
            return True
        for i in range(len(markList)):
            #print(markList[i])
            #print(markList2[i])
            if markList[i] > markList2[i]:
                #print("here3")
                return False
            if markList[i] < markList2[i]:
                #print("here4")
                return True
        #print("here5")
        return False

#temp = Mark("")
#temp.mark = "5:48.10"
#temp2 = Mark("")
#temp2.mark = "5:24.95"
#print(temp < temp2)

athleteStr = "/track-and-field\">"

startStr = "<body"
eventList = [
    Event("100 Meters", "100", "Sprints"),
    Event("200 Meters", "200", "Sprints"),
    Event("400 Meters", "400", "Sprints"),
    Event("800 Meters", "800", "Distance"),
    Event("1600 Meters", "1600", "Distance"),
    Event("3200 Meters", "3200", "Distance"),
    Event("110m Hurdles - 39\"", "110H", "Hurdles"),
    Event("300m Hurdles - 36\"", "300H", "Hurdles"),
    Event("Shot Put - 12lb", "Shot", "Throws", initIsGolfStyle=False),
    Event("Discus - 1.6kg", "Disc", "Throws", initIsGolfStyle=False),
    Event("Javelin - 800g", "Jav", "Throws", initIsGolfStyle=False),
    Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
    Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
    Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
    Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
];
if isGirls:
    eventList = [
        Event("100 Meters", "100", "Sprints"),
        Event("200 Meters", "200", "Sprints"),
        Event("400 Meters", "400", "Sprints"),
        Event("800 Meters", "800", "Distance"),
        Event("1600 Meters", "1600", "Distance"),
        Event("3200 Meters", "3200", "Distance"),
        Event("100m Hurdles - 33\"", "110H", "Hurdles"),
        Event("300m Hurdles - 30\"", "300H", "Hurdles"),
        Event("Shot Put - 4kg", "Shot", "Throws", initIsGolfStyle=False),
        Event("Discus - 1kg", "Disc", "Throws", initIsGolfStyle=False),
        Event("Javelin - 600g", "Jav", "Throws", initIsGolfStyle=False),
        Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
        Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
        Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
        Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
    ];
if includeRelays:
    eventList = [
        Event("100 Meters", "100", "Sprints"),
        Event("200 Meters", "200", "Sprints"),
        Event("400 Meters", "400", "Sprints"),
        Event("800 Meters", "800", "Distance"),
        Event("1600 Meters", "1600", "Distance"),
        Event("3200 Meters", "3200", "Distance"),
        Event("110m Hurdles - 39\"", "110H", "Hurdles"),
        Event("300m Hurdles - 36\"", "300H", "Hurdles"),
        Event("4x100 Relay", "4x1", "Sprints", True),
        Event("4x400 Relay", "4x4", "Sprints", True),
        Event("Shot Put - 12lb", "Shot", "Throws", initIsGolfStyle=False),
        Event("Discus - 1.6kg", "Disc", "Throws", initIsGolfStyle=False),
        Event("Javelin - 800g", "Jav", "Throws", initIsGolfStyle=False),
        Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
        Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
        Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
        Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
    ];
    if isGirls:
        eventList = [
            Event("100 Meters", "100", "Sprints"),
            Event("200 Meters", "200", "Sprints"),
            Event("400 Meters", "400", "Sprints"),
            Event("800 Meters", "800", "Distance"),
            Event("1600 Meters", "1600", "Distance"),
            Event("3200 Meters", "3200", "Distance"),
            Event("100m Hurdles - 33\"", "110H", "Hurdles"),
            Event("300m Hurdles - 30\"", "300H", "Hurdles"),
            Event("4x100 Relay", "4x1", "Sprints", True),
            Event("4x200 Relay", "4x2", "Sprints", True),
            Event("4x400 Relay", "4x4", "Sprints", True),
            Event("Shot Put - 4kg", "Shot", "Throws", initIsGolfStyle=False),
            Event("Discus - 1kg", "Disc", "Throws", initIsGolfStyle=False),
            Event("Javelin - 600g", "Jav", "Throws", initIsGolfStyle=False),
            Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
            Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
            Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
            Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
        ];

eventEndStr = "View full rankings"
athleteEndStr = "<"
started = False
inEvent = False
readingName = False
readingResult = False
startedResult = False
readingTeam = False
startedTeam = False
eventOn = 0
name = ""
i = 0
while True:
    i += 1
    if r.text[i:i + 5] == startStr:
        i += 4
        started = True
    if started:
        if inEvent:
            if readingTeam:
                if startedTeam:
                    if r.text[i] == "<":
                        #print("here 1")
                        startedTeam = False
                        readingTeam = False
                        if eventList[eventOn].isRelay:
                            readingResult = True
                    else:
                        eventList[eventOn].marks[-1].team = eventList[eventOn].marks[-1].team + r.text[i]
                elif r.text[i:i + 25] == "track-and-field-outdoor\">":
                    i += 24
                    #print("here 2")
                    startedTeam = True
            if readingResult:
                if eventList[eventOn].isRelay:
                    if r.text[i:i + 18] == eventEndStr:
                        i += 17
                        #print("here 7")
                        inEvent = False
                        readingResult = False
                        eventOn += 1
                        if eventOn == len(eventList):
                            print("done")
                            print("")
                            break
                if startedResult:
                    if r.text[i] == "<":
                        #print("here 3")
                        startedResult = False
                        readingResult = False
                        readingTeam = True
                    eventList[eventOn].marks[-1].mark = eventList[eventOn].marks[-1].mark + r.text[i]
                elif eventList[eventOn].isRelay:
                    #print("here")
                    if r.text[i:i + 10] == "/i></span>":
                        eventList[eventOn].marks.append(Mark(""))
                        i += 9
                        startedResult = True
                elif r.text[i:i + 13] == "href=\"/result":
                    i += 12
                    #print("here 4")
                    startedResult = True
            elif readingName:
                if r.text[i] == athleteEndStr:
                    eventList[eventOn].marks.append(Mark(name))
                    name = ""
                    #print("here 5")
                    readingName = False
                    readingResult = True
                else:
                    name = name + r.text[i]
            elif r.text[i:i + 18] == athleteStr:
                i += 17
                #print("here 6")
                readingName = True
            elif r.text[i:i + 18] == eventEndStr:
                i += 17
                #print("here 7")
                inEvent = False
                eventOn += 1
                if eventOn == len(eventList):
                    print("done")
                    print("")
                    break
        elif r.text[i:i + len(eventList[eventOn].name)] == eventList[eventOn].name:
            i += len(eventList[eventOn].name) - 1
            #print("here 8")
            inEvent = True
            if eventList[eventOn].isRelay:
                readingResult = True
            print(eventList[eventOn].name)

eventList2 = [
    Event("100 Meters", "100", "Sprints"),
    Event("200 Meters", "200", "Sprints"),
    Event("400 Meters", "400", "Sprints"),
    Event("800 Meters", "800", "Distance"),
    Event("1600 Meters", "1600", "Distance"),
    Event("3200 Meters", "3200", "Distance"),
    Event("110m Hurdles - 39\"", "110H", "Hurdles"),
    Event("300m Hurdles - 36\"", "300H", "Hurdles"),
    Event("Shot Put - 12lb", "Shot", "Throws", initIsGolfStyle=False),
    Event("Discus - 1.6kg", "Disc", "Throws", initIsGolfStyle=False),
    Event("Javelin - 800g", "Jav", "Throws", initIsGolfStyle=False),
    Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
    Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
    Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
    Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
];
if isGirls:
    eventList2 = [
        Event("100 Meters", "100", "Sprints"),
        Event("200 Meters", "200", "Sprints"),
        Event("400 Meters", "400", "Sprints"),
        Event("800 Meters", "800", "Distance"),
        Event("1600 Meters", "1600", "Distance"),
        Event("3200 Meters", "3200", "Distance"),
        Event("100m Hurdles - 33\"", "110H", "Hurdles"),
        Event("300m Hurdles - 30\"", "300H", "Hurdles"),
        Event("Shot Put - 4kg", "Shot", "Throws", initIsGolfStyle=False),
        Event("Discus - 1kg", "Disc", "Throws", initIsGolfStyle=False),
        Event("Javelin - 600g", "Jav", "Throws", initIsGolfStyle=False),
        Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
        Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
        Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
        Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
    ];
if includeRelays:
    eventList2 = [
        Event("100 Meters", "100", "Sprints"),
        Event("200 Meters", "200", "Sprints"),
        Event("400 Meters", "400", "Sprints"),
        Event("800 Meters", "800", "Distance"),
        Event("1600 Meters", "1600", "Distance"),
        Event("3200 Meters", "3200", "Distance"),
        Event("110m Hurdles - 39\"", "110H", "Hurdles"),
        Event("300m Hurdles - 36\"", "300H", "Hurdles"),
        Event("4x100 Relay", "4x1", "Sprints", True),
        Event("4x400 Relay", "4x4", "Sprints", True),
        Event("Shot Put - 12lb", "Shot", "Throws", initIsGolfStyle=False),
        Event("Discus - 1.6kg", "Disc", "Throws", initIsGolfStyle=False),
        Event("Javelin - 800g", "Jav", "Throws", initIsGolfStyle=False),
        Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
        Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
        Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
        Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
    ];
    if isGirls:
        eventList2 = [
            Event("100 Meters", "100", "Sprints"),
            Event("200 Meters", "200", "Sprints"),
            Event("400 Meters", "400", "Sprints"),
            Event("800 Meters", "800", "Distance"),
            Event("1600 Meters", "1600", "Distance"),
            Event("3200 Meters", "3200", "Distance"),
            Event("100m Hurdles - 33\"", "110H", "Hurdles"),
            Event("300m Hurdles - 30\"", "300H", "Hurdles"),
            Event("4x100 Relay", "4x1", "Sprints", True),
            Event("4x200 Relay", "4x2", "Sprints", True),
            Event("4x400 Relay", "4x4", "Sprints", True),
            Event("Shot Put - 4kg", "Shot", "Throws", initIsGolfStyle=False),
            Event("Discus - 1kg", "Disc", "Throws", initIsGolfStyle=False),
            Event("Javelin - 600g", "Jav", "Throws", initIsGolfStyle=False),
            Event("High Jump", "HJ", "Jumps", initIsGolfStyle=False),
            Event("Pole Vault", "PV", "Jumps", initIsGolfStyle=False),
            Event("Long Jump", "LJ", "Jumps", initIsGolfStyle=False),
            Event("Triple Jump", "TJ", "Jumps", initIsGolfStyle=False)
        ];

started = False
inEvent = False
readingName = False
readingResult = False
startedResult = False
readingTeam = False
startedTeam = False
eventOn = 0
name = ""
i = 0
while True:
    i += 1
    if r2.text[i:i + 5] == startStr:
        i += 4
        started = True
    if started:
        if inEvent:
            if readingTeam:
                if startedTeam:
                    if r2.text[i] == "<":
                        #print("here 1")
                        startedTeam = False
                        readingTeam = False
                        if eventList2[eventOn].isRelay:
                            readingResult = True
                    else:
                        eventList2[eventOn].marks[-1].team = eventList2[eventOn].marks[-1].team + r2.text[i]
                elif r2.text[i:i + 25] == "track-and-field-outdoor\">":
                    i += 24
                    #print("here 2")
                    startedTeam = True
            if readingResult:
                if eventList2[eventOn].isRelay:
                    if r2.text[i:i + 18] == eventEndStr:
                        i += 17
                        #print("here 7")
                        inEvent = False
                        readingResult = False
                        eventOn += 1
                        if eventOn == len(eventList2):
                            print("done")
                            print("")
                            break
                if startedResult:
                    if r2.text[i] == "<":
                        #print("here 3")
                        startedResult = False
                        readingResult = False
                        readingTeam = True
                    eventList2[eventOn].marks[-1].mark = eventList2[eventOn].marks[-1].mark + r2.text[i]
                elif eventList2[eventOn].isRelay:
                    #print("here")
                    if r2.text[i:i + 10] == "/i></span>":
                        eventList2[eventOn].marks.append(Mark(""))
                        i += 9
                        startedResult = True
                elif r2.text[i:i + 13] == "href=\"/result":
                    i += 12
                    #print("here 4")
                    startedResult = True
            elif readingName:
                if r2.text[i] == athleteEndStr:
                    eventList2[eventOn].marks.append(Mark(name))
                    name = ""
                    #print("here 5")
                    readingName = False
                    readingResult = True
                else:
                    name = name + r2.text[i]
            elif r2.text[i:i + 18] == athleteStr:
                i += 17
                #print("here 6")
                readingName = True
            elif r2.text[i:i + 18] == eventEndStr:
                i += 17
                #print("here 7")
                inEvent = False
                eventOn += 1
                if eventOn == len(eventList2):
                    print("done")
                    print("")
                    break
        elif r2.text[i:i + len(eventList2[eventOn].name)] == eventList2[eventOn].name:
            i += len(eventList2[eventOn].name) - 1
            #print("here 8")
            inEvent = True
            if eventList2[eventOn].isRelay:
                readingResult = True
            print(eventList2[eventOn].name)

def min(a, b):
    if a < b:
        return a
    return b

def getTeam(teamName, teamList):
    for i in range(len(teamList)):
        if teamName == teamList[i].name:
            return teamList[i]
    print("ERROR: No Team Found")

def isTeam(teamName, teamList):
    for i in range(len(teamList)):
        if teamName == teamList[i].name:
            return True
    return False

def sortTeams(a):
    if len(a) < 2:
        return a
    ref = a[0]
    lower = []
    higher = []
    for i in range(1, len(a)):
        if a[i].score > ref.score:
            higher.append(a[i])
        else:
            lower.append(a[i])
    higher = sortTeams(higher)
    lower = sortTeams(lower)
    toRet = []
    for i in range(len(higher)):
        toRet.append(higher[i])
    toRet.append(ref)
    for i in range(len(lower)):
        toRet.append(lower[i])
    return toRet

for event in eventList:
    print(event)

for event in eventList2:
    print(event)

for i in range(len(eventList)):
    on1 = 0
    on2 = 0
    newMarkList = []
    while on1 < len(eventList[i].marks) and on2 < len(eventList2[i].marks):
        if on1 == len(eventList[i].marks):
            newMarkList.append(eventList2[i].marks[on2])
        elif on2 == len(eventList2[i].marks):
            newMarkList.append(eventList[i].marks[on1])
        elif eventList[i].isGolfStyle:
            if eventList[i].marks[on1] < eventList2[i].marks[on2]:
                newMarkList.append(eventList[i].marks[on1])
                on1 += 1
            else:
                newMarkList.append(eventList2[i].marks[on2])
                on2 += 1
        else:
            if eventList[i].marks[on1] > eventList2[i].marks[on2]:
                newMarkList.append(eventList[i].marks[on1])
                on1 += 1
            else:
                newMarkList.append(eventList2[i].marks[on2])
                on2 += 1
    if isDistricts:
        eventList[i].marks = newMarkList

for event in eventList:
    print(event)

scoring = [10, 8, 6, 5, 4, 3, 2, 1]
teamScores = []

with open(teamOutputFile, "w") as f:
    leftAlign = 400
    #leftAlign = 570
    for event in eventList:
        leftAlign += 25
        if isGirls:
            f.write("<div style=\"top:395px;left:" + str(leftAlign) + "px;width:25px;position:fixed;\">\n")
        else:
            f.write("<div style=\"top:75px;left:" + str(leftAlign) + "px;width:25px;position:fixed;\">\n")
        f.write("<h6>" + event.shortHand + "</h6>\n")
        f.write("</div>\n")
        topAlign = 75
        if isGirls:
            topAlign = 395
        for i in range(min(len(event.marks), len(scoring))):
            topAlign += 25
            if isGirls:
                f.write("<div onmouseover=\"girlsHover(this)\" class=girlsBlock" + ridSpace(event.marks[i].team) + " style=\"top:" + str(topAlign) + "px;left:" + str(leftAlign) + "px\" ")
            else:
                f.write("<div onmouseover=\"boysHover(this)\" class=boysBlock" + ridSpace(event.marks[i].team) + " style=\"top:" + str(topAlign) + "px;left:" + str(leftAlign) + "px\" ")
            f.write("name=\"" + event.marks[i].name + "\" ")
            startEventName = event.name
            eventName = ""
            for idx in range(0, len(startEventName)):
                if startEventName[idx] == "-":
                    eventName = eventName[:-1]
                    break
                else:
                    eventName = eventName + startEventName[idx]
            f.write("event=\"" + eventName + "\" ")
            f.write("team=\"" + event.marks[i].team + "\" ")
            f.write("rank=\"" + str(i + 1) + "\" ")
            f.write("points=\"" + str(scoring[i]) + "\" ")
            f.write("mark=\"" + event.marks[i].mark + "\">\n")

            f.write("<h2>" + event.marks[i].team[0] + "</h2>\n")
            f.write("</div>\n")
            if not isTeam(event.marks[i].team, teamScores):
                teamScores.append(Team(event.marks[i].team))
            #getTeam(event.marks[i].team, teamScores).score += scoring[i]
            getTeam(event.marks[i].team, teamScores).addScore(scoring[i], event.category)

teamScores = sortTeams(teamScores)
mostPointsInCategories = [0, 0, 0, 0, 0]
numTeams = 10
inTop = False
for i in range(numTeams):
    if teamScores[i].name == schoolName:
        inTop = True
        break

for i in range(numTeams):
    for j in range(len(mostPointsInCategories)):
        if teamScores[i].scoreByCategory[j] > mostPointsInCategories[j]:
            mostPointsInCategories[j] = teamScores[i].scoreByCategory[j]

if not inTop:
    numTeams -= 2

with open(teamOutputFile, "a") as f:
    topAlign = 75
    if isGirls:
        topAlign = 395
    for team in teamScores:
        numTeams -= 1
        if numTeams < 0:
            break
        r = int(170 * (teamScores[0].score - team.score) / teamScores[0].score) + 10
        g = 190 - r
        b = 10
        rgbByCategory = []
        for i in range(len(mostPointsInCategories)):
            newR = int(170 * (mostPointsInCategories[i] - team.scoreByCategory[i]) / mostPointsInCategories[i]) + 10
            newG = 190 - newR
            newB = 10
            rgbByCategory.append([newR, newG, newB])
        topAlign += 25
        if isGirls:
            f.write("<div class=\"girlsBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        else:
            f.write("<div class=\"boysBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        f.write("left:200px;width:150px;height:25px;\">\n")
        f.write("<h2>" + team.name + "</h2>\n")
        f.write("</div>\n")
        if isGirls:
            f.write("<div class=\"girlsBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        else:
            f.write("<div class=\"boysBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        f.write("left:350px;width:50px;height:25px;background:rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ");\">\n")
        f.write("<h2 style=\"text-align:right\">" + str(team.score) + "</h2>\n")
        f.write("</div>\n")

        #for i in range(len(mostPointsInCategories)):
        #    if isGirls:
        #        f.write("<div class=\"girlsBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        #    else:
        #        f.write("<div class=\"boysBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
        #    f.write("left:" + str(405 + i * 35) + "px;width:35px;height:25px;background:rgb(" + str(rgbByCategory[i][0]) + ", " + str(rgbByCategory[i][1]) + ", " + str(rgbByCategory[i][2]) + ");\">\n")
        #    f.write("<h2 style=\"text-align:right\">" + str(team.scoreByCategory[i]) + "</h2>\n")
        #f.write("</div>\n")

        print(team)
    if not inTop:
        topAlign += 50
        for team in teamScores:
            if team.name == schoolName:
                r = int(170 * (teamScores[0].score - team.score) / teamScores[0].score) + 10
                g = 190 - r
                b = 10
                if isGirls:
                    f.write("<div class=\"girlsBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
                else:
                    f.write("<div class=\"boysBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
                f.write("left:200px;width:150px;height:25px;\">\n")
                f.write("<h2>" + team.name + "</h2>\n")
                f.write("</div>\n")
                if isGirls:
                    f.write("<div class=\"girlsBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
                else:
                    f.write("<div class=\"boysBlock" + team.nameNoSpace + "\" style=\"top:" + str(topAlign) + "px;")
                f.write("left:350px;width:50px;height:25px;background:rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ");\">\n")
                f.write("<h2 style=\"text-align:right\">" + str(team.score) + "</h2>\n")
                f.write("</div>\n")
                print(team)
                break

numTeams = len(teamScores) - 2
teamCount = -1

with open("extraCSS.html", "w") as f:
    for team in teamScores:
        if team.name == schoolName:
            continue
        teamCount += 1
        if isGirls:
            f.write(".girlsBlock" + team.nameNoSpace + "{")
        else:
            f.write(".boysBlock" + team.nameNoSpace + "{")
        shade = int(teamCount * 250 / numTeams)
        f.write("background: rgb(255, " + str(shade) + ", " + str(shade) + ");")
        f.write("position: fixed;")
        f.write("height: 25px;")
        f.write("width: 25px;")
        f.write("}")

class Athlete:
    name = ""
    results = ""

    def __init__(self, initName, initResults):
        self.name = initName
        self.results = initResults

    def __str__(self):
        toRet = "<h4>" + self.name + "</h4>\n"
        for i in range(len(self.results)):
            toRet = toRet + "<h5>"  + str(self.results[i]) + "</h5>\n"
        return toRet + "\n"

class Result:
    rank = 1
    event = None
    mark = ""

    def __init__(self, initRank, initEvent, initMark):
        self.rank = initRank
        self.event = initEvent
        self.mark = initMark

    def __str__(self):
        return self.event.name + " - " + str(self.rank) + " - " + self.mark

def addAthlete(athlete, list):
    for i in range(len(list)):
        if athlete.name == list[i].name:
            list[i].results.append(athlete.results[0])
            return
    list.append(athlete)

athleteList = []

with open(outputFile, "w") as f:
    for event in eventList:
        f.write("<h2>" + event.name + "</h2>\n")
        f.write("<h4>In</h4>\n")
        hasAthleteIn = False
        for i in range(min(athletesIn, len(event.marks))):
            if event.marks[i].team == schoolName:
                hasAthleteIn = True
                break
        if hasAthleteIn:
            for i in range(min(athletesIn, len(event.marks))):
                if event.marks[i].team == schoolName:
                    addAthlete(Athlete(
                        event.marks[i].name,
                        [
                            Result(
                                i + 1,
                                event,
                                event.marks[i].mark
                            )
                        ]
                    ),
                    athleteList)
                    f.write("<h5>" + str(i + 1) + " - " + event.marks[i].name + " - " + event.marks[i].mark + "</h5>\n")
        else:
            f.write("<h5>None</h5>\n")
        f.write("<h4>Cutoff</h4>\n")
        if len(event.marks) < athletesIn:
            f.write("<h5>-</h5>\n")
        else:
            f.write("<h5>" + event.marks[athletesIn - 1].mark + "</h5>\n")
        if len(event.marks) > athletesIn:
            hasAthleteInTheHunt = False
            for i in range(athletesIn, min(athletesToShow, len(event.marks))):
                if event.marks[i].team == schoolName:
                    hasAthleteInTheHunt = True
                    break
            if hasAthleteInTheHunt:
                f.write("<h4>In the Hunt</h4>\n")
                for i in range(athletesIn, min(athletesToShow, len(event.marks))):
                    if event.marks[i].team == schoolName:
                        addAthlete(Athlete(
                            event.marks[i].name,
                            [
                                Result(
                                    i + 1,
                                    event,
                                    event.marks[i].mark
                                )
                            ]
                        ),
                        athleteList)
                        f.write("<h5>" + str(i + 1) + " - " + event.marks[i].name + " - " + event.marks[i].mark + "</h5>\n")
        f.write("\n")

def nameComesBefore(name, ref):
    startIdxRef = 0
    startIdxName = 0
    for i in range(len(ref.name)):
        if ref.name[i] == " ":
            startIdxRef = i + 1
            break
    for i in range(len(name.name)):
        if name.name[i] == " ":
            startIdxName = i + 1
            break
    while startIdxRef < len(ref.name) and startIdxName < len(name.name):
        if name.name[startIdxName] < ref.name[startIdxRef]:
            return True
        elif name.name[startIdxName] > ref.name[startIdxRef]:
            return False
        startIdxName += 1
        startIdxRef += 1
    if startIdxRef < len(ref.name):
        return True
    if startIdxName < len(name.name):
        return False

    startIdxRef = 0
    startIdxName = 0
    while startIdxRef < len(ref.name) and startIdxName < len(name.name):
        if name.name[startIdxName] < ref.name[startIdxRef]:
            return True
        elif name.name[startIdxName] > ref.name[startIdxRef]:
            return False
        startIdxName += 1
        startIdxRef += 1
    if startIdxRef < len(ref.name):
        return True
    if startIdxName < len(name.name):
        return False
    return False

def sortAthletes(a):
    if len(a) < 2:
        return a
    ref = a[0]
    #print("Ref: " + ref.name)
    lower = []
    higher = []
    for i in range(1, len(a)):
        if nameComesBefore(a[i], ref):
            #print("Before: " + a[i].name)
            lower.append(a[i])
        else:
            #print("After: " + a[i].name)
            higher.append(a[i])
    lower = sortAthletes(lower)
    higher = sortAthletes(higher)
    toRet = []
    for i in range(len(lower)):
        toRet.append(lower[i])
    toRet.append(ref)
    for i in range(len(higher)):
        toRet.append(higher[i])
    return toRet

athleteList = sortAthletes(athleteList)

with open("individual_" + outputFile, "w") as f:
    for athlete in athleteList:
        f.write(str(athlete))























print("Done")
