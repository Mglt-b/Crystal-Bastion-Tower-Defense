from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line, Ellipse, Point
from kivy.clock import Clock
from random import choice

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.uix.image import Image
import os

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.app import App

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Rotate
from kivy.graphics import PushMatrix, PopMatrix

from kivy.storage.jsonstore import JsonStore
from math import atan2, degrees

class Coin(Widget):
    def __init__(self,value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        with self.canvas:
            Color(1, 0.8, 0)  # Gold color for the coin
            self.ellipse = Ellipse(pos=self.pos, size=(dp(10), dp(17)))


        self.bind(pos=self.update_graphics_pos)
        self.update_graphics_pos()

    def update_graphics_pos(self, *args):
        self.ellipse.pos = self.pos

class Monstre(Widget):
    coin_value = NumericProperty(0)
    angle = NumericProperty(0)
    def __init__(self, type_monstre, path, map_size, **kwargs):
        super().__init__(**kwargs)
        #print("Initialisation d'un nouveau monstre de type :", type_monstre)
        
        self.register_event_type('on_monster_death')
        self.is_alive = True

        # Store map size
        self.map_size = map_size
        
        # Define monster characteristics
        self.speed = type_monstre["speed"]
        self.health = type_monstre["health"]
        self.armure = type_monstre["armure"]
        self.magique_resistance = type_monstre["magique_resistance"]
        self.vie_max = self.health
        
        self.rotation_behavior = type_monstre["rotation_behavior"] #rotation type

        self.coin_value = type_monstre["coin"]

        self.path = path
        self.current_target_idx = 1

        self.largeur = type_monstre["size"][0]/2
        
        # Set initial position
        self.center = (self.path[0][0] * self.map_size[0], self.path[0][1] * self.map_size[1])
        

        self.img_directory = "monstres_images/"

        self.name = type_monstre["name"]
        
        # Monster graphics
        with self.canvas:
            # Début de la rotation
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.monster_image = Image(source=os.path.join(self.img_directory, f"monstre_{self.name}.png"), 
                                    pos=(self.center_x, self.center_y), 
                                    size=type_monstre["size"])
            self.bg = self.monster_image

            # Liez le centre de l'image à la méthode de mise à jour de l'origine de la rotation
            self.monster_image.bind(center=self.update_rotation_origin)

            # Fin de la rotation
            PopMatrix()

            # Tout ce qui doit rester fixe (comme la barre de vie) doit être défini AVANT le PushMatrix
            Color(1, 0, 0, 1)  # Rouge
            self.barre_vie_perdue = Rectangle(pos=(self.center_x, self.center_y - dp(10)), size=(self.largeur, dp(5)))

            Color(1, 1, 1, 1)  # Blanc
            # Bordure grise
            self.bordure_vie = Line(rectangle=(self.center_x, self.center_y - dp(10), self.largeur, dp(5)), width=dp(1.2))
            Color(0, 1, 0, 1)              
            # Barre de vie intérieure (verte)
            self.barre_vie = Rectangle(pos=(self.center_x, self.center_y - dp(10)), size=(self.largeur, dp(5)))

        #for ice tower
        self.freeze_effect = Image(source="effect_images/Freeze_image.png", opacity=0, size=(type_monstre["size"][0]/2,type_monstre["size"][1]/2), pos=(self.center_x,self.center_y))
        self.update_freeze_effect_position()
        self.add_widget(self.freeze_effect)
        self.slowed = False  # New property to track if the monster is slowed

        #for fire tower
        self.burn_effect = Image(source="effect_images/Burned_image.png", opacity=0, size=(type_monstre["size"][0]/2,type_monstre["size"][1]/2), pos=(self.center_x,self.center_y))
        self.update_burn_effect_position()
        self.add_widget(self.burn_effect)
        self.burned = False  # New property to track if the monster is slowed

        #for Elec tower
        self.elec_effect = Image(source="effect_images/Elected_image.png", opacity=0, size=(type_monstre["size"][0]/2,type_monstre["size"][1]/2), pos=(self.center_x,self.center_y))
        self.update_elec_effect_position()
        self.add_widget(self.elec_effect)
        self.elected = False  # New property to track if the monster is slowed

        #for Bomb tower
        self.has_bomb = False

        if self.rotation_behavior == "fixed":
            # Start moving
            self.move()
            anim = Animation(angle=360, duration=1)
            anim += Animation(angle=0, duration=0)
            anim.repeat = True
            anim.start(self)
            self.bind(angle=self.on_angle)
        elif self.rotation_behavior == "path_direction":
            # Déplacez simplement le monstre sans l'animation continue
            self.move()

    def is_out_of_screen(self):
        if self.current_target_idx >= len(self.path):
            return True
        else:
            return False

    def update_rotation_origin(self, instance, value):
        self.rotation.origin = value

    def on_angle(self, instance, value):
        self.rotation.angle = value

    def update_freeze_effect_position(self):
        # Center the freeze effect on the monster
        self.freeze_effect.center = self.center

    def apply_slow_effect(self):
        if not self.slowed:
            self.slowed = True
            self.freeze_effect.opacity = 1  # Show the freeze effect with some transparency
            original_speed = self.speed
            self.speed /= 4  # Halving the speed
            # Reset the speed after 2 seconds (or other desired duration)
            self.monster_image.opacity = .7
            Clock.schedule_once(lambda dt: self.remove_slow_effect(original_speed), 5)
            
    def remove_slow_effect(self, original_speed):
        self.slowed = False
        self.speed = original_speed
        self.freeze_effect.opacity = 0  # Hide the freeze effect
        self.monster_image.opacity = 1

    def update_elec_effect_position(self):
        # Center the freeze effect on the monster
        self.freeze_effect.center = self.center

    def apply_elec_effect(self):
        if not self.elected:
            self.elected = True
            self.elec_effect.opacity = 1  # Show the freeze effect with some transparency
            original_speed = self.speed
            self.speed = 0  # Halving the speed
            # Reset the speed after 2 seconds (or other desired duration)
            self.monster_image.opacity = .7
            Clock.schedule_once(lambda dt: self.remove_elec_effect(original_speed), 5)
            
    def remove_elec_effect(self, original_speed):
        self.elected = False
        self.speed = original_speed
        self.elec_effect.opacity = 0  # Hide the freeze effect
        self.monster_image.opacity = 1

    def update_burn_effect_position(self):
        # Center the freeze effect on the monster
        self.burn_effect.center = self.center

    def apply_burn_effect(self):
        if not self.burned:
            self.burned = True
            self.burn_effect.opacity = 1  # Show the burn effect
            
            # Schedule the damage every 2 seconds
            self.burn_event = Clock.schedule_interval(self.burn_damage, 2)
            
            # Stop the burn damage after 10 seconds
            Clock.schedule_once(self.remove_burn_effect, 15)

    def burn_damage(self, dt):
        # Inflict 5 points of damage
        self.take_damage(5, 0)  # Assuming burn is physical damage. Adjust if otherwise.

    def remove_burn_effect(self, dt=None):
        self.burned = False
        self.burn_effect.opacity = 0  # Hide the burn effect
        Clock.unschedule(self.burn_event)  # Stop the recurring damage

    def take_damage(self, damage_physique, damage_magique):
        # Calcul des dégâts réels en prenant en compte l'armure et la résistance magique
        degats_reels_physiques = damage_physique * (1 - (self.armure / (100 + self.armure)))
        degats_reels_magiques = damage_magique * (1 - (self.magique_resistance / (100 + self.magique_resistance)))
        
        # Somme des dégâts réels
        total_damage = degats_reels_physiques + degats_reels_magiques

        #print("take damage :", degats_reels_physiques, degats_reels_magiques, total_damage)
        
        self.health -= total_damage

        # Mettre à jour la taille de la barre de vie
        pct_vie = self.health / self.vie_max
        self.barre_vie.size = (self.largeur * pct_vie, dp(5))
        with self.canvas:
            Color(1, 0, 0, 1)  # Rouge
            self.barre_vie_perdue.size = (self.largeur * (1 - pct_vie), dp(5))

        # Mettre à jour la couleur de la barre de vie
        if pct_vie < 0.5:
            Color(1, 0, 0, 1)  # Rouge
        else:
            Color(0, 1, 0, 1)  # Vert

        if self.health < 1 :
            self.is_alive = False
            self.dead_monster()

    def move(self):
        root_widget = App.get_running_app().root
        map_zone = root_widget.get_screen('game').map_zone  # Accédez directement à map_zone via la référence root_widget
       
        # Calculate target position
        target = (self.path[self.current_target_idx][0] * self.map_size[0], self.path[self.current_target_idx][1] * self.map_size[1])
        dx = target[0] - self.center_x
        dy = target[1] - self.center_y
        distance = (dx**2 + dy**2)**0.5

        self.freeze_effect.pos = self.center
        self.burn_effect.pos = self.center
        self.elec_effect.pos = self.center

        # If close to the target, move to next target
        if distance < self.speed:
            self.current_target_idx += 1
            # If reached the end, remove the monster
            if self.current_target_idx >= len(self.path):
                if self.parent:

                    #si monstre au bout du path, perd vie

                    #print("perd vie")
                    map_zone.lives -= 1
                    map_zone.lives_label.text = f'Vies: {map_zone.lives}'
                    
                    map_zone.current_monsters -= 1
                    map_zone.label_current_monsters.text=f'Mobs: {map_zone.current_monsters}'
                    #print("monstre fin path, retiré, count :",map_zone.current_monsters)

                    map_zone.programmed_monster -= 1

                    #print('map_zone.lives', map_zone.lives)
                    if map_zone.lives <= 0:
                        self.game_over()  # This function needs to be implemented to handle game over logic

                    if map_zone.lives > 0 and map_zone.programmed_monster == 0 and map_zone.current_monsters == 0: 
                        self.game_win()  # This function needs to be implemented to handle game over logic              

                    self.parent.remove_widget(self)

            else:
                self.move()

            return
        
        # Update position
        move_by_x = self.speed * dx / distance
        move_by_y = self.speed * dy / distance
        self.pos = (self.pos[0] + move_by_x, self.pos[1] + move_by_y)
        
        self.center = self.x + self.width / 2, self.y + self.height / 2
        self.canvas.ask_update()
        
        # Update graphics
        #self.monster_image.pos = self.pos
        self.monster_image.pos = (self.center_x - self.monster_image.size[0]/2, self.center_y - self.monster_image.size[1]/2)

        # Update rotation
        if self.rotation_behavior == "path_direction":
            # Prendre le segment actuel et le suivant du chemin
            current_point = self.path[self.current_target_idx - 1]
            next_point = self.path[self.current_target_idx]

            # Calculer les différences en x et en y
            delta_x = next_point[0] - current_point[0]
            delta_y = next_point[1] - current_point[1]

            # Obtenir l'angle en radians
            angle_rad = atan2(delta_y, delta_x)
            
            # Convertir l'angle en degrés
            angle_deg = degrees(angle_rad) - 90  # Soustraire 90 pour que l'image orientée à gauche soit correctement orientée
            
            # Appliquer l'effet miroir si nécessaire
            if 90 <= angle_deg <= 270:  # Ajustez ces valeurs selon vos besoins
                self.monster_image.scale_x = -1
            else:
                self.monster_image.scale_x = 1

            self.rotation.angle = angle_deg

            # Mettre à jour l'origine de la rotation pour qu'elle soit centrée sur le monstre
            self.rotation.origin = self.center



        elif self.rotation_behavior == "fixed":
            pass  # Pas de rotation basée sur le chemin

        # Schedule next move
        Clock.schedule_once(lambda dt: self.move(), 0.1)

    def show_defeat_popup(self):

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Défaite'))
        close_button = Button(text='Fermer')
        content.add_widget(close_button)
        
        popup = Popup(title='Game Over', content=content, size_hint=(0.5, 0.5))

        def on_popup_dismiss(*args):
            root_widget = App.get_running_app().root
            game_screen = root_widget.get_screen('game')
            map_zone = game_screen.map_zone  # Si `map_zone` est un attribut direct de GameScreen

            game_screen.clear_widgets()

            #supprime les enfants
            for child in map_zone.children[:]:
                #print(child)
                map_zone.remove_widget(child)

            #supprime les monstres programmés
            for event in map_zone.scheduled_monster_events:
                Clock.unschedule(event)
                #print("unshedule : ", event)
            map_zone.scheduled_monster_events.clear()  # videz la liste

            #supprime le canvas
            map_zone.canvas.clear()

            # Ajoutez ces deux lignes pour revenir au menu principal
            root_widget.current = 'menu'
            root_widget.transition.direction = 'right'

            #reset popup
            app = App.get_running_app()
            app.game_over_popup_shown = False
            app.game_over_popup_win = False
            
        popup.bind(on_dismiss=on_popup_dismiss)
        
        close_button.bind(on_release=popup.dismiss)
        
        popup.open()

    def show_win_popup(self):

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Victoire'))
        close_button = Button(text='Fermer')
        content.add_widget(close_button)
        
        popup = Popup(title='Game Win', content=content, size_hint=(0.5, 0.5))

        def on_popup_dismiss(*args):
            root_widget = App.get_running_app().root
            game_screen = root_widget.get_screen('game')
            map_zone = game_screen.map_zone  # Si `map_zone` est un attribut direct de GameScreen

            game_screen.clear_widgets()

            #supprime les enfants
            for child in map_zone.children[:]:
                #print(child)
                map_zone.remove_widget(child)

            map_zone.scheduled_monster_events.clear()  # videz la liste

            #supprime le canvas
            map_zone.canvas.clear()

            # Ajoutez ces deux lignes pour revenir au menu principal
            root_widget.current = 'menu'
            root_widget.transition.direction = 'right'

            #reset popup
            app = App.get_running_app()
            app.game_over_popup_shown = False
            app.game_win_popup_shown = False

            #refresh levels :
            root_widget = App.get_running_app().root
            menu_screen = root_widget.get_screen('menu')
            menu_screen.refresh_levels()
            
        popup.bind(on_dismiss=on_popup_dismiss)
        
        close_button.bind(on_release=popup.dismiss)
        
        popup.open()

    def game_over(self):

        app = App.get_running_app()
        
        if not app.game_over_popup_shown:
            app.game_over_popup_shown = True
            self.show_defeat_popup()
            print("game over")

    def game_win(self):

        app = App.get_running_app()
        if not app.game_win_popup_shown:


            # Utilisez JsonStore pour enregistrer la progression
            progress_store = JsonStore(os.path.join('db', 'progress.json'))
            stars_store = JsonStore(os.path.join('db', 'stars.json'))

            # Supposons que vous ayez un identifiant ou un nom pour chaque niveau
            root_widget = App.get_running_app().root
            game_screen = root_widget.get_screen('game')
            map_zone = game_screen.map_zone  # Si `map_zone` est un attribut direct de GameScreen
            level_id = str(map_zone.actual_level)  # Convertir en chaîne pour utiliser comme clé; remplacez par la logique appropriée pour obtenir l'ID du niveau

            progress_store.put(level_id, completed=True)

            # Conditions fictives pour déterminer le nombre d'étoiles obtenues
            stars_earned = 1

            # Get life points = "map_zone.lives"
            if map_zone.lives >= 15:  # terminer le niveau avec >= 15 points de vie
                stars_earned += 1
            if map_zone.lives == 20:  # terminer le niveau avec 20 points de vie
                stars_earned += 1

            # Vérifiez si un record d'étoiles existe pour ce niveau
            previous_stars = 0  # Valeur par défaut
            if stars_store.exists(level_id):
                previous_stars = stars_store.get(level_id)['stars']

            # Si le nombre d'étoiles gagnées est supérieur ou égal au record précédent, mettez à jour le record
            if stars_earned >= previous_stars:
                stars_store.put(level_id, stars=stars_earned)

            first_complete_store = JsonStore(os.path.join('db', 'first_complete_level.json'))
            if not first_complete_store.exists(level_id):  
                # Ajouter 30 cristaux à l'utilisateur
                cristal_store = JsonStore(os.path.join('db', 'cristaux.json'))
                current_cristal_count = cristal_store.get('count')['value']
                cristal_store.put('count', value=current_cristal_count + 30)

                # Marquer le niveau comme complété pour la première fois
                first_complete_store.put(level_id, completed=True)

                app.game_win_popup_shown = True
                self.show_win_popup()
                print("Game win \n First Complete \n +30 cristaux")
            else:
                app.game_win_popup_shown = True
                self.show_win_popup()
                print("Game win")

    def dead_monster(self):
        if self.parent:
            #print("'dead_monster' parent : ", self.parent, "widget delete : ", self)
            self.parent.remove_widget(self)  # Supprime le monstre
            self.dispatch('on_monster_death', self.coin_value)

            #si plus aucun monstre, win
            root_widget = App.get_running_app().root
            game_screen = root_widget.get_screen('game')
            map_zone = game_screen.map_zone  # Si `map_zone` est un attribut direct de GameScreen

            map_zone.current_monsters -= 1
            #print("map_zone.current_monsters", map_zone.current_monsters)
            map_zone.label_current_monsters.text=f'Mobs: {map_zone.current_monsters}'

            map_zone.programmed_monster -= 1
            
            if map_zone.lives > 0 and map_zone.programmed_monster == 0 and map_zone.current_monsters == 0: 
                #print("game_win called")
                self.game_win()
            
    def on_monster_death(self, *args):
        parent_reference = self.parent
        self.animate_coin_to_counter(parent_reference)
        if parent_reference and self in parent_reference.children:
            #print("'on_monster_death' parent : ", parent_reference, "widget delete : ", self)
            parent_reference.remove_widget(self)

    def on_pos(self, *args):
        if hasattr(self, 'bordure_vie') and hasattr(self, 'barre_vie') and hasattr(self, 'barre_vie_perdue'):
            # Mettre à jour la position et la largeur de la bordure
            self.bordure_vie.rectangle = (self.center_x, self.center_y - dp(10), self.largeur, dp(5))
            
            # Mettre à jour la position et la largeur des barres de vie
            self.barre_vie.pos = (self.center_x, self.center_y - dp(10))
            self.barre_vie_perdue.pos = (self.center_x, self.center_y - dp(10))
            self.barre_vie_perdue.size = (self.largeur, dp(5))

    def animate_coin_to_counter(self, parent_reference):
        root_widget = App.get_running_app().root
        game_screen = root_widget.get_screen('game')
        map_zone = game_screen.map_zone  # Accédez directement à map_zone via la référence root_widget

        # Créez une instance de pièce à la position actuelle du monstre
        coin = Coin(value=self.coin_value, pos=self.pos)
        
        # Ajoutez la pièce à map_zone
        map_zone.add_widget(coin)

        # Obtenez la position finale pour la pièce (là où se trouve le label "Pièces")
        end_pos = (map_zone.pieces_label.x + map_zone.pieces_label.width/2, 
                map_zone.pieces_label.y + map_zone.pieces_label.height/2)

        def on_animation_progress(animation, coin_instance, progression):
            #print(coin_instance, f"Progression: {progression}, Position: {coin_instance.pos}")
            pass

        # À la fin de l'animation, supprimez la pièce de map_zone et mettez à jour le nombre de pièces
        def on_animation_complete(animation, coin_instance):
            map_zone.coins += coin.value
            map_zone.pieces_label.text = f"Pièces: {map_zone.coins}"
            map_zone.remove_widget(coin_instance)
            #print("Animation complete!")

        # Créez une animation pour déplacer la pièce vers le label "Pièces"
        animation = Animation(center=end_pos, duration=0.25)
        #print("animate coin from :", self.pos, "to :",end_pos)
        animation.bind(on_progress=on_animation_progress)
        animation.bind(on_complete=on_animation_complete)
        animation.start(coin)
        
    def finalize_coin_animation(self, coin, map_zone):
        # Mettre à jour le nombre de pièces
        map_zone.coins += coin.value
        map_zone.pieces_label.text = f'Pièces: {map_zone.coins}'
        
        # Supprimer la pièce animée de l'écran
        map_zone.remove_widget(coin)
