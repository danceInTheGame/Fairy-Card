# Coding utf-8
import pygame
import os
import sys
import random
import math
import json
import wave
import struct



# Définir une classe qui permettra de créer et d'afficher des cartes

class Card:
    # Attributs
    def __init__(self,LifePoint,AttackPoint,link,card_name=""):
        self.Name = pygame.image.load(link).convert_alpha()
        self.AttackPoint = AttackPoint
        self.LifePoint = LifePoint
        self.card_name = card_name
        
    # Méthodes
    def Resize_Card(self,image,width,height):
        return pygame.transform.scale(image,(width,height))
    
    def Blit_Card(self,origin_surface,card,width,height):
        card_rect = origin_surface.blit(card,(width,height))
        return card_rect



# Fonction pour dessiner du texte clignotant
def draw_blinking_text(text, color, surface, x, y, font, blink_speed=500):
    current_time = pygame.time.get_ticks()  # Obtenir le temps écoulé depuis le début du programme
    if (current_time // blink_speed) % 2 == 0:  # Alterne toutes les 500 ms
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)




# Fonction pour dessiner du texte avec un effet d'apparition progressif
def draw_fading_text(text, color, surface, x, y, font, duration=1000):
    current_time = pygame.time.get_ticks() % (2 * duration)  # Cycle entre fade-in et fade-out
    fade_alpha = 255 * (current_time / duration) if current_time <= duration else 255 * (1 - (current_time - duration) / duration)
    
    # Limiter l'alpha entre 0 et 255
    fade_alpha = max(0, min(255, int(fade_alpha)))
    
    # Créer le texte et appliquer l'alpha
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(fade_alpha)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def normalize_path(folder, filename):
    # Vérifier si le script est exécuté dans un environnement empaqueté
    if getattr(sys, 'frozen', False):
        # Utiliser _MEIPASS pour accéder aux fichiers empaquetés
        base_path = os.path.join(sys._MEIPASS, folder)
    else:
        # Utiliser le répertoire actuel du script
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)

    # Construire le chemin complet
    full_path = os.path.join(base_path, filename)

    # Afficher le chemin pour le débogage
    print(f"Chemin normalisé : {full_path}")

    return full_path


class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, alpha_decay=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alpha_decay = alpha_decay

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0.5, self.size - 0.03)

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime)) if self.alpha_decay else 255
            radius = int(self.size)
            if radius <= 0:
                return
            p_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, alpha), (radius, radius), radius)
            surface.blit(p_surf, (int(self.x - radius), int(self.y - radius)))

class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit_sparkle(self, x, y, color=(255, 200, 50), count=5):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2.5)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            size = random.uniform(2.0, 5.0)
            lifetime = random.randint(15, 30)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))

    def emit_clash(self, x, y, color=(255, 100, 0), count=25):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            size = random.uniform(3.0, 7.0)
            lifetime = random.randint(15, 40)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))

    def emit_ambient(self, width, height, color=(255, 160, 50), count=1):
        for _ in range(count):
            x = random.randint(0, width)
            y = height + 10
            vx = random.uniform(-0.3, 0.3)
            vy = random.uniform(-1.5, -0.5)
            size = random.uniform(1.5, 4.0)
            lifetime = random.randint(120, 240)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime, alpha_decay=True))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class FloatingText:
    def __init__(self, text, x, y, color, font, lifetime=45):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            text_surf = self.font.render(self.text, True, self.color)
            text_surf.set_alpha(alpha)
            rect = text_surf.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(text_surf, rect)


# ==========================================
# SYSTEME DE CONFIGURATION ET SAUVEGARDE
# ==========================================

class SettingsManager:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
        self.data = {
            "volume_music": 0.5,
            "volume_sfx": 0.5,
            "language": "fr",
            "bg_image": "Home_screen.jpeg",
            "brightness": 1.0,
            "mute": False
        }
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    for k, v in loaded.items():
                        self.data[k] = v
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

SETTINGS = SettingsManager()


# ==========================================
# TRADUCTION ET LOCALISATION BILINGUE (FR/EN)
# ==========================================

