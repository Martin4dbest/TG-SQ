from __future__ import division
import pygame
import random
from os import path

import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pygame
import random


import hashlib

## assets folder
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

###############################
## to be placed in "constant.py" later
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)




import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Quiz Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
FONT = pygame.font.Font(None, 36)



# Database Path
DB_PATH = "users.db"
BG_IMAGE_PATH = "images/login_window.PNG"  # Ensure this image exists



def create_database():
    """Ensure the database and table exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            scores INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            failed_quizzes INTEGER DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            last_login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ✅ **Hash Passwords for Security**
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ **Check if user exists**
def user_exists(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        return c.fetchone() is not None  # Returns True if user exists

# ✅ **Validate User Login (Check Hashed Password)**
def validate_login(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return c.fetchone() is not None  # Returns True if credentials match

# ✅ **Register New User (Store Hashed Password)**
def register_user(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

# ✅ **Update Amount Won (Corrected to Increment Instead of Overwrite)**
def update_amount_won(username, amount):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET amount_won = amount_won + ? WHERE username = ?", (amount, username))
        conn.commit()

# ✅ **Authentication Window**
def authenticate():
    global login_window, current_user  

    login_window = tk.Tk()
    login_window.title("Space Quiz Authentication")
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}")  

    # Load Background Image
    if os.path.exists(BG_IMAGE_PATH):
        bg_image = Image.open(BG_IMAGE_PATH)
        bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(login_window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_photo  

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

    # ✅ **Login Function**
    def login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()

        if validate_login(username, password):
            current_user = username  
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_window.destroy()
            show_planet_selection(username)  
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    # ✅ **Register Function**
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
            toggle_form()  

    # ✅ **Toggle Between Login & Register**
    is_login = True

    def toggle_form():
        nonlocal is_login
        if is_login:  
            confirm_password_label.grid(row=2, column=0, pady=5, padx=5)
            confirm_password_entry.grid(row=2, column=1, pady=5, padx=5)
            login_button.config(text="Register", command=register)
            toggle_button.config(text="Back to Login")
        else:  
            confirm_password_label.grid_forget()
            confirm_password_entry.grid_forget()
            login_button.config(text="Login", command=login)
            toggle_button.config(text="Create an Account")
        is_login = not is_login

    # ✅ **Buttons**
    login_button = tk.Button(frame, text="Login", font=("Arial", 12, "bold"), bg="green", fg="white", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=5)

    toggle_button = tk.Button(frame, text="Create an Account", font=("Arial", 12, "bold"), bg="blue", fg="white", command=toggle_form)
    toggle_button.grid(row=4, column=0, columnspan=2, pady=5)

    login_window.mainloop()


def save_score(username, score, correct_answers, failed_quizzes, time_spent):
    """Save or update the player's score correctly without affecting others."""
    if not username:
        return  # Prevents saving data for non-logged-in users

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Ensure username exists
    c.execute("SELECT scores FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        old_score = result[0] if result[0] is not None else 0
        updated_score = old_score + score  # Ensure scores accumulate

        c.execute("""
            UPDATE users 
            SET scores = ?, 
                correct_answers = correct_answers + ?, 
                failed_quizzes = failed_quizzes + ?, 
                time_spent = time_spent + ?, 
                last_updated = CURRENT_TIMESTAMP
            WHERE username = ?
        """, (updated_score, correct_answers, failed_quizzes, time_spent, username))

    else:
        c.execute("""
            INSERT INTO users (username, scores, correct_answers, failed_quizzes, time_spent, last_updated) 
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (username, score, correct_answers, failed_quizzes, time_spent))

    conn.commit()
    conn.close()



import subprocess
import pygame
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk




def show_leaderboard(screen, username): 
    """Display the leaderboard ensuring only logged-in users are shown."""
    import pygame
    import sqlite3

    if not pygame.get_init():
        pygame.init()

    if screen is None or not pygame.display.get_surface():
        screen = pygame.display.set_mode((800, 600))

    conn = sqlite3.connect("users.db")  # Ensure the database name is correct
    c = conn.cursor()

    c.execute("""
        SELECT username, scores, correct_answers, failed_quizzes, time_spent 
        FROM users 
        WHERE scores > 0 
        ORDER BY scores DESC
    """)
    leaderboard_data = c.fetchall()
    conn.close()

    print("Leaderboard Data Retrieved:", leaderboard_data)  # Debugging print

    if not leaderboard_data:
        print("⚠️ No data found in the leaderboard!")  # Check if the leaderboard is empty

    # Render leaderboard
    screen.fill((30, 30, 40))
    font_title = pygame.font.Font(None, 40)
    font_header = pygame.font.Font(None, 30)
    font_body = pygame.font.Font(None, 26)

    title_text = font_title.render(f"🏆 Leaderboard - {username} 🏆", True, (255, 215, 0))
    screen.blit(title_text, (250, 60))

    headers = ["Rank", "Player", "Score", "✅ Correct", "❌ Failed", "⏳ Time"]
    col_positions = [120, 200, 320, 420, 520, 620]
    row_height = 40

    header_y = 120
    for i, header in enumerate(headers):
        text = font_header.render(header, True, (200, 200, 200))
        screen.blit(text, (col_positions[i], header_y))

    y_offset = 160
    for rank, (player, score, correct_answers, failed_quizzes, time_spent) in enumerate(leaderboard_data, start=1):
        print(f"Rendering Player {player} with Score {score}")  # Debugging print

        time_str = f"{int(time_spent // 60)}m {int(time_spent % 60)}s"
        row_data = [f"{rank}.", player, str(score), str(correct_answers), str(failed_quizzes), time_str]

        row_color = (100, 100, 150) if player == username else (40, 40, 50) if rank % 2 == 0 else (30, 30, 40)
        pygame.draw.rect(screen, row_color, (110, y_offset - 5, 580, row_height), border_radius=8)

        for i, item in enumerate(row_data):
            text = font_body.render(item, True, (255, 255, 255))
            screen.blit(text, (col_positions[i], y_offset))

        pygame.draw.line(screen, (80, 80, 100), (110, y_offset + 30), (690, y_offset + 30), 1)
        y_offset += row_height

    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()  # Close leaderboard after delay



def update_scores(username, new_score):
    """Ensure the player's score is correctly updated."""
    if not username:
        return  # Prevent updating for non-logged-in users

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT scores FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        current_score = result[0] if result[0] is not None else 0
        updated_score = current_score + new_score

        c.execute("""
            UPDATE users 
            SET scores = ?, last_updated = CURRENT_TIMESTAMP
            WHERE username = ?
        """, (updated_score, username))
    else:
        c.execute("""
            INSERT INTO users (username, scores, correct_answers, failed_quizzes, time_spent, last_updated) 
            VALUES (?, ?, 0, 0, 0, CURRENT_TIMESTAMP)
        """, (username, new_score))

    conn.commit()
    conn.close()

def get_last_logged_in_user():
    """Retrieve the last logged-in user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username FROM users 
        ORDER BY last_login_time DESC 
        LIMIT 1
    """)
    
    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None  # Return None if no user is found

def show_planet_selection(username):
    global category_window

    category_window = tk.Tk()
    category_window.title("Select a Planet")

    screen_width = category_window.winfo_screenwidth()
    screen_height = category_window.winfo_screenheight()
    category_window.geometry(f"{screen_width}x{screen_height}")

    bg_image = Image.open("images/backgroundCategory.png")  # Update with your image path
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(category_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  # Keep reference

    ttk.Label(category_window, text=f"Welcome {username}! Select a Planet:", 
              font=("Arial", 18, "bold"), foreground="white", background="black").pack(pady=10)

    def start_game_after_selection(planet):
        global selected_category
        selected_category = planet
        category_window.destroy()  # Close selection window
        start_game(username, planet)  # Start game

    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    button_frame = tk.Frame(category_window)
    button_frame.pack(pady=20)

    for planet in planets:
        tk.Button(category_window, text=planet, font=("Arial", 12),
                command=lambda p=planet: start_game_after_selection(p)).pack(pady=5)

    logout_button = tk.Button(category_window, text="Logout", font=("Arial", 14, "bold"), 
                              bg="red", fg="white", bd=0, activebackground="red", 
                              activeforeground='white', cursor="hand2", 
                              command=logout)
    logout_button.place(relx=0.85, rely=0.05)  # ✅ Top-right corner

    category_window.mainloop()

import subprocess

def start_game(username, planet):
    """Launch the game, show leaderboard after game ends, then return to selection."""
    subprocess.run(["python", "comictravel.py", username, planet])
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    show_leaderboard(screen, username)  # Show leaderboard after game ends
    show_planet_selection(username)  # Return to planet selection




def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Close the category selection window
    authenticate()  # ✅ Redirect back to authentication




# ✅ **Main Program Execution**
if __name__ == "__main__":
    create_database()  # Ensure the database exists before authentication
    authenticate()  # Start authentication first

