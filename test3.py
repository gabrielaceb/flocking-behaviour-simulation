import pygame
import sys
import math
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOID_COUNT = 50
MAX_VELOCITY = 4
EVASION_RADIUS = 100
ATTACK_RADIUS = 150
SHOOTING_INTERVAL = 120  # Frames between shots

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


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

    def tuple(self):
        return (self.x, self.y)


class Boid:
    def __init__(self):
        self.position = Vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_VELOCITY
        self.color = (255, 255, 255)  # White for calm behavior
        self.mode = 'calm'

    def update(self, boids, target):
        acceleration = Vector(0, 0)
        if self.mode == 'attack':
            attack = (target - self.position).normalize()
            acceleration += attack

        self.velocity += acceleration
        self.velocity = self.velocity.normalize() * MAX_VELOCITY
        self.position += self.velocity
        self.position.x, self.position.y = wrap_around(self.position.x, self.position.y)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 2)


def wrap_around(x, y):
    x = x % SCREEN_WIDTH
    y = y % SCREEN_HEIGHT
    return x, y


def main():
    boids = [Boid() for _ in range(BOID_COUNT)]
    running = True
    frame_count = 0
    center_point = Vector(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        pygame.draw.circle(screen, (0, 0, 255), center_point.tuple(), 5)  # Central dot

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Central dot attacks every SHOOTING_INTERVAL frames
        if frame_count % SHOOTING_INTERVAL == 0:
            target_boid = min(boids, key=lambda boid: (boid.position - center_point).magnitude())
            if (target_boid.position - center_point).magnitude() < ATTACK_RADIUS:
                target_boid.mode = 'attack'
                target_boid.color = (255, 0, 0)  # Change color to red when attacking

        for boid in boids:
            boid.update(boids, center_point)
            boid.draw()

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
