from psychopy.visual import Window, TextStim
from psychopy.core import wait, Clock, StaticPeriod, quit
from psychopy.event import waitKeys, Mouse
from psychopy import gui
import random, os
import string
import numpy
import calendar
from itertools import chain
import locale
from datetime import datetime

#------------------------------------------- CHANGE PARAMETERS HERE ----------------------------------------------------

numOfBlocks = 1 #change how many blocks to do

practiceN = 5 #change amount of practice trials

soa = [0.0, 0.0167, 0.0334, 0.0501, 0.0668] #stimulus onset asynchrony, needs to be always 5 values

delayForMask = 0.6 #in seconds

lang = 'de_DE' #this may have to be changed depending on OS locale e.g. de_AT for austria

windowSize = [1280, 720]

fullScr = False

quitkey = 'escape' #key for quiting experiment, maybe set to something the participant wont press on accident

#values for random inter trial delay in specific range:
lowerLimit = 0.4
upperLimit = 0.7
increment = 0.1

#text formatting options:
fixationHeight = 0.09

units = 'norm'
textStimHeight = 0.06

posLeft = [-0.4, 0]
posRight = [0.4, 0]


#further tweaks for the practice trials have to be set in the corresponding code chunk below (beginning at line 482)

#-----------------------------------------------------------------------------------------------------------------------

clock = Clock()

#genrate random dates in the form of - JAN 15 - MAI 23 - etc. change lang to generate in different languages
def randomdate(dateNumber = 200, year = 2019, language = lang):
    locale.setlocale(locale.LC_ALL, language)
    dates = []
    monthRange = list(range(1,13,1))
    for date in range(dateNumber):
        month = calendar.month_abbr[random.choice(monthRange)]
        day = list(range(calendar.monthrange(year, random.choice(monthRange))[1]))[1:]
        day.insert(len(day), len(day)+1)
        day = random.choice(day)
        dates.append(' '.join((month.upper(), str(day))))
    return(dates)

#generate interTrialDelay
def interTrialDelay():
   x = round(float(random.choice(list(numpy.arange(lowerLimit, upperLimit, increment)))), 1)
   return(x)

#dialog interface with demographics input
demographicsWindow = gui.Dlg(title = 'testApp')
demographicsWindow.addField('ID: ', '45', color = 'Red')
demographicsWindow.addText('please enter your information')
demographicsWindow.addField('first name: ', 'Peter')
demographicsWindow.addField('last name: ','Huber')
demographicsWindow.addField('country: ', 'Huberstria')
demographicsWindow.addField('adress of your childhood: ', 'Huberstria Street')
demographicsWindow.addField('birthday - (e.g.: JAN 15): ', 'JAN 15')
demographicsWindow.addField('favorite animal: ', 'OCTOPUS')
demographicsWindow.addField('age: ', 35)
#0 is degrade 1 is masked
demographicsWindow.addField('version', '0')

demographics = demographicsWindow.show()

if demographicsWindow.OK:
    personInfo = demographics
else:
    print('user cancel')

expTime = Clock()
startTime = expTime.getTime()
startDate = datetime.now().strftime("%Y%m%d%H%M")

class person:
    pass
    
person.id = demographics[0]
person.first = demographics[1].upper()
person.last = demographics[2].upper()
person.country = demographics[3].upper()
person.adress = demographics[4].upper()
person.birth = demographics[5].upper()
person.animal = demographics[6].upper()
person.age = demographics[7]

expVersion = int(demographics[8])

#setup Window
win = Window(windowSize, fullscr=fullScr, waitBlanking=True, color='grey')


#-------------------------------- FRAMERATE CHECK ----------------------------------------
if win.getActualFrameRate() > 62:
    print('Warning!!! Actual FrameRate is above 60Hz, display times may be inaccurate!!!')
    print('Actual Framerate is: ', win.getActualFrameRate())
    print('If you want to proceed anyway, delete or comment the corresponding lines of code')
    quit() #delete this line if you want to proceed anyway
#-----------------------------------------------------------------------------------------


fixationCross = TextStim(win, text = '+', units='norm', height= fixationHeight)

