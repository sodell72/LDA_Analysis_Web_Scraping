from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
import shutil

# Beautiful Soup Tutorial
# r = requests.get("https://www.eecs.mit.edu/people/faculty-advisors")
# data = r.text
# soup = bs(data, "html.parser")
# print(soup.title)
# print(soup.p)
# for paragraph in soup.find_all("p"):
#     print(paragraph.text)
# print(soup.getText())
# for url in soup.find_all("a"):
#     print(url)
# for url in soup.find_all("a"):
#     print(url.get("href"))


# Creates soup of website containing MIT professor names
sauce = urllib.request.urlopen("https://www.eecs.mit.edu/people/faculty-advisors").read()
soup = bs(sauce, "html.parser")
nameList = []
# for peopleDiv in soup.find_all("div", class_="people-list"):
#     for field in peopleDiv.find_all("li"):
for viewTitle in soup.find_all("div", class_="views-field views-field-title"):
    for name in viewTitle.find_all("a"):
        nameList.append(name.text)
print(nameList)
print("The first name in nameList: ", nameList[0])

# Remove all names with periods in them
for name in nameList:
    if "." in name:
        print(name)
        splitName = name.split()
        for namePart in splitName:
            if "." in namePart:
                splitName.remove(namePart)
        nameList[nameList.index(name)] = " ".join(splitName)

print("this is list: ", nameList)

# authorName = nameList[0].split()
# print(authorName[0])
# authorName = ["Tamara", "Broderick"]

# creates abstracts directory
currentDirectoryPath = os.getcwd()
abstractsPath = currentDirectoryPath + "\\abstracts\\"
if os.path.exists(abstractsPath):
    shutil.rmtree(abstractsPath)
os.makedirs(abstractsPath)


for authorName in nameList:

    authorLink = "https://arxiv.org/find/all/1/au:+{}_{}/0/1/0/all/0/1".format(authorName[1], authorName[0])
    resultsText = requests.get(authorLink).text
    searchResultSoup = bs(resultsText, "html.parser")

    abstractLinks = searchResultSoup.find_all("a", title="Abstract")
    print(abstractLinks)
    links = []
    for link in abstractLinks:
        links.append("https://arxiv.org{}".format(link.get("href")))
    print(links)

    for link in links:
        abstractPageText = requests.get(link).text
        abstractSoup = bs(abstractPageText, "html.parser")
        abstract = abstractSoup.find_all("blockquote", class_="abstract mathjax")

        fileName = authorName + str(links.index(link))
        with open(abstractsPath + fileName, "w") as f:
            f.write(abstract[0].text)





# https://arxiv.org/find/(subject)/1/au:+(lastname)_(initial)/0/1/0/all/0/1
# https://arxiv.org//find/all/1/au:+Broderick_Tamara/0/1/0/all/0/1
# # https://arxiv.org//find/all/1/au:+lastname_firstname/0/1/0/all/0/1
