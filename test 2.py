import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAX_VELOCITY = 4
EVASION_RADIUS = 100
ATTACK_RADIUS = 150
NUM_BOIDS = 20

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector(0, 0)

    def to_list(self):
        return [self.x, self.y]

    def wrap_around(self):
        self.x = self.x % SCREEN_WIDTH
        self.y = self.y % SCREEN_HEIGHT

class Boid:
    def __init__(self):
        self.position = Vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_VELOCITY
        self.color = "White"

    def update(self, boids, mode, target=None):
        if mode == "attack" and target:
            self.attack(target)
        elif mode == "evade" and target:
            self.evade(target)
        else:
            self.flock(boids)

        self.position += self.velocity
        self.position.wrap_around()

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        self.velocity += alignment + cohesion + separation
        if self.velocity.magnitude() > MAX_VELOCITY:
            self.velocity = self.velocity.normalize() * MAX_VELOCITY

    def align(self, boids):
        percep_radius = 50
        steering = Vector(0, 0)
        total = 0
        for other in boids:
            if other != self and (self.position - other.position).magnitude() < percep_radius:
                steering += other.velocity
                total += 1
        if total > 0:
            steering = (steering / total).normalize() * MAX_VELOCITY
        return steering - self.velocity

    def cohere(self, boids):
        percep_radius = 50
        center_mass = Vector(0, 0)
        total = 0
        for other in boids:
            if other != self and (self.position - other.position).magnitude() < percep_radius:
                center_mass += other.position
                total += 1
        if total > 0:
            center_mass = center_mass / total
            return (center_mass - self.position).normalize() * MAX_VELOCITY - self.velocity
        return Vector(0, 0)

    def separate(self, boids):
        percep_radius = 25
        steering = Vector(0, 0)
        total = 0
        for other in boids:
            distance = (self.position - other.position).magnitude()
            if other != self and distance < percep_radius:
                diff = (self.position - other.position).normalize()
                steering += diff / distance
                total += 1
        if total > 0:
            steering /= total
        return steering

    def attack(self, target):
        # Move towards the target
        self.velocity = (target.position - self.position).normalize() * MAX_VELOCITY

    def evade(self, target):
        # Move away from the target
        self.velocity = (self.position - target.position).normalize() * MAX_VELOCITY

    def draw(self, canvas):
        canvas.draw_circle(self.position.to_list(), 10, 1, self.color, self.color)

class Game:
    def __init__(self):
        self.boids = [Boid() for _ in range(NUM_BOIDS)]
        self.mode = "calm"  # can be 'calm', 'attack', or 'evade'
        self.target = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def draw(self, canvas):
        for boid in self.boids:
            boid.update(self.boids, self.mode, self.target)
            boid.draw(canvas)
        canvas.draw_text("Mode: " + self.mode, (50, 50), 20, 'White')

    def keydown(self, key):
        if key == simplegui.KEY_MAP["a"]:
            self.mode = "attack"
        elif key == simplegui.KEY_MAP["e"]:
            self.mode = "evade"
        elif key == simplegui.KEY_MAP["c"]:
            self.mode = "calm"

game = Game()
frame = simplegui.create_frame("Boids Simulation", SCREEN_WIDTH, SCREEN_HEIGHT)
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(game.keydown)
frame.start()
