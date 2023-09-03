# This is a sample Python script.
import random
from pygame import mixer
import pygame

global game_score
game_score = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.font.init()
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 30)

explosion_fx = pygame.mixer.Sound('img/explosion.wav')
explosion_fx.set_volume(0.25)

explosion_fx2 = pygame.mixer.Sound('img/explosion2.wav')
explosion_fx2.set_volume(0.10)

laser_fx = pygame.mixer.Sound('img/laser.wav')
laser_fx.set_volume(0.25)

screen_width = 800
screen_height = 600

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
background_music = pygame.mixer.Sound('img/backround_music.mp3')

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')
run = True

# load image
bg = pygame.image.load('img/background.jpg')
bg1 = pygame.transform.rotate(bg, 180)
bg2 = pygame.transform.flip(bg1, False, True)


class Createspaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.cool_down = 300

    def update(self):
        movement_speed = 8
        key = pygame.key.get_pressed()
        game_over = 0
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= movement_speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += movement_speed
        time_now = pygame.time.get_ticks()

        # create mask
        self.mak = pygame.mask.from_surface(self.image)

        if key[pygame.K_SPACE] and time_now - self.last_shot > self.cool_down:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            self.cool_down -= 0.1
            bullet_group.add(bullet)
            self.last_shot = time_now

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (
            self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)),
            15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        global game_score
        alien_killed = False
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            print("killed")
            game_score += 100


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(f"img/exp{i}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count = random.randint(0, 1)

    def update(self):
        x_speed_val = 3
        y_speed_value = 0.51
        if self.count == 0:
            self.rect.x += x_speed_val
            self.rect.y += y_speed_value
            if self.rect.x >= 800:
                self.rect.y += 10
                self.count = 1
        elif self.count == 1:
            self.rect.x -= x_speed_val
            self.rect.y += y_speed_value
            if self.rect.x < 0:
                self.rect.y += 10
                self.count = 0
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            explosion_fx2.play()
            spaceship.health_remaining -= 1
            self.kill()


alien_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
spaceship = Createspaceship(int(screen_width / 2), screen_height - 100, 10)
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

spaceship_group.add(spaceship)

# define fps
clock = pygame.time.Clock()
fps = 60

scroll_y = -600
background_x = 0
rand = list((scroll_y, screen.get_rect().bottom))
rand1 = -rand[1]
delay_time = 1750
time_level = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()
count_down = 3
game_over = 0
last_count = pygame.time.get_ticks()
background_music.play(-1)

while run:

    clock.tick(fps)
    # draw backround screen
    if count_down == 0:
        background_x += 1.5
        rand1 += 1.5
        scroll_y += 1.5

        screen.blit(bg1, (0, rand1))
        screen.blit(bg2, (0, background_x))

        if rand1 == 0:
            background_x = - 600
            scroll_y = - 600
            bg1 = pygame.transform.rotate(bg, 180)
        if scroll_y == 0:
            rand1 = - 600
        rand_time_var = pygame.time.get_ticks()

        if rand_time_var - time_level >= 5000:
            time_level = pygame.time.get_ticks()
            if delay_time >= 600:
                delay_time -= 50
        if pygame.time.get_ticks() - current_time >= delay_time:
            current_time = pygame.time.get_ticks()
            alien = Aliens(random.randint(1, 800), -10)
            alien_group.add(alien)

        if game_over == 0:
            game_over = spaceship.update()
            bullet_group.update()
            print(game_score)
            draw_text(f"Score: {str(game_score)}", font40, white, 0, 0)
            alien_group.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:
                screen.blit(bg2, (0, 0))
                draw_text('GAME OVER', font40, white, int(screen_width / 2 - 70), int(screen_height / 2 + 50))

    if count_down > 0:
        screen.blit(bg2, (0, 0))
        draw_text('GET READY', font40, white, int(screen_width / 2 - 70), int(screen_height / 2 + 50))
        draw_text(str(count_down), font40, white, int(screen_width / 2), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            count_down -= 1
            last_count = count_timer
    explosion_group.update()

    alien_group.draw(screen)
    bullet_group.draw(screen)
    explosion_group.draw(screen)
    alien_bullet_group.draw(screen)
    spaceship_group.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
