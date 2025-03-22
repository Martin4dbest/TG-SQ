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
import time
import threading



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
            current_user = username  # ✅ Always store the correct logged-in user
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_window.destroy()
            show_planet_selection()  # ✅ No need to pass username, use `current_user`
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



def get_top_scores(logged_in_user):
    """Fetch top scores while ensuring only users with at least 200 points appear."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Fetch the top 10 scorers who have at least 200 points
    c.execute("""
        SELECT username, scores, correct_answers, failed_quizzes, time_spent, last_updated 
        FROM users 
        WHERE scores >= 200 
        ORDER BY scores DESC 
        LIMIT 10
    """)
    top_players = c.fetchall()

    # Fetch only the logged-in user's score separately
    c.execute("""
        SELECT username, scores, correct_answers, failed_quizzes, time_spent, last_updated 
        FROM users 
        WHERE username = ? AND scores >= 200
    """, (logged_in_user,))
    logged_user_data = c.fetchone()

    conn.close()

    # Ensure the logged-in user is always included in the leaderboard
    leaderboard_set = {player[0] for player in top_players}  
    if logged_user_data and logged_user_data[0] not in leaderboard_set:
        top_players.append(logged_user_data)

    return top_players



def update_scores(username, new_score):
    """Update the correct user's score without overriding another player."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Fetch current score
    c.execute("SELECT scores FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        current_score = result[0] if result[0] is not None else 0
        print(f"🔍 Before Update - {username}: Current Score = {current_score}, New Score = {new_score}")

        # Ensure we're updating the correct user
        c.execute("""
            UPDATE users 
            SET scores = ?, last_updated = ? 
            WHERE username = ?
        """, (max(new_score, current_score), time.strftime("%Y-%m-%d %H:%M:%S"), username))

        print(f"✅ After Update - {username}: Updated Score = {max(new_score, current_score)}")
    else:
        print(f"⚠️ ERROR: {username} not found in database!")

    conn.commit()
    conn.close()


def save_score(username, score, correct_answers, failed_quizzes, time_spent):
    """Save or update the player's score properly."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if the user exists
    c.execute("SELECT scores, correct_answers, failed_quizzes, time_spent FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        old_score, old_correct, old_failed, old_time_spent = result
        updated_score = old_score + score  # Add new score to existing score
        
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
        # Insert new user with their first recorded score
        c.execute("""
            INSERT INTO users (username, scores, correct_answers, failed_quizzes, time_spent, last_updated) 
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (username, score, correct_answers, failed_quizzes, time_spent))

    conn.commit()
    conn.close()



