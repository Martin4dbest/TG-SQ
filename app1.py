import pygame
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Quiz Adventure")

# Colors
WHITE, RED, GREEN, BLUE, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)

# Load background images
backgrounds = []
for i in range(1, 10):
    try:
        img = pygame.image.load(f"images/pix{i}.jpg")
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        backgrounds.append(img)
    except pygame.error:
        print(f"Warning: Missing background image: images/pix{i}.jpg")

if not backgrounds:
    raise FileNotFoundError("No background images found!")

# Game assets
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        return pygame.Surface(size)

spaceship_img = load_image("images/spaceship.png", (60, 60))
asteroid_img = load_image("images/asteroid.png", (40, 40))
enemy_ship_img = load_image("images/enemy.png", (50, 50))
energy_orb_img = load_image("images/energy.png", (30, 30))

# Sounds
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

correct_sound = load_sound("audio/aliens.wav")
wrong_sound = load_sound("audio/cartoon-fail-trumpet.mp3")
hit_sound = load_sound("audio/cartoon-fail-trumpet.mp3")
powerup_sound = load_sound("audio/aliens.wav")

# Fonts
font = pygame.font.Font(None, 36)

# Game Variables
spaceship_x, spaceship_y, spaceship_speed = 100, HEIGHT // 2, 5
cosmo_energy, timer, quiz_timer, score = 1000, 60, 20, 0
obstacles, energy_orbs = [], []
running, quiz_active, overload_mode = True, False, False
overload_timer = 0
final_stretch = False

# Category (Starting Planet) Selection
categories = ["Mercury", "Venus", "Mars", "Jupiter"]
selected_category = random.choice(categories)

# Quiz Data
quiz_data = [
    ("Closest planet to the Sun?", ["Mars", "Venus", "Mercury", "Earth"], "Mercury"),
    ("Gas plants absorb?", ["Oxygen", "CO2", "Nitrogen", "Hydrogen"], "CO2"),
    ("Legs of a spider?", ["6", "8", "10", "12"], "8")
]

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Quiz System
quiz_buttons = []

def start_quiz():
    global quiz_active, quiz_question, quiz_options, correct_answer, quiz_buttons
    quiz_active = True
    question, options, answer = random.choice(quiz_data)
    quiz_question, quiz_options, correct_answer = question, options, answer
    quiz_buttons = [Button(opt, 120, 250 + i * 50, 200, 40, lambda opt=opt: check_answer(opt)) for i, opt in enumerate(quiz_options)]

def check_answer(answer):
    global quiz_active, cosmo_energy
    if answer == correct_answer:
        cosmo_energy += 100
        correct_sound.play() if correct_sound else None
    else:
        cosmo_energy -= 50
        wrong_sound.play() if wrong_sound else None
    quiz_active = False

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        draw_text(self.text, self.rect.x + 10, self.rect.y + 10)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Obstacle Class
class Obstacle:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed  # Move the obstacle left
        if self.rect.right < 0:  # Remove when off-screen
            return False
        return True

    def draw(self):
        screen.blit(self.image, self.rect)

# Spawn Obstacles
def spawn_obstacle():
    y_pos = random.randint(50, HEIGHT - 50)
    obstacle_type = random.choice(["asteroid", "enemy"])
    if obstacle_type == "asteroid":
        obstacles.append(Obstacle(WIDTH, y_pos, asteroid_img, random.randint(3, 6)))
    else:
        obstacles.append(Obstacle(WIDTH, y_pos, enemy_ship_img, random.randint(4, 7)))

# Game Loop
clock = pygame.time.Clock()
spawn_timer = 0  # Timer for obstacle spawning

while running:
    screen.fill(BLACK)
    
    # Background transitions
    current_bg_index = int((60 - timer) // 10) % len(backgrounds)
    screen.blit(backgrounds[current_bg_index], (0, 0))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if quiz_active:
            for button in quiz_buttons:
                button.check_click(event)

    # Player Controls (Up, Down, Left, Right)
    keys = pygame.key.get_pressed()
    if not quiz_active:
        if keys[pygame.K_UP]: 
            spaceship_y -= spaceship_speed  # Move Up
        if keys[pygame.K_DOWN]: 
            spaceship_y += spaceship_speed  # Move Down
        if keys[pygame.K_LEFT]: 
            spaceship_x -= spaceship_speed  # Move Left (Backward)
        if keys[pygame.K_RIGHT]: 
            spaceship_x += spaceship_speed  # Move Right (Forward)

    # Ensure spaceship stays within screen bounds
    spaceship_x = max(0, min(spaceship_x, WIDTH - spaceship_img.get_width()))
    spaceship_y = max(0, min(spaceship_y, HEIGHT - spaceship_img.get_height()))

    # Energy Drain & Timer
    cosmo_energy -= 5 / 60
    timer -= 1 / 60
    quiz_timer -= 1 / 60

    # Start Quiz Every 20 Seconds
    if quiz_timer <= 0 and not quiz_active:
        start_quiz()
        quiz_timer = 20

    # Overload Mode Activation
    if cosmo_energy >= 1500 and not overload_mode:
        overload_mode, overload_timer = True, 10 * 60

    if overload_mode:
        spaceship_speed = 10
        overload_timer -= 1
        if overload_timer <= 0:
            overload_mode = False
            cosmo_energy -= 50
            spaceship_speed = 5

    # Final Stretch (Last 20 Seconds)
    if timer <= 20 and not final_stretch:
        final_stretch = True
        spaceship_speed = 7  # Increase speed
        cosmo_energy -= 10 / 60  # Increase energy drain

    # Spawn obstacles every 2 seconds
    spawn_timer += 1 / 60
    if spawn_timer >= 2:
        spawn_obstacle()
        spawn_timer = 0

    # Update and draw obstacles (fix to ensure they appear continuously)
    for obstacle in obstacles[:]:  # Iterate over a copy of the list
        if not obstacle.update():  # Remove obstacles that move off-screen
            obstacles.remove(obstacle)

    for obstacle in obstacles:
        obstacle.draw()

    # Draw spaceship
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))

    # Display Info
    draw_text(f"Energy: {int(cosmo_energy)}", 10, 10, GREEN)
    draw_text(f"Time: {int(timer)}s", 10, 50)
    draw_text(f"Starting Planet: {selected_category}", 10, 90)

    if quiz_active:
        draw_text(quiz_question, 100, 200)
        for button in quiz_buttons:
            button.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
