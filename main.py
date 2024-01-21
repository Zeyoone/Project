import os
import random
import sqlite3
import time

import googletrans
import pygame

pygame.font.init()
TEXTS = {0: 'Начать игру', 1: 'Посмотреть историю игр', 2: 'Разработчики', 3: 'Язык', 4: 'Назад',
         5: 'Если у вас нет подключение к интернету вы не сможете сменить язык', 6: 'Количество',
         7: 'Время', 8: 'Да', 9: 'Нет', 10: 'Вы точно хотите выйти?', 11: 'Ты победил!', 12: 'Ты проиграл!',
         13: 'Выйти'}
LANGS = [googletrans.LANGUAGES[i] for i in googletrans.LANGUAGES]
FONT_FOR_LANGUAGE_CELL = pygame.font.SysFont('arial', 30)
BLACK_RECT = pygame.surface.Surface((360, 80))
ALPHA_RECT = pygame.surface.Surface((360, 80))
ALPHA_RECT.set_alpha(100)
all_sprites = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
killing_borders = pygame.sprite.Group()
palki = pygame.sprite.Group()
korobki = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
current_lang = 'russian'


class Button():
    def __init__(self, x, y, x1, y1, text):
        self.Y, self.Y1 = y, y1
        self.x, self.y, self.x1, self.y1 = x, y, x1, y1
        self.text = text
        self.set_text(self.text)

    def set_text(self, text):
        self.surface_1 = pygame.surface.Surface((abs(self.x1 - self.x), abs(self.y1 - self.y)))
        self.surface_1.fill('#ecc19c')
        self.text_for_surface_1 = pygame.font.Font(None, round(
            75 * ((self.x1 - self.x) * 1 / len(text)) / 35)).render(
            text, True, (18, 79, 76))
        self.surface_1.blit(self.text_for_surface_1,
                            ((abs(self.x1 - self.x) - self.text_for_surface_1.get_width()) / 2,
                             (
                                     abs(self.y1 - self.y) - self.text_for_surface_1.get_height()) / 2))

        self.surface_2 = pygame.surface.Surface((abs(self.x1 - self.x), abs(self.y1 - self.y)))
        self.surface_2.fill('#D0AB8A')
        self.text_for_surface_2 = pygame.font.Font(None, round(
            75 * ((self.x1 - self.x) * 1 / len(text)) / 35)).render(
            text, True, (16, 57, 39))
        self.surface_2.blit(self.text_for_surface_2,
                            ((abs(self.x1 - self.x) - self.text_for_surface_2.get_width()) / 2,
                             (
                                     abs(self.y1 - self.y) - self.text_for_surface_2.get_height()) / 2))

        for i in range(self.surface_2.get_width()):
            for j in range(self.surface_2.get_height()):
                if self.surface_2.get_at((i, j)) == (16, 57, 39):
                    for offset_x, offset_y in (
                            (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, -1),
                            (-1, 0), (-1, 1),
                            (-1, 2),
                            (0, -2), (0, -1), (0, 1), (0, 2), (1, -2), (1, -1), (1, 0), (1, 1),
                            (1, 2), (2, -2),
                            (2, -1),
                            (2, 0), (2, 1), (2, 2)):
                        if self.surface_2.get_at(
                                (pygame.math.clamp(i + offset_x, 0, self.surface_2.get_width() - 1),
                                 pygame.math.clamp(j + offset_y, 0,
                                                   self.surface_2.get_height() - 1))) == (
                                208, 171, 138, 255):
                            self.surface_2.set_at((i + offset_x, j + offset_y), (255, 255, 255))

        pygame.draw.rect(self.surface_2, 'white', (0, 0, self.x1 - self.x, self.y1 - self.y),
                         width=3)

    def render(self, screen):
        x, y = pygame.mouse.get_pos()
        screen.blit(
            self.surface_2 if self.x < x < self.x1 and self.y < y < self.y1 else self.surface_1,
            (self.x, self.y))

    def belong(self, pos):
        if self.x < pos[0] < self.x1 and self.y < pos[1] < self.y1:
            return True
        else:
            return False

    def move_pos(self, offset_y):
        self.y += offset_y
        self.y1 += offset_y


