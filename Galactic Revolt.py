import pygame
import time
import random
import sys

pygame.font.init()
pygame.init()

# Default screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), (pygame.SRCALPHA))
pygame.display.set_caption("Galactic Revolt")
score = 0

# Load images and transform according to initial screen size
GAME_BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
MENU_BG = pygame.transform.scale(pygame.image.load("Menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
SETTINGS_BG = pygame.transform.scale(pygame.image.load("Settings_background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("player_ship.png"), (40, 40))
PLAYER_WIDTH = PLAYER_IMAGE.get_width()
PLAYER_HEIGHT = PLAYER_IMAGE.get_height()

PLAYER_SPEED = 10
BULLET_COLOR = (255, 255, 255)
BULLET_RADIUS = 5
BULLET_SPEED = 10

FONT = pygame.font.SysFont("comicsans", 20)
LARGE_FONT = pygame.font.SysFont("comicsans", 72)

class BasicEnemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load("BasicEnemy.png"), (25, 25))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def create_basic_enemy():
    x = random.randint(0, SCREEN_WIDTH - 25)
    y = -25
    speed = random.randint(1, 2)
    return BasicEnemy(x, y, speed)

snake_enemy_img = pygame.image.load('fighter.png')
class SnakeEnemy:
    def __init__(self, x, y, speed, cooldown=50):
        self.x = x
        self.y = y
        self.speed = speed
        self.original_image = pygame.transform.scale(snake_enemy_img, (50, 50))
        self.image = self.original_image.copy()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 1 
        self.cooldown = cooldown
        self.cooldown_timer = self.cooldown

    def move(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        self.x += self.speed * self.direction
        if (self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0) and self.cooldown_timer == 0:
            self.direction *= -1
            self.y += self.height
            self.cooldown_timer = self.cooldown

        if self.direction == 1:
            self.image = pygame.transform.rotate(self.original_image, 0)
        else:
            self.image = pygame.transform.rotate(self.original_image, 180)

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def create_snake_enemy(_x : int):
    x = _x
    y = 0
    speed = 2
    return SnakeEnemy(x, y, speed)

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
            font = pygame.font.SysFont("comicsans", 20)
            text = font.render(self.text, 1, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = self.hover_color
                return True
        self.color = self.original_color
        return False
    
def draw_game():
    global enemies
    Screen.blit(GAME_BG, (0, 0))
 
    for enemy in enemies:
        enemy.draw(Screen)
        
    # Display score
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    
    Screen.blit(score_text, (10, 10))
    
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        Screen.blit(GAME_BG, (0, 0))  # Redraw game background
        draw_game()  # Draw the game elements
        countdown_text = LARGE_FONT.render(str(i), True, (255, 255, 255))
        text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        Screen.blit(countdown_text, text_rect)
        pygame.display.update()
        time.sleep(1)

def pause_menu():
    resume_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 87, 200, 50, "Resume", (0, 255, 0), (0, 200, 0), (0, 255, 0))
    restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "Restart", (255, 255, 0), (200, 200, 0), (255, 255, 0))
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 37, 200, 50, "Quit", (255, 0, 0), (200, 0, 0), (255, 0, 0))
    buttons = [resume_button, restart_button, quit_button]
    pause = True

    while pause:
        draw_game() 

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        Screen.blit(overlay, (0, 0))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_button.is_over(pos):
                    pause = False
                    countdown_timer(3)
                    return 'resume'
                elif restart_button.is_over(pos):
                    return 'restart'
                elif quit_button.is_over(pos):
                    return 'quit'

        for button in buttons:
            button.draw(Screen, (0, 0, 0))

        pygame.display.update()



        
def settings_menu():
    global Screen, SETTINGS_BG

    Screen.blit(SETTINGS_BG, (0, 0))  # Use SETTINGS_BG as the background

    back_button = Button(50, 50, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))
    #screen_size_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 125, 300, 60, "Change Screen Size", (0, 255, 255), (0, 200, 200), (0, 255, 255))
    game_controls_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 125, 300, 60, "Game Controls", (0, 255, 255), (0, 200, 200), (0, 255, 255))
    credits_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 60, "Credits", (0, 255, 255), (0, 200, 200), (0, 255, 255))
    about_button = Button(SCREEN_WIDTH // 2 -150, SCREEN_HEIGHT // 2 + 25, 300, 60, "About", (0, 255, 255), (0, 200, 200), (0, 255, 255))

    while True:
        Screen.blit(SETTINGS_BG, (0, 0))  # Refresh the background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                back_button.is_over(pygame.mouse.get_pos())
                #screen_size_button.is_over(pygame.mouse.get_pos())
                game_controls_button.is_over(pygame.mouse.get_pos())
                credits_button.is_over(pygame.mouse.get_pos())
                about_button.is_over(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:
                #if screen_size_button.is_over(pygame.mouse.get_pos()):
                #    screen_size_submenu()
                #    return
                if game_controls_button.is_over(pygame.mouse.get_pos()):
                    game_controls_submenu()
                    return
                elif credits_button.is_over(pygame.mouse.get_pos()):
                    credits_submenu()
                    return
                elif about_button.is_over(pygame.mouse.get_pos()):
                    about_submenu()
                    return
                elif back_button.is_over(pygame.mouse.get_pos()):
                    menu()
                    return

        back_button.draw(Screen, (0, 0, 0))
        #screen_size_button.draw(Screen, (0, 0, 0))
        game_controls_button.draw(Screen, (0, 0, 0))
        credits_button.draw(Screen, (0, 0, 0))
        about_button.draw(Screen, (0, 0, 0))

        pygame.display.update()
        
def screen_size_submenu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, Screen, GAME_BG, MENU_BG, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, SETTINGS_BG

    Screen.blit(SETTINGS_BG, (0,0))

    # Screen size buttons
    screen_size_buttons = [
        Button(SCREEN_WIDTH // 2 - 100, 275, 200, 50, "800x600", (0, 255, 255), (0, 200, 200), (0, 255, 255)),
        Button(SCREEN_WIDTH // 2 - 100, 350, 200, 50, "1024x768", (0, 255, 255), (0, 200, 200), (0, 255, 255)),
        Button(SCREEN_WIDTH // 2 - 100, 425, 200, 50, "1280x720", (0, 255, 255), (0, 200, 200), (0, 255, 255)),
        Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "1920x1080", (0, 255, 255), (0, 200, 200), (0, 255, 255)),
        Button(SCREEN_WIDTH // 2 - 100, 575, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))
    ]

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for button in screen_size_buttons:
                    button.is_over(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen_size_buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.text == "800x600":
                            SCREEN_WIDTH = 800
                            SCREEN_HEIGHT = 600
                        elif button.text == "1024x768":
                            SCREEN_WIDTH = 1024
                            SCREEN_HEIGHT = 768
                        elif button.text == "1280x720":
                            SCREEN_WIDTH = 1280
                            SCREEN_HEIGHT = 720
                        elif button.text == "1920x1080":
                            SCREEN_WIDTH = 1920
                            SCREEN_HEIGHT = 1080
                        Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        GAME_BG = pygame.transform.scale(pygame.image.load("Space.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
                        MENU_BG = pygame.transform.scale(pygame.image.load("Menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
                        PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("player_ship.png"), (40, 40))
                        PLAYER_WIDTH = PLAYER_IMAGE.get_width()
                        PLAYER_HEIGHT = PLAYER_IMAGE.get_height()
                        settings_menu()
                        return
                    elif button.text == "Back":
                        settings_menu()
                        return

        for button in screen_size_buttons:
            button.draw(Screen, (0, 0, 0))

        pygame.display.update()
        
def game_controls_submenu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, Screen, GAME_BG, MENU_BG, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, SETTINGS_BG

    Screen.blit(SETTINGS_BG, (0,0))
    back_button = Button(50, 50, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))

    while True:
        
        font = pygame.font.SysFont("Comicsans", 30)

        up_message = font.render("Up arrow - Move the player up", True, (255, 255, 255))
        down_message = font.render("Down arrow - Move the player down", True, (255, 255, 255))
        right_message = font.render("Right arrow - Move the player to the right", True, (255, 255, 255))
        left_message = font.render("Left arrow - Move the player to the left", True, (255, 255, 255))
        shoot_message = font.render("Space bar - Shoot bullets at the enemies", True, (255, 255, 255))
        pause_message = font.render('"P" key - Pause the game', True, (255, 255, 255))
        
        up_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 125))
        down_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75))
        right_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25))
        left_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 25))
        shoot_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75))
        pause_message_rect = up_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 125 ))

        Screen.blit(up_message, up_message_rect)
        Screen.blit(down_message, down_message_rect)
        Screen.blit(right_message, right_message_rect)
        Screen.blit(left_message, left_message_rect)
        Screen.blit(shoot_message, shoot_message_rect)
        Screen.blit(pause_message, pause_message_rect)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEMOTION:
                    back_button.is_over(pygame.mouse.get_pos())
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    back_button.is_over(pygame.mouse.get_pos())
                    settings_menu()
                    return

                
        back_button.draw(Screen, (0, 0, 0))

        
        pygame.display.update()

