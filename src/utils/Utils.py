import json

import pygame


def validateJSON(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def validateJSONFile(file):
    try:
        json.load(file)
    except ValueError:
        return False
    return True


# API: allow rectangles being drawn using RGBA presets
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)