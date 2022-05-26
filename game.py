import gensim, pygame, random, difflib
import pandas as pd
from pygame.locals import *
from deep_translator import GoogleTranslator
from googletrans import Translator, constants
from pprint import pprint
import time

BLACK = (0,0,0)

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 1:
            self.clicked = False
                
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
#Pygame inicijavimas
pygame.init()

#surinkta tasku praeitame zaidime
collectedScore_font = pygame.font.SysFont(None,65)
collectedScoreNumber = 0
collectedScoreWordText = 'SURINKTA TAŠKŲ: '
collectedScoreText = ''
collectedScoreX = 110
collectedScoreY = 240

#rekordas
record_font = pygame.font.SysFont(None,65)
with open('D:/Data/record.txt') as f:
    recordNumber = f.readlines()[0]
f.close()
recordWordText = 'REKORDAS: '
recordText = recordWordText + str(recordNumber)
recordX = 110
recordY = 160

#rules
rules_font = pygame.font.SysFont(None,47)
rulesText = "Įrašyti žodį, kurio reikšmė išsiskiria"
rulesX = 90
rulesY = 240

#Score
score_font = pygame.font.SysFont(None,40)
scoreNumber = 0
scoreText = "Taškai: " + str(scoreNumber)
scoreX = 500
scoreY = 150

#Lifes
lifes_font = pygame.font.SysFont(None, 40)
lifesNumber = 3
lifesText = "Gyvybės: " + str(lifesNumber)
lifesX = 500
lifesY = 410

#answer
answer_font = pygame.font.SysFont(None, 60)
answerX = 150
answerY = 25

#FirstWord
font1 = pygame.font.SysFont(None, 60)
text1 = 'vienas'
firstWordX = 150
firstWordY = 150

#SecondWord
font2 = pygame.font.SysFont(None, 60)
text2 = 'du'
secondWordX = 150
secondWordY = 220

#ThirdWord
font3 = pygame.font.SysFont(None, 60)
text3 = 'trys' 
thirdWordX = 150
thirdWordY = 290

#FourthWord
font4 = pygame.font.SysFont(None, 60)
text4 = 'keturi'
fourthWordX = 150
fourthWordY = 360

input_font = pygame.font.Font(None, 60)
input_text = ''

def screenRender(listOfWords, answer, input_text, lifesText, scoreText):
    firstWordRender(listOfWords[0])
    secondWordRender(listOfWords[1])
    thirdWordRender(listOfWords[2])
    fourthWordRender(listOfWords[3])
    answerRender(answer)
    scoreRender(scoreText)
    lifesRender(lifesText)
        
    text_surface = input_font.render(input_text, True, (0,0,0))
    screen.blit(text_surface, (150, 450))
    pygame.display.update()
    
def startScreenRender(recordText, collectedScoreText):
    start_button.draw(screen)
    rules_button.draw(screen)
    recordRender(recordText)
    collectedScoreRender(collectedScoreText)
    text_surface = input_font.render(input_text, True, (0,0,0))
    screen.blit(text_surface, (150, 450))
    pygame.display.update()

def rulesScreenRender():
    back_button.draw(screen)
    rulesRender(rulesText)
    text_surface = input_font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (150, 450))
    pygame.display.update()

def collectedScoreRender(collectedScoreText):
    collectedScoreMeaning = collectedScore_font.render(collectedScoreText, True, BLACK)
    screen.blit(collectedScoreMeaning, (collectedScoreX, collectedScoreY))

def rulesRender(rulesText):
    rulesMeaning = rules_font.render(rulesText, True, BLACK)
    screen.blit(rulesMeaning, (rulesX, rulesY))

def recordRender(recordText):
    recordMeaning = record_font.render(recordText, True, BLACK)
    screen.blit(recordMeaning, (recordX, recordY))
        
def scoreRender(scoreText):
    scoreMeaning = score_font.render(scoreText, True, BLACK)
    screen.blit(scoreMeaning, (scoreX, scoreY))
    
