import pygame

import sys
from constants import *
import menu
from selecionar import *
from cenas import *

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Batalha")

estado = "menu"
rodando = True

# música e sons
pygame.mixer.music.load("sons/trilha.mp3")
pygame.mixer.music.set_volume(0.01) 
pygame.mixer.music.play()



class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.cena_atual = 1
        self.personagem_escolhido = None


    def mudar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def run(self):
        while True:
            self.clock.tick(FPS)

          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

       
            self.cena_atual.update()
            self.cena_atual.draw(self.janela)

            pygame.display.update()
            
game = Game()


estado = "menu"
resultado_batalha = None

while rodando:
    print("estado atual:", estado)

  
    if estado == "menu":
        resultado = menu.loop(tela)

        if resultado == "sair":
            rodando = False
        else:
            estado = resultado



    elif estado == "selecao":
        resultado = Selecionar.loop(tela, game)

        if resultado == "menu":
            estado = "menu"
        else:
            estado = "batalha"



    elif estado == "batalha":
        cena = CenaBatalha(game)
        resultado = cena.loop(tela)

        if resultado in ["VITORIA", "DERROTA"]:
            resultado_batalha = resultado
            estado = "final"
        else:
            estado = resultado



    elif estado == "final":
        cena = CenaFinal(game, resultado_batalha, [game.personagem_escolhido])
        resultado = cena.loop(tela)

        if resultado == "menu":
            estado = "menu"
        elif resultado == "batalha":
            estado = "batalha"
        elif resultado == "sair":
            rodando = False
