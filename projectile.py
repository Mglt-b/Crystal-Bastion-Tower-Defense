from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.metrics import dp, sp

class Projectile(Widget):
    damage = NumericProperty(0)
    speed = NumericProperty(0)
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
        self.size = (dp(10), dp(5))
        self.pos = self.source.center

        # Calculer la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        with self.canvas:
            Color(1, 0, 0, 1)  # Couleur rouge
            self.rect = Rectangle(pos=(self.center_x - self.width/2, self.center_y - self.height/2), size=self.size)


        Clock.schedule_interval(self.move, 0.01)
        #print(f"Projectile created at position: {self.pos}")

    def move(self, dt):
        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        self.rect.pos = (self.center_x - self.width/2, self.center_y - self.height/2)


        #print(self.center_x,self.center_y)

        # Vérifie si le projectile est au centre de la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)


class IceProjectile(Projectile):
    damage = NumericProperty(0)
    speed = NumericProperty(0)
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


        self.size = (dp(10), dp(5))
        self.pos = self.source.center

        # Calculer la direction une seule fois
        self.direction = Vector(self.target.center_x - self.center_x, self.target.center_y - self.center_y).normalize()

        with self.canvas:
            Color(1, 1, 0, 1)  # Couleur jaune
            self.rect = Rectangle(pos=(self.center_x - self.width/2, self.center_y - self.height/2), size=self.size)


        Clock.schedule_interval(self.move, 0.01)
        #print(f"Projectile created at position: {self.pos}")

    def move(self, dt):
        step = self.direction * self.speed
        self.center_x += step.x
        self.center_y += step.y

        self.rect.pos = (self.center_x - self.width/2, self.center_y - self.height/2)


        #print(self.center_x,self.center_y)

        # Vérifie si le projectile est au centre de la cible
        if Vector(self.center).distance(self.target.center) < dp(7):
            self.target.take_damage(self.degats_physiques, self.degats_magiques)
            self.parent.remove_widget(self)
            Clock.unschedule(self.move)
            self.target.apply_slow_effect()