import sys
import os
import ctypes

'''
("mouse\\mouse_accel_settings.txt", "mouse\\")'''


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def read_settings():
    with open(resource_path("mouse\\mouse_accel_settings.txt"), 'r') as f:
        lines = f.readlines()
        lines = list(lines)
        for idx, line in enumerate(lines):
            lines[idx] = int(line)

        accel_settings = lines[0:-1]
        speed_setting = lines[-1]
    return accel_settings, speed_setting


def change_speed(speed=10):
    """Written by CommonSense, stackoverflow
    (https://stackoverflow.com/questions/45100234/change-mouse-pointer-speed-in-windows-using-python)
    """
    #   1 - slow
    #   10 - standard
    #   20 - fast
    set_mouse_speed = 113  # 0x0071 for SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)


def set_mouse_acceleration(thresh1=0, thresh2=0, accel=0):
    set_mouse = 4  # 0x0004 for SPI_SETMOUSE
    array_type = ctypes.c_int * 3
    aSetAccel = array_type()
    aSetAccel[0], aSetAccel[1], aSetAccel[2] = thresh1, thresh2, accel

    ctypes.windll.user32.SystemParametersInfoA(set_mouse, 0,
                                               ctypes.byref(aSetAccel), 0)


accel, speed = read_settings()
thresh1, thresh2, accel = accel

set_mouse_acceleration(thresh1, thresh2, accel)
change_speed(speed)
