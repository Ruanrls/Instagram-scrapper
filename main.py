import json
from requests import Session, utils
from datetime import datetime
from time import sleep
import getpass

LINK = 'https://www.instagram.com/accounts/login/'
BASE_LINK = LINK + "ajax/"


class User:
    def __init__(self, username, session):
        self.followers = []
        self.session = session
        self.username = username
        self.GetToken('https://www.instagram.com/' + username)

        self.userId = json.loads(self.session.get(
            'https://www.instagram.com/' + username + '?__a=1').text)['graphql']['user']['id']

        self.url = 'https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"' + self.userId + \
            '","include_reel":true,"fetch_mutual":false,"first":48,"after":"QVFEbWxQbXNDXzU1NGpQSGNPUXhXMEUzRlFEM0pfZzlfaTNLaWV3VkRvZnN1MmpHM3ZMVHNPMm1ZYlU2M2xRYTg2OUlkbHR3anEzY0lIeGJPQkJnVjAtag=="}'

    def Followers(self):

        self.GetToken(
            "https://www.instagram.com/" + self.username + "/followers/")

        req = self.session.get(self.url, headers={
            'Referer': "https://www.instagram.com/" + self.username + "/followers/"})

        edges = json.loads(req.text)[
            'data']['user']['edge_followed_by']['edges']
        afterObject = json.loads(req.text)[
            'data']['user']['edge_followed_by']['page_info']

        for each in edges:
            self.followers.append("@" + each['node']['username'] + '\n')

        if(afterObject['has_next_page'] == True):
            if(len(self.followers) >= 2000):
                return

            self.url = 'https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"' + self.userId + \
                '","include_reel":true,"fetch_mutual":false,"first":48,"after":"' + \
                afterObject['end_cursor'] + '"}'
            sleep(1)
            self.Followers()

    def GetToken(self, url):  # atualiza o csrf token e o id_gid
        req = self.session.get(url)
        self.token = req.cookies['csrftoken']
        self.session.headers.update({"X-CSRFToken": self.token})
        try:
            self.id_gid = req.cookies['id_gid']
            self.session.headers.update({"X-CSRFToken": self.id_gid})
        except:
            pass


class Requests():
    def __init__(self):  # Inicia a session e pega o token inicial
        self.session = Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Referer': 'https://www.instagram.com/',
            'Origin': 'https://www.instagram.com',
            'X-Requested-With': 'XMLHttpRequest'
        }
        req = self.session.get(LINK)
        self.token = req.cookies['csrftoken']

        self.session.headers.update(
            {'Referer': LINK, 'X-CSRFToken': self.token})

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

        if(login.status_code == 403):
            print("Can't be logged!\nExiting....")
            exit(0)

        print("logged in!")
        return self.session


username = input("Informe seu username: ")
password = getpass.getpass("Insira sua password: ")
scrapper = input("Buscar seguidores de qual perfil? ")

BotReq = Requests()
session = BotReq.MakeLogin(username, password)

ScrapingUser = User(scrapper, session)
ScrapingUser.Followers()
print(ScrapingUser.followers)
print(len(ScrapingUser.followers))

with open('wordlist.txt', 'w') as file:
    for user in ScrapingUser.followers:
        file.writelines(user)
print("Done!")
