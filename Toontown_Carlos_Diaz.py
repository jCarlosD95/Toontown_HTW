#Toontown Game
from PyQt5 import QtCore, QtGui, QtWidgets

from random import randint
import Map_rc
import sys

####################
####################
class Place(object):
    def __init__(self, name):

    
        #A string containing the place's name
        self.name = name
            
        #List of adjacent places
        self.places = []


        #Toons can warp to a playground.
        #If it's a playground, set to true.
        self.canWarp = True

    #Adds another place to this places list of adjacent places
    #and adds this place to ITS list of adjacent places, as well.
    #######################
    def setAdj(self, place):
        self.places.append(place)
        
        if self not in place.places:
            place.setAdj(self)


#############################
###     End Place Class
##############################

#Technically, Street or CogHQ.
####################
####################
class Street(Place):
    def __init__(self, name):
        Place.__init__(self, name)
        #Can't warp to streets
        self.canWarp = False

        #Booleans indicate the presence of these 3 entitites
        self.banana = False
        self.hole = False
        self.cog = False
        
#############################
###     End Street Class
##############################
        
###################       
###################
class Toon(object):
    def __init__(self, loc):

        #Loc is location. Set to Toontown Central upon initialization.
        self.loc = loc
        self.pies = 5

    def walk_to(self,place,browser):
        #If the place is adjacent to player's location, go there
        if place in self.loc.places:
            self.loc = place
            browser.append("You walk through the tunnel to " + place.name + ".")
        
            #If it's not a playground, check for Banana, hole, or cog
            if place.canWarp == False:

                if place.cog == True:

                    #If the player is in a Cog HQ, move them to the adjacent place
                    if len(place.places) == 1:
                        self.loc = place.places[0]

                    #If the player isn't already in a playground (as they would be if they
                    #had been at the Cog HQ by Acorn Acres), send them to the playground
                    if place.canWarp == False:
                        if place.places[0].canWarp == True:
                            self.loc = place.places[0]
                        else:
                            self.loc = place.places[1]

                    browser.append("\nYou wandered right into the cog!\n"
                           "The terrifying monstrosity tortures you with "
                           "an interminable sermon on synergy, "
                           "sending your depressed erierre right on over to " + self.loc.name +  "."

                    "\n\nYou lost a pie in all the commotion!\n")

                    lossCheck = self.pieLoss(browser)

                    if lossCheck == "gameOver":
                        return "gameOver"
                    else:
                        return "shuffleCog"

                if place.hole == True:
                    browser.append("\nThere was a hole on this street! You stumble into it...\n"
                         "And land right in front of your house, of all places!\n"
                         "It's getting late anyway, so you might as well head off to bed.\n"
                         "Goodnight!"
                          "\n\nYOU LOSE...")

                    return "gameOver"
                
                if place.banana == True:                 
                    browser.append("\nYou slip on a banana peel and bonk your noggin!"
                    "When you come to, one of your pies is splattered on the ground. Also, so much"
                    "time has passed that the holes and banana peels have somehow moved!")
                    lossCheck = self.pieLoss(browser)

                    if lossCheck == "gameOver":
                        return "gameOver"
                    else:
                        return "banana"
              
        else:
            print("You can't go there!")

    #######################        
    def warp_to(self, place, browser):
        if place.canWarp == True:
            self.loc = place
            browser.append("You slap a portable hole onto the ground and hop down into " + place.name + ".")
        else:
            browser.append("You can't go there!")

    #Makes toon throw pie
    #######################
    def throw_pie(self, place, browser):
        if place in self.loc.places:
            #If you can warp there, it's a playground and there's no cog
            if place.canWarp == False and place.cog == True:
                place.cog = False
                browser.append("You throw the pie into " + place.name + " ... AND HIT!")
                browser.append("You hear a cog stutter, spasm, and explode!")
                browser.append("A single, solitary gear rolls out of the tunnel, bumps into your shoe, and falls on its side.\n")


                browser.append("YOU WIN!!!!")
                return "Winner"
            else:
                browser.append("You throw the pie into " + place.name + " ...AND MISS!")
                browser.append("Guess there was no cog there, after all.\n")
                return self.pieLoss(browser)

        else:
            browser.append("Whoa there, buddy! That's too far to throw a pie!\n")
            return False

    #Outputs location and pie count
    ################################
    def look(self):
        return ("\nYou are at " + self.loc.name + "."
        "\nYou have " + str(self.pies) + " pies left.\n")

    #Parses user input into commands
    #Pdict is the allPlaces dictionary
    #browser is the text browser, self.gameHistory
    #string is the command string
    #################################
    def command(self, string, pdict, browser):
        #Formatting input
        s = " "
        string = string.split()

        #Capitalize every word.
        #This way, "the Brrrgh" and "daisy gardens" are recognized.
        for _ in range(len(string)):
            string[_] = string[_].capitalize()
            
        if len(string) == 0:
            browser.append("To pass the time, you sit and do nothing.")

