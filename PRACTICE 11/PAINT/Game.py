import pygame
import sys

# -------------------- CONFIG --------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
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
        
        # Холст для рисования (чтобы фигуры оставались на экране)
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.canvas.fill(COLOR_BLACK)
        
        # Состояние редактора
        self.tool = 'pen'  # pen, rect, circle, eraser
        self.color = COLOR_WHITE
        self.radius = 10
        self.drawing = False
        self.start_pos = None

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Управление клавиатурой
            if event.type == pygame.KEYDOWN:
                # Выбор цвета
                if event.key == pygame.K_r: self.color = COLOR_RED
                elif event.key == pygame.K_g: self.color = COLOR_GREEN
                elif event.key == pygame.K_b: self.color = COLOR_BLUE
                elif event.key == pygame.K_w: self.color = COLOR_WHITE
                
                # Выбор инструмента
                elif event.key == pygame.K_1: self.tool = 'pen'
                elif event.key == pygame.K_2: self.tool = 'square'
                elif event.key == pygame.K_3: self.tool = 'right_triangle'
                elif event.key == pygame.K_4: self.tool = 'equilateral_triangle'
                elif event.key == pygame.K_5: self.tool = 'rhombus'
                elif event.key == pygame.K_6: self.tool = 'eraser'
                
                # Очистка экрана
                elif event.key == pygame.K_c: self.canvas.fill(COLOR_BLACK)

            # Изменение радиуса колесиком мыши
            if event.type == pygame.MOUSEWHEEL:
                self.radius = max(1, min(100, self.radius + event.y))

            # Логика мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # ЛКМ
                    self.drawing = True
                    self.start_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Если выбрана фигура, рисуем её один раз при отпускании кнопки
                    if self.tool in ['square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        self.draw_shape(self.canvas, self.start_pos, event.pos)
                    self.drawing = False
                    self.start_pos = None

            # Рисование кистью или ластиком в реальном времени
            if event.type == pygame.MOUSEMOTION and self.drawing:
                if self.tool == 'pen':
                    pygame.draw.circle(self.canvas, self.color, event.pos, self.radius)
                elif self.tool == 'eraser':
                    pygame.draw.circle(self.canvas, COLOR_BLACK, event.pos, self.radius)

    def draw_shape(self, surface, start, end):
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
            height = int(base * 0.866)  # √3/2
            points = [
                (x1, y2),
                (x2, y2),
                ((x1 + x2) // 2, y2 - height)
            ]
            pygame.draw.polygon(surface, self.color, points, self.radius // 2 + 1)

        elif self.tool == 'rhombus':
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            dx = abs(x2 - x1) // 2
            dy = abs(y2 - y1) // 2

            points = [
                (mid_x, y1),
                (x2, mid_y),
                (mid_x, y2),
                (x1, mid_y)
            ]
            pygame.draw.polygon(surface, self.color, points, self.radius // 2 + 1)

    def draw(self):
        # Сначала рисуем сохраненный холст
        self.screen.blit(self.canvas, (0, 0))
        
        # Если мы в процессе растягивания фигуры, рисуем превью на основном экране
        if self.drawing and self.tool in ['square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
            current_pos = pygame.mouse.get_pos()
            self.draw_shape(self.screen, self.start_pos, current_pos)
            
        # Рисуем индикатор кисти (курсор)
        cursor_color = self.color if self.tool != 'eraser' else COLOR_WHITE
        pygame.draw.circle(self.screen, cursor_color, pygame.mouse.get_pos(), self.radius, 1)

        # Вывод информации о режиме
        self.draw_ui()
        
        pygame.display.flip()

    def draw_ui(self):
        """Отрисовка текста с текущими настройками."""
        font = pygame.font.SysFont("Arial", 18)
        info = f"Tool: {self.tool} | Color: {self.color} | Radius: {self.radius} | [C] to Clear"
        text_surface = font.render(info, True, COLOR_WHITE)
        self.screen.blit(text_surface, (10, 10))

if __name__ == "__main__":
    app = PaintApp()
    app.run()