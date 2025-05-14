# Mini-Project 8: RiceRocks
# On less performant computers the game may perform slower

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from events import *

# Frame initialized
frame.set_keydown_handler(keydown)
frame = simplegui.create_frame("Asteroids", CANVAS_RES[0], CANVAS_RES[1])
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)


# Lastly and most importantly
frame.start()
