import requests
from bs4 import BeautifulSoup

# word = 'halloween'

def get_img_url(word):
    url = f'https://www.google.com/search?q={word}&tbm=isch'
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    return images[1].get('src')


