import pygame
from constants import *
from personagem import *

class Selecionar:
    def loop(tela, game):
        selecionado = 0
        confirmado = False
        escolhido = None

        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:

                   
                    if not confirmado:

                        if evento.key == pygame.K_RIGHT:
                            selecionado = (selecionado + 1) % len(personagens)

                        if evento.key == pygame.K_LEFT:
                            selecionado = (selecionado - 1) % len(personagens)

                        if evento.key == pygame.K_RETURN:
                            escolhido = personagens[selecionado]
                            game.personagem_escolhido = escolhido
                            confirmado = True

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"

                    
                    else:
                        if evento.key == pygame.K_RETURN:
                            return "batalha"

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"

            personagens[0].set_posicao(200, 250)
            personagens[1].set_posicao(450, 250)

            if not confirmado:
                tela.fill((50, 50, 100))
                tela.blit(fundo_selecionar, (0, 0))

                fonte = pygame.font.SysFont("Arial", 50)
                texto = fonte.render("Escolha um personagem", True, (255, 255, 255))
                tela.blit(texto, (115, 100))

                for i, p in enumerate(personagens):
                    rect = p.rect

                    if rect.collidepoint(mouse_pos):
                        selecionado = i

                        if mouse_click:
                            escolhido = p
                            game.personagem_escolhido = p
                            confirmado = True

                    p.desenhar(tela, i == selecionado)

            
            else:
                tela.fill((0, 0, 0))

                rect = escolhido.image.get_rect(center=(340, 200))
                tela.blit(escolhido.image, rect)

                fonte = pygame.font.SysFont("Arial", 40)
                texto = fonte.render("Pressione ENTER para lutar", True, (225, 225, 225))
                tela.blit(texto, (120, 350))

            pygame.display.flip()
