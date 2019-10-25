import re

from ekini_skelet import Wppbot

# set bot name
bot = Wppbot('ekini')

# set contact/group name
bot.start('TOME TERES')

# set the welcome message (will be removed)
bot.welcome(
    ['Salve sou o ekini beta carai, meu arquiteto ta testando uns bagulho novo nessa porra',
     'ao contrário do meu parceiro, o eki, eu sou chamado pelo beki (Beta Ekini)',
     'chama eu ae nesse carai!'])

last_text = ''

while True:
    earing = bot.ear()

    if earing != last_text and re.match(r'beki\w*', earing):
        last_text = earing
        earing = earing.replace('beki', '')
        earing = earing.lower()
        bot.reply(earing)
