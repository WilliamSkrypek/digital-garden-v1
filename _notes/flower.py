"""
Flower Spread (32x32) — no assets, just Python code.

How it works:
- 32x32 grid on a black background.
- Each cell starts as a "flower" with a random color.
- Click a flower to delete it (turns back to black).
- After every click, the remaining flowers get a chance to spread into empty cells.
- New flowers usually inherit the dominant nearby color, but sometimes mutate.

Requires: pygame
Install:  pip install pygame
Run:      python flowers.py
"""

import random
import math
import pygame

# ------------------------- Config -------------------------
GRID_W, GRID_H = 32, 32
CELL_SIZE = 20
MARGIN = 1

WINDOW_W = GRID_W * CELL_SIZE
WINDOW_H = GRID_H * CELL_SIZE

FPS = 60

# Spread behavior
SPREAD_ATTEMPTS_PER_TICK = 450     # more = faster fill after a click
SPREAD_PROB = 0.22                # chance a given attempt succeeds
MUTATION_CHANCE = 0.06            # chance a new flower mutates
MUTATION_STRENGTH = 60            # how far mutation can push RGB channels (0-255)
DOMINANCE_WEIGHT = 2.2            # >1 makes majority colors more "sticky"

# A little visual polish
DRAW_FLOWERS_AS = "petals"        # "petals" or "dots"

# ------------------------- Helpers -------------------------
def clamp(x, lo=0, hi=255):
    return lo if x < lo else hi if x > hi else x

def random_color():
    # Bright-ish random colors so the grid looks lively
    return (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))

def mutate_color(rgb):
    r, g, b = rgb
    r = clamp(r + random.randint(-MUTATION_STRENGTH, MUTATION_STRENGTH))
    g = clamp(g + random.randint(-MUTATION_STRENGTH, MUTATION_STRENGTH))
    b = clamp(b + random.randint(-MUTATION_STRENGTH, MUTATION_STRENGTH))
    return (r, g, b)

def neighbors4(x, y):
    if x > 0: yield (x - 1, y)
    if x < GRID_W - 1: yield (x + 1, y)
    if y > 0: yield (x, y - 1)
    if y < GRID_H - 1: yield (x, y + 1)

def neighbors8(x, y):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                yield (nx, ny)

def dominant_neighbor_color(grid, x, y):
    """
    Look around an empty cell and pick a color to inherit.
    Rule: count neighbor colors (8-neighborhood). The majority wins more often.
    If no neighbors, return None.
    """
    counts = {}
    for nx, ny in neighbors8(x, y):
        c = grid[ny][nx]
        if c is None:
            continue
        counts[c] = counts.get(c, 0) + 1

    if not counts:
        return None

    # Weighted choice: majority colors get amplified
    items = list(counts.items())  # (color, count)
    weights = [(cnt ** DOMINANCE_WEIGHT) for _, cnt in items]
    total = sum(weights)
    r = random.random() * total
    acc = 0.0
    for (color, _), w in zip(items, weights):
        acc += w
        if r <= acc:
            return color
    return items[-1][0]

def draw_flower(surface, rect, color):
    x, y, w, h = rect
    cx = x + w // 2
    cy = y + h // 2
    radius = max(2, min(w, h) // 4)

    if DRAW_FLOWERS_AS == "dots":
        pygame.draw.circle(surface, color, (cx, cy), radius)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), max(1, radius // 2))
        return

    # Petal-style: 4-6 little circles around a center + darker center
    petals = 6
    petal_r = max(2, radius)
    ring = max(2, radius + 2)

    # Slightly lighter petals
    pr, pg, pb = color
    petal_color = (clamp(pr + 35), clamp(pg + 35), clamp(pb + 35))

    for i in range(petals):
        ang = (i / petals) * (2 * math.pi)
        px = cx + int(math.cos(ang) * ring)
        py = cy + int(math.sin(ang) * ring)
        pygame.draw.circle(surface, petal_color, (px, py), petal_r)

    pygame.draw.circle(surface, color, (cx, cy), max(2, petal_r))
    pygame.draw.circle(surface, (0, 0, 0), (cx, cy), max(1, petal_r // 2))

# ------------------------- Simulation -------------------------
def spread_step(grid):
    """
    After a click, try a bunch of stochastic spread attempts.
    We pick random empty cells; if they have neighboring flowers,
    they may become a new flower inheriting the dominant neighbor color (with mutation).
    """
    empties = []
    # Build a quick list of empties (fast enough for 32x32)
    for y in range(GRID_H):
        row = grid[y]
        for x in range(GRID_W):
            if row[x] is None:
                empties.append((x, y))

    if not empties:
        return

    for _ in range(SPREAD_ATTEMPTS_PER_TICK):
        if random.random() > SPREAD_PROB:
            continue

        x, y = random.choice(empties)
        if grid[y][x] is not None:
            continue  # was filled earlier in this step

        base = dominant_neighbor_color(grid, x, y)
        if base is None:
            continue

        new_c = base
        if random.random() < MUTATION_CHANCE:
            new_c = mutate_color(base)

        grid[y][x] = new_c

# ------------------------- Main -------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Flower Spread (click to clear; space to reset)")
    clock = pygame.time.Clock()

    # Grid holds either None (empty/black) or an (r,g,b) color tuple
    grid = [[random_color() for _ in range(GRID_W)] for _ in range(GRID_H)]

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    grid = [[random_color() for _ in range(GRID_W)] for _ in range(GRID_H)]
                elif event.key == pygame.K_c:
                    grid = [[None for _ in range(GRID_W)] for _ in range(GRID_H)]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                gx = mx // CELL_SIZE
                gy = my // CELL_SIZE
                if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
                    # Delete flower if present
                    if grid[gy][gx] is not None:
                        grid[gy][gx] = None
                        # After every click, run a spread step
                        spread_step(grid)

        # Draw
        screen.fill((0, 0, 0))
        for y in range(GRID_H):
            for x in range(GRID_W):
                c = grid[y][x]
                if c is None:
                    continue
                px = x * CELL_SIZE + MARGIN
                py = y * CELL_SIZE + MARGIN
                pw = CELL_SIZE - 2 * MARGIN
                ph = CELL_SIZE - 2 * MARGIN
                draw_flower(screen, (px, py, pw, ph), c)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
