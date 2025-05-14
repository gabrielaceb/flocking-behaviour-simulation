DIMENSIONS = 2
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOID_COUNT = 50
MAX_VELOCITY = 4
EVASION_RADIUS = 100
ATTACK_RADIUS = 150

CANVAS_RES = (SCREEN_WIDTH, SCREEN_HEIGHT)

score = INIT_SCORE = 0
lives = INIT_LIVES = 3
time = 0.5
started = False
# constants for varying different quontities
const_friction = .01
const_thrust = .1
const_rotation = .1
const_missile = 5
const_rock_vicinity = 3  # the rocks won't spawn at a distance closed than 3 radii to the center of the ship
const_rock_speed = INIT_ROCK_SPEED = 1  # the rocks will move/spin faster the greather the constant is
