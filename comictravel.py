#!/usr/bin/env python
from __future__ import division
import pygame
import random
from os import path


total_correct_answers = 0
total_failed_quizzes = 0

import app  # Import app for handling users


# ✅ Get the logged-in user before any game logic
username = app.get_last_logged_in_user()  

if username is None:
    print("Error: No user is logged in.")
    exit()  # Exit the game if no user is logged in


## assets folder
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

###############################


"""
WIDTH = 1400  # Wider but not fullscreen  
HEIGHT = 800  # Slightly taller for better UI space  
"""

WIDTH, HEIGHT = 1400, 700  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Apply new size


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
###############################

###############################
## to placed in "__init__.py" later
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Journey: A Space Survival Quiz ")
clock = pygame.time.Clock()     ## For syncing the FPS
###############################



import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
#WIDTH, HEIGHT = 800, 600
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




# Questions list
questions = [
    {"question": "What is 5 + 3?", "options": ["6", "8", "10", "12"], "answer": "8"},
    {"question": "What is the capital of France?", "options": ["London", "Paris", "Berlin", "Madrid"], "answer": "Paris"},
    {"question": "What is 10 / 2?", "options": ["3", "5", "7", "9"], "answer": "5"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
    {"question": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "answer": "Pacific"},
    {"question": "Who developed the theory of relativity?", "options": ["Newton", "Einstein", "Galileo", "Hawking"], "answer": "Einstein"},
    {"question": "What is the chemical symbol for gold?", "options": ["Ag", "Au", "Pb", "Fe"], "answer": "Au"},
    {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "What is the capital of Japan?", "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"], "answer": "Tokyo"},
    {"question": "Which gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"], "answer": "Da Vinci"},
    {"question": "What is the square root of 64?", "options": ["6", "8", "10", "12"], "answer": "8"},
    {"question": "What is the freezing point of water in Celsius?", "options": ["0", "32", "100", "-5"], "answer": "0"},
    {"question": "What is the currency of the United Kingdom?", "options": ["Dollar", "Euro", "Pound", "Yen"], "answer": "Pound"},
    {"question": "Which is the fastest land animal?", "options": ["Cheetah", "Lion", "Horse", "Tiger"], "answer": "Cheetah"},
    {"question": "What is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippo"], "answer": "Blue Whale"},
    {"question": "Which country is famous for the Great Wall?", "options": ["Japan", "China", "India", "Mongolia"], "answer": "China"},
    {"question": "Who invented the telephone?", "options": ["Edison", "Bell", "Tesla", "Marconi"], "answer": "Bell"},
    {"question": "Which is the smallest prime number?", "options": ["0", "1", "2", "3"], "answer": "2"},
    {"question": "Which metal is liquid at room temperature?", "options": ["Iron", "Mercury", "Aluminum", "Lead"], "answer": "Mercury"},
    {"question": "What is the capital city of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "answer": "Canberra"},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Shakespeare", "Jane Austen", "Charles Dickens", "Homer"], "answer": "Shakespeare"},
    {"question": "In what year did the United States declare its independence?", "options": ["1776", "1789", "1800", "1754"], "answer": "1776"},
    {"question": "Who painted the famous artwork 'Starry Night'?", "options": ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"], "answer": "Vincent van Gogh"},
    {"question": "Which gas makes up the majority of Earth's atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"], "answer": "Nitrogen"},
    {"question": "Who is known as the 'Father of Modern Physics'?", "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"], "answer": "Albert Einstein"},
    {"question": "Which country is known as the 'Land of the Rising Sun'?", "options": ["China", "South Korea", "Japan", "Vietnam"], "answer": "Japan"},
    {"question": "Which of the following elements is a noble gas?", "options": ["Oxygen", "Helium", "Carbon", "Neon"], "answer": "Helium"},
    {"question": "Who wrote the famous novel 'To Kill a Mockingbird'?", "options": ["J.K. Rowling", "Harper Lee", "Ernest Hemingway", "Mark Twain"], "answer": "Harper Lee"},
    {"question": "Who wrote 'War and Peace'?", "options": ["Fyodor Dostoevsky", "Leo Tolstoy", "Ernest Hemingway", "Anton Chekhov"], "answer": "Leo Tolstoy"},
    {"question": "Who wrote 'Moby-Dick'?", "options": ["Stephen King", "Herman Melville", "Charles Dickens", "Nathaniel Hawthorne"], "answer": "Herman Melville"},
    {"question": "Who wrote '1984'?", "options": ["Aldous Huxley", "George Orwell", "J.R.R. Tolkien", "Ray Bradbury"], "answer": "George Orwell"},
    {"question": "Who created the fictional detective Hercule Poirot?", "options": ["Raymond Chandler", "Arthur Conan Doyle", "Agatha Christie", "Dashiell Hammett"], "answer": "Agatha Christie"},
    {"question": "Which Shakespearean tragedy features the character Ophelia?", "options": ["King Lear", "Hamlet", "Othello", "Macbeth"], "answer": "Hamlet"},
    {"question": "Who wrote 'The Lord of the Rings' trilogy?", "options": ["J.K. Rowling", "J.R.R. Tolkien", "Mark Twain", "C.S. Lewis"], "answer": "J.R.R. Tolkien"},
    {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Emily Brontë", "Jane Austen", "Charlotte Brontë", "Louisa May Alcott"], "answer": "Jane Austen"},
    {"question": "Who wrote 'Don Quixote'?", "options": ["Fyodor Dostoevsky", "Miguel de Cervantes", "Leo Tolstoy", "Victor Hugo"], "answer": "Miguel de Cervantes"},
    {"question": "What is the longest river in the world?", "options": ["Amazon", "Nile", "Mississippi", "Yangtze"], "answer": "Nile"},
    {"question": "What is the process of converting light energy into electrical energy known as?", "options": ["Photosynthesis", "Respiration", "Transmutation", "Solarization"], "answer": "Photosynthesis"},
    {"question": "Which famous scientist developed the theory of relativity?", "options": ["Isaac Newton", "Galileo Galilei", "Albert Einstein", "Johannes Kepler"], "answer": "Albert Einstein"},
    {"question": "What is the smallest unit of matter?", "options": ["Molecule", "Atom", "Proton", "Electron"], "answer": "Atom"},
    {"question": "What does CPU stand for in the context of computing?", "options": ["Central Processing Unit", "Computer Processing Unit", "Central Power Unit", "Center Power Unit"], "answer": "Central Processing Unit"},
    {"question": "What is the name of the closest planet to the Sun in our solar system?", "options": ["Mars", "Mercury", "Venus", "Earth"], "answer": "Mercury"},
    {"question": "Who is credited with inventing the World Wide Web?", "options": ["Tim Berners-Lee", "Nikola Tesla", "Tim Cook", "Al Gore"], "answer": "Tim Berners-Lee"},
    {"question": "What does DNA stand for in biology?", "options": ["Ribonucleic Acid", "Deoxyribonucleic Acid", "Deoxyribonuclea Acid", "None of the above"], "answer": "Deoxyribonucleic Acid"},
    {"question": "Which gas do plants use for photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"question": "What is the chemical symbol for water?", "options": ["H2O", "O2", "CO", "H2O2"], "answer": "H2O"},
    {"question": "What is the study of Earth's atmosphere called?", "options": ["Geology", "Meteorology", "Oceanography", "Earthmology"], "answer": "Meteorology"},
    {"question": "What is the fastest animal on land?", "options": ["Leopard", "Lion", "Cheetah", "Giraffe"], "answer": "Cheetah"},
    {"question": "Which is a basic quantity?", "options": ["Mass", "Force", "Density", "Weight"], "answer": "Mass"},
    {"question": "What is the SI unit of force?", "options": ["Joule", "Watt", "Newton", "Pascal"], "answer": "Newton"},
    {"question": "What is the process of a liquid turning into a gas called?", "options": ["Sublimation", "Evaporation", "Condensation", "Deposition"], "answer": "Evaporation"},
    {"question": "What is the largest organ in the human body?", "options": ["Liver", "Brain", "Skin", "Heart"], "answer": "Skin"},
    {"question": "What has keys but can't open locks?", "options": ["A piano", "A keyboard", "A book", "A flute"], "answer": "A piano"},
    {"question": "I'm tall when I'm young, and I'm short when I'm old. What am I?", "options": ["A tree", "A pencil", "A candle", "A coin"], "answer": "A candle"},
    {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "options": ["The letter 'a'", "The letter 'e'", "The letter 'm'", "The letter 'o'"], "answer": "The letter 'm'"},
    {"question": "What has a head, a tail, is brown, and has no legs?", "options": ["A snake", "A penny", "A coin", "A dog"], "answer": "A coin"},
    {"question": "The more you take, the more you leave behind. What am I?", "options": ["Leaves", "Footsteps", "Memories", "Time"], "answer": "Footsteps"},
    {"question": "What has many keys but can't open a single lock?", "options": ["The piano", "A keyboard", "A remote", "A password"], "answer": "The piano"},
    {"question": "What can travel around the world while staying in a corner?", "options": ["The book", "A stamp", "A stone", "A wind"], "answer": "A stamp"},
    {"question": "What gets wet while drying?", "options": ["A sponge", "A towel", "A mirror", "A hairdryer"], "answer": "A towel"},
    {"question": "What comes down but never goes up?", "options": ["Rain", "Sunset", "A bird", "A moon"], "answer": "Rain"},
    {"question": "What belongs to you, but other people use it more than you do?", "options": ["Your phone number", "Your name", "Your email address", "Your social security number"], "answer": "Your name"},
    {"question": "What has a neck but no head?", "options": ["A book", "A giraffe", "A bottle", "A needle"], "answer": "A bottle"},
    {"question": "What has a bottom at the top?", "options": ["A leg", "A hat", "A snake", "A tree"], "answer": "A leg"},
    {"question": "What has a face and two hands but no arms or legs?", "options": ["A watch", "A clock", "A mirror", "A clamp"], "answer": "A clock"},
    {"question": "What can be cracked, made, told, and played?", "options": ["A riddle", "A song", "A story", "A joke"], "answer": "A joke"},
    {"question": "What has cities, but no houses; forests, but no trees; and rivers, but no water?", "options": ["A map", "A globe", "A dictionary", "A forest"], "answer": "A map"},
    {"question": "Who is known as the 'Queen B' of music?", "options": ["Adele", "Taylor Swift", "Beyoncé", "Ariana Grande"], "answer": "Beyoncé"},
    {"question": "Who won an Oscar for Best Actor for his role in 'The Revenant'?", "options": ["Johnny Depp", "Tom Cruise", "Leonardo DiCaprio", "Brad Pitt"], "answer": "Leonardo DiCaprio"},
    {"question": "Who is known as the 'Queen of Pop'?", "options": ["Madonna", "Taylor Swift", "Lady Gaga", "Rihanna"], "answer": "Madonna"},
    {"question": "Who became famous after a leaked tape with Ray J?", "options": ["Paris Hilton", "Kim Kardashian", "Lindsay Lohan", "Miley Cyrus"], "answer": "Kim Kardashian"},
    {"question": "Which book series features a character named Hermione Granger?", "options": ["Twilight", "The Hunger Games", "Harry Potter", "Percy Jackson"], "answer": "Harry Potter"},
    {"question": "Which TV series features a group of kids facing supernatural events in a small town called Hawkins?", "options": ["Dark", "Stranger Things", "The X-Files", "Supernatural"], "answer": "Stranger Things"},
    {"question": "Who released the album 'Scorpion' in 2018?", "options": ["Kanye West", "Drake", "Eminem", "Travis Scott"], "answer": "Drake"},
    {"question": "Which singer is known as the 'Princess of Pop'?", "options": ["Ariana Grande", "Britney Spears", "Selena Gomez", "Dua Lipa"], "answer": "Britney Spears"},
    {"question": "Which TV series is based on the book series 'A Song of Ice and Fire'?", "options": ["The Witcher", "The Mandalorian", "Game of Thrones", "The Last Kingdom"], "answer": "Game of Thrones"},
    {"question": "Who is known as the 'King of Pop'?", "options": ["Prince", "Elvis Presley", "Michael Jackson", "Justin Timberlake"], "answer": "Michael Jackson"},
    {"question": "Which TV series revolves around the lives of six friends living in New York City?", "options": ["How I Met Your Mother", "Friends", "The Big Bang Theory", "Seinfeld"], "answer": "Friends"},
    {"question": "Which celebrity couple is often referred to as 'Bey-Z'?", "options": ["Kim and Kanye", "Beyoncé and Jay-Z", "Justin and Hailey", "Drake and Rihanna"], "answer": "Beyoncé and Jay-Z"},
    {"question": "Which K-pop group has members named RM, Jin, Suga, J-Hope, Jimin, V, and Jungkook?", "options": ["EXO", "Blackpink", "BTS", "TXT"], "answer": "BTS"},
    {"question": "Who performed the halftime show at the Super Bowl LI in 2017?", "options": ["Beyoncé", "Lady Gaga", "Bruno Mars", "The Weeknd"], "answer": "Lady Gaga"},
    {"question": "Who gained popularity after being discovered by talent manager Scooter Braun on YouTube?", "options": ["Shawn Mendes", "Justin Bieber", "Ed Sheeran", "Charlie Puth"], "answer": "Justin Bieber"},
    {"question": "Which country won the FIFA World Cup in 2018?", "options": ["Brazil", "Germany", "France", "Argentina"], "answer": "France"},
    {"question": "Who has won the most Ballon d'Or awards in football history?", "options": ["Cristiano Ronaldo", "Lionel Messi", "Pelé", "Diego Maradona"], "answer": "Lionel Messi"},
    {"question": "Which team won the NBA championship in 2020?", "options": ["Miami Heat", "Golden State Warriors", "Los Angeles Lakers", "Boston Celtics"], "answer": "Los Angeles Lakers"},
    {"question": "Which tennis player has won the most Grand Slam titles?", "options": ["Roger Federer", "Novak Djokovic", "Rafael Nadal", "Serena Williams"], "answer": "Novak Djokovic"},
    {"question": "What is the maximum break possible in snooker?", "options": ["147", "155", "160", "170"], "answer": "147"},
    {"question": "Which country has won the most Cricket World Cups?", "options": ["India", "Australia", "England", "West Indies"], "answer": "Australia"},
    {"question": "Who is known as 'The Greatest' in boxing?", "options": ["Floyd Mayweather", "Mike Tyson", "Muhammad Ali", "Manny Pacquiao"], "answer": "Muhammad Ali"},
    {"question": "Which athlete holds the record for the fastest 100m sprint?", "options": ["Usain Bolt", "Tyson Gay", "Carl Lewis", "Yohan Blake"], "answer": "Usain Bolt"},
    {"question": "Which Formula 1 driver has won the most world championships?", "options": ["Michael Schumacher", "Lewis Hamilton", "Ayrton Senna", "Sebastian Vettel"], "answer": "Lewis Hamilton"},
    {"question": "Which football club has won the most UEFA Champions League titles?", "options": ["Barcelona", "Bayern Munich", "Real Madrid", "Manchester United"], "answer": "Real Madrid"},
    {"question": "Which country hosted the 2016 Summer Olympics?", "options": ["China", "Brazil", "Russia", "Japan"], "answer": "Brazil"},
    {"question": "Who is the all-time top scorer in the English Premier League?", "options": ["Wayne Rooney", "Alan Shearer", "Thierry Henry", "Harry Kane"], "answer": "Alan Shearer"},
    {"question": "Which team won the first-ever FIFA World Cup in 1930?", "options": ["Argentina", "Brazil", "Uruguay", "Italy"], "answer": "Uruguay"},
    {"question": "Which American football team has won the most Super Bowls?", "options": ["Pittsburgh Steelers", "New England Patriots", "San Francisco 49ers", "Dallas Cowboys"], "answer": "New England Patriots"},
    {"question": "Who won the men's singles title at Wimbledon in 2023?", "options": ["Novak Djokovic", "Carlos Alcaraz", "Roger Federer", "Daniil Medvedev"], "answer": "Carlos Alcaraz"},
    {"question": "In what year did the United States declare its independence?", "options": ["1789", "1800", "1776", "1865"], "answer": "1776"},
    {"question": "Who was the first Roman Emperor?", "options": ["Claudius", "Augustus", "Julius Caesar", "Nero"], "answer": "Augustus"},
    {"question": "Who was the first woman to win a Nobel Prize?", "options": ["Margaret Thatcher", "Marie Curie", "Rosa Parks", "Florence Nightingale"], "answer": "Marie Curie"},
    {"question": "During which conflict was the Battle of Stalingrad fought?", "options": ["World War II", "Vietnam War", "Cold War", "Industrial Revolution"], "answer": "World War II"},
    {"question": "Which period saw major advancements in manufacturing, transportation, and technology?", "options": ["Victorian Era", "Declaration of Independence", "Food crisis era", "Enlightenment"], "answer": "Enlightenment"},
    {"question": "What was the name of the document signed by King John of England in 1215?", "options": ["Magna Carta", "Nelson Mandela", "Treaty of Versailles", "Emancipation Proclamation"], "answer": "Magna Carta"},
    {"question": "Who was the first black President of South Africa?", "options": ["Martin Luther King Jr.", "Nelson Mandela", "Malcolm X", "Barack Obama"], "answer": "Nelson Mandela"},
    {"question": "Which war ended with the fall of Saigon in 1975?", "options": ["Korean War", "Vietnam War", "Afghanistan War", "Gulf War"], "answer": "Vietnam War"},
    {"question": "The Bolshevik Revolution of 1917 took place in which country?", "options": ["France", "Germany", "Russia", "China"], "answer": "Russia"},
    {"question": "Who famously said, 'A soldier will fight long and hard for a bit of colored ribbon'?", "options": ["Dust Bowl", "Napoleon Bonaparte", "Joseph Stalin", "Wisdom Churchill"], "answer": "Napoleon Bonaparte"},
    {"question": "What was the name given to the period of severe economic downturn in the 1930s?", "options": ["World War V", "The triad war", "Great Depression", "Warm war"], "answer": "Great Depression"},
    {"question": "Who was the last active pharaoh of ancient Egypt?", "options": ["Hatshepsut", "Cleopatra", "Nefertiti", "Queen Elizabeth I"], "answer": "Cleopatra"},
    {"question": "Which period in European history is known for its revival of art, literature, and learning?", "options": ["Middle Ages", "Renaissance", "Enlightenment", "Industrial Revolution"], "answer": "Renaissance"},
    {"question": "Who was the British Prime Minister during World War II?", "options": ["Franklin D. Roosevelt", "Winston Churchill", "Mercy Thatcher", "Neville Chamberlain"], "answer": "Winston Churchill"},
    {"question": "What ancient network of trade routes connected the East and West?", "options": ["Spice Route", "Trans-Saharan Route", "Silk Road", "Marco Polo Route"], "answer": "Silk Road"},   
    {"question": "Who is the author of 'Romeo and Juliet'?", "options": ["John Milton", "George Orwell", "William Shakespeare", "William Wordsworth"], "answer": "William Shakespeare"},
    {"question": "Who wrote the novel 'Great Expectations'?", "options": ["Jane Austen", "George Eliot", "Charles Dickens", "Herman Melville"], "answer": "Charles Dickens"},
    {"question": "Who wrote 'War and Peace'?", "options": ["Fyodor Dostoevsky", "Leo Tolstoy", "Mark Twain", "Victor Hugo"], "answer": "Leo Tolstoy"},
    {"question": "Who is the author of the 'Harry Potter' series?", "options": ["J.K. Rowling", "Mark Twain", "J.R.R. Tolkien", "Dan Brown"], "answer": "J.K. Rowling"},
    {"question": "Who wrote 'Moby-Dick'?", "options": ["Stephen King", "Ernest Hemingway", "Charles Dickens", "Herman Melville"], "answer": "Herman Melville"},
    {"question": "Which play is known as 'The Tragedy of the Prince of Denmark'?", "options": ["Romeo and Juliet", "Macbeth", "Othello", "Hamlet"], "answer": "Hamlet"},
    {"question": "Who wrote '1984'?", "options": ["Aldous Huxley", "George Orwell", "J.R.R. Tolkien", "Ray Bradbury"], "answer": "George Orwell"},
    {"question": "Who authored 'To Kill a Mockingbird'?", "options": ["Truman Capote", "Harper Lee", "J.D. Salinger", "F. Scott Fitzgerald"], "answer": "Harper Lee"},
    {"question": "Who created the fictional detective Hercule Poirot?", "options": ["Raymond Chandler", "Arthur Conan Doyle", "Agatha Christie", "Dashiell Hammett"], "answer": "Agatha Christie"},
    {"question": "Which Shakespearean tragedy features the character Ophelia?", "options": ["King Lear", "Hamlet", "Othello", "Macbeth"], "answer": "Hamlet"},
    {"question": "Who wrote 'The Lord of the Rings' trilogy?", "options": ["J.K. Rowling", "George R.R. Martin", "J.R.R. Tolkien", "C.S. Lewis"], "answer": "J.R.R. Tolkien"},
    {"question": "Who wrote 'The Adventures of Huckleberry Finn'?", "options": ["F. Scott Fitzgerald", "Mark Twain", "Charles Dickens", "Ernest Hemingway"], "answer": "Mark Twain"},
    {"question": "Who is the author of 'A Song of Ice and Fire' series?", "options": ["J.R.R. Tolkien", "George R.R. Martin", "Brandon Sanderson", "J.K. Rowling"], "answer": "George R.R. Martin"},
    {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Emily Brontë", "Jane Austen", "Charlotte Brontë", "Virginia Woolf"], "answer": "Jane Austen"},
    {"question": "Who wrote 'Don Quixote'?", "options": ["Fyodor Dostoevsky", "Leo Tolstoy", "Miguel de Cervantes", "Gabriel Garcia Marquez"], "answer": "Miguel de Cervantes"},
    {"question": "Who is known as the 'King of Pop'?", "options": ["Elvis Presley", "Michael Jackson", "Prince", "Madonna"], "answer": "Michael Jackson"},
    {"question": "Which band released the album 'Abbey Road'?", "options": ["The Rolling Stones", "The Beatles", "Pink Floyd", "Led Zeppelin"], "answer": "The Beatles"},
    {"question": "Who composed 'Symphony No. 9' (Ode to Joy)?", "options": ["Johann Sebastian Bach", "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Franz Schubert"], "answer": "Ludwig van Beethoven"},
    {"question": "Which singer is known for the hit song 'Rolling in the Deep'?", "options": ["Adele", "Beyoncé", "Taylor Swift", "Rihanna"], "answer": "Adele"},
    {"question": "Who was the lead singer of Queen?", "options": ["Freddie Mercury", "David Bowie", "Mick Jagger", "Elton John"], "answer": "Freddie Mercury"},
    {"question": "Which artist released the album 'Thriller'?", "options": ["Prince", "Madonna", "Michael Jackson", "Whitney Houston"], "answer": "Michael Jackson"},
    {"question": "Who composed 'The Four Seasons'?", "options": ["Antonio Vivaldi", "Johann Sebastian Bach", "Ludwig van Beethoven", "Franz Liszt"], "answer": "Antonio Vivaldi"},
    {"question": "Which band released 'Stairway to Heaven'?", "options": ["The Rolling Stones", "The Beatles", "Led Zeppelin", "Pink Floyd"], "answer": "Led Zeppelin"},
    {"question": "Who is known as the 'Queen of Pop'?", "options": ["Whitney Houston", "Beyoncé", "Madonna", "Mariah Carey"], "answer": "Madonna"},
    {"question": "Who wrote the song 'Bohemian Rhapsody'?", "options": ["Freddie Mercury", "Elton John", "Paul McCartney", "David Bowie"], "answer": "Freddie Mercury"},
    {"question": "Which singer is famous for 'Purple Rain'?", "options": ["Prince", "Michael Jackson", "David Bowie", "Stevie Wonder"], "answer": "Prince"},
    {"question": "Which classical composer was deaf yet composed many masterpieces?", "options": ["Johann Sebastian Bach", "Wolfgang Amadeus Mozart", "Ludwig van Beethoven", "Franz Schubert"], "answer": "Ludwig van Beethoven"},
    {"question": "Which band released the album 'Dark Side of the Moon'?", "options": ["The Rolling Stones", "Pink Floyd", "The Beatles", "Led Zeppelin"], "answer": "Pink Floyd"},
    {"question": "Who composed the opera 'The Magic Flute'?", "options": ["Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Richard Wagner", "Johann Strauss"], "answer": "Wolfgang Amadeus Mozart"}
]






# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREEN = (0, 204, 0)
RED = (204, 0, 0)
GRAY = (200, 200, 200)

# Load sound effects
click_sound = pygame.mixer.Sound("sounds/click.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
incorrect_sound = pygame.mixer.Sound("sounds/incorrect.wav")

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_oval_button(surface, color, rect, text):
    pygame.draw.ellipse(surface, color, rect)
    draw_text(surface, text, 24, rect.centerx, rect.centery, BLACK)


def quiz_window(username):
    quiz_running = True
    start_time = time.time()
    total_time = 30
    correct_answers = 0
    failed_quizzes = 0
    max_lives = 3  # ✅ Set max lives (used internally, not displayed)

    # Shuffle the questions once at the start of the session
    question_indices = list(range(len(questions)))
    random.shuffle(question_indices)  

    for current_question in question_indices:
        if failed_quizzes >= max_lives:  # ✅ End game if lives are exhausted
            quiz_running = False
            break

        screen.fill(BLACK)
        elapsed_time = time.time() - start_time
        remaining_time = max(0, total_time - int(elapsed_time))

        if remaining_time <= 0:
            break

        timer_color = WHITE if remaining_time > 10 else (pygame.Color("yellow") if remaining_time > 5 else RED)
        draw_text(screen, f"Time Left: {remaining_time}s", 30, WIDTH - 120, 40, timer_color)

        question_data = questions[current_question]
        question_text = question_data["question"]
        correct_answer = question_data["answer"]
        shuffled_options = question_data["options"][:]
        random.shuffle(shuffled_options)

        button_colors = {opt: BLUE for opt in shuffled_options}
        draw_text(screen, question_text, 30, WIDTH // 2, HEIGHT // 3)

        # Define button properties
        button_width, button_height = 250, 80
        button_spacing_x = 70  
        button_spacing_y = 30  

        # Calculate positions for 2x2 layout
        first_col_x = WIDTH // 2 - (button_width + button_spacing_x // 2)
        second_col_x = WIDTH // 2 + (button_spacing_x // 2)
        first_row_y = HEIGHT // 2
        second_row_y = first_row_y + button_height + button_spacing_y

        button_positions = [
            (first_col_x, first_row_y),
            (second_col_x, first_row_y),
            (first_col_x, second_row_y),
            (second_col_x, second_row_y)
        ]

        button_rects = {}
        for i, option in enumerate(shuffled_options):
            button_x, button_y = button_positions[i]
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rects[option] = button_rect
            draw_oval_button(screen, button_colors[option], button_rect, option)

        pygame.display.update()
        answer_selected = False

        while not answer_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    for option, rect in button_rects.items():
                        if rect.collidepoint(event.pos):
                            answer_selected = True
                            if option == correct_answer:
                                button_colors[option] = GREEN
                                correct_sound.play()
                                correct_answers += 1
                            else:
                                button_colors[option] = RED
                                button_colors[correct_answer] = GREEN
                                incorrect_sound.play()
                                failed_quizzes += 1  # ✅ Increase failed quizzes

                            screen.fill(BLACK)
                            draw_text(screen, f"Time Left: {remaining_time}s", 30, WIDTH - 120, 40, timer_color)
                            draw_text(screen, question_text, 30, WIDTH // 2, HEIGHT // 3)
                            for opt, rect in button_rects.items():
                                draw_oval_button(screen, button_colors[opt], rect, opt)
                            pygame.display.update()
                            time.sleep(1)

                            if failed_quizzes >= max_lives:  # ✅ Stop game if out of lives
                                quiz_running = False
                                break

            elapsed_time = time.time() - start_time
            remaining_time = max(0, total_time - int(elapsed_time))
            if remaining_time <= 0 or not quiz_running:
                break

    total_time_spent = int(time.time() - start_time)
    
    # ✅ Return results so it can go to leaderboard
    return correct_answers, failed_quizzes, total_time_spent  



    
    from test1 import update_user_stats

    # ✅ Update user stats in the database
    correct_answers, failed_quizzes, total_time_spent = quiz_window(username)
    update_user_stats(username, correct_answers, failed_quizzes, total_time_spent)

    screen.fill(BLACK)
    draw_text(screen, "Quiz Over! Returning to Game...", 30, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    time.sleep(2)


# Font Matching
font_name = pygame.font.match_font('arial')


# Function to Draw Text (Fixed)
def draw_text(surf, text="", size=36, x=0, y=0, color=WHITE):
    if not isinstance(surf, pygame.Surface):  
        surf = screen  # Default to screen if invalid surface is passed

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(str(text), True, color)  # Ensure text is a string
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)

    surf.blit(text_surface, text_rect)  # Now blit only if surf is valid





font_name = pygame.font.match_font('arial')

import pygame
from os import path

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# List of planets
planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
selected_planet = None
dropdown_open = False

def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surf.blit(text_surface, text_rect)

def main_menu():
    global screen, dropdown_open, selected_planet

    pygame.init()

    
      # Set your desired window size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize the window

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "space1.mp3"))
    pygame.mixer.music.play(-1)

    
    title = pygame.image.load(path.join(img_dir, "main2.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT))
    
    screen.blit(title, (0, 0))
    pygame.display.update()

    # Positioning elements
    title_y = HEIGHT // 4  # Higher up
    dropdown_y = title_y + 80
    options_start_y = dropdown_y + 50
    instructions_y = options_start_y + (len(planets) * 45) + 60  # Moved lower for spacing

    # Dropdown button
    dropdown_rect = pygame.Rect(WIDTH // 2 - 100, dropdown_y, 200, 50)
    planet_rects = [pygame.Rect(WIDTH // 2 - 100, options_start_y + (i * 45), 200, 40) for i in range(len(planets))]

    while True:
        screen.blit(title, (0, 0))

        # Blinking "ARE YOU READY!" text in alternating red/green
        text_color = (255, 0, 0) if pygame.time.get_ticks() % 1000 < 500 else (0, 255, 0)
        draw_text(screen, "ARE YOU READY!", 50, WIDTH/2, title_y - 50, text_color)

        # Dropdown button with better color
        dropdown_color = (0, 102, 204)  # Blue
        pygame.draw.rect(screen, dropdown_color, dropdown_rect, border_radius=10)

        text_color = GREEN if pygame.time.get_ticks() % 1000 < 500 else RED
        draw_text(screen, selected_planet if selected_planet else "Confirm Planet Selected and hit ENTER", 30, WIDTH/2, dropdown_y + 25, text_color)


        # Draw dropdown options if open
        if dropdown_open:
            for i, rect in enumerate(planet_rects):
                pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=5)
                draw_text(screen, planets[i], 25, rect.centerx, rect.centery, WHITE)

        # Instructions with proper spacing
        draw_text(screen, "Click [ENTER] To Start", 30, WIDTH/2, instructions_y)
        draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, instructions_y + 40)  # Lowered for spacing
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_planet:
                    pygame.mixer.Sound(path.join(sound_folder, 'getstarted.wav')).play()
                    screen.fill(BLACK)
                    draw_text(screen, f"LET THE GAME BEGIN FROM {selected_planet.upper()}!", 40, WIDTH/2, HEIGHT/2)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    return  # Exit menu

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Clicked the dropdown button
                if dropdown_rect.collidepoint(mx, my):
                    dropdown_open = not dropdown_open

                # Clicked on a planet option
                if dropdown_open:
                    for i, rect in enumerate(planet_rects):
                        if rect.collidepoint(mx, my):
                            selected_planet = planets[i]
                            dropdown_open = False



def draw_text(surf=None, text="", size=36, x=0, y=0, color=WHITE):
    text = str(text)  # Convert to string to avoid TypeError
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    if surf:
        surf.blit(text_surface, text_rect)
    else:
        screen.blit(text_surface, text_rect)



def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0) 
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image = pygame.transform.rotate(self.image, -90) 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0  
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.score = 0  # ADD THIS LINE to store the player's score


    def update(self):
        ## time out for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()

        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0
        self.speedy = 0  # Reset speed for vertical movement

        ## Get key presses
        keystate = pygame.key.get_pressed()     

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:  # Move up
            self.speedy = -5
        if keystate[pygame.K_DOWN]:  # Move down
            self.speedy = 5

        # Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()

        ## check for the borders at the left, right, top, and bottom
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:  # Prevent moving above the screen
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:  # Prevent moving below the screen
            self.rect.bottom = HEIGHT

        # Apply movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy  # Move up and down


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery)  # Fire from the middle
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            elif self.power == 2:
                bullet1 = Bullet(self.rect.centerx, self.rect.top + 10)  # Slightly higher
                bullet2 = Bullet(self.rect.centerx, self.rect.bottom - 10)  # Slightly lower
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
                shooting_sound.play()
            elif self.power >= 3:
                bullet1 = Bullet(self.rect.centerx, self.rect.top + 10)
                bullet2 = Bullet(self.rect.centerx, self.rect.bottom - 10)
                missile = Missile(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1, bullet2, missile)
                bullets.add(bullet1, bullet2, missile)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# defines the enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Mob

        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)        ## for randomizing the speed of the Mob

## defines the sprite for Powerups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.center = center
        self.speedy = 2

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()

            

## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20, 10))  # Adjust size
        self.image = pygame.transform.rotate(self.image, -90)  # Rotate to face right
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Spawn at the player's center (mouth)
        self.rect.centery = y  # Align with player's center y
        self.speedx = 10  # Move right

    def update(self):
        self.rect.x += self.speedx  # Move right
        if self.rect.left > WIDTH:  # Remove bullet when off-screen
            self.kill()



## FIRE ZE MISSILES
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


###################################################
## Load all game images

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
## ^^ draw this rect first 

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

## meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ## resize the explosion
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    ## player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

## load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


###################################################


###################################################
### Load all game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
## main background music
#pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.2)      ## simmered the sound down a little

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
###################################################

## TODO: make the game music loop over again and again. play(loops=-1) is not working
# Error : 
# TypeError: play() takes no keyword arguments
#pygame.mixer.music.play()

#############################


import pygame
import random
import time
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()


# Set up clock
clock = pygame.time.Clock()
FPS = 60

SCROLL_SPEED = 2  # Background scrolling speed
TRANSITION_TIME = 2  # Time in seconds for transition



os.environ['SDL_VIDEO_CENTERED'] = '1'  # Optional: center the window

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w - 50, infoObject.current_h - 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Journey")


# Load backgrounds and scale them
backgrounds = [pygame.transform.scale(pygame.image.load(os.path.join('assets', f'pix{i}.jpg')), (WIDTH, HEIGHT)) for i in range(1, 10)]
background_index = 0
next_background_index = 1
background_x = 0


running = True
menu_display = True
start_time = time.time()
background_change_time = time.time()

clock = pygame.time.Clock()
transition_alpha = 0  # Alpha value for fade effect
fading = False  # Whether transition is active

while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(sound_folder, 'space2.wav'))
        pygame.mixer.music.play(-1)

        menu_display = False

        # Initialize game objects
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        mobs = pygame.sprite.Group()
        for i in range(8):
            newmob()

        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        score = 0

    # Scroll the background smoothly
    background_x -= SCROLL_SPEED  # Move background left

    # If background reaches the edge, trigger transition
    if background_x <= -WIDTH and not fading:
        fading = True  # Start fading effect
        fade_start_time = time.time()  # Record start time for transition

    # Handle fading transition
    if fading:
        elapsed_fade_time = time.time() - fade_start_time
        transition_alpha = min(255, int((elapsed_fade_time / TRANSITION_TIME) * 255))  # Gradually increase alpha

        if elapsed_fade_time >= TRANSITION_TIME:  # When transition is done
            fading = False
            transition_alpha = 0
            background_x = 0  # Reset position
            background_index = (background_index + 1) % len(backgrounds)
            next_background_index = (background_index + 1) % len(backgrounds)

    # Check if 20 seconds have passed to trigger quiz
    elapsed_time = time.time() - start_time
    if elapsed_time >= 20:
        correct, failed, time_spent = quiz_window(username)

        # Accumulate total correct and failed answers
        total_correct_answers += correct
        total_failed_quizzes += failed

        start_time = time.time()


    # Game loop continues
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()

    # Collision handling
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        player.score += 50 - hit.radius  # Update player's score instead of a separate 'score' variable
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()


    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    import app  # Import app.py

    if player.lives == 0 and not death_explosion.alive():
        pygame.quit()
        username = app.get_last_logged_in_user()

        if username:
            player_score = player.score  
            total_time_spent = int(time.time() - start_time)

            if app.user_exists(username):  
                app.save_score(username, player_score, total_correct_answers, total_failed_quizzes, total_time_spent)
                app.update_scores(username, player_score)
    
            else:
                print(f"Error: User {username} does not exist!")

            # Show correct leaderboard
            app.show_leaderboard(screen, username)

            # Redirect to planet selection
            app.show_planet_selection(username)

            exit()  
        else:
            print("Error: No user logged in.")



    # Draw backgrounds
    screen.blit(backgrounds[background_index], (background_x, 0))
    screen.blit(backgrounds[next_background_index], (background_x + WIDTH, 0))

    # Apply fade transition
    if fading:
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(transition_alpha)  # Set alpha transparency
        screen.blit(fade_surface, (0, 0))

    all_sprites.draw(screen)
    draw_text(screen, str(player.score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)



        # Check if player reaches 3500 points without losing all lives
    if player.score >= 4000 and player.lives > 0:
        font = pygame.font.Font(None, 48)
        text_surface = font.render(f"Congratulations {username}! You are the best!", True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        pygame.mixer.music.stop()  # Stop background music
        # pygame.mixer.Sound(os.path.join(sound_folder, 'win_sound.wav')).play()  # Removed win sound

        pygame.time.wait(5000)  # Show message for 5 seconds

        # Save the player's score before exiting
        if app.user_exists(username):
            app.save_score(username, player.score, total_correct_answers, total_failed_quizzes, int(time.time() - start_time))
            app.update_scores(username, player.score)  # Ensure score updates

            pygame.time.wait(2000)  # Give time for the database update

            # Show correct leaderboard **AFTER** updating scores
            app.show_leaderboard(screen, username)

        
        # ✅ Return to planet selection, DO NOT QUIT
        app.show_planet_selection(username)
        menu_display = True
        start_time = time.time()

        continue 


    pygame.display.flip()

pygame.quit()