##        elif string[0].isdigit():
##            return self.walk_to(self.loc.places[int(string[0])-1], browser)

        elif string[0] == "Look":
            browser.append(self.look())

        elif string[0] == "Help":
            browser.append(helpme())
        else:

            #if the player submits a digit, turn that digit into a place in Toontown
            #corresponding to one of the numbers they are given as a potential place to go
            if string[-1].isdigit():
                if int(string[-1]) <= len(self.loc.places):
                    name = self.loc.places[int(string[-1])-1].name.split()
                    string.pop(-1)
                    string.append(name[0])
                    string.append(name[1])

            #Here's where walking, throwing pies, and moving are implemented       
            if len(string) > 1:
                if len(string) == 2 or string[1] == "To":
                    dest = s.join(string[-2:])

                    if dest in pdict:
                        if pdict[dest] in player.loc.places:
                            return self.walk_to(pdict[dest], browser)
                        else:
                            return self.warp_to(pdict[dest], browser)
                    else:
                        browser.append("Uh, I don't think that's in Toontown.")
                        
                elif s.join(string[:3]) == "Throw Pie Into":
                    
                    dest = s.join(string[-2:])
                    if dest in pdict:
                        return self.throw_pie(pdict[dest], browser)
                    else:
                        browser.append("Uh, I don't think that's in Toontown.")

                else:
                    browser.append("Uh, sorry pal, was that even English?")

            else:
                browser.append("Uh, what does that mean?")
                

                
            
##      elif len(string) > 1 and string[1] == "to":
##         dest = s.join(string[2:])
##             if dest in pdict
##                 if pdict[dest] in self.loc.places:
##
##                else:
##                    return self.warp_to(pdict[dest], browser)
##            else:
##                browser.append("Uh, I don't think that's in Toontown.")

            
##        #If Baritone is 3, this supports throw pie into 3 or throw pie into Baritone Boulevard             
##        elif len(string) > 1 and s.join(string[:3]) == "Throw Pie Into":
##            dest = s.join(string[3:])
##            if dest in pdict:
##                return self.throw_pie(pdict[dest], browser)
##            else:
##                browser.append("Uh, I don't think that's in Toontown.")
                
                    
        

    #Checks for the "out of pies" lose condition
    ############################################
    def pieLoss(self, browser):
        self.pies -=1
        if self.pies <= 0:
            browser.append("Oops! You're out of pies! Can't hunt cogs without gags!")
            browser.append("Oh well, it's getting late. Might as well go home for the day.")

            browser.append("YOU LOSE...")

            return "gameOver"
        else:
            return "Alive"
            
#############################
###     End Toon Class
##############################



#Puts all places into one dictionary
####################################
def setDict(pdict, place):
    if place.name not in pdict:
        pdict[place.name] = place

        for x in place.places:
            setDict(pdict, x) 

#Puts items into places
#pdict: dictionary of places
#justCog: A bool. True if you're just shuffling the cog's location.
    #False if you want to place holes and bananas.
