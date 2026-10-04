import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player 
from asteroidfield import AsteroidField
import sys
from shot import Shot
from explosion import Explosion
from background import SpaceBackground

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = SpaceBackground(SCREEN_WIDTH, SCREEN_HEIGHT)
    dt = 0.0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    from asteroid import Asteroid
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (effects, updatable, drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteriod_field = AsteroidField()
    score = 0
    font = pygame.font.Font(None, 36)
    
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  
        
        updatable.update(dt)
        
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += int(asteroid.radius)
                    shot.kill()
                    asteroid.split()
                    break
    
        background.draw(screen)

        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (20, 20))
        
        for obj in drawable:
            obj.draw(screen)
            
        pygame.display.flip()
    
        dt = clock.tick(60) / 1000
    


if __name__ == "__main__":
    main()
