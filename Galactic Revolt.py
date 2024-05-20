import pygame
import time
import random

pygame.font.init()
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galactic Revolt")

# Load background images
GAME_BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load("Menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player image and get its dimensions
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("player_ship.png"), (250, 100))  # Adjusted player ship size
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

# Define buttons
class Button:
    
    # Button attributes
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color

    # Customize buttons
    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != "":
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    # Change button color if mouse is hovering
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# Main menu
def menu():
    Screen.blit(MENU_BG, (0,0))

    start_button = Button(400, 400, 400, 100, "Start", (0, 255, 0), (0, 200, 0))
    options_button = Button(400, 550, 400, 100, "Options", (0, 0, 255), (0, 0, 200))
    quit_button = Button(400, 700, 400, 100, "Quit", (255, 0, 0), (200, 0, 0))

    font = pygame.font.SysFont("comicsans", 50)
    message = font.render("Welcome to Galactic Revolt", True, (255, 255, 255))
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, 100))
    Screen.blit(message, message_rect)

    buttons = [start_button, options_button, quit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        button.color = button.hover_color
                    else:
                        button.color = (0, 255, 0) if button.text == "Start" else (255, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.text == "Start":
                            return
                        elif button.text == "Quit":
                            pygame.quit()
                            quit()

        for button in buttons:
            button.draw(Screen, (0, 0, 0))

        pygame.display.update()

# Place player, bullers, and timer on screen
def draw(player, bullets, elapsed_time):
    Screen.blit(GAME_BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    Screen.blit(time_text, (10, 10))
    
    Screen.blit(PLAYER_IMAGE, (player.x, player.y))
    
    for bullet in bullets:
        pygame.draw.circle(Screen, BULLET_COLOR, (bullet[0], bullet[1]), BULLET_RADIUS)
    
    pygame.display.update()

# Create bullets
def handle_bullets(bullets):
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets.remove(bullet)


def main():
    menu()
    
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
