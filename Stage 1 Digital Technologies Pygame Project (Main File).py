import pygame
import random
from pygame import mixer

# Import classes from other files
from classes.player import Player
from classes.player_bullet import Bullet
from classes.enemy_bullet import EnemyBullet
from classes.enemy import Enemy

# Initialise Pygame and mixer for sounds
pygame.init()
mixer.init()

# CONSTANTS #

# Constants related to the screen and health bar
BG_XSPEED = 0.1
WIDTH = 800
HEIGHT = 600
FPS = 60
ONE_SECOND = 1000
SCREEN_DIMENSIONS = (WIDTH, HEIGHT)

# HEALTH BAR
HEALTH_BAR_LOCATION = (540, 23)
BAR_HEIGHT = 20
MAX_HEALTH = 100
XBAR = 650
YBAR = 20

# PLAYER RELATED
START_X = WIDTH/2
START_Y = HEIGHT-50

# COLOURS AND TEXT
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 24)
SCORE_LOCATION = (430, 23)

# ENEMY RELATED
ENEMY_DAMAGE_PER_HIT = 10
ENEMY_SPAWN_Y = 50
ROOF_Y = 0

# Initialise variables that will change
time = 0
shoot_cooldown = 0
player_shoot = False
game_state = 'start_menu'

# Create game window
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

# Set window title
pygame.display.set_caption('Space Invaders')

# Create clock to control game frame rate.
clock = pygame.time.Clock()

# Load all game images
bg_img = pygame.image.load('images\\space_backdrop.png').convert_alpha()
enemy_plane_img = pygame.image.load('images\\enemy_spaceship.png').convert_alpha()
player_img = pygame.image.load('images\\player_spaceship.png').convert_alpha()
enemy_missile_img = pygame.image.load('images\\enemy_missile.png').convert_alpha()
player_missile_img = pygame.image.load('images\\missile.png').convert_alpha()
explosion_img = pygame.image.load('images\\explosion.png').convert_alpha()
boss_img = pygame.image.load('images\\boss_ship.png').convert_alpha()

# Load game sounds
ship_shoot_sound = mixer.Sound("sounds/laser.wav")
ship_shoot_sound.set_volume(0.1) # Decrease volume of shoot sound

# Create a sprite group to store all sprites.
all_sprites = pygame.sprite.Group()

# Create sprite groups for enemies and bullets
enemy_grp = pygame.sprite.Group()
player_bullet_grp = pygame.sprite.Group()
enemy_bullet_grp = pygame.sprite.Group()

# Set background on screen
bg_width = bg_img.get_width()
bg_x = 0
bg2_x = bg_width

# Create player and add to sprite group
player = Player(START_X, START_Y, player_img)
all_sprites.add(player)

# Add timer event to spawn enemies
pygame.time.set_timer(pygame.USEREVENT+1, 1000)
spawn_enemy = False


# Function used to draw the start menu before main game loop.
def draw_start_menu() -> None:
    screen.fill(BLACK)
    title_font = pygame.font.SysFont('verdana', 40)
    title = title_font.render('Space Shooter Game', True, WHITE)
    title_font = pygame.font.SysFont('verdana', 20)
    description = title_font.render('Achieve a score of over 2000 to win!', True, WHITE)
    start_message = title_font.render('Press SPACE to start, Q to exit', True, WHITE)
    screen.blit(bg_img, (0, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2))
    screen.blit(description, (WIDTH / 2 - description.get_width() / 2, HEIGHT / 2 + 20 + description.get_height() / 2))
    screen.blit(start_message, (WIDTH / 2 - start_message.get_width() / 2, HEIGHT / 2 + 40 + start_message.get_height() / 2))
    pygame.display.update()
    
    
