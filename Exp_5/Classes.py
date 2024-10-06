import pygame
from Functions import resource_path


class Bird(pygame.sprite.Sprite):
    """
    Class for the bird the participant controls.
    """

    def __init__(self, width, height, pos_x, pos_y):
        """Constructor"""
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            resource_path('pics\sampleBird_scaled_state1.png')),
            (int(width),
             int(height))).convert_alpha())
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            resource_path('pics\sampleBird_scaled_state2.png')),
            (int(width),
             int(height))).convert_alpha())
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            resource_path('pics\sampleBird_scaled_state3.png')),
            (int(width),
             int(height))).convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.active_image = self.image

        self.height = height
        self.width = width

        self.true_y = pos_y
        self.true_x = pos_x

        self.screen_y = int(self.true_y)
        self.screen_x = int(self.true_x)

        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_x, self.screen_y)
        self.collideRect = pygame.rect.Rect((0, 0), (width, height))

        self.rad = (width / 2)
        self.right_x = self.rect.center[0] + self.rad

    def update(self, new_x, new_y):
        """
        updates the bird object, i.e. the positioning of the rect. The true coordinates (self.true_y and self.true_x)
        are computed and stored internally for correct collision computations. They are converted to integers for
        displaying the bird.

        self.right_x (the rightmost x-coordinate of the bird rectangle) is used for computing collisions with
        obstacles and stars.

        :param new_x: change in x.
        :param new_y: change in y.
        :return: None
        """

        self.true_y += new_y
        self.true_x += new_x
        self.screen_y = int(round(self.true_y))
        self.screen_x = int(round(self.true_x))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_x + new_x, self.screen_y +
                            new_y)
        # self.collideRect.center = self.rect.center
        self.right_x = self.true_x + self.rad

    def animate(self):
        """
        Animates and rotates the bird object.
        :return: None.
        """
        if self.current_sprite >= 2:
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.current_sprite += 1

    def rotate(self, bird_orientation, dependence):
        """
        rotates the bird object, depending on the bird_orientation and dependence for the current block.
        """
        if bird_orientation > 0:

            if dependence == 1:
                self.image = pygame.transform.rotozoom(self.image,
                                                       min(
                                                           bird_orientation / 2,
                                                           30), 1)

            if dependence == -1:
                self.image = pygame.transform.rotozoom(self.image,
                                                       max(
                                                           -bird_orientation / 2,
                                                           -30), 1)

        else:

            if dependence == 1:
                self.image = pygame.transform.rotozoom(self.image,
                                                       max(
                                                           bird_orientation / 2,
                                                           -30), 1)

                if self.current_sprite >= 2:
                    self.current_sprite = 0

            if dependence == -1:
                self.image = pygame.transform.rotozoom(self.image,
                                                       min(
                                                           -bird_orientation / 2,
                                                           30), 1)

                if self.current_sprite >= 2:
                    self.current_sprite = 0


class Star(pygame.sprite.Sprite):
    """
    A Class for the star objects representing the rewards
    """

    def __init__(self, width, height, pos_x, pos_y, collWidth, collHeight):
        """
        Constructor
        :param width: width of the star object
        :param height: height of the star object
        :param pos_x: center x coordinate of the star object
        :param pos_y: center y coordinate of the star object
        :param collWidth: width of the rectangle that is used for calculating collisions
        :param collHeight: height of the rectangle that is used for calculating collisions
        """
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            resource_path('pics\sampleStar.png')), (int(width),
                                                    int(
                                                        height))).convert_alpha()
        self.current_sprite = 0

        self.true_x = pos_x
        self.screen_x = int(self.true_x)

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.rad = (collWidth / 2)
        self.left_x = self.true_x - self.rad

    def update(self, new_x):
        """
        Updates the star object, i.e. its x position. self.true_x is computed internally for correct
        collision computations and converted to int for displaying the star on the screen.
        :param new_x: change in x
        :return: None.
        """
        self.true_x = self.true_x + new_x
        self.screen_x = int(self.true_x)
        self.rect.center = (self.screen_x, self.rect.center[1])
        self.left_x = self.true_x - self.rad


class Obstacle(pygame.sprite.Sprite):
    """
    Class for the obstacle object on the mid lane.
    """

    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            resource_path('pics\sampleObstacle_scaled.png')), (int(round(
            width)),
                                                               int(round(
                                                                   height)))).convert_alpha()
        self.current_sprite = 0

        self.height = height
        self.width = width

        self.true_x = pos_x
        self.screen_x = int(round(self.true_x))

        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_x, pos_y)

        self.rad = (width / 2)
        self.left_x = self.true_x - self.rad

    def update(self, new_x):
        """updates the obstacle position. self.true_x is computed internally for precise collision computations and is
        converted to an integer for displaying the obstacle."""
        self.true_x += new_x
        self.left_x = self.true_x - self.rad
        self.screen_x = int(round(self.true_x))
        self.rect.center = (self.screen_x, self.rect.center[1])