practiceInstructions = '\
Herzlich willkommen, und vielen Dank fürs Teilnehmen! \n\
\n\
Im folgenden Teil dieses Experiments werden Sie einige Übungsaufgaben bearbeiten \n\
\n \
Auf dem Bildschirm werden Sie widerholt 2 Wörter sehen (eines links, eines rechts). Ihre Aufgabe ist festzustellen welches dieser beiden Wörter für Sie zuerst zu sehen war. \n\
Wenn Sie der Meinung sind, dass das linke Wort zuerst zu sehen war, drücken Sie die "f" Taste. Wenn Sie der Meinung sind, dass das rechte Wort zuerst zu sehen war drücken Sie die "j" Taste. \n\
Falls Sie sich nicht entscheiden können, drücken Sie die "Leertaste". \n\
In den Übungsaufgaben wird Ihnen nach jedem Durchgang kurz angezeigt, ob Ihre Antwort "richtig" oder "falsch" war.\n\
Bitte bearbeiten Sie die Aufgaben aufmerksam und konzentriert! Andernfalls könnten Ihre Daten für uns unbrauchbar sein.\n\
\n Drücken Sie nun die "Leertaste" um zu beginnen.'

practiceEndText = 'Die Übungsrunden sind nun zu Ende. Nun folgt das tatsächliche Experiment. \
darin wird Ihnen nun kein Feedback mehr gegeben und es werden auch keine "links", "rechts" Markierungen mehr angezeigt damit Sie sich \
nur auf die Namen konzentrieren können.\n\n\
Wenn Sie die "Leertaste" drücken beginnt das Experiment.'

mainLoopInstructions = ''

AppEndText = 'Das Experiment is nun vorbei. Vielen Dank für die Teilnahme!\n\
Falls Sie noch Fragen haben, wenden Sie sich bitte an den Experimentalleiter.\n\n\
Auf Wiedersehen.'

unfamFirstNames = [u"Nico", u"Justin", u"Jakob",
u"Gerald", u"Max", u"Mario", u"Jürgen", u"Ferdinand", u"Simon", 
u"Harald", u"Andre", u"Gregor", u"Martin", u"Julian", u"Berat", 
u"Robert", u"Leonard", u"Theodor", u"Arthur", u"Emir", u"Theo", 
u"Marcel", u"Lorenz", u"Moritz", u"Samuel", u"Stefan", u"Anton", 
u"Felix", u"Herbert", u"Clemens", u"Gerhard", u"Peter", u"Sascha", 
u"Richard", u"Günther", u"Ali", u"Johann", u"Nicolas", u"Leo", u"Alexander", 
u"Emanuel", u"Manfred", u"Klaus", u"Roland", u"Laurenz", u"Valentin", u"Dominik",
u"Marvin", u"Helmut", u"Hamza", u"Viktor", u"Jonathan", u"Josef", u"Christoph", 
u"Markus", u"Pascal", u"Maximilian", u"Finn", u"Mathias", u"Rafael", u"Roman", 
u"Yusuf", u"Manuel", u"Oliver", u"Rene", u"Karl", u"Adam", u"Christopher", u"Jan",
u"Kilian", u"Michael", u"Jonas", u"Werner", u"Kevin", u"David", u"Emil", 
u"Constantin", u"Noah", u"Bernhard", u"Bernd", u"Georg", u"Marco", u"Florian", 
u"Franz", u"Fabio", u"Wolfgang", u"Thomas", u"Vincent", u"Christian", u"Andreas",
u"Erik", u"Johannes", u"Tobias", u"Benjamin", u"Ben", u"Sandro", u"Armin", u"Daniel",
u"Reinhard", u"Benedikt", u"Amir", u"Gernot", u"Elias", u"Gabriel", u"Patrik",
u"Andrej", u"Konstantin", u"Oskar", u"Sebastian", u"Matthias", u"Fabian",
u"Hannes", u"Paul", u"Leon", u"Tim", u"Leopold", u"Adrian"]

