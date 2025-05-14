import random

from collision import *
from constants import *
from entities import *

from resources import *



inputs = {"left": (my_ship.turn, -1),
          "right": (my_ship.turn, 1),
          "up": (my_ship.accelerate, 1),
          "space": (my_ship.fire, 1)}


def rock_spawner():
    if len(rock_group) < 12 and started:
        pos = [random.randrange(0, CANVAS_RES[0]), random.randrange(0, CANVAS_RES[1])]
        vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        ang = random.random() * 2 * math.pi
        ang_vel = random.random() * .2 - .1
        rock_group.add(Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info))

timer = simplegui.create_timer(1000.0, rock_spawner)

def click(pos):
    """
    Mouseclick handler that resets UI and conditions whether splash image is drawn.
    Additionally resets the number of lives and the score, the background soundtrack
    """
    global lives, score, started, const_rock_speed

    center = [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
        lives = INIT_LIVES
        score = INIT_SCORE
        const_rock_speed = INIT_ROCK_SPEED

def draw(canvas):
    global time, lives, score, started

    # Background animation logic
    time += 1
    wtime = (time / 4) % CANVAS_RES[0]
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(),
                      [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2], [CANVAS_RES[0], CANVAS_RES[1]])
    canvas.draw_image(debris_image, center, size, (wtime - CANVAS_RES[0] / 2, CANVAS_RES[1] / 2),
                      (CANVAS_RES[0], CANVAS_RES[1]))
    canvas.draw_image(debris_image, center, size, (wtime + CANVAS_RES[0] / 2, CANVAS_RES[1] / 2),
                      (CANVAS_RES[0], CANVAS_RES[1]))

    # Draw and update the ship
    my_ship.draw(canvas)
    my_ship.update()

    # Process all sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # Check for collisions
    if group_collide(rock_group, my_ship):
        lives -= 1

    # Update score based on rocks destroyed by missiles
    score += 10 * group_group_collide(rock_group, missile_group)

    # Game over condition
    if lives == 0:
        started = False
        timer.stop()
        soundtrack.pause()
        rock_group.difference_update(rock_group)

    # Draw UI elements like lives and score
    canvas.draw_text("Lives", [30, 40], 36, "Orange", "monospace")
    canvas.draw_text(str(lives), [30, 76], 36, "Orange", "monospace")
    canvas.draw_text("Score", [670, 40], 36, "Orange", "monospace")
    canvas.draw_text(str(score), [670, 76], 36, "Orange", "monospace")

    # Show splash screen if the game has not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2],
                          splash_info.get_size())


def keydown(key):
    for i in inputs:  # sugested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](inputs[i][1])


def keyup(key):
    for i in inputs:  # sugested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](0)
