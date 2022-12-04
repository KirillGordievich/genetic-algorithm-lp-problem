import pygame
#from ga_ver_for_vis import *
from ga_functions import *
from paramaters_ga import *


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (200, 0, 0 )
BLUE = (0, 0, 128)

def limits(x1, x2):
    if 5*x1 + 2*x2 > 30:
        return False
    if 8*x1 + 11*x2 > 60:
        return False
    if x1 < 0:
        return False
    if x2 < 0:
        return False
    return True

def draw_coordinate_system(screen, init, ordinate, abcissa, fat, color):
    pygame.draw.line(screen, color, init, ordinate, fat)
    pygame.draw.line(screen, color, init, abcissa, fat)

def draw_limits(screen, points, color):
    pygame.draw.line(screen, color, points[0], points[1], 3)

def limits_coordinate(eqution, screen_width, screen_height, d, scale):
    point = []

    for i in range(2):
        if eqution[i] > 0:
            if i == 1:
                y = (screen_height - scale * (eqution[2] / eqution[i]) - d)
                x = d
                if y < 0:
                    y = -(scale * (eqution[2] / eqution[i]) - d - screen_height)
                point.append([x, y])

            else:
                point.append([d + scale*(eqution[2] / eqution[i]), screen_height - d])
        elif eqution[i] < 0:
            if i == 1:
                point.append([d, d + scale*(eqution[2] - eqution[i]*screen_width)])
            else:
                point.append([(eqution[2] - eqution[i]*screen_height), 0])
        else:
            if i == 0:
                point.append([screen_width, screen_height - scale*eqution[2] / eqution[1] - d])
            else:
                point.append([(eqution[2] / eqution[0])*scale + d, 0])

    return point

def draw_population(screen, population, color, scale, d, screen_height):
    for i in range(len(population)):
        pygame.draw.circle(screen, color,
                           [int(population[i][0]*scale + d),
                            screen_height - int(population[i][1]*scale) - d], 5)

f = lambda x1, x2: (2*x1 - 0.1*x1**2 + 3*x2 - 0.1*x2**2)
population = create_random_population(n_gen, n_hrom, initial_range, limits)

pygame.init()
screen_width, screen_height = 1600, 1080

axe_translation = 50
fat = 5
fps = 60
scale = 100
delay = 1000
equation1 = [5, 2, 30]
equation2 = [8, 11, 60]
i = 0
max = 0
max_p = 0
best_outputs = []
num_generations = 3000

points1 = limits_coordinate(equation1, screen_width, screen_height, axe_translation, scale)
points2 = limits_coordinate(equation2, screen_width, screen_height, axe_translation, scale)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN) #, pygame.FULLSCREEN = k
clock = pygame.time.Clock()
init = [axe_translation, screen_height - axe_translation]
ordinate = [screen_width - axe_translation, screen_height - axe_translation]
abcissa = [axe_translation, axe_translation]
mainloop = True
text_size = 36
f1 = pygame.font.Font(None, text_size)

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            mainloop = False
    screen.fill(WHITE)
    draw_coordinate_system(screen, init, ordinate, abcissa, fat, BLACK)
    draw_limits(screen, points1, BLACK)
    draw_limits(screen, points2, BLACK)

    if i < num_generations:
        text1 = f1.render('Generation %s' % (i), 1, BLACK)
        screen.blit(text1, (screen_width/2, text_size))
        draw_population(screen, population, YELLOW, scale, axe_translation, screen_height)
        pygame.display.update()
        pygame.time.delay(delay)
        f_values = function_values(f, population)
        parents = sorted(population, key=lambda tup: f(tup[0], tup[1]))[-1:-int(n_hrom*k):-1]  # выбираем лучших, половину
        draw_population(screen, parents, RED, scale, axe_translation, screen_height)
        pygame.display.update()
        pygame.time.delay(delay)
        best_outputs = sorted(f_values)[-1:-int(n_hrom * k):-1]

        if max < best_outputs[0]:
            max = best_outputs[0]
            max_p = parents[0]
        offspring = crossover(parents, n_hrom, n_gen, limits)
        draw_population(screen, offspring, GREEN, scale, axe_translation, screen_height)
        pygame.display.update()
        pygame.time.delay(delay)
        population = parents + mutation(offspring, k_mutation, limits)
        s = 0
        i += 1
    else:
        if s < 1:
            s += 1
        draw_population(screen, [max_p], GREEN, scale, axe_translation, screen_height)
        text1 = f1.render('Max F(x) = %s находится в точке %s, найдено за %s поколений ' % (max, max_p, i), 1, BLACK)
        screen.blit(text1, (200, 100))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()