import os
import pathlib
import secrets
import time
from tkinter import N
from bs4 import BeautifulSoup
import requests
import random
import math

class Definition:
    def __init__(self, soup):
        self.definition = ""
        self.soup = soup
        self.partOfSpeech = ""

    def getDefinition(self):
        return self.definition

    def getPartOfSpeech(self):
        return self.partOfSpeech

    def definitions(self):
        for i in self.soup.find_all(class_="dtText"):
            self.definition = i.getText()
            break

    def partSpeech(self):
        i = self.soup.find('a', class_="important-blue-link")
            # print(i)
        self.partOfSpeech = i.getText()
            # self.partOfSpeech = i.getText()[:i.getText().index('(')-1]

class synAnt:
    def __init__(self, soup):
        self.totalSynonyms = ""
        self.totalAntonyms = ""
        self.soup = soup

    def getTotalSynonyms(self):
        return self.totalSynonyms

    def getTotalAntonyms(self):
        return self.totalAntonyms

    def synonyms(self):
        passedSyn = False
        for i in self.soup.find_all('div',class_="thes-list-header"):
            # print(i.getText())
            if ("Synonyms for" in i.getText() and passedSyn == False):
                for parent in i.parents:
                    if (parent.name == 'span'):
                        break
                # print(word + " Synonyms")
                self.totalSynonyms = []
                for n in parent.find_all("ul",class_="mw-list"):
                    synoynms = n.getText().replace('\n','').replace('  ',"").split(",")
                    self.totalSynonyms = self.totalSynonyms + synoynms
                # print(self.totalSynonyms,"\n"*2)
                passedSyn = True

    def antonyms(self):
        passedAnt = False
        for i in self.soup.find_all('div',class_="thes-list-header"):
            if ("Antonyms for" in i.getText() and passedAnt == False):
                for parent in i.parents:
                    if (parent.name == 'span'):
                        break
                # print(word + " Antonyms")
                self.totalAntonyms = []
                for n in parent.find_all("ul",class_="mw-list"):
                    # print(i.getText())
                    antonyms = n.getText().replace('\n','').replace('  ',"").split(",")
                    self.totalAntonyms = self.totalAntonyms + antonyms
                # print(self.totalAntonyms,"\n"*2)
                passedAnt = True


class Ety:
    def __init__(self, soup):
        self.soup = soup
        self.etyDef = ""
        self.etyExamples = []
    
    def getDef(self):
        return self.etyDef
    
    def getTotalEx(self):
        return self.etyExamples

    def definitions(self):
        for i in self.soup.find_all('section'):
            try:
                # print("passed first")
                # print(i.find('p').getText())
                b = i.find('p').getText()
                start = b.index('"')
                end = b.find(',', b.index('"') + 1, len(b) - 1)
                try:
                    # print(end, b.index(';'),b.find('"', b.index('"') + 1, len(b)-1))
                    if (b.index(';') < end):
                        end = b.index(';')
                        if (b.find('"', b.index('"') + 1, len(b)-1) < end):
                            end = b.index('"')
                except:
                    pass
                self.etyDef = b[start+1:end]
            except:
                pass
            try:
                # print("passed second")
                b = i.getText()
                # print(b)
                start = b.index('"')
                end = b.find(',', b.index('"') + 1, len(b) - 1)
                try:
                    # print(end, b.index(';'),b.find('"', b.index('"') + 1, len(b)-1))
                    if (b.index(';') < end):
                        end = b.index(';')
                        if (b.find('"', b.index('"') + 1, len(b)-1) < end):
                            end = b.index('"')
                except:
                    pass
                # print(start+1,end)
                self.etyDef = b[start+1:end]
                break
            except:
                pass
            return

    def examples(self, word):
        for i in self.soup.find_all('a', class_="word__name--TTbAA word_thumbnail__name--1khEg"):
            # print(i.getText())
            if word[-1] == "-":
                wordTmp = word[:-1]
            elif word[0] == '-':
                wordTmp = word[1:]

            if ("(" in i.getText() and wordTmp in i.getText()):
                # print(i.getText())
                etyExample = i.getText().split("(", 1)[0].replace(" ", "")[:-1]
                self.etyExamples.append(etyExample)
            
        if(self.etyExamples == []):
            # print(word)
            urlTemp = "https://www.thefreedictionary.com/words-containing-" + wordTmp
            pageTemp = requests.get(urlTemp)
            soupTemp = BeautifulSoup(pageTemp.content, 'html.parser')
            for n in soupTemp.find_all('li'):
                # print(n)
                for child in n.descendants:
                    # print(child)
                    if (wordTmp in child.getText()):
                        if ("Words" not in child.getText()):
                            if word[-1] == "-" and wordTmp == child.getText()[0:len(wordTmp)] and len(child.getText()) > len(wordTmp):
                                self.etyExamples.append(child.getText())
                            if word[0] == '-' and wordTmp == child.getText()[-len(wordTmp)] and len(child.getText()) > len(wordTmp):
                                # print(child.getText())
                                self.etyExamples.append(child.getText())

        for j in range(3):
            for i in range(len(self.etyExamples)):
                if word == self.etyExamples[i-1]:
                    # print(word, self.etyExamples[i-1], i-1)
                    self.etyExamples.pop(i-1)
        # print(self.etyDef)
        # print(self.etyExamples)

