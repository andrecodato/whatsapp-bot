import os
import time
import re

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver


class wppbot:
    # app root path
    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        self.bot = ChatBot(nome_bot)
        self.trainer = ListTrainer(self.bot)
        # chromedriver path
        self.chrome = self.dir_path + '/driver/chromedriver'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" +
                                  self.dir_path + "/profile/wpp")

        self.driver = webdriver.Chrome(self.chrome,
                                       chrome_options=self.options)

    def start(self, nome_contato):
        self.driver.get('https://web.whatsapp.com')
        self.driver.implicitly_wait(15)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name(
            '_2zCfw')
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)

        self.contato = self.driver.find_element_by_xpath("//SPAN[@class='matched-text'][text()='{}']"
                                                         .format(nome_contato))
        self.contato.click()
        time.sleep(2)

    def saudacao(self, frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name(
            '_3u328')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)

                self.botao_enviar = self.driver.find_element_by_xpath(
                    "//SPAN[@data-icon='send']")
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    def escuta(self):
        post = self.driver.find_elements_by_class_name('FTBzM')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector(
            'span.selectable-text').text

        return texto

    def responde(self, texto):
        response = self.bot.get_response(texto)
        response = str(response)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name(
            '_3u328')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)

        self.botao_enviar = self.driver.find_element_by_xpath(
            "//SPAN[@data-icon='send']")
        self.botao_enviar.click()

        conv = ['Salve mestre, eu sou burro, to aprendendo as coisa']
        self.trainer.train(conv)

    def treina(self, nome_pasta):
        for treino in os.listdir(nome_pasta):
            conversas = open(nome_pasta + '/' + treino, 'r').readlines()
            self.bot.train(conversas)
