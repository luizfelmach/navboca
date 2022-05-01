#!/usr/bin/python
from hashlib import sha256
from bs4 import BeautifulSoup
from getpass import getpass
import requests


class NavBoca:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.uri = 'http://200.137.66.69/boca/index.php'
        self.session = requests.Session()

    def login(self):
        cookieHash = self.session.get(self.uri).text[1029:1055]
        passHash = sha256(self.password.encode('utf-8')).hexdigest()
        stringHash = passHash + cookieHash
        finalHash = sha256(stringHash.encode('utf-8')).hexdigest()
        request = f"{self.uri}?name={self.user}&password={finalHash}"
        self.session.get(request)

    def score(self):
        response = self.session.get('http://200.137.66.69/boca/team/score.php')
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')
        cont = 1
        for tr in range(3, len(trs)):
            dados = trs[tr].find_all('td')[1].find_all('td')
            pessoa = dados[0].contents[0]
            progresso = dados[-1].contents[0].split(' ')[0]
            tab = ' ' * (40 - len(pessoa) - len(str(cont)))
            tot = len(dados) - 2
            if (pessoa.lower() == 'luiz felipe machado'):
                pessoa = '\033[32m' + pessoa + '\033[0;0m'
            if tr % 2 == 0:
                print(f' #{cont}   {pessoa.lower()}{tab}{progresso}/{tot}')
                cont += 1


if __name__ == '__main__':
    user = input('User: ')
    password = getpass('Password: ')
    nav = NavBoca(user, password)
    nav.login()
    nav.score()
