import pygame
import time
import random

pygame.font.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galactic Revolt")

# Ensure the image path is correct
BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_XMOV = 5
PLAYER_YMOV = 5

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time):
    Screen.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    Screen.blit(time_text, (10, 10))
    
    pygame.draw.rect(Screen, "red", player)
    
    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(500, SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()  
    start_time = time.time()
    elapsed_time = 0
    
    while run:
        clock.tick(80)
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_XMOV >= 0:
            player.x -= PLAYER_XMOV
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_XMOV + player.width <= SCREEN_WIDTH:
            player.x += PLAYER_XMOV
        elif keys[pygame.K_UP] and player.y - PLAYER_YMOV >= 0:
            player.y -= PLAYER_YMOV
        elif keys[pygame.K_DOWN] and player.y + PLAYER_YMOV + player.height <= SCREEN_HEIGHT:
            player.y += PLAYER_YMOV
            
        draw(player, elapsed_time)
            
    pygame.quit()
    
if __name__ == "__main__":
    main()
