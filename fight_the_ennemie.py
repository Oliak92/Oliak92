import tkinter as tk
import random

# Configure the window to be fullscreen
fenetre = tk.Tk()
fenetre.title("Fight the Enemy")
fenetre.attributes("-fullscreen", True)

# Get screen size to adapt game dimensions
screen_width = fenetre.winfo_screenwidth()
screen_height = fenetre.winfo_screenheight()

# Initialize the main canvas
canvas = tk.Canvas(fenetre, width=screen_width, height=screen_height, bg="sky blue")
canvas.pack()

# Initialize game variables
player = None
projectiles = []
enemies = []
lives = 3
enemies_remaining = 10  # Initial number of enemies to defeat
enemy_speed = 28  # Fixed speed of enemies (quadrupled)

# Display lives and remaining enemies
lives_text = None
enemies_text = None

# Function to start the game
def start_game():
    global player, lives_text, enemies_text, lives, enemies_remaining, projectiles, enemies
    # Reset game variables
    lives = 3
    enemies_remaining = 10
    projectiles.clear()
    enemies.clear()

    # Clear all elements from the canvas
    canvas.delete("all")
    
    # Display the player and HUD
    player = canvas.create_rectangle(50, screen_height // 2 - 25, 100, screen_height // 2 + 25, fill="blue")
    lives_text = canvas.create_text(screen_width - 100, 30, text=f"Lives: {lives}", font=("Arial", 16), fill="black")
    enemies_text = canvas.create_text(screen_width - 100, 60, text=f"Enemies remaining: {enemies_remaining}", font=("Arial", 16), fill="black")
    
    create_enemy()  # Create the first enemy
    fenetre.bind("<Up>", move_player)
    fenetre.bind("<Down>", move_player)
    fenetre.bind("<space>", lambda event: shoot())
    move_enemy()
    check_collision()

# Function to show instructions
def show_instructions():
    instructions = "Comment jouer :\n\n" \
                   "1. Utilisez les flèches pour vous déplacer.\n" \
                   "2. Appuyez sur la barre d'espace pour tirer.\n" \
                   "3. Évitez les ennemis et essayez de les détruire.\n" \
                   "4. Vous avez 3 vies.\n\n" \
                   "Amusez-vous bien !"
    canvas.delete("all")  # Clear the canvas for instructions
    canvas.create_text(screen_width // 2, screen_height // 2 - 50, text=instructions, font=("Arial", 24), fill="black")
    
    # Button to return to the start screen
    back_button = tk.Button(fenetre, text="Retour", font=("Arial", 24), command=start_screen)
    back_button_window = canvas.create_window(screen_width // 2, screen_height // 2 + 50, window=back_button)

# Start screen
def start_screen():
    # Game title
    canvas.create_text(screen_width // 2, screen_height // 2 - 50, text="Fight the Enemy", font=("Arial", 48), fill="red", tags="start_screen")
    # Button to start
    start_button = tk.Button(fenetre, text="Start", font=("Arial", 24), command=start_game)
    start_button_window = canvas.create_window(screen_width // 2, screen_height // 2 + 50, window=start_button, tags="start_screen")
    
    # Button to show instructions
    instructions_button = tk.Button(fenetre, text="Instructions", font=("Arial", 24), command=show_instructions)
    instructions_button_window = canvas.create_window(screen_width // 2, screen_height // 2 + 100, window=instructions_button, tags="start_screen")

# Function to move the player
def move_player(event):
    if event.keysym == "Up" and canvas.coords(player)[1] > 0:
        canvas.move(player, 0, -20)
    elif event.keysym == "Down" and canvas.coords(player)[3] < screen_height:
        canvas.move(player, 0, 20)

# Function to shoot
def shoot():
    x, y1, x2, y2 = canvas.coords(player)
    projectile = canvas.create_rectangle(x2, (y1 + y2) / 2 - 5, x2 + 20, (y1 + y2) / 2 + 5, fill="yellow")
    projectiles.append(projectile)
    move_projectile()

# Function to move projectiles
def move_projectile():
    for projectile in projectiles:
        canvas.move(projectile, 20, 0)
        if canvas.coords(projectile)[0] > screen_width:
            canvas.delete(projectile)
            projectiles.remove(projectile)
    fenetre.after(50, move_projectile)

# Function to create a new enemy
def create_enemy():
    global enemies_remaining
    y = random.randint(0, screen_height - 50)
    enemy = canvas.create_rectangle(screen_width - 50, y, screen_width, y + 50, fill="red")
    enemies.append(enemy)
    enemies_remaining -= 1
    canvas.itemconfig(enemies_text, text=f"Enemies remaining: {enemies_remaining}")

# Function to move enemies
def move_enemy():
    global lives
    for enemy in enemies:
        canvas.move(enemy, -enemy_speed, 0)
        # If an enemy exceeds the player, it loses a life and creates a new enemy
        if canvas.coords(enemy)[2] < 0:
            canvas.delete(enemy)
            enemies.remove(enemy)
            lives -= 1
            canvas.itemconfig(lives_text, text=f"Lives: {lives}")
            if lives > 0:  # Create a new enemy if the player has remaining lives
                create_enemy()
            if lives <= 0:
                end_screen("Game Over")
                return  # Exit the loop to avoid further movements
    if lives > 0:
        fenetre.after(100, move_enemy)

# Collision detection between projectiles and enemies
def check_collision():
    for projectile in projectiles:
        for enemy in enemies:
            if detect_collision(canvas.coords(projectile), canvas.coords(enemy)):
                canvas.delete(projectile)
                canvas.delete(enemy)
                projectiles.remove(projectile)
                enemies.remove(enemy)
                if enemies_remaining > 0:
                    create_enemy()  # Create a new enemy for each elimination
                elif not enemies:  # Check if all enemies are eliminated
                    end_screen("Victory!")
                break
    fenetre.after(50, check_collision)

# Collision detection function
def detect_collision(coords1, coords2):
    x1, y1, x2, y2 = coords1
    x3, y3, x4, y4 = coords2
    return x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3

# End screen function
def end_screen(message):
    canvas.delete("all")  # Clear the canvas
    canvas.create_text(screen_width // 2, screen_height // 2 - 50, text=message, font=("Arial", 32), fill="red")
    restart_button = tk.Button(fenetre, text="Restart", font=("Arial", 24), command=start_game)
    restart_button_window = canvas.create_window(screen_width // 2, screen_height // 2 + 50, window=restart_button)

# Display start screen
start_screen()

# Launch the window
fenetre.mainloop()
