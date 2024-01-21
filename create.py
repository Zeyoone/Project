import pygame
import math
import time
import numpy

pygame.font.init()
FONT_FOR_LANGUAGE_CELL = pygame.font.SysFont('arial', 30)
file = open('data.txt', mode='a', encoding='utf-8')
class Board:
    def __init__(self, width, height):
        self.left, self.top, self.cell_size = 10, 10, 30
        self.width, self.height = width, height
        self.board = [['0' for j in range(width)] for i in range(height)]
        self.b = LanguageCell('Дальше')

    def render(self, screen):
        screen.blit(self.b, (100, 500))

        for i in range(self.width + 1):
            pygame.draw.line(screen, 'white', (self.left + self.cell_size * i, self.top),
                             (self.left + self.cell_size * i, self.top + self.cell_size * self.height), width=1)

        for i in range(self.height + 1):
            pygame.draw.line(screen, 'white', (self.left, self.top + self.cell_size * i),
                             (self.left + self.cell_size * self.width, self.top + self.cell_size * i), width=1)

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == '1':
                    pygame.draw.rect(screen, 'white', (self.left + j * self.cell_size + 2, self.top + i * self.cell_size + 2, self.cell_size - 2, self.cell_size - 2), width=0)

    def get_click(self, pos, a):
        if self.b.belong(pos) and a:
            file.write(''.join([''.join(i) for i in self.board]) + '\n')
            self.board = [['0' for j in range(self.width)] for i in range(self.height)]
        a = self.get_cell(pos)
        if a != None:
            self.board[a[1]][a[0]] = '1'

    def get_cell(self, mouse_move):
        x, y = mouse_move
        if not (self.left < x < self.left + self.cell_size * self.width) or not (
                self.top < y < self.top + self.cell_size * self.height):
            return None

        x -= self.left
        y -= self.top

        x /= self.cell_size
        y /= self.cell_size

        x = math.ceil(x) - 1
        y = math.ceil(y) - 1
        return (x, y)


class LanguageCell(pygame.surface.Surface):
    def __init__(self, text, color1='#d9bea7', color2='#174d4a', scale=(360, 80)):
        self.text = text
        super().__init__(scale)
        self.fill(color1)
        pygame.draw.rect(self, '#0b422a', ((0, 0), scale), 5)
        converted_text = FONT_FOR_LANGUAGE_CELL.render(text, True, color2)
        self.blit(converted_text, (scale[0] / 2 - converted_text.get_size()[0] / 2, scale[1] / 2 - converted_text.get_size()[1] / 2))

    def belong(self, pos):
        x, y = pos
        if 100 < x < 460 and 500 < y < 580:
            print('yes')
            return True
        else:
            print(x, y)
            return False

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((600, 600))
    g = Board(15, 15)
    pygame.display.flip()
    run = True
    clock = pygame.time.Clock()
    while run:
        screen.fill('black')
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                file.close()
                run = False
            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                g.get_click(i.pos, True)
        if pygame.mouse.get_pressed()[0]:
            g.get_click(i.pos, False)
        g.render(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()