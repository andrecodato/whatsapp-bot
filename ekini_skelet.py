import os
import time

from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver


class Wppbot:
    # root path
    dir_path = os.getcwd()

    # def init
    def __init__(self, bot_name):
        # bot definition
        self.bot = ChatBot(bot_name)

        # trainer definition
        self.trainer = ChatterBotCorpusTrainer(self.bot)

        # chromedriver path
        self.chrome = self.dir_path + '/driver/chromedriver'

        # acess Chrome options then create/acess
        # a new user on chrome for the bot
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            r'user-data-dir=' + self.dir_path + '/profile/wpp_ekini')

        # init chromedriver
        self.driver = webdriver.Chrome(
            self.chrome, chrome_options=self.options)

    # function that acees the website then enter in pre-selected group
    # (will be removed later)
    def start(self, contact_group):
        # acess web.whatsapp then
        # wait '15' seconds to site load
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)

        # select the site search box,
        # write the contact/group name then
        # wait 2 seconds for the next step
        # (this function will be removed and replaced by detect calls in all chats)
        self.contact_group_name_box = self.driver.find_element_by_xpath(
            "//INPUT[@type='text']")
        self.contact_group_name_box.send_keys(contact_group)
        time.sleep(2)

        # select the result of search
        # then click and wait 2 seconds
        self.contato = self.driver.find_element_by_xpath(
            "//SPAN[@class='matched-text'][text()='{}']".format(contact_group))
        self.contato.click()
        time.sleep(2)

    # function that run the MOTD message
    # (maybe will be removed)
    def welcome(self, welcome_msg):
        # select the message box
        self.msg_box = self.driver.find_element_by_class_name(
            '_3u328')

        if type(welcome_msg) == list:
            for sentence in welcome_msg:
                # write the sentence(s) in message box then
                # wait 1 second for the send button appears
                self.msg_box.send_keys(sentence)
                time.sleep(1)

                # select the send button,
                # click on it and wait 1 second
                self.send_btn = self.driver.find_element_by_xpath(
                    "//SPAN[@data-icon='send']")
                self.send_btn.click()
                time.sleep(1)
        else:
            self.msg_box.send_keys(welcome_msg)
            time.sleep(1)

            self.send_btn.click()
            time.sleep(1)

    # function that hear all messages
    def ear(self):
        # find all the message boxes,
        # set the last one, then
        # select the text on it
        # and, finaly, return the last text
        chat_balloon = self.driver.find_elements_by_class_name('FTBzM')
        last_chat_balloon = len(chat_balloon) - 1
        chat_balloon_text = chat_balloon[last_chat_balloon].find_element_by_css_selector(
            'span.selectable-text').text
        return chat_balloon_text

    # function that will train the bot
    def training(self):
        self.trainer.train("chatterbot.corpous.portuguese")

    # function that will answer a call
    def reply(self, msg_text):
        # takes the text give by main.py then convert to string
        response = self.bot.get_response(msg_text)
        response = str(response)

        self.msg_box = self.driver.find_element_by_class_name(
            '_3u328')
        self.msg_box.send_keys(response)
        time.sleep(1)

        self.send_btn = self.driver.find_element_by_xpath(
            "//SPAN[@data-icon='send']")
        self.send_btn.click()

        self.training()
