import pygame
import os

pygame.init()


screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()


playlist = [
    "PRACTICE 9/music_player/music/Eminem - Cinderella Man.mp3",
    "PRACTICE 9/music_player/music/Venom - Eminem.mp3"
]

current_track = 0
is_playing = False
is_paused = False


pygame.mixer.music.load(playlist[current_track])


def play_music():
    global is_playing, is_paused
    if is_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play()
    is_playing = True
    is_paused = False

def pause_music():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

def get_track_name():
    return os.path.basename(playlist[current_track])

def draw():
    screen.fill((30, 30, 30))

    track_text = font.render(f"Track: {get_track_name()}", True, (255, 255, 255))
    screen.blit(track_text, (20, 20))


    pos_ms = pygame.mixer.music.get_pos()
    seconds = pos_ms // 1000

    progress_text = font.render(f"Time: {seconds}s", True, (200, 200, 200))
    screen.blit(progress_text, (20, 60))

    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p: 
                if is_playing and not is_paused:
                    pause_music()
                else:
                    play_music()

            elif event.key == pygame.K_s:
                stop_music()

            elif event.key == pygame.K_n:
                next_track()

            elif event.key == pygame.K_b:
                prev_track()

            elif event.key == pygame.K_q:
                running = False

    draw()
    clock.tick(60)

pygame.quit()