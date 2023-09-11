from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color, Line, Ellipse

from niveau import niveaux
from monstres import Monstre
from tour import Tour
from kivy.clock import Clock

from reglages_tours import tours
from projectile import Projectile
from reglage_monstres import monstre_configurations

from kivy.properties import ListProperty, NumericProperty

from reglages_tours import tours_info

import random
import os

from functools import partial
from reglages_tours import tour_dict
from kivy.app import App

# Pour que l'application soit toujours en mode portrait
Window.size = (360, 640)
Window.rotation = 0

# jeu.py
tour_selected = False

class TourSelectionZone(BoxLayout):
    def __init__(self, **kwargs):
        # Custom events to signal end of a level
        self.register_event_type('on_level_completed')
        self.register_event_type('on_game_over')

        super().__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 100  # Hauteur fixe pour la zone de sélection des tours
        self.spacing=30
        self.padding=[10,0,0,0]

        # Ajout de l'arrière-plan
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, .5)  # Gris foncé pour l'arrière-plan
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Ajout de toutes les tours disponibles
        for tour_config in tours:
            # Création d'un layout vertical pour empiler le label et la tour
            tour_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=tour_config["taille"][0], spacing=5)
            
            # Création et ajout du label avec le nom et le coût de la tour
            tour_label = Label(text=f"{tour_config['nom']}\n{tour_config['cost']} coins",height=tour_config["taille"][1], width=tour_config["taille"][0], size_hint_y=.5, font_size=10)
            tour_layout.add_widget(tour_label)
            
            # Création et ajout de la représentation de la tour
            tour = Tour(size=tour_config["taille"], color=tour_config["couleur"], tour_name=tour_config["nom"])
            tour_layout.add_widget(tour)

            self.add_widget(tour_layout)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_level_completed(self, *args):
        pass

    def on_game_over(self, *args):
        pass

