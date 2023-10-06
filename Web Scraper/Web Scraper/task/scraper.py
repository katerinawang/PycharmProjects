import os
import string
import requests
from bs4 import BeautifulSoup
import urllib.parse


def scrape(page_nums, tp):
    page_n = int(page_nums)
    for i in range(page_n):
        folder_name = "Page_" + str(i+1)
        os.mkdir(folder_name)
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='+str(i+1)
        main = requests.get(url)
        soup = BeautifulSoup(main.content, "html.parser")
        article = soup.find_all('article')
        for items in article:
            article_type = items.find('span', {'data-test': 'article.type'}).text.strip()
            article_url = items.find('a', {'data-track-action': 'view article'})
            if article_type == tp:
                article_title = article_url.text.strip()
                title = folder_name + "/" + article_title.translate(str.maketrans(' ', '_', string.punctuation)) + '.txt'
                get_url = urllib.parse.urljoin(url, article_url.get('href'))
                content = requests.get(get_url)
                soup = BeautifulSoup(content.content, "html.parser")
                body = soup.find('div', {'class': 'c-article-body'}).text.strip()
                with open(title, 'wb') as file:
                    file.write(body.encode())
    print('Saved all articles.')


scrape(input(), input())
