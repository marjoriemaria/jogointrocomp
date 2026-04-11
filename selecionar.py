import pygame
from constants import *
from personagem import *


class Selecionar:
    def loop(tela,game):
        selecionado = 0
        confirmado = False
        escolhido = None
        

        while True:
            tela.fill((50, 50, 100))
            tela.blit(fundo_selecionar, (0,0))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:

                    # confirmação
               

                    # seleção
                      tela.fill((50, 50, 100))
            tela.blit(fundo_selecionar, (0,0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:

                    #  SE NÃO CONFIRMOU AINDA
                    if not confirmado:

                        if evento.key == pygame.K_RIGHT:
                            selecionado = (selecionado + 1) % len(personagens)

                        if evento.key == pygame.K_LEFT:
                            selecionado = (selecionado - 1) % len(personagens)

                        if evento.key == pygame.K_RETURN:
                            escolhido = personagens[selecionado]
                            game.personagem_escolhido = escolhido
                            confirmado = True
                            return "batalha"

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"

                    # SE JÁ CONFIRMOU
                    else:
                        if evento.key == pygame.K_RETURN:
                            return "batalha"

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"
            # seleção
            if not confirmado:
                fonte = pygame.font.SysFont("Arial", 50)
                texto = fonte.render("Escolha um personagem", True, (255, 255, 255))
                tela.blit(texto, (115, 100))
                print("estou decidindo")

                for i, p in enumerate(personagens):
                    rect = p.rect

                    if rect.collidepoint(mouse_pos):
                        selecionado = i

                        if mouse_click: 
                            estado = None
                            if not confirmado:
                                escolhido = p
                                game.personagem_escolhido = p
                                confirmado = True
                                
                                
                

                    p.desenhar(tela, i == selecionado)

            # confirmação
            else:
                print("escolhi")
       
            # desenha personagem escolhido no centro
                rect = escolhido.image.get_rect(center=(340, 230))
                tela.blit(escolhido.image, rect)

                fonte = pygame.font.SysFont("Arial", 40)
                texto = fonte.render("Personagem selecionado", True, (255, 255, 255))
                tela.blit(texto, (LARGURA // 4, 100))

                fonte2 = pygame.font.SysFont("Arial", 25)
                
            
                if escolhido.nome == "Personagem 1":
                    texto = fonte2.render("Vovô", True, (255, 255, 255))
               
            
                else:
                    texto = fonte2.render("Vovó", True, (255, 255, 255))
                pygame.time.delay(1000)
                return "batalha"
        
            
            
   
            pygame.display.flip() 
