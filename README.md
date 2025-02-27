Slugger: A Quirky Pygame Adventure
Welcome to Slugger – an inventive and fun game built with Python and Pygame! In this game, you control a slug as it dodges bouncing snail shells on its way to victory. Can you help the slug make it to the top without a collision?

(Replace this placeholder image with your own banner image if you like)

Table of Contents
Introduction

Features

Installation

Usage

High Scores

Contributing

License

Acknowledgements

Introduction
Slugger is a charming and challenging game developed as part of my Introduction to Computer Science course. With vibrant color transitions, dynamic obstacles, and a dash of personality (a randomly selected slug character might even come with a stylish red bow!), the game demonstrates key programming concepts such as:

Game Loop & Event Handling

Collision Detection

Animation and Color Transitions

File I/O with JSON (for a high score system)

Features
Responsive Controls: Use the arrow keys to move the slug in all directions.

Dynamic Obstacles: Bounce past snail shells that change colors over time.

Stylish Characters: Enjoy a randomly chosen slug character—for a female slug, a red bow tops her head!

Strobing Effects: Dynamic visual effects with red flashes on collision and green flashes on winning.

Real-Time High Scores: Your completion time is recorded and, if fast enough, you’re prompted to enter your name using an in-game text box. High scores are stored in a JSON file.

Pre-Loaded High Scores: The high score list comes preloaded with two scores: Slugger (30.0s) and Slugget (40.0s).

Installation
To run Slugger on your local machine, follow these steps:

Clone the repository:

bash
git clone https://github.com/JohnScarrow/cs-115.git
cd cs-115
Install Pygame:

Ensure you have Python installed, then install Pygame using pip:

bash
pip install pygame
Run the game:

bash
python Slugger.py
Usage
Objective: Guide your slug from the bottom to the top of the screen while avoiding bouncing snail shells.

Movement: Use the arrow keys to move in all directions.

High Scores: If you win and your time is one of the best, an in-game prompt will allow you to enter your name. The high score list will then be displayed for 15 seconds before the game exits.

High Scores
The game maintains a list of the top 5 best times, stored in the file high_scores.json. Two initial scores are preloaded:

Slugger: 30.0 seconds

Slugget: 40.0 seconds

Try to beat them and see your name on the leaderboard!

Contributing
Contributions are welcome! Feel free to fork this repository, create new features, or fix bugs. Pull requests and suggestions are highly appreciated.

License
This project is open source and available under the MIT License.

Acknowledgements
Thank you to my instructors and classmates for their support and inspiration in this project.

Thanks to the Pygame community for their stellar resources.

Special shout-out to everyone who believes even a slow slug can leave its mark!

Happy Slugging and enjoy the game!