def lifesRender(lifesText):
    lifesMeaning = lifes_font.render(lifesText, True, BLACK)
    screen.blit(lifesMeaning, (lifesX, lifesY))

def answerRender(text):
    answerMeaning = answer_font.render(text, True, BLACK)
    screen.blit(answerMeaning, (answerX, answerY))

def firstWordRender(text1):
    firstWordMeaning = font1.render(text1, True, BLACK)
    screen.blit(firstWordMeaning, (firstWordX, firstWordY))
   
    
def secondWordRender(text2):
    secondWordMeaning = font2.render(text2, True, BLACK)
    screen.blit(secondWordMeaning, (secondWordX, secondWordY))
    
    
def thirdWordRender(text3):
    thirdWordMeaning = font3.render(text3, True, BLACK)
    screen.blit(thirdWordMeaning, (thirdWordX, thirdWordY))
    
    
def fourthWordRender(text4):
    fourthWordMeaning = font4.render(text4, True, BLACK)
    screen.blit(fourthWordMeaning, (fourthWordX, fourthWordY))
    
def functionToTranslateWord(word):
    return GoogleTranslator(source='en', target='lt').translate(word)

def isSimilar(first, second):
    sequence = difflib.SequenceMatcher(isjunk=None, a=first, b=second)
    difference = sequence.ratio()*100
    difference = round(difference, 1)
    if difference < 60:
        if len(first) > len(second):
            if second in first:
                return True
            else:
                return False
        elif len(second) > len(first):
            if first in second:
                return True
            else:
                return False
        else:
            return False
    else:
        return True
def isSimilar100(first, second):
    sequence = difflib.SequenceMatcher(isjunk=None, a=first, b=second)
    difference = sequence.ratio()*100
    difference = round(difference, 1)
    if difference < 90:
        return False
    else:
        return True
    
def translatedWordsSuggestionsToList(dictionary):
    listOfWords = []
    lengths = []
    if dictionary.extra_data['all-translations'] != None:
        for x in range(len(dictionary.extra_data['all-translations'])):
            lengths.append(len(dictionary.extra_data['all-translations'][x][1]))
        max_value = max(lengths)
        max_index = lengths.index(max_value)
        listOfWords = listOfWords + dictionary.extra_data['all-translations'][max_index][1]
        for x in range(len(dictionary.extra_data['all-translations'])):
            if x != max_index:
                listOfWords = listOfWords + dictionary.extra_data['all-translations'][x][1]
    return listOfWords
def chooseFirstWord():
    word = random.choice(wordList)
    word = word[0]
    return word
def chooseSecondWord(firstWord):
    word = model.wv.most_similar(firstWord, topn = 20)
    i = True
    x=0
    while i == True:
        WordInWhile = word[x];
        WordInWhile = list(WordInWhile)
        WordInWhile = WordInWhile[0];
        
        if isSimilar(firstWord, WordInWhile) == False and len(WordInWhile) > 3 and isSimilar100(WordInWhile, functionToTranslateWord(WordInWhile)) == False:
            word = WordInWhile
            i = False
        else:
            x +=1
    return word
def chooseThirdWord(firstWord, secondWord):
    word = model.wv.most_similar(firstWord, topn = 20)
    i = True
    x=0
    while i == True:
        thirdWordInWhile = word[x];
        thirdWordInWhile = list(thirdWordInWhile)
        thirdWordInWhile = thirdWordInWhile[0];
        
        if isSimilar(firstWord, thirdWordInWhile) == False and isSimilar(secondWord, thirdWordInWhile) == False and len(thirdWordInWhile) > 3 and isSimilar100(thirdWordInWhile, functionToTranslateWord(thirdWordInWhile)) == False :
            word = thirdWordInWhile
            i = False
        else:
            x +=1
    return word
def chooseBadWord(firsWord):
    i = False
    while i == False:
        word = random.choice(wordList)
        word = word[0]
        if model.wv.similarity(word, firstWord) < 0.1:
            break
    return word
