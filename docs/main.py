from bs4 import BeautifulSoup
import requests
# import pandas as pd
# import matplotlib.pyplot as plt

def printQuotes(text, author, tags):
    print("\033[1;30;47m", text, "\033[0m")
    print("\033[1;35mAuthor:", author, "\033[0m")
    print("\033[94mTags: ", ", ".join(tags), "\033[0m")
    print("\033[91m------------------\033[0m\n")  

base_url="https://quotes.toscrape.com/"
url="/"

homepage = requests.get(base_url).text
soup = BeautifulSoup(homepage, "lxml")
tag_attribute_containers = soup.find_all("span", class_="tag-item")
top_tags = [tag.find("a", class_="tag").text for tag in tag_attribute_containers]

print("Available Attributes:", " | ".join(top_tags))
wanted_attribute=top_tags[int(input("Enter which index of the attribute you want: "))+1]
print("\033[91mWanted Attribute: ", wanted_attribute, "\033[0m")

  
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

        if wanted_attribute in tags or wanted_attribute=="":
            printQuotes(text, author, tags)

    next_button = soup.find("li", class_ = "next")
    if next_button:
        url=next_button.find("a")["href"]
    else:
        url=None
    print(url)