unfamSecondNames = [u"Nico", u"Justin", u"Jakob",
u"Gerald", u"Max", u"Mario", u"Jürgen", u"Ferdinand", u"Simon", 
u"Harald", u"Andre", u"Gregor", u"Martin", u"Julian", u"Berat", 
u"Robert", u"Leonard", u"Theodor", u"Arthur", u"Emir", u"Theo", 
u"Marcel", u"Lorenz", u"Moritz", u"Samuel", u"Stefan", u"Anton", 
u"Felix", u"Herbert", u"Clemens", u"Gerhard", u"Peter", u"Sascha", 
u"Richard", u"Günther", u"Ali", u"Johann", u"Nicolas", u"Leo", u"Alexander", 
u"Emanuel", u"Manfred", u"Klaus", u"Roland", u"Laurenz", u"Valentin", u"Dominik",
u"Marvin", u"Helmut", u"Hamza", u"Viktor", u"Jonathan", u"Josef", u"Christoph", 
u"Markus", u"Pascal", u"Maximilian", u"Finn", u"Mathias", u"Rafael", u"Roman", 
u"Yusuf", u"Manuel", u"Oliver", u"Rene", u"Karl", u"Adam", u"Christopher", u"Jan",
u"Kilian", u"Michael", u"Jonas", u"Werner", u"Kevin", u"David", u"Emil", 
u"Constantin", u"Noah", u"Bernhard", u"Bernd", u"Georg", u"Marco", u"Florian", 
u"Franz", u"Fabio", u"Wolfgang", u"Thomas", u"Vincent", u"Christian", u"Andreas",
u"Erik", u"Johannes", u"Tobias", u"Benjamin", u"Ben", u"Sandro", u"Armin", u"Daniel",
u"Reinhard", u"Benedikt", u"Amir", u"Gernot", u"Elias", u"Gabriel", u"Patrik",
u"Andrej", u"Konstantin", u"Oskar", u"Sebastian", u"Matthias", u"Fabian",
u"Hannes", u"Paul", u"Leon", u"Tim", u"Leopold", u"Adrian"]

#read text files with stimuli, if no text files replace righthandside with list of names/strings like
#above for unfamSecondNames
if expVersion == 0:
    unfamCountries = open('countries.txt', 'r').read().upper().split(',')
    unfamAdresses = open('street.txt', 'r').read().upper().split(',')
    unfamBirthdays = randomdate(300, 2019)
    unfamAnimals = open('animals.txt','r').read().upper().split(',')
    unfamFirstNames = [i.upper() for i in unfamFirstNames]
    unfamSecondNames = [i.upper() for i in unfamSecondNames]
    
if expVersion == 1:
    unfamCountries = open('countries.txt', 'r').read().lower().split(',')
    unfamAdresses = open('street.txt', 'r').read().lower().split(',')
    unfamBirthdays = randomdate(300, 2019)
    unfamAnimals = open('animals.txt','r').read().lower().split(',')
    unfamFirstNames = [i.lower() for i in unfamFirstNames]
    unfamSecondNames = [i.lower() for i in unfamSecondNames]

#func to insert the "%" charakter between every character of input word
def garbleWord(*arg):
    k='%' #change for other garbling character
    N=1

    args = list(arg)
    outList = []
    
    for word in args:
        word = list(word)
        word = list(chain(*[word[i : i+N] + [k]
                            if len(word[i : i+N]) == N
                            else word[i : i+N]
                            for i in range(0, len(word), N)]))
        word.insert(0, '%')
        word = ''.join(word[:]).upper()
        outList.append(word)
    return(outList)

