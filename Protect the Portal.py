import tkinter as tk
import random
import math

# Global variables for enemy behavior
shoot_timer = 0
float_offset = 0
weapon = "gun"
spawn_timer = 0

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

def make_enemy_sprite():
    # Simple enemy pattern (Eye of Ra)
    pattern = [
"00000111100000",
"00011111111000",
"00112222221100",
"01122333322110",
"11223333332211",
"12233322233321",
"12333222223321",
"12332222223321",
"12333222233321",
"12233322233321",
"11223333333211",
"01122333332210",
"00112222221100",
"00011111111000",
"00001144110000",
"00011400411000",
"00010000401000",
"00100000400100",
"00000000400000",
    ]
    h = len(pattern)
    w = len(pattern[0])
    scale = 2
    img = tk.PhotoImage(width=w*scale, height=h*scale)
    for y in range(h):
        for x in range(w):
            char = pattern[y][x]
            if char != "0":
                color = {
                    "1": "black",
                    "2": "blue",
                    "3": "red",
                    "4": "green"
                }.get(char, "black")
                for dy in range(scale):
                    for dx in range(scale):
                        img.put(color, [x*scale + dx, y*scale + dy])   
    return img

enemy_img = make_enemy_sprite()
enemies = []
enemy = canvas.create_image(400, 100, image=enemy_img)
enemies.append(enemy)

weapon_text = canvas.create_text(100, 550, text=f"Weapon: {weapon}", fill="white", font=("Arial", 12))


def make_portal_sprite():
    # Simple portal pattern
    pattern = [
"000000111111000000000",
"000011777777110000000",
"000177222222771000000",
"001772333333277100000",
"017233444444332710000",
"017234555555432710000",
"172345555555543271000",
"172345566665543271000",
"123456668866654321000",
"123456688886654321000",
"123456688886654321000",
"123456668866654321000",
"172345566665543271000",
"172345555555543271000",
"017234555555432710000",
"017233444444332710000",
"001772333333277100000",
"000177222222771000000",
"000011777777110000000",
"000000119991000000000",
"000000001110000000000"
    ]
    h = len(pattern)
    w = len(pattern[0])
    scale = 2
    img = tk.PhotoImage(width=w*scale, height=h*scale)
    for y in range(h):
        for x in range(w):
            char = pattern[y][x]
            if char != "0":
                color = {
                    "1": "black",
                    "2": "#4B0082",
                    "3": "#8A2BE2",
                    "4": "#00FFFF",
                    "5": "#001F54",
                    "6": "#FF2F92",
                    "7": "#6E6E6E",
                    "8": "#66D9FF",
                    "9": "#D4AF37"

                }.get(char, "black")
                for dy in range(scale):
                    for dx in range(scale):
                        img.put(color, [x*scale + dx, y*scale + dy])
    
    return img

portal_img = make_portal_sprite()
portal = canvas.create_image(400, 300, image=portal_img)
portal_health = 100
portal_health_text = canvas.create_text(400, 50, text=f"Portal Health: {portal_health}", fill="white", font=("Arial", 16))

round_number = 1
round_timer = 30 * 60  # 30 seconds at ~60 FPS
round_text = canvas.create_text(400, 20, text=f"Round: {round_number}", fill="white", font=("Arial", 12))
timer_text = canvas.create_text(400, 35, text=f"Time: {round_timer // 60}", fill="white", font=("Arial", 12))

# Weapon functions
def switch_weapon(event):
    global weapon
    weapon = "sword" if weapon == "gun" else "gun"
    canvas.itemconfig(weapon_text, text=f"Weapon: {weapon}")

def shoot(event):
    global enemies
    player_coords = canvas.coords(player)
    if weapon == "gun":
        # Shoot bullet upwards
        bullet = canvas.create_oval(player_coords[0]-2, player_coords[1]-2, player_coords[0]+2, player_coords[1]+2, fill="blue")
        def move_bullet():
            canvas.move(bullet, 0, -5)
            bullet_coords = canvas.coords(bullet)
            # Check collision with enemies
            for e in enemies[:]:  # Copy list to avoid modification during iteration
                enemy_coords = canvas.coords(e)
                if (abs(bullet_coords[0] - enemy_coords[0]) < 20 and 
                    abs(bullet_coords[1] - enemy_coords[1]) < 20):
                    canvas.delete(e)
                    enemies.remove(e)
                    canvas.delete(bullet)
                    return
            if bullet_coords[1] > 0:
                root.after(16, move_bullet)
            else:
                canvas.delete(bullet)
        move_bullet()
    elif weapon == "sword":
        # Melee attack
        for e in enemies[:]:
            enemy_coords = canvas.coords(e)
            if (abs(player_coords[0] - enemy_coords[0]) < 50 and 
                abs(player_coords[1] - enemy_coords[1]) < 50):
                canvas.delete(e)
                enemies.remove(e)

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
root.bind('s', switch_weapon)
root.bind('<space>', shoot)

# Basic game loop (placeholder for future game logic)
def game_loop():
    global round_timer, round_number, shoot_timer, float_offset, portal_health, spawn_timer
    # Spawn enemies gradually
    spawn_timer += 1
    if spawn_timer >= 300:  # Spawn every 5 seconds
        new_enemy = canvas.create_image(random.randint(100, 700), 100, image=enemy_img)
        enemies.append(new_enemy)
        spawn_timer = 0
    
    round_timer -= 1
    canvas.itemconfig(timer_text, text=f"Time: {round_timer // 60}")
    if round_timer <= 0:
        round_number += 1
        canvas.itemconfig(round_text, text=f"Round: {round_number}")
        if round_number > 15:
            # Win condition
            win_text = canvas.create_text(400, 300, text="You Win!", fill="green", font=("Arial", 24))
            root.after(2000, root.quit)
            return
        else:
            round_timer = 30 * 60
    
    # Enemy behavior: floats slowly, stops at mid-range, shoots beams at the portal
    float_offset += 0.05
    for e in enemies:
        enemy_coords = canvas.coords(e)
        dx = 1 * math.sin(float_offset)  # Horizontal floating
        dy = 0.5 if enemy_coords[1] < 250 else 0  # Vertical movement until mid-range
        canvas.move(e, dx, dy)
    
    shoot_timer += 1
    if shoot_timer >= 60:  # Shoot every ~1 second
        if enemies:  # Only shoot and damage if there are enemies
            for e in enemies:
                enemy_coords = canvas.coords(e)
                portal_coords = canvas.coords(portal)
                # Create a beam (line) from enemy to portal
                beam = canvas.create_line(enemy_coords[0], enemy_coords[1], portal_coords[0], portal_coords[1], fill="yellow", width=3)
                # Remove the beam after 0.5 seconds
                root.after(500, lambda b=beam: canvas.delete(b))
            # Damage portal once per shot
            portal_health -= 1
            canvas.itemconfig(portal_health_text, text=f"Portal Health: {portal_health}")
            if portal_health <= 0:
                lose_text = canvas.create_text(400, 300, text="Game Over!", fill="red", font=("Arial", 24))
                root.after(2000, root.quit)
                return
        shoot_timer = 0
    
    root.after(16, game_loop)  # ~60 FPS

# Start the game loop
root.after(16, game_loop)

# Start the Tkinter main loop
root.mainloop()