# Function used to draw the win screen.
def draw_loss_menu() -> None:
    screen.fill(BLACK)
    title_font = pygame.font.SysFont('verdana', 80)
    title = title_font.render('YOU LOSE!', True, RED)
    title_font = pygame.font.SysFont('verdana', 40)
    quit_message = title_font.render('Press Q to exit', True, WHITE)
    reset_game_message = title_font.render('Press R to restart.', True, WHITE)
    screen.blit(bg_img, (0, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, (HEIGHT / 2) - 100 - title.get_height() / 2))
    screen.blit(quit_message, (WIDTH / 2 - quit_message.get_width() / 2, HEIGHT / 2 + quit_message.get_height() / 2))
    screen.blit(reset_game_message, (WIDTH / 2 - reset_game_message.get_width() / 2, HEIGHT / 2 + 50 + reset_game_message.get_height() / 2))
    pygame.display.update()


def draw_win_screen() -> None:
    screen.fill(BLACK)
    title_font = pygame.font.SysFont('verdana', 80)
    title = title_font.render('YOU WIN!', True, GREEN)
    title_font = pygame.font.SysFont('verdana', 40)
    quit_message = title_font.render('Press Q to exit', True, WHITE)
    reset_game_message = title_font.render('Press R to restart.', True, WHITE)
    screen.blit(bg_img, (0, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, (HEIGHT / 2) - 100 - title.get_height() / 2))
    screen.blit(quit_message, (WIDTH / 2 - quit_message.get_width() / 2, HEIGHT / 2 + quit_message.get_height() / 2))
    screen.blit(reset_game_message, (WIDTH / 2 - reset_game_message.get_width() / 2, HEIGHT / 2 + 50 + reset_game_message.get_height() / 2))
    pygame.display.update()  


def reset_game_values(): 
    # Utilizing the 'global' keyword allows this function to modify variables in this file instead of creating new ones.
    global time, shoot_cooldown, game_state
    global all_sprites, enemy_grp, player_bullet_grp, enemy_bullet_grp
    global player, spawn_enemy
    
    # Reset variables 
    time = 0
    shoot_cooldown = 0
    player_shoot = False
    game_state = 'start_menu'

    # Create a sprite group to store all sprites.
    all_sprites = pygame.sprite.Group()

    # Create sprite groups for enemies and bullets
    enemy_grp = pygame.sprite.Group()
    player_bullet_grp = pygame.sprite.Group()
    enemy_bullet_grp = pygame.sprite.Group()

    # Create player and add to sprite group
    player = Player(START_X, START_Y, player_img)
    all_sprites.add(player)

    # Add timer event to spawn enemies
    spawn_enemy = False


