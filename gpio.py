import os

gpio_base_path = '/sys/class/gpio/'
# gpio_base_path = '.'
pin_nums_in = (32, 31, 30, 29, 28, 43, 42, 41)
pin_names_in = ('pd0', 'pd1', 'pd2', 'pd3', 'pd4', 'pd5', 'pd6', 'pd7')
pin_nums_out = (14, 13, 12, 27, 26, 25, 24, 23)
pin_names_out = ('pi4', 'pi5', 'pi6', 'pi7', 'pi8', 'pi9', 'pe4', 'pe5')


def btn_dir(num):
    dirname = 'gpio' + str(pin_nums_in[num]) + "_" + str(pin_names_in[num])
    path = os.path.join(gpio_base_path, dirname)
    return path


def led_dir(num):
    dirname = 'gpio' + str(pin_nums_out[num]) + "_" + str(pin_names_out[num])
    path = os.path.join(gpio_base_path, dirname)
    return path


def set_btn():
    gpio_export = open(os.path.join(gpio_base_path, 'export'), 'w')
    for i in range(0, len(pin_nums_in)):
        pin = str(pin_nums_in[i])
        name = pin_names_in[i]
        gpio_export.write(pin)
        try:
            gpio_export.flush()
        except IOError:
            print name + " already exported"
    gpio_export.close()

    for i in range(0, len(pin_nums_in)):
        dirfile = open(os.path.join(btn_dir(i), 'direction'), 'w')
        dirfile.write('in')
        dirfile.close()


def set_led():
    gpio_export = open(os.path.join(gpio_base_path, 'export'), 'w')
    for i in range(0, len(pin_nums_out)):
        pin = str(pin_nums_out[i])
        name = pin_names_out[i]
        gpio_export.write(pin)
        try:
            gpio_export.flush()
        except IOError:
            print name + " already exported"
    gpio_export.close()

    for i in range(0, len(pin_nums_out)):
        dirfile = open(os.path.join(led_dir(i), 'direction'), 'w')
        dirfile.write('out')
        dirfile.close()


def check_btn(num):
    fil = open(os.path.join(btn_dir(num), 'value'))
    val = fil.read()
    fil.close()
    if val == '0':
        return True
    else:
        return False


def set_led_value(led, val):
    valfile = open(os.path.join(led_dir(led), 'value'), 'w')
    valfile.write(str(val))
    valfile.close()
