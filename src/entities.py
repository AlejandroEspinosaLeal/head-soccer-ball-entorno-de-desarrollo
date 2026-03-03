import pygame
import math
from settings import *

class Player:
    def __init__(self, x, y, is_p1):
        self.x = x
        self.y = y
        self.vy = 0
        self.is_p1 = is_p1
        
        self.kicking = False
        self.kick_timer = 0
        self.has_hit_this_kick = False
        
        self.hit_count = 0
        self.stunned = False
        self.stun_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0

    def update_stun_and_kick(self, current_time):
        if self.kicking and current_time - self.kick_timer > 200:
            self.kicking = False
            
        if self.stunned and current_time - self.stun_timer > 2000:
            self.stunned = False
            self.invulnerable = True
            self.invulnerable_timer = current_time
            
        if self.invulnerable and current_time - self.invulnerable_timer > 1500:
            self.invulnerable = False

    def jump(self):
        if self.y >= FLOOR_Y:
            self.vy = JUMP_POWER

    def move(self, direction, speed=PLAYER_SPEED):
        if direction == "LEFT" and self.x > LEFT_WALL:
            self.x -= speed
        elif direction == "RIGHT" and self.x < RIGHT_WALL - 64:
            self.x += speed

    def kick(self, current_time):
        if not self.kicking:
            self.kicking = True
            self.kick_timer = current_time
            self.has_hit_this_kick = False

    def apply_gravity(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= FLOOR_Y:
            self.y, self.vy = FLOOR_Y, 0

    def take_hit(self, current_time):
        if self.stunned or self.invulnerable:
            return 
            
        self.hit_count += 1
        if self.hit_count >= 5:
            self.stunned = True
            self.stun_timer = current_time
            self.hit_count = 0

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        # FÍSICAS DE GLOBO: El balón sufre mucha menos gravedad que los personajes
        self.vy += GRAVITY * 0.55 
        self.vx *= BALL_FRICTION
        self.x += self.vx
        self.y += self.vy

        if self.y >= FLOOR_Y + 32:
            self.y = FLOOR_Y + 32
            self.vy *= BALL_BOUNCE

class GoalBanner:
    def __init__(self):
        self.x = -800
        self.active = False
        self.font = pygame.font.SysFont("impact", 80)

    def trigger(self):
        self.x = -800
        self.active = True

    def update(self):
        if self.active:
            self.x += 25
            if self.x > WIDTH:
                self.active = False
                
    def draw(self, screen):
        if self.active:
            bg_rect = pygame.Rect(0, HEIGHT//2 - 60, WIDTH, 120)
            pygame.draw.rect(screen, NEGRO, bg_rect)
            pygame.draw.rect(screen, AMARILLO, bg_rect, 5) 
            
            text = self.font.render("¡GOOOOOL!", True, BLANCO)
            screen.blit(text, (self.x, HEIGHT//2 - 50))