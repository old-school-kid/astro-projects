import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1020
HEIGHT = 600


win = pygame.display.set_mode((WIDTH, HEIGHT))
colours = [[0, 0, 0], [0, 255, 0], [0, 0, 128], [255, 128, 0], [0, 153, 0]]
# white, red, green, cyan, magenta, orange, dark green
WHITE = [255, 255, 255]
BLUE = [0, 0, 255]
RED = [255, 0, 0]

win.fill(WHITE)

MaxFps = 90

G = 6.7 * (10 ** -2) * 10


class Body(object):
    def __init__(self, x, y, radius, colour, mass, x_vel, y_vel):
        self.x = x
        self.y = y
        self.dead = False
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel

    def move(self, zooms, centre):
        self.x += self.x_vel + centre["x_move"]
        self.y += self.y_vel + centre["y_move"]
        if zooms[1] != zooms[0]:
            x_from_centre, y_from_centre = centre["x"] - self.x, centre["y"] - self.y
            self.x += x_from_centre * zooms[1]
            self.y += y_from_centre * zooms[1]
            self.radius = self.radius * (1 + zooms[1])

    def draw(self, win, zooms, centre):
        if not self.dead:
            self.move(zooms, centre)
            pygame.draw.circle(win, self.colour, (round(self.x), round(self.y)),
                               round(self.radius))


def single_press_inc(key):
    if key > 0:
        if key > 90:
            key = 0
        else:
            key += 1
    return key


def spawn_body(x, y, mass, colour, bodies, x_vel, y_vel):
    radius = math.sqrt(mass)
    bodies.append(Body(x, y, radius, colour, mass, x_vel, y_vel))
    return bodies


def impact(body1, body2, bodies):
    new_mass = body1.mass + body2.mass
    if body1.mass > body2.mass:
        new_x, new_y = body1.x, body1.y
    else:
        new_x, new_y = body2.x, body2.y
    new_x_vel = ((body1.x_vel * body1.mass + body2.x_vel * body2.mass) / new_mass)
    new_y_vel = ((body1.y_vel * body1.mass + body2.y_vel * body2.mass) / new_mass)
    bodies = (spawn_body(new_x, new_y, new_mass, (169, 169, 169), bodies, new_x_vel, new_y_vel))
    body1.dead = True
    body2.dead = True
    return bodies


def gravity_calc(major_body, minor_body):
    hypotenuse = math.hypot(abs(major_body.x - minor_body.x), abs(major_body.y - minor_body.y))
    if hypotenuse == 0:
        g = 0
        ratio_total = 1
    else:
        g = (G * major_body.mass) / hypotenuse ** 2
        ratio_total = (abs(major_body.x - minor_body.x)) + (abs(major_body.y - minor_body.y))
    minor_body.x_vel += g * ((major_body.x - minor_body.x) / ratio_total)
    minor_body.y_vel += g * ((major_body.y - minor_body.y) / ratio_total)


def redraw(bodies, zooms, horizontal_move, vertical_move):
    win.fill(WHITE)
    centre = {"x": (WIDTH + horizontal_move) / 2,
              "y": (HEIGHT + vertical_move) / 2,
              "x_move": horizontal_move,
              "y_move": vertical_move
              }
    for i in bodies:
        Body.draw(i, win, zooms, centre)
    zooms[1] = 0
    pygame.display.update()


def mainloop():
    run = True
    single_press = [0]
    bodies = []
    pause = False
    zoom, last_zoom = 0, 0
    horizontal_move = 0
    vertical_move = 0
    for i in range(0, 200):
        bodies = spawn_body(random.randint(0, WIDTH), random.randint(0, HEIGHT),
                            10, (169, 169, 169), bodies, random.uniform(-2, 2), random.uniform(-2, 2))
    while run:
        clock.tick(MaxFps)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and single_press[0] == 0:
            pause = not pause
            single_press[0] = 1

        for i in single_press:
            single_press[single_press.index(i)] = single_press_inc(i)

        while not pause:
            clock.tick(MaxFps)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = True
                    run = False

            for i in single_press:
                single_press[single_press.index(i)] = single_press_inc(i)

            if keys[pygame.K_SPACE] and single_press[0] == 0:
                pause = True
                single_press[0] = 1

            if keys[pygame.K_a]:
                horizontal_move -= 15

            if keys[pygame.K_d]:
                horizontal_move += 15

            if keys[pygame.K_w]:
                vertical_move -= 15

            if keys[pygame.K_s]:
                vertical_move += 15

            if keys[pygame.K_q]:
                zoom -= 0.001

            if keys[pygame.K_e]:
                zoom += 0.001

            for body1 in bodies:
                for body2 in bodies:
                    if not body1.dead and not body2.dead:
                        gravity_calc(body1, body2)
            for i, body1 in enumerate(bodies):
                for j in range(i + 1, len(bodies)):
                    body2 = bodies[j]
                    radius = max(body1.radius, body2.radius)
                    if math.hypot(abs(body1.x - body2.x), abs(body1.y - body2.y)) < radius and not body1.dead and not body2.dead:
                        bodies = impact(body1, body2, bodies)

            zooms = [last_zoom, zoom]
            last_zoom = zoom
            redraw(bodies, zooms, horizontal_move, vertical_move)
            horizontal_move, vertical_move = 0, 0


mainloop()
pygame.QUIT