LOCALIZATION = {
    "fr": {
        "title": "FAIRY CARD",
        "play_ia": "Jouer contre l'I.A.",
        "host_game": "Heberger une partie",
        "join_game": "Rejoindre une partie",
        "options": "Options",
        "quit": "Quitter",
        "back": "Retour",
        "cancel": "Annuler",
        "selection_title": "Selection des mages",
        "selection_inst": "Cliquez sur la carte que vous souhaitez selectionner",
        "recruits": "HEROS RECRUTES",
        "tech_sheet": "FICHE TECHNIQUE",
        "hover_char": "SURVOLEZ UN PERSONNAGE",
        "discover_stats": "POUR DECOUVRIR SES STATS",
        "chosen": "CHOISI",
        "waiting_opp": "En attente des choix de l'adversaire...",
        "cards_selected": "Cartes selectionnees !",
        "host_ip": "Adresse IP locale :",
        "wait_player2": "En attente du joueur 2...",
        "enter_ip": "Entrez l'adresse IP de l'hote :",
        "connecting": "Se connecter",
        "connecting_to": "Connexion en cours a",
        "conn_failed": "Connexion echouee !",
        "you_win": "Victoire !",
        "you_lose": "Defaite !",
        "opp_disconnected": "Adversaire deconnecte",
        "shuffle": "MELANGE DES CARTES...",
        "choose_card": "Choisissez votre carte pour attaquer",
        "ready": "PRET",
        "options_title": "OPTIONS",
        "volume_music": "Volume Musique",
        "volume_sfx": "Volume Effets Sonores",
        "language": "Langue du jeu",
        "bg_select": "Fond d'ecran principal",
        "brightness": "Luminosite de l'ecran",
        "rules_btn": "Voir les Regles du Jeu",
        "rules_title": "REGLES DU JEU (FAIRY CARD)",
        "rules_text_1": "1. Combat : Chaque joueur a un deck de 5 cartes (10 en solo). A chaque tour, les deux joueurs choisissent secretement une carte.",
        "rules_text_2": "2. Clash : Les cartes s'affrontent. Chacune perd des PV egaux a l'ATK adverse, et son ATK diminue de 20% suite a l'effort.",
        "rules_text_3": "3. Capture : Si une carte descend sous 0 PV, elle est capturee par l'adversaire avec +200 PV et +100 ATK de bonus !",
        "rules_text_4": "4. Melange : Apres chaque combat, les decks sont melanges de maniere synchrone.",
        "rules_text_5": "5. Cartes Speciales : Utilisez vos 2 cartes speciales pour soigner, booster, ou pieger l'adversaire au bon moment !",
        "rules_text_6": "Gagnez en capturant ou eliminant toutes les cartes de l'adversaire !",
        "special_cards_tray": "CARTES SPECIALES",
        "special_used": "Carte speciale jouee !",
        "special_target_prompt": "Cliquez sur une carte pour appliquer le sort...",
        "special_1_name": "Soin Lacryma",
        "special_1_desc": "+800 PV a un allie",
        "special_2_name": "Bouclier Erza",
        "special_2_desc": "Annule les prochains degats",
        "special_3_name": "Rage Dragon",
        "special_3_desc": "+250 ATK permanent allie",
        "special_4_name": "Origine Sec.",
        "special_4_desc": "+400 ATK / -300 PV allie",
        "special_5_name": "Portail Eclipse",
        "special_5_desc": "Echange les PV d'un allie et d'un ennemi",
        "special_6_name": "Loi des Fees",
        "special_6_desc": "Inflige 300 degats a tous les ennemis",
        "special_7_name": "Sceau Zeleph",
        "special_7_desc": "-50% ATK permanent ennemi",
        "eveil_activated": "EVEIL ACTIVE !",
        "eveil_remaining": "Eveil : {} tours restants !",
        "eveil_exhausted": "EPUISEMENT !",
        "eveil_title": "MODE EVEIL ENCLENCHE !",
        "matchmaking": "Matchmaking en ligne",
        "search_match": "Recherche d'adversaire...",
        "match_found": "Adversaire trouve !",
        "connecting_irc": "Connexion au serveur..."
    },
    "en": {
        "title": "FAIRY CARD",
        "play_ia": "Play against A.I.",
        "host_game": "Host a Game",
        "join_game": "Join a Game",
        "options": "Options",
        "quit": "Quit",
        "back": "Back",
        "cancel": "Cancel",
        "selection_title": "Character Selection",
        "selection_inst": "Click on the card you wish to select",
        "recruits": "HEROES RECRUITED",
        "tech_sheet": "TECHNICAL SHEET",
        "hover_char": "HOVER A CHARACTER",
        "discover_stats": "TO DISCOVER THEIR STATS",
        "chosen": "CHOSEN",
        "waiting_opp": "Waiting for opponent's choices...",
        "cards_selected": "Cards selected!",
        "host_ip": "Local IP Address:",
        "wait_player2": "Waiting for player 2...",
        "enter_ip": "Enter host IP address:",
        "connecting": "Connect",
        "connecting_to": "Connecting to",
        "conn_failed": "Connection failed!",
        "you_win": "Victory!",
        "you_lose": "Defeat!",
        "opp_disconnected": "Opponent disconnected",
        "shuffle": "SHUFFLING CARDS...",
        "choose_card": "Choose your card to attack",
        "ready": "READY",
        "options_title": "OPTIONS",
        "volume_music": "Music Volume",
        "volume_sfx": "Sound Effects Volume",
        "language": "Game Language",
        "bg_select": "Main Background Image",
        "brightness": "Screen Brightness",
        "rules_btn": "View Game Rules",
        "rules_title": "GAME RULES (FAIRY CARD)",
        "rules_text_1": "1. Combat: Each player has a deck of 5 cards (10 in solo). Each turn, both players secretly play a card.",
        "rules_text_2": "2. Clash: Cards clash. Each loses HP equal to the opponent's ATK, and their own ATK decays by 20%.",
        "rules_text_3": "3. Capture: If a card falls below 0 HP, it is captured by the opponent and gains +200 HP and +100 ATK bonus!",
        "rules_text_4": "4. Shuffling: After each clash, the decks are shuffled synchronously to maintain surprise.",
        "rules_text_5": "5. Special Cards: Play your 2 special cards to heal, boost, or trap the opponent at the perfect moment!",
        "rules_text_6": "Win by capturing or eliminating all of the opponent's cards!",
        "special_cards_tray": "SPECIAL CARDS",
        "special_used": "Special card played!",
        "special_target_prompt": "Click on a card to apply the spell...",
        "special_1_name": "Lacryma Heal",
        "special_1_desc": "+800 HP to an ally",
        "special_2_name": "Erza Shield",
        "special_2_desc": "Blocks the next damage",
        "special_3_name": "Dragon Rage",
        "special_3_desc": "+250 ATK permanent ally",
        "special_4_name": "Sec. Origin",
        "special_4_desc": "+400 ATK / -300 HP ally",
        "special_5_name": "Eclipse Gate",
        "special_5_desc": "Swap HP of an ally and an enemy",
        "special_6_name": "Fairy Law",
        "special_6_desc": "Deals 300 damage to all enemy cards",
        "special_7_name": "Zeref Seal",
        "special_7_desc": "-50% ATK permanent enemy",
        "eveil_activated": "AWAKENING ACTIVATED!",
        "eveil_remaining": "Awakening: {} turns left!",
        "eveil_exhausted": "EXHAUSTION!",
        "eveil_title": "AWAKENING MODE ACTIVATED!",
        "matchmaking": "Online Matchmaking",
        "search_match": "Searching for opponent...",
        "match_found": "Opponent found!",
        "connecting_irc": "Connecting to server..."
    }
}

