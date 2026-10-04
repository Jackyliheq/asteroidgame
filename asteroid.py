import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from explosion import Explosion
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.points = []
        point_count = 10
        for index in range(point_count):
            angle = index * 360 / point_count
            point_radius = radius * random.uniform(0.78, 1.12)
            self.points.append(
                pygame.Vector2(0, -point_radius).rotate(-angle)
            )

    def draw(self, screen: pygame.Surface) -> None:
        points = [self.position + point for point in self.points]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        
    def split(self) -> None:
        Explosion(self.position, self.radius)
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")
        
        angle = random.uniform(20,50)
        
        velocity1 = self.velocity.rotate(angle) * 1.2
        velocity2 = self.velocity.rotate(-angle) * 1.2
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1
        
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2