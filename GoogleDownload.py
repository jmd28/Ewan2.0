import requests
from bs4 import BeautifulSoup

word = 'halloween'
url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
content = requests.get(url).content
soup = BeautifulSoup(content,'lxml')
images = soup.findAll('img')

print(images[1].get('src'))

