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






class Player:


    def __init__(self):
        self.pos = pygame.math.Vector2(0, HEIGHT // 2)
        self.angle = 90
        self.rotation = 4
        self.maxspd = 40000
        self.velocity = pygame.Vector2(0, 0)
        self.left = pygame.Vector2(-1, 0)
        self.right = pygame.Vector2(1, 0)
        self.up = pygame.Vector2(0, -1)
        self.down = pygame.Vector2(0, 1)
        self.acceleration = pygame.Vector2(0, 0)
        self.thrust = 750
        self.drag = 0.95


    def get_forward(self):
        radians = math.radians(self.angle)
        return pygame.Vector2(math.cos(radians), -math.sin(radians))


    def draw(self, surface):
        forward = self.get_forward()
        left = forward.rotate(180)
        p1 = self.pos + forward * 88
        p2 = self.pos + left * 88


        pygame.draw.polygon(screen, "green", [p2, p1], 10)


    def update(self):
        global dt
        self.velocity += self.acceleration * dt
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
       
        if self.velocity.length() > self.maxspd:
            self.velocity.scale_to_length(self.maxspd)


        self.velocity *= self.drag
        self.pos += self.velocity * dt


   
class Asteroid:


    def __init__(self):
        self.radius = 10
        speed = 50 / self.radius


        self.pos = pygame.math.Vector2(
            (WIDTH // 2) - (self.radius // 2), (HEIGHT // 2) - (self.radius // 2)
        )


        self.vel = (
            pygame.math.Vector2(
                random.uniform(-1, 1), random.uniform(-1, 1)
            ).normalize()
            * speed
        )


        self.mass = self.radius ** 2


    def update(self):
        self.pos += self.vel


        if self.pos.x > WIDTH:
            self.pos.x = 0


        if self.pos.x < 0:
            self.pos.x = WIDTH


        if self.pos.y > HEIGHT:
            self.pos.y = 0


        if self.pos.y < 0:
            self.pos.y = HEIGHT


    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (128, 128, 128),
            (int(self.pos.x), int(self.pos.y)),
            self.radius,
        )




   
def bounce(a1, a2):
    distance_vec = a1.pos - a2.pos
    distance = distance_vec.length()


    min_distance = a1.radius + a2.radius


    if distance < min_distance and distance > 0:
        overlap = min_distance - distance
        direction = distance_vec.normalize()
        a1.pos += direction * (overlap / 2)
        a2.pos -= direction * (overlap / 2)


        total_mass = a1.mass + a2.mass


        new_vel1 = (
            a1.vel * (a1.mass - a2.mass) + (2 * a2.mass * a2.vel)
        ) / total_mass
        new_vel2 = (
            a2.vel * (a2.mass - a1.mass) + (2 * a1.mass * a1.vel)
        ) / total_mass


        a1.vel = new_vel1
        a2.vel = new_vel2


asteroids = [Asteroid() for _ in range(1)]
player = Player()


async def main():
    global dt
    BLUE = (0, 122, 255)
    YELLOW = (255, 223, 0)  


    score = 0
    font = pygame.font.SysFont("arial", 30)
    win_font = pygame.font.SysFont("arial", 60, bold=True)




    running = True
    while running:
        player.acceleration = pygame.Vector2(0, 0)


        keys = pygame.key.get_pressed()


        if keys[pygame.K_LEFT]:
            player.angle += player.rotation


        if keys[pygame.K_RIGHT]:
            player.angle -= player.rotation


        if keys[pygame.K_w]:
            player.acceleration = player.up * player.thrust


        if keys[pygame.K_s]:
            player.acceleration = player.down * player.thrust


        if keys[pygame.K_a]:
            player.acceleration = player.left * player.thrust


        if keys[pygame.K_d]:
            player.acceleration = player.right * player.thrust




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill((30, 30, 30))




        for asteroid in asteroids:
            asteroid.draw(screen)


        player.update()
        player.draw(screen)
       
        # if len(cupcakes) == 0:
        #     win_text = win_font.render("YOU WIN!", True, (0, 255, 128))
        #     text_rect = win_text.get_rect(center=(400, 300))
        #     screen.blit(win_text, text_rect)


        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))


        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        await asyncio.sleep(0)


    pygame.quit()


asyncio.run(main())



