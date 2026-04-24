import pygame
from constants import *
from logica import *
import random
from personagem import *
from selecionar import *
from botao import *
import sys


class CenaBatalha:
    def __init__(self, game):
        self.game = game
        self.tempo_acao = 0

        self.jogador = game.personagem_escolhido
        self.aliados = [game.personagem_escolhido]
    
        self.inimigos = []

        self.inimigo1 = Personagem("Capanga 1", 100, 10, 4, 10, 410, 30, img_reduzida_1)
        self.inimigo2 = Personagem("Capanga 2", 120, 10, 4, 10, 410, 300, img_reduzida_1)
        self.inimigo = Personagem("Chefe", 150, 15, 5, 10, 350, 180, img_reduzida_3)
        
        self.inimigos.append(self.inimigo1)
        self.inimigos.append(self.inimigo)
        self.inimigos.append(self.inimigo2)

        if self.jogador:
            self.jogador.set_posicao(125, 200)

        self.fonte = pygame.font.SysFont("Arial", 24)

        self.turnos = sorted(
            self.aliados + self.inimigos,
            key=lambda p: (-p.velocidade, p.defesa_base)
        )
        if self.jogador in self.turnos:
            self.turnos.remove(self.jogador)
            self.turnos.insert(0, self.jogador)

        self.indice_turno = 0
        self.personagem_atual = self.turnos[0]
        self.estado = "acao"
    
        self.alvo_index = 0
        
        self.animando = False
        self.tempo_animacao = 0
        self.atacante = None
        self.alvo = None

        self.fundo = pygame.image.load("imagens/Fundo batalha.png")

    def loop(self, tela):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                    if self.personagem_atual in self.aliados:

                        if event.key == pygame.K_d:
                            self.personagem_atual.defendendo = True
                            self.proximo_turno()

                        if self.estado == "acao":
                            if event.key == pygame.K_RETURN:
                                self.estado = "alvo"

                        elif self.estado == "alvo":

                            inimigos_vivos = [i for i in self.inimigos if i.esta_vivo()]
                            
                            if self.alvo_index >= len(inimigos_vivos):
                                self.alvo_index = 0
                            
                            if event.key == pygame.K_RIGHT:
                                self.alvo_index = (self.alvo_index + 1) % len(inimigos_vivos)

                            if event.key == pygame.K_LEFT:
                                self.alvo_index = (self.alvo_index - 1) % len(inimigos_vivos)
                            
                            if event.key == pygame.K_RETURN:
                                alvo = inimigos_vivos[self.alvo_index]
                                if alvo.esta_vivo():
                                    self.atacar(self.personagem_atual, alvo)
                                    

            self.desenhar(tela)
            resultado = self.update()

            if resultado:
                return resultado

            pygame.display.flip()

    def atacar(self, atacante, alvo):
        if not alvo.esta_vivo():
            return
        self.animando = True
        self.atacante = atacante
        self.alvo = alvo
        self.tempo_animacao = 0
        
        
    def proximo_turno(self):
        while True:
            self.indice_turno += 1
            self.personagem_atual = self.turnos[self.indice_turno % len(self.turnos)]

            if self.personagem_atual.esta_vivo():
                break

        self.estado = "acao"
        self.alvo_index = 0

       
        self.personagem_atual.defendendo = False

    def update(self):
        
        resultado = verificar_vitoria(self.aliados, self.inimigos)
        if resultado:
            return resultado

        if self.animando:
            self.tempo_animacao += 1

            if self.tempo_animacao < 10:
                self.atacante.rect.x += 5

            elif self.tempo_animacao < 20:
                self.atacante.rect.x -= 5

            else:
                dano = aplicar_dano(self.atacante, self.alvo)
                print(f"{self.atacante.nome} causou {dano}")

                self.animando = False
                self.tempo_animacao = 0

                resultado = verificar_vitoria(self.aliados, self.inimigos)
                if resultado:
                    return resultado

                self.proximo_turno()

            return None  

        # turno do inimigo
        if self.personagem_atual in self.inimigos:
            vivos = [a for a in self.aliados if a.esta_vivo()]

            if vivos:
                alvo = random.choice(vivos)
                self.atacar(self.personagem_atual, alvo)

            return None

        return None
       
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
        
    def desenhar(self, tela):
        
        tela.blit(self.fundo, (0, 0))

        if self.jogador:
            self.jogador.desenhar(tela)

        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                inimigo.desenhar(tela)
            else:
                imagem_cinza = inimigo.image.copy()
                imagem_cinza.fill((100,100,100), special_flags=pygame.BLEND_RGB_MULT)
                tela.blit(imagem_cinza, inimigo.rect)

        if self.personagem_atual in self.aliados:
            texto = self.fonte.render("Seu turno: ENTER atacar | D defender", True, (255,255,255))
        else:
            texto = self.fonte.render("Turno do inimigo...", True, (255,255,255))
        tela.blit(texto, (20, 420))

        x = self.jogador.rect.centerx - 30
        y = self.jogador.rect.top - 15
        
        fonte_pequena = pygame.font.SysFont("Arial", 20)
        self.desenhar_barra_vida(tela, self.jogador, x, y)

        texto = fonte_pequena.render(f"{self.jogador.vida}/{self.jogador.vida_max}", True, (255,255,255))
        tela.blit(texto, (x, y - 12))

        for i, inimigo in enumerate(self.inimigos):
            if inimigo.vida > 0:
                self.desenhar_barra_vida_inimiga(tela, inimigo, 400, 50 + i*135)

                fonte_pequena = pygame.font.SysFont("Arial", 18)
                texto_vida = fonte_pequena.render(f"{inimigo.vida}/{inimigo.vida_max}",True,(255, 255, 255))
                tela.blit(texto_vida, (323, 50 + i*120))

        inimigos_vivos = [i for i in self.inimigos if i.esta_vivo()]

        for i, inimigo in enumerate(inimigos_vivos):
            if self.estado == "alvo" and i == self.alvo_index:
                pygame.draw.rect(tela, (255,255,0), inimigo.rect, 3)


