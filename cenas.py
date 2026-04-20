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

        # garante que existe personagem
        self.jogador = game.personagem_escolhido
        self.aliados = [game.personagem_escolhido]
    
        # cria inimigo
        self.inimigos = []

        self.inimigo1 = Personagem("Capanga 1", 100, 6, 4, 410, 30, img_reduzida_1)

        self.inimigo2 = Personagem("Capanga 2", 120, 5, 4, 410, 300, img_reduzida_1)

        self.inimigo = Personagem("Chefe", 100, 10, 5, 350, 180, img_reduzida_3)
        
        self.inimigos.append(self.inimigo1)
        self.inimigos.append(self.inimigo)
        self.inimigos.append(self.inimigo2)

        # posiciona jogador
        if self.jogador:
            self.jogador.set_posicao(125, 200)

        self.turno = "jogador"

        self.fonte = pygame.font.SysFont("Arial", 24)
        
        #define turnos
        self.turnos = []
        self.indice_turno = 0

        # junta todos
        self.turnos = self.aliados + self.inimigos

        self.personagem_atual = self.turnos[0]
        self.estado = "acao"  #acao ou alvo
    
        self.alvo_index = 0
        
        # tentativa de animação (personagem arrasta)
        self.animando = False
        self.tempo_animacao = 0
        self.atacante = None
        self.alvo = None

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

                        if self.estado == "acao":
                            if event.key == pygame.K_RETURN:
                                self.estado = "alvo"

                        elif self.estado == "alvo":

                            if event.key == pygame.K_RIGHT:
                                self.alvo_index = (self.alvo_index + 1) % len(self.inimigos)

                            if event.key == pygame.K_LEFT:
                                self.alvo_index = (self.alvo_index - 1) % len(self.inimigos)

                            if event.key == pygame.K_RETURN:
                                alvo = self.inimigos[self.alvo_index]
                                self.atacar(self.personagem_atual, alvo)

            self.update()
            self.desenhar(tela)
            resultado = self.update()

            if resultado:
                print("RESULTADO DA BATALHA:", resultado)
                return resultado
            resultado = self.update()

            

            pygame.display.flip()

    def atacar(self, atacante, alvo):

        if not alvo.esta_vivo():
            return

        # inicia animação
        self.animando = True
        self.atacante = atacante
        self.alvo = alvo
        self.tempo_animacao = 0
        
    def atacar_jogador(self):
        alvos = [i for i in self.inimigos if i.vida > 0]
        
        if alvos:
            alvo = alvos[0]  # depois pode escolher com seta
            
        dano = self.jogador.ataque - self.inimigo.defesa
        if dano < 0:
            dano = 0
        self.inimigo.vida -= dano
        print("Jogador causou", dano)

        self.turno = "inimigo"
        
    def ataque_inimigos(self):
        for inimigo in self.inimigos:
            if inimigo.vida > 0:
                dano = inimigo.ataque - self.jogador.defesa
                pygame.time.delay(500)
                if dano < 0:
                    dano = 0

                self.jogador.vida -= dano
                print(f"{inimigo.nome} atacou! Causou", dano)

    def proximo_turno(self):
        self.indice_turno += 1
        self.personagem_atual = self.turnos[self.indice_turno % len(self.turnos)]
        self.estado = "acao"
        self.alvo_index = 0        
            
    def update(self):

 
        if not self.jogador.esta_vivo():
            return "DERROTA"

        if all(not i.esta_vivo() for i in self.inimigos):
            return "VITORIA"



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

        if self.personagem_atual in self.inimigos:
            vivos = [a for a in self.aliados if a.esta_vivo()]

            if vivos:
                alvo = vivos[0]
                self.atacar(self.personagem_atual, alvo)

            return None


  
        return None
       
    
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
        
    def desenhar(self, tela):
        
        
        tela.blit(pygame.image.load("imagens/Fundo batalha.png"), (0, 0))

        # desenha jogador
        if self.jogador:
            self.jogador.desenhar(tela)

        # desenha inimigo
        for inimigo in self.inimigos:
            if inimigo:
                inimigo.desenhar(tela)

        # texto do turno
        if self.turno == "jogador":
            texto = self.fonte.render("Seu turno: ENTER p/atacar; SETAS p/selecionar" , True, (255,255,255))
        
        elif self.turno == "inimigo":
            texto = self.fonte.render("Turno do inimigo...", True, (255,255,255))
        tela.blit(texto, (20, 420))

        # vida jogador
        """vida_j = self.fonte.render(f"Vida: {self.jogador.vida}", True, (0,255,0))
        tela.blit(vida_j, (20, 20))

        # vida inimigo
        vida_i = self.fonte.render(f"Vida Inimigo: {self.inimigo.vida}", True, (255,0,0))
        tela.blit(vida_i, (450, 20))"""
        
        # Barra de vida do jogador
        x = self.jogador.rect.centerx - 30
        y = self.jogador.rect.top - 15
        
        fonte_pequena = pygame.font.SysFont("Arial", 20)

        self.desenhar_barra_vida(tela, self.jogador, x, y)

        texto = fonte_pequena.render(f"{self.jogador.vida}/{self.jogador.vida_max}", True, (255,255,255))
        tela.blit(texto, (x, y - 12))

        # Barra de vida do inimigo
        for i, inimigo in enumerate(self.inimigos):
            if inimigo.vida > 0:
                inimigo.desenhar(tela)
                self.desenhar_barra_vida_inimiga(tela, inimigo, 400, 50 + i*135)
                
                x = self.inimigo.rect.centerx - 300
                y = self.inimigo.rect.top - 5
                
                fonte_pequena = pygame.font.SysFont("Arial", 18)
                texto_vida = fonte_pequena.render(f"{inimigo.vida}/{inimigo.vida_max}",True,(255, 255, 255))
                tela.blit(texto_vida, (323, 50 + i*120))
                
        #seleção de inimigo
        for i, inimigo in enumerate(self.inimigos):
            if inimigo.vida > 0:
                inimigo.desenhar(tela)

                # destaque
                if self.estado == "alvo" and i == self.alvo_index:
                    pygame.draw.rect(tela, (255,255,0), inimigo.rect, 3)
                    
        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                inimigo.desenhar(tela)
            else:
                imagem_cinza = inimigo.image.copy()
                imagem_cinza.fill((100,100,100), special_flags=pygame.BLEND_RGB_MULT)
                tela.blit(imagem_cinza, inimigo.rect)
"""
    def resultados(self):
        
"""

   
   
   
class Outras():   
    def todos_derrotados(self, personagens):
        return all(not p.esta_vivo() for p in personagens)
    
    def checar_resultado_batalha(self, aliados, inimigos):
        if self.todos_derrotados(inimigos):
            return "VITORIA"
        if self.todos_derrotados(aliados):
            return "DERROTA"
        resultado = self.checar_resultado_batalha(self.aliados, self.inimigos)
        if resultado is not None:
            self.game.mudar_cena(CenaFinal(self.game, resultado, self.aliados))
            return
        return None


class CenaFinal:
    def __init__(self, game, resultado, time_aliado):
        self.game = game
        self.resultado = resultado
        self.time_aliado = time_aliado
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
        else:
            cor = (255,0,0)
            titulo = "VOCÊ PERDEU"

        txt_titulo = self.fonte_titulo.render(titulo, True, cor)
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(LARGURA//2, ALTURA//2 - 100)))

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
