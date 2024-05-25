import pygame
import math
from random import randint
import time

pygame.init()
start = time.time()
def normaldegree(degree):
    if degree < 0: degree = 360 + degree
    while degree > 360 or degree == 360: degree -= 360
    return degree


pygame.mixer.Channel(0).play(pygame.mixer.Sound('ambient.mp3'))
class Player:
    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.rect = pygame.rect.Rect(0,0,self.width,self.height)

class Boss:
    def __init__(self, radius, img, angle) -> None:
        self.radius = radius
        self.image = pygame.transform.scale(pygame.image.load(img), (self.radius*2,self.radius*2))
        self.rect = self.image.get_rect()
        self.x = 250
        self.y = 250
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = angle
    def move(self, length):
        self.x = self.x + length*math.sin(math.radians(self.angle))
        self.y = self.y - length*math.cos(math.radians(self.angle))
        self.rect.x = self.x
        self.rect.y = self.y


class Minion:
    def __init__(self, radius, img, angle) -> None:
        self.radius = radius
        self.image = pygame.transform.scale(pygame.image.load(img), (self.radius*2,self.radius*2))
        self.rect = self.image.get_rect()
        self.x = boss.rect.x + boss.radius - radius
        self.y = boss.rect.y + boss.radius - radius
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = angle
    def move(self, length):
        self.x = self.x + length*math.sin(math.radians(self.angle))
        self.y = self.y - length*math.cos(math.radians(self.angle))
        self.rect.x = self.x
        self.rect.y = self.y


class Bullet:
    def __init__(self, radius, img, angle) -> None:
        self.radius = radius
        self.image = pygame.transform.scale(pygame.image.load(img), (self.radius*2,self.radius*2))
        self.rect = self.image.get_rect()
        self.x = gun.rect.x + gun.rect.height/2 - radius
        self.y = gun.rect.y + gun.rect.height/2 - radius
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = angle
    def move(self, length):
        self.x = self.x + length*math.sin(math.radians(self.angle))
        self.y = self.y - length*math.cos(math.radians(self.angle))
        self.rect.x = self.x
        self.rect.y = self.y


class Gun:
    def __init__(self, width, height, image) -> None:
        self.width = width
        self.height = height 
        self.angle = 0
        self.original_image = pygame.image.load(image)
        self.scaled_image = pygame.transform.scale(self.original_image, (width, height))
        self.rotated_image = pygame.transform.rotate(self.scaled_image, -self.angle+90)
        self.rect = self.rotated_image.get_rect()
    def rotate(self, R):
        self.angle += 5
        self.rotated_image = pygame.transform.rotate(self.scaled_image, -self.angle+90)
        self.rect.x = player.rect.x + player.rect.width/2 + R * math.sin(math.radians(self.angle))
        self.rect.y = player.rect.y + player.rect.height/2 - R * math.cos(math.radians(self.angle))
class Shield:
    def __init__(self, width, height, image) -> None:
        self.width = width
        self.height = height 
        self.angle = 180
        self.original_image = pygame.image.load(image)
        self.scaled_image = pygame.transform.scale(self.original_image, (width, height))
        self.rotated_image = pygame.transform.rotate(self.scaled_image, -self.angle-180)
        self.rect = self.rotated_image.get_rect()
    def rotate(self, R):
        self.angle += 5
        self.rotated_image = pygame.transform.rotate(self.scaled_image, -self.angle-180)
        self.rect.x = player.rect.x + player.rect.width/2 + R * math.sin(math.radians(self.angle))
        self.rect.y = player.rect.y + player.rect.height/2 - R * math.cos(math.radians(self.angle))
minions = list()
bullets = list()
boss = Boss(30, 'Blue_circle.png', 30)
player = Player()
gun = Gun(40,30,'Gun.png')
shield = Shield(40,30,'shield.png')
window = pygame.display.set_mode((500,500))
pygame.display.set_caption('Default action Game')
pygame.display.set_icon(pygame.image.load('Blue_circle.png'))
clock = pygame.time.Clock()

print()
done = False
frame = 0
health = 20
while not done:
    frame += 1
    if frame % 150 == 0:
        for _ in range(2):
            minions.append(Minion(10, 'Red_circle.png', randint(1,360)))
    clock.tick(60)
    window.fill('pink')
    player.rect.x = pygame.mouse.get_pos()[0] - player.width/2
    player.rect.y = pygame.mouse.get_pos()[1] - player.height/2
    gun.rotate(50)
    window.blit(gun.rotated_image, (gun.rect.x-gun.width/2, gun.rect.y-gun.height/2))
    shield.rotate(50)
    window.blit(shield.rotated_image, (shield.rect.x-shield.width/2, shield.rect.y-shield.height/2))

    if boss.rect.x + boss.radius*2 > 500 or boss.rect.x < 0: #touching right wall or left wall
        
            boss.angle = 360 - boss.angle
    if boss.rect.y + boss.radius*2 > 500 or boss.rect.y < 0: #touching top wall or bottom wall
        
            boss.angle = 180 - boss.angle
    boss.move(4)
    if boss.rect.colliderect(player.rect) and frame > 60:
        done = True
    window.blit(boss.image, (boss.rect.x, boss.rect.y))
    
    for i in minions:
        if i.rect.x + i.radius*2 > 500 or i.rect.x < 0: #touching right wall or left wall
            
            i.angle = 360 - i.angle
        if i.rect.y + i.radius*2 > 500 or i.rect.y < 0: #touching top wall or bottom wall
            
            i.angle = 180 - i.angle
        i.move(6)
        if i.rect.colliderect(player.rect):
            done = True
        if i.rect.colliderect(shield.rect):
            minions.remove(i)
        window.blit(i.image, (i.rect.x, i.rect.y))
    for i in bullets:
        i.move(20)
        if i.rect.colliderect(boss.rect):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('bullet_hit.mp3'))
            health -= 1
            bullets.remove(i)
        window.blit(i.image, (i.rect.x - i.radius, i.rect.y - i.radius))

    pygame.draw.rect(window, (255,0,0), player.rect)
    pygame.draw.rect(window, (255,40,40), pygame.rect.Rect(0,0,500,10))
    pygame.draw.rect(window, (40,255,40), pygame.rect.Rect(0,0,500*health/20,10))
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if time.time()-start > 0.1:
                start = time.time()
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('bullet_shot.mp3'))
                bullets.append(Bullet(5, 'Black_circle.png', gun.angle))
    if health < 1:
        done = True

if health < 1:
    pygame.display.set_caption('YOU WON!!!!!')
    
    time.sleep(4)