class CenaFinal:
    def __init__(self, game, resultado, time_aliado):
        self.game = game
        self.resultado = resultado
        self.time_aliado = time_aliado
        self.nome = getattr(game, "nome_jogador", "Jogador")
        self.fonte_titulo = pygame.font.SysFont("Arial", 60)
        self.fonte_texto = pygame.font.SysFont("Arial", 24)

    def loop(self, tela):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_s:
                        return "sair"

                    if event.key == pygame.K_r:
                        return "batalha"

                    if event.key == pygame.K_m:
                        return "menu"

            self.draw(tela)
            pygame.display.flip()

    def draw(self, tela):
        tela.fill((0,0,0))

        if self.resultado == "VITORIA":
            cor = (0,255,0)
            titulo = "VOCÊ VENCEU"
            mensagem = f"Parabéns, {self.nome}!"
        else:
            cor = (255,0,0)
            titulo = "VOCÊ PERDEU"
            mensagem = f"{self.nome}, você perdeu!"
            txt_titulo = self.fonte_titulo.render(titulo, True, cor)
            tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA//2, ALTURA//2 - 100)))
            
        txt_msg = self.fonte_texto.render(mensagem, True, (255,255,255))
        tela.blit(txt_msg, txt_msg.get_rect(center=(LARGURA//2, ALTURA//2 - 40)))

        instrucoes = [
            "S - Sair",
            "R - Reiniciar",
            "M - Menu"
        ]

        y = ALTURA//2
        for linha in instrucoes:
            txt = self.fonte_texto.render(linha, True, (255,255,255))
            tela.blit(txt, txt.get_rect(center=(LARGURA//2, y)))
            y += 40
