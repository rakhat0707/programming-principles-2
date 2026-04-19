# Snake Game (Pygame)

## Description
This project is a classic Snake game implemented using Python and Pygame.

---

## Features
- Snake movement using arrow keys
- Collision detection:
  - Wall collision (game over)
  - Self collision (game over)
- Random food generation (not on snake body)
- Score system
- Level system
- Increasing speed with each level

---

## Controls
- ⬅️ Left Arrow — move left
- ➡️ Right Arrow — move right
- ⬆️ Up Arrow — move up
- ⬇️ Down Arrow — move down

---

## Game Logic
- Snake grows when it eats food
- Score increases by 1 for each food
- Every 4 points → level increases
- Speed increases with each level

---

## How to Run

```bash
cd Practice10/Snake
python main.py