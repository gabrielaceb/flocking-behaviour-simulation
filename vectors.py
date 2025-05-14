import math


class Vector:
    def __init__(self, elements):
        self.elements = elements

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.elements, other.elements)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.elements, other.elements)])

    def __mul__(self, scalar):
        return Vector([a * scalar for a in self.elements])

    def __truediv__(self, scalar):
        return Vector([a / scalar for a in self.elements])

    def magnitude(self):
        return math.sqrt(sum(x ** 2 for x in self.elements))

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector([0 for _ in self.elements])

    def tuple(self):
        return tuple(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __iter__(self):
        return iter(self.elements)

# Boid class for each asteroid implementing flocking behavior
class Boid:
    def __init__(self, position, velocity, image, info):
        self.position = Vector(position)
        self.velocity = Vector(velocity)
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.position.tuple(), self.image_size)

    def update(self, boids):
        self.flock(boids)
        self.position += self.velocity

    def flock(self, boids):
        # Parameters for behaviors
        sep_dist = 25
        align_dist = 50
        coh_dist = 50

        # Initialize forces
        sep_force = Vector([0, 0])
        align_force = Vector([0, 0])
        coh_force = Vector([0, 0])
        count_sep = 0
        count_coh_align = 0

        # Calculate forces
        for other in boids:
            dist = (self.position - other.position).magnitude()
            if 0 < dist < sep_dist:  # Separation
                sep_force += (self.position - other.position).normalize() / dist
                count_sep += 1
            if dist < align_dist:  # Alignment and Cohesion
                align_force += other.velocity
                coh_force += other.position
                count_coh_align += 1

        if count_sep > 0:
            sep_force = (sep_force / count_sep).normalize() * 0.05

        if count_coh_align > 0:
            align_force = ((align_force / count_coh_align).normalize() - self.velocity).normalize() * 0.05
            coh_center = coh_force / count_coh_align
            coh_force = ((coh_center - self.position).normalize() * 0.02).normalize() * 0.03

        # Apply forces
        self.velocity += sep_force + align_force + coh_force
        self.velocity = self.velocity.normalize() * min(self.velocity.magnitude(), 2)  # Limit speed

