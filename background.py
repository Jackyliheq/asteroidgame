import random

import pygame


class SpaceBackground:
    def __init__(self, width: int, height: int, star_count: int = 180) -> None:
        self.size = (width, height)
        self.stars: list[tuple[pygame.Vector2, int, tuple[int, int, int]]] = []

        random_generator = random.Random(7)
        star_colors = [(120, 145, 180), (180, 195, 220), (235, 240, 255)]
        for _ in range(star_count):
            position = pygame.Vector2(
                random_generator.randrange(width),
                random_generator.randrange(height),
            )
            size = random_generator.choice((1, 1, 1, 2))
            color = random_generator.choice(star_colors)
            self.stars.append((position, size, color))

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((5, 8, 20))
        for position, size, color in self.stars:
            pygame.draw.circle(screen, color, position, size)