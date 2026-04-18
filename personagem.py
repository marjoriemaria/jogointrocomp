
import pygame
from constants import *

class Personagem(pygame.sprite.Sprite):
    def __init__(self, nome, vida, ataque, defesa, x, y, imagem):
        super().__init__()
        
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

    def desenhar(self, tela, selecionado=False):
        tela.blit(self.image, self.rect)

        if selecionado:
            pygame.draw.rect(tela, (255,255,0), self.rect, 5)
    

    # trocar a posição do personagem
    def set_posicao(self, x, y):
        self.rect.center = (x, y)

    # fazer ele causar dano a um oponente
    def causar_dano(self, oponente):
        dano = self.ataque - oponente.defesa
        # causa dano apenas se ele foi maior que 0
        if dano > 0:
            oponente.receber_dano(dano)
            return dano # retorna o dano causado (informação útil depois)
        else:
            return 0

    # fazer ele receber dano
    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0: # garante que a vida não pode ser negativa
            self.vida = 0

    # verifica se um personagem está vivo
    def esta_vivo(self):
        return self.vida > 0
    
    def desenhar_barra_vida(self, tela, personagem, x, y):
        largura_total = 170
        altura = 20

        proporcao = personagem.vida / personagem.vida_max
        largura_atual = int(largura_total * proporcao)

        # fundo (vermelho)
        pygame.draw.rect(tela, (235, 0, 0), (x, y, largura_total, altura))

        # vida atual (verde)
        pygame.draw.rect(tela, (0, 230, 0), (x, y, largura_atual, altura))
        
    def desenhar_barra_vida_inimiga(self, tela, personagem, x, y):
        largura_total = 100
        altura = 15

        proporcao = personagem.vida / personagem.vida_max
        largura_atual = int(largura_total * proporcao)

        # fundo
        pygame.draw.rect(tela, (255, 0, 0), (x, y, largura_total, altura))

        # vida atual
        pygame.draw.rect(tela, (0, 255, 0), (x, y, largura_atual, altura))
   
personagens = [
            Personagem("Personagem 1", 200, 150, 5, 160, 160, pygame.image.load("imagens/personagem 1.png")),
            Personagem("Personagem 2", 200, 50, 5, 380, 160, pygame.image.load("imagens/personagem 2.png"))
        ]

#imagens reduzidas dos inimigos
img_inimigo1 = pygame.image.load("imagens/gato filhote.png")
img_inimigo3 = pygame.image.load("imagens/gato vilao.png")

img_reduzida_1 = pygame.transform.scale(img_inimigo1, (LARGURA//3, ALTURA//3))
img_reduzida_3= pygame.transform.scale(img_inimigo3, (LARGURA//3, ALTURA//3))
