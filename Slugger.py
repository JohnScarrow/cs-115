import pygame
import sys
import time
import json
import os
import random

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
John Scarrow
Slugger Game
2/26/2025

Homework 7 for CS-115

Dive into the delightfully absurd world of Slugger where slugs wear bows, snail shells bounce like they're at a disco, and every millisecond counts!

In this zany game, you take on the role of either a dapper slug or a chic lady slug (complete with a fashionable red bow!), both striving to make their way to the top of the screen without becoming escargot. Can you dodge, weave, and slither your way past a barrage of bouncing snail shells?

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# -----------------------------
# Preload high scores function
# -----------------------------
def preload_high_scores():
    file_path = "high_scores.json"
    pregen_scores = [
        {"name": "Slugger", "time": 30.0},
        {"name": "Slugget", "time": 40.0}
    ]
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(pregen_scores, file)
    else:
        with open(file_path, "r") as file:
            try:
                high_scores = json.load(file)
            except json.JSONDecodeError:
                high_scores = []
        names = {score["name"] for score in high_scores}
        for ps in pregen_scores:
            if ps["name"] not in names:
                high_scores.append(ps)
        high_scores = sorted(high_scores, key=lambda x: x["time"])[:5]
        with open(file_path, "w") as file:
            json.dump(high_scores, file)

preload_high_scores()

# -----------------------------
# Initialize Pygame and Setup
# -----------------------------
pygame.init()

width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slugger")

# -----------------------------
# Colors and Variables
# -----------------------------
black = (5, 5, 5)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
slug_body_color = (160, 82, 45)

slug_eye_colors = [
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255)
]
slug_pupil_color = (0, 0, 0)

slug = pygame.Rect(400, 750, 70, 30)
slug_speed = 5
eye_color_index = 0

# Character select.
is_female_slug = random.choice([True, False])

# Obstacles (snail shells)
snails = [
    pygame.Rect(100, 100, 60, 60),
    pygame.Rect(200, 200, 60, 60),
    pygame.Rect(300, 300, 60, 60),
    pygame.Rect(400, 400, 60, 60),
    pygame.Rect(500, 500, 60, 60),
    pygame.Rect(600, 600, 60, 60)
]
snail_speed = [2, -2, 2, -2, 2, -2]

color_index = 0

