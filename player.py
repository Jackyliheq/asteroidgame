import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0.0 
    
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def collides_with(self, other: CircleShape) -> bool:
        points = self.triangle()
        if self._point_in_triangle(other.position, points):
            return True

        for start, end in zip(points, points[1:] + points[:1]):
            edge = end - start
            edge_length_squared = edge.length_squared()
            if edge_length_squared == 0:
                closest_point = start
            else:
                projection = (other.position - start).dot(edge) / edge_length_squared
                projection = max(0, min(1, projection))
                closest_point = start + edge * projection

            if other.position.distance_to(closest_point) < other.radius:
                return True

        return False

    @staticmethod
    def _point_in_triangle(
        point: pygame.Vector2, triangle: list[pygame.Vector2]
    ) -> bool:
        signs = []
        for start, end in zip(triangle, triangle[1:] + triangle[:1]):
            edge = end - start
            offset = point - start
            signs.append(edge.x * offset.y - edge.y * offset.x)

        return not (any(sign < 0 for sign in signs) and any(sign > 0 for sign in signs))

    def spaceship(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        radius = self.radius

        return [
            self.position + forward * radius,
            self.position + forward * radius * 0.15 + right * radius * 0.9,
            self.position - forward * radius * 0.75 + right * radius * 0.55,
            self.position - forward * radius,
            self.position - forward * radius * 0.75 - right * radius * 0.55,
            self.position + forward * radius * 0.15 - right * radius * 0.9,
        ]

    def draw(self, screen: pygame.Surface) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        ship = self.spaceship()
        cockpit = [
            self.position + forward * self.radius * 0.55,
            self.position + forward * self.radius * 0.05 + right * self.radius * 0.28,
            self.position + forward * self.radius * 0.05 - right * self.radius * 0.28,
        ]
        engine_left = self.position - forward * self.radius * 0.9 + right * self.radius * 0.35
        engine_right = self.position - forward * self.radius * 0.9 - right * self.radius * 0.35

        pygame.draw.polygon(screen, (55, 95, 145), ship)
        pygame.draw.polygon(screen, "white", ship, LINE_WIDTH)
        pygame.draw.polygon(screen, (120, 210, 240), cockpit)
        pygame.draw.line(screen, (255, 170, 45), engine_left, engine_left - forward * self.radius * 0.45, LINE_WIDTH)
        pygame.draw.line(screen, (255, 170, 45), engine_right, engine_right - forward * self.radius * 0.45, LINE_WIDTH)
        
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        
    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity *= PLAYER_SHOOT_SPEED
        shot.velocity = velocity
        
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        aim_direction = mouse_position - self.position
        if aim_direction.length_squared() > 0:
            self.rotation = pygame.Vector2(0, 1).angle_to(aim_direction)

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if pygame.mouse.get_pressed()[0]:
            self.shoot()
            
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
            
    
                