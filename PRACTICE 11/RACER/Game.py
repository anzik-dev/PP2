import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

pygame.mixer.music.load(r"PRACTICE 11\RACER\background.wav") 
pygame.mixer.music.play(-1) 
pygame.mixer.music.set_volume(0.5)

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED_LEVEL = 1
SCORE = 0
COIN_SCORE = 0 # Переменная для подсчета собранных монет

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"PRACTICE 11\RACER\AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(r"PRACTICE 11\RACER\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(r"PRACTICE 11\RACER\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Класс монетки: создает желтый круг и управляет его логикой
class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_type ="gold"):
        super().__init__()

        self.coin_type = coin_type
        # Создание поверхности 35x35 с поддержкой прозрачности
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        # Разные цвета для разных типов
        if self.coin_type == "gold":
            color = (255, 223, 0)
        elif self.coin_type == "diamond":
            color = (185, 242, 255)
        # Отрисовка монетки
        pygame.draw.circle(self.image, color, (17, 17), 17) 
        self.rect = self.image.get_rect()
        self.rect.center = (0, -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.reset(enemies)

    # Метод сброса: гарантирует, что монетка не появится поверх врага
    def reset(self, enemies_group):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        # Проверка на перекрытие с вражескими машинами
        while pygame.sprite.spritecollideany(self, enemies_group):
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Инициализация объектов и групп
P1 = Player()
E1 = Enemy()
C1 = Coin("gold")
C2 = Coin("diamond")

enemies = pygame.sprite.Group()
enemies.add(E1)

gold_coins = pygame.sprite.Group()
gold_coins.add(C1)

diamond_coins = pygame.sprite.Group()
diamond_coins.add(C2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)

# Начальный сброс монетки для корректного появления на старте
C1.reset(enemies)

while True:
    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Отображение счета врагов (слева) и монет (справа)
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_display = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_display, (SCREEN_WIDTH - 110, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Логика сбора монеток игроком
    if pygame.sprite.spritecollide(P1, gold_coins, False):
        COIN_SCORE += 1
        for coin in gold_coins:
            coin.reset(enemies)

    if pygame.sprite.spritecollide(P1, diamond_coins, False):
        COIN_SCORE += 5
        for coin in diamond_coins:
            coin.reset(enemies)


    NEW_LEVEL = COIN_SCORE // 10 + 1
    if NEW_LEVEL > SPEED_LEVEL:
        SPEED_LEVEL = NEW_LEVEL
        SPEED +=1

    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.music.stop()
          pygame.mixer.Sound(r'PRACTICE 11\RACER\crash.wav').play()
          time.sleep(0.5)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)