# -----------------------------
# Drawing Functions
# -----------------------------
def draw_slug(surface, rect, eye_color):
    # Draw slug body
    pygame.draw.ellipse(surface, slug_body_color, rect)
    # Calculate eye positions
    eye_width = rect.width // 5
    eye_height = rect.height // 2
    eye1 = pygame.Rect(rect.x + eye_width, rect.y - eye_height // 2, eye_width, eye_height)
    eye2 = pygame.Rect(rect.x + 3 * eye_width, rect.y - eye_height // 2, eye_width, eye_height)
    pygame.draw.ellipse(surface, eye_color, eye1)
    pygame.draw.ellipse(surface, eye_color, eye2)
    pupil_width = eye_width // 2
    pupil_height = eye_height // 2
    pupil1 = pygame.Rect(eye1.x + pupil_width // 2, eye1.y + pupil_height // 2, pupil_width, pupil_height)
    pupil2 = pygame.Rect(eye2.x + pupil_width // 2, eye2.y + pupil_height // 2, pupil_width, pupil_height)
    pygame.draw.ellipse(surface, slug_pupil_color, pupil1)
    pygame.draw.ellipse(surface, slug_pupil_color, pupil2)

def draw_red_bow(surface, rect):
    # Draw a red bow for a female slug.
    bow_color = red
    bow_center_x = rect.centerx
    bow_center_y = rect.top - 10 
    bow_width = rect.width // 6
    bow_height = rect.height // 3
    left_lobe = pygame.Rect(bow_center_x - bow_width - 5, bow_center_y - bow_height // 2, bow_width, bow_height)
    right_lobe = pygame.Rect(bow_center_x + 5, bow_center_y - bow_height // 2, bow_width, bow_height)
    pygame.draw.ellipse(surface, bow_color, left_lobe)
    pygame.draw.ellipse(surface, bow_color, right_lobe)
    knot_rect = pygame.Rect(bow_center_x - 5, bow_center_y - 5, 10, 10)
    pygame.draw.ellipse(surface, bow_color, knot_rect)

def draw_snail_shell(surface, rect, color_index):
    color = pygame.Color(0)
    color.hsva = (color_index % 360, 100, 100, 100)
    pygame.draw.ellipse(surface, color, rect)
  # Adding detail to "SHELLS"
    shell_lines = 5
    for i in range(1, shell_lines):
        pygame.draw.arc(surface, black, rect.inflate(-i * 10, -i * 10), 0, 3.14, 1)

def invert_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])

# Flashy end game screen
def strobe_screen(color):
    for _ in range(6):
        screen.fill(color)
        pygame.display.flip()
        time.sleep(0.1)
        screen.fill(invert_color(color))
        pygame.display.flip()
        time.sleep(0.1)

# -----------------------------
# High Score Functions
# Suprize JSON file on your pooter
# -----------------------------
def save_high_score(name, completion_time):
    high_scores = []
    file_path = "high_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    high_scores.append({"name": name, "time": completion_time})
    high_scores = sorted(high_scores, key=lambda x: x["time"])[:5]
    with open(file_path, "w") as file:
        json.dump(high_scores, file)

def is_high_score(completion_time):
    file_path = "high_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    else:
        high_scores = []
      # 5 entry max for high scores
    if len(high_scores) < 5 or any(score["time"] > completion_time for score in high_scores):
        return True
    return False


# Enter name to be saved in JSON
def get_high_score_input(completion_time):
    font = pygame.font.Font(None, 74)
    input_box = pygame.Rect(200, 350, 400, 50)
    color_inactive = white
    color_active = green
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              # Click on Name location to select to input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                  # Enter string to be saved
                    if event.key == pygame.K_RETURN:
                        save_high_score(text, completion_time)
                        done = True
                      # Removes most recent letter inputted (Pooter is dumb)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                      # Input letter that is pressed
                        text += event.unicode
        screen.fill(black)
        txt_surface = font.render(text, True, color)
      # Size of input box
        input_box.w = max(400, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

def display_high_scores():
    font = pygame.font.Font(None, 74)
    file_path = "high_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    else:
        high_scores = []
    screen.fill(black)
    y_offset = 100
    for score in high_scores:
      # Show the top 5 scores in a using a LOOP
        score_text = f"{score['name']}: {score['time']}s"
        txt_surface = font.render(score_text, True, white)
        screen.blit(txt_surface, (200, y_offset))
        y_offset += 80
    pygame.display.flip()
    time.sleep(5)

# -----------------------------
# Main Game Loop
# -----------------------------
running = True
color_index = 0
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Controls to move Slug... Or Slugget
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT] and slug.left > 0:
        slug.x -= slug_speed
        moved = True
    if keys[pygame.K_RIGHT] and slug.right < width:
        slug.x += slug_speed
        moved = True
    if keys[pygame.K_UP] and slug.top > 0:
        slug.y -= slug_speed
        moved = True
    if keys[pygame.K_DOWN] and slug.bottom < height:
        slug.y += slug_speed
        moved = True

  # When player moves eyes roll through colors
    if moved:
        eye_color_index = (eye_color_index + 1) % len(slug_eye_colors)

    for i, snail in enumerate(snails):
        snail.x += snail_speed[i]
        if snail.x <= 0 or snail.x >= width - snail.width:
            snail_speed[i] = -snail_speed[i]

    collision = False
    for snail in snails:
        if slug.colliderect(snail):
            collision = True
            break
# If collisoon with obsticles 
    if collision:
        strobe_screen(red)
        print("Collision detected!")
        display_high_scores()
        running = False
# Win condition
    if slug.top <= 0:
        strobe_screen(green)
        print("Congratulations! You won!")
        end_time = time.time()
        completion_time = round(end_time - start_time, 2)
      # Calculating score
        if is_high_score(completion_time):
            get_high_score_input(completion_time)
        display_high_scores()
        running = False

    screen.fill(black)
    draw_slug(screen, slug, slug_eye_colors[eye_color_index])
  # Random character
    if is_female_slug:
        draw_red_bow(screen, slug)
    for i, snail in enumerate(snails):
        draw_snail_shell(screen, snail, color_index + i * 30)
    color_index += 1
    pygame.display.flip()

pygame.quit()
sys.exit()