#######################
def putItems(pdict, currentCog = None, justCog = False, justItems = False):
    #Create list copy for modification
    plist = list(pdict.values())

    
    #Remove all playgrounds
    playgrounds = []
    for _ in plist:
        if _.canWarp == True:
            plist.remove(_)

    if justItems == False:
        #Add cog in random Street
        if not currentCog == None:
            currentCog.cog = False
        x = randint(0,len(plist)-1)
        plist[x].cog = True
        cogLoc = plist[x]       #Cog location

    if justCog == False:
    #Remove streets before CogHQs because
    #A peel or a hole there would be unavoidable.
        plist.remove(pdict["Oak Street"])
        plist.remove(pdict["Polar Place"])
        plist.remove(pdict["Pajama Place"])

        #Erase current holes and bananas
        for _ in plist:
            _.banana = False
            _.hole = False
    
        #Add holes
        for _ in range(0,3):
            x = randint(0,len(plist)-1)
            if plist[x].hole == False:
                plist[x].hole = True
                plist.pop(x)

                
        #Add peels
        for _ in range(0,3):
            x = randint(0,len(plist)-1)
            if plist[x].banana == False:
                plist[x].banana = True
                plist.pop(x)
                
    if justItems == False:
        return cogLoc

#Return a random cog quote
##################
def cogQuotes():
    x = randint(1,3)

    if x == 1:
        return "Somewhere nearby, a soulless, metallic voice rasps, \"Proffiiit marginsssss.\""

    if x == 2:
        return "You get the sickening feeling that something nearby is managing its stock portfolio."

    if x == 3:
        return "From seemingly all directions, you hear a voice drone:\n\"Marketing reseaaaarrrch. JOIN THE SAMPLE DATAAAAA!!!\n"

        
#Print Instructions   
#################
def helpme():
    return("\n"
            "********************************************************"
            "\n     Welcome to Toontown!"
            "\n"
            "\n     Be alert: A terrifying MECHA-COG lurking in our streets!"
            "\n"
            "\n     If you want to strut the streets of Toontown in safety, listen to these "
            "vital tips!"
            "\n"
            "\n     To go to an ADJACENT PLACE, type its corresponding number. To warp to "
            "any PLAYGROUND, type \"go to (playground name).\" "
            "\n"
            "\n     Don't forget correct capitalization and spelling."
            "\n"
            "\n     Also, Chip 'n Dale's Acorn Acres has been shortened to Acorn Acres."
            "\n"
            "\n     Be careful: The cog has caused a power outage. You're flying blind, here! "
            " BANANA PEELS and PORTABLE HOLES litter the streets. Make sure you avoid streets"
            " where you think these are located."
            "\n"
            "\n     If you fall into a HOLE, you'll end up who-knows-where, and your adventure"
            " is over!"
            "\n"
            "\n     If you slip on a BANANA PEEL, you'll bonk your head and when you wake up,"
            " the holes and banana peels will have changed locations. Plus, you'll have"
            " DROPPED one of your PIES!"
            "\n"
            "\n      You might even find a...*gulp*...hole on your street!"
            "\n"
            "\n      And if you run into the big, bad MECHA-COG itself...well..."
            " He'll send you sobbing right back to the NEAREST PLAYGROUND!"
            "\n"
            "\n      What's worse, the cog will RUN AND HIDE, and you'll have to start your"
            " search all over again!"
            "\n"
            "\n      But don't worry; you may be blind, but you can use CLUES to figure out"
            " what's nearby.\n"
            "\n"
            "If you FEEL A DRAFT, you know there's a hole on an adjacent street or Cog HQ.\n"
            "\n"
            "If you SMELL BANANAS, you know there's a BANANA PEEL on an adjacent street or"
            "Cog HQ.\n"
            "\n"
            "And if a COG is nearby...well...you'll know. Trust me."
            "\n"
            "\n     Also, if you forget where you are, just type \"look around\" to look"
            " around or to see how many pies you have left."
            "\n"
            "\n      But you're not helpless. If you think a cog is nearby, you can THROW A"
            " PIE at it to smash it to smithereens! Just type \"throw pie into (street)\" to"
            " throw a pie into an adjacent street. If your deduction skills are sharp, you'll"
            " have thrown the pie onto the street with the cog and hit him! We've given you"
            " FIVE state-of-the-art heavy-artillery super-pies. Just one well-placed pie"
            " should be enough to take even this mecha-cog down! But be careful. You only have"
            " have 5 pies, so make sure you know which of the adjacent streets the cog is on."
            "\n"
            "\n      Oh, one more thing: The cog moves around."
            "\n"
            "\n      Yep. That's right. Every few steps you take, the cog will move to a space"
            " adjacent to it. It CAN'T ENTER PLAYGROUNDS though, so it can't go very far."
            " Unless, of course, the cog CATCHES YOU and MAKES YOU SAD. Then it could be on"
            " ANY STREET."
            "\n"
            "\n      If you forget any of this, just type \"help\" and this message will repeat."
            "\n"
            "\n      Well, that's it! The fate of Toontown is in your hands. Good luck!"
            "\n"
            "\n********************************************************"
            "\n")
