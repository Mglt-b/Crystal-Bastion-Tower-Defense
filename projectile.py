from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line, Rotate, PushMatrix, PopMatrix
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp, sp

class Projectile(Widget):
    damage = NumericProperty(0)
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    proj_col = ListProperty([1, 1, 1, 1])
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.damage = kwargs.get('damage', 0)
        self.speed = kwargs.get('speed', 5)
        self.proj_col = kwargs.get('proj_col', [1, 1, 1, 1])

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
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            if self.parent:
                self.parent.remove_widget(self)
            Clock.unschedule(self.move)


class IceProjectile(Projectile):  
    damage = NumericProperty(0)
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    proj_col = ListProperty([1, 1, 1, 1])
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.damage = kwargs.get('damage', 0)
        self.speed = kwargs.get('speed', 5)
        self.proj_col = kwargs.get('proj_col', [1, 1, 1, 1])

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
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_slow_effect()


class FireProjectile(Projectile):  
    damage = NumericProperty(0)
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    proj_col = ListProperty([1, 1, 1, 1])
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.damage = kwargs.get('damage', 0)
        self.speed = kwargs.get('speed', 5)
        self.proj_col = kwargs.get('proj_col', [1, 1, 1, 1])

        self.size = (dp(15), dp(15))
        self.pos = self.source.center

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
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_burn_effect()


class ElecProjectile(Projectile):  
    damage = NumericProperty(0)
    speed = NumericProperty(0)
    angle = NumericProperty(0)  # Nouvelle propriété pour stocker l'angle de rotation actuel
    source = ObjectProperty(None)
    target = ObjectProperty(None)
    proj_col = ListProperty([1, 1, 1, 1])
    degats_physiques = NumericProperty(0)
    degats_magiques = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)
        self.damage = kwargs.get('damage', 0)
        self.speed = kwargs.get('speed', 5)
        self.proj_col = kwargs.get('proj_col', [1, 1, 1, 1])

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
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)

            self.target.apply_elec_effect()
