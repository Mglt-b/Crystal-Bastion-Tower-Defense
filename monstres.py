from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line, Ellipse
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

class Coin(Widget):
    def __init__(self,value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        with self.canvas:
            Color(1, 0.8, 0)  # Gold color for the coin
            self.ellipse = Ellipse(pos=self.pos, size=(10, 17))


class Monstre(Widget):
    coin_value = NumericProperty(0)  # Vous l'avez peut-être déjà
    def __init__(self, type_monstre, path, map_size, **kwargs):
        super().__init__(**kwargs)
        #print("Initialisation d'un nouveau monstre de type :", type_monstre)

        self.game_over_popup_shown = False
        
        self.register_event_type('on_monster_death')

        # Store map size
        self.map_size = map_size
        
        # Define monster characteristics
        self.speed = type_monstre["speed"]
        self.health = type_monstre["health"]
        self.vie_max = self.health

        self.coin_value = type_monstre["coin"]

        self.path = path
        self.current_target_idx = 1

        self.largeur = type_monstre["size"][0]
        
        # Set initial position
        self.pos = (self.path[0][0] * self.map_size[0], self.path[0][1] * self.map_size[1])
        
        # Debug: print initial position and map_size
        #print(f"Debug: Initial Position: {self.pos}")
        #print(f"Debug: Map Size: {self.map_size}")

        self.img_directory = "monstres_images/"

        self.name = type_monstre["name"]
        
        # Monster graphics
        with self.canvas:
            self.monster_image = Image(source="", pos=self.pos, size=type_monstre["size"])
            self.monster_image.source = os.path.join(self.img_directory, f"monstre_{self.name}.png")
            self.bg = self.monster_image

        with self.canvas:
            Color(1, 0, 0, 1)  # Rouge
            self.barre_vie_perdue = Rectangle(pos=(self.x, self.y - 10), size=(self.largeur, 5))

        # Barre de vie
        with self.canvas:
            Color(1, 1, 1, 1)  # Rouge
            # Bordure grise
            self.bordure_vie = Line(rectangle=(self.x, self.y - 10, self.largeur, 5), width=1.2)
            Color(0, 1, 0, 1)              
            # Barre de vie intérieure (verte)
            self.barre_vie = Rectangle(pos=(self.x, self.y - 10), size=(self.largeur, 5))

        # Start moving
        self.move()
    
    def move(self):

        if self.current_target_idx >= len(self.path):
            print("Error: Current target index out of range. Stopping the monster.")
            return


        # Calculate target position
        target = (self.path[self.current_target_idx][0] * self.map_size[0], self.path[self.current_target_idx][1] * self.map_size[1])
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        # If close to the target, move to next target
        if distance < self.speed:
            self.current_target_idx += 1
            # If reached the end, remove the monster
            if self.current_target_idx >= len(self.path):
                if self.parent:

                    #si monstre au bout du path, perd vie

                    root_widget = App.get_running_app().root
                    map_zone = root_widget.get_screen('game').map_zone  # Accédez directement à map_zone via la référence root_widget


                    print("perd vie")
                    map_zone.lives -= 1
                    map_zone.lives_label.text = f'Vies: {map_zone.lives}'
                        
                    if map_zone.lives <= 0:
                        self.game_over()  # This function needs to be implemented to handle game over logic

                    self.parent.remove_widget(self)

            else:
                self.move()
            return
        
        # Update position
        move_by_x = self.speed * dx / distance
        move_by_y = self.speed * dy / distance
        self.pos = (self.pos[0] + move_by_x, self.pos[1] + move_by_y)
        
        # Debug: print updated position
        #print(f"Debug: Updated Position: {self.pos}")
        
        # Update graphics
        #self.monster_image.pos = self.pos
        self.monster_image.pos = (self.pos[0] - self.monster_image.size[0]/2, self.pos[1] - self.monster_image.size[1]/2)


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
            # Ajoutez ces deux lignes pour revenir au menu principal
            root_widget.current = 'menu'
            root_widget.transition.direction = 'right'
            
        popup.bind(on_dismiss=on_popup_dismiss)
        
        close_button.bind(on_release=popup.dismiss)
        
        popup.open()



    def game_over(self):
        if not self.game_over_popup_shown:
            self.game_over_popup_shown = True
            self.show_defeat_popup()
            print("game over")


    def take_damage(self, damage):
        self.health -= damage
        # Mettre à jour la taille de la barre de vie
        pct_vie = self.health / self.vie_max
        self.barre_vie.size = (self.largeur * pct_vie, 5)
        with self.canvas:
            Color(1, 0, 0, 1)  # Rouge
            self.barre_vie_perdue.size = (self.largeur * (1 - pct_vie), 5)

        # Mettre à jour la couleur de la barre de vie
        if pct_vie < 0.5:
            Color(1, 0, 0, 1)  # Rouge
        else:
            Color(0, 1, 0, 1)  # Vert

        if self.health < 1 :
            self.dead_monster(damage)

    def dead_monster(self, damage):
        if self.parent:
            print("'dead_monster' parent : ", self.parent, "widget delete : ", self)
            self.parent.remove_widget(self)  # Supprime le monstre
            self.dispatch('on_monster_death', self.coin_value)
            
    def on_monster_death(self, *args):
        parent_reference = self.parent
        self.animate_coin_to_counter(parent_reference)
        if parent_reference and self in parent_reference.children:
            print("'on_monster_death' parent : ", parent_reference, "widget delete : ", self)
            parent_reference.remove_widget(self)

    def on_pos(self, *args):
        if hasattr(self, 'bordure_vie') and hasattr(self, 'barre_vie') and hasattr(self, 'barre_vie_perdue'):
            # Mettre à jour la position et la largeur de la bordure
            self.bordure_vie.rectangle = (self.x, self.y - 10, self.largeur, 5)
            
            # Mettre à jour la position et la largeur des barres de vie
            self.barre_vie.pos = (self.x, self.y - 10)
            self.barre_vie_perdue.pos = (self.x, self.y - 10)
            self.barre_vie_perdue.size = (self.largeur, 5)

    def animate_coin_to_counter(self, parent_reference):
        root_widget = App.get_running_app().root
        map_zone = root_widget.map_zone  # Accédez directement à map_zone via la référence root_widget

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
