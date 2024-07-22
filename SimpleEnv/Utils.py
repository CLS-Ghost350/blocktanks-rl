import math, random, pygame

class Utils:
    @staticmethod
    def rotate_center(image, angle, x, y):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect