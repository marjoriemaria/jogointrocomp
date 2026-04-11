import pygame
from constants import *

def loop(tela):
    opcoes = ["Jogar", "Opções", "Sair"]
    selecionado = 0
    em_opcoes = False

    fundo = pygame.image.load("imagens/img.png").convert()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        tela.blit(fundo, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]  # botão esquerdo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:

                # ---------------- MENU PRINCIPAL ----------------
                if not em_opcoes:
                    if evento.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % len(opcoes)

                    if evento.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % len(opcoes)

                    if evento.key == pygame.K_RETURN:
                        if opcoes[selecionado] == "Jogar":
                            return "selecao"
                        elif opcoes[selecionado] == "Opções":
                            em_opcoes = True
                        elif opcoes[selecionado] == "Sair":
                            return "sair"

                # ---------------- TELA DE OPÇÕES ----------------
                else:
                    if evento.key == pygame.K_ESCAPE:
                        em_opcoes = False

        # ---------------- MENU PRINCIPAL ----------------
        if not em_opcoes:
            for i, texto in enumerate(opcoes):
                cor = VERDE if i == selecionado else BRANCO
                render = FONTEs.render(texto, True, cor)

                x = 300
                y = 120 + i * 60

                rect = render.get_rect(topleft=(x, y))

                
                if rect.collidepoint(mouse_pos):
                    selecionado = i

                    
                    if mouse_click:
                        if texto == "Jogar":
                            return "selecao"
                        elif texto == "Opções":
                            em_opcoes = True
                        elif texto == "Sair":
                            return "sair"

                tela.blit(render, (x, y))
                print("estou no menu")

        # ---------------- TELA DE OPÇÕES ----------------
        else:
            fonte_op = pygame.font.SysFont("Arial", 25)

            linhas = [
                "Opções do Jogo",
                "",
                "Som: Ligado",
                "Dificuldade: Normal",
                "",
                "Pressione ESC para voltar",
            ]

            y = 50
            for linha in linhas:
                txt = fonte_op.render(linha, True, BRANCO)
                tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, y), )
                y += 35

        pygame.display.flip()