def L(key):
    lang = SETTINGS.get("language", "fr")
    return LOCALIZATION[lang].get(key, key)


# ==========================================
# GENERATEUR ACOUSTIQUE DE BRUITAGES WAV
# ==========================================

def generate_game_sounds():
    sound_dir = normalize_path("", "Sound")
    os.makedirs(sound_dir, exist_ok=True)
    
    def write_wav(filename, samples, sample_rate=22050):
        filepath = os.path.join(sound_dir, filename)
        if os.path.exists(filepath):
            return
        try:
            with wave.open(filepath, 'w') as f:
                f.setparams((1, 2, sample_rate, len(samples), 'NONE', 'not compressed'))
                for sample in samples:
                    val = max(-32768, min(32767, int(sample * 32767)))
                    f.writeframesraw(struct.pack('<h', val))
        except Exception as e:
            print(f"Error generating sound {filename}: {e}")

    sample_rate = 22050
    
    # 1. UI Click: sweet digital drop
    click_samples = []
    duration = 0.08
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        freq = 1200 - (t / duration) * 800
        vol = (1.0 - t / duration) * 0.4
        click_samples.append(math.sin(2 * math.pi * freq * t) * vol)
    write_wav("ui_click.wav", click_samples)
    
    # 2. UI Hover: subtle and high-pitched pop
    hover_samples = []
    duration = 0.05
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        freq = 880
        vol = (1.0 - t / duration) * 0.12
        hover_samples.append(math.sin(2 * math.pi * freq * t) * vol)
    write_wav("ui_hover.wav", hover_samples)
    
    # 3. Card Select: upward arpeggio
    sel_samples = []
    duration = 0.25
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        step = int(t * 16)
        notes = [440, 554, 659, 880]
        freq = notes[step % len(notes)]
        vol = (1.0 - t / duration) * 0.3
        sel_samples.append(math.sin(2 * math.pi * freq * t) * vol)
    write_wav("card_select.wav", sel_samples)

    # 4. Clash Impact: deep explosive noise
    clash_samples = []
    duration = 0.4
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        freq = 200 * (1.0 - t / duration)
        noise = random.uniform(-1.0, 1.0) * 0.4
        sine = math.sin(2 * math.pi * freq * t) * 0.6
        vol = (1.0 - t / duration) ** 2 * 0.6
        clash_samples.append((sine + noise) * vol)
    write_wav("clash_impact.wav", clash_samples)
    
    # 5. Special Activate: cosmic magic sweep
    spec_samples = []
    duration = 0.6
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        freq = 200 + (t / duration) ** 2 * 1800
        vol = math.sin(t * math.pi) * (1.0 - t / duration) * 0.4
        spec_samples.append(math.sin(2 * math.pi * freq * t) * vol)
    write_wav("special_activate.wav", spec_samples)

    # 6. Shuffle: rhythmic swooshes
    shuf_samples = []
    duration = 0.4
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        swoosh_t = (t * 3) % 1.0
        freq = 150 + swoosh_t * 600
        vol = math.sin(swoosh_t * math.pi) * (1.0 - t / duration) * 0.3
        shuf_samples.append(math.sin(2 * math.pi * freq * t) * vol)
    write_wav("shuffle.wav", shuf_samples)


