import sys
import requests
from bs4 import BeautifulSoup
import re

SURL = "https://en.wiktionary.org/w/index.php?search="
EURL = "https://en.wiktionary.org/wiki/"

class WiktionarySearch:
    def __init__(self, query):
        print("Buscando "+query)
        self.query = query
        if (self.existe()):
            if (self.soup.find(id="Etymology")):
                self.ety = self.soup.p.get_text()
    def existe(self):
        self.soup = BeautifulSoup(requests.get(EURL+self.query).content,'html.parser')
        if (str(self.soup).find("Wiktionary does not yet have an entry for") == -1):
            return True
        else:
            return False
    def getEty(self):
        if (self.soup.find(id="Etymology")):
            return self.ety
        else:
            return "no"

