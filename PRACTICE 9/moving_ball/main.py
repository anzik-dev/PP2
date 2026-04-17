import pygame

pygame.init()

screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

x = 250
y = 250
radius = 25
step = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            
            if event.key == pygame.K_UP:
                if y - step >= radius:
                    y -= radius

            
            elif event.key == pygame.K_DOWN:
                if y + step <= 500 - radius:
                    y += step

            
            elif event.key == pygame.K_RIGHT:
                if x + step <= 500 - radius:
                    x += step

            
            elif event.key == pygame.K_LEFT:
                if x - step >= radius:
                    x -= step

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