class Main_menu():
    def __init__(self, screen, size):
        self.gray_fill = pygame.surface.Surface((550, 800))
        self.gray_fill.fill((120, 128, 122))
        self.gray_fill.set_alpha(100)

        self.exist = False
        self.width, self.height = size
        self.screen = screen

        self.a = Button(25, 600, 265, 670, TEXTS[0])
        self.b = Button(290, 600, 520, 670, TEXTS[1])
        self.c = Button(25, 690, 265, 770, TEXTS[2])
        self.d = Button(290, 690, 520, 770, TEXTS[3])

        self.developer = Developer(size)
        self.setting = Setting(size)
        self.matchhistory = MatchHistory(size)
        self.game = Game(size)

    def mouse_whell(self, button):
        if self.setting.exist:
            self.setting.move_mouse(30 if button != 4 else -30)
        elif self.matchhistory.exist:
            self.matchhistory.move_mouse(30 if button != 4 else -30)

    def translate_text(self, lang):
        if lang != False:
            a = googletrans.Translator()
            clock.tick(0)
            screen.blit(self.gray_fill, (0, 0))
            pygame.display.flip()
            try:
                self.a.set_text(a.translate(TEXTS[0], scr='russian', dest=lang).text)
                self.b.set_text(a.translate(TEXTS[1], scr='russian', dest=lang).text)
                self.c.set_text(a.translate(TEXTS[2], scr='russian', dest=lang).text)
                self.d.set_text(a.translate(TEXTS[3], scr='russian', dest=lang).text)
                self.developer.set_text(lang)
                self.setting.set_text(lang)
                self.matchhistory.set_text(lang)
                self.game.set_text(lang)
            except Exception as error:
                print('Грусть', error)
            # self..set_text(lang)

            clock.tick(30)
            del a

    def show(self):
        # print('Show do it!')
        self.exist = True

    def hide(self):
        # print('Hide do it!')
        self.exist = False

    def update(self):
        if self.exist:
            # Рисование
            self.a.render(self.screen)
            self.b.render(self.screen)
            self.c.render(self.screen)
            self.d.render(self.screen)

            # Нажатие
            if mouse_button_1:
                if self.a.belong(pygame.mouse.get_pos()):
                    self.hide()
                    self.game.start_the_game()
                elif self.b.belong(pygame.mouse.get_pos()):
                    self.hide()
                    self.matchhistory.show()
                elif self.c.belong(pygame.mouse.get_pos()):
                    self.hide()
                    # self.translate_text('english')
                    self.developer.show()
                elif self.d.belong(pygame.mouse.get_pos()):
                    self.hide()
                    self.setting.show()
        elif self.developer.exist:
            if self.developer.update():
                self.show()
        elif self.setting.exist:
            if mouse_button_1:
                self.setting.click(pygame.mouse.get_pos())
            if self.setting.update():
                self.show()
        elif self.matchhistory.exist:
            if self.matchhistory.update():
                self.show()
        elif self.game.exist:
            if self.game.update():
                self.show()


class MatchHistory():
    def __init__(self, size):
        self.exist = False
        self.width, self.height = size

        self.back = Button(350, 688, 525, 758, 'Назад')
        self.column_name = ResultsCell((TEXTS[7], TEXTS[6]))
        self.column_name.set_alpha(185)

        if not os.path.exists('results.db'):
            conn = sqlite3.connect('results.db')
            cor = conn.cursor()
            cor.execute("""CREATE TABLE results(count TEXT, time TEXT);""")
            conn.commit()

    def func_results(self):
        conn = sqlite3.connect('results.db')
        cor = conn.cursor()
        cor = cor.execute("""SELECT * FROM results;""").fetchall()
        conn.commit()

        self.results = ControlClassResult()
        self.results.append(BLACK_RECT)
        for i in cor:
            self.results.append(ResultsCell(i))
            print('yes')
        self.results.append(BLACK_RECT)

    def show(self):
        self.func_results()
        self.exist = True

    def hide(self):
        self.exist = False

    def update(self):
        if self.exist:
            self.results.render()
            self.back.render(screen)
            screen.blit(self.column_name, (95, 10))
            if mouse_button_1:
                if self.back.belong(pygame.mouse.get_pos()):
                    self.exist = False
                    self.hide()
                    return True

    def set_text(self, lang):
        a = googletrans.Translator()
        self.back.set_text(a.translate('Назад', src='russian', dest=lang).text)
        self.column_name = ResultsCell((a.translate(TEXTS[7], src='russian', dest=lang).text,
                                        a.translate(TEXTS[6], src='russian', dest=lang).text))
        self.column_name.set_alpha(185)

    def move_mouse(self, offset):
        self.results.move_mouse(offset)


