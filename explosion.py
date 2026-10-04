import random

import pygame


class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, position: pygame.Vector2, radius: float) -> None:
        super().__init__(*self.containers)
        self.position = pygame.Vector2(position)
        self.age = 0.0
        self.duration = 0.35
        self.particles: list[dict[str, object]] = []

        for _ in range(12):
            direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            self.particles.append(
                {
                    "direction": direction,
                    "speed": random.uniform(radius * 2.5, radius * 5),
                    "size": random.uniform(2, 4),
                }
            )

    def update(self, dt: float) -> None:
        self.age += dt
        if self.age >= self.duration:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        progress = self.age / self.duration
        color = (255, max(80, int(220 * (1 - progress))), 20)

        for particle in self.particles:
            direction = particle["direction"]
            speed = particle["speed"]
            size = particle["size"]
            position = self.position + direction * speed * self.age
            current_size = max(1, int(size * (1 - progress)))
            pygame.draw.circle(screen, color, position, current_size)