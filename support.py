import pygame
from os import walk
    

def import_folder(path, asset):
    surface_list = []
    match asset:
        case "Knight": 
            vertical_shift = 15
            horizontal_switch = 0
        case "demon": 
            vertical_shift = 0
            horizontal_switch = 0
            crop_rect = pygame.Rect(
                70, # left
                100, # top
                70, # width
                90 # height
            )
        case "jinn": 
            vertical_shift = 0
            horizontal_switch = 0
            crop_rect = pygame.Rect(
                35, # left
                30, # top
                40, # width
                80 # height
            )
        case "lizard": 
            vertical_shift = 0
            horizontal_switch = 0
            crop_rect = pygame.Rect(
                80, # left
                100, # top
                80, # width
                60 # height
            )
        case "Super": 
            vertical_shift = 0
            horizontal_switch = 0
            crop_rect = pygame.Rect(
                20, # left
                40, # top
                50, # width
                20 # height
            )
        
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            if asset != "Knight":
                image_surf = image_surf.subsurface(crop_rect)
            if asset == "Super":
                image_surf = pygame.transform.scale2x(image_surf)
            pygame.Surface.scroll(image_surf, horizontal_switch, vertical_shift)
            surface_list.append(image_surf)
    
    return surface_list

def cursor(screen, color, rect):
    cursor = pygame.Rect(rect.left,rect.top, rect.width, rect.height)
    pygame.draw.rect(screen, color, cursor, 3)