# ==========================================
# GESTIONNAIRE DE BRUITAGES GLOBALES
# ==========================================

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._loaded = False
        generate_game_sounds()
        self._load_sounds()

    def _load_sounds(self):
        """Charge les sons si le mixer est disponible."""
        if self._loaded:
            return
        if not pygame.mixer.get_init():
            return
        self._loaded = True
        for sname in ["ui_click", "ui_hover", "card_select", "clash_impact", "special_activate", "shuffle"]:
            try:
                self.sounds[sname] = pygame.mixer.Sound(normalize_path("Sound", f"{sname}.wav"))
            except Exception as e:
                print(f"Could not load sound {sname}: {e}")
                self.sounds[sname] = None

    def play(self, name):
        self._load_sounds()  # chargement différé si mixer est maintenant prêt
        sound = self.sounds.get(name)
        if sound and not SETTINGS.get("mute", False):
            sound.set_volume(SETTINGS.get("volume_sfx", 0.5))
            sound.play()

    def update_music_volume(self):
        vol = 0.0 if SETTINGS.get("mute", False) else SETTINGS.get("volume_music", 0.5)
        pygame.mixer.music.set_volume(vol)

# Initialiser le mixer avant d'instancier SoundManager
if not pygame.mixer.get_init():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    if not pygame.get_init():
        pygame.init()
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"Mixer init warning: {e}")

SOUNDS = SoundManager()


# ==========================================
# EFFETS GRAPHIQUES ET CONTROLES OPTIONS
# ==========================================

def apply_brightness(surface, level):
    if level >= 1.0:
        return
    opacity = int((1.0 - level) * 230) # max opacity to keep screen visible
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, opacity))
    surface.blit(overlay, (0, 0))


