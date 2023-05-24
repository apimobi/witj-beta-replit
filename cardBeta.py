from bs4 import BeautifulSoup as bs2, NavigableString
import requests
import re
import spacy
from collections import Counter
from string import punctuation
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from list import KEY_WORDS

nlp = spacy.load("en_core_web_sm")


class CardBeta:
    """CardBeta class"""

    def __init__(self, data):
        self.data = data
        self.type = 'beta'

    def loadPage(self):
        print('    loading page : ')
        link = self.data.find_all("a", recursive=True)
        print("       " + link[0]['href'])
        url = "https://beta.gouv.fr" + link[0]['href']
        response = requests.get(url)
        html = response.content
        content = bs2(html, "lxml")
        content = content.find_all('section', class_='fr-py-6w')
        cleanContent = self.remove_html_tags(str(content[0]))
        match = []
        for word in KEY_WORDS:
            if word in cleanContent.lower():
                match.append(word)
        hotwords = self.get_hotwords(cleanContent)
        print("#### match #####")
        print(match)
        print("#### hotwords #####")
        print(hotwords)
        print("#### END #####")

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

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
        return most_common_list

    def between(self, cur, end):
        while cur and cur != end:
            if isinstance(cur, NavigableString):
                text = cur.strip()
                if len(text):
                    yield text
            cur = cur.next_element