#function to prepare shown names/words in trials
def choseItemsForDisplay(blockN = 1, trialsPerBlock = 216):
    trialsPerBlock += 24
    
    #set the unfamiliar words once, so they are always the same for all trials
    unfamFirst = random.choice(unfamFirstNames)
    unfamSecond = random.choice(unfamSecondNames)
    unfamCountry = random.choice(unfamCountries)
    unfamAdress = random.choice(unfamAdresses)
    unfamBirthday = random.choice(unfamBirthdays)
    unfamAnimal = random.choice(unfamAnimals)

    #is hardcoded but it doesnt actually matter, because trialsPerBlock cannot be changed
    classes = (['firstName'] * 40
        + ['lastName'] * 40
        + ['country'] * 40
        + ['adress'] * 40
        + ['birthday'] * 40
        + ['animal'] * 40)

    onsetDelay = soa * int(len(classes)/5)
    side =   [-1,1,1,-1] * int(len(classes)/4) #-1 is left 1 is right
    first =   [1,0,1,0] * int(len(classes)/4) #1 indicates that the unfamWord should be displayed first, 0 indicates that its diplayed second
    
    finalItems = {}
    
    #iterate through all lists above
    for j,k in enumerate(classes):

        if k == 'firstName':
            finalItems[j] = {'class':k, 'unfamWord':unfamFirst, 'famWord':person.first, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

        if k == 'lastName':
            finalItems[j] = {'class':k, 'unfamWord':unfamSecond,'famWord':person.last, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

        if k == 'country':
            finalItems[j] = {'class':k, 'unfamWord':unfamCountry,'famWord':person.country, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

        if k == 'adress':
            finalItems[j] = {'class':k, 'unfamWord':unfamAdress,'famWord':person.adress, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

        if k == 'birthday':
            finalItems[j] = {'class':k, 'unfamWord':unfamBirthday,'famWord':person.birth, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

        if k == 'animal':
            finalItems[j] = {'class':k, 'unfamWord':unfamAnimal,'famWord':person.animal, 'delay':onsetDelay[j], 'side':side[j], 'first':first[j]}

    garbled = [1,1,1,1,0,0,0,0] * int(len(finalItems)/8) #indication if words for item should be garbled (1) or not (0)
    for i in range(len(finalItems)):
        finalItems[i]['garbled'] = garbled[i]

    #find and remove unnecessary zeros; this is just for info which items (1/2 of 0 delay trials) should be removed
    kl = []
    for k,v in finalItems.items():
        if v['delay'] == 0.0:
            if v['garbled'] == 1 or v['garbled'] == 0:
                kl.append(k)
    
    #indexes to remove; did not find an easy way of removing them correcly besides hardcoding the structure of the unwanted zero indexes
    #in the future i will look into it how to do that in a better way
    delIndex = [kl[0:4], kl[8:12], kl[16:20], kl[24:28], kl[32:36], kl[40:44]]
    
    for i in delIndex:
        for j in i:
            del finalItems[j]
    
    #return everything for the finalItems function
    return(finalItems)

#func for generating masks of same length as masked stimulus
def makeMask(char):
    maskList = []
    letters = list(string.ascii_uppercase)*5
    random.shuffle(letters)
    
    for i in range(len(char)):
        maskList.append(random.choice(letters))
        
    mask = ''.join(maskList)
    return(mask)
    
#func to generate the final psychopy.textstim objects and store them together with 
#other item infos in the final dictionary
def finalItems(blockN):
    rawItems = choseItemsForDisplay()
    
    letters = list(string.ascii_uppercase)*5
    random.shuffle(letters)
    
    finalItems = {}
    
    for i in range(216):
        finalItemIndex = random.choice(list(rawItems))
        itemToDisplay = rawItems[finalItemIndex]
        del rawItems[finalItemIndex]
        
        #timeDelayBetweenNames = float(itemToDisplay['delay'])
        
        #generate the final dictionary
        if itemToDisplay['garbled'] == 1 and expVersion == 0: #garble items if garbled = 1 and only if it is garble version of experiment
            garbledList = garbleWord(itemToDisplay['unfamWord'], itemToDisplay['famWord'])
            
            if itemToDisplay['side'] == -1 and itemToDisplay['first'] == 1:
                #this "copied" code below is just for better understanding whats happening here, could be shortened
                nameLeftFirst = garbledList[0]
                nameRightSecond = garbledList[1]
                
                nameToDrawFirst = TextStim(win, nameLeftFirst, units='norm', pos=(posLeft), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameRightSecond, units='norm', pos=(posRight), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                #if expVersion = 1, generate masks for stimuli
                else:
                    mask1 = makeMask(nameToDrawFirst.text.replace('%',''))
                    mask2 = makeMask(nameToDrawSecond.text.replace('%',''))
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posLeft), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posRight), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == 1 and itemToDisplay['first'] == 1:
                nameLeftSecond = garbledList[1]
                nameRightFirst = garbledList[0]
                
                nameToDrawFirst = TextStim(win, nameRightFirst, units='norm', pos=(posRight), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameLeftSecond, units='norm', pos=(posLeft), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text.replace('%',''))
                    mask2 = makeMask(nameToDrawSecond.text.replace('%',''))
            
                    firstMask = TextStim(win,mask1, units='norm', pos=(posRight), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posLeft), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == -1 and itemToDisplay['first'] == 0:
                nameLeftSecond = garbledList[0]
                nameRightFirst = garbledList[1]
                
                nameToDrawFirst = TextStim(win, nameRightFirst, units='norm', pos=(posRight), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameLeftSecond, units='norm', pos=(posLeft), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text.replace('%',''))
                    mask2 = makeMask(nameToDrawSecond.text.replace('%',''))
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posRight), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posLeft), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == 1 and itemToDisplay['first'] == 0:
                nameLeftFirst = garbledList[1]
                nameRightSecond = garbledList[0]
                
                nameToDrawFirst = TextStim(win, nameLeftFirst, units='norm', pos=(posLeft), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameRightSecond, units='norm', pos=(posRight), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text.replace('%',''))
                    mask2 = makeMask(nameToDrawSecond.text.replace('%',''))
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posLeft), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posRight), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
        else: #if garbled = 0
            
            if itemToDisplay['side'] == -1 and itemToDisplay['first'] == 1:
                nameLeftFirst = itemToDisplay['unfamWord']
                nameRightSecond = itemToDisplay['famWord']
                
                nameToDrawFirst = TextStim(win, nameLeftFirst, units='norm', pos=(posLeft), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameRightSecond, units='norm', pos=(posRight), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text)
                    mask2 = makeMask(nameToDrawSecond.text)
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posLeft), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posRight), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == 1 and itemToDisplay['first'] == 1:
                nameLeftSecond = itemToDisplay['famWord']
                nameRightFirst = itemToDisplay['unfamWord']
                
                nameToDrawFirst = TextStim(win, nameRightFirst, units='norm', pos=(posRight), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameLeftSecond, units='norm', pos=(posLeft), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text)
                    mask2 = makeMask(nameToDrawSecond.text)
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posRight), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posLeft), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == -1 and itemToDisplay['first'] == 0:
                nameLeftSecond = itemToDisplay['unfamWord']
                nameRightFirst = itemToDisplay['famWord']
                
                nameToDrawFirst = TextStim(win, nameRightFirst, units='norm', pos=(posRight), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameLeftSecond, units='norm', pos=(posLeft), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text)
                    mask2 = makeMask(nameToDrawSecond.text)
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posRight), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posLeft), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
                
            elif itemToDisplay['side'] == 1 and itemToDisplay['first'] == 0:
                nameLeftFirst = itemToDisplay['famWord']
                nameRightSecond = itemToDisplay['unfamWord']
                
                nameToDrawFirst = TextStim(win, nameLeftFirst, units='norm', pos=(posLeft), height=textStimHeight)
                nameToDrawSecond = TextStim(win, nameRightSecond, units='norm', pos=(posRight), height=textStimHeight)
                
                if expVersion == 0:
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'itemInfo': itemToDisplay}
                else:
                    mask1 = makeMask(nameToDrawFirst.text)
                    mask2 = makeMask(nameToDrawSecond.text)
            
                    firstMask = TextStim(win, mask1, units='norm', pos=(posLeft), height=textStimHeight)
                    secondMask = TextStim(win, mask2, units='norm', pos=(posRight), height=textStimHeight)
                    
                    finalItems[i] = {'firstName':nameToDrawFirst, 'secondName':nameToDrawSecond, 'firstMask':firstMask,\
                    'secondMask':secondMask, 'itemInfo': itemToDisplay}
            
    return(finalItems)

