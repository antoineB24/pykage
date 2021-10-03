import animation
import time

@animation.wait()
def default():
    time.sleep(10)

# clock animation (white, default speed)
clock = ['-','\\','|','/']

@animation.wait(clock)
def do_something():
    time.sleep(10)


# horizontal line animation (blue, default speed)
lines = ['   ','-  ','-- ','---']

@animation.wait(lines, color="blue")
def do_something_else():
    time.sleep(10)


# hashtag animation (cyan, slow)
tags = ["#   ", "##  ", "### ", "####"]

animation_ = animation.Wait(tags, color="blue", speed=0.5)
animation_.start()
time.sleep(4)
animation_.stop()
