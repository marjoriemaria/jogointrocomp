import pygame
from constants import *

class Personagem(pygame.sprite.Sprite):
    def __init__(self, nome, vida, ataque, defesa, velocidade, x, y, imagem):
        super().__init__()
        
        self.velocidade = velocidade
        self.defesa_base = defesa
        self.defendendo = False
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))

    @property
    def defesa(self):
        if self.defendendo:
            return self.defesa_base * 2
        return self.defesa_base

    def desenhar(self, tela, selecionado=False):
        tela.blit(self.image, self.rect)

        if selecionado:
            pygame.draw.rect(tela, (255,255,0), self.rect, 5)

        

    def set_posicao(self, x, y):
        self.rect.center = (x, y)

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

    def desenhar_barra_vida(self, tela, personagem, x, y):
        largura_total = 170
        altura = 20

        proporcao = personagem.vida / personagem.vida_max
        largura_atual = int(largura_total * proporcao)

        pygame.draw.rect(tela, (235, 0, 0), (x, y, largura_total, altura))
        pygame.draw.rect(tela, (0, 230, 0), (x, y, largura_atual, altura))

    def desenhar_barra_vida_inimiga(self, tela, personagem, x, y):
        largura_total = 100
        altura = 15

        proporcao = personagem.vida / personagem.vida_max
        largura_atual = int(largura_total * proporcao)

        pygame.draw.rect(tela, (255, 0, 0), (x, y, largura_total, altura))
        pygame.draw.rect(tela, (0, 255, 0), (x, y, largura_atual, altura))
    def resetar(self):
        self.vida = self.vida_max
        self.defendendo = False

# personagens jogáveis
personagens = [
    Personagem("Personagem 1", 200, 150, 5, 10, 160, 160, pygame.image.load("imagens/personagem 1.png")),
    Personagem("Personagem 2", 200, 150, 5, 8, 380, 160, pygame.image.load("imagens/personagem 2.png"))
]

# inimigos
img_inimigo1 = pygame.image.load("imagens/gato filhote.png")
img_inimigo3 = pygame.image.load("imagens/gato vilao.png")

img_reduzida_1 = pygame.transform.scale(img_inimigo1, (LARGURA//3, ALTURA//3))
img_reduzida_3 = pygame.transform.scale(img_inimigo3, (LARGURA//3, ALTURA//3))
