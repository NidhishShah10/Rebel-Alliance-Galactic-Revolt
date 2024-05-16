import pygame
import time
import random

# Initialize pygame
pygame.font.init()
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galactic Revolt")

# Load background image
BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player image and get its dimensions
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("player_ship.png"), (400, 250))  # Adjusted player ship size
PLAYER_WIDTH = PLAYER_IMAGE.get_width()
PLAYER_HEIGHT = PLAYER_IMAGE.get_height()

# Player speed
PLAYER_SPEED = 20  

# Bullet color and speed
BULLET_COLOR = (255, 255, 255)  # White color
BULLET_RADIUS = 5
BULLET_SPEED = 20

# Font settings
FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, bullets, elapsed_time):
    Screen.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    Screen.blit(time_text, (10, 10))
    
    Screen.blit(PLAYER_IMAGE, (player.x, player.y))
    
    for bullet in bullets:
        pygame.draw.circle(Screen, BULLET_COLOR, (bullet[0], bullet[1]), BULLET_RADIUS)
    
    pygame.display.update()

def handle_bullets(bullets):
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets.remove(bullet)

def main():
    run = True
    
    player = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)  # Start at center bottom
    bullets = []
    
    clock = pygame.time.Clock()  
    start_time = time.time()
    elapsed_time = 0
    
    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = [player.x + player.width // 2, player.y]
                    bullets.append(bullet)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_SPEED >= 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x + PLAYER_SPEED + player.width <= SCREEN_WIDTH:
            player.x += PLAYER_SPEED
        if keys[pygame.K_UP] and player.y - PLAYER_SPEED >= 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.y + PLAYER_SPEED + player.height <= SCREEN_HEIGHT:
            player.y += PLAYER_SPEED
            
        handle_bullets(bullets)
        draw(player, bullets, elapsed_time)
            
    pygame.quit()
    
if __name__ == "__main__":
    main()
