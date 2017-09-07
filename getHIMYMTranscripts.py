from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import codecs
url = 'http://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=how-i-met-your-mother'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html5lib')
newData = soup.findAll('div', attrs={'class':'season-episodes'})

for div in newData:
    links = div.findAll('a', attrs={'class':'season-episode-title'})
    for link in tqdm(links):
        newReq = requests.get('http://www.springfieldspringfield.co.uk/'+link['href'])
        filename = link.text
        newSoup = BeautifulSoup(newReq.text, 'html5lib')
        newDiv = newSoup.findAll('div', attrs={'class':'scrolling-script-container'})
        for newData in newDiv:
            text = newData.text
        outFile = codecs.open(filename+'.txt', 'w', 'utf-8')
        outFile.write(text)
        outFile.close()