def chooseSecondTranslatedWord(wordToTranslate, firstTranslatedWord):
    secondTranslatedWord = GoogleTranslator(source='en', target='lt').translate(wordToTranslate)
    if isSimilar(firstTranslatedWord, secondTranslatedWord) == False and len(secondTranslatedWord) > 3:
        secondTranslatedWord = secondTranslatedWord
    else:
        secondTranslatedWord = translator.translate(wordToTranslate, dest="lt")
        secondListOfWords = translatedWordsSuggestionsToList(secondTranslatedWord)
        i = True
        x=0
        while i == True:
            if x >= len(secondListOfWords):
                secondTranslatedWord = GoogleTranslator(source='en', target='lt').translate(wordToTranslate)
                i = False
                break
            secondTranslatedWordInWhile = secondListOfWords[x]
            if isSimilar(firstTranslatedWord, secondTranslatedWordInWhile) == False and len(secondTranslatedWordInWhile) > 3:
                secondTranslatedWord = secondTranslatedWordInWhile
                i = False
            else:
                x += 1
    return secondTranslatedWord.lower()
def chooseThirdTranslatedWord(wordToTranslate, firstTranslatedWord, secondTranslatedWord):
    
    thirdTranslatedWord = GoogleTranslator(source='en', target='lt').translate(wordToTranslate)
    if isSimilar(firstTranslatedWord, thirdTranslatedWord) == False and len(thirdTranslatedWord) > 3 and isSimilar(secondTranslatedWord, thirdTranslatedWord) == False:
        thirdTranslatedWord = thirdTranslatedWord
    else:
        thirdTranslatedWord = translator.translate(wordToTranslate, dest="lt")
        thirdListOfWords = translatedWordsSuggestionsToList(thirdTranslatedWord)
        i = True
        x=0
        while i == True:
            if x >= len(thirdListOfWords):
                thirdTranslatedWord = GoogleTranslator(source='en', target='lt').translate(wordToTranslate)
                i = False
                break
            thirdTranslatedWordInWhile = thirdListOfWords[x]
            if isSimilar(firstTranslatedWord, thirdTranslatedWordInWhile) == False and len(thirdTranslatedWordInWhile) > 3 and isSimilar(secondTranslatedWord, thirdTranslatedWordInWhile) == False:
                thirdTranslatedWord = thirdTranslatedWordInWhile
                i = False
            else:
                x += 1
    return thirdTranslatedWord.lower()
def randomAnswer():
    return random.randrange(0,3)
def shuffleList(random, listOfWords):
    word = listOfWords[random]
    listOfWords[random] = listOfWords[3]
    listOfWords[3] = word
    return listOfWords

model = gensim.models.Word2Vec.load('D:/Data/model')

words = pd.read_excel('D:/Data/words.xlsx')
wordList = words.values.tolist() 

#Ekrano sukūrimas
screen = pygame.display.set_mode((800,600))

start_img = pygame.image.load('D:/Data/start.png').convert_alpha()
rules_img = pygame.image.load('D:/Data/rules.png').convert_alpha()
back_img = pygame.image.load('D:/Data/back.png').convert_alpha()

#Background
background = pygame.image.load('D:/Data/background.png')

#Pavadinimas ir piktograma
pygame.display.set_caption("Žodžių semantika")
icon = pygame.image.load("D:/Data/puzzle.png")
pygame.display.set_icon(icon)
    
start_button = Button(110, 300, start_img, 1)
rules_button = Button(110, 370, rules_img, 1)
back_button = Button(410, 370, back_img, 1)

i = 0
firstWord = chooseFirstWord()
secondWord = chooseSecondWord(firstWord)
thirdWord = chooseThirdWord(firstWord, secondWord)
badWord = chooseBadWord(firstWord)
gameWordList = [firstWord, secondWord, thirdWord, badWord]

