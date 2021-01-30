import requests
from bs4 import BeautifulSoup
import re

soup=''

#### Paragraph request ####
def paragraph(x):
	ps = soup.find_all("p")
	return str(clean(str(ps[x])))

def clean(x):
	string = x
	search = re.search("<[^>]*>", string)
	if search:
		if search.span()[0]==0:
			string=string[search.span()[1]:]
			#print(string)
			return clean(string)
		else:
			string=string[:search.span()[0]]+string[search.span()[1]:]
			#print(string)
			return clean(string)
	else:
		return string

def run(search):
	URL = "https://en.wikipedia.org/wiki/"
	s = str(search)
	r = requests.get(URL+s).content
	soup = BeautifulSoup(r, 'html.parser')
	toc={}
	contents=[]
	lpar=[]
	# TOC fill
	toctexts = list(map(lambda x: x.contents[0].contents[0] if str(x.contents[0]).startswith("<") else x.contents[0], soup.find_all("span", {'class': 'toctext'}))) # Texts in the TOC
	tocnumbers = list(map(lambda x: x.contents[0], soup.find_all("span", {'class': 'tocnumber'}))) # Numbering of TOC
	for x in range(len(toctexts)): # Generate TOC
		toc[tocnumbers[x]]=toctexts[x]
	# Find first paragraph
	ps = soup.find_all("p")
	for x in range(5):
		if ps[x].contents[0] != '\n':
			contents.append(clean(str(ps[x])))
			break


	# Fill contents list
		# Set section names
	for x in toctexts:
		if " " in x:
			contents.append([tocnumbers[toctexts.index(x)],x.replace(" ", "_"),''])
		else:
			contents.append([tocnumbers[toctexts.index(x)],x,''])
		# Find and set section contents
	for x in range(len(contents)-1):
		if x+2<len(contents):
			contents[x+1][2]=str(soup)[str(soup).find(str(soup.find(id=contents[x+1]))):str(soup).find(str(soup.find(id=contents[x+2])))]
		else:
			contents[x+1][2]=str(soup)[str(soup).find(str(soup.find(id=contents[x+1]))):]

######## Subtract sectioned content from lpar
	for x in lpar:
		if x in contents[1][3]:
			lpar[lpar.index(x)] = ''
		if x in contents[2][3]:
			lpar[lpar.index(x)] = ''

	############
	if "may refer to" in soup.prettify():
		return contents, soup, toctexts, tocnumbers, toc, 0
	elif tocnumbers != [] and not "may refer to:" in soup.prettify():
		return contents, soup, toctexts, tocnumbers, toc, 1


