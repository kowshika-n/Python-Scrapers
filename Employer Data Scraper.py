import glob, os
import ast
import requests
import bs4
import sys
import re
import os
import time
import random
from csv import writer
import pyautogui
import pyperclip

pyautogui.PAUSE = 0.5

def click():
    try:
        pyautogui.click()
    except Exception as e:
        print(e)
        pass
    
def ExtractFrom(link):
    presented = brokered = phones = ""
    header =  {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,en-GB;q=0.4',
        'Connection': 'keep-alive',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'referer': 'https://www.google.com/url?sa=t&source=web&rct=j&url=' + link,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    
    session = requests.Session()
    try:
        url = "https://www.google.com/url?sa=t&source=web&rct=j&url=" + link
        session.get(url, headers=header)
        time.sleep(random.uniform(1, 5))
        resp = session.get(link, headers=header)
        if resp.status_code != 200:
            print('Error connecting to ' + link)
        else:
            # Parse the page using BS4
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            presented = soup.select('.business-card-agent')[0].text.replace('\n', ' ').strip()
            presented = presented.replace('Presented by:', '').replace(rep, '').replace(re2, '').strip()

            brokered = soup.select('.business-card-broker')[0].text.replace('\n', ' ').strip()
            phoneList = r.findall(brokered)
            brokered = brokered.replace('Brokered by:', '').replace(rep, '').strip()
            brokered = brokered.split('(')[0]
            phoneList = list(set(phoneList))
            if (len(phoneList) == 1):
                phones = phoneList[0]
            else:
                phones = str(phoneList)
    except Exception as e:
        print(e)
    finally:
        session.close
    return (presented, brokered, phones)


def AddToCSV(TextList):
    with open("Output.csv", "a+", newline='') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerow(TextList)


def downloadAndSave(file, url):
    time.sleep(random.uniform(1, 10))
    presented, brokered, phones = ExtractFrom(url)
    if (presented and brokered):
        final = [file.split('_pg')[0], presented, brokered, phones, url]
        print(final)
        AddToCSV(final)


def CombineCountyFiles():
    os.chdir(".\details")
    for file in glob.glob("*.txt"):
        with open(file, 'r') as f:
            urlList = f.read().replace('\n', '').replace("    ", '')
            urlList = ast.literal_eval(urlList)
            print(file, len(urlList))
            for url in urlList:
                AddToCSV([file.split('_pg')[0], url])
                #downloadAndSave(file, url)           

def CombineDetailFiles():
    os.chdir(".\details")
    for file in glob.glob("*.txt"):
        with open(file, 'r') as f:
            phones = ""
            lineList = f.read().replace("    ", '').split(" | ")
            if (len(lineList) == 8):
                url = lineList[0]
                name = lineList[1].strip()
                add = lineList[2].strip()
                City = lineList[3].strip()
                Contact = lineList[4].strip()
                link = lineList[5].strip()
                Industry = lineList[6].strip()
                Range = lineList[7].strip()
                AddToCSV([url, name, add, City, Contact, link, Industry, Range])
               
            else:
                print("Incorrect Data at " + file)


def paste(url):
    time.sleep(0.25)
    click()
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press(['delete'])
    time.sleep(0.25)
    pyautogui.typewrite(url)
    print("pasted : " + url)
    pyautogui.press('enter')


listofURLs = ['']

def openCombinedURLs():
    for line in range(0, len(listofURLs), 4):
        ur1l = listofURLs[line]
        url2 = listofURLs[line+1]
        url3 = listofURLs[line+2]
        url4 = listofURLs[line+3]
        time.sleep(0.25)
        pyautogui.moveTo(x=410, y=79)
        paste(ur1l)
        time.sleep(0.25)
        pyautogui.moveTo(x=1278, y=80)
        paste(url2)
        time.sleep(0.25)
        pyautogui.moveTo(x=381, y=606)
        paste(url3)
        time.sleep(0.25)
        pyautogui.moveTo(x=1410, y=597)
        paste(url4)
        time.sleep(2)



#CombineCountyFiles()
#openCombinedURLs()
CombineDetailFiles()
