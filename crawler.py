from bs4 import BeautifulSoup as bs
import requests
from cardBeta import CardBeta
from cardWitj import CardWitj

urls = {
    'beta':
    'https://beta.gouv.fr/recrutement/developpement?',
    'witj':
    'https://www.welcometothejungle.com/fr/companies/communaute-beta-gouv/jobs'
}

divs = {'beta': 'fr-card__body', 'witj': 'sc-1peil1v-4'}


class Crawler:
    """Crawler class"""

    def __init__(self, type):
        self.type = type
        self.stack = { 'total' : 0 }

    def run(self):
        print('... start crawl ' + self.type)
        response = requests.get(urls[self.type])
        html = response.content
        soup = bs(html, "lxml")

        if hasattr(self, f'crawl_{self.type}'):
            getattr(self, f'crawl_{self.type}')(soup)

    def crawl_witj(self, soup):
        myCards = []
        print('    title : ' + soup.title.get_text())
        cards = soup.find_all("div", class_=divs[self.type])
        print('    total found : {}'.format(len(cards)))
        for data in cards:
            myCard = CardWitj(data)
            myCards.append(myCard)
        print('     >>> loop myCards')
        for card in myCards:
            result = card.loadPage()

            for key in result:
              if key in self.stack :
                self.stack[key] += 1
                self.stack['total'] += 1
              else :
                self.stack[key] = 1

        print('    resume stack ::::')
        for key in self.stack:
           print('    tech : {} : {}'.format(key, self.stack[key]))
            

    def crawl_beta(self, soup):
        myCards = []
        print('    title : ' + soup.title.get_text())
        cards = soup.find_all("div", class_=divs[self.type])
        print('    total found : {}'.format(len(cards)))
        for data in cards:
            myCard = CardBeta(data)
            myCards.append(myCard)

        print('     >>> loop myCards')
        for card in myCards:
            card.loadPage()
