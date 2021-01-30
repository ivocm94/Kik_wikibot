import requests
from bs4 import BeautifulSoup
import re

def main():
    #kant = SepEntry("phenomenalism")
    #if kant.setArticleSoup():
    #    print(kant.getFirstParagraph(1))
    #else:
    #    print(kant.searchList)
    #    selection = input()
    #    kant = SepEntry(kant.searchList[int(selection)-1][2])
    #    if kant.setArticleSoup():
    #        print(kant.toc)
    pass

def clean(string):
    string=clean1(string)
    string=clean2(string)
    return string

def clean2(string):
    if string[-1] == "\n":
        return clean2(string[:-1])
    else:
        return string

def clean1(string):
	    tags = re.search("<[^>]*>", string)
	    if tags:
	    	if tags.span()[0]==0:
	    		string=string[tags.span()[1]:]
	    		return clean(string)
	    	else:
	    		string=string[:tags.span()[0]]+string[tags.span()[1]:]
	    		return clean(string)
	    else:
	    	return string

class SepEntry:
    searchList=[]
    toc=[]

    def __init__(self, query):
        print("Executing SepEntry")
        print("Setting name...")
        if " " in query:
            query = query.replace(" ", "-")
        self.name = query
        print("Name set.")

    def isArticle(self):
        if "Document Not Found" in str(self.soup):
            return 0
        else:
            return 1

    def setToc(self):
        toc=[]
        for x in self.soup.ul.findAll("a"):
            toc.append([x['href'], clean(str(x)).split(' ',1)[0], clean(str(x)).split(' ',1)[1]]) if (len(clean(str(x)).split(' ',1)) == 2 and clean(str(x)).split(' ',1)[0][0].isdigit()) else toc.append([x['href'], '', clean(str(x))])
        self.toc = toc

    def getFirstParagraph(self, cleanp): #dep
        if cleanp:
            return clean1(str(self.soup.p))
        else:
            return self.soup.p

    def getSection(self, number): #dep
        for n in range(len(self.toc)):
            if self.toc[n][1] == str(number):
                print("Selected "+str(number)+" from getSelection")
                if n+1<len(self.toc):
                    #return clean(str(self.soup)[str(self.soup).find(str(self.toc[n][0])):str(self.soup).find(str(self.toc[n+1][0]))])
                    return clean(str(self.soup)[str(self.soup).find((str(self.soup.find(id=self.toc[n][0][1:])))):str(self.soup).find((str(self.soup.find(id=self.toc[n+1][0][1:]))))])
                else:
                    return clean(str(self.soup)[str(self.soup).find(str(self.toc[n][0])):str(self.soup).find(str(self.soup.find(id="article-copyright")))])

    def setSearchList(self): #indep
        URL = "https://plato.stanford.edu/search/searcher.py?query="+self.name
        def tit(title):
            tit=''
            for word in title:
                if word != '\n':
                    tit += clean(str(word)) 
            return tit
        self.soup = BeautifulSoup(requests.get(URL).content,'html.parser')
        self.search_results = self.soup.find("div", {'class': 'search_results'})
        self.result_titles = self.soup.findAll('div', {'class': 'result_title'})
        self.results=[]
        for result in self.result_titles:
            self.results.append([self.result_titles.index(result)+1, tit(result), result.a['href'][51:51+result.a['href'][51:].find("/")]])
        self.searchList = self.results[:5]

    def setArticleSoup(self): #indep
        print("Getting and setting article soup for "+self.name)
        URL = "https://plato.stanford.edu/entries/"+self.name
        self.soup = BeautifulSoup(requests.get(URL).content,'html.parser')
        if self.isArticle():
            print("Article soup set.")
            self.soup = self.soup.find(id="article")
            self.main_text = self.soup.find(id="main-text")
            self.setToc()
            return 1
        else:
            print("Error: "+self.name+" is not an article.")
            self.soup = ''
            self.setSearchList()
            return 0

if __name__ == '__main__':
    main()