def practiceLoop(trials):
    
    practiceInfo = TextStim(win, practiceInstructions, units='norm', pos=(0,0), height=0.05, wrapWidth=0.9)
    practiceInfo.draw()
    win.flip()
    
    if waitKeys(keyList=['space']):
        pass
    
    fixationCross.draw()
    win.flip()
    wait(0.6)
    
    t1 = clock.getTime()
    win.flip()
    
    print(clock.getTime() - t1)
    
    namesLeft = []
    namesRight = []
    
    for i in range(trials*2):
        namesLeft.append(random.choice(unfamFirstNames))
        namesRight.append(random.choice(unfamFirstNames))
    
    for i in range(trials):
    
        timeDelay = random.choice([0.0, 0.0334, 0.0835, 0.1, 0.2])
        print('delay should be: ', timeDelay)
        
        waitDuration = StaticPeriod()
        waitDuration.start(0.6)
        
        left = namesLeft[i]
        right = namesRight[i]
        
        leftName = TextStim(win, left, units='norm', pos=(posLeft), color=(1,0,0), height=0.1)
        rightName = TextStim(win, right, units='norm', pos=(posRight), color=(1,0,0), height=0.1)
        
        answer_infoLeft = TextStim(win, 'links', units='norm', pos=(-0.8, -0.7), height=0.1)
        answer_infoRight = TextStim(win, 'rechts', units='norm', pos=(0.8, -0.7), height=0.1)
        answer_infoDontKnow = TextStim(win, "unsicher", units='norm', pos=(0, -0.8), height=0.1)
        
        correct = TextStim(win, 'richtig!', units='norm', pos=(0, 0))
        incorrect = TextStim(win, 'falsch!', units='norm', pos=(0, 0))

        #randomly chose which name will be shown first aand the other will then be second
        nameToDrawFirst = random.choice([leftName, rightName])

        if nameToDrawFirst == leftName:
            nameToDrawSecond = rightName
        else:
            nameToDrawSecond = leftName
        
        stimuli = [nameToDrawFirst, answer_infoLeft, answer_infoRight, answer_infoDontKnow]
        fullStimuli = [nameToDrawFirst, nameToDrawSecond, answer_infoLeft, answer_infoRight, answer_infoDontKnow]
        
        for s in stimuli:
            s.draw()
        
        print('ANSWER: ', nameToDrawFirst.text)
        
        waitDuration.complete()
        
        #make flip and take time
        win.flip()
        t1=clock.getTime()
        
        waitDuration.start(timeDelay)
        
        for s in fullStimuli:
            s.draw()
        
        waitDuration.complete()
        
        win.flip()
        t2 = clock.getTime()
        print('effective time delay: ', t2-t1)
        
        #start response time window
        responseStart = clock.getTime()
        
        #wait a specific amount of time for the keypress
        pressedKey = waitKeys(keyList=['f','j','space', quitkey])
        
        #only for simulating agents
        #pressedKey = random.choice(['f','j'])
        
        responseEnd = clock.getTime()
        
        #calculate response time 
        RT = responseEnd - responseStart
        
        if quitkey in pressedKey:
            win.close()
        
        print('response time: ', RT)
        
        if 'f' in pressedKey and nameToDrawFirst.text == leftName.text:
            correct.draw()
            win.flip()
            wait(0.4)
        elif 'j' in pressedKey and nameToDrawFirst.text == rightName.text:
            correct.draw()
            win.flip()
            wait(0.4)
        elif 'j' in pressedKey and nameToDrawFirst.text != rightName.text:
            incorrect.draw()
            win.flip()
            wait(0.4)
        elif 'f' in pressedKey and nameToDrawFirst.text != leftName.text:
            incorrect.draw()
            win.flip()
            wait(0.4)
        
        fixationCross.draw()
        win.flip()
        wait(0.6)
        win.flip()
        
    TextStim(win, practiceEndText, pos=(0,0), height=0.08, wrapWidth=0.9).draw()
    win.flip()
    #fixationCross.draw()
    waitKeys(keyList=['space'])
    wait(0.4)
    win.flip()
    wait(0.2)
    win.flip()
    
