import pygame
import random
import sys
import json
import db  
from config import *
class Snake:
    def __init__(self, color_head, color_body):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color_head = color_head
        self.color_body = color_body

    def change_dir(self, key):
        if key == pygame.K_UP and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif key == pygame.K_DOWN and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif key == pygame.K_LEFT and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.direction != (-1, 0):
            self.next_direction = (1, 0)

    def move(self, grow=1):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if grow == 0:
            self.body.pop()
        elif grow < 0: # Уменьшение от яда
            self.body.pop()
            if len(self.body) > 1:
                self.body.pop()
        else:
            for _ in range(grow - 1):
                self.body.append(self.body[-1])

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() # Инициализируем микшер
    
        # Загружаем музыку (укажи путь к своему файлу)
        try:
            pygame.mixer.music.load("TSIS\SNAKE\music.mp3") 
            pygame.mixer.music.set_volume(0.5) 
        except:
            print("Файл музыки не найден")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Snake Ultimate")
        self.clock = pygame.time.Clock()
        self.main_font = pygame.font.SysFont("Verdana", 28, bold=True)
        self.ui_font = pygame.font.SysFont("Consolas", 18)
        
        # Инициализация БД и Настроек
        db.create_tables()
        self.load_settings()
        
        self.state = "MENU" # MENU, GAME, GAME_OVER, LEADERBOARD, SETTINGS
        self.username = ""
        self.personal_best = 0
        self.top_players = []


    def update_music(self):
        # Проверяем, есть ли вообще в настройках ключ "sound"
        if self.settings.get("sound", True):
            # Если музыка еще не играет, запускаем её
            if not pygame.mixer.music.get_busy():
                try:
                    pygame.mixer.music.play(-1) # -1 — играть бесконечно
                except pygame.error:
                    print("Ошибка: Не удалось воспроизвести файл. Проверь путь к музыке.")
        else:
            # Если звук выключен в настройках — останавливаем плеер
            pygame.mixer.music.stop()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {
                "sound": True, 
                "grid": True, 
                "snake_color": "Green" # Green, Pink, Orange
            }
            self.save_settings()
            self.update_music()

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def get_snake_colors(self):
        colors = {
            "Green": (SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR),
            "Pink": ((255, 105, 180), (199, 21, 133)),
            "Orange": ((255, 140, 0), (205, 92, 92))
        }
        return colors.get(self.settings["snake_color"], colors["Green"])

    def reset_game(self):
        self.update_music()
        head_c, body_c = self.get_snake_colors()
        self.snake = Snake(head_c, body_c)
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.walls = set() # Стены теперь появляются с 3 уровня
        
        self.food = self._spawn_item()
        self.poison = self._spawn_item() if random.random() > 0.5 else None
        self.powerup = None
        self.powerup_type = None # 1: Speed, 2: Ghost, 3: Double Score
        self.active_powerup = None
        self.powerup_timer = 0
        
        self.food_spawn_time = pygame.time.get_ticks()
        self.powerup_spawn_time = pygame.time.get_ticks()

    def _spawn_item(self):
        while True:
            pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
            if pos not in self.snake.body and pos not in self.walls:
                return pos

    def _generate_level_walls(self):
        self.walls.clear()
        if self.level >= 3:
            # Случайные блоки, кол-во зависит от уровня
            num_blocks = (self.level - 2) * 5
            for _ in range(num_blocks):
                pos = self._spawn_item()
                # Избегаем спавна прямо перед головой змеи
                if abs(pos[0] - self.snake.body[0][0]) > 3 and abs(pos[1] - self.snake.body[0][1]) > 3:
                    self.walls.add(pos)

    def draw_node(self, pos, color, is_food=False):
        gap = 1 if not self.settings["grid"] else 2
        rect = pygame.Rect(
            pos[0] * CELL_SIZE + gap, pos[1] * CELL_SIZE + gap,
            CELL_SIZE - gap * 2, CELL_SIZE - gap * 2
        )
        if is_food:
            pygame.draw.ellipse(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

    # --- ЭКРАНЫ ---
    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        title = self.main_font.render("NEON SNAKE", True, SNAKE_HEAD_COLOR)
        prompt = self.ui_font.render("Enter Username:", True, TEXT_COLOR)
        name_img = self.main_font.render(self.username + "_", True, UI_COLOR)
        hint = self.ui_font.render("Press ENTER to Play | L for Leaderboard | S for Settings", True, WALL_COLOR)

        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        self.screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 200))
        self.screen.blit(name_img, (WIDTH//2 - name_img.get_width()//2, 240))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 400))

    def draw_settings(self):
        self.screen.fill(BG_COLOR)
        title = self.main_font.render("SETTINGS", True, UI_COLOR)
        grid_txt = self.ui_font.render(f"1. Toggle Grid: {self.settings['grid']}", True, TEXT_COLOR)
        sound_txt = self.ui_font.render(f"2. Toggle Sound: {self.settings['sound']}", True, TEXT_COLOR)
        color_txt = self.ui_font.render(f"3. Snake Color: {self.settings['snake_color']}", True, TEXT_COLOR)
        hint = self.ui_font.render("Press 1, 2, 3 to change | ESC to Menu", True, WALL_COLOR)

        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        self.screen.blit(grid_txt, (100, 150))
        self.screen.blit(sound_txt, (100, 200))
        self.screen.blit(color_txt, (100, 250))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 400))

    def draw_leaderboard(self):
        self.screen.fill(BG_COLOR)
        title = self.main_font.render("TOP 10 PLAYERS", True, DOUBLE_POINT_FOOD_COLOR if 'DOUBLE_POINT_FOOD_COLOR' in globals() else (255, 215, 0))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        y = 100
        for i, row in enumerate(self.top_players):
            # row: username, score, level, played_at
            txt = self.ui_font.render(f"{i+1}. {row[0]} - Score: {row[1]} (Lvl {row[2]})", True, TEXT_COLOR)
            self.screen.blit(txt, (100, y))
            y += 30

        hint = self.ui_font.render("Press ESC to return", True, WALL_COLOR)
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 50))

    def game_over(self):
        if self.username:
            db.save_result(self.username, self.score, self.level)
        self.state = "GAME_OVER"

    def draw_game_over(self):
        self.screen.fill(BG_COLOR)
        msg = self.main_font.render("WASTED", True, FOOD_COLOR)
        stats = self.ui_font.render(f"Score: {self.score} | Level: {self.level}", True, TEXT_COLOR)
        hint = self.ui_font.render("Press R to Retry | ESC to Menu", True, UI_COLOR)
        
        self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
        self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 50))

    # --- ИГРОВАЯ ЛОГИКА ---
    def update_game(self):
        current_time = pygame.time.get_ticks()

        # Движение
        head = (self.snake.body[0][0] + self.snake.direction[0], 
                self.snake.body[0][1] + self.snake.direction[1])
        
        # Проверка смерти
        is_ghost = (self.active_powerup == 2)
        hit_wall = head in self.walls
        out_of_bounds = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        hit_self = head in self.snake.body

        if (out_of_bounds or hit_self or (hit_wall and not is_ghost)):
            self.game_over()
            return

        # Взаимодействие с едой и ядом
        grow = 0
        eaten_food = (head == self.food)
        eaten_poison = (self.poison and head == self.poison)
        eaten_powerup = (self.powerup and head == self.powerup)

        if eaten_food:
            points = 2 if self.active_powerup == 3 else 1
            self.score += points
            grow = 1
            self.food = self._spawn_item()
            self.food_spawn_time = current_time
            if random.random() < 0.3: # 30% шанс заспавнить яд
                self.poison = self._spawn_item()

        elif eaten_poison:
            grow = -1 # Уменьшает длину
            self.poison = None

        elif eaten_powerup:
            self.active_powerup = self.powerup_type
            self.powerup_timer = current_time
            self.powerup = None

        self.snake.move(grow=grow)

        # Смерть от яда (если длина меньше 3)
        if len(self.snake.body) < 3:
            self.game_over()
            return

        # Проверка таймеров
        if current_time - self.food_spawn_time > FOOD_LIFETIME:
            self.food = self._spawn_item()
            self.food_spawn_time = current_time

        if not self.powerup and random.random() < 0.01: # Шанс спавна поверапа
            self.powerup = self._spawn_item()
            self.powerup_type = random.choice([1, 2, 3])
            self.powerup_spawn_time = current_time

        if self.powerup and current_time - self.powerup_spawn_time > POWERUP_LIFETIME:
            self.powerup = None

        if self.active_powerup and current_time - self.powerup_timer > POWERUP_DURATION:
            self.active_powerup = None

        # Уровни
        new_level = (self.score // FOOD_LIMIT) + 1
        if new_level > self.level:
            self.level = new_level
            self._generate_level_walls()

        # Применение активных бонусов к скорости
        current_speed = INITIAL_SPEED + (self.level - 1) * 2
        if self.active_powerup == 1:
            current_speed += 5 # Ускорение
        self.speed = current_speed

    def draw_game(self):
        self.screen.fill(BG_COLOR)
        
        # Отрисовка
        for w in self.walls: self.draw_node(w, WALL_COLOR)
        self.draw_node(self.food, FOOD_COLOR, is_food=True)
        if self.poison: self.draw_node(self.poison, POISON_COLOR, is_food=True)
        if self.powerup: self.draw_node(self.powerup, POWERUP_COLOR, is_food=True)

        for i, part in enumerate(self.snake.body):
            color = self.snake.color_head if i == 0 else self.snake.color_body
            if self.active_powerup == 2: # Ghost effect
                color = (255, 255, 255)
            self.draw_node(part, color)

        # UI
        score_img = self.ui_font.render(f"SCORE: {self.score} (PB: {self.personal_best})", True, TEXT_COLOR)
        level_img = self.ui_font.render(f"LEVEL: {self.level}", True, UI_COLOR)
        self.screen.blit(score_img, (15, 10))
        self.screen.blit(level_img, (15, 30))
        
        if self.active_powerup:
            names = {1: "SPEED BOOST", 2: "GHOST", 3: "DOUBLE SCORE"}
            pw_img = self.ui_font.render(names[self.active_powerup], True, POWERUP_COLOR)
            self.screen.blit(pw_img, (WIDTH - 150, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_RETURN and len(self.username) > 0:
                            self.personal_best = db.get_personal_best(self.username)
                            self.reset_game()
                            self.state = "GAME"
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif event.key == pygame.K_l:
                            self.top_players = db.get_top_10()
                            self.state = "LEADERBOARD"
                        elif event.key == pygame.K_s:
                            self.state = "SETTINGS"
                        elif event.unicode.isalnum() and len(self.username) < 15:
                            self.username += event.unicode

                    elif self.state == "GAME":
                        self.snake.change_dir(event.key)
                    
                    elif self.state == "GAME_OVER":
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.state = "GAME"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "MENU"

                    elif self.state == "LEADERBOARD":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                            
                    elif self.state == "SETTINGS":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                        elif event.key == pygame.K_1:
                            self.settings["grid"] = not self.settings["grid"]
                            self.save_settings()
                        elif event.key == pygame.K_2:
                            self.settings["sound"] = not self.settings["sound"]
                            self.save_settings()
                            self.update_music()
                        elif event.key == pygame.K_3:
                            colors = ["Green", "Pink", "Orange"]
                            idx = colors.index(self.settings["snake_color"])
                            self.settings["snake_color"] = colors[(idx + 1) % len(colors)]
                            self.save_settings()

            # Отрисовка в зависимости от состояния
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME":
                self.update_game()
                if self.state == "GAME": # Если не умерли в update_game
                    self.draw_game()
            elif self.state == "GAME_OVER":
                self.draw_game_over()
            elif self.state == "LEADERBOARD":
                self.draw_leaderboard()
            elif self.state == "SETTINGS":
                self.draw_settings()

            pygame.display.flip()
            # Скорость обновления зависит от экрана
            self.clock.tick(self.speed if self.state == "GAME" else 30)

if __name__ == "__main__":
    game = GameEngine()
    game.run()