def main():
    lines = []
    if os.path.exists("vocabulary.txt"):
        os.remove("vocabulary.txt")
    choice = input("Do you want randomizing. Helps prevent cheating\nYes or no\n").upper()
    if (choice) == "YES": randomize = True
    else: randomize = False
    choice = input("Do you want synonyms. \nYes or no\n").upper()
    if (choice) == "YES": printSynonym = True
    else: printSynonym = False
    choice = input("Do you want antonyms.\nYes or no\n").upper()
    if (choice) == "YES": printAntonym = True
    else: printAntonym = False
    words = input("Enter your words seperated by a comma and a space\nEx. apple, bannana\n").split(', ')
    for word in words:
        if word[-1] == "-" or word[0] == '-':
            urlEty = "https://www.etymonline.com/search?q=" + word
            pageEty = requests.get(urlEty)
            soupEty = BeautifulSoup(pageEty.content, 'html.parser')

            ety = Ety(soupEty)

            ety.definitions()
            ety.examples(word)

            randEx = random.randint(0, math.floor(len(ety.getTotalEx())))
            try:
                lines.append(word + " : " + ety.getDef() + " (" + ety.getTotalEx()[randEx-1] + ")\n")
            except:
                pass
            print(word + " : " + ety.getDef() + " (" + ety.getTotalEx()[randEx-1] + ")\n")
        else:
            urlSyn = "https://www.merriam-webster.com/thesaurus/" + word
            pageSyn = requests.get(urlSyn)
            soupSyn = BeautifulSoup(pageSyn.content, 'html.parser')
            
            synonyms = synAnt(soupSyn)

            synonyms.synonyms()
            synonyms.antonyms()


            urlDef = "https://www.merriam-webster.com/dictionary/" + word
            pageDef = requests.get(urlDef)
            soupDef = BeautifulSoup(pageDef.content, 'html.parser')
            
            definition = Definition(soupDef)

            definition.definitions()
            definition.partSpeech()


            randSyn = random.randint(0, math.floor(len(synonyms.getTotalSynonyms())))
            randAnt = random.randint(0, math.floor(len(synonyms.getTotalAntonyms())))
            
            if ( not synonyms.getTotalSynonyms()):
                synonym = "    Synonym: N/A" + "\n"
            else:
                synonym =  "    Synonym: " + synonyms.getTotalSynonyms()[randSyn-1] + "\n"
            
            if (not synonyms.getTotalAntonyms()):
                antonym = "    Antonym: N/A" + "\n"
            else:
                antonym = "    Antonym: " + synonyms.getTotalAntonyms()[randAnt-1] + "\n"

            lines.append(word + " (" + definition.getPartOfSpeech() + ") " + "" + definition.getDefinition() + "\n")
            if (printSynonym):
                lines.append(synonym)
            if(printAntonym):
                lines.append(antonym)

            # lines = [word + " (" + definition.getPartOfSpeech() + ") " + "" + definition.getDefinition() + "\n", synonym, antonym]
            
            print("\n",word + " (" + definition.getPartOfSpeech() + ") " + "" + definition.getDefinition() + "\n", synonym, antonym)

    # print(lines)
    f = open("Vocabulary.txt", 'a')
    for line in lines:
        f.writelines(line)
    f.close()
    print("\n" * 5, "\nYou can find your words in a text file called Vocabulary.txt located at " + str(pathlib.Path().resolve()) + "\\Vocabulary.text")

global randomSeed
global randomize

randomize = False
randomSeed = secrets.randbits(32)
main() 