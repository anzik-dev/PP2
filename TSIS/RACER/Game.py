import pygame, sys
from pygame.locals import *
import random, time
from persistence import *
from ui import *

# --- Инициализация и настройки ---
pygame.init()

# Подгружаем сохраненки, если файла нет — ставим дефолт
settings = load_data("settings_racer.json", {"sound": True, "color_of_car": "Blue", "difficulty": "Medium"})

# Конфиги для уровней сложности: задержки спавна и скорость
DIFFICULTY_SETTINGS = {
    "Easy": {"money": 3000, "spawn": 5000, "speed": 4},
    "Medium": {"money": 5000, "spawn": 4000, "speed": 6},
    "Hard": {"money": 7000, "spawn": 2500, "speed": 8}
}

def apply_settings():
    """Раскидываем настройки сложности по глобальным переменным"""
    global MONEY_DELAY, SPAWN_DELAY, SPEED
    diff = settings.get("difficulty", "Medium")
    config = DIFFICULTY_SETTINGS[diff]
    
    MONEY_DELAY = config["money"]
    SPAWN_DELAY = config["spawn"]
    SPEED = config["speed"]

# Музыкальное сопровождение
pygame.mixer.music.load(r"TSIS\RACER\background.wav") 
if settings["sound"]: 
    pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Технические переменные для FPS и экрана
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета (стандартный набор)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Игровые параметры по умолчанию
SPAWN_DELAY = 4000
MONEY_DELAY = 5000
last_spawn_time = pygame.time.get_ticks()
last_coin_spawn_time = pygame.time.get_ticks()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED_LEVEL = 1
SCORE = 0
STATE = "MENU" 
USER_NAME = "PLAYER"
POWERUP_TYPES = ["nitro", "shield", "repair"]
COIN_SCORE = 0 

# Шрифты и окно
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"TSIS\RACER\AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# --- Игровые классы (Спрайты) ---

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(r"TSIS\RACER\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        # Если враг уехал за экран — засчитываем очко и кидаем его наверх
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, obs_type = "rock"):
        super().__init__()
        self.obs_type = obs_type
        # Грузим картинку в зависимости от того, камень это или бочка
        if self.obs_type == "rock":
            self.image = pygame.image.load(r"TSIS\RACER\rock.png")
        elif self.obs_type == "Petrol barrel":
            self.image = pygame.image.load(r"TSIS\RACER\petrol.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Чтобы не копились в памяти

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__() 
        image_path = f"TSIS\\RACER\\Player_{color}.png"
        
        try:
            self.image = pygame.image.load(image_path)
        except pygame.error:
            # Если с кастомным цветом беда — берем обычную картинку
            print(f"Предупреждение: Файл {image_path} не найден. Загружен стандартный Player.png")
            self.image = pygame.image.load(r"TSIS\RACER\Player.png")
            
        self.image_broken = pygame.image.load(r"TSIS\RACER\broken.png") 
        self.image_exploded = pygame.image.load(r"TSIS\RACER\exploded.png")
        
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
        self.status = "normal"
        self.has_shield = False
        
    def move(self):
        if self.status == "dead": return # Трупы не ездят

        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_type ="gold"):
        super().__init__()
        self.coin_type = coin_type
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        
        # Цвет кружочка зависит от типа монеты
        if self.coin_type == "gold":
            color = (255, 223, 0)
        elif self.coin_type == "diamond":
            color = (185, 242, 255)
            
        pygame.draw.circle(self.image, color, (17, 17), 17) 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def reset(self, enemies_group):
        # Спавним монету заново, но следим, чтобы не попала на врага
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        while pygame.sprite.spritecollideany(self, enemies_group):
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type 
        # Просто цветные квадратики для баффов (оранжевый, циан, зеленый)
        if self.type == "nitro":
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 165, 0)) 
        elif self.type == "shield":
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 255)) 
        elif self.type == "repair":
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))   
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# --- Инициализация групп спрайтов ---
powerups = pygame.sprite.Group()
active_buff = None
buff_timer = 0
last_buff_spawn = pygame.time.get_ticks()

P1 = Player(settings["color_of_car"])
E1 = Enemy()
C1 = Coin("gold")
C2 = Coin("diamond")

enemies = pygame.sprite.Group(E1)
gold_coins = pygame.sprite.Group(C1)
diamond_coins = pygame.sprite.Group(C2)
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(P1, E1, C1, C2)

