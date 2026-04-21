import pygame

LARGURA = 680
ALTURA = 480
FPS = 60
TITULO = "Jogo"

BRANCO = (255, 255, 255)

PRETO = (0, 0, 0)
CINZA = (100, 100, 100)
CINZA_CLARINHO = (220, 220, 220)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

fundo_selecionar = pygame.image.load("imagens/selecao.png")
fundo_selecionar = pygame.transform.scale(fundo_selecionar, (LARGURA, ALTURA))


pygame.font.init()
FONTEs = pygame.font.SysFont(None, 40)

Y_INICIAL_DESENHO_PERSONAGENS = 250
INCREMENTO_DESENHO_PERSONAGENS = 130