#Coordinates for the places on the map
def locations(place):
    if place == TTC:
        return (160, 360)
    elif place == LoopyLane:
        return(90, 310)
    elif place == PunchlinePlace:
        return (310, 420)
    elif place ==SillyStreet:
        return(160, 490)
    elif place == Speedway:
        return(60, 430)
    elif place == DG:
        return(260, 590)
    elif place == ElmStreet: 
        return(290, 500)
    elif place == OakStreet:
        return(120, 580)
    elif place == MapleStreet:
        return(400, 560)
    elif place == SellHQ:
        return(20, 570)
    elif place == DonDock:
        return(540, 390)
    elif place == BarnacleBlvd:
        return(420, 360)
    elif place == SeaweedStreet:
        return(420, 450)
    elif place == LighthouseLane:
        return(570, 290)
    elif place == AA:
        return(510, 500)
    elif place == BossHQ:
        return(560, 570)
    elif place == TB:
        return(430, 160)
    elif place == WalrusWay:
        return(550, 170)
    elif place == SleetStreet:
        return(420, 260)
    elif place == PolarPlace:
        return(450, 60)
    elif place == LawHQ:
        return(550, 50)
    elif place == MM:
        return(160, 170)
    elif place == BaritoneBlvd:
        return(270, 230)
    elif place == AltoAvenue:
        return(110, 240)
    elif place == TenorTerrace:
        return(260, 110)
    elif place == DonDream:
        return(40, 50)
    elif place == LullabyLane:
        return(160, 60)
    elif place == PajamaPlace:
        return(40, 120)
    elif place == CashHQ:
        return(20, 210)

    
##########################
##  Begin Making of Map ##
##########################
TTC = Place("Toontown Central")
LoopyLane = Street("Loopy Lane")
PunchlinePlace = Street("Punchline Place")
SillyStreet = Street("Silly Street")
Speedway = Place("Goofy Speedway")

TTC.setAdj(LoopyLane)
TTC.setAdj(PunchlinePlace)
TTC.setAdj(SillyStreet)
TTC.setAdj(Speedway)

#Done: TTC

DG = Place("Daisy Gardens")
ElmStreet = Street("Elm Street")
OakStreet = Street("Oak Street")
MapleStreet = Street("Maple Street")
SellHQ = Street("Sellbot HQ")

DG.setAdj(ElmStreet)
DG.setAdj(OakStreet)
DG.setAdj(MapleStreet)
OakStreet.setAdj(SellHQ)

ElmStreet.setAdj(SillyStreet)
#Done: DG

DonDock = Place("Donald Docks")
BarnacleBlvd = Street("Barnacle Boulevard")
SeaweedStreet = Street("Seaweed Street")
LighthouseLane = Street("Lighthouse Lane")
AA = Place("Acorn Acres")
BossHQ = Street("Bossbot HQ")

DonDock.setAdj(BarnacleBlvd)
DonDock.setAdj(SeaweedStreet)
DonDock.setAdj(LighthouseLane)
DonDock.setAdj(AA)
AA.setAdj(BossHQ)

SeaweedStreet.setAdj(MapleStreet)
BarnacleBlvd.setAdj(PunchlinePlace)
#Done: DonDock

TB = Place("The Brrrgh")
WalrusWay = Street("Walrus Way")
SleetStreet = Street("Sleet Street")
PolarPlace = Street("Polar Place")
LawHQ = Street("Lawbot HQ")

TB.setAdj(WalrusWay)
TB.setAdj(SleetStreet)
TB.setAdj(PolarPlace)
PolarPlace.setAdj(LawHQ)

WalrusWay.setAdj(LighthouseLane)

#Done: TB

