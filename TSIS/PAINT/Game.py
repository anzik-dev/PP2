import pygame
import sys
import datetime

# НАСТРОЙКИ
WIDTH, HEIGHT = 800, 600
FPS = 60

# Основные цвета
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED   = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE  = (0, 0, 255)

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PyPaint: Tools & Shapes")
        self.clock = pygame.time.Clock()
        
        # Холст, чтобы рисунок не стирался при обновлении экрана
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.canvas.fill(COLOR_BLACK)
        
        # Начальные настройки инструментов
        self.tool = 'pen'
        self.color = COLOR_WHITE
        self.sizes = [2, 5, 10]
        self.size_index = 1
        self.radius = self.sizes[self.size_index]
        
        # Переменные для логики рисования
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        
        # Настройки для текста
        self.text_active = False
        self.text_pos = None
        self.text_input = ""
        self.font = pygame.font.SysFont("Arial", 24)

    def run(self):
        # Главный цикл программы
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # ОБРАБОТКА КЛАВИАТУРЫ
            if event.type == pygame.KEYDOWN:
                # Если печатаем текст, то кнопки работают только для ввода
                if self.text_active:
                    if event.key == pygame.K_RETURN:
                        # Сохраняем текст на холст
                        text_surface = self.font.render(self.text_input, True, self.color)
                        self.canvas.blit(text_surface, self.text_pos)
                        self.text_active = False
                        self.text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        self.text_active = False
                        self.text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    else:
                        self.text_input += event.unicode
                    return

                # Переключение размера кисти (кнопки 1, 2, 3)
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    self.size_index = int(event.unicode) - 1
                    self.radius = self.sizes[self.size_index]

                # Выбор цвета (R, G, B, W)
                if event.key == pygame.K_r: self.color = COLOR_RED
                elif event.key == pygame.K_g: self.color = COLOR_GREEN
                elif event.key == pygame.K_b: self.color = COLOR_BLUE
                elif event.key == pygame.K_w: self.color = COLOR_WHITE
                
                # Выбор инструмента (4-9, 0)
                elif event.key == pygame.K_4: self.tool = 'pen'
                elif event.key == pygame.K_5: self.tool = 'square'
                elif event.key == pygame.K_6: self.tool = 'right_triangle'
                elif event.key == pygame.K_7: self.tool = 'equilateral_triangle'
                elif event.key == pygame.K_8: self.tool = 'rhombus'
                elif event.key == pygame.K_9: self.tool = 'line'
                elif event.key == pygame.K_0: self.tool = 'eraser'
                
                # Доп. функции: очистка, заливка, текст
                elif event.key == pygame.K_c: self.canvas.fill(COLOR_BLACK)
                elif event.key == pygame.K_f: self.tool = 'fill'
                elif event.key == pygame.K_t: self.tool = 'text'

                # Сохранение (Ctrl + S)
                elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.save_canvas()

            # ОБРАБОТКА МЫШКИ
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # ЛКМ нажата
                    self.drawing = True
                    self.start_pos = event.pos
                    self.last_pos = event.pos

                    # Заливка срабатывает сразу при клике
                    if self.tool == 'fill':
                        self.flood_fill(event.pos, self.color)
                    
                    # Режим ввода текста
                    if self.tool == 'text':
                        self.text_active = True
                        self.text_pos = event.pos
                        self.text_input = ""
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # ЛКМ отпущена
                    # Рисуем линию
                    if self.tool == 'line':
                        pygame.draw.line(self.canvas, self.color, self.start_pos, event.pos, self.radius)
                    
                    # Рисуем фигуры (один раз при отпускании)
                    if self.tool in ['square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        self.draw_shape(self.canvas, self.start_pos, event.pos)
                    
                    self.drawing = False
                    self.start_pos = None
                    self.last_pos = None

            # Рисование в реальном времени (перо и ластик)
            if event.type == pygame.MOUSEMOTION and self.drawing:
                if self.tool == 'pen':
                    pygame.draw.line(self.canvas, self.color, self.last_pos, event.pos, self.radius)
                    self.last_pos = event.pos
                elif self.tool == 'eraser':
                    pygame.draw.circle(self.canvas, COLOR_BLACK, event.pos, self.radius)

    def draw_shape(self, surface, start, end):
        # Математика для отрисовки разных фигур
        x1, y1 = start
        x2, y2 = end

        if self.tool == 'square':
            size = min(abs(x2 - x1), abs(y2 - y1))
            rect = pygame.Rect(x1, y1, size, size)
            rect.normalize()
            pygame.draw.rect(surface, self.color, rect, self.radius // 2 + 1)

        elif self.tool == 'right_triangle':
            points = [(x1, y1), (x2, y1), (x1, y2)]
            pygame.draw.polygon(surface, self.color, points, self.radius // 2 + 1)

        elif self.tool == 'equilateral_triangle':
            base = abs(x2 - x1)
            height = int(base * 0.866) # Корень из 3 на 2
            points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
            pygame.draw.polygon(surface, self.color, points, self.radius // 2 + 1)

        elif self.tool == 'rhombus':
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
            pygame.draw.polygon(surface, self.color, points, self.radius // 2 + 1)

    def draw(self):
        # Сначала рисуем то, что уже на холсте
        self.screen.blit(self.canvas, (0, 0))
        
        # Превью линии, пока тянем мышку
        if self.drawing and self.tool == 'line' and self.start_pos:
            pygame.draw.line(self.screen, self.color, self.start_pos, pygame.mouse.get_pos(), self.radius)
        
        # Превью фигур, пока тянем мышку
        if self.drawing and self.tool in ['square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
            self.draw_shape(self.screen, self.start_pos, pygame.mouse.get_pos())

        # Отображение текста в процессе ввода
        if self.text_active:
            text_surface = self.font.render(self.text_input, True, self.color)
            self.screen.blit(text_surface, self.text_pos)
                    
        # Рисуем кружок-курсор
        cursor_color = self.color if self.tool != 'eraser' else COLOR_WHITE
        pygame.draw.circle(self.screen, cursor_color, pygame.mouse.get_pos(), self.radius, 1)

        # Вывод интерфейса
        self.draw_ui()
        pygame.display.flip()

    def flood_fill(self, start_pos, new_color):
        # Алгоритм заливки через стек
        x, y = start_pos
        target_color = self.canvas.get_at((x, y))
        if target_color == new_color: return

        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                if self.canvas.get_at((x, y)) == target_color:
                    self.canvas.set_at((x, y), new_color)
                    stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    def save_canvas(self):
        # Сохранение скрина с датой в названии
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"paint_{now}.png"
        pygame.image.save(self.canvas, filename)
        print(f"Картинка сохранена: {filename}")

    def draw_ui(self):
        # Информация о текущем режиме сверху экрана
        font = pygame.font.SysFont("Arial", 18)
        info = f"Tool: {self.tool} | Color: {self.color} | Radius: {self.radius} | [C] Clear | [T] Text"
        text_surface = font.render(info, True, COLOR_WHITE)
        # Небольшая подложка для текста, чтобы его было видно
        pygame.draw.rect(self.screen, COLOR_BLACK, (5, 5, text_surface.get_width() + 10, 25))
        self.screen.blit(text_surface, (10, 7))

if __name__ == "__main__":
    app = PaintApp()
    app.run()