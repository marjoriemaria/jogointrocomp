import pygame
from constants import *

def loop(tela):
    opcoes = ["Jogar", "Opções", "Créditos", "Sair"]
    selecionado = 0
    em_opcoes = False
    em_creditos = False

    # ---------------- CARREGAR IMAGENS ----------------
    fundo_menu = pygame.image.load("imagens/img.jpeg").convert()
    fundo_selecao = pygame.image.load("imagens/Selecao.jpeg").convert()

    imagem_marjorie = pygame.image.load("imagens/Marjorie.png")
    imagem_debora = pygame.image.load("imagens/Debora.png")
    imagem_murilo = pygame.image.load("imagens/Murilo.png")

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:

                # ---------------- MENU PRINCIPAL ----------------
                if not em_opcoes and not em_creditos:
                    if evento.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % len(opcoes)

                    if evento.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % len(opcoes)

                    if evento.key == pygame.K_RETURN:
                        if opcoes[selecionado] == "Jogar":
                            return "selecao"
                        elif opcoes[selecionado] == "Opções":
                            em_opcoes = True
                        elif opcoes[selecionado] == "Créditos":
                            em_creditos = True
                        elif opcoes[selecionado] == "Sair":
                            return "sair"

                # ---------------- TELAS SECUNDÁRIAS ----------------
                else:
                    if evento.key == pygame.K_ESCAPE:
                        em_opcoes = False
                        em_creditos = False

        # ---------------- FUNDO ----------------
        if not em_opcoes and not em_creditos:
            tela.blit(fundo_menu, (0, 0))
        else:
            tela.blit(fundo_selecao, (0, 0))

        # ---------------- MENU PRINCIPAL ----------------
        if not em_opcoes and not em_creditos:
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
                        elif texto == "Creditos":
                            em_creditos = True
                        elif texto == "Sair":
                            return "sair"

                tela.blit(render, (x, y))

        # ---------------- TELA DE OPÇÕES ----------------
        elif em_opcoes:
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
                tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, y))
                y += 35

        # ---------------- TELA DE CREDITOS ----------------
        elif em_creditos:
            fonte_op = pygame.font.SysFont("Arial", 22)
            fonte_maior = pygame.font.SysFont("Arial", 35)
            
            
            #fotinhas
            pygame.draw.rect(tela, AMARELO, (97, 53, 156, 156))
            tela.blit(imagem_marjorie, (100, 56))
            pygame.draw.rect(tela, AMARELO, (397, 53, 156, 156))
            tela.blit(imagem_debora, (400, 56))
            pygame.draw.rect(tela, AMARELO, (250, 253, 156, 156))
            tela.blit(imagem_murilo, (253, 256))
            
            
            #textos
            texto = fonte_maior.render("CRÉDITOS", True, BRANCO)
            tela.blit(texto, (255, 5))
            
            texto = fonte_op.render("Marjorie", True, BRANCO)
            tela.blit(texto, (135, 208))
            texto = fonte_op.render("Desenvolvedora", True, CINZA_CLARINHO)
            tela.blit(texto, (103, 233))
            
            texto = fonte_op.render("Débora", True, BRANCO)
            tela.blit(texto, (442, 208))
            texto = fonte_op.render("Desenvolvedora", True, CINZA_CLARINHO)
            tela.blit(texto, (408, 233))
            
            texto = fonte_op.render("Murilo", True, BRANCO)
            tela.blit(texto, (300, 410))
            texto = fonte_op.render("Designer/artista", True, CINZA_CLARINHO)
            tela.blit(texto, (265, 435))


        pygame.display.flip()