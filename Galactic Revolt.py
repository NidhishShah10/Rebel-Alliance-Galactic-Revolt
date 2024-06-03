import pygame
import time
import random

pygame.font.init()
pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1400
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Galactic Revolt")
score = 0

GAME_BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load("Menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))


PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("player_ship.png"), (250, 100))  
PLAYER_WIDTH = PLAYER_IMAGE.get_width()
PLAYER_HEIGHT = PLAYER_IMAGE.get_height()


PLAYER_SPEED = 20  


BULLET_COLOR = (255, 255, 255) 
BULLET_RADIUS = 5
BULLET_SPEED = 20


FONT = pygame.font.SysFont("comicsans", 30)


class BasicEnemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load("BasicEnemy.png"), (50, 50))  
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def create_basic_enemy():
    x = random.randint(0, SCREEN_WIDTH - 50)
    y = -50
    speed = random.randint(1, 2)
    return BasicEnemy(x, y, speed)

enemies = []


class Button:
    
  
    def __init__(self, x, y, width, height, text, color, hover_color, original_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.original_color = original_color

    
    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != "":
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = self.hover_color  
                return True
        self.color = self.original_color  
        return False


def menu():
    Screen.blit(MENU_BG, (0,0))

    start_button = Button(600, 400, 400, 100, "Start", (0, 255, 0), (0, 200, 0), (0, 255, 0))
    settings_button = Button(600, 550, 400, 100, "Settings", (0, 0, 255), (0, 0, 200), (0, 0, 255))
    quit_button = Button(600, 700, 400, 100, "Quit", (255, 0, 0), (200, 0, 0), (255, 0, 0))

    font = pygame.font.SysFont("comicsans", 50)
    message = font.render("Welcome to Galactic Revolt", True, (255, 255, 255))
    message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
    Screen.blit(message, message_rect)

    buttons = [start_button, settings_button, quit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.is_over(pygame.mouse.get_pos())
                    button.color = button.hover_color
                    settings_button = (0, 0, 200)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.text == "Start":
                            return
                        if button.text == "Settings":
                            settings_menu()
                            print("Settings button clicked")
                        elif button.text == "Quit":
                            pygame.quit()
                            quit()

        for button in buttons:
            button.draw(Screen, (0, 0, 0))

        pygame.display.update()

class GameMode:
    def __init__(self, name, spawn_rate):
        self.name = name 
        self.spawn_rate = spawn_rate

# Defining game modes
easy_mode = GameMode("Easy", 120)
medium_mode = GameMode("Medium", 80)
hard_mode = GameMode("Hard", 40)
game_modes = [easy_mode, medium_mode, hard_mode]
selected_mode = easy_mode

def settings_menu():
    Screen.fill((0, 0, 0))
    back_button = Button(50, 50, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))

    mode_buttons = []
    for i, mode in enumerate(game_modes):
        if mode.name == "Easy":
            color = (0, 255, 0)
            hover_color = (0, 200, 0)
        elif mode.name == "Medium":
            color = (255, 255, 0)
            hover_color = (200, 200, 0)
        elif mode.name == "Hard":
            color = (255, 0, 0)
            hover_color = (200, 0, 0)
        
        button = Button(600, 300 + i * 100, 400, 80, mode.name, color, hover_color, color)
        mode_buttons.append(button)

    while True:
        Screen.fill((0, 0, 0))  # Clear the screen before drawing buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEMOTION:
                back_button.is_over(pygame.mouse.get_pos())
                for button in mode_buttons:
                    button.is_over(pygame.mouse.get_pos())
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in mode_buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                            global selected_mode
                            selected_mode = next(mode for mode in game_modes if mode.name == button.text)
                if back_button.is_over(pygame.mouse.get_pos()):  # Handle back button click
                    menu()  # Go back to main menu
                    return
                
            back_button.draw(Screen, (0, 0, 0))
            for button in mode_buttons:
                button.draw(Screen, (0, 0, 0))

            pygame.display.update()

def draw(player, bullets, elapsed_time):
    Screen.blit(GAME_BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    Screen.blit(time_text, (10, 10))
    
    Screen.blit(PLAYER_IMAGE, (player.x, player.y))
    
    for bullet in bullets:
        pygame.draw.circle(Screen, BULLET_COLOR, (bullet[0], bullet[1]), BULLET_RADIUS)
        
def draw_score():
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    Screen.blit(score_text, (10, 40))

# Create bullets
def handle_bullets(bullets):
    global score
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            
            for enemy in enemies[:]:
                if pygame.Rect(bullet[0], bullet[1], BULLET_RADIUS, BULLET_RADIUS).colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

# Displays message to player that they have been hit                
def player_hit_message(message, duration):
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render(message, True, (255,255,255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    Screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(duration * 1000)
    
def reset_game():
    global enemies
    player_hit_message("You have been hit!", 1)
    enemies = []
    

def main():
    menu()
    
    run = True
    
    player = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 275, PLAYER_WIDTH, PLAYER_HEIGHT)  # Start at center bottom
    bullets = []
    global score
    global lives
    global enemies
    lives = 3
    clock = pygame.time.Clock()  
    start_time = time.time()
    elapsed_time = 0
    time_since_last_basic_spawn = 0

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        
        interval_for_enemy_spawn = 50

        if elapsed_time - time_since_last_basic_spawn > 10:
            interval_for_enemy_spawn = max(10, interval_for_enemy_spawn - 10)

        
        if random.randint(1, selected_mode.spawn_rate) == 1:
            enemies.append(create_basic_enemy())
            time_since_last_basic_spawn = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = [player.x + player.width // 2, player.y]
                    bullets.append(bullet)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
            if player.x < -PLAYER_WIDTH:  
                player.x = SCREEN_WIDTH  
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
            if player.x > SCREEN_WIDTH:  
                player.x = -PLAYER_WIDTH  
        if keys[pygame.K_UP] and player.y - PLAYER_SPEED >= 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player.y + PLAYER_SPEED + player.height <= SCREEN_HEIGHT:
            player.y += PLAYER_SPEED
            
        handle_bullets(bullets)
        draw(player, bullets, elapsed_time)
        draw_score()
        # Check if player died
        for enemy in enemies:
            enemy.move()
            enemy.draw(Screen)
            if player.colliderect(enemy.rect):
                reset_game()
                player = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 275, PLAYER_WIDTH, PLAYER_HEIGHT)  # Start at center bottom
                lives -= 1
                if lives == 0:
                    menu()
                    lives = 3
                    score = 0
                    enemies.clear()
                    bullets.clear()
                    start_time = time.time()

       
        for enemy in enemies:
            enemy.move()
            enemy.draw(Screen)
        # Display lives
        lives_text = FONT.render(f"Lives: {lives}", True, (255, 255, 255))
        Screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))
        pygame.display.update()  
    pygame.quit()
    
if __name__ == "__main__":
    main()