class ControlClassOfCell(list):
    def __init__(self):
        self.offset = 80
        self.border = (len(LANGS) - 6) * 80

    def render(self):
        pos = pygame.mouse.get_pos()
        if 95 < pos[0] < 455 and 90 < pos[1] < 610:
            for i in enumerate(self[self.offset // 80: self.offset // 80 + 8]):
                screen.blit(i[1], (95, 90 + i[0] * 80 - self.offset % 80))
                if 10 + i[0] * 80 - self.offset % 80 < pos[1] < 10 + i[
                    0] * 80 - self.offset % 80 + 80:
                    screen.blit(ALPHA_RECT, (95, 10 + i[0] * 80 - self.offset % 80))
        else:
            for i in enumerate(self[self.offset // 80: self.offset // 80 + 8]):
                screen.blit(i[1], (95, 90 + i[0] * 80 - self.offset % 80))

        screen.blit(BLACK_RECT, (95, 10))
        screen.blit(BLACK_RECT, (95, 650))

    def click(self, pos):
        g.translate_text(self[self.offset // 80: self.offset // 80 + 8][(pos[1] - 90) // 80].text)
        g.setting.set_lang(self[self.offset // 80: self.offset // 80 + 8][(pos[1] - 90) // 80].text)

    def move_mouse(self, a):
        self.offset = pygame.math.clamp(self.offset + a, 80, self.border)


class LanguageCell(pygame.surface.Surface):
    def __init__(self, text, color1='#d9bea7', color2='#174d4a', scale=(360, 80)):
        self.text = text
        super().__init__(scale)
        self.fill(color1)
        pygame.draw.rect(self, '#0b422a', ((0, 0), scale), 5)
        converted_text = FONT_FOR_LANGUAGE_CELL.render(text, True, color2)
        self.blit(converted_text, (scale[0] / 2 - converted_text.get_size()[0] / 2,
                                   scale[1] / 2 - converted_text.get_size()[1] / 2))


class ResultsCell(pygame.surface.Surface):
    def __init__(self, text, color1='#d9bea7', color2='#174d4a'):
        super().__init__((360, 80))
        count, time = text
        font = pygame.font.SysFont('arial', 20)
        count, time = font.render(count, True, color2), font.render(time, True, color2)

        self.fill(color1)
        pygame.draw.rect(self, '#0b422a', ((0, 0), (360, 80)), 5)
        pygame.draw.line(self, '#0b422a', (180, 0), (180, 80), 10)

        self.blit(count, (90 - count.get_size()[0] / 2, 40 - count.get_size()[1] / 2))
        self.blit(time, (180 + 90 - time.get_size()[0] / 2, 40 - time.get_size()[1] / 2))


class ControlClassResult(list):
    def __init__(self):
        self.offset = 80
        self.border = (len(LANGS) - 6) * 80

    def render(self):
        for i in enumerate(self[self.offset // 80: self.offset // 80 + 8]):
            screen.blit(i[1], (95, 90 + i[0] * 80 - self.offset % 80))

        screen.blit(BLACK_RECT, (95, 10))
        screen.blit(BLACK_RECT, (95, 650))

    def move_mouse(self, a):
        self.offset = pygame.math.clamp(self.offset + a, 80, self.border)


class Setting():
    def __init__(self, size):
        self.set_lang('russian')
        self.exist = False
        self.width, self.height = size
        self.back = Button(350, 688, 525, 758, 'Назад')

        self.warning = pygame.font.SysFont('arial', 15).render(TEXTS[5], True, 'white')

        self.cells = ControlClassOfCell()
        self.cells.append(BLACK_RECT)
        for i in LANGS:
            self.cells.append(LanguageCell(i))
        self.cells.append(BLACK_RECT)

    def click(self, pos):
        if 95 < pos[0] < 455 and 90 < pos[1] < 610:
            self.cells.click(pos)

    def show(self):
        self.exist = True

    def hide(self):
        self.exist = False

    def set_lang(self, lang):
        self.lang = LanguageCell(lang, color2='#0a3015', color1='#a89382')
        current_lang = lang

    def update(self):
        if self.exist:
            self.cells.render()
            self.back.render(screen)
            screen.blit(self.lang, (95, 10))
            screen.blit(self.warning, (75, 655))
            if mouse_button_1:
                if self.back.belong(pygame.mouse.get_pos()):
                    self.exist = False
                    self.hide()
                    return True

    def set_text(self, lang):
        a = googletrans.Translator()
        self.back.set_text(a.translate('Назад', src='russian', dest=lang).text)
        self.warning = pygame.font.SysFont('arial', 15).render(
            a.translate(TEXTS[5], scr='russian', dest=lang).text,
            True, 'white')

    def move_mouse(self, a):
        self.cells.move_mouse(a)


class Developer():
    def __init__(self, size):
        self.create_text()
        self.exist = False
        self.width, self.height = size

        self.back = Button(350, 688, 525, 758, 'Назад')

    def create_text(self, lang='russian'):
        if lang == 'russian':
            with open('text_for_developer.txt', mode='r', encoding='utf-8') as file:
                self.text = [line[:-1] for line in file]

            font = pygame.font.SysFont(None, 22)
            width_for_surface, height_for_surface = 0, 0
            for i in self.text:
                width, height = font.render(i, False, 'white').get_size()
                if width_for_surface < width: width_for_surface = width
                if height_for_surface < height: height_for_surface = height
            self.surface_with_text = pygame.surface.Surface((500, 640))
            self.surface_with_text.fill('#d9bea7')
            for i in range(len(self.text)):
                self.surface_with_text.blit(font.render(self.text[i], True, '#174d4a'),
                                            (10, 10 + i * (height_for_surface - 8)))
        else:
            translate = googletrans.Translator()
            self.text = list()
            with open('text_for_developer.txt', mode='r', encoding='utf-8') as file:
                self.text = translate.translate(''.join([line for line in file]), src='russian',
                                                dest=lang).text.split(
                    '\n')
            font = pygame.font.SysFont(None, 22)
            width_for_surface, height_for_surface = 0, 0

            for i in self.text:
                width, height = font.render(i, False, 'white').get_size()
                if width_for_surface < width: width_for_surface = width
                if height_for_surface < height: height_for_surface = height

            self.surface_with_text = pygame.surface.Surface((500, 640))
            self.surface_with_text.fill('#d9bea7')
            for i in range(len(self.text)):
                self.surface_with_text.blit(font.render(self.text[i], True, '#174d4a'),
                                            (10, 10 + i * (height_for_surface - 8)))

    def show(self):
        self.exist = True

    def hide(self):
        self.exist = False

    def update(self):
        if self.exist:
            screen.blit(self.surface_with_text, (25, 25))
            self.back.render(screen)
            if mouse_button_1:
                if self.back.belong(pygame.mouse.get_pos()):
                    self.exist = False
                    self.hide()
                    return True

    def set_text(self, lang):
        a = googletrans.Translator()
        self.back.set_text(a.translate('Назад', src='russian', dest=lang).text)
        self.create_text(lang)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Ball_Creator(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.radius = radius
        self.add(bonus_group)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("green"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 0
        self.vy = 5

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, palki):
            for i in ball_group:
                a = Ball(15, i.rect.x, i.rect.y)
                if g.game.b.Ultimate_Form is True:
                    a.Ultimate_Form = True
                else:
                    a.Ultimate_Form = False
            self.kill()
        if pygame.sprite.spritecollideany(self, killing_borders):
            self.kill()


class Probivator(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.radius = radius
        self.add(bonus_group)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("blue"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 0
        self.vy = 5

    def Do_Ultimate_Form(self):
        for i in ball_group:
            if i.Ultimate_Form is True:
                i.Ultimate_Form = False
            else:
                i.Ultimate_Form = True

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, palki):
            self.kill()
            self.Do_Ultimate_Form()
        if pygame.sprite.spritecollideany(self, killing_borders):
            self.kill()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.Ultimate_Form = False
        self.radius = radius
        self.radius = radius
        self.add(ball_group)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        print(self.rect)
        self.vx = 4
        self.vy = 10

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, killing_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(-self.vx, -self.vy)
            self.vy = -self.vy + random.randint(-1, 1) / 10
        if pygame.sprite.spritecollideany(self, palki):
            sprite = pygame.sprite.spritecollide(self, palki, dokill=False)[0]
            tuple_point_x = (
                sprite.rect.x, sprite.rect.x + sprite.rect.width, self.rect.x - self.vx,
                self.rect.x + self.rect.width - self.vx)
            tuple_point_x2 = (
                sprite.rect.x, sprite.rect.x + sprite.rect.width, self.rect.x + self.vx,
                self.rect.x + self.rect.width + self.vx)
            if max(tuple_point_x2) - min(
                    tuple_point_x2) < sprite.rect.width + self.rect.width < max(
                tuple_point_x) - min(tuple_point_x):
                self.rect = self.rect.move(-self.vx, -self.vy)
                self.vx = -self.vx + random.randint(-1, 1) / 10
            else:
                self.rect = self.rect.move(-self.vx, -self.vy)
                self.vy = -self.vy + random.randint(-1, 1) / 10
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-self.vx, -self.vy)
            self.vx = -self.vx + random.randint(-1, 1) / 10
        if not self.Ultimate_Form:
            if pygame.sprite.spritecollideany(self, korobki):
                sprite = pygame.sprite.spritecollide(self, korobki, dokill=False)[0]
                tuple_point_x = (
                    sprite.rect.x, sprite.rect.x + sprite.rect.width, self.rect.x - self.vx,
                    self.rect.x + self.rect.width - self.vx)
                tuple_point_x2 = (
                    sprite.rect.x, sprite.rect.x + sprite.rect.width, self.rect.x + self.vx,
                    self.rect.x + self.rect.width + self.vx)
                self.rect = self.rect.move(self.vx, self.vy)
                if max(tuple_point_x2) - min(
                        tuple_point_x2) < sprite.rect.width + self.rect.width < max(
                    tuple_point_x) - min(tuple_point_x):
                    self.vx = -self.vx + random.randint(-1, 1) / 10
                else:
                    self.vy = -self.vy + random.randint(-1, 1) / 10


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        if y1 > 100 and self in horizontal_borders:
            self.add(killing_borders)


class Palka(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(palki)
        self.image = pygame.surface.Surface([x2 - x1, y2 - y1])
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.image.fill('white')

    def update(self):
        if self.rect.x > 395:
            self.rect.x -= 15
        if self.rect.x < 5:
            self.rect.x += 15


class Box(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(korobki)
        self.image = pygame.surface.Surface([x2 - x1, y2 - y1])
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.image.fill('white')

    def update(self):
        if pygame.sprite.spritecollideany(self, ball_group):
            if random.randint(1, 30) == 3:
                Probivator(15, self.rect.x, self.rect.y)
            elif random.randint(1, 30) == 6:
                Ball_Creator(15, self.rect.x, self.rect.y)
            g.game.count += 1
            self.kill()


class Game():
    def __init__(self, size):
        self.exist = False
        self.exactly = False
        self.results = 0
        self.width, self.height = size
        self.back = Button(475, 10, 540, 75, '<-')
        self.label_winner = Button(150, 100, 400, 180, 'Победа!')
        self.label_lose = Button(150, 100, 400, 180, 'Ты проиграл!')
        self.exit = Button(350, 688, 525, 758, 'Выйти')

    def show(self):
        self.exist = True

    def start_the_game(self):
        self.load_game()
        self.show()

    def hide(self):
        self.exactly = True
        self.question = LanguageCell('Вы точно хотите завершить игру?', scale=(430, 80))
        self.yes = Button(125, 350, 250, 400, '  ' + TEXTS[8] + '  ')
        self.no = Button(300, 350, 425, 400, '  ' + TEXTS[9] + '  ')

    def update(self):
        if self.exist:
            if self.exactly:
                self.yes.render(screen)
                self.no.render(screen)
                screen.blit(self.question, (60, 250))
                if mouse_button_1 == True:
                    if self.yes.belong(pygame.mouse.get_pos()):
                        self.exactly = False
                        self.exist = False
                        return True
                    elif self.no.belong(pygame.mouse.get_pos()):
                        self.exactly = False
            elif self.results == 1:
                self.exit.render(screen)
                self.label_winner.render(screen)
                if mouse_button_1 == True:
                    if self.exit.belong(pygame.mouse.get_pos()):
                        self.exist = False
                        self.results = 0
                        conn = sqlite3.connect('results.db')
                        cor = conn.cursor()
                        asd = time.time() - self.times
                        cor.execute(
                            f"""INSERT INTO results(count, time) VALUES('{str(self.count)}', '{str(round(asd))}');""")
                        conn.commit()
                        return True
            elif self.results == 2:
                self.exit.render(screen)
                self.label_lose.render(screen)
                if mouse_button_1 == True:
                    if self.exit.belong(pygame.mouse.get_pos()):
                        self.results = 0
                        self.exist = False
                        conn = sqlite3.connect('results.db')
                        cor = conn.cursor()
                        asd = time.time() - self.times
                        cor.execute(
                            f"""INSERT INTO results(count, time) VALUES('{str(self.count)}', '{str(self.count)}');""")
                        conn.commit()
                        return True
            else:
                self.back.render(screen)
                all_sprites.draw(screen)
                all_sprites.update()
                if mouse_button_1 == True:
                    if self.back.belong(pygame.mouse.get_pos()):
                        self.hide()
                if len(ball_group) == 0:
                    self.results = 2
                elif len(korobki) == 0:
                    self.results = 1

    def load_game(self):
        self.count = 0
        self.times = time.time()
        all_sprites.empty()
        ball_group.empty()
        palki.empty()
        korobki.empty()
        horizontal_borders.empty()
        vertical_borders.empty()
        Border(5, 5, self.width - 5, 5)
        Border(5, self.height - 5, self.width - 5, self.height - 5)
        Border(5, 5, 5, self.height - 5)
        Border(self.width - 5, 5, self.width - 5, self.height - 5)
        self.a = Palka(self.width - 200, self.height - 100, self.width - 50, self.height - 80)
        self.b = Ball(15, 400, 475)
        with open('data.txt', mode='r', encoding='utf-8') as file:
            area = random.choice(file.readlines())[:-1]
            for x in range(15):
                for y in range(15):
                    if area[x + y * 15] == '1':
                        Box(34 + x * 32 + 5, 34 + y * 32 + 5, 34 + (x + 1) * 32, 34 + (y + 1) * 32)

    def set_text(self, lang):
        a = googletrans.Translator()
        self.back.set_text(a.translate('Назад', src='russian', dest=lang).text)
        self.label_winner.set_text(a.translate(TEXTS[11], src='russian', dest=lang).text)
        self.label_lose.set_text(a.translate(TEXTS[12], src='russian', dest=lang).text)
        self.exit.set_text(a.translate(TEXTS[13], src='russian', dest=lang).text)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((550, 800))
    pygame.display.flip()
    g = Main_menu(screen, screen.get_size())
    g.show()
    run = True
    clock = pygame.time.Clock()
    while run:
        keys = pygame.key.get_pressed()
        screen.fill('black')
        mouse_button_1 = False
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 4:
                g.mouse_whell(4)
            elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 5:
                g.mouse_whell(5)
            elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                mouse_button_1 = True
        if keys[pygame.K_LEFT] and g.game.exist:
            g.game.a.rect.x -= 15
        if keys[pygame.K_RIGHT] and g.game.exist:
            g.game.a.rect.x += 15
        g.update()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