#main loop, blocks can be changed and are then a multiple of "trialNumber" trials
#after each block the loop is halted for possible breaks and continues with "space" press
def mainLoop(blocks=1, trialNumber=216):

    #global blockCount
    blockCount = 0

    trialCount = 0
    timer = Clock()
    
    maskDelay = delayForMask
    
    #make finalItems which will be reused for every block
    generatedItems = finalItems(blocks)
    itemsForDisplay = generatedItems
    
    #main trial loop runns for n-blocks
    for block in range(blocks):
        
        #f' is the python3 equivalent of "something{}something.format()" function for python2
        betweenBlocksInfo = (f'Der {blockCount}. Block ist nun vorbei, wenn Sie möchten können Sie eine kurze Pause machen.\n\
        \n\
        Fortfahren mit "Leertaste".') 
        
        if blockCount == blocks-1 and blockCount > 0:
            TextStim(win, (f'Der {blockCount}. Block ist nun vorbei, wenn Sie möchten können Sie eine kurze Pause machen. Nun folgt der letzte Durchgang.\n\
            \n\
Fortfahren mit "Leertaste".'), units='norm', pos=(0.0,0.0)).draw()
            win.flip()
            waitKeys(keyList=['space'])
        elif blockCount > 0:
            TextStim(win, betweenBlocksInfo, units='norm', pos=(0.0,0.0)).draw()
            win.flip()
            waitKeys(keyList=['space'])
        
        fixationCross.draw()
        win.flip()
        wait(0.6)
        win.flip()
        
        blockCount = block+1
        
        #loop run for n-trials
        for trial in range(trialNumber):
            if itemsForDisplay[trial]['itemInfo']['side'] == -1 and itemsForDisplay[trial]['itemInfo']['first'] == 1:
                corr = -1
            elif itemsForDisplay[trial]['itemInfo']['side'] == 1 and itemsForDisplay[trial]['itemInfo']['first'] == 1:
                corr = 1
            elif itemsForDisplay[trial]['itemInfo']['side'] == -1 and itemsForDisplay[trial]['itemInfo']['first'] == 0:
                corr = 1
            elif itemsForDisplay[trial]['itemInfo']['side'] == 1 and itemsForDisplay[trial]['itemInfo']['first'] == 0:
                corr = -1
                    
            timeDelayBetweenNames = itemsForDisplay[trial]['itemInfo']['delay']
            
            timer.reset()
            time1 = timer.getTime()
            intertDelay = 0 
            
            trialCount +=1
            
            waitDuration = StaticPeriod(screenHz=60)
            d = interTrialDelay()
            print('interTrialDelay: ', d)
            t1 = clock.getTime()
            
            if timeDelayBetweenNames != 0.0:
                waitDuration.start(d)
                
                nameToDrawFirst = itemsForDisplay[trial]['firstName']
                nameToDrawSecond = itemsForDisplay[trial]['secondName']
                if expVersion == 1:
                    mask1 = itemsForDisplay[trial]['firstMask']
                    mask2 = itemsForDisplay[trial]['secondMask']
                    maskStimuli = [mask1, mask2]
                    
                stimuli = [nameToDrawFirst, nameToDrawSecond]
                
            
                intertDelay += d
                
                print('delay should be: ', timeDelayBetweenNames)
                
                nameToDrawFirst.draw()
                
                waitDuration.complete()
                print('1. loop dur: ', clock.getTime() - t1)
                
                win.flip()
                t1 = clock.getTime()
                
                w1 = clock.getTime()
                waitDuration.start(timeDelayBetweenNames)
                for s in stimuli:
                    s.draw()
                waitDuration.complete()
                print('2. loop dur: ', clock.getTime() - w1)
                
                win.flip()
                realTimeDelay = clock.getTime() - t1
                print('effective time delay: ',  realTimeDelay)
                
                if expVersion == 1:
                    waitDuration.start(maskDelay)
                    for m in maskStimuli:
                        m.draw()
                    waitDuration.complete()
                    win.flip()
            
            else:
                waitDuration.start(d)
                
                nameToDrawFirst = itemsForDisplay[trial]['firstName']
                nameToDrawSecond = itemsForDisplay[trial]['secondName']
                
                if expVersion == 1:
                    mask1 = itemsForDisplay[trial]['firstMask']
                    mask2 = itemsForDisplay[trial]['secondMask']
                    maskStimuli = [mask1, mask2]
                    
                stimuli = [nameToDrawFirst, nameToDrawSecond]
                
                print('delay should be: ', timeDelayBetweenNames)
                
                for s in stimuli:
                    s.draw()
                waitDuration.complete()
                realTimeDelay = 0
                win.flip()
                
                print('effective time delay: ', realTimeDelay)
                
                if expVersion == 1:
                    waitDuration.start(maskDelay)
                    for m in maskStimuli:
                        m.draw()
                    waitDuration.complete()
                    win.flip()
                
            
            #start response record
            responseStart = clock.getTime()
            
            #wait a specific amount of time for the keypress
            pressedKey = waitKeys(keyList=['f','j','space', quitkey]) #escape for quiting the experiment
            
            #below just for simulating persons
