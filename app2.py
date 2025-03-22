import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pygame
import random
import time

# Initialize Pygame
pygame.init()



# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
QUIZ_DURATION = 30  
QUIZ_INTERVAL = 20  
OVERLOAD_THRESHOLD = 1500  
OVERLOAD_DURATION = 10  
FINAL_STRETCH_TIME = 20  
GAME_DURATION = 120  

# Load Backgrounds
QUIZ_BG_IMAGE = pygame.image.load("images/pix1.jpg")
QUIZ_BG_IMAGE = pygame.transform.scale(QUIZ_BG_IMAGE, (WIDTH, HEIGHT))
GAME_BG_IMAGE = pygame.image.load("images/pix2.jpg")
GAME_BG_IMAGE = pygame.transform.scale(GAME_BG_IMAGE, (WIDTH, HEIGHT))
SUN_BG_IMAGE = pygame.image.load("images/pix3.jpg")

# Load Images for Obstacles
ASTEROID_IMAGE = pygame.image.load("images/asteroid.png")
ENEMY_IMAGE = pygame.image.load("images/enemy.png")
ORB_IMAGE = pygame.image.load("images/energy.png")

# Fonts
font = pygame.font.Font(None, 36)

# Obstacles and energy orbs
obstacles = []
orbs = []

