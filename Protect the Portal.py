import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Protect the Portal")

# Create canvas with space-like background (black)
canvas = tk.Canvas(root, width=800, height=600, bg='black')
canvas.pack()

# Add stars to create a space-like background
stars = []
for _ in range(100):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    star = canvas.create_oval(x, y, x+2, y+2, fill='white')
    stars.append(star)

# Create a pixel-art sprite for enemy aliens
def make_player_sprite():
    # Character pattern: '1' = colored pixel, '0' = transparent
    pattern = [
"0000000004000000000",
"0000000013100000000",
"0000000432340000000",
"0000001113111000000",
"0000011114111100000",
"0000111111111110000",
"0000011111111100000",
"0000001111111000000",
"0000001111111000000",
"0011111111111111100",
"0011111111111111100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0011101111111011100",
"0001001111111001000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000001110111000000",
"0000000100010000000",
    ]
    h = len(pattern)  # Height of sprite (number of rows)
    w = len(pattern[0])  # Width of sprite (characters per row)
    scale = 2  # Make the sprite bigger
    img = tk.PhotoImage(width=w*scale, height=h*scale)  # Create blank PhotoImage canvas

    # Paint pixels based on pattern values, scaled up
    for y in range(h):
        for x in range(w):
            char = pattern[y][x]
            if char != "0":
                color = {
                    "1": "cyan",
                    "2": "white",
                    "3": "orange",
                    "4": "purple"
                }.get(char, "black")
                # Fill the scaled block
                for dy in range(scale):
                    for dx in range(scale):
                        img.put(color, [x*scale + dx, y*scale + dy])

    return img

# Create the player sprite
player_img = make_player_sprite()
player = canvas.create_image(400, 550, image=player_img)

# Player movement functions
def move_left(event):
    x, y = canvas.coords(player)
    if x > 20:  # Keep within left boundary
        canvas.move(player, -10, 0)

def move_right(event):
    x, y = canvas.coords(player)
    if x < 780:  # Keep within right boundary
        canvas.move(player, 10, 0)

def move_up(event):
    x, y = canvas.coords(player)
    if y > 34:  # Keep within top boundary
        canvas.move(player, 0, -10)

def move_down(event):
    x, y = canvas.coords(player)
    if y < 566:  # Keep within bottom boundary
        canvas.move(player, 0, 10)

# Bind keys for movement
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<Up>', move_up)
root.bind('<Down>', move_down)

# Basic game loop (placeholder for future game logic)
def game_loop():
    # For now, just keep the loop running
    # Future: add enemy movement, collision detection, etc.
    root.after(16, game_loop)  # ~60 FPS

# Start the game loop
root.after(16, game_loop)

# Start the Tkinter main loop
root.mainloop()