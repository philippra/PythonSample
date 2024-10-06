import ctypes
import os


def get_current_speed():
    """Written by CommonSense, stackoverflow
    (https://stackoverflow.com/questions/45100234/change-mouse-pointer-speed-in-windows-using-python)
    Gets the current cursor speed.
    :return speed_value (int)
    """
    get_mouse_speed = 112  # 0x0070 for SPI_GETMOUSESPEED
    speed = ctypes.c_int()
    ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0,
                                               ctypes.byref(speed), 0)

    return speed.value


def change_speed(speed=10):
    """Written by CommonSense, stackoverflow
    (https://stackoverflow.com/questions/45100234/change-mouse-pointer-speed-in-windows-using-python)
    Changes the cursor speed.
    :speed (int) : which sensitivity you want to use
    :return None
    """
    #   1 - slow
    #   10 - standard
    #   20 - fast
    set_mouse_speed = 113  # 0x0071 for SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)


def set_mouse_acceleration(thresh1=0, thresh2=0, accel=0):
    """This function sets the mouse acceleration.
    :return None"""
    set_mouse = 4  # 0x0004 for SPI_SETMOUSE
    array_type = ctypes.c_int * 3
    aSetAccel = array_type()
    aSetAccel[0], aSetAccel[1], aSetAccel[2] = thresh1, thresh2, accel

    ctypes.windll.user32.SystemParametersInfoA(set_mouse, 0,
                                               ctypes.byref(aSetAccel), 0)


def get_mouse_acceleration():
    """This function gets the current mouse acceleration settings.
    :return thresh1 (int), thresh2 (int), accel (bool / int)"""
    get_mouse = 3  # 0x0003 for SPI_GETMOUSE
    array_type = ctypes.c_int * 3
    aAccel = array_type()

    ctypes.windll.user32.SystemParametersInfoA(get_mouse, 0,
                                               ctypes.byref(aAccel), 0)

    thresh1, thresh2, accel = aAccel
    return thresh1, thresh2, accel


# save current settings
thresh1Old, thresh2Old, accelOld = get_mouse_acceleration()
current_speed = get_current_speed()

# save settings in a folder/file
# tries to create a folder called mouse (if it not already exists)
try:
    os.mkdir("mouse")
except FileExistsError:
    print("Directory mouse folder already exists.")

# creates a txt-file for storing the participants mouse settings
# (if it doesn't already exist, so we don't override stuff)
mouse_list = [thresh1Old, thresh2Old, accelOld, current_speed]
if not os.path.exists("mouse\\mouse_accel_settings.txt"):
    with open('mouse\\mouse_accel_settings.txt', 'w') as f:
        for item in mouse_list:
            f.write("%s\n" % item)
        f.close()

# change mouse settings to whatever you want
change_speed(3)  # change the sensitivity
set_mouse_acceleration()  # turn acceleration off (using the default arguments (0,0,0) ; see above)

#######################################
# MAGNIFICENT EXPERIMENT HAPPENS HERE #
#######################################

# reset to starting values after experiment
change_speed(current_speed)
set_mouse_acceleration(thresh1Old, thresh2Old, accelOld)