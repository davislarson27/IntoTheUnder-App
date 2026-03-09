import pygame

class Mining_Sprite:
    def __init__(self, screen, block_width):
        self.screen = screen
        self.grid = None
        self.block_width = block_width
        self.ticks_mining = 0
        self.x = None
        self.y = None

    def get_total_ticks_to_mine(self):
        return self.grid.get(self.x, self.y).ticks_to_mine

    def draw(self, camera_x, camera_y):
        total_ticks_to_mine = self.get_total_ticks_to_mine()
        if total_ticks_to_mine is None:
            return

        pct = self.ticks_mining / total_ticks_to_mine
        pct = max(0.0, min(1.0, pct))

        bw = self.block_width
        px = self.x * bw - camera_x
        py = self.y * bw - camera_y
        gx, gy = self.x, self.y

        overlay = pygame.Surface((bw, bw), pygame.SRCALPHA)

        # Coarse, simple look (no highlights)
        a = int(95 + 105 * pct)  # 95..200
        crack = (15, 15, 15, min(255, a))

        # Chunky thickness but not overbearing
        t = max(2, bw // 13)
        t = min(t, max(3, bw // 9))

        # Deterministic RNG per block
        seed = (gx * 928371 + gy * 364479 + 12345) & 0xFFFFFFFF
        def rng():
            nonlocal seed
            seed = (1664525 * seed + 1013904223) & 0xFFFFFFFF
            return seed

        def draw_rect(nx, ny, nw, nh):
            rx = int(nx * bw)
            ry = int(ny * bw)
            rw = max(t, int(nw * bw))
            rh = max(t, int(nh * bw))
            pygame.draw.rect(overlay, crack, pygame.Rect(rx, ry, rw, rh))

        def shuffle_in_place(arr):
            for i in range(len(arr) - 1, 0, -1):
                j = rng() % (i + 1)
                arr[i], arr[j] = arr[j], arr[i]

        # pieces (edge-biased, less center)
        small_segments = [
            (0.14, 0.24, 0.22, 0.09),
            (0.66, 0.26, 0.22, 0.09),
            (0.16, 0.70, 0.24, 0.09),
            (0.62, 0.66, 0.24, 0.09),

            (0.22, 0.12, 0.09, 0.22),
            (0.70, 0.14, 0.09, 0.22),
            (0.24, 0.62, 0.09, 0.26),
            (0.70, 0.58, 0.09, 0.26),
        ]

        connectors = [
            (0.32, 0.34, 0.22, 0.09),
            (0.50, 0.30, 0.09, 0.22),
            (0.34, 0.54, 0.22, 0.09),
        ]

        # NEW: late-stage pieces that are "medium" (never one long line)
        # These add intensity at the end without that dominant stroke.
        late_segments = [
            (0.12, 0.44, 0.22, 0.10),  # left-mid chunk
            (0.68, 0.46, 0.20, 0.10),  # right-mid chunk
            (0.44, 0.12, 0.10, 0.22),  # upper-mid chunk
            (0.46, 0.66, 0.10, 0.20),  # lower-mid chunk
        ]

        chips = [
            (0.24, 0.28, 0.12, 0.12),
            (0.64, 0.30, 0.10, 0.10),
            (0.28, 0.66, 0.11, 0.11),
            (0.66, 0.64, 0.11, 0.11),
        ]

        small = small_segments[:]
        conn = connectors[:]
        late = late_segments[:]
        chip = chips[:]
        shuffle_in_place(small)
        shuffle_in_place(conn)
        shuffle_in_place(late)
        shuffle_in_place(chip)

        # Reveal plan (identical feel, but NO long line at the end)
        if pct < 0.2:
            rs, rc, rlate, rchip = 2, 0, 0, 0
        elif pct < 0.4:
            rs, rc, rlate, rchip = 4, 0, 0, 1
        elif pct < 0.6:
            rs, rc, rlate, rchip = 5, 1, 0, 1
        elif pct < 0.8:
            rs, rc, rlate, rchip = 6, 2, 0, 2
        else:
            rs, rc, rlate, rchip = 7, 2, 2, 2   # add 2 medium late pieces instead of 1 long line

        for nx, ny, nw, nh in small[:rs]:
            draw_rect(nx, ny, nw, nh)

        for nx, ny, nw, nh in conn[:rc]:
            draw_rect(nx, ny, nw, nh)

        for nx, ny, nw, nh in late[:rlate]:
            draw_rect(nx, ny, nw, nh)

        for nx, ny, nw, nh in chip[:rchip]:
            draw_rect(nx, ny, nw, nh)

        self.screen.blit(overlay, (px, py))

    def set_grid(self, grid):
        self.grid = grid

    def set(self, x, y):
        if self.x == x and self.y == y:
            self.ticks_mining += 1
            self.x = x
            self.y = y
        else:
            self.ticks_mining = 0
            self.x = x
            self.y = y

    def reset(self):
        self.ticks_mining = 0