# MAIN GAME LOOP
while True:
    # Keep game loop running at correct speed.
    clock.tick(FPS)
    
    # Retrieve all events to prevent using the method again as it broke the code
    events = pygame.event.get()
    
    # Check for quit button 
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
    
    # Check if the game has not started yet
    if game_state == 'start_menu':
        # Draw start menu and check for event to play the game
        draw_start_menu()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = 'playing'
        # Prevent rest of game from being run by skipping rest of loop
        continue
    if game_state == 'loss':
        # Draw loss screen
        draw_loss_menu()
        # Check if reset key has been pressed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game_values()
        # Prevent rest of game from being run by skipping rest of loop
        continue
    if game_state == 'win':
        # Draw win screen
        draw_win_screen()
        # Check if reset key has been pressed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game_values()
        # Prevent rest of game from being run by skipping loop
        continue
    
    # Increase player's shoot cooldown every frame
    shoot_cooldown += 1
    
    # Check for key and timer events
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Shoot bind
                if shoot_cooldown >= 15: # Shoot cooldown passed
                    shoot_cooldown = 0
                    player_shoot = True
            # Quit game 
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
        # Every 3 seconds spawn an enemy
        if event.type == pygame.USEREVENT+1:
            spawn_enemy = True
    
    # Spawn player bullet and reset cooldown
    if player_shoot:
        bullet = Bullet(player_missile_img, player.rect.midtop)
        # Add sprite to main sprite group and bullet sprite group  
        all_sprites.add(bullet)
        player_bullet_grp.add(bullet)
        # Play shoot sound and reset cooldowns
        ship_shoot_sound.play()
        player_shoot = False
        shoot_cooldown = 0
    
    # Spawn enemy and add to sprite groups
    if spawn_enemy:
        enemy = Enemy(random.randint(0, WIDTH), ENEMY_SPAWN_Y, enemy_plane_img)
        all_sprites.add(enemy)
        enemy_grp.add(enemy)
        # Prevent spawning an enemy next frame
        spawn_enemy = False
    
    # Update player
    player.update(events)
    
    # Update each bullet
    for bullet in player_bullet_grp:
        bullet.update()
        if bullet.y < ROOF_Y:
            player_bullet_grp.remove(bullet)
            all_sprites.remove(bullet)
            
    # Update each enemy
    for enemy in enemy_grp:
        enemy.update() 
        if enemy.y > HEIGHT:
            enemy.y = ROOF_Y
        # 3 Seconds since an enemy has spawned
        if enemy.shoot_cooldown >= 120: 
            # Retrieve bottom middle of enemy sprite to spawn bullet correctly 
            bullet_start_coordinates = enemy.rect.midbottom
            enemy_bullet = EnemyBullet(enemy_missile_img, bullet_start_coordinates, enemy)
            # Reset cooldown and add bullet to sprite groups
            enemy.shoot_cooldown = 0
            enemy_bullet_grp.add(enemy_bullet)
            all_sprites.add(enemy_bullet)
            
    # Update and check if any enemy bullet has gone off screen
    for enemy_bullet in enemy_bullet_grp:
        if enemy_bullet.y > HEIGHT:
            enemy_bullet_grp.remove(enemy_bullet)
            all_sprites.remove(enemy_bullet)
        enemy_bullet.update()
            
    # Enemy bullet hitting player check
    hits = pygame.sprite.spritecollide(player, enemy_bullet_grp, True)
    for hit in hits:
        player.health -= 10
        
    # Player bullet hitting enemy check
    for enemy in enemy_grp:
        hits = pygame.sprite.spritecollide(enemy, player_bullet_grp, True)
        for hit in hits:
            # Despawn enemy and increase player score
            enemy_grp.remove(enemy)
            all_sprites.remove(enemy)
            player.score += 100
        
    # Check if the player has died (lost)
    if player.health <= 0:
        game_state = 'loss'
    # Check if player has achieved a score greater than 200 (won)
    if player.score >= 2000:
        game_state = 'win'
    
    # Move the background
    bg_x -= BG_XSPEED
    bg2_x -= BG_XSPEED
    
    # Blit the background image
    pos = (bg_x, 0)
    screen.blit(bg_img, pos)
    pos = (bg2_x, 0)
    screen.blit(bg_img, pos)
    
    # Make background image not go off screen
    if bg_x < -bg_width:
        bg_x = bg_width
    elif bg2_x < -bg_width:
        bg2_x = bg_width
        
    # Render screen with updated sprites
    all_sprites.draw(screen)
    
    # Render and blit the font text after so it is over the sprites
    img = FONT.render(f"Health: {player.health}", True, WHITE)
    screen.blit(img, HEALTH_BAR_LOCATION)
        
    # Display the health bar also after the sprites.
    bar_outline = pygame.Rect(XBAR, YBAR, MAX_HEALTH, BAR_HEIGHT)
    bar_fill = pygame.Rect(XBAR, YBAR, player.health, BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, bar_fill)
    pygame.draw.rect(screen, WHITE, bar_outline, 2)
    
    # Display the score
    img = FONT.render(f"Score: {player.score}", True, WHITE)
    screen.blit(img, SCORE_LOCATION)
    
    # After rendering everything update the game window
    pygame.display.update()
    
    