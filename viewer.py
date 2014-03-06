#!/usr/bin/env python
import pygame
from pygame import *
from pygame.locals import *
import os
import threading
import gpio


resolution = (1920, 900)
timeout = 10 * 1000
blank_timeout = 60 * 1000

viewer_run = False
images = []

NOOF_BUTTONS = 5

CHANGE_IMAGE_EVENT = pygame.USEREVENT + 1
BLANK_SCREEN_EVENT = pygame.USEREVENT + 2
BTN_EVENT = pygame.USEREVENT + 3


def view_image(image, surface):
    picture = pygame.image.load(image)
    picture = pygame.transform.scale(picture, resolution)
    surface.blit(picture, (0, 0))
    pygame.display.update()


def view_images():
    global viewer_run
    curr_set = images[0]

    main_surface = pygame.display.set_mode(resolution)

    i = 0
    pygame.time.set_timer(CHANGE_IMAGE_EVENT, timeout)
    pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

    while True:
        if viewer_run is False:
                break

        for event in pygame.event.get():
            if event.type == CHANGE_IMAGE_EVENT:
                i += 1
                if i >= len(curr_set):
                    i = 0
                print "next image"
                view_image(curr_set[i], main_surface)

            if event.type == BLANK_SCREEN_EVENT:
                print "BLANK EVENT"

            elif event.type == BTN_EVENT:
                i = 0
                curr_set = images[event.btn]
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

    pygame.init()

    for i in range(0, NOOF_BUTTONS):
        images.append([])
        images[i] = load_images('/home/cubie/obr' + str(i + 1))

    gpio.set_btn()
    gpio.set_led()

    viewer_run = True
    t1 = threading.Thread(target=view_images)
    t2 = threading.Thread(target=control_thread)
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    pygame.quit()


if __name__ == "__main__":
    main()
