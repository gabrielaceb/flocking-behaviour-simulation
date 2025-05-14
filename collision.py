import math
from entities import Sprite, explosion_group
from resources import explosion_image, explosion_info, explosion_sound
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.flock(sprite_group)
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)


def group_collide(sprite_group, other_object):
    """
    Function takes a group of sprites and another object (e.g. the ship, a sprite)
    and if these two collided makes an explosion, returning True; else False
    """
    remove_sprites = set([])

    for sprite in sprite_group:
        if sprite.collide(other_object):
            remove_sprites.add(sprite)

    if len(remove_sprites):  # if something collided..
        sprite_group.difference_update(remove_sprites)
        an_explosion = Sprite(other_object.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
        explosion_group.add(an_explosion)
        return True

    else:  # if not..
        return False


def group_group_collide(rock_group, missile_group):
    """
    Function takes two groups of sprites (i.e. the rock group, the missile group)
    and returns the number of rocks destroyed
    """
    rocks_destroyed = 0

    for missile in list(missile_group):  # itterating over a copy of the missile group
        if group_collide(rock_group, missile):
            rocks_destroyed += 1
            # safely mutating the missile group because we itterate on a copy
            missile_group.discard(missile)

    return rocks_destroyed

