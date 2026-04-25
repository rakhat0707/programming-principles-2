# Practice 11 — Pygame Projects (Racer, Snake, Paint)

## Objective
This practice focuses on extending previous Pygame projects by adding advanced game logic, random generation, and geometric drawing tools.

---

## Projects Overview

### 1. Racer
A simple racing game where the player avoids enemies and collects coins.

#### Features
- Player movement (left/right)
- Enemy cars moving downwards
- Randomly generated coins with different weights:
  - Yellow → 1 point
  - Orange → 2 points
  - Purple → 5 points
- Coin counter displayed on screen
- Enemy speed increases when player collects coins
- Collision detection (Game Over)

---

### 2. Snake
Classic snake game with extended mechanics.

#### Features
- Snake movement with arrow keys
- Collision detection:
  - Wall collision
  - Self collision
- Random food generation with different weights:
  - Red → 1 point
  - Orange → 2 points
  - Yellow → 5 points
- Food disappears after a certain time (timer)
- Score system

---

### 3. Paint
Drawing application using Pygame.

#### Features
- Free drawing mode
- Shape drawing:
  - Rectangle
  - Circle
  - Square
  - Right triangle
  - Equilateral triangle
  - Rhombus
- Mouse interaction for drawing
- Keyboard controls to switch modes

---

## Controls

### Racer
- ⬅️ Left Arrow — move left  
- ➡️ Right Arrow — move right  

---

### Snake
- ⬅️ ➡️ ⬆️ ⬇️ — movement  

---

### Paint
- P — draw  
- R — rectangle  
- C — circle  
- Q — square  
- T — right triangle  
- Y — equilateral triangle  
- U — rhombus  

---

## How to Run

### Racer
```bash
cd Practice11/Racer
python main.py