MM = Place("Minnie's Melodyland")
BaritoneBlvd = Street("Baritone Boulevard")
AltoAvenue = Street("Alto Avenue")
TenorTerrace = Street("Tenor Terrace")

MM.setAdj(TenorTerrace)
MM.setAdj(AltoAvenue)
MM.setAdj(BaritoneBlvd)

AltoAvenue.setAdj(LoopyLane)
BaritoneBlvd.setAdj(SleetStreet)
#Done: MM

DonDream  = Place("Donald's Dreamland")
LullabyLane = Street("Lullaby Lane")
PajamaPlace = Street("Pajama Place")
CashHQ = Street("Cashbot HQ")

DonDream.setAdj(LullabyLane)
DonDream.setAdj(PajamaPlace)
PajamaPlace.setAdj(CashHQ)

LullabyLane.setAdj(TenorTerrace)
##########################
##  End Making of Map   ##
##########################


#Create a dicitonary where each place is a value
#and its name is its key
placeDict = dict()              #Empty dictionary
setDict(placeDict, TTC)         #Function to fill dictionary

#Adds cogs, banana peels, holes
#Also save location of cog to cogLoc
#Create the player
player = Toon(TTC)

###############################################
####            Gui Stuff
###############################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Carlos Diaz\Documents\Jobs\Toontown\Toontown Display.ui'
#
# Created by: PyQt5 UI code generator 5.11.3

