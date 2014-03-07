#!/usr/bin/env python
import pygame
from pygame import *
from pygame.locals import *
import os
import threading
import gpio
import time
import sys

resolution = (0, 0)
timeout = 10 * 1000
blank_timeout = 100 * 1000

viewer_run = False
images = []
blank_image = 'blank.jpg'

NOOF_BUTTONS = 5

CHANGE_IMAGE_EVENT = pygame.USEREVENT + 1
BLANK_SCREEN_EVENT = pygame.USEREVENT + 2
BTN_EVENT = pygame.USEREVENT + 3


def view_image(image, surface):
    picture = pygame.image.load(image)
    picture = pygame.transform.scale(picture, resolution)
    surface.blit(picture, (0, 0))
    pygame.display.update()


def view_images(main_surface):
    global viewer_run
    blank = True

    view_image(blank_image, main_surface)

    i = 0
    pygame.time.set_timer(CHANGE_IMAGE_EVENT, timeout)
    pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

    while True:
        if viewer_run is False:
                break

        for event in pygame.event.get():
            if event.type == CHANGE_IMAGE_EVENT and blank is False:
                i += 1
                if i >= len(curr_set):
                    i = 0
                print "next image"
                if len(curr_set) > 0:
                    view_image(curr_set[i], main_surface)

            if event.type == BLANK_SCREEN_EVENT:
                view_image(blank_image, main_surface)
                blank = True
                print "BLANK EVENT"

            elif event.type == BTN_EVENT:
                blank = False
                i = 0
                curr_set = images[event.btn]
                if len(curr_set) > 0:
                    view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)
                print "Button " + str(event.btn) + " pressed"

            elif ((event.type == KEYDOWN and event.key == K_ESCAPE) or
                  event.type == pygame.QUIT):
                print "escape"
                viewer_run = False


def control_thread():
    global viewer_run

    while True:
        for i in range(0, NOOF_BUTTONS):
            if gpio.check_btn(i):
                pygame.event.post(pygame.event.Event(BTN_EVENT, btn=i))
                for x in range(0, NOOF_BUTTONS):
                    gpio.set_led(x, 0)
                gpio.set_led(i, 1)
                time.sleep(0.2)
                break

        if viewer_run is False:
            break

    print "Ending"


def load_images(dir):
    images = []
    image_dir = os.path.join(dir)
    dirlist = os.listdir(image_dir)
    for f in dirlist:
        if f.endswith('.jpg'):
            images.append(os.path.join(image_dir, f))

    return images


def main():
    global viewer_run
    global images
    global resolution

    pygame.init()

    modes = pygame.display.list_modes()
    if len(modes) > 0:
        resolution = modes[0]
    else:
        print "No available display modes"
        pygame.quit()
        sys.exit(1)

    try:
        main_surface = pygame.display.set_mode(resolution)
    except pygame.error:
        print "Cannot open display"
        pygame.quit()
        sys.exit(1)

    for i in range(0, NOOF_BUTTONS):
        images.append([])
        try:
            images[i] = load_images('/home/cubie/obr' + str(i + 1))
        except OSError:
            print "Missing picture directory"

    try:
        gpio.set_btn()
        gpio.set_led()
    except IOError:
        print "Cannot open GPIO sysfs files, probably not running on Cubie"

    viewer_run = True
    t1 = threading.Thread(target=view_images, args=(main_surface,))
    t2 = threading.Thread(target=control_thread)
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    pygame.quit()


if __name__ == "__main__":
    main()
