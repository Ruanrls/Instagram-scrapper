import json
from requests import Session
from datetime import datetime
from time import sleep

LINK = 'https://www.instagram.com/accounts/login/'
BASE_LINK = LINK + "ajax/"
GRAPHQL_URL = "https://www.instagram.com/graphql/query/?query_hash=3dec7e2c57367ef3da3d987d89f9dbc8&variables="

class User:
    def __init__ (self, username, session):
        self.session = session
        self.username = username
        self.userInfo = json.loads(self.session.get('https://www.instagram.com/' + username + '?__a=1').text)['graphql']['user']
        self.userId = self.userInfo['id']

        self.graphql = '{"id":"' + self.userId + '","include_reel":true,"fetch_mutual":false,"first":10,"after":"QVFETVhMMlpsXzVONWdkWlhnWG9tNTY4TTFheWZjMDdmYXdISk5MUFVpMjgtNnd2QUVYOE5oLWd5NHBGckxia1djeTE1dXJHS0tOQnBtVjZtbVNfb05aSw=="}'
        self.graphqlURL = GRAPHQL_URL + self.graphql
    def Followers(self):
        req = self.session.get(self.graphqlURL)
        edges = json.loads(req.text)['data']['user']['edge_follow']['edges']
        
        print(len(edges))
        for node in edges:
            print(node)


class Requests():
    def __init__(self):#Inicia a session e pega o token inicial
        self.session = Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Referer': 'https://www.instagram.com/',
            'Origin': 'https://www.instagram.com',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.GetToken(LINK)
        self.session.headers.update({'Referer': LINK, 'X-CSRFToken': self.token})

    def GetToken(self, url):#atualiza o token
        req = self.session.get(url)
        self.token = req.cookies['csrftoken']

    def MakeLogin(self, username, password):
        time = int(datetime.now().timestamp())

        loginData = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login = self.session.post(BASE_LINK, data=loginData)
        self.token = login.cookies['csrftoken']
        print(login)
        return self.session



username = "bot"
password = "botter"

BotReq = Requests()
session = BotReq.MakeLogin(username, password)

ScrapingUser = User("perf", session)
ScrapingUser.Followers()

""" 
wordlist = []

for each in userInfo:
    wordlist.append("@" + each['node']['username'] + '\n')

with open('wordlist.txt', 'w') as file:
    file.writelines(wordlist) """