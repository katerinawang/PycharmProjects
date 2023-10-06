import io
import json
import logging
import random
import sys
from collections import defaultdict


def _get_logger():
    loglevel = logging.INFO
    logger = logging.getLogger(__name__)
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(loglevel)
        h = logging.StreamHandler(sys.stdout)
        f = logging.Formatter('%(message)s')
        h.setFormatter(f)
        logger.addHandler(h)
        logger.setLevel(loglevel)
        logger.handler_set = True
    return logger


class FlashCards:
    def __init__(self, logger):
        self.cards = {}
        self.mistakes = defaultdict(int)
        self.logger = logger
        self.stream = io.StringIO()
        s = logging.StreamHandler(self.stream)
        self.logger.addHandler(s)

    def add_card(self):
        self.logger.info('The card:')
        term = input()
        while term in self.cards.keys():
            self.logger.info(f'The term "{term}" already exists. Try again:')
            term = input()
        self.logger.info('The definition of the card:')
        definition = input()
        while definition in self.cards.values():
            self.logger.info(f'The definition "{definition}" already exists. Try again:')
            definition = input()
        self.cards[term] = definition
        self.logger.info(f'The pair ("{term}":"{definition}") has been added.')

    def rm_card(self):
        self.logger.info('Which card?')
        card = input()
        if card in self.cards.keys():
            del self.cards[card]
            self.logger.info('The card has been removed.')
        else:
            self.logger.info(f'Can\'t remove "{card}": there is no such card.')

    def import_card(self, file=None):
        if not file:
            self.logger.info('File name:')
            file = input()
        try:
            with open(file, 'r') as f:
                card_set = json.load(f)
            for k, v in card_set.items():
                self.cards[k] = v
            self.logger.info(f'{len(card_set.keys())} cards have been loaded.')
        except FileNotFoundError:
            self.logger.info('File not found.')

    def export_card(self, filename=None):
        if not filename:
            self.logger.info('File name:')
            filename = input()
        with open(filename, 'w') as f:
            json.dump(self.cards, f)
        self.logger.info(f'{len(self.cards.keys())} cards have been saved.')

    def ask_check(self):
        self.logger.info('How many times to ask?')
        times = int(input())
        terms, definitions = list(self.cards.keys()), list(self.cards.values())
        for _ in range(times):
            qs = random.choice(terms)
            ans = definitions[terms.index(qs)]
            self.logger.info(f'Print the definition of "{qs}"')
            usr_ans = input()
            if usr_ans != ans and usr_ans in definitions:
                correct = terms[definitions.index(usr_ans)]
                self.logger.info(f'Wrong. The right answer is "{ans}", but your definition is correct for "{correct}".')
                self.mistakes[qs] += 1
            else:
                if usr_ans == ans:
                    self.logger.info('Correct!')
                else:
                    self.logger.info(f'Wrong. The right answer is "{ans}"')
                    self.mistakes[qs] += 1

    def log(self):
        self.logger.info('File name:')
        log_name = input()
        with open(log_name, 'w') as f:
            f.write(self.stream.getvalue())
        self.logger.info('The log has been saved.')

    def hardest_card(self):
        freq = defaultdict(list)
        for k, v in self.mistakes.items():
            freq[v].append(k)
        if freq:
            freq = dict(sorted(freq.items(), key=lambda x: x[0], reverse=True))
            hardest = next(iter(freq.items()))
            if len(hardest[1]) > 1:
                self.logger.info(f'The hardest cards are {", ".join(hardest[1])}. You have {hardest[0] * len(hardest[1])} errors answering it.')
            else:
                self.logger.info(f'The hardest card is "{hardest[1][0]}". You have {hardest[0]} errors answering it.')
        else:
            self.logger.info('There are no cards with errors.')

    def reset(self):
        if self.mistakes:
            self.mistakes = {}
            self.logger.info('Card statistics have been reset.')

    def main(self, im_path=None, ex_path=None):
        if im_path:
            self.import_card(im_path)
        while True:
            self.logger.info('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            op = input()
            if op == 'add':
                self.add_card()
            if op == 'remove':
                self.rm_card()
            if op == 'import':
                self.import_card()
            if op == 'export':
                self.export_card()
            if op == 'ask':
                self.ask_check()
            if op == 'log':
                self.log()
            if op == 'hardest card':
                self.hardest_card()
            if op == 'reset stats':
                self.reset()
            if op == 'exit':
                self.logger.info('Bye bye!')
                if ex_path:
                    self.export_card(ex_path)
                break


new_card = FlashCards(_get_logger())
args = sys.argv
if len(args) == 2:
    if 'import' in args[1]:
        new_card.main(im_path=args[1].replace('--import_from=', ''))
    else:
        new_card.main(ex_path=args[1].replace('--export_to=', ''))
elif len(args) == 3:
    if 'import' in args[1]:
        new_card.main(im_path=args[1].replace('--import_from=', ''), ex_path=args[2].replace('--export_to=', ''))
    else:
        new_card.main(im_path=args[2].replace('--import_from=', ''), ex_path=args[1].replace('--export_to=', ''))
else:
    new_card.main()
