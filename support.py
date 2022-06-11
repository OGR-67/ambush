import pygame
from os import walk

    

def import_folder(path, asset):
    surface_list = []
    vertical_shift = 15
    horizontal_switch = 0
        
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = f"{path}/{image}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            if asset == "Super":
                image_surf = pygame.transform.rotozoom(image_surf, 0, 4)
            pygame.Surface.scroll(image_surf, horizontal_switch, vertical_shift)
            surface_list.append(image_surf)
    
    return surface_list

def cursor(screen, color, rect):
    cursor = pygame.Rect(rect.left,rect.top, rect.width, rect.height)
    pygame.draw.rect(screen, color, cursor, 3)