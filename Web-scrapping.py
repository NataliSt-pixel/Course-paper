import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/articles/'

response = requests.get(URL)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article')

for article in articles:
    preview_text = ' '.join([
        article.find('h2').get_text(),
        article.find('div', class_='article-formatted-body').get_text() if article.find('div', class_='article-formatted-body') else '',  
        ' '.join(hub.get_text() for hub in article.find_all('a', class_='tm-article-snippet__hubs-item-link')), 
        ' '.join(tag.get_text() for tag in article.find_all('span', class_='tm-article-snippet__hubs-item'))  
    ]).lower()
    
    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        time_tag = article.find('time')
        date = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y')
        title = article.find('h2').find('span').get_text()
        link = 'https://habr.com' + article.find('h2').find('a')['href']
        print(f'{date} – {title} – {link}')