def draw_slider(surface, x, y, width, val_ratio, label, font):
    # Dessine le label avec le pourcentage en temps réel
    lbl_text = f"{label} : {int(val_ratio * 100)}%"
    lbl_surf = font.render(lbl_text, True, (255, 255, 255))
    surface.blit(lbl_surf, (x, y - 25))
    
    # Dessine la barre
    track_h = 8
    pygame.draw.rect(surface, (60, 60, 80), (x, y, width, track_h), border_radius=4)
    
    # Dessine la partie remplie
    filled_w = int(width * val_ratio)
    pygame.draw.rect(surface, (0, 255, 255), (x, y, filled_w, track_h), border_radius=4)
    
    # Dessine la poignée
    handle_x = x + filled_w
    handle_y = y + track_h // 2
    handle_r = 10
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    # Collision avec la poignée ou la barre
    is_hover = (mouse_pos[0] - handle_x)**2 + (mouse_pos[1] - handle_y)**2 <= (handle_r * 2.0)**2
    handle_color = (255, 215, 0) if is_hover else (0, 255, 255)
    
    pygame.draw.circle(surface, handle_color, (handle_x, handle_y), handle_r)
    pygame.draw.circle(surface, (255, 255, 255), (handle_x, handle_y), handle_r, 2)
    
    new_ratio = val_ratio
    if mouse_click[0] == 1:
        if x <= mouse_pos[0] <= x + width and y - 15 <= mouse_pos[1] <= y + 20:
            new_ratio = (mouse_pos[0] - x) / width
            new_ratio = max(0.0, min(1.0, new_ratio))
            
    return new_ratio


def draw_language_selector(surface, x, y, active_lang, font):
    lbl_surf = font.render(L("language"), True, (255, 255, 255))
    surface.blit(lbl_surf, (x, y - 25))
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    btn_w, btn_h = 100, 35
    
    # Bouton FR
    fr_rect = pygame.Rect(x, y, btn_w, btn_h)
    fr_active = (active_lang == "fr")
    fr_color = (0, 200, 200) if fr_active else (40, 40, 60)
    fr_hover = fr_rect.collidepoint(mouse)
    if fr_hover:
        fr_color = (0, 255, 255) if fr_active else (60, 60, 80)
        if click[0] == 1:
            return "fr", True
            
    pygame.draw.rect(surface, fr_color, fr_rect, border_radius=6)
    pygame.draw.rect(surface, (255, 255, 255), fr_rect, 2 if fr_active else 1, border_radius=6)
    txt_fr = font.render("FR", True, (255, 255, 255))
    surface.blit(txt_fr, txt_fr.get_rect(center=fr_rect.center))
    
    # Bouton EN
    en_rect = pygame.Rect(x + 120, y, btn_w, btn_h)
    en_active = (active_lang == "en")
    en_color = (0, 200, 200) if en_active else (40, 40, 60)
    en_hover = en_rect.collidepoint(mouse)
    if en_hover:
        en_color = (0, 255, 255) if en_active else (60, 60, 80)
        if click[0] == 1:
            return "en", True
            
    pygame.draw.rect(surface, en_color, en_rect, border_radius=6)
    pygame.draw.rect(surface, (255, 255, 255), en_rect, 2 if en_active else 1, border_radius=6)
    txt_en = font.render("EN", True, (255, 255, 255))
    surface.blit(txt_en, txt_en.get_rect(center=en_rect.center))
    
    # Petit bruitage au survol
    if (fr_hover and active_lang != "fr") or (en_hover and active_lang != "en"):
        # On peut jouer un hover, mais attention à ne pas saturer. 
        pass
        
    return active_lang, False


def draw_bg_selector(surface, x, y, active_bg, font):
    lbl_surf = font.render(L("bg_select"), True, (255, 255, 255))
    surface.blit(lbl_surf, (x, y - 25))
    
    bg_options = ["Home_screen.jpeg", "Home_screen(1).jpeg", "Home_screen(2).jpeg"]
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    box_w, box_h = 130, 80
    selected_changed = False
    
    for i, bg in enumerate(bg_options):
        bx = x + i * 150
        by = y
        rect = pygame.Rect(bx, by, box_w, box_h)
        
        is_active = (bg == active_bg)
        box_color = (0, 200, 100) if is_active else (35, 30, 50)
        if rect.collidepoint(mouse):
            box_color = (0, 255, 150) if is_active else (55, 45, 75)
            if click[0] == 1:
                active_bg = bg
                selected_changed = True
                
        pygame.draw.rect(surface, box_color, rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2 if is_active else 1, border_radius=8)
        
        txt = font.render(f"FOND {i+1}", True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=rect.center))
        
    return active_bg, selected_changed


