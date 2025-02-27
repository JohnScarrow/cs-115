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

In this zany game, you take on the role of either a dapper slug or a chic lady slug (with a snazzy red bow!), both striving to make their way to the top of the screen without becoming escargot.
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

# Character selection: randomly choose a female slug (with red bow) or not.
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
# Speed of each snail
snail_speed = [2, -2, 2, -2, 2, -2]

color_index = 0

# -----------------------------
# Drawing Functions
# -----------------------------
def draw_slug(surface, rect, eye_color):# Slug render
    pygame.draw.ellipse(surface, slug_body_color, rect)
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

def draw_red_bow(surface, rect):# Bow Render
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

def draw_snail_shell(surface, rect, color_index):# Shells color change
    color = pygame.Color(0)
    color.hsva = (color_index % 360, 100, 100, 100)
    pygame.draw.ellipse(surface, color, rect)
    # Add detail using arc texture on the shell
    shell_lines = 5
    for i in range(1, shell_lines):
        pygame.draw.arc(surface, black, rect.inflate(-i * 10, -i * 10), 0, 3.14, 1)

def draw_start_and_win_areas(surface):
    # Victory area at the top 
    win_area = pygame.Rect(0, 0, width, 50)
    start_area = pygame.Rect(0, height - 50, width, 50)
    pygame.draw.rect(surface, green, win_area)
    pygame.draw.rect(surface, invert_color(green), start_area)

def draw_obstacle_rows(surface):
    # Horizontal lines separating rows
    row_lines = [175, 275, 375, 475, 575, 675]
    for y in row_lines:
        pygame.draw.line(surface, white, (0, y), (width, y), 5)

def invert_color(color):# Changing color to the opposite color
    return (255 - color[0], 255 - color[1], 255 - color[2])

def strobe_screen(color):# Crazy strobe effect
    for _ in range(24):
        screen.fill(color)
        pygame.display.flip()
        time.sleep(0.05)
        screen.fill(invert_color(color))
        pygame.display.flip()
        time.sleep(0.05)

# -----------------------------
# High Score Functions
# Have a JSON file ;P
# -----------------------------
def save_high_score(name, completion_time):
    high_scores = []
    file_path = "high_scores.json"
    if os.path.exists(file_path):# Checking if high_score.json exists
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    high_scores.append({"name": name, "time": completion_time})
    high_scores = sorted(high_scores, key=lambda x: x["time"])[:5]# Scores in order
    with open(file_path, "w") as file:# Overwrite file
        json.dump(high_scores, file)

def is_high_score(completion_time):# Check if you can add your high_score
    file_path = "high_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    else:
        high_scores = []
    if len(high_scores) < 5 or any(score["time"] > completion_time for score in high_scores):
        return True
    return False

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
            # Toggle active state when clicking on the input box.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:# Input character
                if active:
                    if event.key == pygame.K_RETURN:# Submit name
                        save_high_score(text, completion_time)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                      # remove last input (Stupid Pooter)
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill(black)
        txt_surface = font.render(text, True, color)
        input_box.w = max(400, txt_surface.get_width() + 10)# width of input field
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

def display_high_scores():# Displaying best scores after attempt
    font = pygame.font.Font(None, 74)
    file_path = "high_scores.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            high_scores = json.load(file)
    else:
        high_scores = []
    screen.fill(black)
    y_offset = 100
    for score in high_scores:# Loop display for the number of scores
        score_text = f"{score['name']}: {score['time']}s"
        txt_surface = font.render(score_text, True, white)
        screen.blit(txt_surface, (200, y_offset))
        y_offset += 80
    pygame.display.flip()
    time.sleep(6)

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

    keys = pygame.key.get_pressed()
    moved = False
  # Player controls
    if keys[pygame.K_LEFT] and slug.left > 0:
        slug.x -= slug_speed
        moved = True
    if keys[pygame.K_RIGHT] and slug.right < width:
        slug.x += slug_speed
        moved = True
    if keys[pygame.K_UP]:
        slug.y -= slug_speed
        moved = True
    if keys[pygame.K_DOWN] and slug.bottom < height: 
        slug.y += slug_speed
        moved = True

    if moved:
        eye_color_index = (eye_color_index + 1) % len(slug_eye_colors)

    for i, snail in enumerate(snails):# All move independantly
        snail.x += snail_speed[i]
      # When snail hits a side it changes direction
        if snail.x <= 0 or snail.x >= width - snail.width:
            snail_speed[i] = -snail_speed[i]

    collision = False
    for snail in snails:
        if slug.colliderect(snail):
            collision = True
            break

    if collision:# Fail condition
        strobe_screen(red)
        print("Collision detected!")
        display_high_scores()
        running = False

    if slug.top <= 50:  # Win condition: slug reaches the victory area
        strobe_screen(green)
        print("Congratulations! You won!")
        end_time = time.time()
        completion_time = round(end_time - start_time, 2)
        if is_high_score(completion_time):# Check if new high_score
            get_high_score_input(completion_time)
        display_high_scores()
        running = False

    screen.fill(black)
    draw_start_and_win_areas(screen)  # Draw fixed green start & win areas
    draw_obstacle_rows(screen)        # Draw fixed rows separating obstacles
    draw_slug(screen, slug, slug_eye_colors[eye_color_index])
    if is_female_slug:# mystery character
        draw_red_bow(screen, slug)
    for i, snail in enumerate(snails):
        draw_snail_shell(screen, snail, color_index + i * 30)
    color_index += 1
    pygame.display.flip()

pygame.quit()
sys.exit()
