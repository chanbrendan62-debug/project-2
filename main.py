import asyncio
import pygame
import math
import random


pygame.init()
pygame.font.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
dt = 0


BLUE = (0, 0, 255)
score_player = 0
score_enemy = 0
new_score_player = 0
new_score_enemy = 0


class Player:


    def __init__(self):
        self.pos = pygame.math.Vector2(0, HEIGHT // 2)
        self.angle = 90
        self.rotation = 4
        self.maxspd = 40000
        self.velocity = pygame.math.Vector2(0, 0)
        self.left = pygame.Vector2(-1, 0)
        self.right = pygame.Vector2(1, 0)
        self.up = pygame.Vector2(0, -1)
        self.down = pygame.Vector2(0, 1)
        self.acceleration = pygame.Vector2(0, 0)
        self.thrust = 1250
        self.drag = 0.95




    def get_forward(self):
        radians = math.radians(self.angle)
        return pygame.Vector2(math.cos(radians), -math.sin(radians))


    def draw(self, surface):
        p1 = self.pos
        p2 = self.pos * -1
        pygame.draw.rect(surface, BLUE, (self.pos.x, self.pos.y, 10, 200))


    def update(self):
        global dt
        self.velocity += self.acceleration * dt
        if self.pos.x > WIDTH // 2:
            self.pos.x = WIDTH // 2
        if self.pos.x < 5:
            self.pos.x = 5
        if self.pos.y > HEIGHT - 200:
            self.pos.y = HEIGHT - 200
        if self.pos.y < 0:
            self.pos.y = 0
       
        if self.velocity.length() > self.maxspd:
            self.velocity.scale_to_length(self.maxspd)


        self.velocity *= self.drag
        self.pos += self.velocity * dt


   
class Ball:


    def __init__(self):
        self.radius = 10
        speed = 50 / self.radius
        self.maxspd = 5

        self.pos = pygame.math.Vector2(
            (WIDTH // 2) - (self.radius // 2), (HEIGHT // 2) - (self.radius // 2)
        )


        self.vel = (
            pygame.math.Vector2(0, 0)
        )

    def update(self):
        global new_score_player, new_score_enemy

        self.pos += self.vel


        if self.pos.x > WIDTH:
            self.vel.x *= -1
            new_score_player += 1


        if self.pos.x < 0:
            self.vel.x *= -1
            new_score_enemy += 1


        if self.pos.y > HEIGHT:
            self.vel.y *= -1


        if self.pos.y < 0:
            self.vel.y *= -1

        if self.vel.length() > self.maxspd:
            self.vel.scale_to_length(self.maxspd)
       


    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (128, 128, 128),
            (int(self.pos.x), int(self.pos.y)),
            self.radius,
        )




   
def bounce(player, ball):
    player_rect = pygame.Rect(player.pos.x, player.pos.y, 10, 200)

    p1 = max(player_rect.left, min(ball.pos.x, player_rect.right))
    p2 = max(player_rect.top, min(ball.pos.y, player_rect.bottom))

    dist_x = ball.pos.x - p1
    dist_y = ball.pos.y - p2
    distance_sq = (dist_x**2) + (dist_y**2)

    if distance_sq < (ball.radius**2):
        distance = math.sqrt(distance_sq)

        if distance > 0:
            normal = pygame.Vector2(dist_x / distance, dist_y / distance)
        else:
            normal = pygame.Vector2(1, 0)

        overlap = ball.radius - distance
        ball.pos += normal * overlap

        ball.vel = ball.vel.reflect(normal)

        ball.vel += player.velocity * 0.2

def reset():
    global new_score_player, new_score_enemy, score_player, score_enemy
    if new_score_player > score_player or new_score_enemy > score_enemy:
        score_player = new_score_player
        score_enemy = new_score_enemy

        ball.pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
        ball.vel = pygame.math.Vector2(0, 0)

        player.pos = pygame.math.Vector2(50, HEIGHT // 2 - 100)


ball = Ball()
player = Player()


async def main():
    global dt, new_score_player, new_score_enemy, score_player, score_enemy

    font = pygame.font.SysFont("arial", 30)

    running = True
    while running:
        player.acceleration = pygame.Vector2(0, 0)


        keys = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            player.acceleration += player.up
        
        if keys[pygame.K_s]:
            player.acceleration += player.down
       
        if keys[pygame.K_a]:
            player.acceleration += player.left
        
        if keys[pygame.K_d]:
            player.acceleration += player.right

        if player.acceleration.length() > 0:
            player.acceleration = player.acceleration.normalize() * player.thrust


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update()
        player.update()

        reset()
        bounce(player, ball)


        screen.fill((30, 30, 30))

        ball.draw(screen)
        player.draw(screen)
        

        score_left_text = font.render(f"Player: {new_score_player}", True, (255, 255, 255))
        screen.blit(score_left_text, (20, 20))

        score_right_text = font.render(f"Enemy: {new_score_enemy}", True, (255, 255, 255))
        screen.blit(score_right_text, (WIDTH - score_right_text.get_width() - 20, 20))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
