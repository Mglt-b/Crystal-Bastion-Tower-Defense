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

class Coin(Widget):
    def __init__(self,value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        with self.canvas:
            Color(1, 0.8, 0)  # Gold color for the coin
            self.ellipse = Ellipse(pos=self.pos, size=(dp(10), dp(17)))

class Monstre(Widget):
    coin_value = NumericProperty(0)
    angle = NumericProperty(0)
    def __init__(self, type_monstre, path, map_size, **kwargs):
        super().__init__(**kwargs)
        #print("Initialisation d'un nouveau monstre de type :", type_monstre)
        
        self.register_event_type('on_monster_death')

        # Store map size
        self.map_size = map_size
        
        # Define monster characteristics
        self.speed = type_monstre["speed"]
        self.health = type_monstre["health"]
        self.armure = type_monstre["armure"]
        self.magique_resistance = type_monstre["magique_resistance"]
        self.vie_max = self.health

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


        self.freeze_effect = Image(source="effect_images/Freeze_image.png", opacity=0, size=(type_monstre["size"][0]/2,type_monstre["size"][1]/2), pos=(self.center_x,self.center_y))
        self.update_freeze_effect_position()
        self.add_widget(self.freeze_effect)
        self.slowed = False  # New property to track if the monster is slowed

        # Start moving
        self.move()
        anim = Animation(angle=360, duration=1)
        anim += Animation(angle=0, duration=0)
        anim.repeat = True
        anim.start(self)
        self.bind(angle=self.on_angle)

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

    def move(self):
        root_widget = App.get_running_app().root
        map_zone = root_widget.get_screen('game').map_zone  # Accédez directement à map_zone via la référence root_widget
       
        # Calculate target position
        target = (self.path[self.current_target_idx][0] * self.map_size[0], self.path[self.current_target_idx][1] * self.map_size[1])
        dx = target[0] - self.center_x
        dy = target[1] - self.center_y
        distance = (dx**2 + dy**2)**0.5

        self.freeze_effect.pos = self.center
        
        # If close to the target, move to next target
        if distance < self.speed:
            self.current_target_idx += 1
            # If reached the end, remove the monster
            if self.current_target_idx >= len(self.path):
                if self.parent:

                    #si monstre au bout du path, perd vie

                    print("perd vie")
                    map_zone.lives -= 1
                    map_zone.lives_label.text = f'Vies: {map_zone.lives}'
                    
                    map_zone.current_monsters -= 1
                    print("monstre fin path, retiré, count :",map_zone.current_monsters)

                    print('map_zone.lives', map_zone.lives)
                    if map_zone.lives <= 0:
                        self.game_over()  # This function needs to be implemented to handle game over logic

                    if map_zone.lives > 0 and map_zone.current_monsters == 0: 
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
                print(child)
                map_zone.remove_widget(child)

            #supprime les monstres programmés
            for event in map_zone.scheduled_monster_events:
                Clock.unschedule(event)
                print("unshedule : ", event)
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
                print(child)
                map_zone.remove_widget(child)

            #supprime les monstres programmés
            for event in map_zone.scheduled_monster_events:
                Clock.unschedule(event)
                print("unshedule : ", event)
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

    def game_over(self):

        app = App.get_running_app()
        
        if not app.game_over_popup_shown:
            app.game_over_popup_shown = True
            self.show_defeat_popup()
            print("game over")

    def game_win(self):

        app = App.get_running_app()
        
        if not app.game_win_popup_shown:
            app.game_win_popup_shown = True
            self.show_win_popup()
            print("game win")

    def take_damage(self, damage_physique, damage_magique):
        # Calcul des dégâts réels en prenant en compte l'armure et la résistance magique
        degats_reels_physiques = damage_physique * (1 - (self.armure / (100 + self.armure)))
        degats_reels_magiques = damage_magique * (1 - (self.magique_resistance / (100 + self.magique_resistance)))
        
        # Somme des dégâts réels
        total_damage = degats_reels_physiques + degats_reels_magiques
        
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
            self.dead_monster()

    def dead_monster(self):
        if self.parent:
            print("'dead_monster' parent : ", self.parent, "widget delete : ", self)
            self.parent.remove_widget(self)  # Supprime le monstre
            self.dispatch('on_monster_death', self.coin_value)

            #si plus aucun monstre, win
            root_widget = App.get_running_app().root
            game_screen = root_widget.get_screen('game')
            map_zone = game_screen.map_zone  # Si `map_zone` est un attribut direct de GameScreen

            map_zone.current_monsters -= 1
            print("map_zone.current_monsters", map_zone.current_monsters)
            
            if map_zone.current_monsters == 0:
                self.game_win()
            
    def on_monster_death(self, *args):
        parent_reference = self.parent
        self.animate_coin_to_counter(parent_reference)
        if parent_reference and self in parent_reference.children:
            print("'on_monster_death' parent : ", parent_reference, "widget delete : ", self)
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

        # Créez une animation pour déplacer la pièce vers le label "Pièces"
        animation = Animation(center=end_pos, duration=.5)

        # À la fin de l'animation, supprimez la pièce de map_zone et mettez à jour le nombre de pièces
        def on_animation_complete(animation, coin_instance):
            map_zone.coins += coin.value
            map_zone.pieces_label.text = f"Pièces: {map_zone.coins}"
            map_zone.remove_widget(coin_instance)

        animation.bind(on_complete=on_animation_complete)
        animation.start(coin)

    def finalize_coin_animation(self, coin, map_zone):
        # Mettre à jour le nombre de pièces
        map_zone.coins += coin.value
        map_zone.pieces_label.text = f'Pièces: {map_zone.coins}'
        
        # Supprimer la pièce animée de l'écran
        map_zone.remove_widget(coin)