class Ui_HuntTheWumpusbot(object):
    def setupUi(self, HuntTheWumpusbot):
        HuntTheWumpusbot.setObjectName("HuntTheWumpusbot")
        HuntTheWumpusbot.resize(1142, 650)

        #set silly font
        font = QtGui.QFont()
        font.setFamily("Snap ITC")
        HuntTheWumpusbot.setFont(font)

        #The main widget
        self.SuperWidget = QtWidgets.QWidget(HuntTheWumpusbot)
        self.SuperWidget.setObjectName("SuperWidget")

        #The line edit bar
        self.cmdEnter = QtWidgets.QLineEdit(self.SuperWidget)
        self.cmdEnter.setGeometry(QtCore.QRect(650, 610, 351, 31))
        self.cmdEnter.setInputMask("")
        self.cmdEnter.setObjectName("cmdEnter")

        #The text browser showing the game
        self.gameHistory = QtWidgets.QTextBrowser(self.SuperWidget)
        self.gameHistory.setGeometry(QtCore.QRect(650, 10, 481, 591))
        self.gameHistory.setObjectName("gameHistory")

        #The "enter command" button
        self.pushButton = QtWidgets.QPushButton(self.SuperWidget)
        self.pushButton.setGeometry(QtCore.QRect(1010, 610, 121, 31))
        self.pushButton.setObjectName("pushButton")

        #Turn the Button Red
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 66, 66))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 66, 66))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)

        self.pushButton.setPalette(palette)
        self.pushButton.setAutoFillBackground(True)
        self.pushButton.setFlat(True)


        #Where the map of Toontown is displayed
        self.ttMap = QtWidgets.QLabel(self.SuperWidget)
        self.ttMap.setGeometry(QtCore.QRect(10, 10, 630, 630))
        self.ttMap.setText("")
        self.ttMap.setTextFormat(QtCore.Qt.PlainText)
        self.ttMap.setPixmap(QtGui.QPixmap(":/newPrefix/ToontownWumpus/ToontownMap.png"))
        self.ttMap.setScaledContents(True)
        self.ttMap.setObjectName("ttMap")

        #My toon's head, which I reluctantly severed for the glory of this project
        self.toonIcon = QtWidgets.QLabel(self.SuperWidget)
        self.toonIcon.setGeometry(QtCore.QRect(160, 360, 71, 61))
        self.toonIcon.setText("")
        self.toonIcon.setPixmap(QtGui.QPixmap(":/newPrefix/ToontownWumpus/Toon Head.png"))
        self.toonIcon.setScaledContents(True)
        self.toonIcon.setProperty("myHead", QtGui.QPixmap("Toon Head.png"))
        self.toonIcon.setObjectName("toonIcon")
        HuntTheWumpusbot.setCentralWidget(self.SuperWidget)

        self.retranslateUi(HuntTheWumpusbot)
        QtCore.QMetaObject.connectSlotsByName(HuntTheWumpusbot)

        #Connecting the "enter" button to submission of data
        self.pushButton.clicked.connect(lambda: self.getText())
        self.pushButton.setAutoDefault(True)

        self.cmdEnter.returnPressed.connect(self.pushButton.click)

        #Adds cogs, banana peels, holes
        #Also save location of cog to whereCog
        self.whereCog = putItems(placeDict)

        #Number of turns that have passed
        self.turns = 0

        #True until the toon pies the cog
        self.cogAlive = True

        #Used to read game state
        self.situation = ""


    #Lists the paths the toon can take
    #Also lists nearby obstacles
    #######################
    def paths(self):
        string = ""
        for _ in range (len(player.loc.places)):
            string += (str(_+1) + ") " + player.loc.places[_].name + "\n")
        self.gameHistory.append("\nYou can go to:\n" + string + "Or to any playground, of course!\n")

        cogNearby = False
        holeNearby = False
        bananaNearby = False
                
        #Say whether cog, hole, or banana is nearby.
        for _ in player.loc.places:
            if isinstance(_, Street):
                if _.cog == True:
                    cogNearby = True
                if _.hole == True:
                     holeNearby = True
                if _.banana == True:
                    bananaNearby = True
                            
        if holeNearby == True:
            self.gameHistory.append("You feel a draft.")
            
        if bananaNearby == True:
            self.gameHistory.append("You smell bananas.")
                
        if cogNearby == True:
            self.gameHistory.append(cogQuotes())

    #Gets text from the user and runs the game    
    def getText(self):
        value = self.cmdEnter.text()
        self.cmdEnter.clear()

        #Can only proceed if the game is in progress or being restarted
        if not self.situation == "gameOver" or value == "restart":
            self.gameHistory.append(">> " + value + "\n")

            #Perform action based on that command.
            if not value == "restart":
                self.situation = player.command(value, placeDict, self.gameHistory)
                if self.situation == "shuffleCog":
                    self.whereCog = putItems(placeDict, self.whereCog, True)

                x, y = locations(player.loc)
                self.toonIcon.setGeometry(x, y, 71, 61)

                if self.situation == "Winner":
                    self.gameHistory.append("\nYou won in " + str(self.turns + 1) + " turns!")
                    self.situation = "gameOver"
                    
                if self.situation == "gameOver":
                    self.gameHistory.append("\nType \"restart\" to go again!")
                

                if self.situation == "banana":
                    #Shuffle the Items
                    putItems(placeDict, self.whereCog, False, True)

                #Prevent anything from printing out if game over is met
                if not self.situation == "gameOver":      
                    self.turns += 1
                    #If you didn't just kill the cog,
                    if self.whereCog.cog == True:
                        #Every 3 turns, the cog moves to an adjacent location
                        if self.turns % 3 == 2:
                            self.whereCog.cog = False

                            if self.whereCog.places[0].canWarp == True:
                                self.whereCog = self.whereCog.places[1]
                            else:
                                self.whereCog = self.whereCog.places[0]
                            self.whereCog.cog = True
                                
                        
            else:
                self.whereCog = putItems(placeDict, self.whereCog)
                player.loc = TTC
                
                x, y = locations(player.loc)
                self.toonIcon.setGeometry(x, y, 71, 61)
                
                player.pies = 5
                self.situation = ""
                
            if not self.situation == "gameOver":
                self.paths()
        
    def retranslateUi(self, HuntTheWumpusbot):
        _translate = QtCore.QCoreApplication.translate
        HuntTheWumpusbot.setWindowTitle(_translate("HuntTheWumpusbot", "Hunt The Wumpusbot"))
        self.pushButton.setText(_translate("HuntTheWumpusbot", "Enter Command"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HuntTheWumpusbot = QtWidgets.QMainWindow()
    ui = Ui_HuntTheWumpusbot()
    
    ui.setupUi(HuntTheWumpusbot)
    
    HuntTheWumpusbot.show()
    ui.gameHistory.append(helpme())
    ui.gameHistory.append(player.look())
    ui.gameHistory.append(ui.paths())

    sys.exit(app.exec_())

    

###############################################
####            Gui Stuff
###############################################
