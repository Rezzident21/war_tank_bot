from seleniumrequests import Firefox
import random
from time import sleep


class WarTank:
    def __init__(self, login, password):
        self.url = 'https://wartank.ru'
        self.login = login
        self.password = password
        self.driver = Firefox()

    def sign_in(self):
        self.driver.get(self.url)
        sleep(random.uniform(1, 2))
        self.driver.find_element_by_css_selector(".simple-but.border.gray").click()
        self.driver.find_element_by_name('login').send_keys(self.login)
        self.driver.find_element_by_name('password').send_keys(self.password)
        sleep(random.uniform(1, 2))
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    def get_fuel(self):
        return int(self.driver.find_element_by_class_name("bgn").text)

    def battle(self):
        self.sign_in()
        while self.get_fuel() > 29:
            self.driver.get('https://wartank.ru/battle')
            sleep(random.uniform(1, 2))
            self.driver.find_element_by_css_selector(".simple-but.border").click()
            self.get_fuel()
            sleep(random.uniform(1, 2))

        print('FINISHED')
        self.driver.quit()


bot = WarTank('Mr Pantera', 'dysik16')
bot.battle()
