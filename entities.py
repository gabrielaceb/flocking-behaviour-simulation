from constants import *
from resources import *
from vectors import *

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if (self.thrust):
            canvas.draw_image(ship_image, [3 * self.image_center[0], self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center,
                              self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # determining where is "forward"
        forward_vector = angle_to_vector(self.angle)

        for i in range(DIMENSIONS):
            # sugested in "Programming Tips 7", avoiding code repetition
            # "wrapping" the canvas, updating position, velosity, adding friction, thrusting
            self.pos[i] %= CANVAS_RES[i]
            self.pos[i] += self.vel[i]
            self.vel[i] *= (1 - const_friction)

            if (self.thrust):
                self.vel[i] += forward_vector[i] * const_thrust

        # updating angle
        self.angle += self.angle_vel

    # methods called by key pressing: turn, accelerate, fire
    def turn(self, turn):
        self.angle_vel = const_rotation * turn

    def accelerate(self, thrust_on):
        if (thrust_on > 0):
            self.thrust = True
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.pause()

    def fire(self, shoot):
        if (shoot > 0):
            forward_vector = angle_to_vector(self.angle)
            newpos = [0, 0]
            newvel = [0, 0]

            for i in range(DIMENSIONS):  # determining position and velocity of the missile
                newpos[i] = self.pos[i] + forward_vector[i] * self.image_size[i] / 2
                newvel[i] = self.vel[i] + forward_vector[i] * const_missile

            a_missile = Sprite(newpos, newvel, 0, 0, missile_image, missile_info, missile_sound)
            missile_group.add(a_missile)


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = Vector(pos)
        self.vel = Vector(vel)
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius
    def draw(self, canvas):
        # Convert position to tuple for drawing
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos.tuple(), self.image_size, self.angle)
    def update(self):
        # Update position and age
        self.pos += self.vel
        self.angle += self.angle_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False

    def collide(self, other_object):
        # Check for collision with another object
        other_pos = Vector(other_object.pos)
        distance = (self.pos - other_pos).magnitude()
        return distance < self.radius + other_object.radius

    def flock(self, boids):
        # Apply the boid behaviors: separation, alignment, cohesion
        sep = Vector([0, 0])  # Separation
        align = Vector([0, 0])  # Alignment
        cohere = Vector([0, 0])  # Cohesion
        count = 0
        for boid in boids:
            if boid != self:
                distance = (self.pos - boid.pos).magnitude()
                if distance < 100:  # Neighborhood distance
                    sep += (self.pos - boid.pos) / distance  # More influence from closer boids
                    align += boid.vel
                    cohere += boid.pos
                    count += 1
        if count > 0:
            sep = sep / count * 1.5
            align = (align / count - self.vel) * 0.5
            cohere = ((cohere / count - self.pos).normalize() * 2 - self.vel) * 0.1
            self.vel += sep + align + cohere
        self.vel = self.vel.normalize() * min(self.vel.magnitude(), 3)  # Limit speed

        # Helper class for vector operations, adapted for simplegui



# Ship and three groups of sprites initialized
my_ship = Ship([CANVAS_RES[0] / 2, CANVAS_RES[1] / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
