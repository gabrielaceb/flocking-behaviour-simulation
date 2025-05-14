# Flocking Behaviour Simulation (Boids in Pygame)

This project simulates the flocking behaviour of "boid" agents using Python and Pygame. The agents react to each other and to a central threat using three behaviours: **calm**, **evade**, and **attack**. It was developed as part of the Artificial Intelligence coursework at UTM.

## Main Concepts
- Implementation of custom `Vector` class and vector operations
- Boid agent model with:
  - Alignment (move in same direction)
  - Cohesion (move toward the centre)
  - Separation (avoid crowding)
  - Threat evasion and attack response
- Modes of interaction with the radar area

## Technologies
- Python 3
- Pygame
- Optional: NumPy for alternative vector ops

## How to Run
```bash
pip install pygame
python main.py
