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
images0 = []
images1 = []
images2 = []
images3 = []
images4 = []

CHANGE_IMAGE_EVENT = pygame.USEREVENT + 1
BTN0_EVENT = pygame.USEREVENT + 2
BTN1_EVENT = pygame.USEREVENT + 3
BTN2_EVENT = pygame.USEREVENT + 4
BTN3_EVENT = pygame.USEREVENT + 5
BTN4_EVENT = pygame.USEREVENT + 6
BLANK_SCREEN_EVENT = pygame.USEREVENT + 7


def view_image(image, surface):
    picture = pygame.image.load(image)
    picture = pygame.transform.scale(picture, resolution)
    surface.blit(picture, (0, 0))
    pygame.display.update()


def view_images(images):
    global viewer_run
    curr_set = images1

    main_surface = pygame.display.set_mode(resolution)

    i = 0
    pygame.time.set_timer(CHANGE_IMAGE_EVENT, timeout)
    while True:
        if viewer_run is False:
                break

        for event in pygame.event.get():
            if event.type == CHANGE_IMAGE_EVENT:
                i += 1
                if i >= len(curr_set):
                    i = 0
                view_image(curr_set[i], main_surface)

            if event.type == BLANK_SCREEN_EVENT:
                print "BLANK EVENT"

            elif event.type == BTN0_EVENT:
                i = 0
                curr_set = images0
                view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

            elif event.type == BTN1_EVENT:
                i = 0
                curr_set = images1
                view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

            elif event.type == BTN2_EVENT:
                i = 0
                curr_set = images2
                view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

            elif event.type == BTN3_EVENT:
                i = 0
                curr_set = images3
                view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

            elif event.type == BTN4_EVENT:
                i = 0
                curr_set = images4
                view_image(curr_set[i], main_surface)
                pygame.time.set_timer(BLANK_SCREEN_EVENT, blank_timeout)

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                print "escape"
                viewer_run = False


def control_thread():
    global viewer_run

    while True:
        if gpio.check_btn(0):
            pygame.event.post(pygame.event.Event(BTN0_EVENT))
        elif gpio.check_btn(1):
            pygame.event.post(pygame.event.Event(BTN1_EVENT))
        elif gpio.check_btn(2):
            pygame.event.post(pygame.event.Event(BTN2_EVENT))
        elif gpio.check_btn(3):
            pygame.event.post(pygame.event.Event(BTN3_EVENT))
        elif gpio.check_btn(4):
            pygame.event.post(pygame.event.Event(BTN4_EVENT))

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
    global images0
    global images1
    global images2
    global images3
    global images4

    images0 = load_images('/home/cubie/obr1')
    images1 = load_images('/home/cubie/obr2')
    images2 = load_images('/home/cubie/obr3')
    images3 = load_images('/home/cubie/obr4')
    images4 = load_images('/home/cubie/obr5')

    gpio.set_btn()
    gpio.set_led()

    viewer_run = True
    t1 = threading.Thread(target=view_images, args=(images1,))
    t2 = threading.Thread(target=control_thread)
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    pygame.quit()


if __name__ == "__main__":
    main()
