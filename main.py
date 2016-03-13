# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import datetime
import copy
import sys


acts = []
storyProgress = []
player = None
bp = None
playerDead = False


def typeNormal(stringToBeTypedOut, ending=''):
    '''
    Types 'normal' text character by character, and ending as desired
    '''
    for letter in stringToBeTypedOut:
        print(letter, end='')
        time.sleep(0.05)
    print(ending, end='')


def typePhoneCall(stringToBeTypedOut, static=False):
    '''
    Outputs in a 'phone-call' like format, with optional static added using *
    '''
    for letter in stringToBeTypedOut:
        if letter=='*' and static:
            time.sleep(0.4)
            print("--STATIC--", end='')
            time.sleep(0.4)
        else:
            print(letter, end='')
            time.sleep(0.1)
    print()
    print()


def typeDramatic(stringToBeTypedOut, ending=''):
    '''
    Types 'dramatic' text character by character, and ending as desired
    '''
    for letter in stringToBeTypedOut:
        print(letter, end='')
        if letter in ['.', '?', '!']:
            time.sleep(0.75)
        elif letter in [',', '-']:
            time.sleep(0.5)
        elif letter==':':
            time.sleep(1)
        else:
            time.sleep(0.025)
    print(ending, end='')

        
def typeFinalDramatic(stringToBeTypedOut, ending=''):
    '''
    Types VERY dramatic text (Endgame) to bring a sense of closure
    '''
    for letter in stringToBeTypedOut:
        print(letter, end='')
        if letter in ['.', '?', '!']:
            time.sleep(1.25)
        elif letter in [',', '-']:
            time.sleep(1)
        elif letter==':':
            time.sleep(1.5)
        else:
            time.sleep(0.05)
    print(ending, end='')


def typeQuote(stringToBeTypedOut):
    '''
    Outputs as if someone is speaking these lines.
    '''
    typeDramatic("\"%s\"" % stringToBeTypedOut, ending="\n\n")


def typeCaps(stringToBeTypedOut):
    '''
    Outputs the desired string in all caps and with a pause for dramatic effect
    '''
    print(stringToBeTypedOut.upper(), end="\n\n")
    time.sleep(1)


def validChoice(string, validChoices, exact=False):
    '''
    Determines if the specified choice is valid, and returns both the validity
    of the choice as well as corrected choice in a more easily readable format
    '''
    validity = False
    correctedAnswer = ''
    for choice in validChoices:
        if (choice.upper() == string.upper()):
            validity = True
            correctedAnswer = choice.upper()
    return validity, correctedAnswer


def askValidSC(askString, choicesAnswersDict, exact=False):
    '''
    Asks the user for a single choice from a list of choices, repeatedly asking
    until the choice is deemed acceptable
    '''
    choices = choicesAnswersDict.keys()
    choices.sort()
    typeNormal(askString)
    correctedAnswer = ''
    for choice in choices: 
        print()
        typeNormal("%s. %s" % (choice, choicesAnswersDict[choice]))
    answer = raw_input(">: ")
    while not validChoice(answer, choices, exact)[0]:
        typeNormal("Select an answer %s through %c as listed above." %
        (choices[0], choices[-1]))
        answer = raw_input(">: ")
    correctedAnswer = validChoice(answer, choices, exact)[1]
    typeNormal("You chose %s: %s." % (correctedAnswer,
    choicesAnswersDict[correctedAnswer]), ending="\n\n")
    return correctedAnswer


def askValidMC(askString, choicesAnswersOrigDict, numAnswers):
    '''
    Asks the user for multiple choices from a list of choices, using a similar
    logic as the askValidSC function
    '''
    answers = []
    choicesAnswersDict = copy.deepcopy(choicesAnswersOrigDict)
    currentChoicesAnswersDict = choicesAnswersDict
    for answerIndex in range(numAnswers):
        newAnswer = askValidSC("%s (Choice %i/%i)" % (askString, answerIndex + 1,
        numAnswers),
        currentChoicesAnswersDict)
        currentChoicesAnswersDict.pop(newAnswer)
        answers.append(newAnswer)
    answers.sort()
    return answers


def askValidUI(askString):
    '''
    Asks the user for a string input, and returns this input
    '''
    typeNormal(askString)
    answer = raw_input(">: ")
    print()
    return answer


def askAccept(askString):
    '''
    Asks the user to accept (hit enter to continue)
    '''
    typeNormal(askString)
    raw_input(">: ")
    print()


def introduction():
    '''
    Runs the introduction
    '''
    now = datetime.datetime.now()
    typeDramatic("It is %s, %i. It has been four days \
since the rise of the zombies. Three days since the fall of the government. \
Two days since the last news broadcast. One day since the last of your supplies \
ran out. In this anarchic world rife with unpleasant surprises at every \
corner, there is only one chance for survival:" % (now.strftime("%B %d"), \
int(now.strftime("%Y")) + 20), ending = "\n \n")
    typeCaps("Safehouse 39")
    print(end="")
    time.sleep(1.5)
    typeNormal("A text-based adventure by Raj Khaitan and Jaiveer Singh.",
    ending = "\n")
    typeNormal("Copyright 2016.", ending = "\n \n")
    time.sleep(1.5)
    

def instructions():
    '''
    If asked to, displays instructions, then begins the actual content
    '''
    answer = askValidSC("Show Instructions? (Enter LETTER A or B)", {'A' : "Yes", 'B' : "No"})
    if answer == "A":
        typeNormal("How to Play: When prompted, enter the LETTER corresponding \
to your desired choice. Get to Safehouse 39 before it's too late, and remember, \
if you die, you must restart from the beginning!", ending = "\n\n")
    askAccept("Press enter to begin.")    


def createStorage():
    '''
    Creates the necessary storage space needed for storyProgress
    '''
    for actIndex in range(len(completeStoryline)):
        storyProgress.append([])
        for chapterIndex in range(len(completeStoryline[actIndex][2])):
            storyProgress[-1].append([])
            for sceneIndex in range(len(completeStoryline[actIndex][2][chapterIndex][2])):
                storyProgress[-1][-1].append([])

class Player:
    '''
    Class of player with corresponding attributes
    '''
    
    def __init__(self):
        '''
        Initializes strength, health, and knowledge
        '''
        self.str = 5
        self.hea = 5
        self.kno = 5
        self.name = "Player"
        
    def statModify(self, strChange, heaChange, knoChange):
        '''
        Modifies player stats as specified, notifies the user of the change, and
        if applicable, kills the player for having too little health
        '''
        self.str += strChange
        self.hea += heaChange
        self.kno += knoChange
        if(strChange > 0):
            typeDramatic("Strength upgraded! +%i" % strChange, ending = "\n")
        elif(strChange < 0):
            typeDramatic("Strength downgraded! %i" % strChange, ending = "\n")
        if(heaChange > 0):
            typeDramatic("Health upgraded! +%i" % heaChange, ending = "\n")
        elif(heaChange < 0):
            typeDramatic("Health downgraded! %i" % heaChange, ending = "\n")
        if(knoChange > 0):
            typeDramatic("Knowledge upgraded! +%i" % knoChange, ending = "\n")
        elif(knoChange < 0):
            typeDramatic("Knowledge downgraded! %i" % knoChange, ending = "\n")
        print()
        typeDramatic("Strength: %i \nHealth: %i \nKnowledge: %i" 
                    % (self.str, self.hea, self.kno))
        print("\n")
        if(self.hea <= 0):
            self.die("succumbed to the injuries and hardships of the apocalypse")
            
    def statSet(self, strNew, heaNew, knoNew):
        '''
        Sets the player stats to exactly what is specified
        '''
        self.str, self.hea, self.kno = strNew, heaNew, knoNew
        
    def die(self, deathmsg):
        '''
        Kills the player, and lets them know exactly how they died and how they
        can play again
        '''
        typeDramatic("%s %s." % (self.name, deathmsg), ending = "\n\n")
        typeCaps("Game over.")
        typeDramatic("To play again, type 'adv()' and hit enter.", ending = "\n\n")
        sys.exit()

player = Player()


class Backpack:
    '''
    Class of backpack that stores items for the user
    '''
    
    def __init__(self, backpackStorageAmount):
        '''
        Intializes backpack storage and how much it can store
        '''
        self.ms = backpackStorageAmount
        self.cb = []
    
    def update(self, listBackpackItems, dictChoices):
        '''
        Updates the backpack with items as specified. If there is an error, the
        backpack corrects itself by dumping items as necessary
        '''
        for newItem in listBackpackItems:
            if not newItem in self.cb:
                self.cb.append(dictChoices[newItem])
            if len(self.cb) > self.ms:
                typeNormal("Capacity exceeded!")
                tempDict = {}
                for i in range(len(self.cb)):
                    tempDict[chr(i + ord('A'))] = self.cb[i]
                self.cb.remove(tempDict[askValidSC("Throw something out:", tempDict)])
            print()
        if len(self.cb) < self.ms:
                typeNormal("Backpack capacity is %i out of %i. " % (len(self.cb),
                self.ms))
        elif len(self.cb) == self.ms:
                typeNormal("Warning! Backpack full!", ending="\n\n")
        typeNormal("Current backpack contents:", ending="\n\n")
        self.display()
        
    def display(self):
        '''
        Notifies the user of the current backpack contents
        '''
        print(self.cb, end="\n\n")


bp = Backpack(3)

