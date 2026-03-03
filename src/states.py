import pygame
import math
from settings import *
from entities import Player, Ball, GoalBanner

class State:
    def __init__(self, sm, assets):
        self.sm = sm
        self.assets = assets
        self.current_events = []
        
    def enter(self): pass
    def exit(self): pass
    def update(self, events): pass
    def draw(self, screen): pass

    def draw_button(self, screen, text, x, y, font, c_def, c_hov, events):
        mouse_pos = pygame.mouse.get_pos()
        surf = font.render(text, True, c_def)
        rect = surf.get_rect(center=(x, y))
        is_hovered = rect.collidepoint(mouse_pos)
        
        if is_hovered: 
            surf = font.render(text, True, c_hov)
        screen.blit(surf, rect)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_hovered:
                    # SONIDO DE MENÚ AUTOMÁTICO EN TODOS LOS BOTONES
                    self.assets.play_sfx('menu_select') 
                    return True
        return False

    def draw_gear(self, screen):
        x, y = WIDTH - 50, 20
        center = (x + 16, y + 16)
        pygame.draw.circle(screen, AMARILLO, center, 26)
        pygame.draw.circle(screen, BLANCO, center, 26, 3) 
        screen.blit(self.assets.images['gear'], (x, y))

    def check_gear_click(self, origin_state, events):
        mouse_pos = pygame.mouse.get_pos()
        x, y = WIDTH - 50, 20
        hitbox = pygame.Rect(x - 10, y - 10, 52, 52) 
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hitbox.collidepoint(mouse_pos):
                    self.assets.play_sfx('menu_select')
                    self.sm.states["Settings"].set_origin(origin_state)
                    self.sm.change_state("Settings", with_fade=False)

class IntroState(State):
    def enter(self):
        self.timer = pygame.time.get_ticks()
        self.assets.play_sfx('intro_sfx') 
        
    def update(self, events):
        if pygame.time.get_ticks() - self.timer > 3000:
            self.sm.change_state("MainMenu")
    def draw(self, screen):
        screen.blit(self.assets.images['intro'], (0, 0))