def update_user_stats(username, correct_answers, failed_quizzes, total_time_spent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_exists = c.fetchone()

    if user_exists:
        c.execute("""
            UPDATE users 
            SET correct_answers = correct_answers + ?, 
                failed_quizzes = failed_quizzes + ?, 
                time_spent = time_spent + ?
            WHERE username = ?
        """, (correct_answers, failed_quizzes, total_time_spent, username))
    else:
        c.execute("""
            INSERT INTO users (username, scores, correct_answers, failed_quizzes, time_spent, last_updated) 
            VALUES (?, 0, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (username, correct_answers, failed_quizzes, total_time_spent))

    conn.commit()
    conn.close()


def show_leaderboard(screen, username):
    """Display the leaderboard with scores, correct answers, failed quizzes, and time spent."""
    if not pygame.get_init():
        pygame.init()

    if screen is None or not pygame.display.get_surface():
        screen = pygame.display.set_mode((800, 600))

    #leaderboard_data = get_top_scores()  # Get all players sorted by score

    logged_in_user = get_last_logged_in_user()
    leaderboard_data = get_top_scores(logged_in_user)


    # Find the logged-in user's data and separate it
    user_data = None
    for entry in leaderboard_data:
        if entry[0] == username:
            user_data = entry
            break  # Stop searching once found

    if user_data:
        leaderboard_data.remove(user_data)  # Remove user from sorted leaderboard
        leaderboard_data.insert(0, user_data)  # Insert at the top

    # Background gradient effect
    for y in range(600):
        color = (30 + y // 20, 30 + y // 20, 40 + y // 10)  # Dark blue gradient
        pygame.draw.line(screen, color, (0, y), (800, y))

    pygame.draw.rect(screen, (20, 20, 30), (100, 50, 600, 500), border_radius=15)

    font_title = pygame.font.Font(None, 40)
    font_header = pygame.font.Font(None, 30)
    font_body = pygame.font.Font(None, 26)

    title_text = font_title.render("🏆 Leaderboard 🏆", True, (255, 215, 0))  # Gold color
    screen.blit(title_text, (300, 60))

    headers = ["Rank", "Player", "Score", "✅ Correct", "❌ Failed", "⏳ Time"]
    col_positions = [120, 200, 320, 420, 520, 620]
    row_height = 40

    header_y = 120
    pygame.draw.rect(screen, (50, 50, 70), (110, header_y - 5, 580, row_height), border_radius=10)

    for i, header in enumerate(headers):
        text = font_header.render(header, True, (200, 200, 200))
        screen.blit(text, (col_positions[i], header_y))

    y_offset = 160
    for rank, (player, score, correct_answers, failed_quizzes, time_spent, timestamp) in enumerate(leaderboard_data, start=1):
        time_str = f"{int(time_spent // 60)}m {int(time_spent % 60)}s"
        row_data = [f"{rank}.", player, str(score), str(correct_answers), str(failed_quizzes), time_str]

        # Highlight the logged-in user's row
        if player == username:
            row_color = (100, 100, 150)  # A different color for the logged-in user
        else:
            row_color = (40, 40, 50) if rank % 2 == 0 else (30, 30, 40)

        pygame.draw.rect(screen, row_color, (110, y_offset - 5, 580, row_height), border_radius=8)

        for i, item in enumerate(row_data):
            text = font_body.render(item, True, (255, 255, 255))
            screen.blit(text, (col_positions[i], y_offset))

        pygame.draw.line(screen, (80, 80, 100), (110, y_offset + 30), (690, y_offset + 30), 1)
        y_offset += row_height

    pygame.display.update()
    pygame.time.delay(10000)


def show_planet_selection():
    global category_window

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
    bg_label.image = bg_photo  

    ttk.Label(category_window, text=f"Welcome {current_user}! Select a Planet:", 
              font=("Arial", 18, "bold"), foreground="white", background="black").pack(pady=10)

    def start_game_after_selection(planet):
        global selected_category
        selected_category = planet
        category_window.destroy()
        start_game(planet, current_user)  # ✅ Use `current_user`, not `username`

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
    logout_button.place(relx=0.85, rely=0.05)

    category_window.mainloop()




def record_game_session(username, score, correct_answers, failed_quizzes, time_spent):
    """Records a player's game session in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO game_sessions (username, score, correct_answers, failed_quizzes, time_spent)
        VALUES (?, ?, ?, ?, ?)
    """, (username, score, correct_answers, failed_quizzes, time_spent))

    conn.commit()
    conn.close()
    print(f"Game session for {username} recorded successfully!")


def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Close the category selection window
    authenticate()  # ✅ Redirect back to authentication




import subprocess

def start_game(username, planet):
    try:
        subprocess.Popen(["python", "comictravel.py", username, planet], shell=True)  
    except Exception as e:
        print(f"Error starting the game: {e}")




import sqlite3

def get_last_logged_in_user():
    conn = sqlite3.connect("users.db")  # Ensure this is your correct database file
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users LIMIT 1")  # Fetch the most recent username
    user = cursor.fetchone()  # Get the result
    
    conn.close()
    
    return user[0] if user else "Guest"  # Return username or "Guest" if no user is found



# ✅ **Main Program Execution**
if __name__ == "__main__":
    create_database()  # Ensure the database exists before authentication
    authenticate()  # Start authentication first

