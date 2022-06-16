"""
This module have some useful custom functions.
- import_folder(path, asset)
- transform_image(image_surf, asset)
- cursor(screen, color, rect)
"""

from os import walk
import pygame

def import_folder(path, asset):
    """Return a list of all assets from a folder. Two parameters:
    - path: relative path to the folder
    - asset: name of the asset"""
    surface_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = transform_image(image_surf, asset)
            surface_list.append(image_surf)
    return surface_list


def transform_image(image_surf, asset):
    """Apply modifications to the image to fit it's purpose
    return the modified image"""
    vertical_shift = 15
    horizontal_switch = 0
    match asset:
        case "Super":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 4)
        case "Shield":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 0.70)
            image_surf.set_alpha(100)
            vertical_shift = 0
        case "Charged":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 0.20)
            vertical_shift = 0
        case "Charged_bar":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 0.50)
            vertical_shift = 0
        case "Heart":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 0.3)
            vertical_shift = 0
        case "Blood":
            image_surf = pygame.transform.rotozoom(image_surf, 0, 1.5)
    pygame.Surface.scroll(image_surf, horizontal_switch, vertical_shift)
    return image_surf


def cursor(screen, color, rect):
    """
    A helper function to draw a cursor on a given screen with
    a given color of a given rect.
    - screen: the display surface to draw on
    - color: color code
    - rect: rect object to highlight
    """
    cursor_rect = pygame.Rect(rect.left,rect.top, rect.width, rect.height)
    cursor_width = 3
    pygame.draw.rect(screen, color, cursor_rect, cursor_width)
