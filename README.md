# 🚀 Comic Travel - Space Adventure Game  

## 📝 Overview  
**Comic Travel** is an exciting **space adventure game** built with **Python and Pygame**, where players navigate through space, battle enemies, and answer quizzes to progress. The game features smooth background transitions, a scoring system, power-ups, and an interactive leaderboard.  

---

## 🎮 Gameplay  

### 🎯 Objective  
Survive in space, defeat enemies, and score points while answering quizzes to boost your knowledge.  

### 🎮 Controls  
- **⬆️⬇️⬅️➡️ Arrow Keys** - Move the player spaceship  
- **Spacebar** - Fire bullets  
- **ESC** - Quit the game  

### 🏆 Scoring System  
- Defeat enemies to earn points  
- Reach **3500 points** to win  
- Answer quizzes to improve your ranking  

### ⚡ Power-ups  
- Shields & health boosts  
- Special abilities to enhance your spaceship  

---

## 🏆 Leaderboard  
- The game records high scores and quiz performance.  
- The leaderboard is stored in a **SQLite database (`myusers.db`)**.  
- You can reset the leaderboard using the following script:  

```python
import sqlite3

conn = sqlite3.connect("myusers.db")  
c = conn.cursor()
c.execute("DELETE FROM users")  
conn.commit()
conn.close()

print("Leaderboard wiped successfully!")
