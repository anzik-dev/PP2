import pygame
from datetime import datetime
from zoneinfo import ZoneInfo

pygame.init()

screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

center = pygame.math.Vector2(512, 384)


main_image = pygame.image.load("PRACTICE 9/mickeys_clock/images/main_image.png")
left_hand_orig = pygame.image.load("PRACTICE 9/mickeys_clock/images/left_hand.png")
right_hand_orig = pygame.image.load("PRACTICE 9/mickeys_clock/images/right_hand.png")

rect_main = main_image.get_rect(center=center)


left_pivot_offset = pygame.math.Vector2(20, left_hand_orig.get_height() / 2 - 65)
right_pivot_offset = pygame.math.Vector2(-40, right_hand_orig.get_height() / 2 - 65)

def rotate_on_pivot(image, angle, pivot_offset, screen_center):
    
    
    rotated_image = pygame.transform.rotate(image, -angle)
    
    
    rotated_offset = pivot_offset.rotate(angle)
    
    
    rect = rotated_image.get_rect(center=screen_center + rotated_offset)
    
    return rotated_image, rect

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.draw.circle(screen, (255,0,0), center, 5)
    now = datetime.now(ZoneInfo("Asia/Almaty"))
    seconds = now.second
    minutes = now.minute
    
    angle_sec = seconds * 6 + 180
    angle_min = minutes * 6 + seconds * 0.1 + 180

    screen.fill((255, 255, 255))
    screen.blit(main_image, rect_main)

    
    sec_img, sec_rect = rotate_on_pivot(left_hand_orig, angle_sec, left_pivot_offset, center)
    min_img, min_rect = rotate_on_pivot(right_hand_orig, angle_min, right_pivot_offset, center)

    
    screen.blit(sec_img, sec_rect)
    screen.blit(min_img, min_rect)



    pygame.display.flip()
    clock.tick(1)

pygame.quit()