from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line, Rotate, PushMatrix, PopMatrix, Ellipse
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp, sp
from kivy.storage.jsonstore import JsonStore

class Projectile(Widget):
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.speed = kwargs.get('speed', 5)
        self.size = (dp(15), dp(15))
        self.pos = self.source.center

        with self.canvas:
            PushMatrix()  # Sauvegarde de l'état graphique actuel
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.image = Rectangle(source='projectiles_images/fusee_image.png', pos=self.pos, size=self.size)
            PopMatrix()  # Restaure l'état graphique précédent
        
        # Calcul de la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        Clock.schedule_interval(self.move, 0.01)

    def move(self, dt):
        # Recalculez la direction pour pointer vers la position actuelle de la cible
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        new_pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        self.image.pos = new_pos

        # Mise à jour de l'angle de rotation en fonction de la direction et en utilisant (-1, 1) comme référence
        self.angle = -Vector(-1, 1).angle(self.direction)
        self.rotation.angle = self.angle
        self.rotation.origin = self.center

        # Vérification si le projectile a atteint la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques, self.source)
            if self.parent:
                self.parent.remove_widget(self)
            Clock.unschedule(self.move)


class IceProjectile(Projectile):  
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.speed = kwargs.get('speed', 5)

        self.size = (dp(15), dp(15))
        self.pos = self.source.center

        with self.canvas:
            PushMatrix()  # Sauvegarde de l'état graphique actuel
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.image = Rectangle(source='projectiles_images/glace_image.png', pos=self.pos, size=self.size)
            PopMatrix()  # Restaure l'état graphique précédent
        
        # Calcul de la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        Clock.schedule_interval(self.move, 0.01)

    def move(self, dt):
        # Recalculez la direction pour pointer vers la position actuelle de la cible
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        new_pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        self.image.pos = new_pos

        # Mise à jour de l'angle de rotation en fonction de la direction et en utilisant (-1, 1) comme référence
        self.angle = -Vector(0, -1).angle(self.direction)
        self.rotation.angle = self.angle
        self.rotation.origin = self.center

        # Vérification si le projectile a atteint la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques, self.source)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_slow_effect()


class FireProjectile(Projectile):  
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.speed = kwargs.get('speed', 5)
        self.size = (dp(15), dp(15))
        self.pos = self.source.center

        print("Fire projectile init")

        with self.canvas:
            PushMatrix()  # Sauvegarde de l'état graphique actuel
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.image = Rectangle(source='projectiles_images/feu_image.png', pos=self.pos, size=self.size)
            PopMatrix()  # Restaure l'état graphique précédent
        
        # Calcul de la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        Clock.schedule_interval(self.move, 0.01)

    def move(self, dt):
        # Recalculez la direction pour pointer vers la position actuelle de la cible
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        new_pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        self.image.pos = new_pos

        # Mise à jour de l'angle de rotation en fonction de la direction et en utilisant (-1, 1) comme référence
        self.angle = -Vector(-1, 1).angle(self.direction)
        self.rotation.angle = self.angle
        self.rotation.origin = self.center

        # Vérification si le projectile a atteint la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques, self.source)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_burn_effect()


class ElecProjectile(Projectile):  
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.speed = kwargs.get('speed', 5)

        self.size = (dp(15), dp(15))
        self.pos = self.source.center

        with self.canvas:
            PushMatrix()  # Sauvegarde de l'état graphique actuel
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.image = Rectangle(source='projectiles_images/elec_image.png', pos=self.pos, size=self.size)
            PopMatrix()  # Restaure l'état graphique précédent
        
        # Calcul de la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        Clock.schedule_interval(self.move, 0.01)

    def move(self, dt):
        # Recalculez la direction pour pointer vers la position actuelle de la cible
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        new_pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        self.image.pos = new_pos

        # Mise à jour de l'angle de rotation en fonction de la direction et en utilisant (-1, 1) comme référence
        self.angle = -Vector(-1, 1).angle(self.direction)
        self.rotation.angle = self.angle
        self.rotation.origin = self.center

        # Vérification si le projectile a atteint la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques, self.source)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_elec_effect()


