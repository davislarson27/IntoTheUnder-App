import pygame

def blit_letterboxed(src, dst, bg_color, scale_type=min):
    sw, sh = src.get_size()
    dw, dh = dst.get_size()
    scale = scale_type(dw / sw, dh / sh)
    new_size = (round(sw * scale), round(sh * scale))
    x = (dw - new_size[0]) // 2
    y = (dh - new_size[1]) // 2
    scaled = pygame.transform.smoothscale(src, new_size)
    dst.fill(bg_color)
    dst.blit(scaled, (x, y))
    return scale, x, y  # useful for mouse coordinate mapping

def get_scale(screen, window, scale_type=min):
    sw, sh = screen.get_size()
    dw, dh = window.get_size()
    scale = scale_type(dw / sw, dh / sh)
    new_size = (round(sw * scale), round(sh * scale))
    x = (dw - new_size[0]) // 2
    y = (dh - new_size[1]) // 2
    return scale, x, y  # useful for mouse coordinate mapping

def blit_screen_to_window(screen, window, bg_color, scale, x, y):
    sw, sh = screen.get_size()
    new_size = (round(sw * scale), round(sh * scale))
    scaled = pygame.transform.smoothscale(screen, new_size)
    scaled = pygame.transform.smoothscale(screen, new_size)
    window.fill(bg_color)
    window.blit(scaled, (x, y))
