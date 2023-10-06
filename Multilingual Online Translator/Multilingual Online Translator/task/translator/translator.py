import sys

import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self, f, t, w):
        self.lang_lst = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        self.lang = f.capitalize()
        self.usr_f = f
        self.usr_t = t
        self.trans_lang = t.capitalize()
        if self.trans_lang.lower() == 'all':
            lang_index = self.lang_lst.index(self.lang)
            self.all_lst = self.lang_lst[:lang_index] + self.lang_lst[lang_index+1:]
        self.term = w

    def request(self, f, t):
        url = 'https://context.reverso.net/translation/' + f.lower() + '-' + t.lower() + '/' + self.term
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            trans_term = soup.find('span', {'class': 'display-term'}).text.strip()
            gender = soup.find('span', {'class': 'display-term'}).find_next_sibling()
            if not trans_term:
                return 0
            if gender:
                trans_term += ' ' + gender.text.strip()
            lang_eg = soup.find('div', {'class': 'src'}).text.strip()
            trans_eg = soup.find('div', {'class': 'trg'}).text.strip()
            return trans_term, lang_eg, trans_eg
        else:
            print('Something wrong with your internet connection')

    def translate_single(self):
        filename = self.term.lower() + '.txt'
        url = 'https://context.reverso.net/translation/' + self.lang.lower() + '-' + self.trans_lang.lower() + '/' + self.term
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            trans_terms = soup.find_all('span', {'class': 'display-term'})
            trans_sec = soup.find('section', {'id': 'examples-content'})
            if not trans_terms or not trans_sec:
                return print(f'Sorry, unable to find {self.term}')
            trans_pairs = trans_sec.find_all('span', {'class': 'text'})
            terms = [term.text for term in trans_terms]
            pairs = [pair.text.strip() for pair in trans_pairs]
            string = self.trans_lang + ' Translations:\n'
            for term in terms:
                string += term + '\n'
            string += '\n' + self.trans_lang + ' Examples:\n'
            for pair in pairs[1::2]:
                pairs[pairs.index(pair)] = pair + '\n'
            for eg in pairs:
                string += eg + '\n'
            with open(filename, 'a') as f:
                f.write(string)
            print(string)
        else:
            print('Something wrong with your internet connection')

    def translate_all(self, string=''):
        filename = self.term.lower() + '.txt'
        for lang in self.all_lst:
            try:
                term, lang_eg, trans_eg = self.request(self.lang, lang)
                string += lang + ' Translation:\n' + term + '\n\n' + lang + ' Example:\n' + lang_eg + '\n' + trans_eg + '\n\n'
                with open(filename, 'w') as f:
                    f.write(string)
                with open(filename, 'r') as f:
                    print(f.read())
            except TypeError:
                print(f'Sorry, unable to find {self.term}')
                break

    def main(self):
        if self.lang not in self.lang_lst:
            return print(f"Sorry, the program doesn't support {self.usr_f}")
        if self.trans_lang not in self.lang_lst and self.trans_lang != 'All':
            return print(f"Sorry, the program doesn't support {self.usr_t}")
        if self.trans_lang.lower() != 'all':
            self.translate_single()
        else:
            self.translate_all()


tr = Translator(sys.argv[1], sys.argv[2], sys.argv[3])
tr.main()
