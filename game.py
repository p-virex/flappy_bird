from random import choice

import pygame

pygame.init()
WIDTH, HEIGHT = (500, 500)
ARIAL_FONT_M = pygame.font.SysFont('rage', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('bg1.png'), (WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = True

pos_x = 0
speed = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.images = [pygame.image.load(f'fly_{ind}.png') for ind in range(1, 4)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (100, 100)

    def update(self):
        self.rect.y += 6
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipes, self).__init__()
        self.image = pygame.image.load('pipes.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.score = 0

    def update(self):
        self.rect.x -= 3
        if self.rect.x + self.rect.width < 0:
            self.rect.x = WIDTH
            self.rect.y = choice([0, -20, -30, -50, -70, -90, -110, -130, -150, -170, -200, -220, -250])
            self.score += 1


bird = Bird()
pipes = Pipes()
group = pygame.sprite.Group()
group.add(bird)
group.add(pipes)

while game is True:
    pressed = False

    clock.tick(20)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    pos_x -= speed
    x_rel = pos_x % WIDTH
    x_part2 = x_rel - WIDTH if x_rel > 0 else x_rel + WIDTH
    screen.blit(bg, (x_rel, 0))
    screen.blit(bg, (x_part2, 0))
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_SPACE]:
        bird.rect.y -= 10
        pressed = True
    group.update()
    if pygame.sprite.collide_mask(bird, pipes):
        game = False
        pygame.time.delay(5000)
    group.draw(screen)
    text = ARIAL_FONT_M.render(f'Score: {pipes.score}', True, (0, 0, 0))
    screen.blit(text, (20, 20))
    pygame.display.update()