#            pressedKey = random.choice(['f','j','space'])
#            wait(0.2)
            
            #end response clock
            responseEnd = clock.getTime()
            
            #calculate response time 
            RT = responseEnd - responseStart
            
            if pressedKey == None:
                pass
            elif quitkey in pressedKey:
                quit()
            print('response time: ', RT)
            
            correct = 0
            
            #if-else statements for 'possible' feedback and response recording
            if pressedKey == None:
                correct = 0
            elif itemsForDisplay[trial]['itemInfo']['delay'] == 0.0:
                correct = -2 #with 0 delay there cannot be a correct answer
            elif 'f' in pressedKey and corr == 1:
                print('incorrect')
                correct = 0
            elif 'j' in pressedKey and corr == -1:
                print('incorrect')
                correct = 0
            elif 'f' in pressedKey and corr == -1:
                print('correct')
                correct = 1
            elif 'j' in pressedKey and corr == 1:
                print('correct')
                correct = 1
            elif 'space' in pressedKey:
                correct = -1 # -1 then means didnt know
            
            win.flip()
            d = interTrialDelay()
            print('interTrialDelay: ', d)
            intertDelay += d
            wait(d)
            fixationCross.draw()
            win.flip()
            
            #aand again save the current trials while waiting the inter-trial duration instead of doing nothing
            d = interTrialDelay()
            print('interTrialDelay: ', d)
            t1 = clock.getTime()
            waitDuration.start(d)
            intertDelay += d
            interTrialDuration = intertDelay
            trialDuration = timer.getTime() - time1 + d
            
            #what is saved:
                #name class
                #if garbled or not
                #left name
                #right name
                #intended time delay
                #real time delay
                #which name was displayed first
                #response time
                #if the response was correct
                #person ID, first name, last name, country, adress
            
            if itemsForDisplay[trial]['itemInfo']['side'] == -1:
                leftName = itemsForDisplay[trial]['itemInfo']['unfamWord']
                rightName = itemsForDisplay[trial]['itemInfo']['famWord']
                leftNameType = 'unfamiliar'
                rightNameType = 'familiar'
            else:
                leftName = itemsForDisplay[trial]['itemInfo']['famWord']
                rightName = itemsForDisplay[trial]['itemInfo']['unfamWord']
                leftNameType = 'familiar'
                rightNameType = 'unfamiliar'
                
            if itemsForDisplay[trial]['itemInfo']['first'] == 1:
                firstNameType = 'unfamiliar'
            else:
                firstNameType = 'familiar'
                
            if os.path.isfile(f'exp_degrade_{person.id}_{startDate}.txt'):
                    with open(f'exp_degrade_{person.id}_{startDate}.txt', 'a') as file:
                        file.write('\t'.join([itemsForDisplay[trial]['itemInfo']['class'],str(itemsForDisplay[trial]['itemInfo']['garbled']),leftName ,\
                        rightName , leftNameType, rightNameType, str(itemsForDisplay[trial]['itemInfo']['delay']) , str(realTimeDelay), \
                        nameToDrawFirst.text.replace('%',''), firstNameType , str(RT) , str(pressedKey) ,str(correct) , str(blockCount) , str(trialCount) , person.id ,\
                        str(trialDuration), str(interTrialDuration)])+ '\n')
                
            else:
                    with open(f'exp_degrade_{person.id}_{startDate}.txt', 'w+') as file:
                        file.write('class\tgarbled\tleft Name\tright Name\tleftNameType\trightNameType\tintendedTimeDelay\trealTimeDelay\t\
nameShowedFirst\tfirstNameType\tresponseTime\tpressedKey\tcorrectAnswer\tblock\ttrial\tID\ttrialDuration\tinterTrialDuration' + '\n')
                    with open(f'exp_degrade_{person.id}_{startDate}.txt', 'a') as file:
                        file.write('\t'.join([itemsForDisplay[trial]['itemInfo']['class'],str(itemsForDisplay[trial]['itemInfo']['garbled']),leftName ,\
                        rightName , leftNameType, rightNameType, str(itemsForDisplay[trial]['itemInfo']['delay']) , str(realTimeDelay), \
                        nameToDrawFirst.text.replace('%',''), firstNameType , str(RT) , str(pressedKey) ,str(correct) , str(blockCount) , str(trialCount) , person.id ,\
                        str(trialDuration), str(interTrialDuration)])+ '\n')
                        
            waitDuration.complete()
            print('3. loop dur: ', clock.getTime() - t1)
            
            win.flip()
            
            print('trialDuration: ', trialDuration)
    
    endTime = expTime.getTime() - startTime
    #write person demographics
    with open(f'exp_degrade_{person.id}_{startDate}.txt', 'a') as file:
        file.write(' '.join(['experiment Duration: ', str(endTime),' ID: ',person.id,' first name: ',person.first,\
    ' last name: ',person.last,' country: ',person.country,\
    ' adress: ',person.adress,' birhtday: ',person.adress,' animal: ',person.animal]))
    
    TextStim(win, AppEndText, font='Calibri', units='norm', pos=(0,0), height = 0.08, wrapWidth=0.9).draw()
    win.flip()
    waitKeys(keyList=['escape'])

Mouse(visible = False)

practiceLoop(practiceN) 
mainLoop(numOfBlocks, 216)


