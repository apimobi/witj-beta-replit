from bs4 import BeautifulSoup as bs2, NavigableString
import requests
import re
import spacy
from collections import Counter
from string import punctuation
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from list import KEY_WORDS, DUPLICATES, MANDATORY

nlp = spacy.load("en_core_web_sm")


class CardWitj:
    """CardWitj class"""

    def __init__(self, data):
        self.data = data
        self.type = 'beta'
        self.link = ''

    def loadPage(self):
        print('    loading page : ')
        link = self.data.find_all("a", recursive=True)
        url = f"https://www.welcometothejungle.com{link[0]['href']}"
        self.link = url
        response = requests.get(url)
        html = response.content
        content = bs2(html, "lxml")
        content = content.find_all('section')
        match = []
        hotwords = []

        for text in content:
            cleanContent = self.remove_html_tags(str(text))

            for key, value in KEY_WORDS.items():
                if key in cleanContent.lower() and key not in match:
                    match.append(key)

            hotwords = hotwords + self.get_hotwords(cleanContent)

        match = self.remove_duplicates(match)
        score = self.calcul_score(match)
        print(f"score {score}")
        if score > 30:
            print(f'    >> {self.link}')
            print("#### Total #####")
            print(self.calcul_score(match))
            print("#### match #####")
            print(match)
            print("#### hotwords #####")
            print(Counter(hotwords).most_common(10))
        else:
            print("#### PAS INTERESSANT #####")
        print("#### END #####")
        return match

    def calcul_score(self, words):
        total = 0
        mandatory = False
        for key in words:
            total += KEY_WORDS[key]
            if key in MANDATORY:
                mandatory = True

        if mandatory == False:
            total -= 20
        return total

    def remove_duplicates(self, words):
        for key in DUPLICATES:
            if key in words:
                for elt in DUPLICATES[key]:
                    try:
                        words.remove(elt)
                    except ValueError:
                        """value error"""
                words.append(key)
        return words

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, ' ', text)

    def get_hotwords(self, text):
        result = []
        pos_tag = ['PROPN', 'ADJ', 'NOUN']
        doc = nlp(text.lower())
        for token in doc:
            if (token.text in fr_stop or token.text in punctuation):
                continue
            if (token.pos_ in pos_tag):
                result.append(token.text)
        most_common_list = Counter(result).most_common(10)
        #for item in most_common_list:
        #    print(item[0])
        return result

    def between(self, cur, end):
        while cur and cur != end:
            if isinstance(cur, NavigableString):
                text = cur.strip()
                if len(text):
                    yield text
            cur = cur.next_element
