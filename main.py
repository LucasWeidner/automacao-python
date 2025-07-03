import pyautogui as pg
from time import sleep
from random import randint

# def abrir_navegador(browser):
#     pg.hotkey('win', 'r')
#     pg.write(browser)
#     pg.press('Enter')

# opcao = pg.prompt('[1]Edge \n[2]Chrome','Navegador')
# if opcao == '1':
#     abrir_navegador('msedge')
# elif opcao=='2':
#     abrir_navegador('chrome')
# else:
#     pg.alert('Programa não encontrado')

sleep(randint(1,15))
pg.mouseInfo()

