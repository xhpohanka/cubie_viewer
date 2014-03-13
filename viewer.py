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
blank_timeout = 70 * 1000

viewer_run = False
images = []
blank_image = 'blank.jpg'
# images_dir = './'
images_dir = '/home/cubie/'

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

    curr_set = []
    pic_counter = 0
    pygame.time.set_timer(CHANGE_IMAGE_EVENT, timeout)
    pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

    gpio.set_stripes_value(1)

    while True:
        if viewer_run is False:
                break

        for event in pygame.event.get():
            if ((event.type == KEYDOWN and event.key == K_ESCAPE) or
               event.type == pygame.QUIT):
                print "escape"
                viewer_run = False
                break

            if event.type == CHANGE_IMAGE_EVENT and blank is False:
                pic_counter += 1
                if pic_counter >= len(curr_set):
                    pic_counter = 0

                print "next image"
                if pic_counter < len(curr_set):
                    view_image(curr_set[pic_counter], main_surface)

            if event.type == BLANK_SCREEN_EVENT:
                view_image(blank_image, main_surface)
                blank = True
                print "BLANK EVENT"
                gpio.set_stripes_value(1)
                for i in range(0, NOOF_BUTTONS):
                    gpio.set_led_value(i, 0)

            if event.type == BTN_EVENT or event.type == KEYDOWN:
                blank = False
                pic_counter = 0

                if event.type == KEYDOWN:
                    position = event.key - 48
                else:
                    position = event.key

                if position < 0 or position > len(images) - 1:
                    print "Wrong key pressed"
                    continue

                curr_set = images[position]
                if pic_counter < len(curr_set):
                    view_image(curr_set[pic_counter], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)
                pygame.time.set_timer(CHANGE_IMAGE_EVENT, timeout)
                gpio.set_stripes_value(0)
                gpio.set_all_led_value(0)
                gpio.set_led_value(position, 1)
                print "Button " + str(position) + " pressed"


def control_thread():
    global viewer_run

    while True:
        for i in range(0, NOOF_BUTTONS):
            if gpio.check_btn(i):
                pygame.event.post(pygame.event.Event(BTN_EVENT, key=i))
                time.sleep(0.2)
                break

        if viewer_run is False:
            break

        if os.path.exists('./stop'):
            viewer_run = False

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
        main_surface = pygame.display.set_mode(resolution, FULLSCREEN)
    except pygame.error:
        print "Cannot open display"
        pygame.quit()
        sys.exit(1)

    pygame.mouse.set_visible(False)

    for i in range(0, NOOF_BUTTONS):
        images.append([])
        try:
            images[i] = load_images(images_dir + 'obr' + str(i + 1))
        except OSError:
            print "Missing picture directory"

    try:
        gpio.setup_btn()
        gpio.setup_led()
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
