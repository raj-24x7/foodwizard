try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import requests  
BASEURL = 'http://allrecipes.com'
LIMIT = 5
DATAFILE = 'dishsearchresult.txt'
def findArticles(soup):
	i = 0
	items = []
	for ar in soup.find_all('article'):
	#for item in ar.find_all('a',attrs={'data-internal-referrer-link':'hub recipe'}):
		item = ar.find('a')
		if not item: continue	
		i += 1
		if i%2==0:
			continue
		for htag in item.find_all('h3',attrs={'class':'grid-col__h3 grid-col__h3--recipe-grid'}):
			if 'recipe' in item['href']:
				items.append((htag.text.strip()).lower()+'::::'+BASEURL+item['href'])
			else:
				i=i-1
		if i >= LIMIT*2:
			break;
	return '\n'.join(items),len(items)

def readingfromfile():
	filename='ingList.txt'
	ings=[]
	for line in open(filename):
		ings.append(line)
	return ','.join(ings)

def searchdishfroming():
	query=readingfromfile()	
	#http://allrecipes.com/search/results/?ingIncl=bread,cheese&sort=re
	url = "http://allrecipes.com/search/results/?ingIncl="+query+"&sort=re"
	print url
	r  = requests.get(url)
	data = r.text
	# print data
	soup = BeautifulSoup(data,"html.parser")
	res,n = findArticles(soup)
	with open(DATAFILE,'w') as resultfile:
		resultfile.write(res)
	return n

# print search()