class MainMenuState(State):
    def __init__(self, sm, assets):
        super().__init__(sm, assets)
        self.font = pygame.font.SysFont("impact", 48)

    def update(self, events):
        self.current_events = events 
        self.check_gear_click("MainMenu", events)

    def draw(self, screen):
        screen.blit(self.assets.images['intro'], (0,0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        screen.blit(overlay, (0,0))
        
        titulo = self.font.render("SELECCIONA MODO", True, BLANCO)
        screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, 100)))

        if self.draw_button(screen, "1 JUGADOR", WIDTH//2, 200, self.font, BLANCO, AMARILLO, self.current_events):
            self.sm.change_state("DifficultyMenu")
        if self.draw_button(screen, "2 JUGADORES", WIDTH//2, 280, self.font, BLANCO, AMARILLO, self.current_events):
            self.sm.states["Gameplay"].set_mode("2P", "MEDIO")
            self.sm.change_state("Gameplay")
            
        self.draw_gear(screen)

class DifficultyMenuState(State):
    def __init__(self, sm, assets):
        super().__init__(sm, assets)
        self.font = pygame.font.SysFont("impact", 48)
        self.font_s = pygame.font.SysFont("impact", 32)
        
    def update(self, events):
        self.current_events = events
        
    def draw(self, screen):
        screen.blit(self.assets.images['intro'], (0,0))
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(180); screen.blit(overlay, (0,0))
        
        titulo = self.font.render("DIFICULTAD IA", True, BLANCO)
        screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, 80)))

        if self.draw_button(screen, "FÁCIL", WIDTH//2, 180, self.font, BLANCO, AMARILLO, self.current_events):
            self._start_game("FACIL")
        if self.draw_button(screen, "MEDIO", WIDTH//2, 250, self.font, BLANCO, AMARILLO, self.current_events):
            self._start_game("MEDIO")
        if self.draw_button(screen, "DIFÍCIL", WIDTH//2, 320, self.font, BLANCO, AMARILLO, self.current_events):
            self._start_game("DIFICIL")
        if self.draw_button(screen, "< VOLVER", 100, 50, self.font_s, GRIS, BLANCO, self.current_events):
            self.sm.change_state("MainMenu")

    def _start_game(self, diff):
        self.sm.states["Gameplay"].set_mode("1P", diff)
        self.sm.change_state("Gameplay")

class SettingsState(State):
    def __init__(self, sm, assets):
        super().__init__(sm, assets)
        self.font_title = pygame.font.SysFont("impact", 48)
        self.font_opt = pygame.font.SysFont("impact", 32)
        self.origin = "MainMenu"
        self.fullscreen = False
        self.dragging_music = False
        self.dragging_sfx = False

    def set_origin(self, origin_state):
        self.origin = origin_state

    def update(self, events):
        self.current_events = events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        music_rect = pygame.Rect(WIDTH//2 - 150, 150, 300, 20)
        if mouse_pressed:
            if music_rect.collidepoint(mouse_x, mouse_y) or self.dragging_music:
                self.dragging_music = True
                val = (mouse_x - (WIDTH//2 - 150)) / 300.0
                self.assets.music_volume = max(0.0, min(1.0, val))
                self.assets.update_volumes()
        else:
            self.dragging_music = False

        sfx_rect = pygame.Rect(WIDTH//2 - 150, 240, 300, 20)
        if mouse_pressed:
            if sfx_rect.collidepoint(mouse_x, mouse_y) or self.dragging_sfx:
                self.dragging_sfx = True
                val = (mouse_x - (WIDTH//2 - 150)) / 300.0
                self.assets.sfx_volume = max(0.0, min(1.0, val))
                self.assets.update_volumes()
        else:
            self.dragging_sfx = False

    def draw(self, screen):
        screen.fill(NEGRO)
        titulo = self.font_title.render("AJUSTES", True, BLANCO)
        screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, 50)))

        vol_txt = self.font_opt.render(f"Volumen Música: {int(self.assets.music_volume * 100)}%", True, GRIS)
        screen.blit(vol_txt, vol_txt.get_rect(center=(WIDTH//2, 120)))
        pygame.draw.rect(screen, GRIS, (WIDTH//2 - 150, 150, 300, 20)) 
        pygame.draw.rect(screen, AMARILLO, (WIDTH//2 - 150, 150, int(300 * self.assets.music_volume), 20)) 

        sfx_txt = self.font_opt.render(f"Efectos (SFX): {int(self.assets.sfx_volume * 100)}%", True, GRIS)
        screen.blit(sfx_txt, sfx_txt.get_rect(center=(WIDTH//2, 210)))
        pygame.draw.rect(screen, GRIS, (WIDTH//2 - 150, 240, 300, 20)) 
        pygame.draw.rect(screen, AMARILLO, (WIDTH//2 - 150, 240, int(300 * self.assets.sfx_volume), 20)) 

        modo_txt = "MODO: PANTALLA COMPLETA" if self.fullscreen else "MODO: VENTANA"
        if self.draw_button(screen, modo_txt, WIDTH//2, 320, self.font_opt, BLANCO, AMARILLO, self.current_events):
            self.fullscreen = not self.fullscreen
            pygame.display.toggle_fullscreen()
            return 

        if self.draw_button(screen, "< VOLVER", 100, 50, self.font_opt, GRIS, BLANCO, self.current_events):
            self.sm.change_state(self.origin, with_fade=False)

        if self.origin == "Gameplay":
            if self.draw_button(screen, "ABANDONAR PARTIDO", WIDTH//2, HEIGHT - 40, self.font_opt, ROJO, BLANCO, self.current_events):
                # Importante: resetear estado si se abandona
                self.sm.states["Gameplay"].paused = False
                self.sm.change_state("MainMenu", with_fade=False)


class GameplayState(State):
    def __init__(self, sm, assets):
        super().__init__(sm, assets)
        self.mode = "2P"
        self.difficulty = "MEDIO"
        self.score_p1 = 0
        self.score_p2 = 0
        self.font = pygame.font.SysFont("impact", 48)
        self.font_time = pygame.font.SysFont("impact", 36) 
        self.font_pause = pygame.font.SysFont("impact", 70) # Fuente grande para el título de PAUSA
        self.banner = GoalBanner()
        self.kickoff_player = 0 
        self.paused = False # ESTADO DE PAUSA INICIALIZADO

    def set_mode(self, mode, difficulty):
        self.mode = mode
        self.difficulty = difficulty
        self.score_p1, self.score_p2 = 0, 0
        self.kickoff_player = 0 
        self.reset_positions()
        
        self.time_left = 120000 
        self.match_over = False
        self.is_new_game = True 
        self.paused = False # Asegurarnos que no arranca en pausa al jugar de nuevo

    def enter(self):
        self.last_tick = pygame.time.get_ticks()
        self.assets.play_crowd() 
        
        if getattr(self, 'is_new_game', False):
            self.assets.play_sfx('whistle') 
            self.is_new_game = False

    def exit(self):
        self.assets.stop_crowd()

    def reset_positions(self):
        self.p1 = Player(150, FLOOR_Y, True)
        self.p2 = Player(600, FLOOR_Y, False)
        
        if self.kickoff_player == 1:
            self.ball = Ball(250, 100) 
        elif self.kickoff_player == 2:
            self.ball = Ball(550, 100) 
        else:
            self.ball = Ball(WIDTH//2, 100) 

    def bot_ai(self):
        dist_x = self.ball.x - self.p2.x
        speed = PLAYER_SPEED * (0.4 if self.difficulty == "FACIL" else 0.75 if self.difficulty == "MEDIO" else 1.1)
        jump_range = 100 if self.difficulty == "FACIL" else 60 if self.difficulty == "MEDIO" else 30
        
        if dist_x < -20: self.p2.move("LEFT", speed)
        elif dist_x > 20: self.p2.move("RIGHT", speed)
        
        if abs(dist_x) < jump_range and self.ball.y < self.p2.y: self.p2.jump()
        if abs(dist_x) < 50 and abs(self.ball.y - self.p2.y) < 60: self.p2.kick(pygame.time.get_ticks())

    def update(self, events):
        self.current_events = events # Guardamos eventos para el draw_button de la pausa
        self.check_gear_click("Gameplay", events)
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.match_over:
                    # ALTERNAR PAUSA en vez de salir
                    self.paused = not self.paused 
                    self.assets.play_sfx('menu_select')
                return
        
        # SI ESTÁ EN PAUSA, CONGELAMOS EL RELOJ Y NO ACTUALIZAMOS FÍSICAS
        if self.paused:
            self.last_tick = pygame.time.get_ticks() 
            return
                
        # --- GESTIÓN DE FINAL DEL PARTIDO ---
        if self.match_over:
            if pygame.time.get_ticks() - self.game_over_timer > 4000:
                if self.sm.current_state == self: 
                    self.sm.change_state("MainMenu")
            return 
            
        # --- GESTIÓN DEL TEMPORIZADOR ---
        current_ticks = pygame.time.get_ticks()
        dt = current_ticks - self.last_tick
        self.last_tick = current_ticks
        
        if not self.banner.active: 
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.match_over = True
                self.assets.play_sfx('whistle') 
                self.game_over_timer = pygame.time.get_ticks()
                return
        
        if self.banner.active:
            self.banner.update()
            if not self.banner.active: 
                self.reset_positions()
            return 

        keys = pygame.key.get_pressed()
        curr_time = pygame.time.get_ticks()

        self.p1.update_stun_and_kick(curr_time)
        self.p2.update_stun_and_kick(curr_time)

        if not self.p1.stunned:
            if keys[pygame.K_a]: self.p1.move("LEFT")
            if keys[pygame.K_d]: self.p1.move("RIGHT")
            if keys[pygame.K_w]: self.p1.jump()
            if keys[pygame.K_SPACE]: self.p1.kick(curr_time)

        if not self.p2.stunned:
            if self.mode == "2P":
                if keys[pygame.K_LEFT]: self.p2.move("LEFT")
                if keys[pygame.K_RIGHT]: self.p2.move("RIGHT")
                if keys[pygame.K_UP]: self.p2.jump()
                if keys[pygame.K_RETURN]: self.p2.kick(curr_time)
            else:
                self.bot_ai()

        self.p1.apply_gravity()
        self.p2.apply_gravity()
        self.update_ball_physics()
        self._check_player_collision(self.p1, self.p2)
        self._check_ball_collision(self.p1)
        self._check_ball_collision(self.p2)
        self._check_stun_collision(self.p1, self.p2, curr_time)
        self._check_stun_collision(self.p2, self.p1, curr_time)

    def update_ball_physics(self):
        self.ball.vy += GRAVITY * 0.55
        self.ball.y += self.ball.vy
        
        if self.ball.y >= FLOOR_Y + 32:
            self.ball.y = FLOOR_Y + 32
            self.ball.vy *= BALL_BOUNCE
            
        if self.ball.y < 0:
            self.ball.y = 0
            self.ball.vy *= BALL_BOUNCE

        if self.ball.vy > 0: 
            if self.ball.y + 32 >= GOAL_TOP and (self.ball.y + 32 - self.ball.vy) <= GOAL_TOP + 15:
                if self.ball.x < LEFT_WALL or self.ball.x > RIGHT_WALL - 32:
                    self.ball.y = GOAL_TOP - 32
                    self.ball.vy *= BALL_BOUNCE
                    self.ball.vx *= 0.8 

        self.ball.vx *= BALL_FRICTION
        self.ball.x += self.ball.vx
        
        if self.ball.y + 32 <= GOAL_TOP + 10:
            if self.ball.x < LEFT_WALL:
                self.ball.x = LEFT_WALL
                self.ball.vx *= BALL_BOUNCE
            elif self.ball.x > RIGHT_WALL - 32:
                self.ball.x = RIGHT_WALL - 32
                self.ball.vx *= BALL_BOUNCE
                
        else:
            if self.ball.x < LEFT_WALL and (self.ball.x - self.ball.vx) >= LEFT_WALL:
                if self.ball.y < GOAL_TOP + 20: 
                    self.ball.x = LEFT_WALL
                    self.ball.vx *= BALL_BOUNCE
                    
            elif self.ball.x > RIGHT_WALL - 32 and (self.ball.x - self.ball.vx) <= RIGHT_WALL - 32:
                if self.ball.y < GOAL_TOP + 20:
                    self.ball.x = RIGHT_WALL - 32
                    self.ball.vx *= BALL_BOUNCE

            if self.ball.x <= 15:
                self.ball.x = 15
                self.ball.vx *= BALL_BOUNCE
                if not self.banner.active and self.ball.y > GOAL_TOP + 15:
                    self.score_p2 += 1
                    self.assets.play_sfx('cheer')
                    self.assets.play_sfx('goal_banner') 
                    self.kickoff_player = 1 
                    self.banner.trigger()
                    
            elif self.ball.x >= WIDTH - 47:
                self.ball.x = WIDTH - 47
                self.ball.vx *= BALL_BOUNCE
                if not self.banner.active and self.ball.y > GOAL_TOP + 15:
                    self.score_p1 += 1
                    self.assets.play_sfx('cheer')
                    self.assets.play_sfx('goal_banner') 
                    self.kickoff_player = 2 
                    self.banner.trigger()

    def _check_player_collision(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dist = math.hypot(dx, dy)
        if 0 < dist < 50: 
            overlap = 50 - dist
            nx = dx / dist
            p1.x -= nx * (overlap / 2)
            p2.x += nx * (overlap / 2)

    def _check_ball_collision(self, player):
        center_px, center_py = player.x + 32, player.y + 32
        center_bx, center_by = self.ball.x + 16, self.ball.y + 16
        dx, dy = center_bx - center_px, center_by - center_py
        dist = math.hypot(dx, dy)
        
        if dist < 45:
            if dist == 0: dist = 1
            nx, ny = dx / dist, dy / dist
            
            self.ball.x, self.ball.y = center_px + nx * 45 - 16, center_py + ny * 45 - 16
            
            if player.kicking:
                self.assets.play_sfx('kick')
                dir_x = 1 if player.is_p1 else -1
                self.ball.vx = (dir_x * 9) + (nx * 2) 
                self.ball.vy = -7 
            else:
                self.ball.vx = nx * 5
                self.ball.vy = ny * 5 - 1

    def _check_stun_collision(self, attacker, defender, curr_time):
        if attacker.kicking and not attacker.has_hit_this_kick and not attacker.stunned:
            ax = (attacker.x + 35) if attacker.is_p1 else (attacker.x - 15)
            ay = attacker.y + 10
            dist = math.hypot(ax - (defender.x + 32), ay - (defender.y + 32))
            if dist < 55:
                attacker.has_hit_this_kick = True
                defender.take_hit(curr_time)
                if defender.stunned:
                    self.assets.play_sfx('stun')

    def draw_goal_net(self, screen, x, y, w, h, is_left):
        net_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        net_surface.fill((20, 20, 20, 150)) 
        screen.blit(net_surface, (x, y))
        
        for i in range(0, w, 15):
            pygame.draw.line(screen, (150, 150, 150), (x + i, y), (x + i, y + h), 1)
        for i in range(0, h, 15):
            pygame.draw.line(screen, (150, 150, 150), (x, y + i), (x + w, y + i), 1)
            
        pygame.draw.line(screen, BLANCO, (x, y), (x + w, y), 8) 
        if is_left:
            pygame.draw.line(screen, BLANCO, (x + w, y), (x + w, y + h), 8) 
            pygame.draw.line(screen, BLANCO, (x, y), (x, y + h), 4)         
        else:
            pygame.draw.line(screen, BLANCO, (x, y), (x, y + h), 8)         
            pygame.draw.line(screen, BLANCO, (x + w, y), (x + w, y + h), 4) 

    def draw(self, screen):
        screen.blit(self.assets.images['campo'], (0, 0))
        
        goal_h = (FLOOR_Y + 64) - GOAL_TOP 
        self.draw_goal_net(screen, 0, GOAL_TOP, LEFT_WALL, goal_h, True)
        self.draw_goal_net(screen, RIGHT_WALL, GOAL_TOP, WIDTH - RIGHT_WALL, goal_h, False)
        
        score_t = self.font.render(f"{self.score_p1} - {self.score_p2}", True, BLANCO)
        screen.blit(score_t, score_t.get_rect(center=(WIDTH//2, 40)))

        seconds_total = int(self.time_left // 1000)
        mins = seconds_total // 60
        secs = seconds_total % 60
        time_str = f"{mins:02d}:{secs:02d}"
        
        time_col = BLANCO if seconds_total > 10 else ROJO
        time_surf = self.font_time.render(time_str, True, time_col)
        screen.blit(time_surf, time_surf.get_rect(center=(WIDTH//2, 90)))

        for p, img_head, img_boot in [(self.p1, 'head_p1', 'boot_p1'), (self.p2, 'head_p2', 'boot_p2')]:
            if p.invulnerable and (pygame.time.get_ticks() // 150) % 2 == 0:
                continue 

            b_img = self.assets.images[img_boot]
            if p.kicking:
                b_img = pygame.transform.rotate(b_img, 45 if p.is_p1 else -45)
                b_img.set_colorkey(NEGRO) 
                screen.blit(b_img, (p.x + 35 if p.is_p1 else p.x - 15, p.y + 10))
            else:
                screen.blit(b_img, (p.x + 20 if p.is_p1 else p.x - 10, p.y + 30))
            screen.blit(self.assets.images[img_head], (p.x, p.y))
            
            if p.stunned:
                curr_ticks = pygame.time.get_ticks() / 150 
                for i in range(3): 
                    offset_x = math.cos(curr_ticks + i * (math.pi * 2 / 3)) * 25
                    offset_y = math.sin(curr_ticks + i * (math.pi * 2 / 3)) * 10 - 20
                    pygame.draw.circle(screen, AMARILLO, (int(p.x + 32 + offset_x), int(p.y + offset_y)), 6)
                    pygame.draw.circle(screen, BLANCO, (int(p.x + 32 + offset_x), int(p.y + offset_y)), 3)

        screen.blit(self.assets.images['ball'], (int(self.ball.x), int(self.ball.y)))
        
        self.draw_gear(screen)
        self.banner.draw(screen)

        if self.match_over:
            go_surf = self.font.render("¡FIN DEL PARTIDO!", True, BLANCO)
            bg_rect = pygame.Rect(0, HEIGHT//2 - 60, WIDTH, 120)
            pygame.draw.rect(screen, NEGRO, bg_rect)
            pygame.draw.rect(screen, AMARILLO, bg_rect, 5) 
            screen.blit(go_surf, go_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

        # --- DIBUJADO DE LA CAPA DE PAUSA ---
        if self.paused:
            # Filtro oscuro sobre el juego
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0, 0))
            
            # Título "PAUSA"
            titulo = self.font_pause.render("PAUSA", True, BLANCO)
            screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
            
            # Botones Interactivos
            if self.draw_button(screen, "CONTINUAR", WIDTH//2, HEIGHT//2 - 10, self.font, BLANCO, AMARILLO, self.current_events):
                self.paused = False
                
            if self.draw_button(screen, "REINICIAR PARTIDO", WIDTH//2, HEIGHT//2 + 60, self.font, BLANCO, AMARILLO, self.current_events):
                self.set_mode(self.mode, self.difficulty)
                self.enter() # Esto resetea el reloj y vuelve a sonar el silbato inicial
                
            if self.draw_button(screen, "SALIR AL MENÚ", WIDTH//2, HEIGHT//2 + 130, self.font, BLANCO, AMARILLO, self.current_events):
                self.paused = False
                self.sm.change_state("MainMenu")