# Coding Utf-8

import pygame
import time
from Customize_home_screen import *
from Confrontation import *
from NetworkManager import NetworkManager, InternetNetworkManager

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


def SelectCharacters(mode='single', net_mgr=None):
    # Initialisation et configuration de la fenêtre
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Fairy Card")
    

    # Charger l'image de fond
    background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
    scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Configuration de la musique de fond
    pygame.mixer.init()
    pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
    pygame.mixer.music.play(loops=-1)
    SOUNDS.update_music_volume()

    # Liste des cartes équilibrées (65 personnages, 5 archétypes stratégiques)
    card_data = [
        # --- BOSS SUPRÊMES / CLASSE S (HP très élevés, ATK très élevée - Puissants mais à double tranchant si capturés)
        ("Acnologia", 3000, 500),    # Boss Suprême
        ("Zeleph", 2850, 480),       # Mage Noir Éternel
        ("Ignir", 2950, 495),        # Roi des Dragons de Feu
        ("Gildart", 2900, 490),      # Mage Suprême de Fairy Tail
        ("August", 2800, 450),       # Roi de la Magie (S-Class)
        ("Eileen", 2700, 440),       # Reine des Dragons (S-Class)
        ("MardGheer", 2700, 430),    # Roi des Démons de Tartaros
        ("Zeros", 2750, 460),        # Mage Sombre d'Élite
        ("Larcade", 2600, 410),      # Mage Blanc du Zodiaque
        ("Weisslogia", 2800, 380),   # Dragon de Lumière

        # --- TANKS / PROTECTEURS (HP massifs, ATK faible - Absorbent les dégâts, sans danger si capturés par l'adversaire)
        ("Makarof", 2700, 220),      # Maître de Guilde / Tank Suprême
        ("Jura", 2600, 200),         # Tank Sacré de la Terre
        ("Metalicana", 2800, 210),   # Dragon de Fer
        ("Elfman", 2400, 220),       # Force Brute (Beast Take Over)
        ("Grandinet", 2500, 200),    # Dragon Céleste protecteur
        ("Azuma", 2450, 210),        # Gardien de l'Arbre de l'Île Tenrô
        ("Freed", 2350, 220),        # Mage des Runes / Barrière
        ("Bicksrow", 2300, 230),     # Marionnettiste de Runes
        ("Jose", 2400, 215),         # Ancien Maître de Guilde de Phantom Lord

        # --- GLASS CANNONS / ASSASSINS (HP très bas, ATK dévastatrice - Menace absolue mais très facile à éliminer/capturer)
        ("Ikaruga", 1200, 490),      # Assassin suprême au sabre
        ("Jackal", 1250, 480),       # Démon Explosif de Tartaros
        ("Seila", 1280, 470),        # Démon au pouvoir Macro
        ("Kyoka", 1320, 465),        # Reine de la Douleur de Tartaros
        ("Midnight", 1300, 460),     # Mage de la Réfraction Céleste
        ("Cobra", 1350, 450),        # Dragon Slayer du Poison
        ("Tempester", 1300, 450),    # Fléau Élémentaire de Tartaros
        ("Keith", 1300, 440),        # Nécromancien de Tartaros
        ("Bora", 1150, 430),         # Magicien du Feu Rose
        ("Ezer", 1380, 440),         # Démon aux Sabres Tranchants

        # --- COMBATTANTS ÉQUILIBRÉS (Stats solides - Le noyau de base indispensable à toute stratégie)
        ("Natsu", 2000, 380),        # Dragon Slayer du Feu - DPS Explosif
        ("Luxus", 2050, 390),        # Dragon Slayer de la Foudre - Brutal
        ("Erza", 2100, 370),         # Reine des Fées - Polyvalente & Solide
        ("Jellal", 1980, 375),       # Mage Céleste de premier plan
        ("Grey", 1950, 360),         # Mage de Glace - Équilibre Parfait
        ("Mirajane", 1900, 365),     # Satan Soul - Puissante & Équilibrée
        ("Gajil", 2050, 350),        # Dragon Slayer de Fer - Tanky DPS
        ("Silver", 2000, 360),       # Chasseur de Démons de Glace
        ("Sting", 1900, 350),        # Dragon Slayer Blanc
        ("Rogue", 1900, 350),        # Dragon Slayer de l'Ombre
        ("Oul", 1950, 340),          # Maître des Mages de Glace
        ("Leon", 1850, 330),         # Créateur de Glace Animée
        ("Kagura", 1900, 360),       # Épéiste de la Gravité
        ("Minerva", 1950, 370),      # Manipulation de l'Espace-Temps
        ("Backus", 1800, 340),       # Combattant de l'Ivresse
        ("Orga", 1850, 350),         # Chasseur de Dieux de Foudre
        ("Blunote", 2100, 390),      # Mage de Gravité (Classe S)
        ("Di_maria", 1800, 360),     # Guerrière du Temps (Chronos)
        ("Hades", 2650, 420),        # Maître du Grimoire Heart

        # --- SUPPORTS / TACTICIENS (HP modérés, ATK basse - Utilitaires stratégiques, idéaux pour les buffs)
        ("Lucy", 1650, 210),         # Constellationniste aux esprits variés
        ("Mavis", 1700, 220),        # Stratège suprême / Première Maîtresse
        ("Wendy", 1600, 180),        # Dragon Slayer Céleste - Soins
        ("Cherrya", 1550, 190),      # Chasseuse de Dieux Célestes
        ("Leo", 1700, 250),          # Esprit du Lion (Loki)
        ("Kanna", 1650, 240),        # Mage des Cartes de Support
        ("Aria", 1500, 230),         # Magicien du Vent Élémentaire
        ("Mest", 1600, 220),         # Téléportation & Infiltration
        ("Melty", 1550, 200),        # Magie du Lien Sensoriel
        ("Yukino", 1500, 200),       # Constellationniste de rechange
        ("Eligoal", 1600, 260),      # Vent Noir
        ("Reby", 1450, 170),         # Écriture Magique Utilitaire (Reby)
        ("Jenny", 1500, 180),        # Support de Lumière
        ("Ichiya", 1400, 160),       # Parfums Magiques Utilitaires
        ("Juvia", 1750, 250)         # Elémentaire de l'Eau
    ]

    cards = []
    selected_cards = []  # Liste pour stocker les cartes sélectionnées
    scroll_x = 0  # Position du défilement horizontal
    scroll_speed = -2  # Vitesse de défilement automatique (négatif pour aller vers la gauche)
    card_width = 150  # Largeur d'une carte

    # Charger les cartes
    for name, life, attack in card_data:
        card_path = normalize_path("Image", f"{name}.jpg")
        card = Card(life, attack, card_path, name)
        cards.append(card)
    hovered_card = None  # Variable pour garder la carte agrandie
    last_hovered_in_carousel = None  # Evite de spammer le son
    particle_mgr = ParticleManager()
    font_title = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 70)
    font_small = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 20)
    font_instruction = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 30)  # Taille plus réduite
    font_average = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 25)

    selected_rects = []
    left_arrow_rect = pygame.Rect(15, 640, 50, 60)
    right_arrow_rect = pygame.Rect(screen_width - 65, 640, 50, 60)

    # Fonction pour afficher du texte avec effet d'apparition
    def display_text_for_duration(surface, text, color, duration=3, font=font_title):
        start_time = time.time()
        fade_alpha = 0
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            if elapsed_time < duration / 2:
                fade_alpha = min(255, int(255 * elapsed_time / (duration / 2)))
            else:
                fade_alpha = max(0, int(255 * (1 - (elapsed_time - duration / 2) / (duration / 2))))
            text_surf.set_alpha(fade_alpha)
            surface.blit(scaled_background_image, (0, 0))
            surface.blit(text_surf, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()
            pygame.time.delay(16)

    # Fonction pour dessiner les cartes à l'écran
    def blit_cards_on_screen():
        screen.fill((0, 0, 0))
        screen.blit(scaled_background_image, (0, 0))
        
        # Filtre sombre pour faire ressortir les éléments de sélection
        overlay_bg = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay_bg.fill((10, 10, 15, 130))
        screen.blit(overlay_bg, (0, 0))

        card_list = []
        total_card_width = card_width * len(cards)  # Largeur totale de toutes les cartes
        offset = scroll_x % total_card_width  # Calcul de l'offset de défilement

        mouse_pos = pygame.mouse.get_pos()
        hovered_in_carousel = None
        hovered_x = 0

        # Premier passage pour identifier la carte survolée dans le carrousel
        for i, card in enumerate(cards * 2):
            card_x = i * card_width - offset
            if card_x > screen_width or card_x + card_width < 0:
                continue
            
            rect = pygame.Rect(card_x, 570, card_width, 200)
            if rect.collidepoint(mouse_pos):
                hovered_in_carousel = card
                hovered_x = card_x
                break

        # Gestion intelligente du son au survol pour éviter la saturation
        nonlocal last_hovered_in_carousel
        if hovered_in_carousel != last_hovered_in_carousel:
            if hovered_in_carousel is not None:
                SOUNDS.play("ui_hover")
            last_hovered_in_carousel = hovered_in_carousel

        # Deuxième passage pour dessiner toutes les cartes sauf celle survolée
        for i, card in enumerate(cards * 2):
            card_x = i * card_width - offset
            if card_x > screen_width or card_x + card_width < 0:
                continue

            if card == hovered_in_carousel and card_x == hovered_x:
                continue

            resized_card = card.Resize_Card(card.Name, card_width, 200)
            card_rect = card.Blit_Card(screen, resized_card, card_x, 570)

            # Si sélectionnée, dessiner un effet
            if card in selected_cards:
                sel_overlay = pygame.Surface((card_width, 200), pygame.SRCALPHA)
                sel_overlay.fill((0, 255, 0, 50))
                screen.blit(sel_overlay, (card_x, 570))
                pygame.draw.rect(screen, (0, 255, 0), (card_x, 570, card_width, 200), 2, border_radius=5)
                draw_text(L("chosen"), (255, 255, 255), screen, card_rect.centerx, card_rect.centery, font_small)

            card_list.append((card, card_rect))

        # Troisième passage : dessiner la carte survolée par-dessus les autres
        if hovered_in_carousel is not None:
            zoom_w = int(card_width * 1.15)
            zoom_h = int(200 * 1.15)
            x_pos = hovered_x - (zoom_w - card_width) // 2
            y_pos = 570 - 25
            
            resized_card = hovered_in_carousel.Resize_Card(hovered_in_carousel.Name, zoom_w, zoom_h)
            card_rect = hovered_in_carousel.Blit_Card(screen, resized_card, x_pos, y_pos)

            # Dessiner une lueur dorée
            pygame.draw.rect(screen, (255, 215, 0), (x_pos, y_pos, zoom_w, zoom_h), 4, border_radius=8)

            if hovered_in_carousel in selected_cards:
                sel_overlay = pygame.Surface((zoom_w, zoom_h), pygame.SRCALPHA)
                sel_overlay.fill((0, 255, 0, 60))
                screen.blit(sel_overlay, (x_pos, y_pos))
                pygame.draw.rect(screen, (0, 255, 0), (x_pos, y_pos, zoom_w, zoom_h), 3, border_radius=8)
                draw_text(L("chosen"), (255, 255, 255), screen, card_rect.centerx, card_rect.centery, font_small)

            card_list.append((hovered_in_carousel, card_rect))

        return card_list

    # Fonction pour gérer le survol des cartes
    def handle_card_hover_and_select(card_list):
        nonlocal hovered_card
        mouse_pos = pygame.mouse.get_pos()
        hovered_card = None

        for card, rect in card_list:
            if rect.collidepoint(mouse_pos):
                hovered_card = card
                # Petit effet d'étincelles lors du survol
                particle_mgr.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 215, 0), count=1)
                break
        return selected_cards

    # Fonction pour dessiner le texte (Points de vie et d'attaque)
    def draw_text(text, color, surface, x, y, font):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

    # Fonction pour créer et afficher un bouton stylé
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
            SOUNDS.play("ui_click")
            if action:
                action()

    # Fonction pour dessiner les flèches de navigation
    def draw_navigation_arrows():
        mouse_pos = pygame.mouse.get_pos()
        
        # Flèche gauche
        left_hover = left_arrow_rect.collidepoint(mouse_pos)
        left_color = (0, 255, 255, 200) if left_hover else (0, 255, 255, 100)
        
        # Flèche droite
        right_hover = right_arrow_rect.collidepoint(mouse_pos)
        right_color = (0, 255, 255, 200) if right_hover else (0, 255, 255, 100)
        
        # Rendu flèche gauche
        l_surf = pygame.Surface((left_arrow_rect.width, left_arrow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(l_surf, (20, 20, 35, 180), (0, 0, left_arrow_rect.width, left_arrow_rect.height), border_radius=10)
        pygame.draw.rect(l_surf, left_color, (0, 0, left_arrow_rect.width, left_arrow_rect.height), 2, border_radius=10)
        screen.blit(l_surf, left_arrow_rect.topleft)
        
        font_arrow = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 30)
        lbl_l = font_arrow.render("<", True, (255, 255, 255) if left_hover else (0, 255, 255))
        screen.blit(lbl_l, lbl_l.get_rect(center=left_arrow_rect.center))
        
        # Rendu flèche droite
        r_surf = pygame.Surface((right_arrow_rect.width, right_arrow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(r_surf, (20, 20, 35, 180), (0, 0, right_arrow_rect.width, right_arrow_rect.height), border_radius=10)
        pygame.draw.rect(r_surf, right_color, (0, 0, right_arrow_rect.width, right_arrow_rect.height), 2, border_radius=10)
        screen.blit(r_surf, right_arrow_rect.topleft)
        
        lbl_r = font_arrow.render(">", True, (255, 255, 255) if right_hover else (0, 255, 255))
        screen.blit(lbl_r, lbl_r.get_rect(center=right_arrow_rect.center))

    # Fonction pour dessiner la fiche technique de droite
    def draw_details_panel():
        panel_x = screen_width - 540
        panel_y = 60
        panel_w = 520
        panel_h = 480
        
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((25, 20, 30, 200)) # Transparent violet
        screen.blit(panel_surf, (panel_x, panel_y))
        
        pygame.draw.rect(screen, (255, 165, 0), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=15)
        
        draw_text(L("tech_sheet"), (255, 215, 0), screen, panel_x + panel_w // 2, panel_y + 30, font_average)
        
        if hovered_card is not None:
            # Carte agrandie
            resized = hovered_card.Resize_Card(hovered_card.Name, 200, 300)
            screen.blit(resized, (panel_x + 160, panel_y + 65))
            
            # Nom
            draw_text(hovered_card.card_name.upper(), (255, 255, 255), screen, panel_x + panel_w // 2, panel_y + 380, font_small)
            
            # HP et ATK en barres
            hp_ratio = min(1.0, hovered_card.LifePoint / 3000.0)
            bar_w = 440
            bar_h = 16
            bar_x = panel_x + 40
            
            # HP
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, panel_y + 405, bar_w, bar_h), border_radius=8)
            pygame.draw.rect(screen, (0, 255, 100), (bar_x, panel_y + 405, int(bar_w * hp_ratio), bar_h), border_radius=8)
            font_stat = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
            lbl_hp = font_stat.render(f"HP: {hovered_card.LifePoint} / 3000", True, (255, 255, 255))
            screen.blit(lbl_hp, (bar_x + 15, panel_y + 405 + 1))
            
            # ATK
            atk_ratio = min(1.0, hovered_card.AttackPoint / 500.0)
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, panel_y + 435, bar_w, bar_h), border_radius=8)
            pygame.draw.rect(screen, (255, 50, 50), (bar_x, panel_y + 435, int(bar_w * atk_ratio), bar_h), border_radius=8)
            lbl_atk = font_stat.render(f"ATK: {hovered_card.AttackPoint} / 500", True, (255, 255, 255))
            screen.blit(lbl_atk, (bar_x + 15, panel_y + 435 + 1))
        else:
            # Message par défaut clignotant
            draw_blinking_text(L("hover_char"), (255, 255, 0), screen, panel_x + panel_w // 2, panel_y + panel_h // 2 - 20, font_small, blink_speed=400)
            draw_fading_text(L("discover_stats"), (255, 255, 255), screen, panel_x + panel_w // 2, panel_y + panel_h // 2 + 10, font_small, duration=1000)

    # Fonction pour dessiner le cadre des cartes sélectionnées
    def draw_selected_cards_frame():
        nonlocal selected_rects
        selected_rects = []
        
        panel_x = 20
        panel_y = 60
        panel_w = 520
        panel_h = 480
        
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((15, 20, 25, 200))
        screen.blit(panel_surf, (panel_x, panel_y))
        
        pygame.draw.rect(screen, (0, 255, 255), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=15)
        
        max_cards = 5 if mode == 'multi' else 10
        count = len(selected_cards)
        
        # Titre et jauge de progression
        draw_text(f"{L('recruits')} : {count} / {max_cards}", (0, 255, 255), screen, panel_x + panel_w // 2, panel_y + 30, font_average)
        
        bar_w = 440
        bar_h = 10
        bar_x = panel_x + 40
        pygame.draw.rect(screen, (40, 45, 55), (bar_x, panel_y + 55, bar_w, bar_h), border_radius=5)
        
        pct = count / max_cards
        pygame.draw.rect(screen, (0, 255, 255), (bar_x, panel_y + 55, int(bar_w * pct), bar_h), border_radius=5)
        
        # Grid layout
        for slot in range(max_cards):
            col = slot % 5
            row = slot // 5
            
            card_x = panel_x + 35 + col * 92
            card_y = panel_y + 90 + row * 180
            
            if slot < len(selected_cards):
                card = selected_cards[slot]
                resized_card = card.Resize_Card(card.Name, 80, 120)
                card_rect = card.Blit_Card(screen, resized_card, card_x, card_y)
                
                pygame.draw.rect(screen, (0, 255, 0), (card_x, card_y, 80, 120), 2, border_radius=5)
                selected_rects.append((card, pygame.Rect(card_x, card_y, 80, 120)))
                
                # Nom en bas
                font_name = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 9)
                lbl_name = font_name.render(card.card_name[:11], True, (255, 255, 255))
                screen.blit(lbl_name, lbl_name.get_rect(center=(card_x + 40, card_y + 135)))
            else:
                # Hologramme slot vide
                pygame.draw.rect(screen, (0, 255, 255, 80), (card_x, card_y, 80, 120), 1, border_radius=5)
                
                font_plus = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 20)
                lbl_plus = font_plus.render("+", True, (0, 255, 255, 80))
                screen.blit(lbl_plus, lbl_plus.get_rect(center=(card_x + 40, card_y + 60)))
    

    # Fonction pour fermer le jeu
    def quit_game():
        pygame.quit()
        quit()


    # Boucle de jeu
    def main_loop():
        nonlocal scroll_x, scroll_speed
        running = True
        target_scroll_x = 0

        # Affichage successif des deux textes avec effet d'apparition
        display_text_for_duration(screen, L("selection_title"), (255, 215, 0), duration=3, font=font_title)
        display_text_for_duration(screen, L("selection_inst"), (255, 255, 255), duration=3, font=font_instruction)

        while running:
            # Gestion du défilement
            target_scroll_x += scroll_speed
            scroll_x += (target_scroll_x - scroll_x) * 0.12

            card_list = blit_cards_on_screen()
            selected_cards = handle_card_hover_and_select(card_list)

            # Dessiner les éléments de l'UI
            draw_selected_cards_frame()
            draw_details_panel()
            draw_navigation_arrows()

            # Particules ambiantes
            particle_mgr.emit_ambient(screen_width, screen_height, color=(255, 180, 50), count=1)
            particle_mgr.update()
            particle_mgr.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        scroll_speed = 8  # Défile vers la droite
                    elif event.key == pygame.K_RIGHT:
                        scroll_speed = -8  # Défile vers la gauche
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        scroll_speed = -2  # Défilement auto
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic gauche
                        mouse_pos = event.pos
                        
                        # Clic sur Flèche gauche
                        if left_arrow_rect.collidepoint(mouse_pos):
                            target_scroll_x += 350
                            SOUNDS.play("ui_click")
                            particle_mgr.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(0, 255, 255), count=15)
                        
                        # Clic sur Flèche droite
                        elif right_arrow_rect.collidepoint(mouse_pos):
                            target_scroll_x -= 350
                            SOUNDS.play("ui_click")
                            particle_mgr.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(0, 255, 255), count=15)
                            
                        else:
                            # Clic sur les cartes sélectionnées pour désélection
                            clicked_deselect = False
                            for card, rect in selected_rects:
                                if rect.collidepoint(mouse_pos):
                                    selected_cards.remove(card)
                                    SOUNDS.play("ui_click")
                                    particle_mgr.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(255, 50, 0), count=20)
                                    clicked_deselect = True
                                    break
                            
                            # Clic sur les cartes du carrousel pour ajouter
                            if not clicked_deselect:
                                for card, rect in card_list:
                                    if rect.collidepoint(mouse_pos):
                                        max_cards = 5 if mode == 'multi' else 10
                                        if len(selected_cards) < max_cards:
                                            if card not in selected_cards:
                                                selected_cards.append(card)
                                                SOUNDS.play("card_select")
                                                particle_mgr.emit_sparkle(mouse_pos[0], mouse_pos[1], color=(0, 255, 100), count=25)
                                        break

            # Vérifie si le joueur a sélectionné le bon nombre de cartes
            max_cards = 5 if mode == 'multi' else 10
            if len(selected_cards) == max_cards:
                 if mode == 'single':
                      gerer_affrontement(screen, selected_cards)
                      return
                 else:
                      # Étape 1 : Envoyer notre deck sélectionné
                      deck_msg = {"type": "selection", "cards": [c.card_name for c in selected_cards]}
                      net_mgr.send(deck_msg)
                      
                      # Étape 2 : Boucle d'attente du choix de l'adversaire
                      waiting_for_opponent = True
                      opponent_cards_names = []
                      font_msg = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 20)
                      
                      while waiting_for_opponent:
                          msg = net_mgr.get_message()
                          while msg is not None:
                              if msg["type"] == "selection":
                                  opponent_cards_names = msg["cards"]
                                  waiting_for_opponent = False
                              elif msg["type"] == "disconnected":
                                  waiting_for_opponent = False
                                  net_mgr.disconnect()
                                  return
                              msg = net_mgr.get_message()
                              
                          for event in pygame.event.get():
                              if event.type == pygame.QUIT:
                                  net_mgr.disconnect()
                                  pygame.quit()
                                  exit()
                              elif event.type == pygame.MOUSEBUTTONDOWN:
                                  mouse = pygame.mouse.get_pos()
                                  if screen_width - 200 <= mouse[0] <= screen_width - 10 and 50 <= mouse[1] <= 100:
                                      net_mgr.disconnect()
                                      return
                                      
                          screen.blit(scaled_background_image, (0, 0))
                          box_rect = pygame.Rect(screen_width // 2 - 300, screen_height // 2 - 80, 600, 160)
                          pygame.draw.rect(screen, (30, 30, 30, 220), box_rect, border_radius=15)
                          pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, border_radius=15)
                          
                          draw_blinking_text(L("cards_selected"), (0, 255, 0), screen, screen_width // 2, screen_height // 2 - 30, font_msg)
                          draw_fading_text(L("waiting_opp"), (255, 255, 255), screen, screen_width // 2, screen_height // 2 + 20, font_msg)
                          
                          draw_button(screen, L("cancel"), screen_width - 100, 50, 10, (100, 0, 0), (150, 0, 0), font_instruction, None)
                          
                          apply_brightness(screen, SETTINGS.get("brightness", 1.0))
                          pygame.display.flip()
                          pygame.time.delay(30)
                          
                      opponent_cards = []
                      for name in opponent_cards_names:
                          for c_name, life, attack in card_data:
                              if c_name == name:
                                  c_path = normalize_path("Image", f"{name}.jpg")
                                  opponent_cards.append(Card(life, attack, c_path, name))
                                  break
                                  
                      gerer_affrontement_reseau(screen, selected_cards, opponent_cards, net_mgr)
                      return

            # Dessiner le bouton "Quitter"
            draw_button(screen, L("quit"), screen_width - 100, 50, 10, (0, 128, 0), (0, 200, 0), font_instruction, quit_game)
           
            # Mettre à jour l'affichage
            apply_brightness(screen, SETTINGS.get("brightness", 1.0))
            pygame.display.flip()
            pygame.time.delay(30)
        
            
    main_loop()
    pygame.quit()



BTN_STATES = {}
def draw_btn_global(surface, text, x, y, width, height, color, hover_color, font, btn_id=None, particle_mgr=None):
    global BTN_STATES
    if btn_id is None:
        btn_id = text
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    is_hover = x <= mouse[0] <= x + width and y <= mouse[1] <= y + height
    
    # Gestion du son au survol (évite le spam à chaque frame)
    was_hover = BTN_STATES.get(btn_id, False)
    if is_hover and not was_hover:
        SOUNDS.play("ui_hover")
        BTN_STATES[btn_id] = True
    elif not is_hover:
        BTN_STATES[btn_id] = False
    
    # Animation d'agrandissement doux au survol
    if is_hover:
        expand = 4
        bx, by, bw, bh = x - expand, y - expand, width + expand * 2, height + expand * 2
        c = hover_color
        border_color = (255, 215, 0) # Lueur dorée au survol
        if particle_mgr and random.random() < 0.2:
            particle_mgr.emit_sparkle(mouse[0], mouse[1], color=(255, 215, 0), count=1)
    else:
        bx, by, bw, bh = x, y, width, height
        c = color
        border_color = (0, 255, 255) # Lueur cyan par défaut
        
    # Dessiner la forme du bouton avec un effet transparent (glassmorphism)
    btn_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    # S'assurer que c est bien un tuple RGB (3 valeurs) avant d'ajouter l'alpha
    rgb = c[:3] if len(c) >= 3 else c
    btn_surf.fill((*rgb, 210))
    surface.blit(btn_surf, (bx, by))
    
    # Bordure néon
    pygame.draw.rect(surface, border_color, (bx, by, bw, bh), 2, border_radius=10)
    
    # Dessiner le texte au centre
    text_surf = font.render(text, True, (255, 255, 255) if is_hover else (230, 230, 230))
    text_rect = text_surf.get_rect(center=(bx + bw // 2, by + bh // 2))
    surface.blit(text_surf, text_rect)
    
    if is_hover and click[0] == 1:
        return True
    return False


def play_screen_fade(screen, scaled_bg, duration=12, on_midpoint=None):
    clock = pygame.time.Clock()
    fade_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    # Fade Out
    for i in range(duration + 1):
        alpha = int(255 * (i / duration))
        fade_surf.fill((10, 10, 15, alpha))
        screen.blit(scaled_bg, (0, 0))
        screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        
    if on_midpoint:
        on_midpoint()
        
    # Fade In
    for i in range(duration + 1):
        alpha = int(255 * (1.0 - i / duration))
        fade_surf.fill((10, 10, 15, alpha))
        screen.blit(scaled_bg, (0, 0))
        screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def MainMenu():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Fairy Card - Menu")
    
    background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
    scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    
    pygame.mixer.init()
    pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
    pygame.mixer.music.play(loops=-1)
    SOUNDS.update_music_volume()
    
    font_title = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 70)
    font_menu = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 25)
    font_lobby = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 20)
    font_rule = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
    
    net_mgr = NetworkManager()
    menu_particles = ParticleManager()
    
    menu_state = "main"
    options_tab = "settings" # "settings", "themes", "rules"
    ip_input = "192.168.1."
    error_msg = ""
    error_timer = 0
    
    clock = pygame.time.Clock()
    running = True
    
    def change_state(new_state):
        nonlocal menu_state
        play_screen_fade(screen, scaled_background_image, duration=8)
        menu_state = new_state
        
    while running:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_state == "main":
                        running = False
                    elif menu_state in ["host_lobby", "join_input", "connecting", "options", "matchmaking"]:
                        net_mgr.disconnect()
                        change_state("main")
                elif menu_state == "join_input":
                    if event.key == pygame.K_BACKSPACE:
                        ip_input = ip_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        SOUNDS.play("ui_click")
                        net_mgr.start_client(ip_input)
                        change_state("connecting")
                        error_msg = ""
                    else:
                        if event.unicode in "0123456789.":
                            ip_input += event.unicode
                            
        # Réception réseau en arrière plan
        if menu_state == "host_lobby":
            msg = net_mgr.get_message()
            while msg is not None:
                if msg["type"] == "connected":
                    SelectCharacters(mode='multi', net_mgr=net_mgr)
                    # Recharger l'environnement après la fermeture du jeu
                    background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
                    scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                    pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
                    pygame.mixer.music.play(loops=-1)
                    SOUNDS.update_music_volume()
                    menu_state = "main"
                msg = net_mgr.get_message()
                
        elif menu_state == "connecting":
            msg = net_mgr.get_message()
            while msg is not None:
                if msg["type"] == "connected":
                    SelectCharacters(mode='multi', net_mgr=net_mgr)
                    background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
                    scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                    pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
                    pygame.mixer.music.play(loops=-1)
                    SOUNDS.update_music_volume()
                    menu_state = "main"
                elif msg["type"] == "connection_failed":
                    error_msg = L("conn_failed")
                    error_timer = pygame.time.get_ticks()
                    menu_state = "join_input"
                    net_mgr.disconnect()
                msg = net_mgr.get_message()
                
        elif menu_state == "matchmaking":
            msg = net_mgr.get_message()
            while msg is not None:
                if msg["type"] == "connected":
                    SelectCharacters(mode='multi', net_mgr=net_mgr)
                    background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
                    scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                    pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
                    pygame.mixer.music.play(loops=-1)
                    SOUNDS.update_music_volume()
                    menu_state = "main"
                elif msg["type"] == "connection_failed":
                    error_msg = L("conn_failed")
                    error_timer = pygame.time.get_ticks()
                    menu_state = "main"
                    net_mgr.disconnect()
                msg = net_mgr.get_message()
                
        # Rendu du fond
        screen.blit(scaled_background_image, (0, 0))
        
        # Effets de particules magiques (Fairy style)
        menu_particles.emit_ambient(screen_width, screen_height, color=(255, 120, 0), count=1)
        if random.random() < 0.05:
            # Petites particules bleues scintillantes de temps en temps
            menu_particles.emit_ambient(screen_width, screen_height, color=(0, 200, 255), count=1)
        menu_particles.update()
        menu_particles.draw(screen)
        
        # Affichage du titre animé
        t_ms = pygame.time.get_ticks()
        y_osc = math.sin(t_ms / 600.0) * 12
        glow_val = int(127 + 128 * math.sin(t_ms / 400.0))
        
        # Ombre portée du titre
        title_shadow = font_title.render(L("title"), True, (10, 5, 15))
        shadow_rect = title_shadow.get_rect(center=(screen_width // 2 + 5, screen_height // 4 + y_osc + 5))
        screen.blit(title_shadow, shadow_rect)
        
        # Halo néon
        title_glow = font_title.render(L("title"), True, (255, 100, 0))
        title_glow.set_alpha(glow_val // 2)
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            screen.blit(title_glow, (screen_width // 2 - title_glow.get_width() // 2 + dx, screen_height // 4 + y_osc - title_glow.get_height() // 2 + dy))
            
        # Titre principal
        title_surf = font_title.render(L("title"), True, (255, 230, 160))
        title_rect = title_surf.get_rect(center=(screen_width // 2, screen_height // 4 + y_osc))
        screen.blit(title_surf, title_rect)
        
        btn_w, btn_h = 360, 50
        btn_x = screen_width // 2 - btn_w // 2
        
        if menu_state == "main":
            # Liste des boutons avec effet glassmorphic et sonore
            if draw_btn_global(screen, L("play_ia"), btn_x, screen_height // 2 - 120, btn_w, btn_h, (15, 70, 20), (25, 120, 35), font_menu, "play_ia", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                SelectCharacters(mode='single')
                background_image = pygame.image.load(normalize_path("Image", SETTINGS.get("bg_image", "Home_screen.jpeg"))).convert_alpha()
                scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                pygame.mixer.music.load(normalize_path("Sound", "Background(1).mp3"))
                pygame.mixer.music.play(loops=-1)
                SOUNDS.update_music_volume()
                
            if draw_btn_global(screen, L("matchmaking"), btn_x, screen_height // 2 - 55, btn_w, btn_h, (90, 20, 90), (140, 30, 140), font_menu, "matchmaking", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                net_mgr = InternetNetworkManager()
                net_mgr.start_matchmaking()
                change_state("matchmaking")
                
            if draw_btn_global(screen, L("host_game"), btn_x, screen_height // 2 + 10, btn_w, btn_h, (15, 20, 80), (25, 35, 140), font_menu, "host_game", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                net_mgr = NetworkManager()
                net_mgr.start_host()
                change_state("host_lobby")
                
            if draw_btn_global(screen, L("join_game"), btn_x, screen_height // 2 + 75, btn_w, btn_h, (80, 40, 10), (130, 65, 20), font_menu, "join_game", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                net_mgr = NetworkManager()
                change_state("join_input")
                
            if draw_btn_global(screen, L("options"), btn_x, screen_height // 2 + 140, btn_w, btn_h, (90, 60, 10), (140, 95, 15), font_menu, "options", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                change_state("options")
                options_tab = "settings"
                
            if draw_btn_global(screen, L("quit"), btn_x, screen_height // 2 + 205, btn_w, btn_h, (80, 10, 10), (130, 15, 15), font_menu, "quit", menu_particles):
                SOUNDS.play("ui_click")
                pygame.time.delay(150)
                running = False
                
        elif menu_state == "options":
            # Rénovation complète de l'onglet Options avec onglets
            box_w, box_h = 920, 540
            box_x = screen_width // 2 - box_w // 2
            box_y = screen_height // 2 - 190
            
            # Box principal transparent glassmorphic
            box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            box_surf.fill((20, 15, 30, 230))
            screen.blit(box_surf, (box_x, box_y))
            pygame.draw.rect(screen, (0, 255, 255), (box_x, box_y, box_w, box_h), 2, border_radius=15)
            
            # Panneau latéral pour les onglets
            sidebar_w = 280
            sidebar_surf = pygame.Surface((sidebar_w, box_h), pygame.SRCALPHA)
            sidebar_surf.fill((10, 5, 18, 160))
            screen.blit(sidebar_surf, (box_x, box_y))
            pygame.draw.line(screen, (0, 255, 255, 120), (box_x + sidebar_w, box_y), (box_x + sidebar_w, box_y + box_h), 2)
            
            # Dessin des onglets (Tabs) — labels simples sans emojis pour éviter tout dépassement
            tabs = [
                ("settings", L('options_title')),
                ("themes",   L('bg_select')),
                ("rules",    L('rules_btn'))
            ]

            font_tab = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 13)

            for idx, (tab_id, tab_label) in enumerate(tabs):
                tx = box_x + 10
                ty = box_y + 30 + idx * 70
                # Largeur fixe pour rester parfaitement dans la sidebar
                tw = sidebar_w - 20
                th = 48

                is_active = (options_tab == tab_id)
                b_color       = (130, 90, 10) if is_active else (25, 20, 45)
                b_hover_color = (170, 120, 15) if is_active else (40, 30, 70)

                if draw_btn_global(screen, tab_label, tx, ty, tw, th, b_color, b_hover_color, font_tab, f"tab_{tab_id}", menu_particles):
                    if options_tab != tab_id:
                        SOUNDS.play("ui_click")
                        options_tab = tab_id
                        
            # Contenu des onglets (Zone de droite)
            cx = box_x + sidebar_w + 30
            cy = box_y + 30
            cw = box_w - sidebar_w - 60
            
            if options_tab == "settings":
                # --- Onglet Paramètres Audio & Vidéo ---
                # Volume Musique
                old_music = SETTINGS.get("volume_music", 0.5)
                new_music = draw_slider(screen, cx, cy + 30, cw, old_music, L("volume_music"), font_lobby)
                if new_music != old_music:
                    SETTINGS.set("volume_music", new_music)
                    SOUNDS.update_music_volume()
                    
                # Volume SFX
                old_sfx = SETTINGS.get("volume_sfx", 0.5)
                new_sfx = draw_slider(screen, cx, cy + 120, cw, old_sfx, L("volume_sfx"), font_lobby)
                if new_sfx != old_sfx:
                    SETTINGS.set("volume_sfx", new_sfx)
                    
                # Luminosité de l'écran
                old_bright = SETTINGS.get("brightness", 1.0)
                new_bright = draw_slider(screen, cx, cy + 210, cw, old_bright, L("brightness"), font_lobby)
                if new_bright != old_bright:
                    SETTINGS.set("brightness", max(0.2, new_bright))
                    
                # Choix de la langue
                old_lang = SETTINGS.get("language", "fr")
                new_lang, lang_clicked = draw_language_selector(screen, cx, cy + 320, old_lang, font_lobby)
                if lang_clicked and new_lang != old_lang:
                    SETTINGS.set("language", new_lang)
                    SOUNDS.play("ui_click")
                    
            elif options_tab == "themes":
                # --- Onglet Apparence & Thèmes ---
                old_bg = SETTINGS.get("bg_image", "Home_screen.jpeg")
                
                # Rendu du titre de section
                sect_title = font_lobby.render(L("bg_select"), True, (0, 255, 255))
                screen.blit(sect_title, (cx, cy))
                
                bg_options = ["Home_screen.jpeg", "Home_screen(1).jpeg", "Home_screen(2).jpeg"]
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                
                # Rendre des cartes miniatures interactives de prévisualisation
                thumb_w, thumb_h = 150, 220
                for idx_bg, bg_name in enumerate(bg_options):
                    bx_bg = cx + idx_bg * 175
                    by_bg = cy + 60
                    
                    is_active = (bg_name == old_bg)
                    border_c = (255, 215, 0) if is_active else (100, 100, 120)
                    
                    bg_rect = pygame.Rect(bx_bg, by_bg, thumb_w, thumb_h)
                    hovered_thumb = bg_rect.collidepoint(mouse)
                    
                    if hovered_thumb:
                        border_c = (0, 255, 255)
                        if click[0] == 1:
                            SETTINGS.set("bg_image", bg_name)
                            background_image = pygame.image.load(normalize_path("Image", bg_name)).convert_alpha()
                            scaled_background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                            SOUNDS.play("ui_click")
                            pygame.time.delay(100)
                            
                    # Fond miniature en violet sombre
                    pygame.draw.rect(screen, (30, 25, 45), bg_rect, border_radius=10)
                    # Image d'aperçu dessinée au milieu
                    try:
                        preview_img = pygame.image.load(normalize_path("Image", bg_name)).convert_alpha()
                        scaled_preview = pygame.transform.scale(preview_img, (thumb_w - 12, thumb_h - 12))
                        screen.blit(scaled_preview, (bx_bg + 6, by_bg + 6))
                    except Exception:
                        pass
                        
                    # Bordure décorative
                    pygame.draw.rect(screen, border_c, bg_rect, 3 if is_active else 1, border_radius=10)
                    
                    # Titre sous la miniature
                    txt_lbl = font_lobby.render(f"THEME {idx_bg+1}", True, (255, 255, 255) if is_active else (180, 180, 180))
                    screen.blit(txt_lbl, txt_lbl.get_rect(center=(bx_bg + thumb_w // 2, by_bg + thumb_h + 30)))
                    
            elif options_tab == "rules":
                # --- Onglet Règles du Jeu — Rendu premium avec word-wrap ---

                # Utilitaire word-wrap : découpe une chaîne en lignes tenant dans max_w pixels
                def wrap_text(text, font_obj, max_w):
                    words = text.split(" ")
                    lines = []
                    current = ""
                    for word in words:
                        test = (current + " " + word).strip()
                        if font_obj.size(test)[0] <= max_w:
                            current = test
                        else:
                            if current:
                                lines.append(current)
                            current = word
                    if current:
                        lines.append(current)
                    return lines

                font_rule_title = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 14)
                font_rule_body  = pygame.font.Font(normalize_path("Fonts", "anime-ace.regular.ttf"), 11)
                content_w = cw  # largeur disponible pour le texte
                y_r = cy

                # ── Titre principal ──
                t_surf = font_rule_title.render(L("rules_title"), True, (255, 215, 0))
                screen.blit(t_surf, (cx, y_r))
                y_r += t_surf.get_height() + 6
                pygame.draw.line(screen, (255, 215, 0), (cx, y_r), (cx + content_w, y_r), 1)
                y_r += 10

                # ── Règles de base (bullets colorés) ──
                rule_keys = [
                    ("rules_text_1", (0, 220, 255)),
                    ("rules_text_2", (255, 120, 0)),
                    ("rules_text_3", (0, 255, 120)),
                    ("rules_text_4", (180, 100, 255)),
                    ("rules_text_5", (255, 215, 0)),
                    ("rules_text_6", (255, 80, 80)),
                ]
                for r_key, r_color in rule_keys:
                    full_txt = L(r_key)
                    wrapped  = wrap_text(full_txt, font_rule_body, content_w - 18)
                    # Bullet rond coloré aligné sur la première ligne
                    pygame.draw.circle(screen, r_color, (cx + 6, y_r + 7), 4)
                    for li, line in enumerate(wrapped):
                        indent = 18 if li == 0 else 18
                        line_surf = font_rule_body.render(line, True, (240, 240, 240) if li == 0 else (200, 200, 200))
                        screen.blit(line_surf, (cx + indent, y_r + li * 14))
                    y_r += len(wrapped) * 14 + 7

                y_r += 6
                pygame.draw.line(screen, (0, 255, 255, 120), (cx, y_r), (cx + content_w, y_r), 1)
                y_r += 8

                # ── Cartes Spéciales ──
                sp_title = font_rule_title.render(L("special_cards_tray"), True, (0, 255, 255))
                screen.blit(sp_title, (cx, y_r))
                y_r += sp_title.get_height() + 6

                specials = [
                    ("special_1_name", "special_1_desc", (0, 255, 100)),
                    ("special_2_name", "special_2_desc", (0, 200, 255)),
                    ("special_3_name", "special_3_desc", (255, 100, 0)),
                    ("special_4_name", "special_4_desc", (255, 50, 120)),
                    ("special_5_name", "special_5_desc", (180, 180, 255)),
                    ("special_6_name", "special_6_desc", (255, 215, 0)),
                    ("special_7_name", "special_7_desc", (160, 0, 255)),
                ]
                # Deux colonnes côte à côte
                col_w = content_w // 2 - 8
                for i, (s_name, s_desc, s_color) in enumerate(specials):
                    col = i % 2
                    row = i // 2
                    sx = cx + col * (col_w + 12)
                    sy = y_r + row * 36
                    # Badge coloré avec le nom
                    badge_surf = pygame.Surface((col_w, 28), pygame.SRCALPHA)
                    badge_surf.fill((*s_color[:3], 50))
                    screen.blit(badge_surf, (sx, sy))
                    pygame.draw.rect(screen, s_color, (sx, sy, col_w, 28), 1, border_radius=5)
                    name_s = font_rule_body.render(L(s_name), True, s_color)
                    desc_s = font_rule_body.render(L(s_desc), True, (210, 210, 210))
                    screen.blit(name_s, (sx + 6, sy + 2))
                    screen.blit(desc_s, (sx + 6, sy + 15))
                        
            # Bouton de retour en bas
            back_btn_w = 200
            back_btn_h = 40
            if draw_btn_global(screen, L("back"), box_x + box_w - back_btn_w - 20, box_y + box_h - back_btn_h - 15, back_btn_w, back_btn_h, (90, 20, 20), (140, 30, 30), font_lobby, "back_btn", menu_particles):
                SOUNDS.play("ui_click")
                change_state("main")
                
        elif menu_state == "host_lobby":
            local_ip = net_mgr.host_ip
            box_rect = pygame.Rect(screen_width // 2 - 250, screen_height // 2 - 100, 500, 220)
            pygame.draw.rect(screen, (25, 20, 35, 220), box_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 255, 255), box_rect, 2, border_radius=15)
            
            ip_lbl = font_lobby.render(f"{L('host_ip')}", True, (255, 255, 255))
            screen.blit(ip_lbl, ip_lbl.get_rect(center=(screen_width // 2, screen_height // 2 - 50)))
            
            val_ip_lbl = font_menu.render(local_ip, True, (0, 255, 255))
            screen.blit(val_ip_lbl, val_ip_lbl.get_rect(center=(screen_width // 2, screen_height // 2 - 15)))
            
            draw_blinking_text(L("wait_player2"), (255, 215, 0), screen, screen_width // 2, screen_height // 2 + 30, font_lobby)
            
            if draw_btn_global(screen, L("back"), btn_x, screen_height // 2 + 150, btn_w, btn_h, (80, 10, 10), (130, 15, 15), font_menu, "back_host", menu_particles):
                SOUNDS.play("ui_click")
                net_mgr.disconnect()
                change_state("main")
                
        elif menu_state == "join_input":
            box_rect = pygame.Rect(screen_width // 2 - 270, screen_height // 2 - 120, 540, 250)
            pygame.draw.rect(screen, (25, 20, 35, 220), box_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 255, 255), box_rect, 2, border_radius=15)
            
            prompt_lbl = font_lobby.render(L("enter_ip"), True, (255, 255, 255))
            screen.blit(prompt_lbl, prompt_lbl.get_rect(center=(screen_width // 2, screen_height // 2 - 70)))
            
            input_rect = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 30, 400, 42)
            pygame.draw.rect(screen, (40, 35, 55), input_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 255, 255), input_rect, 2, border_radius=8)
            
            ip_val_lbl = font_lobby.render(ip_input, True, (0, 255, 0))
            screen.blit(ip_val_lbl, ip_val_lbl.get_rect(center=input_rect.center))
            
            if error_msg and pygame.time.get_ticks() - error_timer < 3000:
                err_lbl = font_lobby.render(error_msg, True, (255, 50, 50))
                screen.blit(err_lbl, err_lbl.get_rect(center=(screen_width // 2, screen_height // 2 + 40)))
                
            if draw_btn_global(screen, L("connecting"), btn_x, screen_height // 2 + 150, btn_w, btn_h, (15, 70, 20), (25, 120, 35), font_menu, "join_connect", menu_particles):
                SOUNDS.play("ui_click")
                net_mgr.start_client(ip_input)
                change_state("connecting")
                error_msg = ""
                
            if draw_btn_global(screen, L("back"), btn_x, screen_height // 2 + 215, btn_w, btn_h, (80, 10, 10), (130, 15, 15), font_menu, "join_back", menu_particles):
                SOUNDS.play("ui_click")
                change_state("main")
                
        elif menu_state == "connecting":
            box_rect = pygame.Rect(screen_width // 2 - 250, screen_height // 2 - 100, 500, 200)
            pygame.draw.rect(screen, (25, 20, 35, 220), box_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 255, 255), box_rect, 2, border_radius=15)
            
            draw_blinking_text(f"{L('connecting_to')}...", (255, 255, 255), screen, screen_width // 2, screen_height // 2 - 30, font_lobby)
            
            val_ip_lbl = font_lobby.render(ip_input, True, (0, 255, 255))
            screen.blit(val_ip_lbl, val_ip_lbl.get_rect(center=(screen_width // 2, screen_height // 2 + 10)))
            
            if draw_btn_global(screen, L("back"), btn_x, screen_height // 2 + 130, btn_w, btn_h, (80, 10, 10), (130, 15, 15), font_menu, "back_connecting", menu_particles):
                SOUNDS.play("ui_click")
                net_mgr.disconnect()
                change_state("join_input")
                
        elif menu_state == "matchmaking":
            box_rect = pygame.Rect(screen_width // 2 - 250, screen_height // 2 - 100, 500, 200)
            pygame.draw.rect(screen, (25, 20, 35, 220), box_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 255, 255), box_rect, 2, border_radius=15)
            
            # Déterminer si nous sommes déjà connectés au serveur IRC ou non
            if not net_mgr.sock:
                txt = L("connecting_irc")
            else:
                txt = L("search_match")
                
            draw_blinking_text(txt, (255, 255, 255), screen, screen_width // 2, screen_height // 2 - 20, font_lobby)
            
            if draw_btn_global(screen, L("cancel"), btn_x, screen_height // 2 + 130, btn_w, btn_h, (80, 10, 10), (130, 15, 15), font_menu, "cancel_matchmaking", menu_particles):
                SOUNDS.play("ui_click")
                net_mgr.disconnect()
                change_state("main")
                
        apply_brightness(screen, SETTINGS.get("brightness", 1.0))
        pygame.display.flip()
        
    net_mgr.disconnect()
    pygame.quit()

if __name__ == "__main__":
    MainMenu()
    

