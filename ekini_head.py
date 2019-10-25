import re

from ekini_skelet import wppbot

bot = wppbot('ekini')

bot.treina('treino')

bot.start('Pega na main_a e balanca')

bot.saudacao(['Salve mestre, sou o Ekini, eu vim pra falar que a Dominika nasceu pelada',
              'Use "eki" pra falar comigo!'])

ultimo_texto = ''

while True:
    texto = bot.escuta()

    if texto != ultimo_texto and re.match(r'^eki', texto):
        ultimo_texto = texto
        texto = texto.replace('eki', '')
        texto = texto.lower()
        bot.responde(texto)
