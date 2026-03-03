import pygame
import os
import sys
from settings import WIDTH, HEIGHT

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music_volume = 0.5 
        self.sfx_volume = 0.5   
        self.audio_enabled = False 
        self.crowd_bg = None # Sonido especial ambiental en bucle

    def get_base_dir(self):
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        else:
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_assets(self):
        base_dir = self.get_base_dir()
        img_dir = os.path.join(base_dir, "assets", "images")
        snd_dir = os.path.join(base_dir, "assets", "sounds") 

        def load_img(filename, scale=None, colorkey=None):
            filepath = os.path.join(img_dir, filename) 
            try:
                img = pygame.image.load(filepath).convert_alpha()
                if scale: 
                    img = pygame.transform.scale(img, scale)
                if colorkey:
                    img.set_colorkey(colorkey)
                return img
            except Exception as e:
                print(f"⚠️ Error cargando {filename}: {e}")
                surf = pygame.Surface(scale if scale else (50, 50))
                surf.fill((255, 0, 255))
                return surf

        self.images['intro'] = load_img("intro_logo.png", scale=(WIDTH, HEIGHT))
        self.images['campo'] = load_img("campo 100%.png", scale=(WIDTH, HEIGHT))
        self.images['gear'] = load_img("gear_icon.png", scale=(32, 32))
        
        img_head_p1 = load_img("cabezon moreno.png", scale=(64, 64), colorkey=(0,0,0))
        self.images['head_p1'] = pygame.transform.flip(img_head_p1, True, False) 
        self.images['boot_p1'] = load_img("bota negra adidas.png", scale=(48, 48), colorkey=(0,0,0)) 
        
        self.images['head_p2'] = load_img("cabezon rubio.png", scale=(64, 64), colorkey=(0,0,0)) 
        self.images['boot_p2'] = load_img("bota nike blancas.png", scale=(48, 48), colorkey=(0,0,0)) 
        
        self.images['ball'] = load_img("ball.png", scale=(32, 32), colorkey=(255,255,255))
        self.images['goal_banner'] = load_img("goal_banner.png")

        try:
            pygame.mixer.init() 
            self.audio_enabled = True
        except Exception as e:
            print("⚠️ No se detectaron altavoces. El juego iniciará sin sonido.")
            self.audio_enabled = False

        def load_snd(filename):
            if not self.audio_enabled:
                return None
            filepath = os.path.join(snd_dir, filename)
            if os.path.exists(filepath):
                try:
                    return pygame.mixer.Sound(filepath)
                except:
                    return None
            return None

        # --- CARGA DE TODOS LOS SONIDOS ---
        self.sounds['cheer'] = load_snd("cheer.wav")
        self.sounds['kick'] = load_snd("kick.wav")
        self.sounds['stun'] = load_snd("stun.wav")
        self.sounds['menu_select'] = load_snd("menu_select.wav")
        self.sounds['intro_sfx'] = load_snd("intro_sfx.wav")
        self.sounds['whistle'] = load_snd("whistle.wav")
        self.sounds['goal_banner'] = load_snd("goal_banner.wav")
        
        self.crowd_bg = load_snd("crowd_bg.wav")
        
        if self.audio_enabled:
            bgm_path = os.path.join(snd_dir, "bgm.wav")
            if os.path.exists(bgm_path):
                try:
                    pygame.mixer.music.load(bgm_path)
                    pygame.mixer.music.play(-1) 
                except:
                    pass
            
        self.update_volumes()

    def update_volumes(self):
        if not self.audio_enabled: return
        pygame.mixer.music.set_volume(self.music_volume)
        for snd in self.sounds.values():
            if snd:
                snd.set_volume(self.sfx_volume)
        
        # Le bajamos un poco la fuerza a la grada para que no tape la canción de fondo
        if self.crowd_bg:
            self.crowd_bg.set_volume(self.sfx_volume * 0.4) 

    def play_sfx(self, name):
        if not self.audio_enabled: return
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
            
    def play_crowd(self):
        if not self.audio_enabled: return
        if self.crowd_bg:
            self.crowd_bg.play(-1) # Loop infinito
            
    def stop_crowd(self):
        if not self.audio_enabled: return
        if self.crowd_bg:
            self.crowd_bg.stop()