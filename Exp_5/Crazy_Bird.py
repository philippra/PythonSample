import pygame
from pandas import DataFrame, read_csv
import sys
import os
import shutil
from time import sleep
from time import perf_counter
import ctypes
from random import shuffle, choice, randint, uniform
import pyminizip
from win32api import EnumDisplaySettings, EnumDisplayDevices, ShellExecute
from datetime import datetime
from Functions import *
from Classes import *
from Pre_Experiment import *
from Post_Experiment import *

"""CREATED BY PHILIPP RASSBACH, DEPARTMENT FOR PSYCHOLOGY III, JMU WÜRZBURG; 
   Some functions were written by other people which are credited in the 
   function descriptions"""

# if is_admin():

# test if disc has enough space
free_space = shutil.disk_usage("/")[2]
print("Freier Speicherplatz: %d GiB" % (free_space // (2 ** 30)))

if (free_space // (2 ** 30)) < 2:
    print(
        "Festplattenspeicher kleiner als 2 GiB. Durchführung des Experiments ist damit nicht möglich\n"
        "Bitte sorge zunächst für ausreichend Speicherplatz.")
    sleep(10)
    sys.exit()
else:
    print("Ausreichend Festplattenspeicher vorhanden!")

global age_input
global gender_input
global handedness_input
global hypothesis_input
global regularities_input
global strategy_input
global strategy_effort_input
global delayedPerc_input
global hold_flag
global perceptibility_input
global other_input
global informed_consent
global participated_earlier_input
global diff_input
global effort_input
global delayedPerc_input

hold_flag = "NO INPUT"
strategy_input = "NO INPUT"
strategy_effort_input = "NO INPUT"
regularities_input = "NO INPUT"
hypothesis_input = "NO INPUT"
perceptibility_input = "NO INPUT"
other_input = "NO INPUT"
diff_input = "NO INPUT"
effort_input = "NO INPUT"
participated_earlier_input = "NO INPUT"
delayedPerc_input = "NO INPUT"

# file paths for images and instructions; add to datas-variable in .spec file
"""[('pics\\sampleBird_scaled_state1.png', 'pics\\'), 
('pics\\sampleBird_scaled_state2.png', 'pics\\'), 
('pics\\sampleBird_scaled_state3.png', 'pics\\'), 
('pics\\sampleStar.png', 'pics\\'), 
('pics\\sampleObstacle_scaled.png', 'pics\\'),
('pics\\sampleGate_scaled.png', 'pics\\'),
('pics\\Instruct_1.png', 'pics\\'),
('pics\\Instruct_2.png', 'pics\\'),
('pics\\Instruct_3.png', 'pics\\'),
('pics\\Instruct_4.png', 'pics\\'),
('pics\\Instruct_5.png', 'pics\\'),
('pics\\Instruct_6.png', 'pics\\'),
('pics\\Training_1.png', 'pics\\'),
('pics\\Training_2.png', 'pics\\'),
('pics\\Training_3.png', 'pics\\'),
('pics\\Training_4.png', 'pics\\'),
('files\\Exp_Conditions_Infrequent.csv', 'files\\'),
('files\\Exp_Conditions_Frequent.csv', 'files\\'),
('files\\Instruktion_1.txt', 'files\\'),
('files\\Instruktion_2.txt', 'files\\'),
('files\\Instruktion_3.txt', 'files\\'),
('files\\Instruktion_4.txt', 'files\\'),
('files\\Instruktion_5.txt', 'files\\'),
('files\\Instruktion_6.txt', 'files\\'),
('files\\Instruktion_7.txt', 'files\\'),
('files\\Instruktion_8.txt', 'files\\'),
('pics\\InformierteEinwilligung_short_1.ppm', 'pics\\'),
('pics\\InformierteEinwilligung_short_2.ppm', 'pics\\'),
('pics\\InformierteEinwilligung_short_3.ppm', 'pics\\')]"""

# center window / frame
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Turn of windows scaling for the experiment
ctypes.windll.user32.SetProcessDPIAware()
# Get true resolution
true_res = (ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1))

aspect_ratio = true_res[0] / true_res[1]

aspect_ratio_scaler = (aspect_ratio * 9) / 16

demographics_font_size = int(12)

# close_programms()

participant_id, counterbalance, changeFreq = select_partNum_counterbalance()

informed_consent = display_informed_consent()

part = 1 # if select_part() == "Teil 1" else 2

# participant_id = create_id_code()

age_input, gender_input, handedness_input = collect_demographics()

hold_flag = True

pygame.init()  # initialize pygame
pygame.display.set_caption("MLTT_Ayesh")
clock = pygame.time.Clock()

screen, screen_width, screen_height, screen_surface = set_screen_vars(true_res)

# Screen variables dict
screen_variables = {"upper_lane": (screen_height / 8) * 2,
                    "middle_lane": (screen_height / 8) * 4,
                    "lower_lane": (screen_height / 8) * 6,
                    "bgColor": (0, 0, 0),
                    "laneColor": (255, 255, 255),
                    "lanes": {
                        "upper": ((screen_height / 8) * 2 - (screen_height /
                                                             13),
                                  (screen_height / 8) * 2 + (screen_height /
                                                             13)),
                        "middle": ((screen_height / 8) * 4 - (screen_height
                                                              / 13),
                                   (screen_height / 8) * 4 + (screen_height
                                                              / 13)),
                        "lower": ((screen_height / 8) * 6 - (screen_height
                                                             / 13),
                                  (screen_height / 8) * 6 + (screen_height
                                                             / 13))},
                    "x_pos": screen_width // 2,  # middle of the screen, x axis
                    "y_pos": screen_height // 2}  # middle of the screen, y axis

# dictionary containing the experimental parameters
expGlobals = {
    "perturb": screen_height / 100,
    # perturbation factor, gets multiplied by csv-file coefficient (which is currently 1)
    "direction": 0,  # direction of the perturbation (0 = up, 1 = down)
    "bird_lane": "middle",  # current lane the bird is on
    "game_active": 1,  # boolean which controls the game loop
    "score": 0,  # participant score
    "score_total": 0,
    "eaten_total": 0,
    "falls_total": 0,
    "upper_jump_boundary": 210,
    "lower_jump_boundary": -210,
    "orientation_weight": 0.60,
    # controls the impact of bird orientation on jumping behavior
    "speed_multiplier": 1,
    "object_speed": -(screen_width / (500 / 1.11)) * (6.475 / 6),
    "object_speed_backup": -(screen_width / (500 / 1.11)) * (4 / 3),
    # controls the speed of the gates, obstacle and stars
    "star_position": screen_width * 1.33,
    "obstacle_position": screen_width * 1.17,
    "gate_position": screen_width * 0.93,
    "continue": 0,  # controls the loop for gathering demographics
    "bgColor": (0, 0, 0),  # background color (black)
    "screen": screen,  # screen object
    "font": pygame.font.SysFont("Arial", int(screen_width / 52.53)),  # font
    "game_font": pygame.font.SysFont("Arial", int(screen_width / 34.15)),
    "screenRect": screen.get_rect(),  # rectangle of the screen
    "textColor": (255, 255, 255),  # color for text (white)
    "instWidth": screen_width // 1.1,  # maximum width of instructions
    "instHeight": screen_height // 2,  # maximum height of instructions
    "scrollPar": (screen_height / 50) / 2.5,  # determines necessary scrolling action to readjust cursor
    "previewDict": {"long": 2.75, "short": .75}  # sets preview times for rewards
}

# dictionary containing the relevant variables # JUMP DIRECTION MISSING
results = {"informed_consent": [],
           "trial_num": [],
           "id": [],
           "counterbalance": [],
           "changeFreq": [],
           "handedness": [],
           "age": [],
           "gender": [],
           "part": [],
           "screen_resolution_x": [],
           "screen_resolution_y": [],
           "monitor_refresh_rate": [],
           "trial": [],
           "block": [],
           "subblock": [],
           "dependence": [],
           "pert_direct": [],
           "preview_congr": [],
           "pert_strength": [],
           "reward_upper": [],
           "reward_lower": [],
           "bird_orientation": [],
           "jump": [],
           "higher_reward": [],
           "reward_collected": [],
           "gate_passed": [],
           "stars_visible": [],
           "bird_lane": [],
           "star_position": [],
           "gate_position": [],
           "obstacle_position": [],
           "bird_position": [],
           "block_start": [],
           "trial_start": [],
           "time_stamp": [],
           "trial_display_start": [],
           "current_mouse_posx": [],
           "current_mouse_posy": [],
           "post_gate_rel_mouse_pos": [],
           "mouse_wheel_input": [],
           "score": [],
           "block_errors": [],
           "error_type": [],
           "training": [],
           "hypothesis": [],
           "regularities": [],
           "strategy": [],
           "strategy_effort": [],
           "delayedPerc": [],
           "perceptibility": [],
           "other": [],
           "participated_earlier": [],
           "effort": [],
           "diff": [],
           }

pygame.mouse.set_visible(False)

# Disabling mouse acceleration, setting mouse speed
thresh1Old, thresh2Old, accelOld = get_mouse_acceleration()
current_speed = get_current_speed()

# check_mousewheel(age_input, gender_input, handedness_input,
#                  hypothesis_input, regularities_input, strategy_input,
#                  strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
#                  informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
#                  screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
#                  part, participant_id)

device = EnumDisplayDevices()
monitor_refresh_rate = get_display_frequency(device)

exp_conds = resource_path('files\Exp_Conditions_Infrequent.csv') if changeFreq == "L" else \
    resource_path('files\Exp_Conditions_Frequent.csv')

cond_df = read_in_conds(exp_conds)

upper_lane, middle_lane, lower_lane, lane_width, lane_height = create_lanes(
    screen_width, screen_variables["lanes"][
        "upper"][1], screen_variables["lanes"]["upper"][0],
    screen_variables["lanes"]["upper"][0],
    screen_variables["lanes"]["middle"][0],
    screen_variables["lanes"]["lower"][0])

star_group, obst_group, gates_group = initialize_sprite_groups()


def display_error(error_msg: str, trial_display_start: float):
    """
    Displays an error message if the bird falls of the lane or collides with an obstacle.
    :return: None.
    """
    expGlobals["game_active"] = 0
    error_surface = expGlobals["game_font"].render(
        str(error_msg), True, (255, 0, 0))
    error_rect = error_surface.get_rect(
        center=(screen_width // 2, screen_height // 2))
    error_current_time = perf_counter()

    while abs(trial_display_start - error_current_time) <= 5.99:
        screen.fill(expGlobals["bgColor"])
        screen.blit(error_surface, error_rect)
        error_current_time = perf_counter()
        pygame.display.flip()
        clock.tick_busy_loop(100)

    pygame.event.clear()

    bird, bird_group = create_bird(lane_height, aspect_ratio_scaler,
                                   screen_variables["middle_lane"])
    return bird, bird_group


def display_block_start(block_id, block_n, errors_previous, score_previous, fall_errors,
                        obstacle_errors):
    """
    Displays a message informing the participant about the next experimental
    block. Participant can proceed in their own pace.
    :param block_id (int): current block number.
    :return: None
    """
    if block_id == 1:
        text = 'Nun starten die ' + str((block_n-1)*2) + ' Versuchsblöcke. Die Abhängigkeit der notwendigen Mausbewegung für einen Sprung von der Vogelposition variiert von Block zu Block, achte deswegen auf die Drehung des Vogels. ' \
                                                     'Zudem kann sich von Block zu Block verändern, zu welchem Zeitpunkt die Punktzahlen und Sterne zu sehen sind. Nach jedem Versuchsblock kannst ' \
                                                     'Du bei Bedarf eine Pause einlegen. Du kannst den Versuch ' \
                                                     'jederzeit mit der ESC-Taste abbrechen.\n\nDenke bitte daran, nach jedem Durchgang Deine Maus wieder in die Ausgangsposition zu bewegen.\n\n' \
                                                     'Verzögere Deine Entscheidung bei frühen Punktedarstellungen bitte nicht. \n\nDrücke die Leertaste, um zu beginnen.\n\n' \
                                                     'Möchtest Du Dir die Instruktionen nochmals durchlesen, drücke die I-Taste.\n\n'
    else:
        text = 'Im vorherigen Block hast Du ' + str(
            score_previous) + ' Punkte ' \
                              'gesammelt. Dabei bist du ' + str(
            fall_errors) + '-mal von der Bahn geweht sowie ' + \
               str(
                   obstacle_errors) + '-mal von der mittleren Katze gefressen worden.\n\nBlock ' + str(
            block_id) + \
               ' von ' + str((block_n-1)*2) + ' ist als nächster dran. Strenge Dich bitte weiterhin an, ' \
                                          'so viele Punkte wie möglich zu sammeln!\n\nDenke bitte daran, nach jedem Durchgang Deine Maus wieder in die Ausgangsposition zu bewegen.\n\n' \
                                          'Achte zudem auf die Drehung des Vogels, um sein Sprungverhalten in diesem Block zu erkennen. ' \
                                          'Verzögere Deine Entscheidung bei frühen Punktedarstellungen bitte nicht.' \
                                          '\n\nBeginne mit dem nächsten Block, indem Du die Leertaste drückst.\n\n' \
                                          'Möchtest Du Dir die Instruktionen nochmals durchlesen, drücke die I-Taste.\n\n'
    inst_coords = (
        expGlobals["screenRect"].centerx - (expGlobals["instWidth"] // 2),
        expGlobals[
            "screenRect"].centery - screen_height // 3)
    done = 0

    while not done:
        screen.fill(expGlobals["bgColor"])
        text_object_blit_wrapped(screen, text, expGlobals["font"],
                                 expGlobals["instWidth"],
                                 expGlobals["instHeight"], inst_coords,
                                 expGlobals["textColor"])
        pygame.display.flip()
        clock.tick_busy_loop(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm_exit(*exitParams)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = 1
                if event.key == pygame.K_ESCAPE:
                    confirm_exit(*exitParams)
                if event.key == pygame.K_i:
                    start_welcome_block(*welcomParams)
                    done = 1

    pygame.event.clear()


def display_training_block_start(changeFreq ,subblock):
    """
    Displays a message informing the participant about the training block. Participant can proceed at their own
    pace.
    :return: None
    """
    if changeFreq == "H":
        if subblock == 1:
            text = 'Es folgen nun zunächst einige Übungsblöcke. ' \
                   'Im 1. Übungsblock werden die Punktzahlen früh dargestellt. In durchschnittlich 3 von 4 Fällen stimmt die Windrichtung ' \
                   'zu diesem Zeitpunkt mit der Windrichtung zum Zeitpunkt des Sprungs überein (lila Pfeile). In durchschnittlich 1 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'KOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. Dies ist auch im unteren Bild dargestellt ' \
                   '(kürzere Bewegung zur nahen Bahn [grüner Pfeil]; längere Bewegung zur fernen Bahn [roter Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(1) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)
        elif subblock == 2:
            text = 'Im nächsten Übungsblock werden die Punktzahlen erneut früh dargestellt. In durchschnittlich 3 von 4 Fällen stimmt die Windrichtung ' \
                   'zu diesem Zeitpunkt mit der Windrichtung zum Zeitpunkt des Sprungs überein (lila Pfeile). In durchschnittlich 1 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'INKOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(längere Bewegung zur nahen Bahn [roter Pfeil]; kürzere Bewegung zur fernen Bahn [grüner Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(2) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)

        elif subblock == 3:
            text = 'Im nächsten Übungsblock werden die Punktzahlen sehr spät dargestellt. In durchschnittlich 3 von 4 Fällen hat sich die ' \
                   'Windrichtung zu diesem Zeitpunkt kurz zuvor nochmals verändert (siehe lila Pfeil). In durchschnittlich 1 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'KOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(kürzere Bewegung zur nahen Bahn [grüner Pfeil]; längere Bewegung zur fernen Bahn [roter Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du erneut als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(3) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)

        elif subblock == 4:
            text = 'Im nächsten Übungsblock werden die Punktzahlen erneut sehr spät dargestellt. In durchschnittlich 3 von 4 Fällen hat sich die ' \
                   'Windrichtung zu diesem Zeitpunkt kurz zuvor nochmals verändert (siehe lila Pfeil). In durchschnittlich 1 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'INKOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(längere Bewegung zur nahen Bahn [roter Pfeil]; kürzere Bewegung zur fernen Bahn [grüner Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du erneut als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(4) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)
    if changeFreq == "L":
        if subblock == 1:
            text = 'Es folgen nun zunächst einige Übungsblöcke. ' \
                   'Im 1. Übungsblock werden die Punktzahlen früh dargestellt. In durchschnittlich 1 von 4 Fällen stimmt die Windrichtung ' \
                   'zu diesem Zeitpunkt mit der Windrichtung zum Zeitpunkt des Sprungs überein (siehe lila Pfeile). In durchschnittlich 3 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'KOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. Dies ist auch im unteren Bild dargestellt ' \
                   '(kürzere Bewegung zur nahen Bahn [grüner Pfeil]; längere Bewegung zur fernen Bahn [roter Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(1) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)
        elif subblock == 2:
            text = 'Im nächsten Übungsblock werden die Punktzahlen erneut früh dargestellt. In durchschnittlich 1 von 4 Fällen stimmt die Windrichtung ' \
                   'zu diesem Zeitpunkt mit der Windrichtung zum Zeitpunkt des Sprungs überein. In durchschnittlich 3 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'INKOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(längere Bewegung zur nahen Bahn [roter Pfeil]; kürzere Bewegung zur fernen Bahn [grüner Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(2) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)

        elif subblock == 3:
            text = 'Im nächsten Übungsblock werden die Punktzahlen sehr spät dargestellt. In durchschnittlich 1 von 4 Fällen hat sich die ' \
                   'Windrichtung zu diesem Zeitpunkt kurz zuvor nochmals verändert (siehe lila Pfeil). In durchschnittlich 3 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'KOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(kürzere Bewegung zur nahen Bahn [grüner Pfeil]; längere Bewegung zur fernen Bahn [roter Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du erneut als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(3) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)

        elif subblock == 4:
            text = 'Im nächsten Übungsblock werden die Punktzahlen erneut sehr spät dargestellt. In durchschnittlich 1 von 4 Fällen hat sich die ' \
                   'Windrichtung zu diesem Zeitpunkt kurz zuvor nochmals verändert (siehe lila Pfeil). In durchschnittlich 3 von 4 Fällen ist ' \
                   'dies nicht der Fall (grauer Pfeil). ' \
                   'Zudem beeinflusst die Position des Vogels die notwendige ' \
                   'Mausbewegung für einen Sprung auf die obere oder untere Bahn in einer ' \
                   'INKOMPATIBLEN Weise in Bezug auf seine Distanz zu den Bahnen. ' \
                   'Dies ist auch im unteren Bild dargestellt ' \
                   '(längere Bewegung zur nahen Bahn [roter Pfeil]; kürzere Bewegung zur fernen Bahn [grüner Pfeil]). ' \
                   'Die Drehung des Vogels kannst Du erneut als Hinweis dafür nutzen, ' \
                   'in welche Richtung ein Sprung leichter duchzuführen ist. Drücke die Leertaste, um mit diesem Übungsblock zu beginnen.'
            train_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Training_' + str(4) + ".png")), (int(round(
                screen_width // 2)), int(round(screen_height // 2)))). \
                convert_alpha()

            train_image_rect = train_image.get_rect()
            train_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)
    inst_coords = (
        expGlobals["screenRect"].centerx - (expGlobals["instWidth"] // 2),
        expGlobals[
            "screenRect"].centery - screen_height // 2.25)
    done = 0

    while not done:
        screen.fill(expGlobals["bgColor"])
        text_object_blit_wrapped(screen, text, expGlobals["font"],
                                 expGlobals["instWidth"],
                                 expGlobals["instHeight"], inst_coords,
                                 expGlobals["textColor"])
        screen.blit(train_image, train_image_rect)
        pygame.display.flip()
        clock.tick_busy_loop(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm_exit(*exitParams)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = 1
                if event.key == pygame.K_ESCAPE:
                    confirm_exit(*exitParams)
    pygame.event.clear()


mouse_list = [thresh1Old, thresh2Old, accelOld, current_speed]

# tries to create a folder called mouse (if it not already exists)
try:
    os.mkdir("mouse")
    # print("Mouse folder created.")
except FileExistsError:
    print("Directory mouse folder already exists.")

# creates a txt-file for storing the participants mouse settings
# (if it not already exists)
if not os.path.exists("mouse\\mouse_accel_settings.txt"):
    with open('mouse\\mouse_accel_settings.txt', 'w') as f:
        for item in mouse_list:
            f.write("%s\n" % item)
        f.close()

# dictionary containing starting and ending time for the current trial
trial_data = {"starting_time": perf_counter(),
              "ending_time": perf_counter()}

# Perturbation timer - perturbation is applied roughly every 100ms
PERTURB = pygame.USEREVENT + 1
pygame.time.set_timer(PERTURB, 100)

# Perturbation random variation timer - perturbation strength is randomly
# varied roughly every 100ms
PERTURBVAR = pygame.USEREVENT + 2
pygame.time.set_timer(PERTURBVAR, 100)

# this conditional statement checks if there already exists a MLTT_Ayesh_results.csv; if
# so, it gets deleted
if os.path.exists("MLTT_Ayesh_results.csv"):
    os.remove("MLTT_Ayesh_results.csv")
# else:
#    print("The file does not exist")

cond_df = prepare_cond_df(cond_df)

# set the order of blocks (position dependence) and subblocks (preview time) according to counterbalance condition
if counterbalance == "1":
    blocks = (0, 1, 3, 4, 2)
    subblock_list = ((1, 2), (1, 2), (2, 1), (2, 1))
if counterbalance == "2":
    blocks = (0, 1, 3, 4, 2)
    subblock_list = ((2, 1), (2, 1), (1, 2), (1, 2))
elif counterbalance == "3":
    blocks = (0, 4, 2, 1, 3)
    subblock_list = ((1, 2), (1, 2), (2, 1), (2, 1))
elif counterbalance == "4":
    blocks = (0, 4, 2, 1, 3)
    subblock_list = ((2, 1), (2, 1), (1, 2), (1, 2))

print(blocks)
print(subblock_list)

exitParams = [age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
              strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
              informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
              screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed,  results,
              part, participant_id]

welcomParams = [expGlobals, screen_height, screen_width, screen, age_input, gender_input, handedness_input, hypothesis_input,
                regularities_input, strategy_input, strategy_effort_input, delayedPerc_input, hold_flag,
                perceptibility_input, other_input, diff_input, informed_consent, participated_earlier_input, effort_input,
                clock, thresh1Old, thresh2Old, accelOld, current_speed, results, part, participant_id]

start_welcome_block(*welcomParams) if part == 1 else print("Willkommen zu Teil 2!")

# setting the pertur_ratio
pertur_ratio = expGlobals["perturb"]

latest_reward = 0
latest_reward_duration = 0

trials = [x for x in range(1,
                           81)]  # change the range to adjust trial count; e.g. range(1, 7) would only run 6 trials per subblock; maximum is range(1, 57)
trials_copy = trials.copy()

# change mouse settings
change_speed(3)
set_mouse_acceleration()
thresh1New, thresh2New, accelNew = get_mouse_acceleration()

block_num = 0
trial_num = 1
subblock_counter = 0

# expGlobals["speed_multiplier"] *= 1

practice_error_dict = {"nError": 0, "nTrial": 0, "mFlag": True}

try:
    for idx, block in enumerate(blocks):
        if block == 0:
            trials = [x for x in range(1,
                                       25)]  # change the range to adjust practice trial count; e.g. range(1, 7) would only run 6 trials per subblock
            subblocks = [x for x in range(1, 5)]
        elif block != 0:
            subblocks = subblock_list[subblock_counter]  # don't change this
            subblock_counter += 1
        block_start = round(perf_counter(), 4)
        for sidx, subblock in enumerate(subblocks):
            if block != 0:
                trials = trials_copy
                block_num += 1
            # counter for errors in current subblock
            expGlobals["score"] = 0
            gate_errors = 0
            obstacle_errors = 0
            fall_errors = 0
            errors = 0
            # score before current subblock
            start_score = expGlobals["score"]

            # displaying different instructions for training blocks and
            # experimental blocks
            if block == 0:
                display_training_block_start(changeFreq, subblock)
            elif block != 0 and block_num != 0:
                display_block_start(block_num, len(blocks), errors_previous, score_previous,
                                    fall_errors_previous,
                                    obstacle_errors_previous)

            # print("Randomizing trials, please wait...")

            shuffle(trials)

            # print("Trials randomized!")

            # assign dependence conditions for current block / subblock
            dependence = cond_df[(cond_df["block"] == block)][
                "dependence"].unique()[0]

            # choose two random trials as warm-up trials before each subblock;
            # placing them in front of the other trials
            if block > 0:
                trials_practice = trials.copy()
                practice_trial_one = choice(trials_practice)
                trials_practice.remove(practice_trial_one)
                practice_trial_two = choice(trials_practice)
                del trials_practice
                practice_trials = [practice_trial_one, practice_trial_two]
                trials = practice_trials + trials
                # print("trials ", trials)
                # print(len(trials))
            no_input_counter = 0
            previous_no_input = 0
            error_in_prev_trial = 0
            for i, trial in enumerate(trials):
                practice_error_dict["nTrial"] += 1 if block == 0 else 0
                no_input_flag = 1
                bird, bird_group = create_bird(lane_height,
                                               aspect_ratio_scaler,
                                               screen_variables["middle_lane"])
                trial_start = round(perf_counter(), 4)
                display_stars_flag = 1  # flag to control the display of the stars
                ERROR = 0  # flag to control the execution of events (see event loop)
                error_type = "None"  # to fill in the error_type in the results file
                bird_group.add(bird)
                if block == 0:
                    # retrieve dependence condition for practice block
                    dependence = cond_df[(cond_df["block"] == block) &
                                         (cond_df["subblock"] == subblock)][
                        "dependence"].unique()[0]


                def get_results():
                    results["informed_consent"].append(informed_consent)
                    results["trial_num"].append(trial_num)
                    results["id"].append(participant_id)
                    results["counterbalance"].append(counterbalance)
                    results["changeFreq"].append(changeFreq)
                    results["age"].append(age_input)
                    results["gender"].append(gender_input)
                    results["part"].append(part)
                    results["handedness"].append(handedness_input)
                    results["screen_resolution_x"].append(screen_width)
                    results["screen_resolution_y"].append(screen_height)
                    results["trial"].append(trial)
                    results["block"].append(block)
                    results["subblock"].append(subblock)
                    results["dependence"].append(dependence)
                    results["pert_strength"].append(expGlobals["perturb"])
                    results["pert_direct"].append(direction)
                    results["reward_upper"].append(upper_value)
                    results["reward_lower"].append(lower_value)
                    results["preview_congr"].append(preview_congr)
                    results["bird_orientation"].append(bird_orientation)
                    results["jump"].append(jump)
                    results["bird_lane"].append(expGlobals["bird_lane"])
                    results["block_start"].append(block_start)
                    results["trial_start"].append(trial_start)
                    results["time_stamp"].append(round(perf_counter(), 4))
                    results["current_mouse_posx"].append(
                        pygame.mouse.get_pos()[0])
                    results["current_mouse_posy"].append(
                        pygame.mouse.get_pos()[1])
                    results["post_gate_rel_mouse_pos"].append(y_change)
                    results["score"].append(expGlobals["score"])
                    results["block_errors"].append(errors)
                    results["error_type"].append(error_type)
                    results["training"].append(1 if block == 0 else 0)
                    results["trial_display_start"].append(trial_display_start)
                    results["monitor_refresh_rate"].append(
                        monitor_refresh_rate)
                    results["gate_passed"].append(gate_passed)
                    results["stars_visible"].append(display_stars_flag)
                    results["bird_position"].append(bird.right_x)
                    results["obstacle_position"].append(
                        round(mid_obstacle.left_x, 5))
                    results["star_position"].append(round(up_star.left_x, 5))
                    results["gate_position"].append(round(up_gate.left_x, 5))
                    results["mouse_wheel_input"].append(mouse_wheel_input)


                gate_passed = 0
                jump = 0

                object_group = pygame.sprite.Group()
                star_group = pygame.sprite.Group()

                # print(block, subblock, trial)

                pert_direct, upper_value, lower_value, \
                pertur_strength, direction, preview_congr, last_change = set_trial_parameters(
                    cond_df, block,
                    subblock, trial)

                old_score = expGlobals["score"]

                if expGlobals["perturb"] == (screen_height / 100):
                    expGlobals["perturb"] = round(
                        pertur_ratio * pertur_strength, 5)

                start_trial(direction, star_group, screen, expGlobals,
                            trial_data,
                            bird,
                            screen_variables, lane_height)

                mid_obstacle = create_obstacle(lane_height,
                                               aspect_ratio_scaler,
                                               expGlobals["obstacle_position"],
                                               screen_variables["middle_lane"])

                up_gate, low_gate = create_gate(lane_height,
                                                aspect_ratio_scaler,
                                                expGlobals["gate_position"],
                                                screen_variables["upper_lane"],
                                                screen_variables["lower_lane"])

                upper_val, lower_val = upper_value, lower_value

                scored = True

                up_star, low_star = create_stars(upper_value, lower_value,
                                                 lane_height,
                                                 aspect_ratio_scaler,
                                                 expGlobals["star_position"],
                                                 screen_variables[
                                                     "lower_lane"],
                                                 screen_variables[
                                                     "upper_lane"])
                object_group.add([mid_obstacle, low_gate, up_gate])
                star_group.add([up_star, low_star])

                # used to adjust jumping threshold according to bird_orientation
                modifier = (expGlobals["orientation_weight"] * dependence) * (
                    -1)

                trial_display_start = round(perf_counter(), 4)

                freeze_flag = 1

                if freeze_flag == 1:
                    # this condition stops the trial after one frame so that
                    # participants have about 1 second to readjust their hand
                    # and mouse position
                    pygame.event.clear(PERTURB)
                    pygame.event.clear()

                    bird_orientation = 0
                    bird.current_sprite = 0
                    bird.true_y = screen_variables["middle_lane"]
                    bird.screen_y = screen_variables["middle_lane"]
                    bird.animate()
                    bird.rotate(0, dependence)

                    pygame.event.clear(PERTURB)

                    draw_background(screen, screen_variables["bgColor"],
                                    screen_variables["laneColor"],
                                    upper_lane, middle_lane, lower_lane)
                    if i > 0:
                        latest_reward_duration = round(perf_counter(),
                                                       4) - trial_display_start

                    bird_group.draw(screen)

                    score_display(expGlobals["game_font"], expGlobals["score"],
                                  screen_width,
                                  screen_height, screen)

                    pygame.display.flip()

                    freeze_flag = 0

                    running = 1

                    start_time = round(perf_counter(), 10)
                    while running:
                        current_time = round(perf_counter(), 10)
                        if i > 0:
                            draw_background(screen,
                                            screen_variables["bgColor"],
                                            screen_variables["laneColor"],
                                            upper_lane, middle_lane,
                                            lower_lane)
                            score_display(expGlobals["game_font"],
                                          expGlobals["score"],
                                          screen_width,
                                          screen_height, screen)
                            if not error_in_prev_trial:
                                latest_score_display(latest_reward,
                                                     latest_reward_duration,
                                                     expGlobals["game_font"],
                                                     screen_width,
                                                     screen_height,
                                                     screen)
                            latest_reward_duration = round(perf_counter(),
                                                           4) - trial_display_start

                            bird_group.draw(screen)

                        pygame.display.flip()
                        if current_time - start_time >= 1.0:
                            running = 0
                            pygame.event.clear()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = 0
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    confirm_exit(*exitParams)

                        pygame.mouse.set_pos(screen_variables["x_pos"],
                                             screen_variables["y_pos"])

                        clock.tick(100)

                # get starting position for the mouse cursor
                start_cursor_y = pygame.mouse.get_pos()[1]
                new_cursor_y = pygame.mouse.get_pos()[1]

                # first update time point
                last_time = perf_counter()

                collision_time = 4.0

                # print("Start cursor ", start_cursor_y)

                time_start_flag = 1
                # switch_time = round(perf_counter(), 10)
                time_flag_1 = 1
                time_flag_2 = 1
                time_flag_3 = 1
                time_flag_4 = 1

                while expGlobals["game_active"]:
                    time_start = perf_counter() if time_start_flag else time_start
                    time_start_flag = 0
                    draw_background(screen, screen_variables["bgColor"],
                                    screen_variables["laneColor"],
                                    upper_lane, middle_lane, lower_lane)

                    dt = (perf_counter() - last_time) * 100
                    time_since_start = round(perf_counter() - time_start, 2)
                    # print("Trial update! ", time_since_start)
                    # print(direction)
                    last_time = round(perf_counter(), 10)
                    current_trial_duration = round(perf_counter(), 4)
                    bird_y = bird.true_y
                    lane_y = screen_variables[
                        expGlobals["bird_lane"] + "_lane"]
                    bird_orientation = round(lane_y - bird_y, 5)

                    time_since_start, time_flag_1, time_flag_2, time_flag_3, time_flag_4, PERTURB, direction, bird, \
                    lane_y = switch_perturbation_direction(time_since_start, time_flag_1, time_flag_2, time_flag_3,
                                                           time_flag_4, PERTURB, direction, bird, lane_y, last_change)

                    # print("Gate Passed: ", gate_passed)

                    # get starting position for the mouse cursor
                    new_cursor_y = pygame.mouse.get_pos()[1]

                    # print("New Cursor ", new_cursor_y)

                    y_change = start_cursor_y - new_cursor_y
                    mouse_wheel_input = 0
                    # screen.blit(update_fps(clock, expGlobals["font"]), (10, 0))
                    # print("upper screen bound ", new_cursor_y < 5)
                    # print("lower screen bound ", new_cursor_y > (screen_height - 5))
                    if (new_cursor_y < 5) or (
                            new_cursor_y > (screen_height - 5)):
                        # print(abs(y_change) >= (screen_height // 2 - 40))
                        y_change = expGlobals["upper_jump_boundary"] + 1 if y_change > 0 else expGlobals[
                                                                                                  "lower_jump_boundary"]-1
                    else:
                        y_change -= bird_orientation / modifier

                    if not gate_passed and time_since_start < 3.2 and \
                            abs(
                                start_cursor_y - new_cursor_y) > screen_height / 7:
                        error_in_prev_trial = 1
                        pygame.event.clear(PERTURB)
                        errors += 1
                        if block == 0:
                            practice_error_dict["nError"] += 1
                        error_type = "mouse_movement"
                        bird_group.empty()
                        bird.kill()
                        display_error(
                            "Du hast die Maus zu früh bewegt!",
                            trial_display_start)
                        expGlobals["game_active"] = 0

                    elif not gate_passed and 3.2 <= time_since_start <= \
                            3.25:
                        start_cursor_y = pygame.mouse.get_pos()[1]
                        new_cursor_y = pygame.mouse.get_pos()[1]

                    elif gate_passed and not ((y_change < expGlobals[
                        "lower_jump_boundary"]) or y_change >
                                              expGlobals[
                                                  "upper_jump_boundary"]):
                        new_cursor_y = pygame.mouse.get_pos()[1]

                    elif gate_passed and (y_change < expGlobals[
                        "lower_jump_boundary"] or y_change > expGlobals[
                                              "upper_jump_boundary"]) and jump == 0:

                        # print("Time of jump ",
                        #      round(perf_counter(), 4) - trial_start)

                        if y_change > expGlobals["upper_jump_boundary"]:

                            if expGlobals[
                                "bird_lane"] == "middle" and jump == 0:
                                jump += 1
                                expGlobals["bird_lane"] = "upper"

                                bird.true_y = screen_variables[
                                                  "upper_lane"] - \
                                              bird_orientation
                                bird.rect.center = (
                                    2 * lane_height, bird.true_y)
                                start_cursor_y = pygame.mouse.get_pos()[1]
                                new_cursor_y = pygame.mouse.get_pos()[1]

                        elif y_change < expGlobals["lower_jump_boundary"]:

                            if expGlobals[
                                "bird_lane"] == "middle" and jump == 0:
                                jump += 1
                                expGlobals["bird_lane"] = "lower"

                                bird.true_y = screen_variables[
                                                  "lower_lane"] - \
                                              bird_orientation

                                bird.rect.center = (2 * lane_height,
                                                    bird.true_y)
                                start_cursor_y = pygame.mouse.get_pos()[1]
                                new_cursor_y = pygame.mouse.get_pos()[1]

                        start_cursor_y = pygame.mouse.get_pos()[1]

                    if expGlobals["game_active"] is True and not ERROR:
                        # display_debug_rectangles(screen, screen_variables, screen_width, lane_height,
                        #                              bird)
                        bird.update(0, 0)
                        object_group.update(expGlobals["object_speed"] * dt)

                        star_group.update(expGlobals["object_speed"] * dt)

                        bird_group.draw(screen)
                        # print(expGlobals["previewDict"][preview_congr])
                        if time_since_start >= (
                                collision_time - expGlobals["previewDict"][preview_congr]):
                            points_display_bird(trial, block, subblock,
                                                bird,
                                                bird,
                                                expGlobals["game_font"],
                                                cond_df,
                                                screen_height, screen)
                            star_group.draw(screen)
                            object_group.draw(screen)
                            if display_stars_flag == 1:
                                # print("Stars are visible")

                                display_stars_flag = 0

                        score_display(expGlobals["game_font"],
                                      expGlobals["score"],
                                      screen_width,
                                      screen_height, screen)
                        if i > 0 and not error_in_prev_trial:
                            latest_score_display(latest_reward,
                                                 latest_reward_duration,
                                                 expGlobals["game_font"],
                                                 screen_width, screen_height,
                                                 screen)

                        # if not 0 <= up_gate.rect.center[0] <= screen_width:
                        #     object_group.remove([up_gate, low_gate])

                        gate_passed = 1 if time_since_start >= 3.25 else 0

                        scored, expGlobals["score"] = check_scoring(
                            [up_star, low_star],
                            upper_value,
                            lower_value, expGlobals["bird_lane"], bird,
                            trial_data["ending_time"],
                            expGlobals["score"], time_since_start,
                            collision_time)

                        # if time_since_start >= collision_time and \
                        #         expGlobals["bird_lane"] in ("middle"):
                        #     print("COLLISION")

                        collidedObst, expGlobals["score"] = (0, expGlobals[
                            "score"] - 30) if time_since_start >= collision_time and \
                                              expGlobals["bird_lane"] in (
                                                  "middle") else \
                            (1, expGlobals["score"])

                        if gate_passed:

                            if not scored:
                                ERROR = 1
                                bird_group.empty()
                                bird.kill()
                                pygame.event.clear(PERTURB)
                                pygame.event.clear()
                                trial_data["ending_time"] = perf_counter()

                                expGlobals["game_active"] = 0

                            if not collidedObst:
                                # print("Collision Time ",
                                #       round(perf_counter(),
                                #             4) - trial_display_start)
                                pygame.event.clear(PERTURB)
                                if block == 0:
                                    practice_error_dict["nError"] += 1
                                errors += 1
                                obstacle_errors += 1
                                error_type = "obstacle"
                                bird_group.empty()
                                bird.kill()
                                bird, bird_group = display_error(
                                    "Oh nein, die Katze auf der mittleren Bahn hat Dich gefressen!",
                                    trial_display_start)
                                error_in_prev_trial = 0

                                expGlobals["game_active"] = 0
                    if freeze_flag == 0:
                        for event in pygame.event.get():

                            if event.type == PERTURB and expGlobals["game_active"] and not ERROR:
                                new_cursor_y = pygame.mouse.get_pos()[1]

                                if direction:
                                    bird_group.update(0,
                                                      expGlobals[
                                                          "perturb"] * dt)
                                    bird.animate()
                                    bird.rotate(bird_orientation, dependence)

                                else:
                                    bird_group.update(0,
                                                      -expGlobals[
                                                          "perturb"] * dt)
                                    bird.animate()
                                    bird.rotate(bird_orientation, dependence)

                            if event.type == PERTURBVAR and expGlobals["game_active"] and not ERROR:
                                expGlobals["perturb"] = round((
                                                                      pertur_ratio * pertur_strength) * uniform(
                                    0.5, 1), 5)
                            if event.type == pygame.QUIT:
                                confirm_exit(*exitParams)
                            if event.type == pygame.MOUSEBUTTONDOWN and \
                                    expGlobals[
                                        "game_active"] and not ERROR:
                                if event.button == 4 and direction == 1:
                                    bird_group.update(0, -expGlobals["scrollPar"] * dt)
                                    mouse_wheel_input = 1
                                    no_input_flag = 0
                                if event.button == 5 and direction == 0:
                                    bird_group.update(0, expGlobals["scrollPar"] * dt)
                                    mouse_wheel_input = 1
                                    no_input_flag = 0

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE and expGlobals["game_active"] is False:
                                    expGlobals["game_active"] = 1
                                    start_cursor_y = pygame.mouse.get_pos()[1]
                                    expGlobals["bird_lane"] = "middle"
                                    bird_group.update(lane_height * 2,
                                                      screen_variables[
                                                          "middle_lane"])
                                if event.key == pygame.K_ESCAPE:
                                    confirm_exit(*exitParams)
                    bird_too_far_up, bird_too_far_down = screen_variables[
                                                             expGlobals[
                                                                 "bird_lane"] + "_lane"] > \
                                                         bird.true_y + \
                                                         lane_height / 1.175, \
                                                         bird.true_y - lane_height / 1.175 > \
                                                         screen_variables[
                                                             expGlobals[
                                                                 "bird_lane"] + "_lane"]

                    if bird_too_far_up or bird_too_far_down and not \
                            ERROR:
                        pygame.event.clear(PERTURB)
                        ERROR = 1
                        trial_data["ending_time"] = perf_counter()
                        error_type = "fall"
                        expGlobals["score"] -= 30
                        fall_errors += 1
                        if block == 0:
                            practice_error_dict["nError"] += 1
                        errors += 1
                        bird_group.empty()
                        bird.kill()
                        bird, bird_group = display_error(
                            "Der Vogel wurde von der Bahn geweht!",
                            trial_display_start)

                        expGlobals["game_active"] = 0
                        error_in_prev_trial = 0

                    pygame.display.flip()

                    clock.tick_busy_loop(100)

                    new_score = expGlobals["score"]
                    added_score = new_score - old_score
                    if added_score != 0:
                        latest_reward = added_score
                    latest_reward_duration = round(perf_counter(),
                                                   4) - trial_display_start
                    higher_reward = max(upper_value, lower_value)

                    if added_score < 0 and not scored:
                        pygame.event.clear(PERTURB)
                        errors += 1
                        gate_errors += 1
                        error_type = "outer_lane"
                        bird_group.empty()
                        bird.kill()
                        bird, bird_group = display_error(
                            "Oh nein, eine Katze auf den äußeren Bahnen hat Dich gefressen!",
                            trial_display_start)

                        expGlobals["game_active"] = 0
                        error_in_prev_trial = 0

                    if not scored and higher_reward == added_score:
                        results["higher_reward"].append(1)
                        results["reward_collected"].append(added_score)
                        error_in_prev_trial = 0
                    elif not scored and higher_reward != added_score:
                        results["higher_reward"].append(0)
                        results["reward_collected"].append(added_score)
                        error_in_prev_trial = 0
                    else:
                        results["reward_collected"].append(added_score)
                        results["higher_reward"].append(99)

                    get_results()

                # for key in results.keys():
                #     (key, len(results[key]))

                trial_end = round(perf_counter(), 4)

                trial_duration = trial_end - trial_display_start

                trial_num += 1

                if no_input_flag and previous_no_input:
                    no_input_counter += 1
                    # print(no_input_counter)
                    if no_input_counter >= 2:
                        confirm_exit(*exitParams)
                        no_input_counter = 0
                elif no_input_flag:
                    previous_no_input = 1
                else:
                    previous_no_input = 0
                    no_input_counter = 0

                # print("TRIAL DURATION ", trial_duration)

            if block == 0:
                expGlobals["score"] = 0
                score_previous = 0
                errors_previous = 0
                fall_errors_previous, obstacle_errors_previous = \
                    0, 0
            else:
                errors_previous = errors
                score_previous = expGlobals["score"] - start_score
                expGlobals["score_total"] += expGlobals["score"]
                fall_errors_previous, obstacle_errors_previous = \
                    fall_errors, obstacle_errors
                expGlobals["eaten_total"] += obstacle_errors
                expGlobals["falls_total"] += fall_errors

    change_speed(current_speed)

    set_mouse_acceleration(thresh1Old, thresh2Old, accelOld)
    thresh1New, thresh2New, accelNew = get_mouse_acceleration()

    pygame.quit()

    hypothesis_input, regularities_input, strategy_input, \
    strategy_effort_input, \
    delayedPerc_input, diff_input, effort_input, \
    perceptibility_input, \
    hold_flag, other_input, participated_earlier_input = run_post_experiment_questionnaires(
        participant_id,
        expGlobals[
            "score_total"],
        expGlobals[
            "falls_total"],
        expGlobals[
            "eaten_total"])

    while hold_flag:
        pass

    fill_question_entries(hypothesis_input, regularities_input,
                          strategy_input, strategy_effort_input,
                          delayedPerc_input,
                          diff_input, effort_input,
                          perceptibility_input,
                          hold_flag, other_input,
                          participated_earlier_input, results)

    results_df = DataFrame.from_dict(results)

    results_df.to_csv("MLTT_Ayesh_results.csv", sep=";")

    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]

    print("Daten werden verpackt, bitte warten...")

    pyminizip.compress("MLTT_Ayesh_results.csv", None,
                       "ERGEBNISSE_" + str(participant_id) + "_" + current_date + ".zip",
                       "crosstalk2022", 9)

    print("Daten verpackt!")

    if os.path.exists("MLTT_Ayesh_results.csv"):
        os.remove("MLTT_Ayesh_results.csv")
    else:
        print("MLTT_Ayesh_results.csv does not exist!")

    sys.exit()

except Exception:

    change_speed(current_speed)

    set_mouse_acceleration(thresh1Old, thresh2Old, accelOld)
    thresh1New, thresh2New, accelNew = get_mouse_acceleration()

    pygame.quit()

    hypothesis_input, regularities_input, strategy_input, strategy_effort_input, \
    delayedPerc_input, \
    diff_input, effort_input, perceptibility_input, \
    hold_flag, other_input, participated_earlier_input = run_post_experiment_questionnaires(
        participant_id,
        expGlobals[
            "score_total"],
        expGlobals[
            "falls_total"],
        expGlobals[
            "eaten_total"])


    while hold_flag:
        pass

    results = fill_question_entries(hypothesis_input, regularities_input,
                          strategy_input, strategy_effort_input,
                          delayedPerc_input,
                          diff_input, effort_input,
                          perceptibility_input,
                          hold_flag, other_input,
                          participated_earlier_input, results)

    results_df = DataFrame.from_dict(results)

    results_df.to_csv("MLTT_Ayesh_results.csv", sep=";")

    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]

    print("Daten werden verpackt, bitte warten...")

    pyminizip.compress("MLTT_Ayesh_results.csv", None,
                       "ERGEBNISSE_" + str(participant_id) + "_" + current_date + "_CRASH_" + ".zip",
                       "crosstalk2022", 9)

    print("Daten verpackt!")


    if os.path.exists("MLTT_Ayesh_results.csv"):
        os.remove("MLTT_Ayesh_results.csv")
    else:
        print("MLTT_Ayesh_results.csv does not exist!")

    sleep(5)
    sys.exit()

# else:
#   ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,
#                                       __file__, None, 1)
