from __future__ import division
import sqlite3
from datetime import datetime
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

import sqlite3
import hashlib
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import pygame
import functools

#import hashlib


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
DB_PATH = "myusers.db"
BG_IMAGE_PATH = "images/login_window.PNG"  # Ensure this image exists



def create_database():
    """Ensure the database and table exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,  -- ✅ Add password column
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


def user_exists(username):
    username = username.strip()  # ⛔ Don't convert to lowercase
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        return c.fetchone() is not None



# ✅ Validate User Login (Case-Sensitive Username)
def validate_login(username, password):
    username = username.strip()  # ❌ No .lower()
    hashed_password = hash_password(password)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return c.fetchone() is not None


def register_user(username, password):
    username = username.strip()  # ⛔ Don't convert to lowercase
    hashed_password = hash_password(password)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            print(f"✅ User {username} registered successfully.")
    except sqlite3.IntegrityError:
        print(f"❌ Error: Username '{username}' already exists.")




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
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty!")
            return

        if validate_login(username, password):
            current_user = username  
            update_last_login(username)  # ✅ Update last login timestamp
            handle_login(username)  # ✅ Handle login event properly
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
    """Save the user's score to the database, updating if the user already exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT scores FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()

    if existing_user:
        # Update existing user's score
        c.execute("""
            UPDATE users
            SET scores = scores + ?,
                correct_answers = correct_answers + ?,
                failed_quizzes = failed_quizzes + ?,
                time_spent = time_spent + ?,
                last_updated = ?
            WHERE username = ?
        """, (score, correct_answers, failed_quizzes, time_spent, datetime.now(), username))
    else:
        # Insert new user record
        c.execute("""
            INSERT INTO users (username, scores, correct_answers, failed_quizzes, time_spent, last_login_time, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, score, correct_answers, failed_quizzes, time_spent, datetime.now(), datetime.now()))

    conn.commit()
    conn.close()


def show_leaderboard(screen, username):
    """Display the leaderboard with users having scores of 1500 and above."""
    if not pygame.get_init():
        pygame.init()
        screen = pygame.display.set_mode((1400, 800)) 

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT username, scores, correct_answers, failed_quizzes
                FROM users 
                WHERE scores >= 200
                ORDER BY scores DESC
            """)
            leaderboard = c.fetchall()

        screen.fill((15, 15, 35))  
        pygame.font.init()

        title_font = pygame.font.Font(None, 50)
        header_font = pygame.font.Font(None, 36)
        entry_font = pygame.font.Font(None, 30)

        # Title
        title_text = title_font.render(" LEADERBOARD ", True, (255, 215, 0))  
        title_x = (screen.get_width() - title_text.get_width()) // 2  
        screen.blit(title_text, (title_x, 20))

        # Headers
        headers = ["Rank", "Player", "Score", "Correct Answers", "Incorrect Answers"]
        header_positions = [100, 300, 500, 750, 1050]  

        for i, header in enumerate(headers):
            header_text = header_font.render(header, True, (200, 200, 255))
            screen.blit(header_text, (header_positions[i], 80))

        # Leaderboard Entries
        if not leaderboard:
            msg = entry_font.render("No players have reached 1500 points yet.", True, (255, 255, 255))
            screen.blit(msg, (screen.get_width() // 2 - 150, 140))
        else:
            y_offset = 120  
            for idx, (user, score, correct, wrong) in enumerate(leaderboard, 1):
                marker = " (YOU)" if user == username else ""

                row_values = [
                    f"{idx}.", user, f"{score}", f"{correct}", f"{wrong}"
                ]
                for i, value in enumerate(row_values):
                    color = (255, 255, 255)
                    if i == 1 and marker:  
                        color = (0, 255, 0)  
                        value += marker  

                    entry_text = entry_font.render(value, True, color)
                    screen.blit(entry_text, (header_positions[i], y_offset))

                y_offset += 40  

        pygame.display.flip()

        # Event Loop to Close Leaderboard After a While
        running = True
        start_time = pygame.time.get_ticks()  
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif pygame.time.get_ticks() - start_time > 5000:  
                    running = False

        pygame.display.quit()  

    except pygame.error as e:
        print(f"⚠️ Pygame error: {e}")



def update_scores(username, new_score):
    """Update the user's score with the new score."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT scores FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()

        if user_data:
            c.execute("""
                UPDATE users
                SET scores = ?, last_updated = ?
                WHERE username = ?
            """, (new_score, datetime.now(), username))
        else:
            c.execute("""
                INSERT INTO users (username, scores, last_updated)
                VALUES (?, ?, ?)
            """, (username, new_score, datetime.now()))

        conn.commit()
        





def update_last_login(username):
    """Update the last login time and the last logged-in user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            current_time = datetime.now().isoformat()  # Get the current time
            # Update the last_login_time for the user
            c.execute("""
                UPDATE users
                SET last_login_time = ?
                WHERE username = ?
            """, (current_time, username))
            conn.commit()  # Save changes
            print(f"✅ Updated last login time for {username} at {current_time}")
            
            # Update the "last logged-in user" field if necessary
            c.execute("UPDATE settings SET value = ? WHERE key = 'last_logged_in_user'", (username,))
            conn.commit()  # Ensure the last logged-in user is updated
            print(f"✅ Updated last logged-in user to {username}")
    except sqlite3.Error as e:
        print(f"⚠️ Failed to update login time for {username}: {e}")

def get_last_logged_in_user():
    """Retrieve the last logged-in user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # Retrieve the last logged-in user from the settings table
            c.execute("SELECT value FROM settings WHERE key = 'last_logged_in_user'")
            result = c.fetchone()
            if result:
                return result[0]
            else:
                return None
    except sqlite3.Error as e:
        print(f"⚠️ Database Error: {e}")
        return None

def handle_login(username):
    """Handles post-login logic and displays last logged-in user."""
    update_last_login(username)  # Update the login time and last logged-in user
    
    # Immediately fetch the most recent logged-in user after the update
    last_user = get_last_logged_in_user()
    
    if last_user:
        print(f"Last logged-in user updated: {last_user}")
    else:
        print("No last logged-in user found.")




import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def show_planet_selection(username):
    """Display the planet selection screen."""
    global category_window

    category_window = tk.Tk()
    category_window.title("Select a Planet")

    screen_width = category_window.winfo_screenwidth()
    screen_height = category_window.winfo_screenheight()
    category_window.geometry(f"{screen_width}x{screen_height}")

    # Background Image
    bg_image = Image.open("images/backgroundCategory.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(category_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  # Keep reference

    # Title Label
    ttk.Label(category_window, text=f"Welcome {username}! Select a Planet:",
              font=("Arial", 18, "bold"), foreground="white", background="black").pack(pady=10)

    def start_game_after_selection(planet):
        """Start the game after selecting a planet."""
        global selected_category
        selected_category = planet

        # Destroy the Tkinter window before starting the game
        category_window.quit()  # Gracefully exit the Tkinter loop
        category_window.destroy()  # Properly close the window

        # Now start the game with the selected planet
        #subprocess.Popen(["python", "comictravel.py", str(username), str(planet)])
        process = subprocess.Popen(["python", "comictravel.py", str(username), str(planet)])
        process.wait()  # This makes app.py wait until comictravel.py closes


    # Planets & Their Colors
    planets = {
        "Mercury": "#808080",
        "Venus": "#FFD700",
        "Earth": "#2E8B57",
        "Mars": "#FF4500",
        "Jupiter": "#D2691E",
        "Saturn": "#DAA520",
        "Uranus": "#40E0D0",
        "Neptune": "#0000CD",
        "Pluto": "#A52A2A"
    }

    # Create a frame to hold the buttons
    button_frame = tk.Frame(category_window, bg="black")
    button_frame.pack(pady=20)

    # Arrange buttons in a 3-column grid
    for index, (planet, color) in enumerate(planets.items()):
        row = index // 3  
        col = index % 3  
        tk.Button(button_frame, text=planet, font=("Arial", 14, "bold"),
                  width=12, height=2, bg=color, fg="white",
                  bd=2, relief="raised", activebackground=color,
                  activeforeground="white", cursor="hand2",
                  command=lambda p=planet: start_game_after_selection(p)).grid(row=row, column=col, padx=15, pady=10)

    # Leaderboard Button
    leaderboard_button = tk.Button(category_window, text="🏆 View Leaderboard", font=("Arial", 14, "bold"),
                                   bg="#FFD700", fg="black", bd=3, relief="raised",
                                   activebackground="#FFD700", activeforeground="black", cursor="hand2",
                                   command=lambda: show_leaderboard_screen(username))
    leaderboard_button.pack(pady=20)

    # Logout Button
    logout_button = tk.Button(category_window, text="Logout", font=("Arial", 14, "bold"),
                              bg="red", fg="white", bd=0, activebackground="red",
                              activeforeground='white', cursor="hand2",
                              command=logout)
    logout_button.place(relx=0.85, rely=0.05)


        # Game Rules Function
    
    # Game Rules Function
        # Game Rules Function
    def show_game_rules():
        rules_window = tk.Toplevel(category_window)
        rules_window.title("Game Rules - Cosmo Trial")
        rules_window.geometry("600x500")
        rules_window.configure(bg="black")

        rules_text = (
            "🎯 Objective\n"
            "Pilot your spaceship, dodge asteroids, shoot threats, and complete quizzes to reach the sun.\n\n"
            "🕹 Controls\n"
            "↑ Move Up\n↓ Move Down\n← Move Backward\n→ Move Forward\nSpacebar: Shoot asteroids\n\n"
            "🧠 Quizzes\n"
            "- Appear every 30 seconds\n"
            "- Correct = Score boost\n"
            "- 3 wrong in a row = Health penalty\n\n"
            "💥 Gameplay\n"
            "- Destroy asteroids & answer quizzes to earn points\n"
            "- Collect Energy Orbs to restore health\n"
            "- Only asteroid hits cost lives\n"
            "- 3 Lives Total\n\n"
            "🏆 Win: Score 4000 points\n💀 Game Over: Health = 0 or Lives = 0"
        )

        tk.Label(rules_window, text="Cosmo Trial - Game Rules", font=("Arial", 16, "bold"),
                 fg="white", bg="black").pack(pady=10)

        rules_box = tk.Text(rules_window, wrap="word", font=("Arial", 12),
                            bg="#1c1c1c", fg="white", bd=0, padx=20, pady=10)
        rules_box.insert("1.0", rules_text)
        rules_box.config(state="disabled")
        rules_box.pack(expand=True, fill="both", padx=20, pady=10)

    # Game Rules Button
    rules_button = tk.Button(category_window, text="📜 Game Rules", font=("Arial", 14, "bold"),
                             bg="#1E90FF", fg="white", bd=3, relief="raised",
                             activebackground="#1E90FF", activeforeground="white", cursor="hand2",
                             command=show_game_rules)
    rules_button.pack(pady=10)


    category_window.mainloop()


    
def show_leaderboard_screen(username):
    """Wrapper function to open the leaderboard using Pygame."""
    pygame.init()
    screen = pygame.display.set_mode((1400, 800))  # Larger window but not fullscreen
    show_leaderboard(screen, username)  # Pass screen to leaderboard function





    

def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Close the category selection window
    authenticate()  # ✅ Redirect back to authentication




# ✅ **Main Program Execution**
if __name__ == "__main__":
    create_database()  # Ensure the database exists before authentication
    authenticate()  # Start authentication first


   