
import pygame
from constants import BRANCO # essa linha será explicada em breve

# os botões também são subclasse de pygame.sprite.Sprite
class Botao(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, indice, image_cursor, personagem=None):
        super().__init__()

        # informações sobre qual imagem desenhar e onde
        # realizar o desenho na tela
        self.image_normal = image
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        # informações para indicar se o botão está
        # selecionado e o que desenhar quando estiver
        self.indice = indice
        self.image_cursor = image_cursor

        # O personagem associado a este botão (opcional)
        # essa parte é utilizada na cena de seleção de personagens
        self.personagem = personagem

    # essa função apenas verifica se o botão está selecionado
    # a partir de seu indice (cada botão possui um indice único)
    def checar_selecao(self, cursor_indice):
        return cursor_indice == self.indice

    # essa função desenha uma imagem diferente caso o
    # botão esteja selecionado
    def desenhar_cursor(self, superficie, cursor_indice):
        # desenha o cursor no canto superior esquerdo do rect do botão
        # se ele estiver selecionado
        if self.checar_selecao(cursor_indice):
            superficie.blit(self.image_cursor, (self.rect.x, self.rect.y))

    def update(self, cursor_indice):
        # Apenas desenha o cursor se o índice bater
        # Nota: A lógica de desenhar o cursor separadamente na tela principal
        # é mantida se preferir, mas aqui o botão já sabe se está selecionado.
        pass