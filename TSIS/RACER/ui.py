import pygame
from persistence import load_data, save_data

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

def draw_text(surface, text, font, color, x, y, center=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center: text_rect.center = (x, y)
    else: text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_main_menu(surface, font_big, font_small):
    surface.fill(WHITE)
    draw_text(surface, "RACER 2026", font_big, BLACK, 200, 150)
    play_rect = pygame.Rect(100, 250, 200, 50)
    sett_rect = pygame.Rect(100, 320, 200, 50)
    lead_rect = pygame.Rect(100, 390, 200, 50)
    pygame.draw.rect(surface, GREEN, play_rect)
    pygame.draw.rect(surface, GRAY, sett_rect)
    pygame.draw.rect(surface, BLUE, lead_rect)
    draw_text(surface, "START GAME", font_small, WHITE, 200, 275)
    draw_text(surface, "SETTINGS", font_small, WHITE, 200, 345)
    draw_text(surface, "LEADERBOARD", font_small, WHITE, 200, 415)
    return play_rect, sett_rect, lead_rect

# В ui.py
def draw_settings_screen(surface, font_small, settings): # Добавь settings в аргументы
    surface.fill(WHITE)
    
    draw_text(surface, "SETTINGS", font_small, BLACK, 200, 50)

    # Кнопка звука - берет значение из переданного словаря
    sound_status = "ON" if settings["sound"] else "OFF"
    sound_rect = pygame.Rect(100, 150, 200, 50)
    pygame.draw.rect(surface, BLACK, sound_rect)
    draw_text(surface, f"SOUND: {sound_status}", font_small, WHITE, 200, 175)

    # Кнопка цвета
    color_rect = pygame.Rect(100, 250, 200, 50)
    pygame.draw.rect(surface, BLUE, color_rect)
    draw_text(surface, f"CAR: {settings['color_of_car']}", font_small, WHITE, 200, 275)

    # Кнопка сложности
    diff_rect = pygame.Rect(100, 350, 200, 50)
    pygame.draw.rect(surface, (100, 0, 100), diff_rect)
    draw_text(surface, f"DIFF: {settings['difficulty']}", font_small, WHITE, 200, 375)

    # Кнопка возврата
    back_rect = pygame.Rect(100, 500, 200, 50)
    pygame.draw.rect(surface, RED, back_rect)
    draw_text(surface, "SAVE & BACK", font_small, WHITE, 200, 525)

    return sound_rect, color_rect, diff_rect, back_rect

def draw_leaderboard_screen(surface, font_small):
    surface.fill(WHITE)
    draw_text(surface, "TOP 10 PLAYERS", font_small, BLACK, 200, 50)
    scores = load_data("leaderboard.json", [])
    for i, entry in enumerate(scores):
        y_pos = 100 + (i * 35)
        draw_text(surface, f"{i+1}. {entry['name']} : {entry['score']}", font_small, BLACK, 50, y_pos, center=False)
    back_rect = pygame.Rect(100, 520, 200, 40)
    pygame.draw.rect(surface, RED, back_rect)
    draw_text(surface, "BACK", font_small, WHITE, 200, 540)
    return back_rect

def draw_game_over_screen(surface, font_big, font_small, score):
    surface.fill(RED)
    draw_text(surface, "GAME OVER", font_big, WHITE, 200, 200)
    draw_text(surface, f"COINS: {score}", font_small, WHITE, 200, 300)
    draw_text(surface, "Click to Menu", font_small, WHITE, 200, 450)