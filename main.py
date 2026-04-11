import pygame
#lohgfsojnpfhdn
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

    # essa função muda de cenas, mas ainda não temos nenhuma :(
    def mudar_cena(self, nova_cena):
        self.cena_atual = nova_cena

    def run(self):
        while True:
            self.clock.tick(FPS)

            # lidamos com eventos Globais (Fechar jogo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # atualização e desenho da cena atual
            self.cena_atual.update()
            self.cena_atual.draw(self.janela)

            pygame.display.update()
            
game = Game()


while rodando:
    print("estado atual:", estado)

    if estado == "menu":
        resultado = menu.loop(tela)

    elif estado == "selecao":
        resultado = Selecionar.loop(tela,game)
        print("voltou da seleção com:", resultado)
        
    elif estado == "batalha":
        cena = CenaBatalha(game)
        estado = cena.loop(tela)   
        
    elif estado == "fim":
        cena = CenaFinal(game)
        estado = CenaFinal.loop()
    
    
    if resultado == "sair":
        rodando = False
        
    else:
        estado = resultado

pygame.quit()

# executamos o jogo