# Spaceship
spaceship = pygame.Rect(WIDTH // 2, HEIGHT - 100, 50, 50)
spaceship_speed = 5

# Game screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Quiz Adventure")
# Game Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


# Spaceship Settings
spaceship_x = 370
spaceship_y = 500


# Game Variables
selected_category = None
category_selected = False
quiz_active = False

# Database Path
DB_PATH = "users.db"
BG_IMAGE_PATH = "images/login_window.PNG"  # Ensure this image exists

# ✅ **Create Database and Table**
def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY, 
                 password TEXT, 
                 scores INTEGER DEFAULT 0, 
                 amount_won REAL DEFAULT 0.0)''')
    conn.commit()
    conn.close()

# ✅ **Check if user exists in the database**
def user_exists(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None  # Returns True if user exists

# ✅ **Validate User Login**
def validate_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None  # Returns True if credentials match

# ✅ **Register New User**
def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# ✅ **Update Scores**
def update_scores(username, new_score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET scores = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

# ✅ **Update Amount Won**
def update_amount_won(username, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET amount_won = ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()


# ✅ Function to handle authentication window
def authenticate():
    global login_window, current_user  # Declare current_user globally

    login_window = tk.Tk()
    login_window.title("Space Quiz Authentication")
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}")  # Fullscreen

    # Load Background Image
    if os.path.exists(BG_IMAGE_PATH):
        bg_image = Image.open(BG_IMAGE_PATH)
        bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(login_window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_photo  # Keep reference

    # Authentication Frame
    frame = tk.Frame(login_window, bg="black", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Username & Password Fields
    tk.Label(frame, text="Username:", fg="white", bg="black", font=("Arial", 14)).grid(row=0, column=0, pady=5, padx=5)
    username_entry = tk.Entry(frame, font=("Arial", 14))
    username_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(frame, text="Password:", fg="white", bg="black", font=("Arial", 14)).grid(row=1, column=0, pady=5, padx=5)
    password_entry = tk.Entry(frame, font=("Arial", 14), show="*")
    password_entry.grid(row=1, column=1, pady=5, padx=5)

    confirm_password_label = tk.Label(frame, text="Confirm Password:", fg="white", bg="black", font=("Arial", 14))
    confirm_password_entry = tk.Entry(frame, font=("Arial", 14), show="*")

    # Login Function
    def login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()

        if validate_login(username, password):
            current_user = username  # Store logged-in user
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_window.destroy()
            show_planet_selection(username)  # Pass username to next step
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    # Register Function
    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if user_exists(username):
            messagebox.showerror("Error", "Username already exists!")
        else:
            register_user(username, password)
            messagebox.showinfo("Success", "Registration Successful!")
            toggle_form()  # Switch back to login form

    # Toggle Between Login & Register
    is_login = True

    def toggle_form():
        nonlocal is_login
        if is_login:  # Switch to Register Form
            confirm_password_label.grid(row=2, column=0, pady=5, padx=5)
            confirm_password_entry.grid(row=2, column=1, pady=5, padx=5)
            login_button.config(text="Register", command=register)
            toggle_button.config(text="Back to Login")
        else:  # Switch to Login Form
            confirm_password_label.grid_forget()
            confirm_password_entry.grid_forget()
            login_button.config(text="Login", command=login)
            toggle_button.config(text="Create an Account")
        is_login = not is_login

    # Buttons
    login_button = tk.Button(frame, text="Login", font=("Arial", 12, "bold"), bg="green", fg="white", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=5)

    toggle_button = tk.Button(frame, text="Create an Account", font=("Arial", 12, "bold"), bg="blue", fg="white", command=toggle_form)
    toggle_button.grid(row=4, column=0, columnspan=2, pady=5)

    login_window.mainloop()

def show_planet_selection(username):
    global selected_category, category_selected

    category_window = tk.Tk()
    category_window.title("Select a Planet")

    screen_width = category_window.winfo_screenwidth()
    screen_height = category_window.winfo_screenheight()
    category_window.geometry(f"{screen_width}x{screen_height}")

    bg_image = Image.open("images/backgroundCategory.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(category_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  # Keep reference

    ttk.Label(category_window, text=f"Welcome {username}! Select a Planet:", 
              font=("Arial", 18, "bold"), foreground="white", background="black").pack(pady=10)

    def on_planet_selected(planet):
        global selected_category, category_selected
        selected_category = planet  # Store the selected planet
        category_selected = True
        category_window.destroy()  # Close selection screen
        start_game(username)  # Start game

    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    
    for planet in planets:
        btn = ttk.Button(category_window, text=planet, command=lambda p=planet: on_planet_selected(p))
        btn.pack(pady=5)

    category_window.mainloop()



# Define QUESTIONS before using it
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "What is 5 + 3?",
        "options": ["5", "8", "10", "15"],
        "answer": "8"
    },
    {
        "question": "Who developed Python?",
        "options": ["Dennis Ritchie", "Guido van Rossum", "Bjarne Stroustrup", "James Gosling"],
        "answer": "Guido van Rossum"
    }
]

# ✅ Function to start the quiz using Tkinter
def start_quiz(username):
    global energy
    quiz_window = tk.Tk()
    quiz_window.title("Quiz Time!")
    quiz_window.geometry("400x300")
    quiz_window.configure(bg="black")

    tk.Label(quiz_window, text=f"Quiz for {username}", 
             font=("Arial", 18, "bold"), fg="white", bg="black").pack(pady=20)

    question = random.choice(QUESTIONS)  # Select a random question
    tk.Label(quiz_window, text=question["question"], font=("Arial", 12), fg="white", bg="black").pack(pady=10)

    def check_answer(option):
        global energy
        if option == question["answer"]:
            messagebox.showinfo("Correct!", "You got it right! +100 Energy")
            energy += 100
        else:
            messagebox.showerror("Wrong!", "Oops, incorrect! -50 Energy")
            energy -= 50
        quiz_window.destroy()  # Close quiz after answering

    for option in question["options"]:
        tk.Button(quiz_window, text=option, font=("Arial", 12, "bold"), bg="blue", fg="white",
                  command=lambda opt=option: check_answer(opt)).pack(pady=5)

    quiz_window.mainloop()


# ✅ **Game Logic**
def spawn_obstacle():
    """ Creates a new asteroid or enemy ship """
    x = random.randint(100, WIDTH - 100)
    y = -50
    obstacle_type = random.choice(["asteroid", "enemy"])
    image = ASTEROID_IMAGE if obstacle_type == "asteroid" else ENEMY_IMAGE
    obstacles.append({"rect": pygame.Rect(x, y, 50, 50), "image": image, "type": obstacle_type})

def spawn_energy_orb():
    """ Creates a new energy orb """
    x = random.randint(100, WIDTH - 100)
    y = -50
    orbs.append({"rect": pygame.Rect(x, y, 30, 30), "image": ORB_IMAGE})

def update_obstacles():
    """ Moves obstacles and checks collisions """
    global energy
    for obs in obstacles:
        obs["rect"].y += 5
        if obs["rect"].y > HEIGHT:
            obstacles.remove(obs)
        if spaceship.colliderect(obs["rect"]):
            if obs["type"] == "asteroid":
                energy -= 30
            elif obs["type"] == "enemy":
                energy -= 50
            obstacles.remove(obs)

def update_orbs():
    """ Moves orbs and checks collection """
    global energy
    for orb in orbs:
        orb["rect"].y += 3
        if orb["rect"].y > HEIGHT:
            orbs.remove(orb)
        if spaceship.colliderect(orb["rect"]):
            energy += 50
            orbs.remove(orb)

# ✅ **Main Game Loop**
def start_game(username):
    """ Main game loop """
    global energy
    clock = pygame.time.Clock()
    energy = 500
    start_time = pygame.time.get_ticks()
    last_quiz_time = 0
    overload_active = False
    overload_start_time = 0

    running = True
    while running:
        clock.tick(FPS)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        time_left = max(GAME_DURATION - elapsed_time, 0)

        # Change background near the Sun
        if time_left <= FINAL_STRETCH_TIME:
            screen.blit(SUN_BG_IMAGE, (0, 0))
        else:
            screen.blit(GAME_BG_IMAGE, (0, 0))

        # Overload Mode
        if energy >= OVERLOAD_THRESHOLD and not overload_active:
            overload_active = True
            overload_start_time = elapsed_time
        if overload_active:
            pygame.draw.rect(screen, (255, 215, 0), (50, 550, 200, 30))
            if elapsed_time - overload_start_time >= OVERLOAD_DURATION:
                overload_active = False
                energy -= 50

        # Quiz Logic
        if elapsed_time - last_quiz_time >= QUIZ_INTERVAL:
            pygame.display.update()
            pygame.time.wait(500)  # Pause before quiz
            start_quiz(username)
            last_quiz_time = elapsed_time

        # Spawn Obstacles & Orbs
        if random.randint(1, 60) == 1:
            spawn_obstacle()
        if random.randint(1, 80) == 1:
            spawn_energy_orb()

        update_obstacles()
        update_orbs()

        # Spaceship Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and spaceship.x > 0:
            spaceship.x -= spaceship_speed
        if keys[pygame.K_d] and spaceship.x < WIDTH - 50:
            spaceship.x += spaceship_speed

        # Draw Spaceship
        pygame.draw.rect(screen, (0, 255, 0), spaceship)

        # Draw Energy Bar
        pygame.draw.rect(screen, (0, 255, 0), (50, 50, energy / 2, 20))

        # Draw Timer
        timer_text = font.render(f"Time Left: {time_left}s", True, (255, 255, 255))
        screen.blit(timer_text, (WIDTH - 200, 20))

        pygame.display.flip()

        # Check Game Over
        if energy <= 0 or time_left == 0:
            if time_left == 0 and energy >= 800:
                print("Victory! You reached the Sun!")
            else:
                print("Game Over!")
            running = False

    pygame.quit()


# ✅ **Main Program Execution**
if __name__ == "__main__":
    create_database()  # Ensure database is initialized
    username = authenticate()  # Start authentication and get username
    start_game(username)  # Start game after authentication