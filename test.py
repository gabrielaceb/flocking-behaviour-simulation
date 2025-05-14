import pygame
import sys
import math
import random

# declararea variabilelor
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOID_COUNT = 50
MAX_VELOCITY = 4
EVASION_RADIUS = 100
ATTACK_RADIUS = 150
RADAR_SWEEP_MAX_RADIUS = max(SCREEN_WIDTH, SCREEN_HEIGHT)
RADAR_SWEEP_START_RADIUS = 0
RADAR_SWEEP_SPEED = 1
radar_sweep_radius = RADAR_SWEEP_START_RADIUS

# inițializare joc Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Vector:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    # adunarea a doi vectori, returnează un nou vector care este suma vectorială
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # scăderea a doi vectori, returnează un nou vector care este diferența vectorială
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # înmulțirea vectorului cu un scalar, returnează un nou vector scalat
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # împărțirea vectorului la un scalar, returnează un nou vector scalat
    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("The scalar must be a number")
        return Vector(self.x / scalar, self.y / scalar)

    # produsul scalar (dot product) a doi vectori, returnează o valoare scalară
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Produsul vectorial (cross product) a doi vectori în 2D,
    # care returnează un nou vector cu componenta z reprezentând perpendiculara în spațiul 3D
    def cross(self, other):
        z = self.x * other.y - self.y * other.x
        return Vector(0, 0, z)

    # returnează lungimea vectorului
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # normalizează vectorul, returnează un vector unitate cu aceeași direcție
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector(0, 0)

    # returnează o reprezentare în formă de tuplu a vectorului, util pentru operații în Pygame
    def tuple(self):
        return (self.x, self.y)

def wrap_around(x, y):
    x = x % SCREEN_WIDTH
    y = y % SCREEN_HEIGHT
    return x, y

class Boid:
    # inițializează poziția boidului într-un punct aleatoriu pe ecran
    # viteza este de asemenea aleatorie și normalizată, înmulțită cu viteza maximă
    def __init__(self):
        self.position = Vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_VELOCITY # prin acest mecanism, toate boids vor avea aceeași viteză maximă, dar direcții inițiale diferite.
        self.color = (255, 255, 255)

    # actualizează starea boidului în funcție de modul în care se află
    def update(self, boids, mode='calm'):
        acceleration = Vector(0, 0)

        # selectează boids-urile din apropiere în funcție de raza de evitare
        near_boids = [b for b in boids if b is not self and (b.position - self.position).magnitude() < EVASION_RADIUS]

        # poziția navei spațiale
        threat = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # comportamentul de bază
        if mode == 'calm':
            self.color = (255, 255, 255)
            alignment = self.align(near_boids)
            cohesion = self.cohere(near_boids)
            separation = self.separate(near_boids)
            center_avoidance = self.avoid(threat)
            acceleration = alignment + cohesion + separation + center_avoidance

        # comportamentul de evadare și atac
        elif mode in ['evade', 'attack']:
            alignment = self.align(near_boids)
            cohesion = self.cohere(near_boids)
            separation = self.separate(near_boids)
            combined_flocking = alignment + cohesion + separation

            if mode == 'evade':
                self.color = (0, 255, 0)
                evasion = self.evade(threat)
                acceleration = evasion + separation

            elif mode == 'attack':
                self.color = (255, 0, 0)
                attack = self.attack(threat)
                acceleration = attack + combined_flocking

        # actualizează viteza și poziția boidului
        self.velocity += acceleration
        self.velocity = self.velocity.normalize() * MAX_VELOCITY
        self.position += self.velocity # mișcarea fundamentală a boidului de la un cadru la altul în simulare.
        self.position.x, self.position.y = wrap_around(self.position.x, self.position.y)

    # desenează boidul pe ecran ca un cerc
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 2)

    #  calculează vectorul mediu de viteză al boids-urilor apropiate și normalizează rezultatul
    def align(self, boids):
        if not boids:
            return Vector(0, 0)

        mean_vel = sum((b.velocity for b in boids), Vector(0, 0))
        return (mean_vel / len(boids)).normalize() # calcularea vitezei medii din vecinătate și anilierea grupului

    # calculează un vector de forță pentru a se îndepărta de centrul perceput ca amenințare
    def avoid(self, center):
        diff = self.position - center
        distance = diff.magnitude()

        if distance < EVASION_RADIUS:
            force = diff.normalize() # obține direcția în care entitatea ar trebui să se deplaseze pentru a evita centrul.
            force_strength = (EVASION_RADIUS - distance) / EVASION_RADIUS
            return force * force_strength * 2 # se returnează un vector de forță rezultat din combinarea direcției normalizate (force) și intensității forței de evitare (force_strength)

        return Vector(0, 0)

    # îndreaptă boidul către centrul de masă al boids-urilor apropiate
    def cohere(self, boids):
        if not boids: return Vector(0, 0)

        center_mass = sum((b.position for b in boids), Vector(0, 0)) # se determină suma tuturor pozițiilor
        return ((center_mass / len(boids)) - self.position).normalize() # se calculează vectorul de forță de coeziune

    #  calculează o forță care determină boidul să mențină o distanță de siguranță față de ceilalți boids
    def separate(self, boids):
        separation = Vector(0, 0)

        for b in boids:
            if b is not self:
                diff = self.position - b.position
                # forța de separare este invers proporțională cu distanța
                separation += diff.normalize() / diff.magnitude()
        return separation

    # determină boidul să se îndepărteze de nava spațială
    def evade(self, threat):
        diff = self.position - threat
        # normalizează diferența de poziție pentru a obține direcția opusă amenințării
        return diff.normalize() if diff.magnitude() < EVASION_RADIUS else Vector(0, 0)

    # determină boidul să se miște în direcția țintei
    def attack(self, target):
        # normalizează diferența de poziție pentru a obține un vector direcționat către țintă
        return (target - self.position).normalize()


