import pygame
import random
import sys

# CONFIG
CELL_SIZE = 20
COLS = 30
ROWS = 20

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Цветовая палитра (Cyberpunk Neon)
BG_COLOR = (15, 15, 25)
SNAKE_HEAD_COLOR = (0, 255, 150)
SNAKE_BODY_COLOR = (0, 100, 80)
FOOD_COLOR = (255, 0, 110)
DOUBLE_POINT_FOOD_COLOR = (255, 215, 0)
WALL_COLOR = (180, 180, 180)
TEXT_COLOR = (255, 255, 255)
UI_COLOR = (0, 180, 255)

INITIAL_SPEED = 7
FOOD_LIMIT = 4 # Через сколько съеденных яблок повышается уровень


FOOD_LIFETIME = 20000
GOLD_FOOD_LIFETIME = 10000


class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

    def change_dir(self, key):
        """Меняем направление, не позволяя змейке 'сломать шею' об себя."""
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
        else:
            for _ in range(grow - 1):
                self.body.append(self.body[-1])

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Snake")
        self.clock = pygame.time.Clock()
        self.main_font = pygame.font.SysFont("Verdana", 28, bold=True)
        self.ui_font = pygame.font.SysFont("Consolas", 18)
        self.reset()

    def reset(self):
        """Полный сброс параметров игры."""
        self.snake = Snake()
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.walls = self._create_walls()
        self.food = self._spawn_food()
        self.gold_food = None
        self.food_spawn_time = pygame.time.get_ticks()
        self.gold_food_spawn_time = pygame.time.get_ticks()

    def _create_walls(self):
        """Создаем препятствия на карте."""
        w = set()
        # Горизонтальная стена сверху
        for x in range(5, 15): w.add((x, 6))
        # Вертикальная стена снизу
        for y in range(12, 17): w.add((20, y))
        return w

    def _spawn_food(self):
        """Ищем свободную клетку для еды, чтобы не попасть в стену или хвост."""
        while True:
            pos = (random.randint(2, COLS - 3), random.randint(2, ROWS - 3))
            if pos not in self.snake.body and pos not in self.walls:
                return pos

    def draw_node(self, pos, color, is_food=False):
        """Рисуем квадратный блок с отступом для сеточного эффекта."""
        gap = 2
        rect = pygame.Rect(
            pos[0] * CELL_SIZE + gap, 
            pos[1] * CELL_SIZE + gap,
            CELL_SIZE - gap * 2, 
            CELL_SIZE - gap * 2
        )
        if is_food:
            pygame.draw.ellipse(self.screen, color, rect) # Еда будет круглой
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=5)

    def game_over_screen(self):
        """Финальный экран при проигрыше."""
        self.screen.fill(BG_COLOR)
        msg = self.main_font.render("WASTED", True, FOOD_COLOR)
        stats = self.ui_font.render(f"Score: {self.score} | Level: {self.level}", True, TEXT_COLOR)
        hint = self.ui_font.render("Press R to Respawn or Q to Quit", True, UI_COLOR)
        
        self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
        self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: return
                    if event.key == pygame.K_q: pygame.quit(); sys.exit()

    def run(self):
        """Главный цикл управления."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.snake.change_dir(event.key)



            # Рассчитываем будущую позицию головы
            head = (self.snake.body[0][0] + self.snake.direction[0], 
                    self.snake.body[0][1] + self.snake.direction[1])
            
            # Проверка поедания
            eaten = head == self.food
            eaten_gold = (self.gold_food is not None and head == self.gold_food)

            # Проверка смерти (стены поля, свои стены, хвост)
            if (not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or 
                head in self.snake.body or 
                head in self.walls):
                self.game_over_screen()
                self.reset()
                continue

            grow = 1 if eaten else(2 if eaten_gold else 0)
            self.snake.move(grow=grow)

            current_time = pygame.time.get_ticks()
            if current_time - self.food_spawn_time > FOOD_LIFETIME:
                self.food = self._spawn_food()
                self.food_spawn_time = current_time

            if self.gold_food and (current_time - self.gold_food_spawn_time > GOLD_FOOD_LIFETIME):
                self.gold_food = None
            
            
            

            if eaten:
                self.score += 1
                self.food = self._spawn_food()
                self.food_spawn_time = current_time

                if self.gold_food is None and random.random() < 0.2:
                    self.gold_food = self._spawn_food()
                    self.gold_food_spawn_time = current_time
            
            elif eaten_gold:
                self.score += 4
                self.gold_food = None
            
            new_level = (self.score // FOOD_LIMIT) + 1
            if new_level > self.level:
                self.level = new_level
                self.speed = INITIAL_SPEED + (self.level - 1) * 2

            # Визуализация
            self.screen.fill(BG_COLOR)
            
            # Стены
            for w in self.walls: self.draw_node(w, WALL_COLOR)
            
            # Еда
            time_left = (FOOD_LIFETIME - (current_time - self.food_spawn_time)) // 1000

            self.draw_node(self.food, FOOD_COLOR, is_food=True)
            # таймер над яблоком
            timer_text = self.ui_font.render(str(max(0, time_left)), True, TEXT_COLOR)
            x = self.food[0] * CELL_SIZE + CELL_SIZE // 2 - timer_text.get_width() // 2
            y = self.food[1] * CELL_SIZE - 15
            self.screen.blit(timer_text, (x, y))
            
            if self.gold_food:
                time_left_gold = (GOLD_FOOD_LIFETIME - (current_time - self.gold_food_spawn_time)) // 1000

                self.draw_node(self.gold_food, DOUBLE_POINT_FOOD_COLOR, is_food=True)
                # таймер над золотым яблоком
                timer_text = self.ui_font.render(str(max(0, time_left_gold)), True, TEXT_COLOR)
                x = self.gold_food[0] * CELL_SIZE + CELL_SIZE // 2 - timer_text.get_width() // 2
                y = self.gold_food[1] * CELL_SIZE - 15
                self.screen.blit(timer_text, (x, y))
                
            
            # Змейка
            for i, part in enumerate(self.snake.body):
                color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
                self.draw_node(part, color)

            # Статистика в углу
            score_img = self.ui_font.render(f"SCORE: {self.score}", True, TEXT_COLOR)
            level_img = self.ui_font.render(f"LEVEL: {self.level}", True, UI_COLOR)
            self.screen.blit(score_img, (15, 10))
            self.screen.blit(level_img, (15, 30))

            pygame.display.flip()
            self.clock.tick(self.speed)

if __name__ == "__main__":
    game = GameEngine()
    game.run()