class MapZone(Widget):
    tours = ListProperty([])
    def __init__(self, niveau, **kwargs):
        print("Début de l'initialisation de MapZone")  # Ajouté pour le débogage
        self.lives = super().__init__(**kwargs)
        self.niveau = niveau
        self.path_points = []
        self.dragging_tour = None  # Pour suivre la tour que nous déplaçons
        self.tower_drag_start_pos = None  # Pour sauvegarder la position d'origine de la tour

        with self.canvas:
            Color(1, 0, 0, 1)  # Rouge pour le chemin
            self.path = Line(points=[], width=2)
        self.bind(size=self.on_size)

        self.coins = 200
        

        self.pieces_label = Label(text=f'Pièces: {self.coins}', pos=(10, Window.height - 30), color="red")
        self.pieces_label.id = 'pieces_label'  # Ajout d'un ID
        self.add_widget(self.pieces_label)

        self.lives = 2  # Initialize with 20 lives
        self.lives_label = Label(text=f'Vies: {self.lives}', pos=(150, Window.height - 30), color="blue")
        self.add_widget(self.lives_label)
        print("Fin de l'initialisation de MapZone")   # Ajouté pour le débogage

        self.bind(size=self.update_labels_position)

    def update_labels_position(self, *args):
        self.pieces_label.pos = (10, self.height - 30)
        self.lives_label.pos = (150, self.height - 30)
        
    def on_size(self, *args):
        print('Debug: self.width:', self.width)
        print('Debug: self.height:', self.height)
        adjusted_path = [(p[0]*self.width, p[1]*self.height) for p in self.niveau["path"]]
        print('Debug: adjusted_path:', adjusted_path)
        self.path.points = self.flatten_path(adjusted_path)

    def flatten_path(self, path):
        """Transforme une liste de points (x, y) en une liste plate pour Kivy."""
        return [coord for point in path for coord in point]

    def start_level(self, niveau):
        print("Démarrage du niveau avec la configuration :", niveau)
        self.path_points = niveau["path"]
        print(niveau["path"])
        delay = 0
        path = niveau["path"]
        for monster_info in niveau["monsters"]:
            for _ in range(monster_info["count"]):
                print("Programmation de l'appel à add_monster avec un délai de :", delay)
                Clock.schedule_once(partial(self.add_monster, monster_info=monster_info, path=path), delay)
                print("Appel à add_monster programmé.")
                delay += 2

    def add_monster(self, dt,monster_info, path):
        self._add_monster(monster_info, path)

    def _add_monster(self, monster_info, path):
        monster_type = monstre_configurations[monster_info["type"]]
        monster = Monstre(type_monstre=monster_type, path=path, map_size=self.size)
        app = App.get_running_app()
        app.active_monsters.append(self)
        monster.bind(on_monster_death=self.add_coins)
        self.add_widget(monster)

    def on_touch_down(self, touch):

        
        # Vérifiez si le toucher est sur un BoxLayout de Tour dans TourSelectionZone
        for tour_layout in self.parent.tour_selection_zone.children:
            if tour_layout.collide_point(*touch.pos):
                # Récupérez l'objet Tour à partir des enfants du BoxLayout
                tour = next((widget for widget in tour_layout.children if isinstance(widget, Tour)), None)
                
                if tour is not None:
                    # Récupérez le coût de la tour à partir des attributs de la tour
                    tour_cost = getattr(tour, 'cout', None) or getattr(tour, 'cost', None)
                    if tour_cost is not None:
                        self.cout = tour_cost
                    else:
                        print("Error: Unable to retrieve tour cost")
                        return False
                else:
                    print("Error: Tour object not found inside the BoxLayout")
                    return False
                if self.coins >= self.cout:
                    # Créez une nouvelle instance de la tour pour le drag-and-drop
                    self.dragging_tour = Tour(pos=touch.pos, size_hint=(None, None), size=tour.size, color=tour.color, tour_name=tour.name)
                    self.add_widget(self.dragging_tour)
                    return True
                else:
                    return False
        
        # Handle touch/click on existing towers on the map
        for tower in self.tours:
            if tower.collide_point(*touch.pos):
                # Logic to display icons for the clicked tower
                tower.show_buttons()
                return True

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        try:
            # Vérifiez d'abord si l'attribut 'dragging_tour' existe
            if hasattr(self, 'dragging_tour') and self.dragging_tour:
                self.dragging_tour.center = touch.pos

                # Supprimez le cercle précédent s'il existe
                if hasattr(self.dragging_tour, 'range_circle') and self.dragging_tour.range_circle:
                    self.dragging_tour.canvas.before.remove(self.dragging_tour.range_circle)

                # Dessinez un cercle semi-transparent autour de la tour
                with self.dragging_tour.canvas.before:
                    Color(1, 1, .7, 0.5)  # Jaune avec 50% d'opacité
                    self.dragging_tour.range_circle = Ellipse(
                        pos=(self.dragging_tour.center_x - self.dragging_tour.range, self.dragging_tour.center_y - self.dragging_tour.range),
                        size=(self.dragging_tour.range*2, self.dragging_tour.range*2)
                    )

                collision_detected = False

                # Vérifiez si la tour est en collision avec MapZone
                tour_right = self.dragging_tour.x + self.dragging_tour.width
                tour_top = self.dragging_tour.y + self.dragging_tour.height
                
                if (self.dragging_tour.x < self.x or tour_right > self.right or
                    self.dragging_tour.y < self.y or tour_top > self.top):
                    self.dragging_tour.tower_image.source = os.path.join(self.dragging_tour.img_directory, f"tower_Impossible.png")
                    print("collision with MapZone")
                    collision_detected = True
                # Vérifiez si la tour est en collision avec le chemin
                elif self.collides_with_path(self.dragging_tour.pos, self.dragging_tour.size):
                    self.dragging_tour.color = [1, 0, 0, 1]  # Rouge
                    self.dragging_tour.tower_image.source = os.path.join(self.dragging_tour.img_directory, f"tower_Impossible.png")
                    collision_detected = True
                # Vérifiez si la tour est en collision avec une autre tour, seulement si aucune collision précédente n'a été détectée
                elif not collision_detected:
                    for tour in self.tours:
                        if tour.collide_point(*touch.pos):
                            self.dragging_tour.tower_image.source = os.path.join(self.dragging_tour.img_directory, f"tower_Impossible.png")
                            print("collision tour")
                            collision_detected = True
                            break

                # Si aucune collision n'a été détectée, réinitialisez la couleur et l'image de la tour
                if not collision_detected:
                    self.dragging_tour.color = self.dragging_tour.initial_color  # Réinitialisez à la couleur initiale
                    self.dragging_tour.tower_image.source = os.path.join(self.dragging_tour.img_directory, f"tower_{self.dragging_tour.name}.png")

                return True
            return super().on_touch_move(touch)
        except Exception as e:
            print("'on_touch_move' Err:", e)

    def on_touch_up(self, touch):

        if self.dragging_tour.tower_image.source.endswith("tower_Impossible.png"):
            # Supprimez simplement la tour "fantôme" et n'ajoutez pas de nouvelle tour.
            self.remove_widget(self.dragging_tour)
        else:
            try:
                if self.dragging_tour:
                    # Si la tour ne touche pas le chemin, placez-la
                    if self.dragging_tour.color != [1, 0, 0, 1]:
                        if not hasattr(self.dragging_tour, 'colliding_with_path') or not self.dragging_tour.colliding_with_path:
                            
                            # Créez une nouvelle instance de la tour avec les mêmes attributs que dragging_tour
                            tour_name = self.dragging_tour.name
                            color = self.dragging_tour.color
                            size = self.dragging_tour.size
                            new_tour = Tour(tour_name, size, color)
                            self.tours.append(new_tour)
                            new_tour.pos = self.dragging_tour.pos
                            new_tour.active = True
                            new_tour.dragged = True
                            
                            # Ajoutez la nouvelle instance de la tour à MapZone
                            self.add_widget(new_tour)
                            
                            # Supprimez la tour "fantôme" du widget principal
                            self.remove_widget(self.dragging_tour)

                            # Réinitialisez dragging_tour à None
                            self.dragging_tour = None

                            self.coins -= self.cout
                            self.pieces_label.text = str(f'Pièces: {self.coins}')



                else:
                    self.remove_widget(self.dragging_tour)
                    return True
                

            except Exception as e:
                print("Err:", e)
            
    def collides_with_path(self, tour_pos, tour_size):
        x, y = tour_pos
        right, top = x + tour_size[0], y + tour_size[1]
        
        for i in range(len(self.path_points) - 1):
            adjusted_path_point1 = (self.path_points[i][0] * self.width, self.path_points[i][1] * self.height)
            adjusted_path_point2 = (self.path_points[i+1][0] * self.width, self.path_points[i+1][1] * self.height)
            
            if self.segment_intersects_rect((adjusted_path_point1, adjusted_path_point2), (x, y, right, top)):
                return True

        return False
    
    def point_inside_circle(self, point, circle_center, circle_radius):
        """Vérifie si un point est à l'intérieur d'un cercle."""
        return self.distance(point, circle_center) < circle_radius

    def line_intersects_circle(self, line_start, line_end, circle_center, circle_radius):
        """Vérifie si un segment de ligne intersecte un cercle."""
        a, b = line_start, line_end
        c = circle_center
        r = circle_radius

        # Vérifie si l'une des extrémités de la ligne est à l'intérieur du cercle
        if self.point_inside_circle(a, c, r) or self.point_inside_circle(b, c, r):
            return True

        # Vérifie si le cercle intersecte la ligne
        A = b[1] - a[1]
        B = a[0] - b[0]
        C = b[0] * a[1] - a[0] * b[1]
        dist = abs(A * c[0] + B * c[1] + C) / (A**2 + B**2)**0.5

        return dist < r

    def segment_intersects_rect(self, segment, rect):
        """Vérifie si un segment de ligne intersecte un rectangle."""
        x, y, right, top = rect
        rect_segments = [
            [(x, y), (right, y)],
            [(right, y), (right, top)],
            [(right, top), (x, top)],
            [(x, top), (x, y)]
        ]
        for rect_segment in rect_segments:
            if self.line_intersects_line(segment[0], segment[1], rect_segment[0], rect_segment[1]):
                return True
        return False

    def line_intersects_line(self, l1_p1, l1_p2, l2_p1, l2_p2):
        """Vérifie si deux lignes (l1_p1, l1_p2) et (l2_p1, l2_p2) se croisent."""
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        return ccw(l1_p1, l2_p1, l2_p2) != ccw(l1_p2, l2_p1, l2_p2) and ccw(l1_p1, l1_p2, l2_p1) != ccw(l1_p1, l1_p2, l2_p2)
    

    def add_coins(self, instance, value):
        self.coins += value
        self.pieces_label.text = str(f'Pièces: {self.coins}')

class MainLayout(BoxLayout):
    def __init__(self, niveau, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Sélectionnez un niveau (par exemple le premier)
        selected_niveau = niveau
        
        # Ajout de la zone de la carte avec le niveau sélectionné
        self.map_zone = MapZone(niveau,size_hint=(1, 0.8))  # Initialise MapZone avec le niveau choisi
        
        # Associez map_zone à l'ID 'map_zone'
        self.ids['map_zone'] = self.map_zone
        
        self.add_widget(self.map_zone)
        
        # Ajout de la zone de sélection des tours
        self.tour_selection_zone = TourSelectionZone(size_hint=(1, 0.2))
        self.add_widget(self.tour_selection_zone)

        # Démarrer le niveau après avoir ajouté la MapZone
        self.map_zone.start_level(selected_niveau)
