import pygame
from Customize_home_screen import *
import random
import math

def apply_spell_effect(spell_id, target_card, all_enemy_cards=None):
    if spell_id == 1: # Soin Lacryma
        if target_card:
            target_card.LifePoint += 800
    elif spell_id == 2: # Bouclier Erza
        if target_card:
            target_card.has_shield = True
    elif spell_id == 3: # Rage Dragon
        if target_card:
            target_card.AttackPoint += 250
    elif spell_id == 4: # Origine Sec.
        if target_card:
            target_card.AttackPoint += 400
            target_card.LifePoint = max(100, target_card.LifePoint - 300)
    elif spell_id == 5: # Portail Eclipse
        if target_card and all_enemy_cards:
            enemy = max(all_enemy_cards, key=lambda c: c.LifePoint)
            target_card.LifePoint, enemy.LifePoint = enemy.LifePoint, target_card.LifePoint
    elif spell_id == 6: # Loi des Fées
        if all_enemy_cards:
            for c in all_enemy_cards:
                c.LifePoint = max(0, c.LifePoint - 300)
    elif spell_id == 7: # Sceau Zeleph
        if target_card:
            target_card.AttackPoint = max(50, int(target_card.AttackPoint * 0.5))
            target_card.has_seal = True


def draw_eveil_button(surface, x, y, width, height, font):
    # DESSIN D'UN BOUTON ÉVEIL LOOK ULTRA PREMIUM FAIRY TAIL (FLAMMES/NEON CHAUD)
    t = pygame.time.get_ticks()
    # Effet d'oscillation/pulsation pour le néon
    pulse = int(180 + 75 * math.sin(t / 150.0))
    glow_color = (255, int(100 + 80 * math.sin(t / 200.0)), 0) # Dégradé orange-rouge enflammé
    
    mouse = pygame.mouse.get_pos()
    is_hover = x <= mouse[0] <= x + width and y <= mouse[1] <= y + height
    
    # Bouton de fond
    btn_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    if is_hover:
        btn_surf.fill((180, 30, 10, 230)) # Rouge vif au survol
        border_c = (255, 215, 0) # Or scintillant
    else:
        btn_surf.fill((100, 10, 5, 190)) # Rouge sombre
        border_c = glow_color
        
    surface.blit(btn_surf, (x, y))
    
    # Bordures multiples pour effet de halo magique
    pygame.draw.rect(surface, border_c, (x, y, width, height), 3, border_radius=12)
    pygame.draw.rect(surface, (255, 69, 0), (x - 2, y - 2, width + 4, height + 4), 1, border_radius=14)
    
    # Texte du bouton
    text_surf = font.render("🔥 EVEIL 🔥", True, (255, 255, 255) if is_hover else (255, 220, 150))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surf, text_rect)
    
    return pygame.Rect(x, y, width, height)