def start_new_game():
    """Сброс всех параметров для начала новой катки"""
    global P1, E1, all_sprites, enemies, obstacles, gold_coins, diamond_coins, powerups, SCORE, COIN_SCORE, GAME_ENDING, active_buff, last_spawn_time, last_coin_spawn_time, last_buff_spawn
    apply_settings()
    SCORE = 0
    COIN_SCORE = 0
    GAME_ENDING = False
    active_buff = None
    
    P1 = Player(settings["color_of_car"])
    E1 = Enemy()
    
    enemies = pygame.sprite.Group(E1)
    obstacles = pygame.sprite.Group()
    gold_coins = pygame.sprite.Group()
    diamond_coins = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(P1, E1)
    
    now = pygame.time.get_ticks()
    last_spawn_time = now
    last_coin_spawn_time = now
    last_buff_spawn = now

# --- ГЛАВНЫЙ ЦИКЛ ИГРЫ ---
STATE = "MENU"
GAME_ENDING = False

while True:
    events = pygame.event.get()
    current_time = pygame.time.get_ticks()

    # --- ЛОГИКА МЕНЮ ---
    if STATE == "MENU":
        p_btn, s_btn, l_btn = draw_main_menu(DISPLAYSURF, font, font_small)
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if p_btn.collidepoint(event.pos):
                    start_new_game()
                    # Подтягиваем цвет машины из настроек перед стартом
                    selected_color = settings.get("color_of_car", "Blue")
                    P1 = Player(selected_color)
                    all_sprites.empty()
                    enemies.empty()
                    obstacles.empty()
                    gold_coins.empty()
                    diamond_coins.empty()
                    powerups.empty()
                    
                    E1 = Enemy()
                    enemies.add(E1)
                    all_sprites.add(P1, E1)
                    STATE = "GAME"
                    GAME_ENDING = False
                elif s_btn.collidepoint(event.pos):
                    STATE = "SETTINGS"
                elif l_btn.collidepoint(event.pos):
                    STATE = "LEADERBOARD"

    # --- ЛОГИКА НАСТРОЕК ---
    elif STATE == "SETTINGS":
        sn_btn, cl_btn, df_btn, back_btn = draw_settings_screen(DISPLAYSURF, font_small, settings)
        
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if sn_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    if settings["sound"]: pygame.mixer.music.unpause()
                    else: pygame.mixer.music.pause()
                
                elif cl_btn.collidepoint(event.pos):
                    colors = ["Blue", "Red", "Green"]
                    current_idx = colors.index(settings["color_of_car"])
                    next_idx = (current_idx + 1) % len(colors)
                    settings["color_of_car"] = colors[next_idx]
                
                elif df_btn.collidepoint(event.pos):
                    diffs = ["Easy", "Medium", "Hard"]
                    current_idx = diffs.index(settings["difficulty"])
                    next_idx = (current_idx + 1) % len(diffs)
                    settings["difficulty"] = diffs[next_idx]

                elif back_btn.collidepoint(event.pos):
                    save_data("settings.json", settings)
                    apply_settings() 
                    STATE = "MENU"

    # --- ЛОГИКА ГЕЙМПЛЕЯ ---
    elif STATE == "GAME":
        DISPLAYSURF.blit(background, (0,0))
        current_time = pygame.time.get_ticks()

        # Спавним препятствия по таймеру
        if current_time - last_spawn_time > SPAWN_DELAY:
            obs_type = random.choice(["rock", "Petrol barrel"])
            obstacle = Obstacles(obs_type)

            # Пытаемся не заспавнить препятствие на голове у врага
            attempts = 0
            while pygame.sprite.spritecollideany(obstacle, enemies) and attempts < 10:
                obstacle.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
                attempts += 1

            obstacles.add(obstacle)
            all_sprites.add(obstacle)
            last_spawn_time = current_time

        # Спавним монетки
        if current_time - last_coin_spawn_time > MONEY_DELAY:
            new_type = "diamond" if random.randint(1, 5) == 1 else "gold"
            new_coin = Coin(new_type)
            
            if not pygame.sprite.spritecollideany(new_coin, enemies):
                all_sprites.add(new_coin)
                if new_type == "gold": gold_coins.add(new_coin)
                else: diamond_coins.add(new_coin)
                last_coin_spawn_time = current_time
        
        # Рисуем интерфейс (счетчики и таймер баффа)
        scores = font_small.render(f"Score: {SCORE}", True, BLACK)
        coin_display = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
        if active_buff:
            timer_sec = 5 - (current_time - buff_timer) // 1000
            buff_txt = font_small.render(f"BUFF: {active_buff.upper()} ({timer_sec}s)", True, BLUE)
            DISPLAYSURF.blit(buff_txt, (10, 40))
        
        DISPLAYSURF.blit(scores, (10,10))
        DISPLAYSURF.blit(coin_display, (SCREEN_WIDTH - 110, 10))

        # Двигаем и рисуем всё, что есть на экране
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # Подбираем монетки (золото +1, алмаз +5)
        if pygame.sprite.spritecollide(P1, gold_coins, False):
            COIN_SCORE += 1
            for coin in gold_coins: coin.reset(enemies)

        if pygame.sprite.spritecollide(P1, diamond_coins, False):
            COIN_SCORE += 5
            for coin in diamond_coins: coin.reset(enemies)

        # Спавним баффы каждые 7 сек
        if current_time - last_buff_spawn > 7000:
            b_type = random.choice(["nitro", "shield", "repair"])
            new_buff = PowerUp(b_type)
            powerups.add(new_buff)
            all_sprites.add(new_buff)
            last_buff_spawn = current_time

        # Обработка того, что подобрали бафф
        buff_hit = pygame.sprite.spritecollideany(P1, powerups)
        if buff_hit:
            active_buff = buff_hit.type
            buff_timer = pygame.time.get_ticks()
            
            if active_buff == "repair":
                if P1.status == "broken":
                    P1.status = "normal"
                    P1.image = P1.image_normal
                active_buff = None # Починка разовая, таймер не включаем
            elif active_buff == "nitro":
                SPEED += 5 
            elif active_buff == "shield":
                P1.has_shield = True
            buff_hit.kill()

        # Выключение баффов по истечении 5 секунд
        if active_buff and current_time - buff_timer > 5000:
            if active_buff == "nitro": SPEED -= 5
            elif active_buff == "shield": P1.has_shield = False
            active_buff = None       

        # Столкновения с камнями/бочками
        obstacle_hit = pygame.sprite.spritecollideany(P1, obstacles)
        if obstacle_hit:
            if P1.has_shield:
                P1.has_shield = False
                active_buff = None 
                obstacle_hit.kill()
            else:    
                if obstacle_hit.obs_type == "Petrol barrel":
                    # Взрываемся на бочке
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(r'TSIS\RACER\explosion.mp3').play()
                    update_leaderboard(USER_NAME, SCORE)
                    P1.image = P1.image_exploded
                    P1.is_dead = True
                    GAME_ENDING = True
                    for entity in all_sprites:
                        if entity != P1: entity.kill()

                elif obstacle_hit.obs_type == "rock":
                    if P1.status == "broken":
                        # Добило вторым камнем
                        P1.status = "dead"
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound(r'TSIS\RACER\explosion.mp3').play()
                        P1.image = P1.image_exploded
                        update_leaderboard(USER_NAME, SCORE)
                        STATE = "GAMEOVER"
                        GAME_ENDING = True
                        for entity in all_sprites:
                            if entity != P1: entity.kill()
                    else:
                        # Просто ломаемся от первого камня
                        P1.status = "broken"
                        P1.image = P1.image_broken
                        obstacle_hit.kill()

        # Повышаем сложность (скорость) каждые 10 монет
        NEW_LEVEL = COIN_SCORE // 10 + 1
        if NEW_LEVEL > SPEED_LEVEL:
            SPEED_LEVEL = NEW_LEVEL
            SPEED += 1

        # Прямое столкновение с вражеской машиной
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop()
            pygame.mixer.Sound(r'TSIS\RACER\crash.wav').play()
            time.sleep(0.5)
            update_leaderboard(USER_NAME, SCORE)
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))
            pygame.display.update()
            for entity in all_sprites: entity.kill() 
            time.sleep(2)
            pygame.quit()
            sys.exit() 

        # Если игра "затухает" (после взрыва бочки)
        if GAME_ENDING:
            SPEED *= 0.95 
            if SPEED < 0.1:
                SPEED = 0
                time.sleep(1) 
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_over, (30, 250))
                pygame.display.update()
                time.sleep(2)
                pygame.quit()
                sys.exit()

    # --- КОНЕЦ ИГРЫ И ТАБЛИЦА ---
    elif STATE == "GAMEOVER":
        draw_game_over_screen(DISPLAYSURF, font, font_small, COIN_SCORE)
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                STATE = "MENU"

    elif STATE == "LEADERBOARD":
        back_btn = draw_leaderboard_screen(DISPLAYSURF, font_small)
        for event in events:
            if event.type == MOUSEBUTTONDOWN and back_btn.collidepoint(event.pos):
                STATE = "MENU"

    # Обработка выхода из окна
    if any(event.type == QUIT for event in events):
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)