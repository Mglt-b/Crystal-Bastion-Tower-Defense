from niveau import niveaux

from jeu import MapZone
from niveau import niveaux

from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from jeu import MapZone, MainLayout
from functools import partial

from kivy.clock import Clock

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[50, 50], spacing=20)

        # Dynamically create buttons for each level
        for index, niveau in enumerate(niveaux):
            button = Button(text="Niveau " + str(index + 1), on_release=partial(self.start_level, niveau))
            layout.add_widget(button)

        exit_button = Button(text="Quitter", on_release=App.get_running_app().stop)
        layout.add_widget(exit_button)
        self.add_widget(layout)

    def start_level(self, niveau, instance):
        # Logic to start the chosen level
        self.manager.current = 'game'
        self.manager.get_screen('game').start_game(niveau)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.niveau = None
        self.map_zone = None

    def start_game(self, niveau):
        print("Début de start_game")  # Ajouté pour le débogage
        self.niveau = niveau
        self.main_layout = MainLayout(niveau)  # Initialise MainLayout avec le niveau choisi
        self.add_widget(self.main_layout)  # Assurez-vous d'ajouter MainLayout à GameScreen
        self.map_zone = self.main_layout.map_zone  # Accédez à MapZone à partir de MainLayout

        # Binding the events
        print("map_zone avant liaison:", self.map_zone)  # Ajouté pour le débogage
        self.map_zone.bind(on_level_completed=self.return_to_menu)
        self.map_zone.bind(on_game_over=self.return_to_menu)

        self.manager.current = 'game'
        print("Fin de start_game")   # Ajouté pour le débogage
        
    # Function to return to the main menu
    def return_to_menu(self, *args):
        self.manager.current = 'menu'

        self.niveau = self.niveau
        self.map_zone = MapZone(self.niveau)
        self.add_widget(self.map_zone)
        # TODO: Further logic to initialize and start the level

class MenuApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game'))

        self.scheduled_functions = []
        self.active_monsters = []

        return sm

        

    def schedule_function(self, func, *args, **kwargs):
        event = Clock.schedule_interval(func, *args, **kwargs)
        self.scheduled_functions.append((func, event, args, kwargs))

    def unschedule_all(self):
        for func, event, args, kwargs in self.scheduled_functions:
            Clock.unschedule(event)

    def reschedule_all(self):
        for func, event, args, kwargs in self.scheduled_functions:
            self.schedule_function(func, *args, **kwargs)



if __name__ == '__main__':
    MenuApp().run()
