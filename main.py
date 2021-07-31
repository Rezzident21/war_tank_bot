                                          # coding: utf-8

import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import datetime
import json


class WarTank:
    def __init__(self, login, password):
        self.url = 'https://wartank.ru/'
        self.login = login
        self.password = password

        self.s = requests.Session()

    def auth(self):  # Auth
        soup = BeautifulSoup(self.s.get(self.url).text, 'html.parser')
        show_link = soup.find('a', href=True, attrs={'class': 'simple-but gray border'})['href']  # Show link for auth
        self.s.post(self.url + show_link)  # Send post
        # Get link  form then send post method for sign up
        soup_link_soup = BeautifulSoup(self.s.get(self.url + show_link).text, 'html.parser')
        show_link_button = soup_link_soup.find('form', action=True)['action']

        data = {"id1_hf_0": "", "login": self.login, "password": self.password}

        self.s.post(self.url + show_link_button, data=data, headers=dict(Referer=self.url))  # Send post auth
        self.get_fuel()

    def get_fuel(self):  # Get fuel
        soup = BeautifulSoup(self.s.get(self.url + 'angar').text, 'html.parser')
        fuel = int(soup.find('td', attrs={'class': 'small lh1 bgn'}).text)
        return fuel

    def available_battle(self):  # Get availables battle. 1 battle = 90 fuels
        return int(self.get_fuel() / 30 / 3)

    def battle(self):

        print('Fuels: {}\nAvailable opponents: {} '.format(int(self.get_fuel()), self.available_battle()))
        if self.available_battle() > 0:
            while self.available_battle() > 0:
                soup = BeautifulSoup(self.s.get(self.url + 'battle').text, 'html.parser')
                get_link_battle = soup.find('a', attrs={'class': 'simple-but border'}, href=True)['href']
                print(self.s.post(self.url + get_link_battle).url)

                sleep(random.uniform(1, 2))
            else:
                print('Out of opponents')

    def pve_join(self):
        if datetime.datetime.now().hour >= 23 or datetime.datetime.now().hour < 6:
            return -1
        self.s.get(self.url + 'pve')

        soup = BeautifulSoup(self.s.get(self.url + 'pve').text, 'html.parser')
        get_link_pve = soup.find('a', attrs={'class': 'simple-but border'}, href=True)

        if get_link_pve:
            print(self.s.post(self.url + get_link_pve['href']))

        name_battle = soup.find('span', attrs={'class': 'green2'})
        print('Подано заявку на  {}'.format(name_battle.string))

    def convoy(self):
        soup = BeautifulSoup(self.s.get(self.url + 'convoy').text, 'html.parser')
        get_link_convoy_attack = soup.find('a', attrs={'class': 'simple-but border gray'}, href=True)

        if get_link_convoy_attack:
            print(self.s.post(self.url + get_link_convoy_attack['href']).url)

        get_link_convoy = soup.find('a', attrs={'class': 'simple-but border'}, href=True)
        text_wait_convoy = soup.find('div', attrs={'class': 'small white cntr sh_b bold p5'})

        if text_wait_convoy:
            print(text_wait_convoy)
            return -1

        if get_link_convoy:
            self.s.post(self.url + get_link_convoy['href'])
            print('Начать разведку')
            sleep(random.uniform(1, 2))

        soup = BeautifulSoup(self.s.get(self.url + 'convoy').text, 'html.parser')
        get_link_convoy_fight = soup.find('a', attrs={'class': 'simple-but border red'}, href=True)

        if get_link_convoy_fight:
            self.s.post(self.url + get_link_convoy_fight['href'])
            print('Бой начался')
            sleep(random.uniform(1, 2))

        soup = BeautifulSoup(self.s.get(self.url + 'convoy').text, 'html.parser')
        get_link_convoy_attack = soup.find('a', attrs={'class': 'simple-but gray'}, href=True)

        while get_link_convoy_attack:
            soup_fight = BeautifulSoup(self.s.get(self.url + 'convoy').text, 'html.parser')
            hp = soup_fight.findAll('div', attrs={'class': 'value-block lh1'})
            try:
                get_link_convoy_attack = soup_fight.find('a', attrs={'class': 'simple-but gray'}, href=True)
                print('Удар')
                print(self.s.post(self.url + get_link_convoy_attack['href']).url)
                sleep(random.uniform(1, 2))
            except:
                self.convoy()

    def get_link(self, link, name='simple-but border'):
        soup = BeautifulSoup(self.s.get(self.url + link).text, 'html.parser')
        return soup.findAll('a', attrs={'class': name})

    def missions(self):

        for link_mission in self.get_link('missions/'):
            if link_mission.text == 'Получить награду':
                print('Получена награда за миссию')
                self.s.post(self.url + link_mission['href'])
                sleep(random.uniform(1, 2))

    def soup(self, link):
        return BeautifulSoup(self.s.get(self.url + link).text, 'html.parser')

    def coins(self):
        self.s.post(self.url + self.get_link('coins')[0]['href'])
        print('Собираю колелкцию')
        sleep(random.uniform(1, 2))

    def builds(self):
        for links in self.get_link('buildings'):
            if links.text == 'Забрать':
                self.s.post(self.url + links['href'])
                sleep(random.uniform(1, 2))
        try:
            production_mine = self.get_link('production/Mine')[random.randint(0, 3)]
            if production_mine.text == 'Начать производство':
                print(self.s.post(self.url + 'production/' + production_mine['href']))
        except:
            print('Уже начало призводство в шахте')
        sleep(random.uniform(1, 2))

        try:
            production_polygon = self.get_link('polygon')[random.randint(0, 3)]
            if production_polygon.text == 'Получить бесплатно':
                print(self.s.post(self.url + 'production/' + production_polygon['href']))
        except:
            print('Уже получено бонус')

        sleep(random.uniform(1, 2))

        try:
            production_armory = self.get_link('production/Armory')[random.randint(0, 3)]
            if production_armory.text == 'Начать производство':
                print(self.s.post(self.url + 'production/' + production_armory['href']))
        except:
            print('Уже делают Armory ')
        sleep(random.uniform(1, 2))

        try:
            production_bank = self.get_link('production/Bank')[random.randint(0, 1)]
            if production_bank.text == 'Начать производство':
                print(self.s.post(self.url + 'production/' + production_bank['href']))
        except:
            print('Уже работа в Банке начата ')
        sleep(random.uniform(1, 2))

    def run(self):
        while True:
            try:
                print('Вход...')
                self.auth()
                sleep(random.uniform(1, 2))
            except:
                print('Авторизация не выполена\nЛогин:{}\nПароль:{}'.format(self.login, self.password))
            self.builds()

            self.battle()
            sleep(random.uniform(1, 2))
            self.pve_join()
            sleep(random.uniform(1, 2))
            self.convoy()
            sleep(random.uniform(1, 2))
            try:
                self.coins()
            except:
                print('Зарабатывай опыт и собирай коллекции!')
            self.missions()
            sleep(random.uniform(1, 2))
            sleep(random.uniform(3600,4500))

with open('accounts_wartank.json') as json_load_accounts:
    accounts = json.load(json_load_accounts)


for account in accounts:
    w = WarTank(account['login'], account['password'])
    w.run()