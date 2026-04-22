import pygame
from constants import *
from personagem import *

class Selecionar:
    def loop(tela, game):
        selecionado = 0
        confirmado = False
        escolhido = None

        digitando_nome = False
        nome_digitado = ""
        cursor_visivel = True
        tempo_cursor = 0

        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"

                if evento.type == pygame.KEYDOWN:

                    # ---------------- TELA DE NOME ----------------
                    if digitando_nome:
                        if evento.key == pygame.K_BACKSPACE:
                            nome_digitado = nome_digitado[:-1]

                        elif evento.key == pygame.K_RETURN:
                            if nome_digitado.strip() != "":
                                escolhido.nome = nome_digitado
                                return "batalha"

                        else:
                            if evento.unicode.isalnum() and len(nome_digitado) < 10:
                                nome_digitado += evento.unicode

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"

                        continue

                    # ---------------- SELEÇÃO ----------------
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

                    # ---------------- TELA PERSONAGEM ----------------
                    else:
                        if evento.key == pygame.K_RETURN:
                            digitando_nome = True  # agora vai pra tela preta

                        if evento.key == pygame.K_ESCAPE:
                            return "menu"

            personagens[0].set_posicao(200, 250)
            personagens[1].set_posicao(450, 250)

            # ---------------- TELA PRETA (NOME) ----------------
            if digitando_nome:
                tela.blit(fundo_selecionar, (0, 0))

                fonte = pygame.font.SysFont("Arial", 40)
                texto = fonte.render("Digite seu nome", True, BRANCO)
                tela.blit(texto, (200, 100))

                rect_caixa = pygame.Rect(200, 180, 280, 40)
                pygame.draw.rect(tela, BRANCO, rect_caixa)
                pygame.draw.rect(tela, CINZA, rect_caixa, 2)

                fonte = pygame.font.SysFont("Arial", 30)
                texto = fonte.render(nome_digitado, True, PRETO)
                tela.blit(texto, (rect_caixa.x + 5, rect_caixa.y + 5))

                # cursor piscando
                tempo_cursor += 1
                if tempo_cursor >= 30:
                    cursor_visivel = not cursor_visivel
                    tempo_cursor = 0

                if cursor_visivel:
                    cursor_x = rect_caixa.x + 5 + texto.get_width()
                    pygame.draw.line(
                        tela, PRETO,
                        (cursor_x, rect_caixa.y + 5),
                        (cursor_x, rect_caixa.y + 35),
                        2
                    )

                texto = fonte.render("ENTER para continuar", True, BRANCO)
                tela.blit(texto, (195, 300))

                pygame.display.flip()
                continue

            # ---------------- TELA DE SELEÇÃO ----------------
            if not confirmado:
                tela.fill((50, 50, 100))
                tela.blit(fundo_selecionar, (0, 0))

                fonte = pygame.font.SysFont("Arial", 50)
                texto = fonte.render("Escolha um personagem", True, BRANCO)
                tela.blit(texto, (115, 100))

                for i, p in enumerate(personagens):
                    if p.rect.collidepoint(mouse_pos):
                        selecionado = i
                        if mouse_click:
                            escolhido = p
                            game.personagem_escolhido = p
                            confirmado = True

                    p.desenhar(tela, i == selecionado)

            # ---------------- TELA PERSONAGEM ----------------
            else:
                tela.blit(fundo_selecionar, (0, 0))

                pygame.draw.circle(tela, BRANCO, (340, 200), 100)

                rect = escolhido.image.get_rect(center=(340, 200))
                tela.blit(escolhido.image, rect)

                fonte = pygame.font.SysFont("Arial", 40)
                fonte2 = pygame.font.SysFont("Arial", 20)

                texto = fonte.render("Personagem selecionado", True, VERDE_CLARO)
                tela.blit(texto, (170, 30))

                texto = fonte.render("Pressione ENTER para continuar", True, BRANCO)
                tela.blit(texto, (120, 350))

                texto = fonte2.render("Pressione ESC para voltar ao menu", True, BRANCO)
                tela.blit(texto, (190, 395))

            pygame.display.flip()