def animer_combat_resolution(screen, scaled_bg, carte_locale, carte_distante, initial_hp_loc, initial_hp_dist, damage_loc, damage_dist, initial_atk_loc, initial_atk_dist, label_loc="VOUS", label_dist="ADVERSAIRE"):
    font_large = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 25)
    font_dmg = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 40)
    
    largeur_carte, hauteur_carte = 200, 300
    y_center = screen.get_height() // 2 - hauteur_carte // 2
    
    x_loc = (screen.get_width() // 2 - largeur_carte) - 100
    x_dist = (screen.get_width() // 2 + largeur_carte) + 100
    
    y_start_loc = screen.get_height()
    y_start_dist = -hauteur_carte
    y_target = y_center
    
    card_back_img = pygame.image.load(normalize_path('Image', 'Card_Back.png')).convert_alpha()
    
    steps = 20
    clock = pygame.time.Clock()
    
    # 1. Slide in
    for step in range(steps + 1):
        t = step / steps
        y_curr_loc = y_start_loc + (y_target - y_start_loc) * (1 - (1-t)**2)
        y_curr_dist = y_start_dist + (y_target - y_start_dist) * (1 - (1-t)**2)
        
        screen.blit(scaled_bg, (0, 0))
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        screen.blit(img_loc, (x_loc, int(y_curr_loc)))
        
        img_dist = carte_distante.Resize_Card(card_back_img, largeur_carte, hauteur_carte)
        screen.blit(img_dist, (x_dist, int(y_curr_dist)))
        
        pygame.display.update()
        clock.tick(60)
        
    # 2. Flip opponent card to reveal it
    flip_steps = 15
    for step in range(flip_steps + 1):
        t = step / flip_steps
        if t < 0.5:
            scale_x = 1.0 - (t * 2)
            w = max(1, int(largeur_carte * scale_x))
            img_dist = carte_distante.Resize_Card(card_back_img, w, hauteur_carte)
        else:
            scale_x = (t - 0.5) * 2
            w = max(1, int(largeur_carte * scale_x))
            img_dist = carte_distante.Resize_Card(carte_distante.Name, w, hauteur_carte)
            
        screen.blit(scaled_bg, (0, 0))
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        screen.blit(img_loc, (x_loc, y_target))
        
        offset_x = x_dist + (largeur_carte - w) // 2
        screen.blit(img_dist, (offset_x, y_target))
        
        pygame.display.update()
        clock.tick(60)

    pygame.time.delay(400)
    
    # 3. Clash
    clash_steps = 10
    x_clash_loc = screen.get_width() // 2 - largeur_carte
    x_clash_dist = screen.get_width() // 2
    
    for step in range(clash_steps + 1):
        t = step / clash_steps
        curr_x_loc = x_loc + (x_clash_loc - x_loc) * t
        curr_x_dist = x_dist + (x_clash_dist - x_dist) * t
        
        screen.blit(scaled_bg, (0, 0))
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        img_dist = carte_distante.Resize_Card(carte_distante.Name, largeur_carte, hauteur_carte)
        screen.blit(img_loc, (int(curr_x_loc), y_target))
        screen.blit(img_dist, (int(curr_x_dist), y_target))
        
        pygame.display.update()
        clock.tick(60)
        
    # Impact! Screen shake and particles
    SOUNDS.play("clash_impact")
    impact_duration = 20
    particle_mgr = ParticleManager()
    clash_x = screen.get_width() // 2
    clash_y = y_target + hauteur_carte // 2
    particle_mgr.emit_clash(clash_x, clash_y, color=(255, 69, 0), count=40)
    particle_mgr.emit_clash(clash_x, clash_y, color=(255, 215, 0), count=20)
    
    for frame in range(impact_duration):
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        screen.blit(scaled_bg, (dx, dy))
        
        bounce_x_loc = x_clash_loc - 15 + dx
        bounce_x_dist = x_clash_dist + 15 + dx
        
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        img_dist = carte_distante.Resize_Card(carte_distante.Name, largeur_carte, hauteur_carte)
        
        screen.blit(img_loc, (bounce_x_loc, y_target + dy))
        screen.blit(img_dist, (bounce_x_dist, y_target + dy))
        
        particle_mgr.update()
        particle_mgr.draw(screen)
        
        pygame.display.update()
        clock.tick(60)
        
    # Slide back
    slide_back_steps = 10
    for step in range(slide_back_steps + 1):
        t = step / slide_back_steps
        curr_x_loc = x_clash_loc - 15 + (x_loc - (x_clash_loc - 15)) * t
        curr_x_dist = x_clash_dist + 15 + (x_dist - (x_clash_dist + 15)) * t
        
        screen.blit(scaled_bg, (0, 0))
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        img_dist = carte_distante.Resize_Card(carte_distante.Name, largeur_carte, hauteur_carte)
        screen.blit(img_loc, (int(curr_x_loc), y_target))
        screen.blit(img_dist, (int(curr_x_dist), y_target))
        
        particle_mgr.update()
        particle_mgr.draw(screen)
        pygame.display.update()
        clock.tick(60)
        
    # Floating damage and stats update
    damage_texts = []
    if damage_loc > 0:
        damage_texts.append(FloatingText(f"-{damage_loc} HP", x_loc + largeur_carte // 2, y_target + hauteur_carte // 2, (255, 0, 0), font_dmg, lifetime=50))
    if damage_dist > 0:
        damage_texts.append(FloatingText(f"-{damage_dist} HP", x_dist + largeur_carte // 2, y_target + hauteur_carte // 2, (255, 0, 0), font_dmg, lifetime=50))
        
    atk_decay_loc = initial_atk_loc - int(initial_atk_loc * 0.8)
    atk_decay_dist = initial_atk_dist - int(initial_atk_dist * 0.8)
    if atk_decay_loc > 0:
        damage_texts.append(FloatingText(f"-{atk_decay_loc} ATK", x_loc + largeur_carte // 2, y_target + hauteur_carte // 2 + 40, (255, 140, 0), font_dmg, lifetime=50))
    if atk_decay_dist > 0:
        damage_texts.append(FloatingText(f"-{atk_decay_dist} ATK", x_dist + largeur_carte // 2, y_target + hauteur_carte // 2 + 40, (255, 140, 0), font_dmg, lifetime=50))

    float_duration = 60
    for frame in range(float_duration):
        screen.blit(scaled_bg, (0, 0))
        
        img_loc = carte_locale.Resize_Card(carte_locale.Name, largeur_carte, hauteur_carte)
        img_dist = carte_distante.Resize_Card(carte_distante.Name, largeur_carte, hauteur_carte)
        screen.blit(img_loc, (x_loc, y_target))
        screen.blit(img_dist, (x_dist, y_target))
        
        lbl_l = font_large.render(label_loc, True, (0, 255, 255))
        lbl_d = font_large.render(label_dist, True, (255, 128, 0))
        screen.blit(lbl_l, (x_loc + 40, y_target - 40))
        screen.blit(lbl_d, (x_dist + 10, y_target - 40))
        
        t = min(1.0, frame / 30.0)
        curr_hp_loc = int(initial_hp_loc - damage_loc * t)
        curr_hp_dist = int(initial_hp_dist - damage_dist * t)
        
        curr_atk_loc = int(initial_atk_loc - atk_decay_loc * t)
        curr_atk_dist = int(initial_atk_dist - atk_decay_dist * t)
        
        atk_txt_l = font_large.render(f'ATK: {curr_atk_loc}', True, (255, 0, 0))
        hp_txt_l = font_large.render(f'HP: {max(curr_hp_loc, 0)}', True, (0, 255, 0))
        atk_txt_d = font_large.render(f'ATK: {curr_atk_dist}', True, (255, 0, 0))
        hp_txt_d = font_large.render(f'HP: {max(curr_hp_dist, 0)}', True, (0, 255, 0))
        
        screen.blit(atk_txt_l, (x_loc, y_target + hauteur_carte + 5))
        screen.blit(hp_txt_l, (x_loc, y_target + hauteur_carte + 35))
        screen.blit(atk_txt_d, (x_dist, y_target + hauteur_carte + 5))
        screen.blit(hp_txt_d, (x_dist, y_target + hauteur_carte + 35))
        
        for dt in damage_texts:
            dt.update()
            dt.draw(screen)
            
        particle_mgr.update()
        particle_mgr.draw(screen)
        
        pygame.display.update()
        clock.tick(60)
        
    pygame.time.delay(1000)




# Variable globale pour stocker la dernière carte jouée par le bot
derniere_carte_bot = None


def bot_choisir_carte(cartes_bot, cartes_joueur):
    global derniere_carte_bot  # On utilise la variable globale pour mémoriser la dernière carte jouée

    # Fonction d'évaluation pour déterminer la valeur d'une carte
    def evaluer_carte(carte):
        return carte.LifePoint + carte.AttackPoint * 2

    # Identifier la carte la plus menaçante du joueur
    def carte_menaçante(cartes_joueur):
        return max(cartes_joueur, key=lambda carte: evaluer_carte(carte))

    # Appliquer les règles de combat sans affecter les vraies valeurs
    def appliquer_regles_combat(LifePoint_bot, AttackPoint_bot, LifePoint_joueur, AttackPoint_joueur):
        LifePoint_joueur -= AttackPoint_bot
        LifePoint_bot -= AttackPoint_joueur

        AttackPoint_joueur = int(AttackPoint_joueur - (AttackPoint_joueur * 0.2))
        AttackPoint_bot = int(AttackPoint_bot - (AttackPoint_bot * 0.2))

        if LifePoint_bot < 0:
            LifePoint_bot = abs(LifePoint_bot) + 200
        elif LifePoint_joueur < 0:
            LifePoint_joueur = abs(LifePoint_joueur) + 200

        if LifePoint_bot == 0 or AttackPoint_bot <= 0:
            LifePoint_bot = 0
            AttackPoint_bot = 0
        if LifePoint_joueur == 0 or AttackPoint_joueur <= 0:
            LifePoint_joueur = 0
            AttackPoint_joueur = 0

        return LifePoint_bot, AttackPoint_bot, LifePoint_joueur, AttackPoint_joueur

    # Minimax avec élagage alpha-bêta
    def minimax(LifePoint_bot, AttackPoint_bot, LifePoint_joueur, AttackPoint_joueur, profondeur, alpha, beta, maximisant):
        if profondeur == 0 or LifePoint_joueur <= 0 or LifePoint_bot <= 0:
            return LifePoint_bot + AttackPoint_bot * 2

        if maximisant:
            max_eval = -float('inf')
            for carte_joueur in cartes_joueur:
                LifePoint_joueur_clone, AttackPoint_joueur_clone, LifePoint_bot_clone, AttackPoint_bot_clone = appliquer_regles_combat(
                    LifePoint_bot, AttackPoint_bot, carte_joueur.LifePoint, carte_joueur.AttackPoint)
                evaluation = minimax(LifePoint_bot_clone, AttackPoint_bot_clone, LifePoint_joueur_clone, AttackPoint_joueur_clone, profondeur - 1, alpha, beta, False)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for carte_bot in cartes_bot:
                LifePoint_joueur_clone, AttackPoint_joueur_clone, LifePoint_bot_clone, AttackPoint_bot_clone = appliquer_regles_combat(
                    carte_bot.LifePoint, carte_bot.AttackPoint, LifePoint_joueur, AttackPoint_joueur)
                evaluation = minimax(LifePoint_bot_clone, AttackPoint_bot_clone, LifePoint_joueur_clone, AttackPoint_joueur_clone, profondeur - 1, alpha, beta, True)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    meilleure_carte_bot = None
    profondeur = 5

    # Identifier la carte menaçante du joueur
    carte_cible = carte_menaçante(cartes_joueur)

    # Liste des cartes avec leur score
    cartes_et_scores = []

    for carte_bot in cartes_bot:
        if carte_bot.LifePoint <= 0 or carte_bot.AttackPoint <= 0:
            continue

        # Calcul du score via Minimax
        score_carte = minimax(carte_bot.LifePoint, carte_bot.AttackPoint, carte_cible.LifePoint, carte_cible.AttackPoint, profondeur, -float('inf'), float('inf'), True)

        # Bonus pour cibler la carte la plus menaçante
        if carte_cible in cartes_joueur:
            score_carte += random.randint(50, 150)

        cartes_et_scores.append((carte_bot, score_carte))

    # Gestion du cas où aucune carte n'est disponible après filtrage
    if not cartes_et_scores:
        meilleure_carte_bot = random.choice(cartes_bot)
        derniere_carte_bot = meilleure_carte_bot
        return meilleure_carte_bot

    # Trier les cartes en fonction de leur score, de la meilleure à la pire
    cartes_et_scores.sort(key=lambda x: x[1], reverse=True)

    # Ne pas rejouer la dernière carte si possible
    if derniere_carte_bot is not None:
        cartes_et_scores = [cs for cs in cartes_et_scores if cs[0] != derniere_carte_bot]
        # Si le filtrage supprime toutes les options, on réinitialise la liste
        if not cartes_et_scores:
            cartes_et_scores = [(c, minimax(c.LifePoint, c.AttackPoint, carte_cible.LifePoint, carte_cible.AttackPoint, profondeur, -float('inf'), float('inf'), True)) for c in cartes_bot]

    # Prendre une carte parmi les 3 meilleures, avec variabilité
    top_cartes = cartes_et_scores[:3]
    nb_cartes_disponibles = len(top_cartes)

    if nb_cartes_disponibles == 1:
        meilleure_carte_bot = top_cartes[0][0]
    elif nb_cartes_disponibles == 2:
        meilleure_carte_bot = random.choices([c[0] for c in top_cartes], weights=[0.7, 0.3])[0]
    else:
        meilleure_carte_bot = random.choices([c[0] for c in top_cartes], weights=[0.6, 0.3, 0.1])[0]

    # Mémoriser la carte sélectionnée
    derniere_carte_bot = meilleure_carte_bot

    return meilleure_carte_bot



def gerer_affrontement(screen, cartes_selectionnees):
    cartes_joueur = cartes_selectionnees[:5]
    cartes_bot = cartes_selectionnees[5:]

    image_de_fond = pygame.image.load(normalize_path('Image', 'Home_screen(2).jpeg')).convert_alpha()
    scaled_image_de_fond = pygame.transform.scale(image_de_fond, (screen.get_width(), screen.get_height()))

    pygame.mixer.music.load(normalize_path('Sound', 'Background.mp3'))
    pygame.mixer.music.play(loops=-1)

    def afficher_cartes_grandes(screen,scaled_image_de_fond,carte_joueur, carte_bot, vie_attaque):
        screen.blit(scaled_image_de_fond, (0, 0))
        largeur_carte_grande, hauteur_carte_grande = 200, 300
        x_joueur = (screen.get_width() // 2 - largeur_carte_grande) - 100
        x_bot = (screen.get_width() // 2 + largeur_carte_grande) + 100

        image_joueur = carte_joueur.Resize_Card(carte_joueur.Name, largeur_carte_grande, hauteur_carte_grande)
        image_bot = carte_bot.Resize_Card(carte_bot.Name, largeur_carte_grande, hauteur_carte_grande)

        screen.blit(image_joueur, (x_joueur, screen.get_height() // 2 - hauteur_carte_grande // 2))
        screen.blit(image_bot, (x_bot, screen.get_height() // 2 - hauteur_carte_grande // 2))

        font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 25)

        # Affichage des points de vie et d'attaque actuels ou calculés
        if vie_attaque == "avant":
            attaque_text_joueur = font.render(f'ATK: {carte_joueur.AttackPoint}', True, (255, 0, 0))
            vie_text_joueur = font.render(f'HP: {carte_joueur.LifePoint}', True, (0, 255, 0))

            attaque_text_bot = font.render(f'ATK: {carte_bot.AttackPoint}', True, (255, 0, 0))
            vie_text_bot = font.render(f'HP: {carte_bot.LifePoint}', True, (0, 255, 0))
        elif vie_attaque == "apres":
            attaque_text_joueur = font.render(f'ATK: {carte_joueur.AttackPoint}', True, (255, 0, 0))
            vie_text_joueur = font.render(f'HP: {max(carte_joueur.LifePoint, 0)}', True, (0, 255, 0))

            attaque_text_bot = font.render(f'ATK: {carte_bot.AttackPoint}', True, (255, 0, 0))
            vie_text_bot = font.render(f'HP: {max(carte_bot.LifePoint, 0)}', True, (0, 255, 0))

        # Afficher les textes en évitant le chevauchement
        screen.blit(attaque_text_joueur, (x_joueur, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 5))
        screen.blit(vie_text_joueur, (x_joueur, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 35))

        screen.blit(attaque_text_bot, (x_bot, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 5))
        screen.blit(vie_text_bot, (x_bot, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 35))

        pygame.display.update()

    def afficher_message_final(message):
        font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 60)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        screen.blit(scaled_image_de_fond, (0, 0))  # Réafficher l'image de fond
        screen.blit(text_surface, text_rect)
        pygame.display.update()

        pygame.time.delay(3000)  # Affiche le message pendant 3 secondes
    


    def draw_button(surface, text, x, y, padding, color, hover_color, font, action=None):
        text_surface = font.render(text, True, (255, 255, 255))
        button_width = text_surface.get_width() + padding * 2
        button_height = text_surface.get_height() + padding
        button_x = x - button_width + 20  # Ajuster la position x pour qu'il soit à droite
        button_y = y

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_color = hover_color if button_x < mouse[0] < button_x + button_width and button_y < mouse[1] < button_y + button_height else color
        pygame.draw.rect(surface, button_color, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), (button_x, button_y, button_width, button_height), 3, border_radius=10)

        text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        surface.blit(text_surface, text_rect)

        if button_x < mouse[0] < button_x + button_width and button_y < mouse[1] < button_y + button_height and click[0] == 1:
            if action:
                action()


    # Fonction pour fermer le jeu
    def quit_game():
        pygame.quit()
        quit()
    

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    font_instruction = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 30)  # Taille plus réduite


    def mainloop():
        play_particles = ParticleManager()
        running = True
        
        # Initialisation du deck de cartes spéciales (2 aléatoires chacun)
        player_specials = [random.randint(1, 7), random.randint(1, 7)]
        bot_specials = [random.randint(1, 7), random.randint(1, 7)]
        active_spell_id = None
        floating_texts = []
        bot_evaluated_specials = False
        bot_active_spell_banner = None
        bot_banner_timer = 0
        
        # Initialisation de l'Éveil (Awakening)
        eveil_disponible = True
        eveil_actif = False
        eveil_tours_restants = 0
        
        bot_eveil_disponible = True
        bot_eveil_actif = False
        bot_eveil_tours_restants = 0
        
        def add_floating_text(text, x, y, color=(0, 255, 0)):
            floating_texts.append({
                "text": text,
                "x": x,
                "y": y,
                "color": color,
                "timer": 45
            })
            
        def bot_decide_special(bot_cards, player_cards, bot_specs):
            if not bot_specs:
                return None
            if random.random() > 0.35: # 35% de chance de lancer un sort à chaque tour
                return None
                
            spell_id = random.choice(bot_specs)
            
            if spell_id == 1: # Soin Lacryma (+800 HP)
                weak_allies = [c for c in bot_cards if c.LifePoint < 1500]
                if weak_allies:
                    target = min(weak_allies, key=lambda c: c.LifePoint)
                    apply_spell_effect(1, target)
                    SOUNDS.play("special_activate")
                    idx = bot_cards.index(target)
                    px = 50 + idx * 120
                    play_particles.emit_sparkle(px + 50, 125, color=(0, 255, 100), count=25)
                    add_floating_text("+800 HP", px + 50, 210, (0, 255, 100))
                    bot_specs.remove(1)
                    return 1
            elif spell_id == 2: # Bouclier Erza
                if bot_cards:
                    target = max(bot_cards, key=lambda c: c.AttackPoint)
                    apply_spell_effect(2, target)
                    SOUNDS.play("special_activate")
                    idx = bot_cards.index(target)
                    px = 50 + idx * 120
                    play_particles.emit_sparkle(px + 50, 125, color=(0, 200, 255), count=25)
                    add_floating_text("SHIELD!", px + 50, 210, (0, 200, 255))
                    bot_specs.remove(2)
                    return 2
            elif spell_id == 3: # Rage Dragon (+250 ATK)
                if bot_cards:
                    target = max(bot_cards, key=lambda c: c.LifePoint)
                    apply_spell_effect(3, target)
                    SOUNDS.play("special_activate")
                    idx = bot_cards.index(target)
                    px = 50 + idx * 120
                    play_particles.emit_sparkle(px + 50, 125, color=(255, 100, 0), count=25)
                    add_floating_text("+250 ATK", px + 50, 210, (255, 100, 0))
                    bot_specs.remove(3)
                    return 3
            elif spell_id == 4: # Origine Sec. (+400 ATK, -300 HP)
                healthy = [c for c in bot_cards if c.LifePoint > 500]
                if healthy:
                    target = max(healthy, key=lambda c: c.LifePoint)
                    apply_spell_effect(4, target)
                    SOUNDS.play("special_activate")
                    idx = bot_cards.index(target)
                    px = 50 + idx * 120
                    play_particles.emit_sparkle(px + 50, 125, color=(255, 0, 100), count=25)
                    add_floating_text("+400 ATK / -300 HP", px + 50, 210, (255, 0, 100))
                    bot_specs.remove(4)
                    return 4
            elif spell_id == 5: # Portail Eclipse
                if bot_cards and player_cards:
                    weakest = min(bot_cards, key=lambda c: c.LifePoint)
                    strongest = max(player_cards, key=lambda c: c.LifePoint)
                    if weakest.LifePoint < 800 and strongest.LifePoint > 1600:
                        apply_spell_effect(5, weakest, all_enemy_cards=player_cards)
                        SOUNDS.play("special_activate")
                        idx_b = bot_cards.index(weakest)
                        idx_p = player_cards.index(strongest)
                        play_particles.emit_sparkle(50 + idx_b * 120 + 50, 125, color=(200, 200, 255), count=15)
                        play_particles.emit_sparkle(50 + idx_p * 120 + 50, screen.get_height() - 145, color=(200, 200, 255), count=15)
                        add_floating_text("HP SWAP!", 50 + idx_b * 120 + 50, 210, (200, 200, 255))
                        add_floating_text("HP SWAP!", 50 + idx_p * 120 + 50, screen.get_height() - 250, (200, 200, 255))
                        bot_specs.remove(5)
                        return 5
            elif spell_id == 6: # Loi des Fées (-300 HP all player cards)
                apply_spell_effect(6, None, all_enemy_cards=player_cards)
                SOUNDS.play("special_activate")
                for idx_p, c in enumerate(player_cards):
                    px = 50 + idx_p * 120
                    play_particles.emit_sparkle(px + 50, screen.get_height() - 145, color=(255, 50, 50), count=15)
                    add_floating_text("-300 HP", px + 50, screen.get_height() - 250, (255, 50, 50))
                bot_specs.remove(6)
                return 6
            elif spell_id == 7: # Sceau Zeleph (-50% ATK enemy)
                if player_cards:
                    target = max(player_cards, key=lambda c: c.AttackPoint)
                    apply_spell_effect(7, target)
                    SOUNDS.play("special_activate")
                    idx_p = player_cards.index(target)
                    px = 50 + idx_p * 120
                    play_particles.emit_sparkle(px + 50, screen.get_height() - 145, color=(150, 0, 255), count=25)
                    add_floating_text("-50% ATK!", px + 50, screen.get_height() - 250, (150, 0, 255))
                    bot_specs.remove(7)
                    return 7
            return None

        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Évaluation des sorts du bot à chaque nouveau tour
            if not bot_evaluated_specials:
                used_sp = bot_decide_special(cartes_bot, cartes_joueur, bot_specials)
                if used_sp:
                    bot_active_spell_banner = f"I.A. UTILISE {L('special_' + str(used_sp) + '_name').upper()} !"
                    bot_banner_timer = 45
                bot_evaluated_specials = True

            # --- ÉVALUATION DE L'ÉVEIL DU BOT ---
            if bot_eveil_disponible and ((len(cartes_bot) <= 3 and len(cartes_bot) < len(cartes_joueur)) or len(cartes_bot) == 1):
                bot_eveil_actif = True
                bot_eveil_tours_restants = 3
                bot_eveil_disponible = False
                SOUNDS.play("special_activate")
                for card in cartes_bot:
                    card.LifePoint += 800
                    card.AttackPoint += 300
                    card.is_eveiled = True
                    add_floating_text(L("eveil_activated"), 50 + cartes_bot.index(card) * 120 + 50, 210, (255, 140, 0))
                for card in cartes_bot:
                    idx_c = cartes_bot.index(card)
                    play_particles.emit_clash(50 + idx_c * 120 + 50, 125, color=(255, 69, 0), count=25)
                bot_active_spell_banner = "🔥 L'I.A. ACTIVE SON EVEIL MAGIQUE ! 🔥"
                bot_banner_timer = 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # 0. Clic sur le bouton Éveil
                        if eveil_btn_rect and eveil_btn_rect.collidepoint(event.pos):
                            eveil_actif = True
                            eveil_tours_restants = 3
                            eveil_disponible = False
                            SOUNDS.play("special_activate")
                            for card in cartes_joueur:
                                card.LifePoint += 800
                                card.AttackPoint += 300
                                card.is_eveiled = True
                                add_floating_text(L("eveil_activated"), 50 + cartes_joueur.index(card) * 120 + 50, screen.get_height() - 250, (255, 140, 0))
                            for card in cartes_joueur:
                                idx_c = cartes_joueur.index(card)
                                play_particles.emit_clash(50 + idx_c * 120 + 50, screen.get_height() - 125, color=(255, 69, 0), count=25)
                            bot_active_spell_banner = f"🔥 {L('eveil_title')} 🔥"
                            bot_banner_timer = 60
                            continue

                        # 1. Clic sur le plateau de cartes spéciales locales
                        spell_clicked = False
                        for idx_sp, spell_id in enumerate(player_specials):
                            sp_x = screen.get_width() - 380 + 15 + idx_sp * 160
                            sp_y = screen.get_height() - 230 + 35
                            sp_w, sp_h = 150, 110
                            if sp_x <= event.pos[0] <= sp_x + sp_w and sp_y <= event.pos[1] <= sp_y + sp_h:
                                spell_clicked = True
                                if active_spell_id == spell_id:
                                    active_spell_id = None
                                    SOUNDS.play("ui_click")
                                else:
                                    active_spell_id = spell_id
                                    SOUNDS.play("ui_click")
                                break
                                
                        if spell_clicked:
                            continue
                            
                        # 2. Clic avec sort actif (Ciblage)
                        if active_spell_id is not None:
                            target_selected = False
                            
                            # Sorts ciblant des alliés (1, 2, 3, 4, 5)
                            if active_spell_id in [1, 2, 3, 4, 5]:
                                for i, carte in enumerate(cartes_joueur):
                                    position_x = 50 + i * (100 + 20)
                                    if position_x <= event.pos[0] <= position_x + 100 and screen.get_height() - 220 <= event.pos[1] <= screen.get_height() - 50:
                                        apply_spell_effect(active_spell_id, carte, all_enemy_cards=cartes_bot)
                                        SOUNDS.play("special_activate")
                                        
                                        p_color = (0, 255, 100)
                                        if active_spell_id == 2: p_color = (0, 200, 255)
                                        elif active_spell_id == 3: p_color = (255, 100, 0)
                                        elif active_spell_id == 4: p_color = (255, 0, 100)
                                        elif active_spell_id == 5: p_color = (200, 200, 255)
                                        
                                        play_particles.emit_sparkle(event.pos[0], event.pos[1], color=p_color, count=25)
                                        add_floating_text(L(f"special_{active_spell_id}_name").upper(), position_x + 50, screen.get_height() - 240, p_color)
                                        
                                        player_specials.remove(active_spell_id)
                                        active_spell_id = None
                                        target_selected = True
                                        break
                                        
                            # Sort ciblant un ennemi (7)
                            elif active_spell_id == 7:
                                for i, carte in enumerate(cartes_bot):
                                    position_x = 50 + i * (100 + 20)
                                    if position_x <= event.pos[0] <= position_x + 100 and 50 <= event.pos[1] <= 200:
                                        apply_spell_effect(7, carte)
                                        SOUNDS.play("special_activate")
                                        
                                        play_particles.emit_sparkle(event.pos[0], event.pos[1], color=(150, 0, 255), count=25)
                                        add_floating_text(L("special_7_name").upper(), position_x + 50, 210, (150, 0, 255))
                                        
                                        player_specials.remove(7)
                                        active_spell_id = None
                                        target_selected = True
                                        break
                                        
                            # Sort immédiat (6 - Loi des Fées)
                            if active_spell_id == 6:
                                apply_spell_effect(6, None, all_enemy_cards=cartes_bot)
                                SOUNDS.play("special_activate")
                                for i, c in enumerate(cartes_bot):
                                    px = 50 + i * 120
                                    play_particles.emit_sparkle(px + 50, 125, color=(255, 215, 0), count=15)
                                    add_floating_text("-300 HP", px + 50, 210, (255, 50, 50))
                                    
                                player_specials.remove(6)
                                active_spell_id = None
                                target_selected = True
                                
                            if target_selected:
                                continue
                                
                        # 3. Clic normal sur une carte de combat (seulement si aucun sort n'est en cours de ciblage)
                        if active_spell_id is None:
                            for i, carte in enumerate(cartes_joueur):
                                position_x = 50 + i * (100 + 20)
                                if position_x <= event.pos[0] <= position_x + 100 and screen.get_height() - 220 <= event.pos[1] <= screen.get_height() - 50:
                                    carte_joueur_choisie = carte
                                    carte_bot_choisie = bot_choisir_carte(cartes_bot, cartes_joueur)
                                    
                                    init_hp_loc = carte_joueur_choisie.LifePoint
                                    init_hp_dist = carte_bot_choisie.LifePoint
                                    init_atk_loc = carte_joueur_choisie.AttackPoint
                                    init_atk_dist = carte_bot_choisie.AttackPoint
                                    
                                    # Gestion des boucliers dans l'animation et le combat
                                    dmg_loc = carte_bot_choisie.AttackPoint
                                    if getattr(carte_joueur_choisie, 'has_shield', False):
                                        dmg_loc = 0
                                        
                                    dmg_dist = carte_joueur_choisie.AttackPoint
                                    if getattr(carte_bot_choisie, 'has_shield', False):
                                        dmg_dist = 0
                                        
                                    animer_combat_resolution(screen, scaled_image_de_fond, carte_joueur_choisie, carte_bot_choisie,
                                                             init_hp_loc, init_hp_dist, dmg_loc, dmg_dist, init_atk_loc, init_atk_dist,
                                                             "VOUS", "I.A.")
                                                             
                                    # Calcul des HP après affrontement
                                    if getattr(carte_joueur_choisie, 'has_shield', False):
                                        carte_joueur_choisie.has_shield = False
                                        add_floating_text("BLOCKED!", 50 + cartes_joueur.index(carte_joueur_choisie) * 120 + 50, screen.get_height() - 250, (0, 220, 255))
                                    else:
                                        carte_joueur_choisie.LifePoint -= carte_bot_choisie.AttackPoint
                                        
                                    if getattr(carte_bot_choisie, 'has_shield', False):
                                        carte_bot_choisie.has_shield = False
                                        add_floating_text("BLOCKED!", 50 + cartes_bot.index(carte_bot_choisie) * 120 + 50, 210, (0, 220, 255))
                                    else:
                                        carte_bot_choisie.LifePoint -= carte_joueur_choisie.AttackPoint
                                        
                                    carte_joueur_choisie.AttackPoint = int(carte_joueur_choisie.AttackPoint * 0.8)
                                    carte_bot_choisie.AttackPoint = int(carte_bot_choisie.AttackPoint * 0.8)
                                    
                                    # Si les points de vie tombent en dessous de zéro (Capture)
                                    if carte_bot_choisie.LifePoint < 0:
                                        carte_bot_choisie.LifePoint = abs(carte_bot_choisie.LifePoint) + 200
                                        carte_bot_choisie.AttackPoint += 100
                                        carte_bot_choisie.is_eveiled = False
                                        if carte_bot_choisie in cartes_bot:
                                            cartes_bot.remove(carte_bot_choisie)
                                        cartes_joueur.append(carte_bot_choisie)
                                    elif carte_joueur_choisie.LifePoint < 0:
                                        carte_joueur_choisie.LifePoint = abs(carte_joueur_choisie.LifePoint) + 200
                                        carte_joueur_choisie.AttackPoint += 100
                                        carte_joueur_choisie.is_eveiled = False
                                        if carte_joueur_choisie in cartes_joueur:
                                            cartes_joueur.remove(carte_joueur_choisie)
                                        cartes_bot.append(carte_joueur_choisie)
                                        
                                    # Suppression si mort définitive
                                    if carte_bot_choisie.LifePoint == 0 or carte_bot_choisie.AttackPoint <= 0:
                                        if carte_bot_choisie in cartes_bot:
                                            cartes_bot.remove(carte_bot_choisie)
                                    if carte_joueur_choisie.LifePoint == 0 or carte_joueur_choisie.AttackPoint <= 0:
                                        if carte_joueur_choisie in cartes_joueur:
                                            cartes_joueur.remove(carte_joueur_choisie)
                                            
                                    # Permet de re-évaluer les sorts I.A. au tour suivant
                                    bot_evaluated_specials = False
                                    
                                    # --- DECREMENTATION DES TIMERS D'EVEIL ---
                                    if eveil_actif:
                                        eveil_tours_restants -= 1
                                        if eveil_tours_restants == 0:
                                            eveil_actif = False
                                            for card in cartes_joueur:
                                                if getattr(card, 'is_eveiled', False):
                                                    card.is_eveiled = False
                                                    card.AttackPoint = max(50, card.AttackPoint - 300 - 150)
                                                    card.LifePoint = max(100, card.LifePoint - 500)
                                                    add_floating_text(L("eveil_exhausted"), 50 + cartes_joueur.index(card) * 120 + 50, screen.get_height() - 250, (255, 50, 50))
                                            
                                    if bot_eveil_actif:
                                        bot_eveil_tours_restants -= 1
                                        if bot_eveil_tours_restants == 0:
                                            bot_eveil_actif = False
                                            for card in cartes_bot:
                                                if getattr(card, 'is_eveiled', False):
                                                    card.is_eveiled = False
                                                    card.AttackPoint = max(50, card.AttackPoint - 300 - 150)
                                                    card.LifePoint = max(100, card.LifePoint - 500)
                                                    add_floating_text(L("eveil_exhausted"), 50 + cartes_bot.index(card) * 120 + 50, 210, (255, 50, 50))
                                    
                                    if not cartes_joueur:
                                        afficher_message_final("You Lose")
                                        running = False
                                    elif not cartes_bot:
                                        afficher_message_final("You Win")
                                        running = False
                                    break

            # Dessin de l'arène
            screen.blit(scaled_image_de_fond, (0, 0))
            
            # Mise à jour des particules
            play_particles.emit_ambient(screen.get_width(), screen.get_height(), color=(255, 160, 50), count=1)
            play_particles.update()
            play_particles.draw(screen)
            
            font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 15)
            
            # 1. Rendu des cartes alliées
            for i, carte in enumerate(cartes_joueur):
                position_x = 50 + i * (100 + 20)
                is_hovered = position_x <= mouse_pos[0] <= position_x + 100 and screen.get_height() - 200 <= mouse_pos[1] <= screen.get_height() - 50
                offset_y = -15 if is_hovered else 0
                
                if is_hovered:
                    play_particles.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 215, 0), count=1)
                    
                glow_border = None
                if active_spell_id is not None:
                    if active_spell_id in [1, 2, 3, 4, 5]:
                        g_val = int(127 + 128 * math.sin(pygame.time.get_ticks() / 150.0))
                        glow_border = (0, g_val, 0) # Vert scintillant ciblage
                        
                image_redim = carte.Resize_Card(carte.Name, 100, 150)
                screen.blit(image_redim, (position_x, screen.get_height() - 200 + offset_y))
                
                # Auras des sorts
                if glow_border:
                    pygame.draw.rect(screen, glow_border, (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)
                elif getattr(carte, 'is_eveiled', False):
                    t_val = pygame.time.get_ticks()
                    g_val = int(150 + 105 * math.sin(t_val / 100.0))
                    pygame.draw.rect(screen, (255, g_val, 0), (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 4, border_radius=6)
                    if random.random() < 0.12:
                        play_particles.emit_sparkle(position_x + 50, screen.get_height() - 125 + offset_y, color=(255, 140, 0), count=2)
                elif getattr(carte, 'has_shield', False):
                    pygame.draw.rect(screen, (0, 220, 255), (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)
                elif getattr(carte, 'has_seal', False):
                    pygame.draw.rect(screen, (150, 0, 255), (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)
                    
                attaque_text = font.render(f'ATK: {carte.AttackPoint}', True, (255, 0, 0))
                vie_text = font.render(f'HP: {carte.LifePoint}', True, (0, 255, 0))
                screen.blit(attaque_text, (position_x, screen.get_height() - 200 + offset_y + 155))
                screen.blit(vie_text, (position_x, screen.get_height() - 200 + offset_y + 175))
                
            # 2. Rendu des cartes ennemies
            for i, carte in enumerate(cartes_bot):
                position_x = 50 + i * (100 + 20)
                
                glow_border = None
                if active_spell_id is not None:
                    if active_spell_id == 7:
                        g_val = int(127 + 128 * math.sin(pygame.time.get_ticks() / 150.0))
                        glow_border = (g_val, 0, g_val) # Violet scintillant ciblage sceau
                        
                image_redim = carte.Resize_Card(carte.Name, 100, 150)
                screen.blit(image_redim, (position_x, 50))
                
                # Auras des sorts
                if glow_border:
                    pygame.draw.rect(screen, glow_border, (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)
                elif getattr(carte, 'is_eveiled', False):
                    t_val = pygame.time.get_ticks()
                    g_val = int(150 + 105 * math.sin(t_val / 100.0))
                    pygame.draw.rect(screen, (255, g_val, 0), (position_x - 3, 50 - 3, 106, 156), 4, border_radius=6)
                    if random.random() < 0.12:
                        play_particles.emit_sparkle(position_x + 50, 125, color=(255, 140, 0), count=2)
                elif getattr(carte, 'has_shield', False):
                    pygame.draw.rect(screen, (0, 220, 255), (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)
                elif getattr(carte, 'has_seal', False):
                    pygame.draw.rect(screen, (150, 0, 255), (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)
                    
                vie_text = font.render(f'HP: {carte.LifePoint}', True, (0, 255, 0))
                attaque_text = font.render(f'ATK: {carte.AttackPoint}', True, (255, 0, 0))
                screen.blit(vie_text, (position_x, 50 + 155))
                screen.blit(attaque_text, (position_x, 50 + 175))
                
            # 3. Rendu du Plateau de Cartes Spéciales
            tray_x = screen.get_width() - 380
            tray_y = screen.get_height() - 230
            tray_w = 340
            tray_h = 160
            
            tray_surf = pygame.Surface((tray_w, tray_h), pygame.SRCALPHA)
            tray_surf.fill((25, 15, 35, 190))
            screen.blit(tray_surf, (tray_x, tray_y))
            pygame.draw.rect(screen, (0, 255, 255), (tray_x, tray_y, tray_w, tray_h), 2, border_radius=10)
            
            font_tray = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 12)
            lbl_tray = font_tray.render(L("special_cards_tray"), True, (255, 215, 0))
            screen.blit(lbl_tray, (tray_x + 15, tray_y + 10))
            
            for idx_sp, spell_id in enumerate(player_specials):
                sp_x = tray_x + 15 + idx_sp * 160
                sp_y = tray_y + 35
                sp_w, sp_h = 150, 110
                
                is_hovered = sp_x <= mouse_pos[0] <= sp_x + sp_w and sp_y <= mouse_pos[1] <= sp_y + sp_h
                is_active = (active_spell_id == spell_id)
                
                card_color = (35, 20, 50, 220)
                border_color = (100, 80, 120)
                
                if is_active:
                    border_color = (0, 255, 100)
                    card_color = (15, 55, 25, 240)
                elif is_hovered:
                    border_color = (255, 215, 0)
                    card_color = (55, 30, 80, 235)
                    if random.random() < 0.15:
                        play_particles.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 215, 0), count=1)
                        
                slot_surf = pygame.Surface((sp_w, sp_h), pygame.SRCALPHA)
                slot_surf.fill(card_color)
                screen.blit(slot_surf, (sp_x, sp_y))
                pygame.draw.rect(screen, border_color, (sp_x, sp_y, sp_w, sp_h), 2 if (is_hovered or is_active) else 1, border_radius=8)
                
                sp_name = L(f"special_{spell_id}_name")
                sp_name_surf = font_tray.render(sp_name, True, (255, 255, 255))
                screen.blit(sp_name_surf, sp_name_surf.get_rect(center=(sp_x + sp_w // 2, sp_y + 25)))
                
                sp_desc = L(f"special_{spell_id}_desc")
                font_desc = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 9)
                if len(sp_desc) > 20:
                    split_idx = sp_desc.rfind(" ", 0, 18)
                    if split_idx == -1: split_idx = 18
                    desc_p1 = font_desc.render(sp_desc[:split_idx], True, (200, 200, 200))
                    desc_p2 = font_desc.render(sp_desc[split_idx:], True, (160, 160, 160))
                    screen.blit(desc_p1, desc_p1.get_rect(center=(sp_x + sp_w // 2, sp_y + 60)))
                    screen.blit(desc_p2, desc_p2.get_rect(center=(sp_x + sp_w // 2, sp_y + 80)))
                else:
                    desc_surf = font_desc.render(sp_desc, True, (200, 200, 200))
                    screen.blit(desc_surf, desc_surf.get_rect(center=(sp_x + sp_w // 2, sp_y + 70)))
                    
            # 3.5. Rendu du bouton Éveil et du timer
            eveil_btn_rect = None
            if eveil_disponible and ((len(cartes_joueur) <= 3 and len(cartes_joueur) < len(cartes_bot)) or len(cartes_joueur) == 1):
                font_eveil = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
                eveil_btn_rect = draw_eveil_button(screen, screen_width - 550, screen_height - 180, 150, 50, font_eveil)
                
            if eveil_actif:
                font_timer = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
                lbl_timer = font_timer.render(L("eveil_remaining").format(eveil_tours_restants), True, (255, 140, 0))
                t_val = pygame.time.get_ticks()
                alpha_timer = int(180 + 75 * math.sin(t_val / 120.0))
                lbl_timer.set_alpha(alpha_timer)
                screen.blit(lbl_timer, lbl_timer.get_rect(center=(screen_width - 475, screen_height - 150)))
                # Particules d'ambiance de feu autour du timer
                if random.random() < 0.15:
                    play_particles.emit_sparkle(screen_width - 475 + random.randint(-40, 40), screen_height - 150 + random.randint(-8, 8), color=(255, 100, 0), count=1)
                    
            # 4. Rendu des textes flottants
            for ft in list(floating_texts):
                ft["timer"] -= 1
                ft["y"] -= 1.8
                alpha = int(255 * (ft["timer"] / 45.0))
                ft_font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 13)
                txt_surf = ft_font.render(ft["text"], True, ft["color"])
                txt_surf.set_alpha(alpha)
                screen.blit(txt_surf, (ft["x"] - txt_surf.get_width() // 2, ft["y"]))
                if ft["timer"] <= 0:
                    floating_texts.remove(ft)
                    
            # 5. Rendu du bandeau d'alerte des sorts de l'I.A.
            if bot_active_spell_banner and bot_banner_timer > 0:
                bot_banner_timer -= 1
                alpha_banner = int(min(255, 255 * (bot_banner_timer / 15.0)))
                
                banner_w = 600
                banner_h = 50
                banner_x = screen.get_width() // 2 - banner_w // 2
                banner_y = 230
                
                banner_surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
                banner_surf.fill((30, 10, 20, int(200 * (alpha_banner / 255.0))))
                screen.blit(banner_surf, (banner_x, banner_y))
                pygame.draw.rect(screen, (255, 50, 100, alpha_banner), (banner_x, banner_y, banner_w, banner_h), 2, border_radius=6)
                
                font_banner = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 16)
                text_b = font_banner.render(bot_active_spell_banner, True, (255, 220, 100))
                text_b.set_alpha(alpha_banner)
                screen.blit(text_b, text_b.get_rect(center=(screen.get_width() // 2, banner_y + banner_h // 2)))
                
                if bot_banner_timer <= 0:
                    bot_active_spell_banner = None
                    
            # Message d'instruction pour le ciblage
            if active_spell_id is not None:
                lbl_prompt = font_instruction.render(L("special_target_prompt"), True, (255, 215, 0))
                screen.blit(lbl_prompt, lbl_prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 280)))
                
            draw_button(screen, "Quitter", screen_width - 100, 50, 10, (120, 20, 20), (180, 30, 30), font_instruction, quit_game)
            pygame.display.update()


    mainloop()


def animer_melange_cartes(screen, scaled_bg, cartes_locales, cartes_distantes, local_order, remote_order, card_back_img):
    font_msg = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 30)
    font_small = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 15)
    
    # Préparez les nouvelles listes temporaires
    new_locales = [cartes_locales[idx] for idx in local_order]
    new_distantes = [cartes_distantes[idx] for idx in remote_order]
    
    clock = pygame.time.Clock()
    steps = 40
    particle_mgr = ParticleManager()
    
    # Positions de départ et d'arrivée
    start_x_loc = []
    target_x_loc = []
    for new_idx, old_idx in enumerate(local_order):
        start_x_loc.append(50 + old_idx * 120)
        target_x_loc.append(50 + new_idx * 120)
        
    start_x_dist = []
    target_x_dist = []
    for new_idx, old_idx in enumerate(remote_order):
        start_x_dist.append(50 + old_idx * 120)
        target_x_dist.append(50 + new_idx * 120)
        
    y_loc = screen.get_height() - 200
    y_dist = 50
    
    for step in range(steps + 1):
        t = step / steps
        t_smooth = t * t * (3 - 2 * t)
        
        screen.blit(scaled_bg, (0, 0))
        
        # Effet de texte clignotant
        draw_blinking_text("MELANGE DES CARTES...", (255, 215, 0), screen, screen.get_width() // 2, screen.get_height() // 2, font_msg, blink_speed=200)
        
        # Animer les cartes de l'adversaire (distantes)
        for i, carte in enumerate(new_distantes):
            curr_x = start_x_dist[i] + (target_x_dist[i] - start_x_dist[i]) * t_smooth
            wave_y = math.sin(t * math.pi) * 40 * (-1 if i % 2 == 0 else 1)
            curr_y = y_dist + wave_y
            
            image_redim = carte.Resize_Card(card_back_img, 100, 150)
            screen.blit(image_redim, (int(curr_x), int(curr_y)))
            
            if step % 2 == 0:
                particle_mgr.emit_sparkle(int(curr_x + 50), int(curr_y + 75), color=(255, 140, 0), count=1)
                
            vie_text = font_small.render('HP: ???', True, (0, 255, 0))
            attaque_text = font_small.render('ATK: ???', True, (255, 0, 0))
            screen.blit(vie_text, (int(curr_x), int(curr_y + 155)))
            screen.blit(attaque_text, (int(curr_x), int(curr_y + 175)))
            
        # Animer nos cartes (locales)
        for i, carte in enumerate(new_locales):
            curr_x = start_x_loc[i] + (target_x_loc[i] - start_x_loc[i]) * t_smooth
            wave_y = math.sin(t * math.pi) * 40 * (1 if i % 2 == 0 else -1)
            curr_y = y_loc + wave_y
            
            image_redim = carte.Resize_Card(carte.Name, 100, 150)
            screen.blit(image_redim, (int(curr_x), int(curr_y)))
            
            if step % 2 == 0:
                particle_mgr.emit_sparkle(int(curr_x + 50), int(curr_y + 75), color=(0, 255, 255), count=1)
                
            attaque_text = font_small.render(f'ATK: {carte.AttackPoint}', True, (255, 0, 0))
            vie_text = font_small.render(f'HP: {carte.LifePoint}', True, (0, 255, 0))
            screen.blit(attaque_text, (int(curr_x), int(curr_y + 155)))
            screen.blit(vie_text, (int(curr_x), int(curr_y + 175)))
            
        particle_mgr.update()
        particle_mgr.draw(screen)
        
        pygame.display.update()
        clock.tick(60)
        
    pygame.time.delay(300)


def gerer_affrontement_reseau(screen, local_cards, opponent_cards, net_mgr):
    image_de_fond = pygame.image.load(normalize_path('Image', 'Home_screen(2).jpeg')).convert_alpha()
    scaled_image_de_fond = pygame.transform.scale(image_de_fond, (screen.get_width(), screen.get_height()))

    pygame.mixer.music.load(normalize_path('Sound', 'Background.mp3'))
    pygame.mixer.music.play(loops=-1)

    # Identifie P1 (Hôte) et P2 (Client)
    if net_mgr.is_host:
        cartes_p1 = local_cards
        cartes_p2 = opponent_cards
    else:
        cartes_p1 = opponent_cards
        cartes_p2 = local_cards

    # Raccourcis pour l'affichage local vs distant
    cartes_locales = local_cards
    cartes_distantes = opponent_cards

    def afficher_combat_grandes(screen, scaled_image, carte_locale, carte_distante, vie_attaque):
        screen.blit(scaled_image, (0, 0))
        largeur_carte_grande, hauteur_carte_grande = 200, 300
        x_locale = (screen.get_width() // 2 - largeur_carte_grande) - 100
        x_distante = (screen.get_width() // 2 + largeur_carte_grande) + 100

        image_locale = carte_locale.Resize_Card(carte_locale.Name, largeur_carte_grande, hauteur_carte_grande)
        image_distante = carte_distante.Resize_Card(carte_distante.Name, largeur_carte_grande, hauteur_carte_grande)

        screen.blit(image_locale, (x_locale, screen.get_height() // 2 - hauteur_carte_grande // 2))
        screen.blit(image_distante, (x_distante, screen.get_height() // 2 - hauteur_carte_grande // 2))

        font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 25)

        # Labels pour identifier les cartes
        lbl_local = font.render("VOUS", True, (0, 255, 255))
        lbl_dist = font.render("ADVERSAIRE", True, (255, 128, 0))
        screen.blit(lbl_local, (x_locale + 40, screen.get_height() // 2 - hauteur_carte_grande // 2 - 40))
        screen.blit(lbl_dist, (x_distante + 10, screen.get_height() // 2 - hauteur_carte_grande // 2 - 40))

        if vie_attaque == "avant":
            attaque_text_locale = font.render(f'ATK: {carte_locale.AttackPoint}', True, (255, 0, 0))
            vie_text_locale = font.render(f'HP: {carte_locale.LifePoint}', True, (0, 255, 0))

            attaque_text_dist = font.render(f'ATK: {carte_distante.AttackPoint}', True, (255, 0, 0))
            vie_text_dist = font.render(f'HP: {carte_distante.LifePoint}', True, (0, 255, 0))
        elif vie_attaque == "apres":
            attaque_text_locale = font.render(f'ATK: {carte_locale.AttackPoint}', True, (255, 0, 0))
            vie_text_locale = font.render(f'HP: {max(carte_locale.LifePoint, 0)}', True, (0, 255, 0))

            attaque_text_dist = font.render(f'ATK: {carte_distante.AttackPoint}', True, (255, 0, 0))
            vie_text_dist = font.render(f'HP: {max(carte_distante.LifePoint, 0)}', True, (0, 255, 0))

        screen.blit(attaque_text_locale, (x_locale, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 5))
        screen.blit(vie_text_locale, (x_locale, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 35))

        screen.blit(attaque_text_dist, (x_distante, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 5))
        screen.blit(vie_text_dist, (x_distante, screen.get_height() // 2 - hauteur_carte_grande // 2 + hauteur_carte_grande + 35))

        pygame.display.update()

    def afficher_message_final(message):
        font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 60)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        screen.blit(scaled_image_de_fond, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)

    def draw_button(surface, text, x, y, padding, color, hover_color, font, action=None):
        text_surface = font.render(text, True, (255, 255, 255))
        button_width = text_surface.get_width() + padding * 2
        button_height = text_surface.get_height() + padding
        button_x = x - button_width + 20
        button_y = y

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_color = hover_color if button_x < mouse[0] < button_x + button_width and button_y < mouse[1] < button_y + button_height else color
        pygame.draw.rect(surface, button_color, (button_x, button_y, button_width, button_height), border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), (button_x, button_y, button_width, button_height), 3, border_radius=10)

        text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        surface.blit(text_surface, text_rect)

        if button_x < mouse[0] < button_x + button_width and button_y < mouse[1] < button_y + button_height and click[0] == 1:
            if action:
                action()

    def quit_game():
        net_mgr.disconnect()
        pygame.quit()
        quit()

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    font_instruction = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 30)
    font_small = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 15)

    local_choice_idx = None
    remote_choice_idx = None
    play_particles = ParticleManager()
    card_back_img = pygame.image.load(normalize_path('Image', 'Card_Back.png')).convert_alpha()
    running = True

    # Système de cartes spéciales en Réseau
    local_specials = []
    remote_specials = []
    active_spell_id = None
    floating_texts = []
    bot_active_spell_banner = None
    bot_banner_timer = 0
    
    # Système d'Éveil Multijoueur
    eveil_disponible = True
    eveil_actif = False
    eveil_tours_restants = 0
    
    opponent_eveil_disponible = True
    opponent_eveil_actif = False
    opponent_eveil_tours_restants = 0
    
    def add_floating_text(text, x, y, color=(0, 255, 0)):
        floating_texts.append({
            "text": text,
            "x": x,
            "y": y,
            "color": color,
            "timer": 45
        })

    # L'hôte distribue les cartes spéciales synchrones au début
    if net_mgr.is_host:
        local_specials = [random.randint(1, 7), random.randint(1, 7)]
        remote_specials = [random.randint(1, 7), random.randint(1, 7)]
        net_mgr.send({"type": "init_specials", "local": remote_specials, "remote": local_specials})

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # 1. Lire TOUS les messages réseau en attente
        msg = net_mgr.get_message()
        while msg is not None:
            if msg["type"] == "play_card":
                remote_choice_idx = msg["index"]
            elif msg["type"] == "init_specials":
                local_specials = msg["local"]
                remote_specials = msg["remote"]
            elif msg["type"] == "play_special":
                s_id = msg["spell_id"]
                if s_id == 6: # Global spell
                    apply_spell_effect(6, None, all_enemy_cards=cartes_locales)
                    SOUNDS.play("special_activate")
                    for idx_p, c in enumerate(cartes_locales):
                        px = 50 + idx_p * 120
                        play_particles.emit_sparkle(px + 50, screen.get_height() - 145, color=(255, 50, 50), count=15)
                        add_floating_text("-300 HP", px + 50, screen.get_height() - 250, (255, 50, 50))
                    bot_active_spell_banner = f"L'ADVERSAIRE LANCE {L('special_6_name').upper()} !"
                    bot_banner_timer = 45
                    if s_id in remote_specials:
                        remote_specials.remove(s_id)
                else:
                    t_idx = msg["target_idx"]
                    t_enemy = msg["target_is_enemy"] # Cible du point de vue de l'émetteur
                    
                    if t_enemy:
                        # Si l'adversaire cible son ennemi, c'est notre carte locale !
                        t_card = cartes_locales[t_idx]
                        px = 50 + t_idx * 120 + 50
                        py = screen.get_height() - 145
                    else:
                        # Si l'adversaire cible son allié, c'est sa propre carte (donc distante pour nous)
                        t_card = cartes_distantes[t_idx]
                        px = 50 + t_idx * 120 + 50
                        py = 125
                        
                    apply_spell_effect(s_id, t_card, all_enemy_cards=cartes_locales)
                    SOUNDS.play("special_activate")
                    
                    p_color = (0, 255, 100)
                    if s_id == 2: p_color = (0, 200, 255)
                    elif s_id == 3: p_color = (255, 100, 0)
                    elif s_id == 4: p_color = (255, 0, 100)
                    elif s_id == 5: p_color = (200, 200, 255)
                    elif s_id == 7: p_color = (150, 0, 255)
                    
                    play_particles.emit_sparkle(px, py, color=p_color, count=25)
                    add_floating_text(L(f"special_{s_id}_name").upper(), px, py - 40 if t_enemy else py + 85, p_color)
                    
                    bot_active_spell_banner = f"L'ADVERSAIRE LANCE {L('special_' + str(s_id) + '_name').upper()} !"
                    bot_banner_timer = 45
                    if s_id in remote_specials:
                        remote_specials.remove(s_id)
                        
            elif msg["type"] == "activate_eveil":
                opponent_eveil_actif = True
                opponent_eveil_tours_restants = 3
                opponent_eveil_disponible = False
                SOUNDS.play("special_activate")
                for card in cartes_distantes:
                    card.LifePoint += 800
                    card.AttackPoint += 300
                    card.is_eveiled = True
                    add_floating_text(L("eveil_activated"), 50 + cartes_distantes.index(card) * 120 + 50, 210, (255, 140, 0))
                for card in cartes_distantes:
                    idx_c = cartes_distantes.index(card)
                    play_particles.emit_clash(50 + idx_c * 120 + 50, 125, color=(255, 69, 0), count=25)
                bot_active_spell_banner = "🔥 L'ADVERSAIRE ACTIVE SON EVEIL ! 🔥"
                bot_banner_timer = 60
            elif msg["type"] == "disconnected":
                afficher_message_final("Adversaire deconnecte")
                net_mgr.disconnect()
                return
            msg = net_mgr.get_message()

        # 2. Lire les entrées utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Bouton Quitter
                    if screen_width - 200 <= event.pos[0] <= screen_width - 10 and 50 <= event.pos[1] <= 100:
                        running = False
                        net_mgr.disconnect()
                        return
                        
                    # 0. Clic sur le bouton Éveil
                    if eveil_btn_rect and eveil_btn_rect.collidepoint(event.pos):
                        eveil_actif = True
                        eveil_tours_restants = 3
                        eveil_disponible = False
                        SOUNDS.play("special_activate")
                        net_mgr.send({"type": "activate_eveil"})
                        for card in cartes_locales:
                            card.LifePoint += 800
                            card.AttackPoint += 300
                            card.is_eveiled = True
                            add_floating_text(L("eveil_activated"), 50 + cartes_locales.index(card) * 120 + 50, screen.get_height() - 250, (255, 140, 0))
                        for card in cartes_locales:
                            idx_c = cartes_locales.index(card)
                            play_particles.emit_clash(50 + idx_c * 120 + 50, screen.get_height() - 125, color=(255, 69, 0), count=25)
                        bot_active_spell_banner = f"🔥 {L('eveil_title')} 🔥"
                        bot_banner_timer = 60
                        continue

                    # Clic sur le plateau de cartes spéciales
                    spell_clicked = False
                    for idx_sp, spell_id in enumerate(local_specials):
                        sp_x = screen.get_width() - 380 + 15 + idx_sp * 160
                        sp_y = screen.get_height() - 230 + 35
                        sp_w, sp_h = 150, 110
                        if sp_x <= event.pos[0] <= sp_x + sp_w and sp_y <= event.pos[1] <= sp_y + sp_h:
                            spell_clicked = True
                            if active_spell_id == spell_id:
                                active_spell_id = None
                                SOUNDS.play("ui_click")
                            else:
                                active_spell_id = spell_id
                                SOUNDS.play("ui_click")
                            break
                            
                    if spell_clicked:
                        continue
                        
                    # Clic avec sort actif (Ciblage)
                    if active_spell_id is not None:
                        target_selected = False
                        
                        # Sorts ciblant un allié (1, 2, 3, 4, 5)
                        if active_spell_id in [1, 2, 3, 4, 5]:
                            for i, carte in enumerate(cartes_locales):
                                position_x = 50 + i * (100 + 20)
                                if position_x <= event.pos[0] <= position_x + 100 and screen.get_height() - 220 <= event.pos[1] <= screen.get_height() - 50:
                                    apply_spell_effect(active_spell_id, carte, all_enemy_cards=cartes_distantes)
                                    SOUNDS.play("special_activate")
                                    
                                    # Envoyer le sort au réseau
                                    net_mgr.send({"type": "play_special", "spell_id": active_spell_id, "target_idx": i, "target_is_enemy": False})
                                    
                                    p_color = (0, 255, 100)
                                    if active_spell_id == 2: p_color = (0, 200, 255)
                                    elif active_spell_id == 3: p_color = (255, 100, 0)
                                    elif active_spell_id == 4: p_color = (255, 0, 100)
                                    elif active_spell_id == 5: p_color = (200, 200, 255)
                                    
                                    play_particles.emit_sparkle(event.pos[0], event.pos[1], color=p_color, count=25)
                                    add_floating_text(L(f"special_{active_spell_id}_name").upper(), position_x + 50, screen.get_height() - 240, p_color)
                                    
                                    local_specials.remove(active_spell_id)
                                    active_spell_id = None
                                    target_selected = True
                                    break
                                    
                        # Sort ciblant un ennemi (7)
                        elif active_spell_id == 7:
                            for i, carte in enumerate(cartes_distantes):
                                position_x = 50 + i * (100 + 20)
                                if position_x <= event.pos[0] <= position_x + 100 and 50 <= event.pos[1] <= 200:
                                    apply_spell_effect(7, carte)
                                    SOUNDS.play("special_activate")
                                    
                                    # Envoyer au réseau
                                    net_mgr.send({"type": "play_special", "spell_id": 7, "target_idx": i, "target_is_enemy": True})
                                    
                                    play_particles.emit_sparkle(event.pos[0], event.pos[1], color=(150, 0, 255), count=25)
                                    add_floating_text(L("special_7_name").upper(), position_x + 50, 210, (150, 0, 255))
                                    
                                    local_specials.remove(7)
                                    active_spell_id = None
                                    target_selected = True
                                    break
                                    
                        # Sort global (6 - Loi des Fées)
                        if active_spell_id == 6:
                            apply_spell_effect(6, None, all_enemy_cards=cartes_distantes)
                            SOUNDS.play("special_activate")
                            
                            # Envoyer au réseau
                            net_mgr.send({"type": "play_special", "spell_id": 6})
                            
                            for i, c in enumerate(cartes_distantes):
                                px = 50 + i * 120
                                play_particles.emit_sparkle(px + 50, 125, color=(255, 215, 0), count=15)
                                add_floating_text("-300 HP", px + 50, 210, (255, 50, 50))
                                
                            local_specials.remove(6)
                            active_spell_id = None
                            target_selected = True
                            
                        if target_selected:
                            continue

                    # Choix classique de carte de combat (si aucun sort n'est actif)
                    if active_spell_id is None and local_choice_idx is None:
                        for i, carte in enumerate(cartes_locales):
                            position_x = 50 + i * (100 + 20)
                            if position_x <= event.pos[0] <= position_x + 100 and screen.get_height() - 220 <= event.pos[1] <= screen.get_height() - 50:
                                local_choice_idx = i
                                net_mgr.send({"type": "play_card", "index": local_choice_idx})
                                break

        # 3. Résolution du combat
        if local_choice_idx is not None and remote_choice_idx is not None:
            if net_mgr.is_host:
                idx_p1 = local_choice_idx
                idx_p2 = remote_choice_idx
            else:
                idx_p1 = remote_choice_idx
                idx_p2 = local_choice_idx

            carte_p1 = cartes_p1[idx_p1]
            carte_p2 = cartes_p2[idx_p2]

            carte_locale = cartes_locales[local_choice_idx]
            carte_distante = cartes_distantes[remote_choice_idx]

            init_hp_loc = carte_locale.LifePoint
            init_hp_dist = carte_distante.LifePoint
            init_atk_loc = carte_locale.AttackPoint
            init_atk_dist = carte_distante.AttackPoint
            
            # Application des boucliers
            dmg_loc = carte_distante.AttackPoint
            if getattr(carte_locale, 'has_shield', False):
                dmg_loc = 0
                
            dmg_dist = carte_locale.AttackPoint
            if getattr(carte_distante, 'has_shield', False):
                dmg_dist = 0

            animer_combat_resolution(screen, scaled_image_de_fond, carte_locale, carte_distante,
                                     init_hp_loc, init_hp_dist, dmg_loc, dmg_dist, init_atk_loc, init_atk_dist,
                                     "VOUS", "ADVERSAIRE")

            # Résolution des dégâts
            if getattr(carte_p1, 'has_shield', False):
                carte_p1.has_shield = False
                # Déterminer la coordonnée X selon qui est p1
                p1_idx = local_choice_idx if net_mgr.is_host else remote_choice_idx
                px_p1 = 50 + p1_idx * 120 + 50
                py_p1 = screen.get_height() - 250 if net_mgr.is_host else 210
                add_floating_text("BLOCKED!", px_p1, py_p1, (0, 220, 255))
            else:
                carte_p1.LifePoint -= carte_p2.AttackPoint

            if getattr(carte_p2, 'has_shield', False):
                carte_p2.has_shield = False
                p2_idx = remote_choice_idx if net_mgr.is_host else local_choice_idx
                px_p2 = 50 + p2_idx * 120 + 50
                py_p2 = 210 if net_mgr.is_host else screen.get_height() - 250
                add_floating_text("BLOCKED!", px_p2, py_p2, (0, 220, 255))
            else:
                carte_p2.LifePoint -= carte_p1.AttackPoint

            carte_p1.AttackPoint = int(carte_p1.AttackPoint * 0.8)
            carte_p2.AttackPoint = int(carte_p2.AttackPoint * 0.8)

            # Vols de cartes
            if carte_p2.LifePoint < 0:
                carte_p2.LifePoint = abs(carte_p2.LifePoint) + 200
                carte_p2.AttackPoint += 100
                carte_p2.is_eveiled = False
                if carte_p2 in cartes_p2:
                    cartes_p2.remove(carte_p2)
                cartes_p1.append(carte_p2)
            elif carte_p1.LifePoint < 0:
                carte_p1.LifePoint = abs(carte_p1.LifePoint) + 200
                carte_p1.AttackPoint += 100
                carte_p1.is_eveiled = False
                if carte_p1 in cartes_p1:
                    cartes_p1.remove(carte_p1)
                cartes_p2.append(carte_p1)

            # Mort définitive
            if carte_p2.LifePoint == 0 or carte_p2.AttackPoint <= 0:
                if carte_p2 in cartes_p2:
                    cartes_p2.remove(carte_p2)
            if carte_p1.LifePoint == 0 or carte_p1.AttackPoint <= 0:
                if carte_p1 in cartes_p1:
                    cartes_p1.remove(carte_p1)

            local_choice_idx = None
            remote_choice_idx = None

            # --- DECREMENTATION DES TIMERS D'EVEIL EN RESEAU ---
            if eveil_actif:
                eveil_tours_restants -= 1
                if eveil_tours_restants == 0:
                    eveil_actif = False
                    for card in cartes_locales:
                        if getattr(card, 'is_eveiled', False):
                            card.is_eveiled = False
                            card.AttackPoint = max(50, card.AttackPoint - 300 - 150)
                            card.LifePoint = max(100, card.LifePoint - 500)
                            add_floating_text(L("eveil_exhausted"), 50 + cartes_locales.index(card) * 120 + 50, screen.get_height() - 250, (255, 50, 50))
                            
            if opponent_eveil_actif:
                opponent_eveil_tours_restants -= 1
                if opponent_eveil_tours_restants == 0:
                    opponent_eveil_actif = False
                    for card in cartes_distantes:
                        if getattr(card, 'is_eveiled', False):
                            card.is_eveiled = False
                            card.AttackPoint = max(50, card.AttackPoint - 300 - 150)
                            card.LifePoint = max(100, card.LifePoint - 500)
                            add_floating_text(L("eveil_exhausted"), 50 + cartes_distantes.index(card) * 120 + 50, 210, (255, 50, 50))

            if not cartes_locales:
                afficher_message_final("You Lose")
                running = False
            elif not cartes_distantes:
                afficher_message_final("You Win")
                running = False

            if running:
                # Mélange synchronisé après round
                if net_mgr.is_host:
                    p1_order = list(range(len(cartes_p1)))
                    p2_order = list(range(len(cartes_p2)))
                    random.shuffle(p1_order)
                    random.shuffle(p2_order)
                    net_mgr.send({"type": "shuffle", "p1_order": p1_order, "p2_order": p2_order})
                else:
                    p1_order = None
                    p2_order = None
                    waiting_for_shuffle = True
                    while waiting_for_shuffle:
                        msg_shuf = net_mgr.get_message()
                        while msg_shuf is not None:
                            if msg_shuf["type"] == "shuffle":
                                p1_order = msg_shuf["p1_order"]
                                p2_order = msg_shuf["p2_order"]
                                waiting_for_shuffle = False
                                break
                            elif msg_shuf["type"] == "disconnected":
                                afficher_message_final("Adversaire deconnecte")
                                net_mgr.disconnect()
                                return
                            msg_shuf = net_mgr.get_message()
                        if waiting_for_shuffle:
                            pygame.time.delay(5)
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    net_mgr.disconnect()
                                    pygame.quit()
                                    exit()

                if net_mgr.is_host:
                    local_order = p1_order
                    remote_order = p2_order
                else:
                    local_order = p2_order
                    remote_order = p1_order

                animer_melange_cartes(screen, scaled_image_de_fond, cartes_locales, cartes_distantes, local_order, remote_order, card_back_img)

                cartes_p1[:] = [cartes_p1[idx] for idx in p1_order]
                cartes_p2[:] = [cartes_p2[idx] for idx in p2_order]

        # 4. Rendu du Plateau
        screen.blit(scaled_image_de_fond, (0, 0))

        # Particules ambiantes
        play_particles.emit_ambient(screen.get_width(), screen.get_height(), color=(255, 160, 50), count=1)
        play_particles.update()
        play_particles.draw(screen)

        font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 15)

        # Dessin des cartes adverses (en haut)
        for i, carte in enumerate(cartes_distantes):
            position_x = 50 + i * (100 + 20)
            
            glow_border = None
            if active_spell_id is not None:
                if active_spell_id == 7:
                    g_val = int(127 + 128 * math.sin(pygame.time.get_ticks() / 150.0))
                    glow_border = (g_val, 0, g_val)
                    
            image_redim = carte.Resize_Card(card_back_img, 100, 150)
            card_rect = pygame.Rect(position_x, 50, 100, 150)
            screen.blit(image_redim, card_rect.topleft)

            # Dessin de l'aura
            if glow_border:
                pygame.draw.rect(screen, glow_border, (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)
            elif getattr(carte, 'has_shield', False):
                pygame.draw.rect(screen, (0, 220, 255), (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)
            elif getattr(carte, 'has_seal', False):
                pygame.draw.rect(screen, (150, 0, 255), (position_x - 3, 50 - 3, 106, 156), 3, border_radius=6)

            if remote_choice_idx == i:
                pygame.draw.rect(screen, (255, 128, 0), card_rect, 4, border_radius=5)
                lbl_sel = font_small.render("PRET", True, (255, 128, 0))
                screen.blit(lbl_sel, (position_x + 20, 50 + 60))

            vie_text = font_small.render('HP: ???', True, (0, 255, 0))
            attaque_text = font_small.render('ATK: ???', True, (255, 0, 0))
            screen.blit(vie_text, (position_x, 50 + 155))
            screen.blit(attaque_text, (position_x, 50 + 175))

        # Dessin de nos cartes (en bas)
        for i, carte in enumerate(cartes_locales):
            position_x = 50 + i * (100 + 20)
            is_hovered = position_x <= mouse_pos[0] <= position_x + 100 and screen.get_height() - 200 <= mouse_pos[1] <= screen.get_height() - 50
            offset_y = -15 if is_hovered else 0
            
            if is_hovered:
                play_particles.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 215, 0), count=1)

            glow_border = None
            if active_spell_id is not None:
                if active_spell_id in [1, 2, 3, 4, 5]:
                    g_val = int(127 + 128 * math.sin(pygame.time.get_ticks() / 150.0))
                    glow_border = (0, g_val, 0)

            image_redim = carte.Resize_Card(carte.Name, 100, 150)
            card_rect = pygame.Rect(position_x, screen.get_height() - 200 + offset_y, 100, 150)
            screen.blit(image_redim, card_rect.topleft)

            if glow_border:
                pygame.draw.rect(screen, glow_border, (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)
            elif getattr(carte, 'has_shield', False):
                pygame.draw.rect(screen, (0, 220, 255), (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)
            elif getattr(carte, 'has_seal', False):
                pygame.draw.rect(screen, (150, 0, 255), (position_x - 3, screen.get_height() - 200 + offset_y - 3, 106, 156), 3, border_radius=6)

            if local_choice_idx == i:
                pygame.draw.rect(screen, (0, 255, 0), card_rect, 4, border_radius=5)
                lbl_sel = font_small.render("CHOISI", True, (0, 255, 0))
                screen.blit(lbl_sel, (position_x + 10, screen.get_height() - 120 + offset_y))

            attaque_text = font_small.render(f'ATK: {carte.AttackPoint}', True, (255, 0, 0))
            vie_text = font_small.render(f'HP: {carte.LifePoint}', True, (0, 255, 0))
            screen.blit(attaque_text, (position_x, screen.get_height() - 200 + offset_y + 155))
            screen.blit(vie_text, (position_x, screen.get_height() - 200 + offset_y + 175))

        # 3. Rendu du Plateau de Cartes Spéciales
        tray_x = screen.get_width() - 380
        tray_y = screen.get_height() - 230
        tray_w = 340
        tray_h = 160
        
        tray_surf = pygame.Surface((tray_w, tray_h), pygame.SRCALPHA)
        tray_surf.fill((25, 15, 35, 190))
        screen.blit(tray_surf, (tray_x, tray_y))
        pygame.draw.rect(screen, (0, 255, 255), (tray_x, tray_y, tray_w, tray_h), 2, border_radius=10)
        
        font_tray = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 12)
        lbl_tray = font_tray.render(L("special_cards_tray"), True, (255, 215, 0))
        screen.blit(lbl_tray, (tray_x + 15, tray_y + 10))
        
        for idx_sp, spell_id in enumerate(local_specials):
            sp_x = tray_x + 15 + idx_sp * 160
            sp_y = tray_y + 35
            sp_w, sp_h = 150, 110
            
            is_hovered = sp_x <= mouse_pos[0] <= sp_x + sp_w and sp_y <= mouse_pos[1] <= sp_y + sp_h
            is_active = (active_spell_id == spell_id)
            
            card_color = (35, 20, 50, 220)
            border_color = (100, 80, 120)
            
            if is_active:
                border_color = (0, 255, 100)
                card_color = (15, 55, 25, 240)
            elif is_hovered:
                border_color = (255, 215, 0)
                card_color = (55, 30, 80, 235)
                if random.random() < 0.15:
                    play_particles.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 215, 0), count=1)
                    
            slot_surf = pygame.Surface((sp_w, sp_h), pygame.SRCALPHA)
            slot_surf.fill(card_color)
            screen.blit(slot_surf, (sp_x, sp_y))
            pygame.draw.rect(screen, border_color, (sp_x, sp_y, sp_w, sp_h), 2 if (is_hovered or is_active) else 1, border_radius=8)
            
            sp_name = L(f"special_{spell_id}_name")
            sp_name_surf = font_tray.render(sp_name, True, (255, 255, 255))
            screen.blit(sp_name_surf, sp_name_surf.get_rect(center=(sp_x + sp_w // 2, sp_y + 25)))
            
            sp_desc = L(f"special_{spell_id}_desc")
            font_desc = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 9)
            if len(sp_desc) > 20:
                split_idx = sp_desc.rfind(" ", 0, 18)
                if split_idx == -1: split_idx = 18
                desc_p1 = font_desc.render(sp_desc[:split_idx], True, (200, 200, 200))
                desc_p2 = font_desc.render(sp_desc[split_idx:], True, (160, 160, 160))
                screen.blit(desc_p1, desc_p1.get_rect(center=(sp_x + sp_w // 2, sp_y + 60)))
                screen.blit(desc_p2, desc_p2.get_rect(center=(sp_x + sp_w // 2, sp_y + 80)))
            else:
                desc_surf = font_desc.render(sp_desc, True, (200, 200, 200))
                screen.blit(desc_surf, desc_surf.get_rect(center=(sp_x + sp_w // 2, sp_y + 70)))

        # 3.5. Rendu du bouton Éveil et du timer (Multijoueur)
        eveil_btn_rect = None
        if eveil_disponible and ((len(cartes_locales) <= 3 and len(cartes_locales) < len(cartes_distantes)) or len(cartes_locales) == 1):
            font_eveil = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
            eveil_btn_rect = draw_eveil_button(screen, screen_width - 550, screen_height - 180, 150, 50, font_eveil)
            
        if eveil_actif:
            font_timer = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
            lbl_timer = font_timer.render(L("eveil_remaining").format(eveil_tours_restants), True, (255, 140, 0))
            t_val = pygame.time.get_ticks()
            alpha_timer = int(180 + 75 * math.sin(t_val / 120.0))
            lbl_timer.set_alpha(alpha_timer)
            screen.blit(lbl_timer, lbl_timer.get_rect(center=(screen_width - 475, screen_height - 150)))
            if random.random() < 0.15:
                play_particles.emit_sparkle(screen_width - 475 + random.randint(-40, 40), screen_height - 150 + random.randint(-8, 8), color=(255, 100, 0), count=1)
                
        if opponent_eveil_actif:
            font_timer = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
            lbl_timer_opp = font_timer.render("Adversaire " + L("eveil_remaining").format(opponent_eveil_tours_restants), True, (255, 69, 0))
            t_val = pygame.time.get_ticks()
            alpha_timer = int(180 + 75 * math.sin(t_val / 120.0))
            lbl_timer_opp.set_alpha(alpha_timer)
            screen.blit(lbl_timer_opp, lbl_timer_opp.get_rect(center=(screen_width - 475, 190)))
            if random.random() < 0.15:
                play_particles.emit_sparkle(screen_width - 475 + random.randint(-40, 40), 190 + random.randint(-8, 8), color=(255, 50, 0), count=1)

        # 4. Dessin des textes flottants
        for ft in list(floating_texts):
            ft["timer"] -= 1
            ft["y"] -= 1.8
            alpha = int(255 * (ft["timer"] / 45.0))
            ft_font = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 13)
            txt_surf = ft_font.render(ft["text"], True, ft["color"])
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (ft["x"] - txt_surf.get_width() // 2, ft["y"]))
            if ft["timer"] <= 0:
                floating_texts.remove(ft)

        # 5. Dessin du bandeau d'alerte des sorts de l'adversaire
        if bot_active_spell_banner and bot_banner_timer > 0:
            bot_banner_timer -= 1
            alpha_banner = int(min(255, 255 * (bot_banner_timer / 15.0)))
            
            banner_w = 600
            banner_h = 50
            banner_x = screen.get_width() // 2 - banner_w // 2
            banner_y = 230
            
            banner_surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
            banner_surf.fill((30, 10, 20, int(200 * (alpha_banner / 255.0))))
            screen.blit(banner_surf, (banner_x, banner_y))
            pygame.draw.rect(screen, (255, 50, 100, alpha_banner), (banner_x, banner_y, banner_w, banner_h), 2, border_radius=6)
            
            font_banner = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 16)
            text_b = font_banner.render(bot_active_spell_banner, True, (255, 220, 100))
            text_b.set_alpha(alpha_banner)
            screen.blit(text_b, text_b.get_rect(center=(screen.get_width() // 2, banner_y + banner_h // 2)))
            
            if bot_banner_timer <= 0:
                bot_active_spell_banner = None

        # Instructions / Attente au centre
        font_msg = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 20)
        if active_spell_id is not None:
            lbl_prompt = font_instruction.render(L("special_target_prompt"), True, (255, 215, 0))
            screen.blit(lbl_prompt, lbl_prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 280)))
        elif local_choice_idx is not None and remote_choice_idx is None:
            draw_fading_text("En attente du choix de l'adversaire...", (255, 255, 0), screen, screen_width // 2, screen_height // 2, font_msg)
        elif local_choice_idx is None:
            draw_blinking_text("Choisissez votre carte pour attaquer", (255, 255, 255), screen, screen_width // 2, screen_height // 2, font_msg)

        # Dessiner le bouton Quitter
        draw_button(screen, "Quitter", screen_width - 100, 50, 10, (120, 20, 20), (180, 30, 30), font_instruction, None)

        pygame.display.update()
        pygame.time.delay(30)

