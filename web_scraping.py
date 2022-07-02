# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:20:16 2022

@author: luisf
"""

from bs4 import BeautifulSoup
import requests

typesWithStats  = ['Creature', 'Legendary Creature', 'Snow Creature', 'Artifact Creature', 'Legendary Artifact Creature', 'Enchantment Creature', 'Legendary Enchantment Creature', 'Legendary Planeswalker']
typesWithoutCMC = ['Land', 'Basic Land', 'Legendary Land', 'Snow Land', 'Basic Snow Land', 'Artifact Land']

# =============================================================================
# Function to call gather info of the cards from the set taken from the webpage
# =============================================================================
def getCardInfo(soup):
    name = ''
    efect = ''
    CMC = ''
    primarytype = ''
    subtype = ''
    stats = ''
    name   = soup.findAll('span',class_='card-text-card-name')[0].text.strip() #name
    efect = soup.findAll('div',class_="card-text-oracle")     #effect
    if(len(efect)>0):
        efect=efect[0].text.strip()
    else:
        efect=''
    type = soup.findAll('p',class_="card-text-type-line")[0].text.strip().split(' — ')
    primarytype = type[0]
    if((primarytype in typesWithoutCMC) == False):
        CMC = soup.findAll('span',class_='card-text-mana-cost')[0].text.strip() #CMC
        if(primarytype in typesWithStats):
            subtype = type[1]
            stats = soup.findAll('div',class_="card-text-stats")[0].text.strip()      #stats
    return name, efect, CMC, primarytype, subtype, stats
# =============================================================================
# This function runs through the set webpage and separetes the URL of each card in the set
# this URLs are stored in an array and will be used to gather info for each card.
# =============================================================================
def getCardsURL(url):
    SetPage = requests.get(url)
    SetPageHTML = SetPage.content
    SetSoup = BeautifulSoup(SetPageHTML, "html.parser")
    SetName = SetSoup.findAll('h1',class_='set-header-title-h1')[0].text.strip() 
    CardsURL = []
    
    for a in SetSoup.find_all('a',class_='card-grid-item-card', href=True):
        CardsURL.append(a['href'])
    return SetName, CardsURL
# =============================================================================
# 
# =============================================================================
def saveData(CardsURL,SetName):
    filename = ((SetName + "_Cards_Info.txt"))
    print("Criando o arquivo: ", filename)
    file = open((filename), "w", encoding="utf-8")
    file.write('name, efect, CMC, primarytype, subtype,stats\n')
    for i in range(len(CardsURL)):
        print(i)
        CardPage = requests.get(CardsURL[i])
        html = CardPage.content
        soup = BeautifulSoup(html, "html.parser")
        name, efect, CMC, primarytype, subtype,stats = getCardInfo(soup)
        file.write(name + ' | ' + CMC + ' | ' + primarytype + ' | ' + subtype + ' | ' + stats + ' | ' + efect + '\n')
    
    file.close()


# =============================================================================
#  Main part of the code
# =============================================================================
specialChars = ":'<>" #used to allow the creation of files in a windows OS
SetURL = 'https://scryfall.com/sets/mh2'
SetName, CardsURL = getCardsURL(SetURL)

for specialChar in specialChars:
  SetName = SetName.replace(specialChar, '_')
  SetName = SetName.replace(" ","_")

saveData(CardsURL,SetName)
