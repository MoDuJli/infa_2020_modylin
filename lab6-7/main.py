import pygame as pg
from pygame.draw import *
from random import randint
import numpy

pg.init()

nickname = input("Nickname ")
file = open("top.txt", 'a')

screen_width = 1200
screen_height = 800
score = 0
FPS = 30

finished = False
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

max_velocity = 3
min_death_time = 50
max_death_time = 180
min_radius = 10
max_radius = 100

ball_number = 10
ball_X = []
ball_Y = []
ball_R = []
ball_Color = []
ball_Vx = []
ball_Vy = []
ball_time = []
ball_death_time = []
brownian_particle_number = 3
brownian_particle_ax = []
brownian_particle_ay = []
max_acceleration = 1


def text(score):
    f1 = pg.font.SysFont('arial', 55)
    text = f1.render(score, 1, GREEN)
    screen.blit(text, (60, 20))


# Заполняем массивы с параметрами шариков
for i in range(ball_number + brownian_particle_number):
    ball_X.append(0)
    ball_Y.append(0)
    ball_Vx.append(0)
    ball_Vy.append(0)
    ball_R.append(0)
    ball_Color.append(0)
    ball_time.append(0)
    ball_death_time.append(0)

# Заполняем массивы с параметрами броуновских частиц
for i in range(brownian_particle_number):
    brownian_particle_ax.append(randint(-max_acceleration, max_acceleration))
    brownian_particle_ay.append(randint(-max_acceleration, max_acceleration))


# функция изменяет параметры i-того шарика на новые
def new_ball(i):
    ball_X[i] = randint(int(screen_width * 0.1), int(screen_width * 0.9))
    ball_Y[i] = randint(int(screen_height * 0.1), int(screen_height * 0.9))
    ball_Vx[i] = randint(-max_velocity, max_velocity)
    ball_Vy[i] = randint(-max_velocity, max_velocity)
    ball_R[i] = randint(min_radius, max_radius)
    ball_Color[i] = COLORS[randint(0, 5)]
    ball_time[i] = 0
    ball_death_time[i] = randint(min_death_time, max_death_time)


# создаем первую партию шариков и броуновских частиц
for i in range(ball_number + brownian_particle_number):
    new_ball(i)

# Основной цикл программы
while not finished:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

        # Проверяем попадание по шарику
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            for i in range(ball_number + brownian_particle_number):
                if (mouse_x - ball_X[i]) ** 2 + (mouse_y - ball_Y[i]) ** 2 <= ball_R[i] ** 2:
                    new_ball(i)
                    if max_radius >= ball_R[i] >= max_radius * 0.5:
                        score += 1
                    if max_radius * 0.5 > ball_R[i] >= max_radius * 0.3:
                        score += 2
                    if ball_R[i] < max_radius * 0.3:
                        score += 4

    # Поддерживаем кол-во шариков
    for i in range(ball_number - brownian_particle_number):

        circle(screen, ball_Color[i], (ball_X[i], ball_Y[i]), ball_R[i])
        ball_time[i] += 1

        if ball_time[i] >= ball_death_time[i]:
            new_ball(i)

        # Проверяем выход i-того шарика из зоны экрана
        if ball_X[i] > screen_width * 0.9:
            ball_Vx[i] = randint(-max_velocity, 0)
        if ball_X[i] < screen_width * 0.1:
            ball_Vx[i] = randint(0, max_velocity)
        if ball_Y[i] > screen_height * 0.9:
            ball_Vy[i] = randint(-max_velocity, 0)
        if ball_Y[i] < screen_height * 0.1:
            ball_Vy[i] = randint(0, max_velocity)

        # Изменяем положение шариков на новое
        ball_X[i] += ball_Vx[i]
        ball_Y[i] += ball_Vy[i]

    # Прорисовываем броуноские частицы
    for i in range(brownian_particle_number):
        j = i + ball_number
        R = numpy.abs((ball_Color[j][0] + 3 * ball_time[j]) % 255)
        G = numpy.abs((ball_Color[j][1] + 3 * ball_time[j]) % 255)
        B = numpy.abs((ball_Color[j][2] + 3 * ball_time[j]) % 255)

        circle(screen, (R, G, B), (ball_X[j], ball_Y[j]), ball_R[j])
        circle(screen, (BLACK), (ball_X[j], ball_Y[j]), ball_R[j], 8)
        ball_time[j] += 1

        if ball_time[j] >= ball_death_time[j]:
            new_ball(j)

        # Проверяем выход i-того шарика из зоны экрана
        if ball_X[j] > screen_width * 0.9:
            ball_Vx[j] = randint(-max_velocity, 0)
        if ball_X[j] < screen_width * 0.1:
            ball_Vx[j] = randint(0, max_velocity)
        if ball_Y[j] > screen_height * 0.9:
            ball_Vy[j] = randint(-max_velocity, 0)
        if ball_Y[j] < screen_height * 0.1:
            ball_Vy[j] = randint(0, max_velocity)

        # изменяем скорость броуновской частицы
        ball_Vx[j] += randint(-max_velocity, max_velocity)
        ball_Vy[j] += randint(-max_velocity, max_velocity)

        # Изменяем положение броуновской частицы на новое
        ball_X[j] += ball_Vx[j]
        ball_Y[j] += ball_Vy[j]

    text(str(score))
    pg.display.update()
    screen.fill((100, 100, 100))

file.write(nickname + " " + str(score) + '\n')
file.close()

pg.quit()