'''
This list is the fundamental storyline of the entire game. The overall list 
contains numerous items, each of which is an Act. Each Act contains an Act
number, an Act name, and a list inside it. This list is called the Chapter List 
and contains numerous items, each of which is a Chapter. Each Chapter contains a 
Chapter number, a Chapter name, and a list inside it. This list is called the 
Scene List and contains numerous items, each of which is a Scene. Each Scene contains
a Scene number, a list of pretext strings to be typed out prior to asking a question
as specified, the question to be asked, the type of question to be asked, and a 
list of acceptable responses.

NOTE: As per the Python-esque idea of solving problems in the simplest way possible,
we chose to remain with the easily mutable list shown below, as opposed to a more
complex method we were unfamiliar with. Additionally, we continued to use the 
backslash operator throughout the list in order to prevent indexing errors that
occured. This was because instead of using the print() statement as used in
examples, we defined our own functions, which could not handle multi-string
input as was suggested as an alternative. Thus, our code was written to the
fullest extent possible by our limited knowledge and instruction in the Python
language, and thus has some minor instances where it deviates from the strict
standards as set forth here.
'''
completeStoryline =[
#List of Acts
    [ #Act 1
        0,
        "Beginnings",
        [ #List of Chapters
            [ #Chapter 1
                0,
                "Mysterious Call",
                [ #List of Scenes
                    [ #Scene 1
                        0, #Scene ID
                        [ #Pre-question texts
                            "DYou wake up to stark white sunlight glaring down through a \
window. Dazed and confused, you panic until you recognize the small apartment as \
your own. You can't seem to remember anything, as you ask yourself,"
                        ],
                        "'What is my name?'", #Question text
                        "UI", #Question type
                        { #Choices dictionary
                        }
                    ],
                    [ #Scene 2
                        1,
                        [
                            "DIn a sudden rush, the events of the past week come \
back to you. You close your eyes, hoping this is just a dream, but it isn't.",
                            "DThis is the apocalypse.",
                            "DAs your stomach groans from hunger, you hear the \
discordant ringing of your cellphone. The dimly lit screen reads:",
                            "CUnidentified Caller"
                        ],
                        "Do you accept the call?",
                        "SC",
                        {
                            "A" : "Accept",
                            "B" : "Reject"
                        }
                    ],
                    [ #Scene 3
                        2,
                        [
                            "DYou decline the call, but then your phone begins \
to ring again. This time, you pick it up."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [ #Scene 4
                        3,
                        [
                            "DGingerly, you lift the phone up to your ear and \
hear a raspy voice emerge from the static:",
                            "PG-get to the *house before * late! Hurry! There \
are only * hours until * [Signal Lost]"
                        ],
                        "What do you make of the call?",
                        "SC",
                        {
                            "A" : "This 'warning' is just some kind of joke.",
                            "B" : "I've played enough videogames to know a phone \
call is always a warning..."
                        }
                    ],
                    [ #Scene 5
                        4,
                        [
                        "DYou ignore the call and look through your pantry for \
food. As you try to eat ramen noodles without any hot water to cook them in, you \
turn on the television, but nothing is playing."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 6
                        5,
                        [
                            "DParanoia (or self-preservation) taking control, you \
start packing some essentials into a small backpack. With nothing to go on \
besides the mysterious warning, you debate on what to pack."
                        ],
                        "Choose one at a time.",
                        "MC2",
                        {
                            "A" : "Baseball bat",
                            "B" : "Wallet",
                            "C" : "Food and water",
                            "D" : "GPS",
                            "E" : "Flashlight"
                        }
                    ],
                    [#Scene 7
                        6,
                        [
                            "DYou try to think of something to do as you while \
your day away."
                        ],
                        "What do you do to relieve the boredom?",
                        "SC",
                        {
                            "A" : "Read a book",
                            "B" : "Lift some weights",
                            "C" : "Take a nap"
                        }
                    ],
                    [#Scene 8
                        7,
                        [
                            "DYou pick up an old classic - Stevenson's Treasure \
Island - and begin to read. As you flip through the pages, your eyelids slowly \
droop downwards."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 9
                        8,
                        [
                            "DTrying to keep up your strength, you begin doing \
some reps. However, a combination of fatigue and hunger makes you tire quickly, \
and your eyelids slowly droop downwards." 
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 10
                        9,
                        [
                            "DSlowly drifting asleep, your mind becomes free of \
worries, as you lie blissfully unaware of what is yet to come..."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [ #Chapter 2
                1,
                "Daring Escape",
                [
                    [#Scene 11
                        10,
                        [
                            "DAs the sun approaches the horizon, you are jolted \
awake by a deep rumble. The walls of your apartment are shaking violently. \
It's an earthquake!"
                        ],
                        "Do you stay inside and get under something sturdy to outlast \
the quake, or do you try and escape the building?",
                        "SC",
                        {
                            "A" : "Stay put!",
                            "B" : "Run for it!"
                        }
                    ],
                    [#Scene 12
                        11,
                        [
                            "DYou quickly snatch your backpack and run out of the \
door of your apartment and into the collapsing hallway. The entire building starts \
to shake and rumble. Dashing faster, you see both the fire escape and the staircase."   
                        ],
                        "Which one do you take to exit the building?",
                        "SC",
                        {
                            "A" : "Staircase",
                            "B" : "Fire Escape"
                        }
                    ],
                    [#Scene 13
                        12,
                        [
                            "DYou decide to hide, but suddenly you see your ceiling \
and walls start to crack. Whole chunks of plaster rain everywhere, and you \
narrowly dodge a falling mirror. There is only one escape!",
                            "DYou leap out through your window and fall down \
two stories into the bushes below, taking a severe pounding but making it out alive." 
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 14
                        13,
                        [
                            "DYou run down the staircase as fast as you can, but \
you find part of the ceiling has collapsed and blocked off the way. You find a \
medium-sized hole in the wall from the damage and jump through it, leaping into \
the air from the first story and collapsing into the bushes below."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 15
                        14,
                        [
                            "DYou go down the fire escape ladder as fast as \
possible, nearly spraining your ankle but making it out safely. You collapse in \
nearby bushes, without any major injuries."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 16
                        15,
                        [
                            "DYou continue running away from the danger zone \
as the building lets out a dying groan. Suddenly, the entire apartment complex \
structure collapses in on itself, crushing what little you once had. A brown \
cloud of dust hovers in the air, and as it slowly settles down on the rubble, \
you realize that this was no earthquake.",
                            "DIt was a zombie horde.",
                            "DThe destructive mass of zombies continues moving \
towards your direction, ripping apart cars, trees, buildings, and anything else \
that stands in its way. You do the only thing that you can do: run."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 3
                2,
                "A Second Message",
                [
                    [#Scene 17
                        16,
                        [
                            "DThe setting sun above you, you sprint in the \
opposite direction from the zombies. You might be able to outrun them, but it's \
of no use.",
                            "DThe zombies have caught your scent and will pursue \
you relentlessly unless you find a way to hide from their enhanced smell and \
hearing. As you continue sprinting down through the tall grass surrounding your \
neighborhood, you see a pond and a small forest ahead."
                        ],
                        "Which location do you run towards?",
                        "SC",
                        {
                            "A" : "Pond",
                            "B" : "Forest"
                        }
                    ],
                    [#Scene 18
                        17,
                        [
                            "DGood thinking! By submerging yourself in the \
murky water of the pond, you successfully masked your smell."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 19
                        18,
                        [
                            "DGood thinking! By running into the forest and \
slathering yourself with mud, leaves, and twigs, you successfully masked your smell."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 20
                        19,
                        [
                            "DThe zombie horde, losing interest in this fleeting \
chance at fresh meat, stops following you. Instead, the horde returns to its \
original course, slowly demolishing building after building in a mindless march \
to an unknown goal...",
                            "DAfter your harrowing escape, you feel incredibly \
fatigued. As you trudge along a deserted road in the hopes of re-encountering \
civilization, you realize that you must eat soon or die of hunger. Luckily, you \
spot a recently abandoned restaurant further along the road, and hurry inside.",
                            "DFor a post-apocalyptic restaurant, the establishment \
is not bad at all. Scattered items everywhere suggest that whoever escaped was in \
a rush.",
                            "DThen you notice reddish-brown stains and bits of \
decaying matter scattered on the tile floor. Not an escape after all.",
                            "DAs you try to forget the gruesome image you \
just saw, you look in the kitchen to find any food you could eat. Picking through \
the now-useless freezer and refrigerator, you see that you can prepare yourself \
a nice hearty hamburger, or a lean and green kale salad instead."
                        ],
                        "Which meal do you choose?",
                        "SC",
                        {
                            "A" : "Burger",
                            "B" : "Salad"
                        }
                    ],
                    [#Scene 21
                        20,
                        [
                            "DThe burger is a great boost to your strength, but \
the meat tastes a few days old. You feel slightly sick in your stomach as you \
swallow the sandwich down, bite by bite."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 22
                        21,
                        [
                            "DThe kale salad is a healthy meal that helps you \
recover from the ordeals of the first day out, but the lack of protein leaves \
you feeling a bit weaker than before."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 23
                        22,
                        [
                            "DYour dinner finished, you continue to sit in the \
rapidly darkening restaurant, when suddenly, your phone vibrates faintly.",
                            "DThe caller ID reads the same as before:",
                            "CUnidentified Caller",
                        ],
                        "Do you accept or reject the call?",
                        "SC",
                        {
                            "A" : "Accept",
                            "B" : "Reject"
                        }
                    ],
                    [#Scene 24
                        23,
                        [
                            "DYou can't help but feel as if you might have missed \
out on something tremendously important. You have an urge to try and call the \
number back, but it is too late. Your phone screen briefly shows the Android logo, \
and then dies. In a sudden release of anger, you throw the now-useless piece of \
plastic onto the hard tile floor, smashing it into millions of small pieces."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 25
                        24,
                        [
                            "DYou once again accept the call. It is the same low, \
raspy voice, and the second message is just as cryptic:",
                            "PLoca* is 39" + u"\u00b0" + "41'26.0\"N 104" + 
u"\u00b0" + "51* [Signal Lost]",
                            "DRight in the middle of the call, your phone runs out \
of battery and dies. You are left with part of a location, but still you now \
know something more than what you did before."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 26
                        25,
                        [
                            "DLuckily, you have a GPS with you that you packed \
in your backpack! Using the coordinates from your mysterious friend, you find \
that the location he refers to is an abandoned warehouse, hundreds of miles away.",
                            "DThere's no way you can get there by walking, so you \
know you need to find a different method for transportation.",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 27
                        26,
                        [
                            "DBut that's the least of your worries. It's now almost \
nightfall, and there are many dangers lurking in the darkness..."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 4: First Night
                 3,
                 "First Night",
                 [
                    [#Scene 28
                        27,
                        [
                            "DAs night approaches, you need to find some \
kind of shelter to keep you safe. The moon is bright outside, bright enough \
that you can see the outlines of the landscape, but not much else.",
                            "DYou can stay in the restaurant and sleep \
on the cold tile, or you can risk venturing outside to find a better safe \
place."                        
                        ],
                        "Which do you choose?",
                        "SC",
                        {
                            "A": "Stay in the restaurant",
                            "B": "Venture outside"
                        }
                    ],
                    [#Scene 29
                        28,
                        [
                            "DLuckily for you, you have a flashlight to \
illuminate your way through the darkness.",
                            "DYou slowly creep along the worn out road, \
and reach a fork. You see two buildings, a library and a grocery store."
                        ],
                        "Where do you choose to sleep?",
                        "SC",
                        { 
                            "A": "Library",
                            "B": "Grocery Store"
                        }
                    ],
                    [#Scene 30
                        29,
                        [
                            "DUnluckily for you, you have no flashlight to \
illuminate your way through the darkness.",
                            "DYou slowly creep along the worn out road, \
and reach a fork. You see the silhouttes of two buildings."
                        ],
                        "Which direction do you go?",
                        "SC",
                        { 
                            "A": "Left",
                            "B": "Right"
                        }
                    ],
                    [#Scene 31
                        30,
                        [
                            "DYou go inside the building, a library, and bolt the main \
door behind you. Just for good measure, you grab a cart of books and park \
it behind the entrance.",
                            "DYou find matches strewn on the floor. You \
spark a match and hold it up to a book, engulfing it in a flame.",
                            "DAs you fashion a crude torch from the book, \
you look at its title. Good, it's just one of those trashy romance novels.",
                            "DYou find a nice corner by where you can sleep. \
As you lie down on the worn out couch, the corner of a book pokes your side. \
You read the title:",
                            "CThe Ultimate Guide to Survival in a Zombie \
Apocalypse",
                            "DHuh. What a coincidence. You begin reading \
, and slowly nod off to sleep. Just as you feel too tired to continue, you \
extinguish the torch and close your eyes..."
                        ],
                        "",
                        "",
                        { 
                        }
                    ],
                    [#Scene 32
                        31,
                        [
                            "DYou go inside the building, a grocery store, \
and bolt the main door behind you. Just for good measure, you grab a cart \
of rotten vegetables and park it behind the entrance.",
                            "DYou walk around and crouch down to find a \
lighter on the floor. You pick it up and light it using it as a torch to \
find your way around. ",
                            "DYou begin to explore the aisles to try to find \
some food. The shelves are mostly empty but you are lucky enough to find \
a protein bar lying around.",
                            "DAfter eating the bar, you find a set of dumbells \
lying in a corner. You lift them absentmindedly, trying to distract yourself \
from your current plight.",
"Soon you begin feeling sleepy, and slowly drift asleep...",
                        ],
                        "",
                        "",
                        { 
                        }
                    ],
                    [#Scene 33
                        32,
                        [
                            "DYou chose to stay where you were.",
                            "DScaredy cat? Sure. But continuing with the \
feline analogy, \"curiosity killed the cat.\" Not a bad move after all.",
                            "DYou find a booth in the corner and you lie \
down. After a few moments, you close your eyes and fall asleep..."
                        ],
                        "",
                        "",
                        { 
                        }
                    ]
                 ]   
            ],
            [#Chapter 5
                4,
                "Safe... For Now",
                [
                    [#Scene 34
                        33,
                        [
                            "DYou wake up just before dawn to a small noise. \
You sit silently in your makeshift bed, straining your ears.",
                            "DThere it is again. A soft, repetitive scratching \
sound. Then a pause, and then the scratching once more.",
                            "DYour heart begins to pound as you try to determine \
the cause of the sound. It might just be the wind, or it could be a \
zombie. Maybe it's a fellow survivor desperate for shelter."
                        ],
                        "Is the noise worth investigating?",
                        "SC",
                        {
                            "A" : "Yes",
                            "B" : "No"
                        }
                    ],
                    [#Scene 35
                        34,
                        [
                            "DIt's only the wind, of course. No need to \
get up. Better to just stay inside and--",
                            "CJump scare!!!\nJump scare!!!\nJump scare!!!\nJump scare!!!"
                            "DA zombie stumbles into the room in which you've \
made your bed, moaning with a renewed ferocity. You hear more around the corner \
and outside, hunting for you."
                        ],
                        "",
                        "",
                        {
                        }
                   ],
                   [ #Scene 36
                        35,
                        [
                            "DMustering up your courage, you sneak up to a boarded \
up window. Carefully, you peek past the boards and see-",
                            "DSuddenly the oblong head of a decaying zombie blocks \
your view. A single, oozing yellow eyeball stares stright at you as you step back \
from a combination of fear and disgust. The zombie begins scratching at the boards \
with renewed fervor.",
                            "DYou dash back to your little bed and grab your \
belongings. The scratching sound is replaced by the sound of splintering wood and \
then loud animalistic cries as your shelter is raided by zombies.",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 37
                        36,
                        [
                            "DDarting through the exit at full speed, you run past \
the surprised zombies. They quickly realize that their target is fleeing, and soon \
you have a mindless horde quick on your tail.",
                            "DYou sprint along the main road as the sun begins to \
illuminate the early dawn sky. The zombies behind you show no sign of slowing, \
and more and more zombies appear from behind the desolate buildings along the street.",
                            "DYou need to lose them, and fast, before you are caught \
and brutally killed. You see an alleyway up ahead that you could duck into."
                        ],
                        "Do you run into the alleyway or stick to the main road?",
                        "SC",
                        {
                            "A" : "Alleyway",
                            "B" : "Main Road"
                        }
                    ],
                    [#Scene 38
                        37,
                        [
                            "DYou skid to the left as you duck into a narrow alleyway. \
Unfortunately, your attempt to hide is brought to an abrupt stop by a one-armed zombie \
in tattered rags that resemble a police officer's uniform.",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 39
                        38,
                        [
                            "DNarrowly avoiding a vicious swing, you dash back onto \
the main road and continue running for your life."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 40
                        39,
                        [
                            "DYou take a nasty jab to your face and barely block \
another punch. However, you quickly free yourself from the zombie's grasp and run back \
to the main road."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 41
                        40,
                        [
                            "DYou look ahead and see the main road ending in an \
intersection crowded by abandoned cars. The moans behind you are getting louder, \
and suddenly they are joined by moans from ahead of you, too.",
                            "DQuickly, you look for options to make an escape. \
An abandoned office building lies directly to your right, but is being rapidly \
encroached by zombies. You also see a battered up SUV parked by the side of the \
road."
                        ],
                        "How do you try to survive?",
                        "SC",
                        {
                            "A" : "Hide inside the office",
                            "B" : "Escape in the car"
                        }
                    ],
                    [#Scene 42
                        41,
                        [
                            "DYou try to open the door to the office building, \
but it's locked. Desperately, you repeatedly push your weight against the door, \
to no avail."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 43
                        42,
                        [
                            "DYou break open the car's handle and jump into \
the driver's seat, noticing that luckily for you the key is in a cupholder. \
As your hand fumbles to turn the key in the ignition, you instinctively buckle up.",
                            "DSome things never change, even if you are in the \
middle of a life-or-death scenario.",
                            "DThe car makes a guttural noise as you try to get it \
to start. Your heart sinks as you look at the fuel gauge:",
                            "CEmpty",
                            "DYou dash outside the car and try to escape another \
way, but the zombies have already closed in."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 44
                        43,
                        [
                            "DCornered by zombies at all sides, you search in \
your pack for a weapon."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 45
                        44,
                        [
                            "DLuckily for you, you have a baseball bat to try and \
hold the zombies off. You swing at everything that moves with a final desperation, \
as you realize that this is your last stand.",
                            "DYou look up at the sky and see a harsh sun glaring \
through an impassive cover of clouds. What a way to go..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 46
                        45,
                        [
                            "DWith no baseball bat or other weapon to use, you \
raise your trembling fists. But your attempts to stop the zombies are useless. \
You dodge the first lunge and swing at the nearest zombie, but then the second \
blow goes straight to your stomach. The zombies, now foaming at the mouth, move \
closer to their kill as you collapse to the hard asphalt..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 47
                        46,
                        [
                            "DThen suddenly:",
                            "CBang!",
                            "CBang!",
                            "CBang!",
                            "CBang!",
                            "DYou hear the screech of tires, and then feel \
yourself pulled up into the air.",
                            "DYou hear a voice - a human voice - speak, and you \
listen to it as you pass into unconsciousness.",
                            "QHe'll be alright. Time to get moving."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ]
        ]
    ],
    [#Act 2
        1,
        "The Enigma Unfolds",
        [
            [#Chapter 6
                5,
                "Negotiations",
                [
                    [#Scene 48
                        47,
                        [
                            "DAs you regain consciousness, you feel your arm ache with a \
persistent throb. Your vision is blurred, and all you can make out are a few big \
splotches of color. It feels strangely warm, as if you were playing on a sunny \
beach in the middle of summer...",
                            "QWelcome back to the land of the living, kid.",
                            "DThe sharp words puncture your dreamy hallucinations. Your vision \
regains focus. You see several technicians in white lab coats, and a tall, muscular \
man wearing all black: black boots, black cargo pants, black T-shirt, and black shades.",
                            "DOne of the scientists grabs a syringe and stabs it into your \
aching arm.",
                            "QOw!",
                            "DThe man dressed in black pulls up a chair close to you and \
looks at you intently. He speaks again, and you recognize him as the one who saved \
you from the zombies.",
                            "QLet's get down to business. Who are you?",
                        ],
                        "",
                        "SC",
                        {
                            "A" : "I am a survivor, just like you.",
                            "B" : "I could ask the same of you."
                        }
                    ],
                    [#Scene 49
                        48,
                        [
                            "QThis isn't a game, kid. You were attacked \
by a zombie. You were even bitten on the shoulder. And yet you're still \
a 100% functional human being. No signs of degeneration at all. Explain."
                        ],
                        "",
                        "SC",
                        {
                            "A" : "Let me tell you the whole story.",
                            "B" : "I don't know if I can trust you."
                        }
                    ],
                    [#Scene 50
                        49,
                        [
                            "QI see.",
                            "DThe mercenary looks unconvinced as his \
brows furrow in deep contemplation.",
                            "QYou know, I am feeling kind of generous today. \
I'll strike you a deal. You let my boys run a few test or whatnot on you, \
discover if you have some kind of anti-zombie secret, and I'll let you in. \
I'll make life as easy for you as is possible after the apocalypse."
                        ],
                        "",
                        "SC",
                        {
                            "A" : "Alright, I accept.",
                            "B" : "No! I won't become a science experiment!"
                        }
                    ],
                    [#Scene 51
                        50,
                        [
                            "DThe mercenary casually reaches down to his \
belt and puts a revolver to your forehead.",
                            "QLet's try this again. I get your secret, you \
get to live."
                        ],
                        "",
                        "SC",
                        {
                            "A" : "Fine, please don't kill me!",
                            "B" : "Same answer: No."
                        }
                    ],
                    [#Scene 52
                        51,
                        [
                            "QExcellent! Put him under again boys. Kid, \
welcome to the Den!"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 53
                        52,
                        [
                            "DThe mercenary gives you a long, hard stare. \
Then suddenly he puts the gun back in his holster and gives you a broad \
smile.",
                            "QI like your spirit, kid. You remind me a bit of \
myself. Take this hunting knife, it'll come in handy one day. Wouldn't \
want such a promising candidate dead now, would we?",
                            "DThe mercenary winks at you and then walks \
away, as you collapse back into unconsciousness."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [ #Chapter 7
                6,
                "The Den",
                [
                    [#Scene 11
                        10,
                        [
                            "DThe next day, you are discharged from the ward and \
begin to explore The Den. You see the mercenary from before once again.",
                            "QGlad to see you're up and running. I gotta run, \
but I'll catch you around. Oh, and the name's Knox by the way.",
	                    "DYou stroll around The Den and come up to a hallway with different \
rooms. There is a large training arena, a mess hall, small living quarters, and \
a final door at the end of the corridor. The windows of this room are all blacked out, \
the door bolted, and the handle replaced by an iris scanner. As you approach, a \
holographic display reads:",
                            "CAuthorized Personnel Only."
          		],
		        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 12
                        11,
                        [
                            "DYou enter the mess hall but there is no food prepared. The cook tells \
you to grab a biscuit and come back at 1400 hours for lunch. You go back outside."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 13
                        12,
                        [
                            "DYou enter the living quarters and see that all the bunks are empty, \
with some scattered personal belongings strewn about. You go back outside."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 14
                        13,
                        [
                            "DYou walk up to the bolted door and try to open the lock. \
A robotic voice warns you to step away from the secure area immediately, and you \
hurriedly do so."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 15
                        14,
                        [
                        ],
                        "Where do you wish to explore?",
                        "SC",
                        {
                            "A" : "Mess Hall",
                            "B" : "Living Quarters",
                            "C" : "Training Arena",
                            "D" : "AUTHORIZED PERSONNEL ONLY"
                        }
                    ],
                    [#Scene 16
                        15,
                        [
                            "DYou hear shouts and hurry to the Training Arena."	
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 17
                        16,
                        [
                            "DThe Training Arena is a large, enclosed space the size \
of a gymnasium. There is a large assortment of weapons along the wall, as well as several \
unusual machines. These machines are like dentist's chairs, but with a built in harness \
and some kind of protective goggles.",
                            "DAs you near the Training Arena, you see the source of \
the loud shouting and laughter. A large, heavyset man with bleached blond hair \
swaggers about with some of his equally brutish friends. The man notices you, \
and walks over to you. As he introduces himself as Brock, you notice that he \
is covered with tattoos, including one prominently displayed on his forehead.",
                            "QYou must be the new guy who we found in the desert. I gotta ask, how \
did you survive alone for that long?",
			    "QIt's a long story.",
			    "QHmm. You don't look too tough, do you?",
			    "DHe smirks and knocks you on the arm.",
			    "QHow 'bout you take a run through the ARS?",
			    "QThe- the what?",
                            "QNot too bright either, are you? Augmented Reality Simulation. \
That thing with the chair and goggles over there."
                        ],
                        "How do you respond?",
                        "SC",
                        {
                            "A" : "Says the brute who got a forehead tattoo.",
                            "B" : "I'm sorry you think so poorly of me."
                        }
                    ],
                    [#Scene 18
                        17,
                        [
                            "QSo you're the wise guy now, huh? Alright Mr. Genius, go take a run \
of the ARS. Let's see how well you do with that.",
                            "DHe leaves you to the ARS device with a \
vindicated smile on his face.",
                            "DA short technician hurries over to you to help you. Some of the brute's \
cronies start to laugh at you for needing help with the harness."	
                        ],
                        "What do you say?",
                        "SC",
                        {
                            "A" : "I don't need help, shortie. Scram.", 
                            "B" : "Sorry, I am a little new at this."
                        }
                    ],
                    [#Scene 19
                        18,
                        [
                            "DThe technician scurries away, leaving you to figure out \
controls for yourself."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 19
                        18,
                        [
                            "DAs the technician straps you in, he briefly explains \
the controls, and warns you to be careful when using the ARS or you could die. You thank him."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 19
                        18,
                        [
                            "DIt's time to begin your training.",
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [ #Chapter 8
                7,
                "Supply Lines",
                [
                    [#Scene 11
                        10,
                        [
                            "DAs you enter the simulation, you feel your entire \
world go black in an infinitely long fall. Finally you can see again, but the \
landscape is nothing like the Training Arena.",
                            "DA robotic voice greets you.",
                            "QThis is the ARS, or Augmented Reality Simulation, \
a system that allows you to train in a very realistic setting. You will \
be recorded as you progress. You will be doing all of your training in this device.",
                            "QI'm not sure I understand.",
                            "QYou will soon. Nod your head and the simulation \
will begin. Good luck!",
			    "DNot sure what to expect, you slowly nod your head. \
You hear the hiss of releasing air, and then the world goes black once more. When \
you can see again, you observe a forest landscape. You gaze down at yourself and \
take note of your attire: combat fatigues and a gun."
		      ],
              	      "",
                      "",
                      {
                      } 
                    ],
                    [#Scene 12
                        11,
                        [
"D3 soldiers spawn around you. One of them, with markings identifying him as your \
captain, reads off your mission.",
			"QWe need to rendezvous with the perishable supplies at \
a location 10 clicks east. There are hostiles in the area; avoid confrontation and \
bring the supplies to safety!",
                        "DThe leader gestures to the two other sim-soldiers and \
tells them to go scout for enemy movement. Then, he orders you to follow him \
through the forest in search of the objective.",
                        "DSuddenly you hear rapid bursts of gunfire. You and the \
leader drop into a ditch. The leader tells you to split up and evade enemy fire. \
Heeding his command, you get up and dash behind a tree."
                        ],
                        "What do you do next?",
                        "SC",
                        {
                            "A" : "Continue dashing forward",
                            "B" : "Stay behind this tree",
                        }
                    ],
                    [#Scene 13
                        12,
                        [
                            "DYou stay hidden behind the tree. A \
small object lands in front of you, and then-",
                            "CBoom"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 14
                        13,
                        [
                            "DYou continue dashing forwards through the trees, and \
soon the gunfire ceases. You strain your eyes to try and find your leader, but he \
is nowhere in sight. You know you are pretty close to the supplies you have to find, \
but you debate as to whether you should find the leader first or take the perfect \
opportunity.",
                        ],
                        "What do you do next?",
                        "SC",
                        {
                            "A" : "Continue towards the supplies",
                            "B" : "Wait for the leader"
                        }
                    ],
                    [#Scene 15
                        14,
                        [
                            "DYou sprint forwards and reach the supplies, which \
are marked in your view by a large green flag. Seeing nothing in your way, you \
jump forwards and place your hands on the flag, completing the simulation run.",
                            "DYou exit the landscape thinking you have performed \
extremely well, but the robotic voice tells you otherwise.",
                            "QOverall performance: C Minus. Subject left commander \
behind to die and reached objective without any way of securing it from hostiles."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 16  
                        15,
                        [
                            "DYou start looking for the leader and finally find \
him meeting back up with the other soldiers.",
                            "DSuddenly the simulation ends as your view fades to \
black. The robotic voice reports on your performance.",
                            "QOverall performance: C Minus. Subject left objective \
to fall into enemy control and failed to communicate change of mission plan to \
fellow team members."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 16
                        15,
                        [
			    "DYou take off the harness and VR goggles feeling \
dejected at your poor performance. To your surprise, there is a small crowd \
gathered by your chair, watching the replay of your performance on a large TV \
screen. Among the throng of people, you notice Brock laughing his heart out, as \
well as Knox writing a few things down on a digital clipboard. Knox sees that you \
have exited the ARS, and then walks over to you.",
                            "QNot a bad performance for your first try. I know \
you think you failed, but you're clearly not a soldier. Based on that performance, \
you are clearly more of the thinking and strategizing type. With practice, you'll \
be acing these simulations in no time. Keep it up, and remember: I'll be watching \
you.",
                            "DKnox smiles at you and then turns around and walks \
away. Your sadness is replaced by a sense of elation, as you become determined \
to work hard and show Knox and Brock the best of your abilities."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 9
                8,
                "Reconnaissance",
                [
                    [#Scene 1
                        0,
                        [
                            "DIt has been 3 weeks since your introduction to \
the Den. You now are consistently ranking highest in the simulation scores for \
your class, and are some of the best of all the members in the Den.",
                            "DYou have just completed a vehicle piloting simulation \
and eagerly await your score, as do the many others crowded around the monitor. \
Finally, the robotic voice announces:",
                            "QOverall Performance: A Plus. No noticeable errors \
made.",
                            "DYou and the others begin to cheer and celebrate. \
Brock and his cronies, on the other hand, are less pleased. Beginner's luck, they \
say.",
                            "DAs the euphoria begins to wear off, you are \
approached by Knox.",
                            "QHey kid, congrats on the score. Well, I'll get straight \
to it. Your ARS scores are doing very well, so the heads of the Den have decided \
to send you on your first field test. You'll be going with me and some of the \
other experienced boys just to get a feel of what we do. Probably won't even be \
any combat on this one, just a recon mission."
                        ],
                        "Are you up to the challenge?",
                        "SC",
                        {
                            "A" : "Of course!",
                            "B" : "I don't feel ready..."
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "DKnox laughs.",
                            "QAlways a jokester, aren't you. Suit up, it's time \
to go."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "QPerfect. Grab your stuff, let's move."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 4
                        3,
                        [
                            "DYou, Knox, and a few other burly men with huge \
weapons board a small helicopter. One of the men squeezes into the pilot's chair \
and begins the journey aboard the helicopter. As the trip commences, Knox briefly \
explains the mission.",
                            "QJust another reconnaissance mission, boys. Checking \
up on outpost 17. Bill - you know Bill, right kid? The guy who runs the ARS sims \
and stuff? - Bill says there's a sensor anomaly there. Looks like a horde of \
zombies 5000 strong just magically appeared. Probably another glitch, zombies \
aren't smart enough to converge like that. We'll swoop in, dig up the sensor, \
replace it, and be back home by dinnertime.",
                            "DThe soldiers yell affirmatives and coax as many \
machine-like noises from their weapons as possible. You just nod and continue \
staring at the flowing desert landscape.",
                           "DFinally, you arrive at the dropoff point. The \
helicopter is landed on top of a stone mesa, and then you and the other soldiers \
rappel down the face into the valley below. You notice the stillness and remark:",
                           "QEverything is quiet. Perhaps... too quiet.",
                           "DSuddenly you hear rapid movement behind you."
                        ],
                        "What do you do?",
                        "SC",
                        {
                            "A" : "Jump for cover",
                            "B" : "Shoot the movement behind you"
                        }
                    ],
                    [#Scene 5
                        4,
                        [
                            "DThe soldiers guffaw at your tensed up nerves. It was \
only a small rabbit. Embarrassed, you fall back in line and march to the sensor \
location. Knox issues some instructions.",
                            "QZane, Cody, go do a quick scout about the perimeter. \
Dirk, go switch up the sensor. Kid, come with me, we'll do a scan just in case.",
                            "DThe two of you begin walking into the shadows of the \
valley. The stillness is unnerving, but you attribute your nervousness to the fact \
that this is your first field test.",
                            "QHey kid, you're tensed up again. What is it?"
                        ],
                        "How do you respond?",
                        "SC",
                        {
                            "A" : "Oh, just a bit jumpy, that's all",
                            "B" : "I have a bad feeling about this..."
                        }
                    ],
                    [#Scene 6
                        5,
                        [
                            "QHey, it's your first mission, it'll be fine. Just stick \
with me."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 7
                        6,
                        [
                            "QI think you're being a bit paranoid. Still, it is \
a bit unusual for a sensor to get such weird readings, especially considering it's \
only about a month old."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 8
                        7,
                        [
                            "DSuddenly, you hear a scream in the distance. You \
panic and look to Knox for guidance, but he already has his gun drawn and is \
on the ground.",
                            "QGet down and stay sharp! Follow my lead!",
                            "DYou dash after Knox as you both speed towards \
where you left the other soldiers. Suddenly, you see a shadow on the rock wall. \
Knox tenses up, and then relaxes as the shadow resembles his soldiers."
                        ],
                        "What do you do?",
                        "SC",
                        {
                            "A" : "Hurry and ask the soldier about the scream",
                            "B" : "Shoot the shadow before it gets closer"
                        }
                    ],
                    [#Scene 9
                        8,
                        [
                            "DKnox approaches the soldier with his gun lowered.",
                            "QHey Dirk, what's going on? We heard something and -",
                            "DThe soldier - now a zombie - suddenly draws his \
weapon and unleashes a hail of bullets, catching you off guard.",
                            "QArghh!",
                            "DKnox struggles against the soldier and finally \
shoots the zombie."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 10
                        9,
                        [
                            "QWHAT ARE YOU DOING!?",
                            "DKnox is at a loss for words as he attempts to subdue \
you. Then he looks back at the body you shot at: it's no soldier, it's a zombie."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 11
                        10,
                        [
                            "DSuddenly more zombies emerge from the shadows from behind you. \
Knox realizes that you are severely outnumbered. He begins to mow them down, as \
he yells:",
                            "QRUN!!!"
                        ],
                        "Do you leave Knox and save yourself?",
                        "SC",
                        {
                            "A" : "Run",
                            "B" : "Wait for Knox"
                        }
                    ],
                    [#Scene 12
                        11,
                        [
                            "DYou sprint away as fast as you can from the zombies. \
Suddenly you are greeted by two more zombie soldiers. Without a moment's hesitation, \
they release a hail of bullets, and you collapse to the ground."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 13
                        12,
                        [
                            "DYou stay by Knox's side and help him take care of the \
zombies. There are still too many of them, and they rapidly get closer and closer...",
                            "DKnox pushes you behind him as he slashes out with a \
machete, and then throws several grenades into the mass. He pulls you along and \
runs towards the helicopter.",
                            "DAs you outrun the zombies, Knox stumbles and then \
collapses onto the ground. He clutches his side, and you realize he's been injured.",
                            "QSir, are you alright?",
                            "QK-kid, it's too late for me! You n-need to get out \
of here before I-I transform! Take this crystal!"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 14
                        13,
                        [
                            "QSir, I can't leave you behind! We'll get you to the \
helicopter as fast as possible!",
                            "QNo! Run b-b-before I-I transform...",
                            "DKnox pushes you away. A look of grim determination sweeps \
his face. He pulls out a gun and holds it up to his own head.",
                            "QI - won't - become - a - zombie...",
                            "CBang!",
                            "DWithout looking back, you run from the valley and get into \
the helicopter, knowing you must warn the Den. As you soar into the sky, you look \
down and see a huge horde of zombies.",
                            "DThe sensor was wrong after all. The horde isn't 5000 strong - \
it's closer to 50,000."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 10
                9,
                "Escape the Den",
                [
                    [#Scene 1,
                        0,
                        [
                            "DAs you finally arrive at the Den, you realize \
you must warn Bill and the others before the zombies attack. You land on the \
helipad and dash through the double doors into the Training Arena. You see \
Brock and Bill in the middle of an argument.",
                            "QListen to me, nerd boy! I'm Knox's second-in-command, \
and since he's not back yet, I get to make the decisions around here!",
                            "QBut Knox specifically said no!",
                            "QOh look, they're back. Now watch and I will \
ask Knox. He'll shut you up!",
                            "DThe two of them look at you, frowning at your \
expression wracked with anxiety.",
                            "QHey Mr. Genius, where's Knox?",
                            "DYou swallow.",
                            "QHe... he didn't make it back. He was infected, and \
he-he killed himself.",
                            "QWHAT!? Knox is DEAD!? What have you DONE!?",
                            "DBrock grabs you by the shoulders and shakes you.",
                            "QI knew you were good for nothing! You're a coward \
and a traitor to your own race! You killed Knox to take control!"
                        ],
                        "",
                        "SC",
                        {
                            "A" : "It was an accident! I didn't do it!",
                            "B" : "We don't have time to argue!"
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "QOh yeah? And whose word do we have to prove it? \
Oh, how convenient! You were the only survivor!",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "DBrock pulls out a gun and points it at you.",
                            "QYou're right, we don't have time for snivelling \
cowards like you!",
                            "CBang"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 4
                        3,
                        [
                            "DRealizing the situation is rapidly falling out of \
control, you address the entire group at the Den. Some of the men are growing \
in anger as they listen to Brock, while others (including Bill) are more fearful \
as they listen to you.",
                            "QListen! There is a whole horde of zombies coming \
this way! If we don't evacuate, we will be overrun! Grab what we need and go!"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 5
                        4,
                        [
                            "DYour level of knowledge is too low to convince the \
mercenaries. The majority now listen to Brock.",
                            "QPlease listen! There's isn't much time!"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 6
                        5,
                        [
                            "DThe mercenaries begin to listen to you instead of \
Brock. Brock, finding himself in a losing battle, gathers what few followers he \
has and makes a final stance.",
                            "QYou're all traitors! TRAITORS!",
                            "DYou organize the mercenaries and tell them to get \
onto helicopters for evacuation. Food, water, medicine, weapons, all get loaded \
into crates."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 7
                        6,
                        [
                            "DSuddenly, a siren begins to wail. It is soon joined \
by a robotic voice:",
                            "QWarning. Horde detected in sector 7, 5 mile radius.",
                            "DYour premonitions confirmed, the mercenaries suddenly \
pick up the pace of their packing",
                            "QLet's move! Hurry!",
                            "DThen a loud rumble and the sound of an explosion shake \
through the Den. The siren changes in pitch, and the calm robotic voice is replaced \
by a much more urgent one.",
                            "QZOMBIE BREACH. ZOMBIE BREACH. ZOMBIE BREACH.",
                            "DPandemonium breaks loose and you struggle to control \
the chaos. Bill sees you and reaches you through the crowd.",
                            "QWe can't stay here any longer! The Den has fallen! \
If we want to survive, we must leave now!"
                        ],
                        "",
                        "SC",
                        {
                            "A" : "No! We can't leave until everything is packed!",
                            "B" : "You're right, let's go!"
                        }
                    ],
                    [#Scene 8
                        7,
                        [
                            "DYou and Bill stay in the Den and try to drag as many \
supplies as you can to the helicopters. Suddenly the sounds of the siren are \
interrupted by screams of agony and animalistic moans.",
                            "DThe zombies crush everything and slowly dismember \
every person they see. As you are trampled under the moving mass of bodies, alive, \
dead, and undead, your vision slowly fades to black..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 9
                        8,
                        [
                            "DRealizing that there is only one escape, you and Bill \
run up the stairs and onto the helipad. Others with the same idea as you have already \
flown away with most of the helicopters, but there is one left in the far corner.",
                            "QGET TO DA CHOPPA!",
                            "DAs you clamber onboard, your training from the ARS \
kicks in. You look back and see Bill in one of the seats, but five other seats \
empty. Guilt washes through you, but you know nobody can be saved.",
                            "DThe helicopter ascends high into the air, and suddenly \
the air becomes full with screams of agony and then animalistic moans. You realize \
that the mercenaries have not been killed - they have been transformed.",
                            "DThere are too many lives at stake here. You know what \
you must do to prevent sensitive information and powerful technologies from falling \
into the wrong hands, and to free the brave soldiers from a horrible existence. With \
grim determination, you swing the helicopter around to face the collapsing Den. Bill \
understands, and gives you a gentle nod. Your eyes closed, you flip open the cap \
and push down on the trigger."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 10,
                        9,
                        [
                            "DA pair of missiles streak through the sky. They find \
their target, and the Den explodes into a blossom of fire."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ]
        ]
    ],
    [#Act 3
        2,
        "Race to SAFEHOUSE 39",
        [
            [#Chapter 11
                0,
                "Realizations",
                [
                    [#Scene 1
                        0,
                        [
                            "DYour knuckles are white as they clutch the throttle. \
It has been 4 hours since your escape from the Den, and the helicopter continues \
to fly into the night.",
                            "DBill gently taps you on the shoulder.",
                            "QListen, we can't just keep flying. We need to go \
somewhere safe and stay there for the night. I know a place, a small shack somewhere. \
C'mon, take a break and I'll fly us there. I've been through the ARS too, you know. \
Matter of fact, I designed it, every little print statement and while loop...",
                            "DAs Bill continues speaking, you slump into the \
copilot's chair and fall asleep..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "DYou wake up on a small mattress tucked into the corner \
of a dusty room. You look around and see Bill napping gently on a desk, his head \
and hands on a keyboard. A truly ancient device.",
                            "DYou get up and stretch yourself. The room is illuminated \
only by some light that filters through a dusty skylight in the roof, and as your \
eyes become accustomed to the darkness, you realize that you are in a small cabin.",
                            "DGlancing over at the still-sleeping Bill, you decide \
to make yourself useful. Opening the door, you find yourself in the middle of a forest, \
surrounded by towering trees. You make sure you have your gun with you, and then muse \
over what you can do."
                        ],
                        "Do you cut down some trees for firewood, scout for signs \
of zombies, or look for some food to eat?",
                        "SC",
                        {
                            "A" : "Firewood",
                            "B" : "Signs of Zombies",
                            "C" : "Food"
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "DFinding an ax lying around by the cabin, you cut down \
a small tree to replenish your supplies, getting an extra workout at the same time."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 4
                        3,
                        [
                            "DYou ascend a tall tree and scout for any signs of \
destruction that might signal the arrival of a zombie horde. In every direction, \
all you see are the tips of trees and mountains looming in the distance. All clear."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 5
                        4,
                        [
                            "DFinding an old hunting rifle, you head out into the \
woods, thanking yourself for having spent a day with the ancient weapons ARS sim. \
You don't find any game, but you do find a bush of berries that you identify to be \
harmless."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 6
                        5,
                        [
                            "DYou return to the cabin, and as you slam the door shut \
you hear Bill call out to you.",
                            "QOh I knew you must have been outside. I was worried \
when I saw that you left no note, but seeing that you had taken your boots and gun \
I assumed you'd been out.",
                            "QSo, where did you bring us, Bill? Looks like a \
forest. Really quiet out here.",
                            "QWell we're in the forest all right. This place is \
so far north we're practically in Canada. It's an old camping cabin I used to know. \
Turned out pretty handy.",
                            "QBill- What are we going to do now? There's nowhere safe \
now.",
                            "DA look of indecision passes Bill's face.",
                            "QWe'll have to make do with what we have I guess. \
Survive for as long as possible, maybe meet up with some others..."
                        ],
                        "Do you think you need to gather supplies for the long \
term, or pack up everything for the short term?",
                        "SC",
                        {
                            "A" : "Gather supplies, we'll be here a while",
                            "B" : "Pack everything up, we'll leave soon"
                        }
                    ],
                    [#Scene 7
                        6,
                        [
                            "QAlright Bill, let's get everything we'd need to stay here for \
a while: food, water, wood -",
                            "QThere's no need for that, I have everything laid out on \
this map right here.",
                            "DBill pulls out a tattered map from his pocket and carefully \
unfolds it on his desk.",
                            "QYou see? Shed, bushes of berries, spots for hunting \
and fishing, everything's laid out here. We'll be quite safe here for as long \
as we need."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 8
                        7,
                        [
                            "QAlright Bill, we need to get everything packed up. \
We'll rest here for a few days, then we'll get moving.",
                            "QAlready done, my friend. Everything's in the crates \
still, and we just need to pop everything into a sack and go when we see the chance.",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 9
                        8,
                        [
                            "QWell then. I am going to take a short nap, Bill.",
                            "QI'm not quite tired yet. I think I'll work on \
something, maybe a radio...",
                            "DYou fall into a fitful sleep.",
                            "CSeveral Hours later",
                            "DIt is dark outside as you slowly wake from your slumber. \
Bill's voice suddenly rings out from the sounds of the forest.",
                            "QGlad to see you're awake! I'm getting a campfire \
started, why don't you grab some of our cans of food?",
                            "DYou heed Bill's orders and grab a few cans of provisions \
from the cabin's store. You search through your bag for a can opener, though you \
don't find one. However, your hand brushes against something sharp, smooth, and cool.",
                            "DAs you pull it out, you recognize this object as the \
mysterious crystal Knox had given to you as he died. Absentmindedly twirling the \
crystal around in one hand, you grab the can opener in the other and walk outside \
to help Bill.",
                            "QExcellent! Now let's settle down and eat!",
                            "DThe fire now roaring, you munch on your tasteless meal, \
still thinking about Knox and what he might have meant with his secretive ways. Bill, \
sitting opposite from you, notices the crystal with a start.",
                            "QHey! Where- How did you get that crystal?",
                            "QWhat? This one? It's- Knox gave it to me. As he died.",
                            "DBill frowns as his face becomes one of deep concentration.",
                            "QListen- That crystal was practically Knox's life. He \
really thought that that little thing would be the ultimate cure to the whole zombie \
plague. He wouldn't let anybody else even touch the thing, for fear they might break it. \
If he gave it to you, he must've really trusted you. Even if he was a little weird, in \
all other respects Knox was a great leader. So I guess I trust you too.",
                            "DBill shifts in his seat a little, and then speaks \
again.",
                            "QYou see- I guess I haven't been completely honest \
with you. I didn't know if I could trust you at first."
                        ],
                        "",
                        "SC",
                        {
                            "A" : "I saved your life, and you couldn't trust me!?",
                            "B" : "It's alright. I would've felt the same."
                        }
                    ],
                    [#Scene 10,
                        9,
                        [
                            "QNo! It's not like that at all! I just-"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 11
                        10,
                        [
                            "DBill stops talking for a moment, then begins again.",
                            "QListen. There's been a rumor. Spread through the airwaves. \
Some people have been talking about it. A thing- A thing they call- the Safehouse."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 12,
                1,
                "Rumors",
                [
                    [#Scene 1
                        0,
                        [
                            "DBill puts his can of food down and pulls out a small \
notebook." ,
                            "QI think it's time you learned a little about the start \
of the whole apocalypse. I'll tell you the truth, not the lies spread by the \
government and media to try to keep things contained.",
                            "QThe first thing you need to understand is that this plague \
began a whole lot longer ago than you think. This was a global phenomenon. It didn't \
unfold overnight. First signs of a neuroregenerative disease sprouted up in Brazil, \
spread by some mosquito or whatnot. But pretty soon the virus became airborne, \
and soon it was practically the world over. It didn't seem to be anything bad and it \
was a pretty low level threat according to the CDC, until new research showed dangerous \
potential.",
                            "QSuddenly entire nations began closing off their borders. \
China, Russia, out of the blue cutting off all trade and enforcing strict isolation. \
The US began to get worried. What did these countries know that we didn't? When Europe \
issued an order of military control, the White House decided it needed to respond. \
The misinformation campaign began, and all public reports called it just another global recession.",
                            "QThen it happened. The brass disappeared, evacuated \
to a bunker somewhere. FEMA took control of the entire nation and ordered a period of \
almost absolute anarchy. The CDC changed objective from curing the zombie plague to \
developing bioweapons capable of obliterating the infected.",
                            "QAbout then was when the Den was created. Knox and a few \
ex-military guys converted the warehouse into a bunker, and we began recruiting as \
many survivors as possible. Soon the zombie plague was upon us, but due to our \
planning we held out for the time being. When it became clear that this plague \
was not going to disappear any time soon, Knox began to become even more obsessed \
with finding out the secrets of the crystal and the rumors of a safehouse. We tried to tell him that it was just an \
ordinary crystal and we offered to run some tests on it, but he wouldn't let us \
touch it. That's where you came in. And I think you know the rest of the story from \
there."
                        ],
                        "",
                        "SC",
                        {
                            "A" : "I need to process this. Give me a second.",
                            "B" : "Wait. I have a few questions."
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "QIt's getting dark anyways. Time to sleep.",
                            "DBill douses the fire and takes his things inside. \
You follow him in, pack your belongings away, and go to sleep still pondering the \
mysterious zombie plague... and still pondering the mysterious Safehouse 39..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "QBill- How do you know all this, if it wasn't on the \
news?",
                            "DBill's expression is blank as he sits in silence for a \
moment.",
                            "QWell. Can't hide from the truth now. I worked for the \
CDC. I was a scientist researching different disease vectors when the higher ups \
called me. They blindfolded me and brought me to a secret facility with no windows. \
For weeks I was told to analyze disease specimens brought into the lab in huge \
biohazard trucks with combination locks on every barrel. To my horror, I was being \
told to work with the scourges of civilization - smallpox, MERS, H1N1, you name it - \
and to combine the traits of these diseases to create the ultimate bioweapon.",
                            "QI- I was weak. I did what they told me to do. And \
as soon as they let me outside again, I fled. Knox rescued me and protected me \
from the government, and soon they gave up searching for me. They were probably dead.",
                            "DThe two of you sit in silence as the embers of the \
campfire continue to burn. These revelations should surprise you, make you feel \
scared- but instead they seem like things you already knew, like pieces in a puzzle \
fitting together.",
                            "DBill finally breaks the silence."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 13
                2,
                "Ghosttown",
                [
                    [#Scene 1
                        0,
                        [
                            "DYou wake up early the next morning. Bill is already \
awake, and he appears to be tinkering with some electronics on his desk.",
                            "QWhat are you up to, Bill?",
                            "QOh! Glad to see you're awake. I am trying to modify \
the helicopter's radio to increase the range. Without getting into specifics-"
                        ],
                        "",
                        "SC",
                        {
                            "A" : "Sure, have fun with your tinkering.",
                            "B" : "Whoa! Please explain!"
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "QOf course! Using some spare parts, I am trying to \
add an amplifier to the signal, so that we can not only receive and send messages \
longer distances, but also track down the sources of signals. It'll be useful if we \
need to find other survivors alone in the wilderness."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "QWait a second... Bill, where's the helicopter? We can \
use that to fly around!",
                            "QNo can do. It's out of fuel. All it's good for is spare \
parts.",
                            "QAw. Well, I am going to try and get some grub going for \
us.",
                            "DYou prepare a simple breakfast of pancakes and berries, \
with some fortified protein bars on the side."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 4
                        3,
                        [
                            "DSuddenly you hear a screech of static followed by an \
exclamation from Bill.",
                            "QYES! It works!",
                            "DLeaving the pancakes on the griddle, you hurry back \
to Bill to see what he has done.",
                            "QWhat is it? Did you fix the radio?",
                            "QShh! I am picking up a signal...",
                            "DYou watch as Bill listens intently to the faint signals \
emitting from the radio.",
                            "DA loud broadcast emerges from the radio:",
                            "Q-remain calm. FEMA and the CDC are working to \
protect the American people. Follow all safety advisories, and remember: Please \
remain calm. FEMA and the CDC -",
                            "DBill turns the volume off and gets out of his chair, \
disappointed.",
                            "QI had thought we might find a survivor. It's just the \
advisory trash, nothing more.",
                            "QWait! Bill, can't you track the source of the signal? \
If the signal is still going out right now, then there's probably a safe place somewhere \
wherever it's originating from!",
                            "DBill nods excitedly and begins turning some knobs on \
the radio.",
                            "QYou're right! I got it! I have the coordinates of the \
signal!",
                            "QBut how are we going to get there Bill? You said the \
helicopter is out of fuel.",
                            "QYes, but if I remember correctly...",
                            "COne hour later",
                            "DDriving through the forest on motorcycles so old \
they could be considered antiques, you and Bill approach the source of the signals \
at high speed.",
                            "DAs you cross a deserted road, you enter the fringes \
of a small town. The buildings are all shuttered, the cars are all broken, and \
the single road is full of potholes. A fine layer of dust lies on everything.",
                            "DBill stops and disembarks from his motorcycle, radio \
still in hand.",
                            "QWell. This is it. The signal is coming from right here.",
                            "DYou look around. The entire town appears to be devoid \
of inhabitants. And yet, there are no signs of anybody fleeing, or of any kind of \
zombie attack. Curious..."
                        ],
                        "You see two buildings you can explore. Which do you choose?",
                        "SC",
                        {
                            "A" : "Town Hall",
                            "B" : "Library"
                        }
                    ],
                    [#Scene 5
                        4,
                        [
                            "DYou enter the Town Hall and take a look around. The \
building looks ancient, and ready to fall apart at any moment. You carefully step \
around, leaving footprints in the dust covering the floor.",
                            "DYou notice a glint somewhere above you. Unsure of \
what it is, you find a staircase to reach the first floor and investigate.",
                            "DAs you step onto the landing, the rotted wooden beams \
suddenly give way. You fall ten feet to the ground, and gaze upwards in horror as \
the wooden staircase tumbles down onto your prone body..."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 6,
                        5,
                        [
                            "DAs you explore the library, you notice some footprints \
in the dust. Cautiously, you yell out to Bill.",
                            "QHey Bill! Check this out. I think I might've found \
something.",
                            "DBill quickly follows you into the library.",
                            "QHmm, you might be right. My radio device seems to be \
picking up slightly stronger signals here. But still - it seems as if we're still \
far away from the source. Almost as if-",
                            "DThe same thought rushes through your mind like an electric \
shock. Your heartbeat quickening, you stride down the bookshelves, scanning the \
titles, looking, looking...",
                            "DThere. How you know is a mystery. But it's the right one. \
With Bill close behind you, you pull out the book. The ground begins to rumble.",
                            "DThe bookcases part, revealing a tunnel \
built into the wall. Stark white electric lights suddenly flicker on, illuminating \
a descending staircase. The signals are coming from a secret bunker underground.",
                            "DCarefully, you and Bill descend the stone steps, entering \
a huge underground complex. The sign posted along the walls reads:",
                            "CBunker #23. Authorized Personnel Only.",
                            "DThe two of you continue walking down the corridor. \
Finally, you reach a set of heavy double doors. You read the warnings:",
                            "DBIOHAZARD",
                            "DRISK OF DEATH",
                            "DAUTHORIZED PERSONNEL ONLY",
                            "DThese warnings would be enough to cause most to turn \
back, but not you. You grasp the cold metal of the door handle and pull it open..."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 14
                3,
                "Biohazard",
                [
                    [#Scene 1,
                        0,
                        [
                            "DYou walk into the lab and see total chaos. Some of the \
lights are burned out, and broken glass litters the floor. Treading cautiously, \
you continue to explore."
                        ],
                        "You see a left wing and a right wing to the lab. Which do you \
choose?",
                        "SC",
                        {
                            "A" : "Left Wing",
                            "B" : "Right Wing"
                        }
                    ],
                    [#Scene 2,
                        1,
                        [
                            "DYou walk into the left wing, but the passageway is \
sealed off with heavy doors. You try to push them open, but the doors do not budge. \
You instead walk over to the right wing."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "DYou walk into the right wing, gently pushing open \
the already ajar door. As you walk through the corridor, you hear talking. You freeze \
in silence, trying to determine what the voices are and what to do."
                        ],
                        "Do you burst in and use the element of surprise, or creep \
in slowly but risk getting caught?",
                        "SC",
                        {
                            "A" : "Burst in",
                            "B" : "Creep in"
                        }
                    ],
                    [#Scene 4,
                        3,
                        [
                            "DYou rush through the door of the room from where you \
hear the voices and find -"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 5,
                        4,
                        [
                            "DYou sneak through the corridor and peek past the door \
to find-"
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 6
                        5,
                        [
                            "DYou let out a small laugh. It's just a recording playing \
from a projector screen, not an actual person. You walk inside and watch the recording play.",
                            "QExperiment #35, Group B. Trial 13. Begin.",
                            "DYou watch as a body is strapped into a harness on an \
operating table. A small quantity of green fluid is injected, and suddenly the body \
begins to shake violently. The shaking does not last, however, and the voice speaks \
once again.",
                            "QTrial: Failed. Begin Trial 14.",
                            "DThe gruesome experiment is conducted yet again. You mess \
around with the computer connected to the projector to see if there are any other \
recordings you can find. You find one labelled 'EMERGENCY BULLETIN' and play it.",
                            "QAttention All Personnel: Experiment #35 has been breached, \
and the left wing has now been shut down. Biohazard status has been upgraded to level 5. \
Several deadly specimens are believed to have been released in the lab. Quarantine \
is in place. Do not attempt to open doors that have been closed. Obey all uniformed \
personnel at all times.",
                            "DYou look to see if you can find any other records, \
but there is nothing to be found. You leave the room and continue to walk down the \
corridor, looking for any other clues that might help you make sense of what is going on.",
                            "DYou walk down the corridor and notice a series of framed \
portraits along the wall.",
                            "DDr. Meyer. Assistant Biotechnology Researcher. Dr. Spencer. \
Lead Biotechnology Researcher. The list continues.",
                            "DAs you reach the very last name, you read:",
                            "DDr. Roberts. Lead Scientist, Infectious Diseases Research \
Division.",
                            "DBut the place where the picture would be is ripped up \
and destroyed.",
                            "DYou continue down the corridor and reach an ominous-looking \
door."
                        ],
                        "Do you open the door?",
                        "SC",
                        {
                            "A" : "Yes",
                            "B" : "No"
                        }
                    ],
                    [#Scene 7
                        6,
                        [
                            "DAs you open the door, you bump against a shelf of \
specimens. A green liquid spills on the floor and a foul-smelling gas is released \
into the air.",
                            "DCoughing heavily, you struggle to breathe, but manage \
to miraculously recover yourself."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 8
                        7,
                        [
                            "DSuddenly sirens begin to ring. You hear the hiss of gas \
and realize that a deadly contagion has been released into the air.",
                            "DA horrible thought begins to creep on you...",
                            "DWhen was the last time you saw Bill?",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 9
                        8,
                        [
                            "DYou dash back down the corridor to try and find Bill.",
                            "DYou skid to a stop. You've found Bill.",
                            "DFacedown with some broken vials besides him, \
Bill's body lies dead in the middle of the corridor.",
                            "DYou try not to throw up as you turn away from the body. \
You seem fine, unusually so, but you don't want to chance it.",
                            "DYou decide to take the files from the projector with you. \
As you download them to a USB - such an antiquated form of storage, you notice \
a door labelled:",
                            "CTo Road Vehicles",
                            "DUSB in hand, you run through the door and jump into \
a jeep. You drive up an endless spiral, until finally you see the light of day again.",
                            "DYou realize you have no clue where to go next, and \
with Bill gone, you are completely alone. You bring the jeep to a stop by the edge of \
the ghosttown, and plug the USB into the jeep's media player.",
                            "DYou notice a file you had missed before. It's labelled:",
                            "CKill Order",
                            "DYou click play, and wait with bated breath.",
                            "Q39" + u"\u00b0" + "41'26.0\"N 104" + 
u"\u00b0" + "51'26.0",
                            "DThese numbers remind you of something, something you \
once knew but chose to forget...",
                            "DYour path is clear. You must go to these coordinates and \
finally uncover the truth about the plague, the Safehouse, and your reality..."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ],
            [#Chapter 15
                4,
                "Memories",
                [
                    [#Scene 1
                        0,
                        [
                            "FThis is it, then. Safehouse 39.",
                            "FAfter hours of driving, you jump out of your jeep \
in front of a building. The doors read 39 in huge numerals, and in the center \
you see a familiar symbol.",
                            "FSlowly, you reach into your pocket and pull out \
the mysterious crystal from a lifetime ago. The deep purple hue matches the color \
of the crystal symbol emblazoned on the building.",
                            "FYou push open the glass door and see an empty lobby.",
                            "FAs if in a dream, you walk to the lone elevator at the \
far end of the lobby, and push B for basement.",
                            "FThe elevator descends, and you stare into the crystal \
in your hand.",
                            "FThe memories come back.",
                            "FWon the Google Science Fair at age 7.",
                            "FGraduated from high school in 2 years.",
                            "FGot a full ride scholarship to a top university.",
                            "FLanded the dream job right out of college.",
                            "FAnd then something more recent...",
                            "FA closed corporate office, with a close minded corporate \
boss. Motivated by money. Harsh words and threats.",
                            "QMr. Bergson, do you realize what you're trying to do? \
If you release my project into the world, it will kill millions. Millions. The entire \
world would collapse! Can't you see beyond your selfish aims!",
                            "FAn enraged face, red and round as a beet.",
                            "QThis company is proceeding with my plan, with or without \
you. I own your equipment, I own your buildings, I own your work, I can do whatever I want. \
And you, you can either stand down and do as I say, or else. Do I make myself clear?",
                            "FA horrified face, but submitted.",
                            "QYes... sir.",
                            "FThe memories change again.",
                            "FA dark and stormy night, and a stolen vial.",
                            "QThis-this is the only cure to my creation. The corporates \
will try to sell it as they kill off the world, but they do not know the dangerous power \
they wield. I must protect it, and save it to ensure humanity lives to see a brighter day.",
                            "FA closed safe and a knock on the door.",
                            "QDon't let him escape! Yes, shoot to kill! Bergson said \
to kill him, and I'm not losing my job tonight! Get him before he leaves the laboratory!",
                            "FA screech of tires and a tape recorder.",
                            "QGet to the Safehouse before it's too late! There are \
only four weeks until the cure is useless!",
                            "FA violet crystal and a small little pill.",
                            "QI must forget everything- forget and rediscover \
when it is time. I must wait. They do not know. They cannot know. I must wait.",
                            "FAnd then the elevator dings."
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 2
                        1,
                        [
                            "FYou step out, still in a trance like state. You see \
the lab as it was so long ago.",
                            "FYou know the truth. You have the cure.",
                            "FA pleasant robotic voice greets you.",
                        ],
                        "",
                        "",
                        {
                        }
                    ],
                    [#Scene 3
                        2,
                        [
                            "QWelcome back, Dr. Roberts."
                        ],
                        "",
                        "",
                        {
                        }
                    ]
                ]
            ]
        ]
    ]
]


class Scene:
    '''
    Class of Scene that contains individual characteristics as outlined above
    '''
    
    def __init__(self, sceneID, chapterID, actID):
        '''
        Initializes the scene and its properties
        '''
        self.id = int(sceneID)
        self.cid = int(chapterID)
        self.aid = int(actID)
        self.pret = completeStoryline[self.aid][2][self.cid][2][self.id][1]
        self.q = completeStoryline[self.aid][2][self.cid][2][self.id][2]
        self.qt = completeStoryline[self.aid][2][self.cid][2][self.id][3]
        self.c = completeStoryline[self.aid][2][self.cid][2][self.id][4]
    
    def run(self):
        '''
        Runs the scene and executes all associated functionality
        '''
        for pretext in self.pret:
            if(pretext[0] == "D"):
                typeDramatic(pretext[1:], ending="\n\n")
            elif(pretext[0] == "P"):
                typePhoneCall(pretext[1:], static=True)
            elif(pretext[0] == "C"):
                typeCaps(pretext[1:])
            elif(pretext[0] == "Q"):
                typeQuote(pretext[1:])
            elif(pretext[0] == "F"):
                typeFinalDramatic(pretext[1:], ending="\n\n")
        self.answer = ""
        if(self.qt.upper() == "SC"):
            self.answer = askValidSC(self.q, self.c)
        elif(self.qt.upper() == "UI"):
            self.answer = askValidUI(self.q)
        elif("MC" in self.qt.upper()):
            self.answer = askValidMC(self.q, self.c, int(self.qt[2]))
        try: 
            storyProgress[self.aid][self.cid][self.id].append(self.answer)
        except:
            #If error, pass through
            pass
            
            
class Chapter:
    '''
    Class of Chapter that contains individual characteristics as outlined above
    '''
    
    def __init__(self, chapterID, actID):
        '''
        Initializes the chapter and its properties
        '''
        self.id =int(chapterID)
        self.aid = int(actID)
        self.realChId = self.id + 1
        for actIndex in range(self.aid):
            self.realChId += len(completeStoryline[actIndex][2])
        self.h = completeStoryline[self.aid][2][self.id][1]
        self.scenes = []
        completeStoryline
        for sceneIndex in range(len(completeStoryline[self.aid][2][self.id][2])):
            self.scenes.append(Scene(sceneIndex, self.id, self.aid))
            
    def run(self):
        '''
        Runs the chapter and also the scenes of that chapter
        '''
        typeDramatic("Chapter %i: %s" % (self.realChId, self.h), ending='\n\n')
        for scene in self.scenes:
            scene.run()
            
    def runAlone(self):
        '''
        Runs the chapter alone.
        '''
        typeDramatic("Chapter %i: %s" % (self.realChId, self.h), ending='\n\n')
        time.sleep(1)
    
    def end(self):
        '''
        Ends the chapter
        '''
        typeDramatic("End Chapter %i" % (self.realChId), ending = '\n\n')
        time.sleep(1)       
        
        
class Act:
    '''
    Class of Act that contains individual characteristics as outlined above
    '''
    
    def __init__(self, actID):
        '''
        Initializes the act and its properties
        '''
        self.id = int(actID)
        self.h = completeStoryline[self.id][1]
        self.chapters = []
        for chapterIndex in range(len(completeStoryline[self.id][2])):
            self.chapters.append(Chapter(chapterIndex, self.id))
            
    def run(self):
        '''
        Runs the act, and also the chapters and scenes in it
        '''
        typeDramatic("ACT %i: %s" % (self.id + 1, self.h), ending='\n\n')
        chapterLen = 0
        for actIndex in range(self.id + 1):
            chapterLen += len(completeStoryline[actIndex][2])
        for chapter in self.chapters:
            chapter.run()
            
    def runAlone(self):
        '''
        Runs the act alone
        '''
        typeDramatic("ACT %i: %s" % (self.id + 1, self.h), ending='\n\n')
        time.sleep(1)
        
    def end(self):
        '''
        Ends the act
        '''
        typeDramatic("END ACT %i" % (self.id + 1), ending = "\n\n")        
        time.sleep(1)


def createStoryline():
    '''
    Creates the storyline by resorting it into lists
    '''
    for actIndex in range(len(completeStoryline)):
        acts.append(Act(actIndex))


def runScene(actID, chapterID=None, sceneID=None):
    '''
    Wrapper function that makes running a desired scene easier
    '''
    if(chapterID == None):
        acts[actID].runAlone()
    elif(sceneID == None):
        acts[actID].chapters[chapterID].runAlone()
    else:
        acts[actID].chapters[chapterID].scenes[sceneID].run()


def endScene(actID, chapterID=None):
    '''
    Wrapper function that makes ending a desired scene easier
    '''
    if(chapterID == None):
        acts[actID].end()
    else:
        acts[actID].chapters[chapterID].end()


def getAnswer(actID, chapterID, sceneID):
    '''
    Gets the desired answer as asked for for future use, watching out for errors
    '''
    try:
        return storyProgress[actID][chapterID][sceneID][0]
    except:
        return "Fail"


def act1():
    '''
    Runs act 1 only
    '''
    runScene(0)
    runScene(0, 0)
    runScene(0, 0, 0)
    player.name = getAnswer(0, 0, 0)
    runScene(0, 0, 1)
    if(getAnswer(0, 0, 1) == "B"):
        runScene(0, 0, 2)
    runScene(0, 0, 3)
    if(getAnswer(0, 0, 3) == "A"):
        runScene(0, 0, 4)
    else:
        runScene(0, 0, 5)
        bp.update(getAnswer(0, 0, 5), completeStoryline[0][2][0][2][5][4])
    runScene(0, 0, 6)
    if(getAnswer(0, 0, 6) == "A"):
        runScene(0, 0, 7)
        player.statModify(0, 0, 1)
    elif(getAnswer(0, 0, 6) == "B"):
        runScene(0, 0, 8)
        player.statModify(1, 0, 0)
    else:
        player.statModify(0, 1, 0)
    runScene(0, 0, 9)
    endScene(0, 0)
    runScene(0, 1)
    runScene(0, 1, 0)
    if(getAnswer(0, 1, 0) == "A"):
        runScene(0, 1, 2)
        player.statModify(0, -2, 0)
    else:
        runScene(0, 1, 1)
        if(getAnswer(0, 1, 1) == "A"):
            runScene(0, 1, 3)
            player.statModify(0, -1, 0)
        else:   
            runScene(0, 1, 4)
    runScene(0, 1, 5)
    endScene(0, 1)
    runScene(0, 2)
    runScene(0, 2, 0)
    if(getAnswer(0, 2, 0) == "A"):
        runScene(0, 2, 1)
    else:
        runScene(0, 2, 2)
    runScene(0, 2, 3)
    if(getAnswer(0, 2, 3) == "A"):
        runScene(0, 2, 4)
        player.statModify(1, -1, 0)
    else:
        runScene(0, 2, 5)
        player.statModify(-1, 1, 0)
    runScene(0, 2, 6)
    if(getAnswer(0, 2, 6) == "A"):
        runScene(0, 2, 8)
        if('GPS' in bp.cb):
            runScene(0, 2, 9)
    else:
        runScene(0, 2, 7)
    runScene(0, 2, 10)
    endScene(0, 2)
    runScene(0, 3)
    runScene(0, 3, 0)
    if(getAnswer(0, 3, 0) == "A"):
        runScene(0, 3, 5)
    elif('Flashlight' in bp.cb):
        runScene(0, 3, 1)
    else:
        runScene(0, 3, 2)
    if(getAnswer(0, 3, 0) != "A"):
        if("A" in [getAnswer(0, 3, 1), getAnswer(0, 3, 2)]):
            runScene(0, 3, 3)
            player.statModify(0, 0, 1)
        else:
            runScene(0, 3, 4)
            player.statModify(1, 0, 0)
    endScene(0, 3)
    runScene(0, 4)
    runScene(0, 4, 0)
    player.statModify(0, 1, 0)
    if(getAnswer(0, 4, 0) == "B"):
        runScene(0, 4, 1)
    else:
        runScene(0, 4, 2)
    runScene(0, 4, 3)
    if(getAnswer(0, 4, 3) == "A"):
        runScene(0, 4, 4)
        if(player.str >= 7):
            runScene(0, 4, 5)
        else:
            runScene(0, 4, 6)
            player.statModify(0, -1, 0)
    runScene(0, 4, 7)
    if(getAnswer(0, 4, 7) == "A"):
        runScene(0, 4, 8)
    else:
        runScene(0, 4, 9)
    runScene(0, 4, 10)
    if('Baseball bat' in bp.cb):
        runScene(0, 4, 11)
    else:
        runScene(0, 4, 12)
        player.statModify(0, -1, 0)
    runScene(0, 4, 13)
    endScene(0, 4)
    endScene(0)
    
    
def act2():
    '''
    Runs only act 2
    '''
    runScene(1)
    runScene(1, 0)
    runScene(1, 0, 0)
    runScene(1, 0, 1)
    runScene(1, 0, 2)
    if(getAnswer(1, 0, 2) == "B"):
        runScene(1, 0, 3)
    if(getAnswer(1, 0, 3) == "B"):
        runScene(1, 0, 5)
    else:
        runScene(1, 0, 4)
    endScene(1, 0)
    runScene(1, 1)
    runScene(1, 1, 0)
    runScene(1, 1, 4)
    if(getAnswer(1, 1, 4) == "A"):
        runScene(1, 1, 1)
        player.statModify(0, 1, 0)
    elif(getAnswer(1, 1, 4) == "B"):
        runScene(1, 1, 2)
    elif(getAnswer(1, 1, 4) == "C"):
        runScene(1, 1, 3)
    runScene(1, 1, 5)
    runScene(1, 1, 6)
    runScene(1, 1, 7)
    if(getAnswer(1, 1, 7) == "A"):
        runScene(1, 1, 8)
        player.statModify(0, 0, -1)
    else:
        runScene(1, 1, 9)
        player.statModify(0, 0, 1)
    runScene(1, 1, 10)
    endScene(1, 1)
    runScene(1, 2)
    runScene(1, 2, 0)
    runScene(1, 2, 1)
    if(getAnswer(1, 2, 1) == "B"):
        runScene(1, 2, 2)
        player.die("was killed by a grenade explosion")
        return
    runScene(1, 2, 3)
    if(getAnswer(1, 2, 3) == "A"):
        runScene(1, 2, 4)
    else:
        runScene(1, 2, 5)
    runScene(1, 2, 6)
    endScene(1, 2)
    runScene(1, 3)
    runScene(1, 3, 0)
    if(getAnswer(1, 3, 0) == "A"):
        runScene(1, 3, 2)
    else:
        runScene(1, 3, 1)
    runScene(1, 3, 3)
    player.statModify(-1, 0, 0)
    runScene(1, 3, 4)
    if(getAnswer(1, 3, 4) == "A"):
        runScene(1, 3, 5)
    else:
        runScene(1, 3, 6)
    runScene(1, 3, 7)
    if(getAnswer(1, 3, 7) == "A"):
        runScene(1, 3, 8)
        player.statModify(0, -1, 0)
    else:
        runScene(1, 3, 9)
    runScene(1, 3, 10)
    if(getAnswer(1, 3, 10) == "A"):
        runScene(1, 3, 11)
        player.die("was shot and killed by zombie soldiers")
        return
    runScene(1, 3, 12)
    bp.update("A", {"A" : "Mysterious Crystal"})
    runScene(1, 3, 13)
    endScene(1, 3)
    runScene(1, 4)
    runScene(1, 4, 0)
    if(getAnswer(1, 4, 0) == "A"):
        runScene(1, 4, 2)
        player.die("was shot and killed by Brock")
        return
    runScene(1, 4, 1)
    runScene(1, 4, 3)
    if(player.kno >= 7):
        runScene(1, 4, 5)
    else:
        runScene(1, 4, 4)
    runScene(1, 4, 6)
    if(getAnswer(1, 4, 6) == "A"):
        runScene(1, 4, 7)
        player.die("was brutally dismembered by the zombie horde")
        return
    runScene(1, 4, 8)
    time.sleep(1)
    runScene(1, 4, 9)
    endScene(1, 4)
    endScene(1)


def act3():
    '''
    Runs only Act 3
    ''' 
    runScene(2)
    runScene(2, 0)
    runScene(2, 0, 0)
    runScene(2, 0, 1)
    if(getAnswer(2, 0, 1) == "A"):
        runScene(2, 0, 2)
        player.statModify(1, 0, 0)
    elif(getAnswer(2, 0, 1) == "B"):
        runScene(2, 0, 3)
        player.statModify(0, 0, 1)
    else:
        runScene(2, 0, 4)
        player.statModify(0, 1, 0)
    runScene(2, 0, 5)
    if(getAnswer(2, 0, 5) == "A"):
        runScene(2, 0, 6)
    else:
        runScene(2, 0, 7)
    runScene(2, 0, 8)
    if(getAnswer(2, 0, 8) == "A"):
        runScene(2, 0, 9)
    runScene(2, 0, 10)
    endScene(2, 0)
    runScene(2, 1)
    runScene(2, 1, 0)
    if(getAnswer(2, 1, 0) == "B"):
        runScene(2, 1, 2)
    runScene(2, 1, 1)
    endScene(2, 1)
    runScene(2, 2)
    runScene(2, 2, 0)
    if(getAnswer(2, 2, 0) == "B"):
        runScene(2, 2, 1)
        player.statModify(0, 0, 1)
    runScene(2, 2, 2)
    runScene(2, 2, 3)
    if(getAnswer(2, 2, 3) == "A"):
        runScene(2, 2, 4)
        player.die("was crushed under a collapsing staircase")
        return
    runScene(2, 2, 5)
    endScene(2, 2)
    runScene(2, 3)
    runScene(2, 3, 0)
    if(getAnswer(2, 3, 0) == "A"):
        runScene(2, 3, 1)
    runScene(2, 3, 2)
    if(getAnswer(2, 3, 2) == "A"):
        runScene(2, 3, 3)
    else:
        runScene(2, 3, 4)
    time.sleep(1)
    runScene(2, 3, 5)
    if(getAnswer(2, 3, 5) == "A"):
        runScene(2, 3, 6)
        player.statModify(0, -2, 0)
    runScene(2, 3, 7)
    time.sleep(1)
    runScene(2, 3, 8)
    endScene(2, 3)
    runScene(2, 4)
    runScene(2, 4, 0)
    time.sleep(1)
    runScene(2, 4, 1)
    time.sleep(1)
    runScene(2, 4, 2)
    time.sleep(2)
    endScene(2, 4)
    endScene(2)
    
    
def resetAdv():
    '''
    Resets all variables to restart the text adventure
    '''
    storyProgress[:] = []
    player.statSet(5, 5, 5)
    bp.cb = []
    createStoryline()
    createStorage()
    
    
def testBob():
    '''
    Test function only, used to determine if sys import package is already present. 
    Useful for debugging; end user will never need to execute/view this function
    '''
    if(True):
        print("bob")
        sys.exit()
    print("notbob")
        
        
def adv(showIntroduction=True):
    '''
    Runs the entire text adventure
    '''
    resetAdv()
    if showIntroduction:
        introduction()
    instructions()
    act1()
    act2()
    act3()


#Intro text when file is run
print()
print("Recommended settings: iPython full screen, background applications closed,",
       "quiet surroundings.\n")
print("WARNING: Estimated playing time: 1.5 - 2 hours assuming only 1 death.\n")
print("Type 'adv()' without the quotes and hit enter to begin.\n")