class BombProjectile(Widget):
    speed = NumericProperty(5)
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    angle = NumericProperty(0)
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    degats_bombe = NumericProperty(25)

    def __init__(self, source, target, **kwargs):
        super().__init__(**kwargs)

        # Lisez les talents actuels depuis le fichier JSON
        talents = self.get_current_talents()

        # Ajustez les attributs de la tour en fonction des talents
        #example : self.range = config["range"] * (1 + talents["speed"] / 100)
        
        # Bomb attributes
        self.explosion_range = dp(40) * (1 + talents["Bomb_range"] / 100)
        self.explosion_delay = 5 - (5 * (talents["Bomb_delay"] / 100))
        self.degats_bombe = self.degats_bombe * (1 + talents["Bomb_damage"] / 100)
        
        self.source = source
        self.target = target

        self.size = (dp(15), dp(15))
        self.pos = self.source.center
        
        # Draw the bomb
        with self.canvas:        
            PushMatrix()  # Sauvegarde de l'état graphique actuel
            self.rotation = Rotate(angle=self.angle, origin=self.center)
            self.image = Rectangle(source='projectiles_images/bomb_image.png', pos=self.pos, size=self.size)
            PopMatrix()  # Restaure l'état graphique précédent

        # Calculate the direction once
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()
        
        Clock.schedule_interval(self.move, 0.01)
        Clock.schedule_interval(self.check_target, 0.5)

    def get_current_talents(self):
        # Lisez les talents depuis le fichier JSON et retournez-les sous forme de dictionnaire
        talent_store = JsonStore("db/talent.json")
        if not talent_store.exists("ATK speed"):
            # Si le fichier n'existe pas encore, initialisez les talents à 0
            return {"ATK speed" :0, "Bomb_damage": 0, "Bomb_range": 0, "Bomb_delay": 0}
        
        return {
            "Bomb_damage": talent_store.get("Bomb_damage")["value"],
            "Bomb_range": talent_store.get("Bomb_range")["value"],
            "Bomb_delay": talent_store.get("Bomb_delay")["value"]
        }

    def move(self, dt):
        # Recalculez la direction pour pointer vers la position actuelle de la cible
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()
        
        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y
        
        new_pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        self.image.pos = new_pos

        # Mettez à jour l'angle de rotation en fonction de la direction, en utilisant (-1, 1) comme référence
        self.angle = -Vector(-1, 1).angle(self.direction)
        self.rotation.angle = self.angle
        self.rotation.origin = self.center

        # Vérifiez si le projectile a atteint la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            Clock.unschedule(self.move)
            # Commencez à suivre la cible (monstre)
            Clock.schedule_interval(self.follow_target, 0.01)
            Clock.schedule_once(self.explode, self.explosion_delay)

    def follow_target(self, dt):
        # Mettez continuellement à jour le centre de la bombe pour correspondre au centre de la cible
        self.center = self.target.center
        self.image.pos = (self.center_x - self.width/2, self.center_y - self.height/2)
        # Assurez-vous que la bombe reste centrée sur la cible, sans rotation
        self.rotation.angle = 0

    def explode(self, *args):
        # Ajustez la taille de l'image pour correspondre à la portée de l'explosion et la centrer sur le monstre
        self.size = (self.explosion_range * 2, self.explosion_range * 2)
        self.center = self.target.center
        self.image.pos = (self.center_x - self.explosion_range, self.center_y - self.explosion_range)
        self.image.size = self.size
        self.image.source = 'effect_images/Explosed_image.png'

        # Infligez des dégâts à tous les monstres dans la portée de l'explosion
        from monstres import Monstre
        for child in self.parent.children:
            if isinstance(child, Monstre):
                if Vector(self.center).distance(child.center) <= self.explosion_range:
                    child.take_damage(self.degats_bombe, self.degats_bombe, self.source)  # En supposant que la classe Monstre ait une méthode take_damage

        Clock.unschedule(self.follow_target)
        Clock.schedule_once(self.remove_bomb, 0.2)  # Supprimez la bombe après l'animation de l'explosion
      
    def check_target(self, dt):
        # Check if the target (monster) is still active or if it has left the screen
        # TODO: Add the appropriate condition to check if the monster is out of the screen or has been removed
        if not self.target or self.target.is_out_of_screen() or not self.target.is_alive:
            Clock.unschedule(self.explode)  # Déprogrammez l'explosion
            self.remove_bomb()

    def remove_bomb(self, *args):
        self.target.has_bomb = False
        if self.parent:
            self.parent.remove_widget(self)
        Clock.unschedule(self.check_target)