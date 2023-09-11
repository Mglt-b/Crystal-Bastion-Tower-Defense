from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.properties import ListProperty, NumericProperty
from reglages_tours import tours
from kivy.clock import Clock, partial

from monstres import Monstre
from reglages_tours import tour_dict
from projectile import Projectile

from kivymd.uix.button import MDIconButton

from ameliorations_tours import ameliorations
from kivy.uix.image import Image

import uuid, os

import math

def calculate_angle(source, target):
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    return math.degrees(math.atan2(dy, dx))

class Tour(Widget):
    color = ListProperty([1, 1, 1, 1])  # Par défaut blanc
    dragging = False

    def __init__(self, tour_name, size, color=[1, 1, 1, 1], **kwargs):  # tour_type est l'index de la tour dans reglages_tours.py
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())  # Ajoutez cet identifiant unique
        self.register_event_type('on_touch_up')
        self.x_button = None

       

    def rotate_to_target(self, target):
        angle = calculate_angle(self.center, target.center)
        self.canvas.ask_update()
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size, rotation=angle)

    def update(self, dt):
        if self.target:
            self.rotate_to_target(self.target)

    def __init__(self, tour_name, size, color=[1, 1, 1, 1], **kwargs):  # tour_type est l'index de la tour dans reglages_tours.py
        super().__init__(**kwargs)

        self.id = str(uuid.uuid4())  # Ajoutez cet identifiant unique

        self.register_event_type('on_touch_up')
        self.x_button = None
        self.up_button = None
        self.del_button = None
        self.dragged = False

        self.colliding_with_path = False
        self.color = color
        self.initial_color = color  # Stockez la couleur initiale

        config = tour_dict[tour_name]

        self.size = config["taille"]

        self.proj_col = config["projectile_color"]
        self.name = config["nom"]
        self.range = config["range"]
        self.attack_speed = config["temps_entre_attaque"]
        self.damage = config["degats_physiques"]  # ou combinez les dégâts physiques et magiques si nécessaire
        self.img_directory = "tower_images/"
        self.projectile_speed = 10
        Clock.schedule_interval(self.attack, self.attack_speed)

        self.active = False  # Par défaut, la tour n'est pas active

        with self.canvas.before:
            self.tower_image = Image(source="", pos=self.pos, size=self.size)
            self.bg_color = Color(*self.initial_color)
            self.tower_image.source = os.path.join(self.img_directory, f"tower_{self.name}.png")
            self.bg = self.tower_image


        self.bind(color=self.update_color, pos=self.update_bg, size=self.update_bg)
        self.bind(pos=self.update_graphics_pos)
        self.bind(size=self.update_graphics_size)
        
        self.cout = config["cost"]
        self.niveau_amelioration = 0

        self.range_circle = None


    def update_graphics_pos(self, instance, value):
        self.bg.pos = value

    def update_graphics_size(self, instance, value):
        self.bg.size = value

    def select(self):
        with self.canvas:
            Color(1, 0, 0, 1)

    def update_color(self, *args):
        self.bg_color.rgba = self.color

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        

    def attack(self, *args):
        #print('Attack function called. Tower active:', self.active)
        # Vérifiez que self.parent existe
        if self.parent is None:
            return
        
        if self.active == False:
            return
        
        # Appel à self.find_closest_monster après un délai
        Clock.schedule_once(self._attack, 0)

    def _attack(self, dt):
        # Trouver le monstre le plus proche (vous pouvez ajuster cette logique si nécessaire)
        closest_monster = self.find_closest_monster()

        # Si un monstre est à portée, attaquez-le
        if closest_monster:
            # Vérifiez que le monstre a une position valide
            #print(closest_monster, closest_monster.x, closest_monster.y)
            if closest_monster.x != 0 or closest_monster.y != 0:
                self.animate_attack()
                # Créez un projectile
                projectile = Projectile(source=self, target=closest_monster, damage=self.damage, speed=self.projectile_speed, proj_col=self.proj_col)
                print(f"Projectile created with speed: {projectile.speed}")  # Pour le débogage
                #print('Projectile created and added to parent.', self, dt)
                self.parent.add_widget(projectile)


    def distance(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    
    def find_closest_monster(self):
        closest_monster = None
        closest_distance = float('inf')

        for child in self.parent.children:
            
            if isinstance(child, Monstre):
                
                distance = self.distance(self.center, child.center)
                if distance < closest_distance and distance <= self.range:
                    #print("debug",child.pos, child.x, child.y)
                    closest_distance = distance
                    closest_monster = child

        #print('Closest monster found:', closest_monster)
        return closest_monster
        


    def on_touch_up(self, touch):
        #print("on touch up called")
        #print('is drag?:', self.dragged)
        if not self.active:
            #print("not active")
            return super().on_touch_up(touch)
        #print(f"on_touch_up called for Tour with ID: {self.id}")
        # Vérifiez si le toucher est à l'intérieur de la zone de la tour
        #print("on_touch_up called")  # Pour vérifier si la méthode est appelée
        #print(self.collide_point(*touch.pos))  # Pour vérifier la détection du toucher à l'intérieur de la tour
        #print(self.dragged)  # Pour vérifier la valeur de l'attribut dragged
        if self.collide_point(*touch.pos) and self.dragged:
            # Affichez les boutons X et UP
            self.show_buttons()

            return True
        return super().on_touch_up(touch)

    def show_buttons(self):

        print(self.parent.parent.parent.width)

        if self.x < (self.parent.parent.parent.width * .8):
            

            # Logique pour afficher les boutons X et UP à côté de la tour
            if not self.x_button:

                self.x_button = MDIconButton(icon_size="20sp",icon="delete-forever",md_bg_color= (1,1,.6,1), pos=(self.x + self.width, self.y))
                self.x_button.bind(on_release=self.remove_tour)
                self.add_widget(self.x_button)
            
            if not self.up_button:
                self.up_button = MDIconButton(icon_size="20sp",icon="arrow-up-bold-hexagon-outline",md_bg_color= (1,1,.6,1),pos=(self.x + self.width, self.y + self.x_button.height))
                self.up_button.bind(on_release=self.upgrade_tour)
                self.add_widget(self.up_button)

            if not self.del_button:
                self.del_button = MDIconButton(icon_size="20sp",icon="eye-off",md_bg_color= (0,1,.6,1),pos=(self.x + self.width, self.y + self.x_button.height*2))
                self.del_button.bind(on_release=self.hidden_buttons_tour)
                self.add_widget(self.del_button)


        else:

            # Logique pour afficher les boutons X et UP à côté de la tour
            if not self.x_button:

                self.x_button = MDIconButton(icon_size="10sp",icon="delete-forever",md_bg_color= (1,1,.6,1), pos=(self.x - self.width*2, self.y))
                self.x_button.bind(on_release=self.remove_tour)
                self.add_widget(self.x_button)
            
            if not self.up_button:
                self.up_button = MDIconButton(icon_size="10sp",icon="arrow-up-bold-hexagon-outline",md_bg_color= (1,1,.6,1),pos=(self.x - self.width*2, self.y + self.x_button.height))
                self.up_button.bind(on_release=self.upgrade_tour)
                self.add_widget(self.up_button)

            if not self.del_button:
                self.del_button = MDIconButton(icon_size="10sp",icon="eye-off",md_bg_color= (0,1,.6,1),pos=(self.x - self.width*2, self.y + self.x_button.height*2))
                self.del_button.bind(on_release=self.hidden_buttons_tour)
                self.add_widget(self.del_button)

            

    def remove_tour(self, instance):
        # Stockez une référence à l'objet parent
        parent_ref = self.parent

        # Supprimez la tour elle-même
        if parent_ref:
            parent_ref.remove_widget(self)

        # Supprimez le bouton x_button
        if self.x_button and self.x_button.parent:
            self.x_button.parent.remove_widget(self.x_button)

        # Supprimez le bouton up_button
        if self.up_button and self.up_button.parent:
            self.up_button.parent.remove_widget(self.up_button)

        # Incrémente le compteur de pièces  -> on rembourse l'utilisateur de 25% du cout initial
        refund_amount = self.cout // 4
        if parent_ref:
            parent_ref.coins += refund_amount
            parent_ref.pieces_label.text = str(f'Pièces: {parent_ref.coins}')


    def upgrade_tour(self, instance):
        """Améliore les attributs de la tour en fonction des valeurs dans ameliorations_tours.py."""
        # Vérifiez si d'autres améliorations sont disponibles
        try :
            upgrade_data = ameliorations[self.name][self.niveau_amelioration]
        except Exception as e:
            print("Upgrade de cette tour non defini:", e)
            return
        
        if self.parent.coins < upgrade_data["cout_amelioration"]:
            print('pas assez argent')
            return


        if self.niveau_amelioration < len(ameliorations.get(self.name, [])):
            
            self.attack_speed = upgrade_data["temps_entre_attaque"]
            self.damage = upgrade_data["degats_physiques"]
            self.range = upgrade_data["range"]
            self.color = upgrade_data["color"]
            # Déduisez le coût de l'amélioration des pièces du joueur
            self.parent.coins -= upgrade_data["cout_amelioration"]
            # Mettez à jour le label du compteur de pièces
            self.parent.pieces_label.text = str(f'Pièces: {self.parent.coins}')
            # Augmentez le niveau d'amélioration
            self.niveau_amelioration += 1

            self.x_button.parent.remove_widget(self.x_button)
            self.x_button = None
            self.up_button.parent.remove_widget(self.up_button)
            self.up_button = None
            self.del_button.parent.remove_widget(self.del_button)
            self.del_button = None

        else:
            print(f"La tour de type {self.name} est déjà au niveau maximal d'amélioration.")


    def hidden_buttons_tour(self, instance):
        self.x_button.parent.remove_widget(self.x_button)
        self.x_button = None
        self.up_button.parent.remove_widget(self.up_button)
        self.up_button = None
        self.del_button.parent.remove_widget(self.del_button)
        self.del_button = None


    def animate_attack(self):
        """Change l'image de la tour pour montrer l'animation d'attaque."""
        self.tower_image.source = os.path.join(self.img_directory, f"tower_{self.name}_attack.png")
        # Programme la remise à l'état normal après 0,5 seconde
        Clock.schedule_once(self.reset_image, 0.5)

    def reset_image(self, *args):
        """Remet l'image de la tour à son état normal."""
        self.tower_image.source = os.path.join(self.img_directory, f"tower_{self.name}.png")
