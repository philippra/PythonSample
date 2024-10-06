import sys
import os
import pygame
from win32api import EnumDisplaySettings, EnumDisplayDevices, ShellExecute
import ctypes
from time import perf_counter
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
from Post_Experiment import *

def is_admin():
    """From https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script/41930586#41930586,
    Author: Martin De la Fuente"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def resource_path(relative_path):
    '''
    Constructs the complete path for a file
    :param relative_path: path relative to the current folder
    :return: absolute path of the given file
    '''

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def set_screen_vars(true_res):
    screen = pygame.display.set_mode(true_res,
                                 pygame.FULLSCREEN)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    screen_surface = pygame.Surface((screen_width, screen_height))

    return screen, screen_width, screen_height, screen_surface


def initialize_sprite_groups():
    star_group = pygame.sprite.Group()

    obst_group = pygame.sprite.Group()

    gates_group = pygame.sprite.Group()

    return star_group, obst_group, gates_group


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


def set_mouse_acceleration(thresh1=0, thresh2=0, accel=0):
    """This function sets the mouse acceleration.
    :return None"""
    set_mouse = 4  # 0x0004 for SPI_SETMOUSE
    array_type = ctypes.c_int * 3
    aSetAccel = array_type()
    aSetAccel[0], aSetAccel[1], aSetAccel[2] = thresh1, thresh2, accel

    ctypes.windll.user32.SystemParametersInfoA(set_mouse, 0,
                                               ctypes.byref(aSetAccel), 0)


def change_speed(speed=10):
    """Written by CommonSense, stackoverflow
    (https://stackoverflow.com/questions/45100234/change-mouse-pointer-speed-in-windows-using-python)
    Changes the cursor speed.
    :return None
    """
    #   1 - slow
    #   10 - standard
    #   20 - fast
    set_mouse_speed = 113  # 0x0071 for SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)


def draw_background(screen, bgColor, laneColor, upper_lane, middle_lane, lower_lane):
    """
    Draws a (black) background with three white lanes positioned horizontally.
    """
    screen.fill(bgColor)
    pygame.draw.rect(screen, laneColor, upper_lane)
    pygame.draw.rect(screen, laneColor, middle_lane)
    pygame.draw.rect(screen, laneColor, lower_lane)


def create_bird(lane_height, aspect_ratio_scaler, middle_lane):
    """
    Creates a bird the participant can control
    :return: bird: a bird object, bird_group: a sprite group containing the created bird object
    """
    from Classes import Bird
    bird = Bird(int((lane_height / 2 + lane_height / 6)),
                int((lane_height / 2 + lane_height / 6 * aspect_ratio_scaler)),
                int((lane_height * 2) * aspect_ratio_scaler),
                middle_lane)
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)
    return bird, bird_group


def create_stars(upper_value, lower_value, lane_height, aspect_ratio_scaler, star_position, lower_lane, upper_lane):
    """
    This function creates the reward stars on the upper and lower lane, respectively.
    :param upper_value (int)
    :param lower_value (int)
    :return: upper_star, lower_star: pygame.Rect objects
    """
    from Classes import Obstacle, Star
    if lower_value == -50:
        lower_star = Obstacle(int(lane_height),
                              int(lane_height * aspect_ratio_scaler),
                              star_position,
                              lower_lane)
        upper_star = Star(int((lane_height * (upper_value / 60))),
                          int((lane_height * (
                                  upper_value / 60)) * aspect_ratio_scaler),
                          star_position,
                          upper_lane, lane_height,
                          lane_height)
    elif upper_value == -50:
        upper_star = Obstacle(int(lane_height),
                              int(lane_height * aspect_ratio_scaler),
                              star_position,
                              upper_lane)
        lower_star = Star(int(lane_height * (lower_value / 60)),
                          int((lane_height * (
                                  lower_value / 60)) * aspect_ratio_scaler),
                          star_position,
                          lower_lane, lane_height,
                          lane_height)
    else:
        lower_star = Star(int((lane_height * (50 / 60))), # equal size
                          int((lane_height * (
                                  50 / 60)) * aspect_ratio_scaler),
                          star_position,
                          lower_lane, lane_height,
                          lane_height)
        upper_star = Star(int((lane_height * (50 / 60))), # equal size
                          int((lane_height * (
                                  50 / 60)) * aspect_ratio_scaler),
                          star_position,
                          upper_lane, lane_height,
                          lane_height)
    return upper_star, lower_star


def create_obstacle(lane_height, aspect_ratio_scaler, obstacle_position, middle_lane):
    """
    Creates an obstacle for the middle lane.
    :return: mid_obstacle (Obstacle)
    """
    from Classes import  Obstacle
    mid_obstacle = Obstacle(int(lane_height),
                            int(lane_height * aspect_ratio_scaler),
                            obstacle_position,
                            middle_lane)
    return mid_obstacle


def create_gate(lane_height, aspect_ratio_scaler, gate_position, upper_lane, lower_lane):
    """
    Creates the gate for the gates sprite group.
    :return: upper_gate, lower_gate: Obstacle objects
    """
    from Classes import Obstacle
    upper_gate = Obstacle(int(lane_height),
                          int(lane_height * aspect_ratio_scaler),
                          gate_position,
                          upper_lane)
    lower_gate = Obstacle(lane_height, lane_height * aspect_ratio_scaler,
                          gate_position,
                          lower_lane)
    return upper_gate, lower_gate


def switch_perturbation_direction(time_since_start, time_flag_1, time_flag_2, time_flag_3, time_flag_4, PERTURB, direction,
                                  bird, lane_y, last_change):
    if 2. > time_since_start >= 1. and time_flag_1:
        pygame.event.clear(PERTURB)
        direction = 1 if direction == 0 else 0
        bird.true_y = lane_y + 0.5 * (lane_y - bird.true_y)
        time_flag_1 = 0
    elif 3. > time_since_start >= 2. and time_flag_2:
        pygame.event.clear(PERTURB)
        direction = 1 if direction == 0 else 0
        bird.true_y = lane_y + 0.5 * (lane_y - bird.true_y)
        time_flag_2 = 0
    elif 4. > time_since_start >= 3. and time_flag_3 and last_change:
        pygame.event.clear(PERTURB)
        direction = 1 if direction == 0 else 0
        bird.true_y = lane_y + 0.5 * (lane_y - bird.true_y)
        time_flag_3 = 0
    elif time_since_start >= 4. and time_flag_4:
        pygame.event.clear(PERTURB)
        direction = 1 if direction == 0 else 0
        bird.true_y = lane_y + 0.5 * (lane_y - bird.true_y)
        time_flag_4 = 0

    return time_since_start, time_flag_1, time_flag_2, time_flag_3, time_flag_4, PERTURB, direction, bird, lane_y


def check_gate_collision(gates, passed, bird_lane, bird, ending_time, score):
    """
    Checks if the participant has collided with a gate. The true x coordinates are used for computing collisions.
    :param gates: sprite group containing the gate objects.
    :param passed: Flag which represents whether the player has passed the gate objects.
    :return: True if no gate collision, False if gate collision
    """

    if bird_lane in ("lower", "upper") and not passed:
        for gate in gates:
            if bird.right_x >= gate.left_x:
                ending_time = perf_counter()
                # print("COLLISION!!!")
                score -= 50
                return False
    return True


def check_obst_collision(obst, bird_lane, bird, ending_time, score):
    """
    Checks if the player has collided with the central obstacle.
    :param obst: central obstacle object
    :return: True if participant has not collided, else False.
    """
    if bird_lane in ("middle"):
        # print("BIRD ", bird.right_x, "\\n", "OBST ", obst.left_x)
        if (bird.true_x + bird.height / 2) >= (obst.true_x - obst.height / 2):
            ending_time = perf_counter()
            # print("COLLISION!!!")
            score -= 50
            return False, score
    return True, score


def check_scoring(stars, upper_value, lower_value, bird_lane, bird,
                  ending_time, score, current_time, collision_time):
    """
    Checks if the player has scored, i.e. has collided with a star on the upper or lower lane.
    :param stars: sprite group containing the star objects.
    :param upper_value (int): reward for the collecting the upper star.
    :param lower_value (int): reward for collectiong the lower_star.
    :return: True if player has not scored, else False.
    """

    if bird_lane in ("upper", "lower"):
        for star in stars:
            if current_time >= (collision_time+0.75):
                ending_time = perf_counter()
                # print("Time since trial start: ",
                #     trial_data["ending_time"] - trial_data["starting_time"])
                if bird_lane == "upper":
                    score += upper_value

                    return False, score
                if bird_lane == "lower":
                    score += lower_value

                    return False, score
    return True, score


def check_gate_passing(gates, bird, x_pos, y_pos):
    """
    Checks if the player has passed the gate.
    :param gates: sprite group containing the gate objects.
    :return: True if gate was passed, else False.
    """
    check_list = []
    for gate in gates:
        if (bird.true_x - bird.height / 2) >= (gate.true_x + gate.height / 2):
            check_list.append(1)
        else:
            check_list.append(0)
            # pygame.mouse.set_pos(x_pos,
            #                      y_pos)
    if any(check_list):
        return True
    else:
        return False


def start_welcome_block(expGlobals, screen_height, screen_width, screen, age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, clock, thresh1Old, thresh2Old, accelOld,
                 current_speed, results, part, participant_id):
    """Presents welcome and instruction text to participant;
    see https://github.com/imarevic/psy_python_course/blob/master/notebooks/Chapter8/InstructionPresentation.ipynb"""

    # set background
    expGlobals["screen"].fill(expGlobals["bgColor"])
    i = 1
    while i < 9:
        expGlobals["continue"] = 0
        instructions = load_instructions("Instruktion_" + str(i) + ".txt")
        inst_coords = (
            expGlobals["screenRect"].centerx - (expGlobals["instWidth"] // 2),
            expGlobals[
                "screenRect"].centery - screen_height // 2.25)

        y_axis = inst_coords[1]
        if i < 7:
            inst_image = pygame.transform.scale(pygame.image.load(
                resource_path('pics\\Instruct_' + str(i) + ".png")),
                (int(round(
                    screen_width // 1.75)),
                 int(round(screen_height // 1.75)))). \
                convert_alpha()

            inst_image_rect = inst_image.get_rect()
            inst_image_rect.center = (
                expGlobals["screenRect"].centerx, expGlobals[
                    "screenRect"].centery + screen_height // 5)

        while expGlobals["continue"] != 1:
            expGlobals["screen"].fill(expGlobals["bgColor"])
            text_object_blit_wrapped(expGlobals["screen"], instructions,
                                     expGlobals["font"],
                                     expGlobals["instWidth"],
                                     expGlobals["instHeight"], inst_coords,
                                     expGlobals["textColor"]
                                     )
            if i < 7:
                screen.blit(inst_image, inst_image_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
                    elif event.key == pygame.K_r:
                        i = i - 1 if i > 1 else i
                        expGlobals["continue"] = 1
                    elif event.key == pygame.K_SPACE and not i == 9:
                        i += 1
                        expGlobals["continue"] = 1
                    # elif event.key == pygame.K_SPACE and i == 9:
                        # display_false_key_warning()
                    elif event.key == pygame.K_RETURN:
                        i += 1
                        expGlobals["continue"] = 1

            pygame.display.flip()


def confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id):
    """
    Displays a confirmation message to check if participant really wants to exit.
    :return: None.
    """

    pygame.event.clear()

    expGlobals["game_active"] = 0
    exit_surface = expGlobals["game_font"].render(
        str("Y-Taste (evtl. Z-Taste), um das Experiment abzubrechen. N-Taste, "
            "um zurückzukehren."), True, (255, 255, 255))
    exit_rect = exit_surface.get_rect(
        center=(screen_width // 2, screen_height // 4))
    instruction_surface = expGlobals["game_font"].render(
        str("I-Taste, um die Instruktionen erneut anzuzeigen."), True,
        (255, 255, 255))
    instruction_rect = instruction_surface.get_rect(
        center=(screen_width // 2, screen_height // 2))
    exit_running = 1

    while exit_running:
        screen.fill(expGlobals["bgColor"])
        screen.blit(exit_surface, exit_rect)
        screen.blit(instruction_surface, instruction_rect)
        pygame.display.flip()
        clock.tick_busy_loop(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_mouse_acceleration(thresh1Old, thresh2Old, accelOld)
                change_speed(current_speed)
                pygame.quit()

                hypothesis_input, regularities_input, strategy_input, strategy_effort_input, \
                delayedPerc_input, \
                diff_input, effort_input, perceptibility_input, \
                hold_flag, other_input, \
                participated_earlier_input = run_post_experiment_questionnaires(
                    participant_id,
                    expGlobals[
                        "score_total"],
                    expGlobals[
                        "falls_total"],
                    expGlobals[
                        "eaten_total"])

                while hold_flag:
                    pass

                fill_question_entries(hypothesis_input,
                                      regularities_input, strategy_input,
                                      strategy_effort_input,
                                      delayedPerc_input,
                                      diff_input,
                                      effort_input, perceptibility_input,
                                      hold_flag, other_input,
                                      participated_earlier_input, results)

                results_df = DataFrame.from_dict(results)

                results_df.to_csv("MLTT_Ayesh_results.csv", sep=";")

                now = datetime.now()
                current_date = now.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]

                print("Daten werden verpackt, bitte warten...")

                pyminizip.compress("MLTT_Ayesh_results.csv", None,
                                   "ERGEBNISSE_" + str(
                                       participant_id) + "_" + current_date + "-99" + ".zip",
                                   "crosstalk2022", 9)

                print("Daten verpackt!")

                if os.path.exists("MLTT_Ayesh_results.csv"):
                    os.remove("MLTT_Ayesh_results.csv")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    set_mouse_acceleration(thresh1Old, thresh2Old, accelOld)
                    change_speed(current_speed)
                    pygame.quit()

                    hypothesis_input, regularities_input, strategy_input, strategy_effort_input, \
                    delayedPerc_input, \
                    diff_input, effort_input, perceptibility_input, \
                    hold_flag, other_input, \
                    participated_earlier_input = run_post_experiment_questionnaires(
                        participant_id,
                        expGlobals[
                            "score_total"],
                        expGlobals[
                            "falls_total"],
                        expGlobals[
                            "eaten_total"])

                    while hold_flag:
                        pass

                    fill_question_entries(hypothesis_input,
                                          regularities_input,
                                          strategy_input,
                                          strategy_effort_input,
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
                                       "ERGEBNISSE_" + str(
                                           participant_id) + "_" + current_date + "-99" + ".zip",
                                       "crosstalk2022", 9)

                    print("Daten verpackt!")

                    if os.path.exists("MLTT_Ayesh_results.csv"):
                        os.remove("MLTT_Ayesh_results.csv")
                    sys.exit()
                if event.key == pygame.K_n:
                    exit_running = 0
                if event.key == pygame.K_i:
                    start_welcome_block(expGlobals, screen_height, screen_width, screen, age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, clock, thresh1Old, thresh2Old, accelOld,
                 current_speed, results, part, participant_id)
                    exit_running = 0

    pygame.event.clear()


def check_mousewheel(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id):
    """
    Check if the participant has a mouse with a wheel.
    :return: None.
    """
    pygame.event.clear()

    expGlobals["game_active"] = 0
    inst_surface = expGlobals["game_font"].render(
        str(
            "Für dieses Experiment benötigst Du eine Computer-Maus mit Mausrad."),
        True,
        (255, 255, 255))
    inst_rect = inst_surface.get_rect(
        center=(screen_width // 2, screen_height // 6))
    wheel_surface = expGlobals["game_font"].render(
        str("Bewege Dein Mausrad nun, um zu beginnen."), True, (255, 255, 255))
    wheel_rect = wheel_surface.get_rect(
        center=(screen_width // 2, screen_height // 3))
    esc_surface = expGlobals["game_font"].render(
        str("Drücke die Esc-Taste, um das Experiment zu beenden."), True,
        (255, 255, 255))
    esc_rect = esc_surface.get_rect(
        center=(screen_width // 2, screen_height // 2))
    wheel_running = 1

    while wheel_running:
        screen.fill(expGlobals["bgColor"])
        screen.blit(wheel_surface, wheel_rect)
        screen.blit(inst_surface, inst_rect)
        screen.blit(esc_surface, esc_rect)
        pygame.display.flip()
        clock.tick_busy_loop(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):
                    wheel_running = 0
    pygame.event.clear()


def process_space_event(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id):
    """Processes continue events;
    see https://github.com/imarevic/psy_python_course/blob/master/notebooks/Chapter8/InstructionPresentation.ipynb"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                confirm_exit(age_input, gender_input, handedness_input, hypothesis_input, regularities_input, strategy_input,
                 strategy_effort_input, delayedPerc_input, hold_flag, perceptibility_input, other_input, diff_input,
                 informed_consent, participated_earlier_input, effort_input, screen, expGlobals, screen_width,
                 screen_height, clock, thresh1Old, thresh2Old, accelOld, current_speed, results,
                 part, participant_id)
            elif event.key == pygame.K_SPACE:
                expGlobals["continue"] = 1


def get_display_frequency(device):
    """Script adapted from Smiley Barry; https://stackoverflow.com/questions/1225057/how-can-i-determine-the-monitor-refresh-rate
    """
    settings = EnumDisplaySettings(device.DeviceName, -1)
    # for varName in ['Color', 'BitsPerPel', 'DisplayFrequency']:
    #     print("%s: %s"%(varName, getattr(settings, varName)))
    return getattr(settings, 'DisplayFrequency')


def update_fps(clock, font):
    """
    Displays the current frames per second
    :return: fps_text: text object representing the current frames per second
    """
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def score_display(game_font, score, screen_w, screen_h, screen):
    """
    Displays the score on the screen
    :return:
    """

    score_surface = game_font.render(
        'Score: ' + str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(
        center=(screen_w // 8, screen_h // 16))
    screen.blit(score_surface, score_rect)


def latest_score_display(latest_reward, display_duration, game_font, screen_w,
                         screen_h, screen):
    """
    Displayes the latest reward
    :return:
    """

    sign = "+" if latest_reward >= 0 else "-"
    color = (0, 255, 0) if latest_reward >= 0 else (255, 0, 0)
    latest_surface = game_font.render(
        sign + " " + str(abs(int(latest_reward))), True, color)
    latest_rect = latest_surface.get_rect(
        center=(screen_w // 6.5, screen_h // 8))
    if display_duration < 2.0:
        screen.blit(latest_surface, latest_rect)


def points_display(trial, block, subblock, up_star, low_star, game_font,
                   cond_df, screen_h, screen):
    """
    Displays the points awarded for collecting each star.
    :param trial (int): current trial
    :param block (int): current block
    :param subblock (int): current subblock
    :param up_star (Star): star object upper lane
    :param low_star (Star): star object lower lane
    :return: None
    """
    upper_surface = game_font.render(str(
        cond_df[
            (cond_df["block"] == block) & (cond_df["subblock"] == subblock) & (
                    cond_df["trial"] == trial)][
            "reward_upper"].unique()[0]), False,
        (255, 255, 255))
    upper_rect = upper_surface.get_rect(center=(
        up_star.rect.center[0], up_star.rect.center[1] - screen_h // 8))
    screen.blit(upper_surface, upper_rect)

    lower_surface = game_font.render(str(
        cond_df[
            (cond_df["block"] == block) & (cond_df["subblock"] == subblock) & (
                    cond_df["trial"] == trial)][
            "reward_lower"].unique()[0]), False,
        (255, 255, 255))
    lower_rect = lower_surface.get_rect(center=(
        low_star.rect.center[0], low_star.rect.center[1] + screen_h // 8))
    screen.blit(lower_surface, lower_rect)


def points_display_bird(trial, block, subblock, up_star, low_star, game_font,
                   cond_df, screen_h, screen):
    """
    Displays the points awarded for collecting each star.
    :param trial (int): current trial
    :param block (int): current block
    :param subblock (int): current subblock
    :param up_star (Star): star object upper lane
    :param low_star (Star): star object lower lane
    :return: None
    """

    color = (255, 255, 255)
    upper_surface = game_font.render(str(
        cond_df[
            (cond_df["block"] == block) & (cond_df["subblock"] == subblock) & (
                    cond_df["trial"] == trial)][
            "reward_upper"].unique()[0]), False,
        color)
    upper_rect = upper_surface.get_rect(center=(
        up_star.rect.center[0] + up_star.rad*2, ((screen_h / 8) * 4 +
                                                 (screen_h / 8) * 2)//2))
    screen.blit(upper_surface, upper_rect)

    lower_surface = game_font.render(str(
        cond_df[
            (cond_df["block"] == block) & (cond_df["subblock"] == subblock) & (
                    cond_df["trial"] == trial)][
            "reward_lower"].unique()[0]), False,
        color)
    lower_rect = lower_surface.get_rect(center=(
        low_star.rect.center[0] + up_star.rad*2, ((screen_h / 8) * 4 +
                                                  (screen_h / 8) * 6)//2))
    screen.blit(lower_surface, lower_rect)


def text_object(text, font, width, height):
    """THIS FUNCTION WAS WRITTEN BY IMAREVIC;
    https://github.com/imarevic/psy_python_course/blob/master/notebooks/Chapter8/TextPresenter.py"""
    """splits text by lines and renders each line."""

    paragraphSize = (width, height)
    fontSize = font.get_height()

    # create a surface for the text paragraph
    paragraphSurface = pygame.Surface(paragraphSize)

    # set colorkey to create transparent paragraph surface
    paragraphSurface.fill((0, 0, 0))
    paragraphSurface.set_colorkey((0, 0, 0))

    # split the lines of the text block
    splitLines = text.splitlines()

    # center the text vertically
    offSet = (paragraphSize[1] - len(splitLines) * (fontSize + 1)) // 2

    # loop over lines and blit each line
    for idx, line in enumerate(splitLines):
        currentTextline = font.render(line, True, (255, 255, 255))
        currentPosition = (
            (paragraphSize[0] - currentTextline.get_width()) // 2,
            # x-coordinate
            idx * fontSize + offSet)  # y-coordinate
        paragraphSurface.blit(currentTextline, currentPosition)

    return paragraphSurface


def text_object_blit_wrapped(surface, text, font, width, height, position,
                             color):
    """THIS MODULE WAS WRITTEN BY IMAREVIC;
    https://github.com/imarevic/psy_python_course/blob/master/notebooks/Chapter8/TextPresenter.py"""
    """
    blits text on multiple lines while wrapping text onto new line whenever it exceeds the width that is specified
    """

    # get list of words row wise
    words = [word.split(' ') for word in text.splitlines()]
    # get size of spaces
    space = font.size(' ')[0]
    # unpack tuple for x and y coordinates of the text object
    xPos, yPos = position

    # iterate over words and lines
    for line in words:
        for word in line:
            # create words surface and get width and height of current words
            wordSurface = font.render(word, 1, color)
            wordWidth, wordHeight = wordSurface.get_size()

            # check if new line needs to be started
            if xPos + wordWidth >= width:
                # reset position to new line coordinates
                xPos = position[0]
                yPos += wordHeight

            # blit current word and update position
            surface.blit(wordSurface, (xPos, yPos))
            xPos += wordWidth + space

        # reset positions for each new line
        xPos = position[0]
        yPos += wordHeight


def read_in_conds(pathway):
    '''
    Reads the Exp_Conditions.csv file and constructs a pandas data frame
    :return: cond_df: pandas data frame
    '''
    from pandas import DataFrame, read_csv
    with open(pathway, newline='') as csvfile:
        cond_df = read_csv(csvfile, sep=';')

        return cond_df


def prepare_cond_df(cond_df):

    # renaming columns of the cond_df data frame
    cond_df.columns = ["trial", "block", "subblock", "dependence",
                       "pertur_strength", "reward_upper", "reward_lower",
                       "pert_direct", "training", "preview", "last_change"]

    # adjust penalty for obstacle collisions - not in current exp
    # cond_df.loc[cond_df["reward_upper"] == -100, "reward_upper"] = -50
    # cond_df.loc[cond_df["reward_lower"] == -100, "reward_lower"] = -50
    return cond_df


def load_instructions(filename):
    """
    Loads the instructions from a .txt file;
    see https://github.com/imarevic/psy_python_course/blob/master/notebooks/Chapter8/InstructionPresentation.ipynb

    :return: infile: string object containing the text from the file
    """
    import codecs
    instPath = resource_path("files\\" + filename)

    with codecs.open(instPath, 'r', 'utf-8') as file:
        infile = file.read()
    return infile


def fill_question_entries(hypothesis_input, regularities_input, strategy_one_input, strategy_two_input,
                          strategy_three_input,
                         diff_input, effort_input, perceptibility_input,
                          hold_flag, other_input, participated_earlier_input,
                          results):
    fill_keys = [
        ("hypothesis", hypothesis_input),
        ("regularities", regularities_input),
        ("strategy", strategy_one_input),
        ("strategy_effort", strategy_two_input),
        ("delayedPerc", strategy_three_input),
        ("perceptibility", perceptibility_input),
        ("other", other_input),
        ("effort", effort_input),
        ("diff", diff_input),
        ("participated_earlier", participated_earlier_input)]

    # for key in results.keys():
    #     (key, len(results[key]))

    for key, key_input in fill_keys:
        for idx in range(0, len(results["time_stamp"])):
            results[key].append(key_input)
        # print(key, len(results[key]))

    return results


def create_lanes(screen_w, lane_height_1, lane_height_0, upper, middle, lower):
    """
    Creates the lanes; lane width and height are set relative to participants screen.
    :return: upper_lane (Rect), middle_lane (Rect), lower_lane (Rect), lane_width (int), lane_height (int)
    """
    lane_width = screen_w
    lane_height = int(round((lane_height_1 -
                             lane_height_0)))
    upper_lane = pygame.Rect((0, upper,
                              lane_width, lane_height))
    middle_lane = pygame.Rect(0, middle,
                              lane_width, lane_height)
    lower_lane = pygame.Rect(0, lower,
                             lane_width, lane_height)
    return upper_lane, middle_lane, lower_lane, lane_width, lane_height


def start_trial(direction: int, star_group, screen, expGlobals, trial_data, bird,
                screen_variables, lane_height):
    """
    This function re-sets the relevant variables for each trial.
    :return: None
    """
    star_group.clear(screen, screen)

    expGlobals["game_active"] = True
    trial_data["starting_time"] = perf_counter()
    # print("STARTING: ", perf_counter())
    expGlobals["bird_lane"] = "middle"
    bird.true_y = screen_variables["middle_lane"]
    bird.rect.center = (2 * lane_height, screen_variables["middle_lane"])
    bird.true_y = screen_variables["middle_lane"]
    bird.screen_y = int(bird.true_y)
    bird.rect = bird.image.get_rect()
    bird.rect.center = (bird.screen_x, bird.screen_y)
    bird.collideRect = pygame.rect.Rect((0, 0), (
        lane_height / 2 + lane_height / 6, lane_height / 2 + lane_height / 6))

    bird.right_x = bird.rect.center[0] + bird.rad
    expGlobals["direction"] = direction

    # print("STARTING NEW TRIAL")


def set_trial_parameters(cond_df, block, subblock, trial):
    pert_direct = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "pert_direct"].unique()[0]
    upper_value = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "reward_upper"].unique()[0]
    lower_value = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "reward_lower"].unique()[0]
    pertur_strength = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "pertur_strength"].unique()[0]
    direction = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "pert_direct"].unique()[0]
    freq = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "preview"].unique()[0]
    last_change = \
        cond_df[(cond_df["block"] == block) & (
                cond_df["subblock"] == subblock) & (
                        cond_df["trial"] == trial)][
            "last_change"].unique()[0]
    return pert_direct, upper_value, lower_value, pertur_strength, \
           direction, freq, last_change


def display_debug_rectangles(screen, screen_variables, screen_width, lane_height,
                             bird):
    pygame.draw.rect(screen, (255, 0, 0), (
        0, screen_variables["lanes"]["middle"][0],
        screen_width,
        3))
    pygame.draw.rect(screen, (255, 0, 0), (
        0, screen_variables["lanes"]["middle"][1],
        screen_width,
        3))
    pygame.draw.rect(screen, (255, 255, 0),
                     (0,
                      bird.rect.center[1] + lane_height / 2.5,
                      screen_width, 3))
    pygame.draw.rect(screen, (255, 255, 0),
                     (0,
                      bird.rect.center[1] - lane_height / 2.5,
                      screen_width, 3))
    pygame.draw.rect(screen, (255, 0, 0), bird.rect, 2)

