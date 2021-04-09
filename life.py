import pygame
import os
from os import path
import sys
from random import randint
from copy import deepcopy


RES = 1500, 1000
WIDTH, HEIGHT = 1500, 900
pice = 30
W, H = WIDTH // pice, HEIGHT // pice
FPS = 6

pygame.init()
surface = pygame.display.set_mode(RES)
pygame.display.set_caption('LIFE')
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (30, 30))
    return image


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("cell.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)

snd_dir = path.join(path.dirname(__file__), 'sounds')
click_s= pygame.mixer.Sound(os.path.join(snd_dir, 'boing.mp3'))
blop_s = pygame.mixer.Sound(os.path.join(snd_dir, 'blop.mp3'))
music_s = pygame.mixer.Sound(os.path.join(snd_dir, 'cave.mp3'))
music_s.play()
def main():

    surface.fill(pygame.Color(40, 41, 41, 1))
    game()


font_name = pygame.font.match_font('Segoe UI Light')


def draw_text(surf=surface, text='НАЧАТЬ ЭВОЛЮЦИЮ', size=40, x=750, y=950, color=(246, 255, 166, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def cell(cur_mass, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if cur_mass[j][i]:
                count += 1

    if cur_mass[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0

#функция отвечающая за случайную генерацию клеток
def rand_dot(cur_mass, next_mass):
    cur_mass.clear()
    surface.fill(pygame.Color(40, 41, 41, 1))
    [pygame.draw.line(surface, pygame.Color('darkslategray'),
                      (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, pice)]
    [pygame.draw.line(surface, pygame.Color('darkslategray'),
                      (0, y), (WIDTH, y)) for y in range(0, HEIGHT, pice)]
    cur_mass = [[0 for i in range(W)] for j in range(H)]
    cur_mass = [[randint(-5, 5) for i in range(W)] for j in range(H)]
    for i in range(H):
        for j in range(W):
            if cur_mass[i][j] > 1:
                sprite.rect.x = j * pice
                sprite.rect.y = i * pice
                all_sprites.draw(surface)


def star_game(cur_mass, next_mass):
    global FPS
    
    m_x = int(pice / 2)
    m_y = int(pice / 2)
    for i in range(H):
        for j in range(W):
            last_color = surface.get_at((m_x, m_y))
            print(last_color)
            if last_color != (40, 41, 41, 255):
                cur_mass[i][j] = 1
            m_x = m_x + pice
        m_y = m_y + pice
        m_x = int(pice / 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    FPS += 1
                else:
                    FPS -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                cu_x, cu_y = pygame.mouse.get_pos()
                last_color = surface.get_at((cu_x, cu_y))
                print(last_color)
                if last_color == (22, 84, 84, 255) or last_color == (249, 255, 166, 255):
                    blop_s.play()
                    exit()
                if last_color == (227, 84, 84, 255) or last_color == (242, 226, 152, 255):
                    FPS = 10
                    blop_s.play()
                    main()
        surface.fill(pygame.Color(40, 41, 41, 1))
        pygame.draw.rect(surface, pygame.Color(
            'mediumaquamarine'), (0, 900, 1500, 1000))
        draw_text(surface, 'Идёт процесс эволюции', y=940)
        pygame.draw.rect(surface, pygame.Color(
            (227, 84, 84)), (1300, 900, 1500, 1000))
        draw_text(surface, 'Перезапуск', 30, 1400,
                  940, color=(245, 255, 166, 255))
        pygame.draw.rect(surface, pygame.Color(
            (22, 84, 84)), (0, 900, 200, 1000))
        draw_text(surface, 'Выход', 30, 90, 940, color=(249, 255, 166, 255))
        [pygame.draw.line(surface, pygame.Color('darkslategray'),
                          (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, pice)]
        [pygame.draw.line(surface, pygame.Color('darkslategray'),
                          (0, y), (WIDTH, y)) for y in range(0, HEIGHT, pice)]
        # draw life
        for x in range(1, W - 1):
            for y in range(1, H - 1):
                if cur_mass[y][x]:

                    sprite.rect.x = x * pice + 2
                    sprite.rect.y = y * pice + 2
                    all_sprites.draw(surface)
                    click_s.play()
                next_mass[y][x] = cell(cur_mass, x, y)

        cur_mass = deepcopy(next_mass)

        print(clock.get_fps())
        pygame.display.flip()
        clock.tick(FPS)

#изначальная функци
def game():
    while True:
        next_mass = [[0 for i in range(W)] for j in range(H)]
        cur_mass = [[0 for i in range(W)] for j in range(H)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cu_x, cu_y = pygame.mouse.get_pos()
                m_x = int(cu_x / pice)
                m_y = int(cu_y / pice)
                last_color = surface.get_at((cu_x, cu_y))
                blop_s.play()
                if last_color == (102, 205, 170, 255) or last_color == (246, 255, 166, 255):
                    star_game(cur_mass, next_mass)
                elif last_color == (40, 41, 41, 255):
                    sprite.rect.x = m_x * pice
                    sprite.rect.y = m_y * pice
                    all_sprites.draw(surface)
                    print(m_x * pice, m_y * pice)
                elif last_color == (220, 248, 164, 255) or last_color == (74, 145, 137, 255):
                    blop_s.play()
                    rand_dot(cur_mass, next_mass)
                else:
                    pygame.draw.rect(surface, pygame.Color(
                        40, 41, 41, 1), (m_x * pice, m_y * pice, pice, pice))

        pygame.draw.rect(surface, pygame.Color(
            'mediumaquamarine'), (0, 900, 1500, 1000))
        draw_text(surface)
        pygame.draw.rect(surface, pygame.Color(
            (74, 145, 137, 1)), (0, 900, 300, 1000))
        draw_text(surface, text='Случайная генерация', size=30,
                  x=150, y=950, color=(230, 255, 166, 255))
        [pygame.draw.line(surface, pygame.Color('darkslategray'),
                          (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, pice)]
        [pygame.draw.line(surface, pygame.Color('darkslategray'),
                          (0, y), (WIDTH, y)) for y in range(0, HEIGHT, pice)]

        print(clock.get_fps())
        pygame.display.flip()
        clock.tick(FPS)


main()
