import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

isRunning = True
base_url="https://quotes.toscrape.com/"
url="/"

authorFreqs = {}
tagFreqs = {}

homepage = requests.get(base_url).text
soup = BeautifulSoup(homepage, "lxml")
tag_attribute_containers = soup.find_all("span", class_="tag-item")
top_tags = [tag.find("a", class_="tag").text for tag in tag_attribute_containers]
wanted_attribute = None


def help():
    print("\nHelp: /help")
    print("Show Quotes: /show")
    print("Plot Quotes: /plot")
    print("Quit: /quit\n")

def show():
    global wanted_attribute
    global url
    global base_url
    global authorFreqs
    while url:
        full_url=base_url+url
        response = requests.get(full_url)
        soup=BeautifulSoup(response.text, "lxml")

        quote_containers = soup.find_all("div", class_="quote")

        for quote in quote_containers:

            text=quote.find("span", class_ = "text").text
            tag_elements = quote.find_all("a", class_="tag")
            tags = [tag.text for tag in tag_elements]
            author = quote.find("small", class_="author").text
            
            if wanted_attribute in tags or wanted_attribute==None:
                authorFreqs[author] = authorFreqs.get(author, 0)+1
                for tag in tags:
                    tagFreqs[tag] = tagFreqs.get(tag, 0)+1
                print("\033[1;30;47m", text, "\033[0m")
                print("\033[1;35mAuthor:", author, "\033[0m")
                print("\033[94mTags: ", ", ".join(tags), "\033[0m")
                print("\033[91m------------------\033[0m\n") 

        next_button = soup.find("li", class_ = "next")
        if next_button:
            url=next_button.find("a")["href"]
        else:
            url=None
        print(url)
    print(authorFreqs)
    print(tagFreqs)

def plot():
    print("Here is a graph\n")

def setAttribute():
    global wanted_attribute
    global top_tags
    print("Available Attributes:", " | ".join(top_tags))
    input_attribute = input("Enter which index of the attribute you want or enter nothing for all: ")
    if input_attribute == "":
        wanted_attribute = None
    elif int(input_attribute)>0 and int(input_attribute)<=10:
        wanted_attribute=top_tags[int(input_attribute)-1]

def quit():
    global isRunning
    print("Goodbye.\n")
    isRunning = False

def getInput():
    print("Please enter a command to continue.")

    test_input = str(input("test.py:    ")).lower()
    match test_input:
        case "/help":
            help()
        case "/show":
            show()
        case "/plot":
            plot()
        case "/setattr":
            setAttribute()
        case "/quit":
            quit()
        case _:
            print("Invalid Input.")
    print("Would you like to continue?\n")


def main():
    while isRunning:

        getInput()

if __name__ == "__main__":
    main()
