import pygame

def blit_letterboxed(src, dst, color):
    sw, sh = src.get_size()
    dw, dh = dst.get_size()
    scale = min(dw / sw, dh / sh)
    new_size = (int(sw * scale), int(sh * scale))
    x = (dw - new_size[0]) // 2
    y = (dh - new_size[1]) // 2
    scaled = pygame.transform.smoothscale(src, new_size)
    dst.fill(color)
    dst.blit(scaled, (x, y))
    return scale, x, y  # useful for mouse coordinate mapping