# main simulation loop
boids = [Boid() for _ in range(BOID_COUNT)]
running = True
mode = 'calm'

while running:
    screen.fill((0, 0, 0))

    # desenare radar
    if radar_sweep_radius >= RADAR_SWEEP_MAX_RADIUS:
        radar_sweep_radius = RADAR_SWEEP_START_RADIUS
    else:
        radar_sweep_radius += RADAR_SWEEP_SPEED
    pygame.draw.circle(screen, (200, 200, 200), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radar_sweep_radius, 1)

    # desenare cerculețe
    for i in range(50, RADAR_SWEEP_MAX_RADIUS, 50):
        pygame.draw.circle(screen, (200, 200, 200), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), i, 1)

    # desenare linii care mimează X și Y pe radar
    pygame.draw.line(screen, (200, 200, 200), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 1)  # Y-axis
    pygame.draw.line(screen, (200, 200, 200), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 1)  # X-axis

    # desenare poziția navei spațiale (poziționată în centrul radarului)
    pygame.draw.circle(screen, (0, 0, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 5)

    # funcție pentru schimbarea comportamnetului boizilor
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                mode = 'evade'
            elif event.key == pygame.K_q:
                mode = 'attack'
            elif event.key == pygame.K_c:
                mode = 'calm'

    #
    for boid in boids:

        # actualizează starea fiecărui boid în funcție de modul curent și de pozițiile celorlalte boids
        boid.update(boids, mode)

        # desenează fiecare boid pe ecran
        boid.draw()

    # actualizează întregul ecran pentru a afișa noile poziții ale boids-urilor
    pygame.display.flip()

    #  Așteaptă suficient timp pentru a menține rata cadrelor la 60 de cadre pe secundă
    clock.tick(60)

# oprește Pygame, eliberând resursele utilizate de acesta
pygame.quit()
sys.exit()