def credits_submenu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, Screen, GAME_BG, MENU_BG, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, SETTINGS_BG

    Screen.blit(SETTINGS_BG, (0, 0))
    back_button = Button(50, 50, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))
    
    while True:
        font = pygame.font.SysFont("Comicsans", 30)
        chase_message = font.render("Chase Brown - Scrum master", True, (255, 255, 255))
        mark_message = font.render("Mark Georgi - Developer", True, (255, 255, 255))
        nidhish_message = font.render("Nidhish Shah - Developer", True, (255, 255, 255))
        ronel_message = font.render("Ronel Kakos - Developer", True, (255, 255, 255))
        lucas_message = font.render("Lucas Hermiz - Developer/Tester", True, (255, 255, 255))
        rachel_message = font.render("Rachel Michil - Developer", True, (255, 255, 255))
        
        chase_message_rect = chase_message.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 125))
        mark_message_rect = mark_message.get_rect(center=(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 - 75))
        nidhish_message_rect = nidhish_message.get_rect(center=(SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 25))
        ronel_message_rect = ronel_message.get_rect(center=(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 25))
        lucas_message_rect = lucas_message.get_rect(center=(SCREEN_WIDTH // 2 - 115, SCREEN_HEIGHT // 2 + 75))
        rachel_message_rect = rachel_message.get_rect(center=(SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 125 ))
        
        Screen.blit(chase_message, chase_message_rect)
        Screen.blit(mark_message,mark_message_rect)
        Screen.blit(nidhish_message, nidhish_message_rect)
        Screen.blit(ronel_message, ronel_message_rect)
        Screen.blit(lucas_message, lucas_message_rect)
        Screen.blit(rachel_message, rachel_message_rect)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEMOTION:
                    back_button.is_over(pygame.mouse.get_pos())
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    back_button.is_over(pygame.mouse.get_pos())
                    settings_menu()
                    return

                
        back_button.draw(Screen, (0, 0, 0))

        
        pygame.display.update()
        
def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    # Get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # Determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # If we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # Render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # Remove the text we just blitted
        text = text[i:]

    return text

def about_submenu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, Screen, GAME_BG, MENU_BG, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, SETTINGS_BG

    Screen.blit(SETTINGS_BG, (0, 0))
    back_button = Button(50, 50, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))
    
    font = pygame.font.SysFont("Comicsans", 20)
    about_message = ("Rebel Alliance: Galactic Revolt is a thrilling space shooter that takes players back to "
                     "the golden era of arcade games. Engage in intense space battles, dodge incoming fire, "
                     "and take down enemy ships to save the galaxy. This game, takes its design inspiration"
                     "from old-school videogames like Galaga and it delivers a nostalgic yet fresh experience"
                     "In this game while facing waves of increasingly difficult and proficient competitors,"
                     "players can gather power-ups to strengthen their weaponry and defenses.")

    while True:
        Screen.blit(SETTINGS_BG, (0, 0))

        draw_text(Screen, about_message, (255, 255, 255), pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 125, 500, 150), font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                back_button.is_over(pygame.mouse.get_pos())
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_over(pygame.mouse.get_pos()):
                    settings_menu()
                    return

        back_button.draw(Screen, (0, 0, 0))
        pygame.display.update()


def menu():
    Screen.blit(MENU_BG, (0, 0))

    start_button = Button(300, 200, 200, 50, "Start", (0, 255, 0), (0, 200, 0), (0, 255, 0))
    settings_button = Button(300, 275, 200, 50, "More", (0, 0, 255), (0, 0, 200), (0, 0, 255))
    quit_button = Button(300, 350, 200, 50, "Quit", (255, 0, 0), (200, 0, 0), (255, 0, 0))

    font = pygame.font.SysFont("comicsans", 30)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.text == "Start":
                            difficulty_menu()
                            return
                        elif button.text == "More":
                            settings_menu()
                            return
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

easy_mode = GameMode("Easy", 120)
medium_mode = GameMode("Medium", 80)
hard_mode = GameMode("Hard", 40)
game_modes = [easy_mode, medium_mode, hard_mode]
selected_mode = easy_mode

def difficulty_menu():
    global selected_mode
    easy_button = Button(300, 200, 200, 50, "Easy", (0, 255, 0), (0, 200, 0), (0, 255, 0))
    medium_button = Button(300, 275, 200, 50, "Medium", (255, 255, 0), (200, 200, 0), (255, 255, 0))
    hard_button = Button(300, 350, 200, 50, "Hard", (255, 0, 0), (200, 0, 0), (255, 0, 0))
    back_button = Button(300, 425, 200, 50, "Back", (255, 165, 0), (200, 130, 0), (255, 165, 0))
    buttons = [easy_button, medium_button, hard_button, back_button]

    while True:
        Screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.is_over(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.text == "Easy":
                            selected_mode = easy_mode
                            main()
                            return
                        elif button.text == "Medium":
                            selected_mode = medium_mode
                            main()
                            return
                        elif button.text == "Hard":
                            selected_mode = hard_mode
                            main()
                            return
                        elif button.text == "Back":
                            menu()
                            return

        font = pygame.font.SysFont("comicsans", 30)
        message = font.render("Select Difficulty", True, (255, 255, 255))
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
        Screen.blit(message, message_rect)

        for button in buttons:
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
    run = True

    player = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 75, PLAYER_WIDTH, PLAYER_HEIGHT)  # Start at center bottom
    bullets = []
    global score
    global lives
    global enemies
    lives = 3
    clock = pygame.time.Clock()  
    start_time = time.time()
    elapsed_time = 0
    time_for_snakes = False

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        if random.randint(1, selected_mode.spawn_rate) == 1:
            enemies.append(create_basic_enemy())

        if time_for_snakes or time.time() - start_time >= 5:
            time_for_snakes = True
            if random.randint(1, selected_mode.spawn_rate) == 1:
                for i in (-2, -1, 0):
                    enemies.append(create_snake_enemy(i * 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = [player.x + player.width // 2, player.y]
                    bullets.append(bullet)

                if event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == 'quit':
                        menu()
                    if action == 'restart':
                        main()
                        return
                    elif action == 'resume':
                        pass

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
                player = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 75, PLAYER_WIDTH, PLAYER_HEIGHT)  # Start at center bottom
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
        if not run:
            break

    pygame.quit()
    


if __name__ == "__main__":
    menu()