translator = Translator()
firstTranslatedWord = GoogleTranslator(source='en', target='lt').translate(firstWord)
firstTranslatedWord = firstTranslatedWord.lower()
secondTranslatedWord = chooseSecondTranslatedWord(secondWord, firstTranslatedWord)
thirdTranslatedWord = chooseThirdTranslatedWord(thirdWord, firstTranslatedWord, secondTranslatedWord)
fourthTranslatedWord = GoogleTranslator(source='en', target='lt').translate(badWord)
fourthTranslatedWord = fourthTranslatedWord.lower()
translatedWords = [firstTranslatedWord, secondTranslatedWord, thirdTranslatedWord, fourthTranslatedWord]

answer = randomAnswer()
gameWordList = shuffleList(answer, gameWordList)
translatedWords = shuffleList(answer, translatedWords)

#Žaidimo ciklas
running = True
gameWindow = 1
while running:
    if gameWindow == 0:
        screen.fill((153, 204, 255))
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:                 
                    if input_text in translatedWords:
                        if input_text == translatedWords[answer]:
                            screenRender(translatedWords, 'Teisingai!', input_text, lifesText, scoreText)
                            scoreNumber = scoreNumber + 1
                            collectedScoreNumber = scoreNumber
                            scoreText = "Taškai: " + str(scoreNumber)
                        else:
                            screenRender(translatedWords, 'Neteisingai!', input_text, lifesText, scoreText)
                            lifesNumber = lifesNumber - 1
                            lifesText = "Gyvybės: " + str(lifesNumber)
                            if lifesNumber == 0:
                                if scoreNumber >int(recordNumber):
                                    recordNumber = scoreNumber
                                    recordText = 'NAUJAS REKORDAS: ' + str(recordNumber)
                                else:
                                    recordText = 'REKORDAS: ' + str(recordNumber)
                                scoreNumber = 0
                                lifesNumber = 3
                                scoreText = "Taškai: " + str(scoreNumber)
                                lifesText = "Gyvybės: " + str(lifesNumber)
                                collectedScoreText = collectedScoreWordText + str(collectedScoreNumber)
                                with open('D:/Data/record.txt', 'w') as f:
                                    f.write(str(recordNumber))
                                f.close()
                                collectedScoreNumber = 0
                                gameWindow = 1

                        firstWord = chooseFirstWord()
                        secondWord = chooseSecondWord(firstWord)
                        thirdWord = chooseThirdWord(firstWord, secondWord)
                        badWord = chooseBadWord(firstWord)
                        gameWordList = [firstWord, secondWord, thirdWord, badWord]
                    
                        translator = Translator()
                        firstTranslatedWord = GoogleTranslator(source='en', target='lt').translate(firstWord)
                        secondTranslatedWord = chooseSecondTranslatedWord(secondWord, firstTranslatedWord)
                        thirdTranslatedWord = chooseThirdTranslatedWord(thirdWord, firstTranslatedWord, secondTranslatedWord)
                        fourthTranslatedWord = GoogleTranslator(source='en', target='lt').translate(badWord)
                        translatedWords = [firstTranslatedWord, secondTranslatedWord, thirdTranslatedWord, fourthTranslatedWord]
                        
                        answer = randomAnswer()
                        gameWordList = shuffleList(answer, gameWordList)
                        translatedWords = shuffleList(answer, translatedWords)
                        input_text = ''
                        print(gameWordList)
                        print(translatedWords)
                    else:
                        screenRender(translatedWords, 'Netinkamas žodis!', input_text, lifesText, scoreText)
                        time.sleep(2)
                    
                else:
                    input_text += event.unicode
            screenRender(translatedWords, ' ', input_text, lifesText, scoreText)
    elif gameWindow == 1:
        if start_button.draw(screen):
            gameWindow = 0
        if rules_button.draw(screen):
            gameWindow = 2
        screen.fill((153, 204, 255))
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        startScreenRender(recordText, collectedScoreText)
    else:
        if back_button.draw(screen):
            gameWindow = 1
        screen.fill((153, 204, 255))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        rulesScreenRender()