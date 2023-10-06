import os
import sys
import requests
from colorama import Fore
from bs4 import BeautifulSoup

directory = sys.argv[1]


def main(cache=None, msg=''):
    if cache is None:
        cache = []
    usr_input = input(msg)
    if usr_input == 'exit':
        return
    if usr_input == 'back' and len(cache) > 1:
        path = os.path.join(directory, cache.pop(len(cache)-2))
        with open(path, 'r') as f:
            print(f.read())
    if '.' not in usr_input:
        return main(None, 'Incorrect URL\n')
    web_cache = usr_input.replace('.', '_')
    usr_input = 'https://' + usr_input if 'https://' not in usr_input else usr_input
    path = os.path.join(directory, web_cache)
    if web_cache not in cache:
        if not os.access(directory, os.F_OK):
            os.mkdir(directory)
        url = requests.get(usr_input)
        soup = BeautifulSoup(url.content, 'html.parser')
        tags = ['p', 'h1', 'h2', 'h3', 'a', 'ul', 'ol', 'li']
        text = []
        for tag in tags:
            for i in soup.find_all(tag):
                href = Fore.BLUE + i.text if tag == 'a' else i.text
                text.append(href)
        content = set(text)
        print(*content)
    else:
        with open(path, 'r') as f:
            print(f.read())
    cache.append(web_cache)
    return main(cache)


if __name__ == '__main__':
    main()
