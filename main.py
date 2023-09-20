from kivy import platform
if platform == "win":   
    from kivy.modules.screen import apply_device
    #(device, scale, orientation)
    apply_device("phone_iphone_4",1,"portrait") 

from jeu import MapZone, MainLayout
from niveau import niveaux

from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window
from functools import partial
import os

from kivymd.uix.button import MDRaisedButton
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.uix.widget import Widget

class WorldScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.worldscreen_widget = Widget()

        self.add_widget(self.worldscreen_widget)


        # Cristaux label
        self.cristaux_label = Label(text='Vies: as  a   a', pos=(dp(150), Window.height - dp(40)), color="blue", font_size = dp(12))

        self.worldscreen_widget.add_widget(self.cristaux_label)
        

        self.update_cristaux_label()

        # Get unique worlds
        worlds = list(set([niveau["world"] for niveau in niveaux]))
        worlds.sort()
        pos_worlds = [(dp(20), dp(20)),
                      (Window.width -dp(40), dp(40)),
                      (dp(20), dp(60)),
                      (Window.width -dp(110), dp(80)),
                      (dp(20), dp(100)),
                      (Window.width -dp(110), dp(120))]
        p=1
        for world in worlds:
            button = MDRaisedButton(text=world, on_release=partial(self.select_world, world), pos=pos_worlds[niveaux[p]["level"]])
            self.worldscreen_widget.add_widget(button)
            p+=1

        quit_button = MDRaisedButton(text="Quitter", on_release=App.get_running_app().stop)
        self.worldscreen_widget.add_widget(quit_button)


    def select_world(self, world, instance):
        self.manager.get_screen('menu').set_world(world)
        self.manager.current = 'menu'

    def get_cristaux(self):
        store = JsonStore(os.path.join('db', 'cristaux.json'))
        if not store.exists('count'):
            store.put('count', value=0)
        return store.get('count')['value']

    def update_cristaux_label(self):
        cristal_count = self.get_cristaux()
        self.cristaux_label.text = f"Cristaux : {cristal_count}"

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('init menu')
        self.world = None  # Initialisez l'attribut world


    def start_level(self, niveau, instance):
        # Logic to start the chosen level
        self.manager.current = 'game'
        self.manager.get_screen('game').start_game(niveau)

    def set_world(self, world):
        self.world = world
        print("set world", world)
        self.refresh_levels()

    def refresh_levels(self):
        self.clear_widgets()  # Clear existing buttons

        # Create a vertical layout for buttons
        layout = MDBoxLayout(orientation='vertical')
        
        # Load progress from JSON store
        store = JsonStore(os.path.join('db', 'progress.json'))
        
        # Determine the highest completed level
        completed_levels = [int(key) for key, value in store.find(completed=True)]
        highest_completed_level = max(completed_levels, default=0)

        for niveau in [n for n in niveaux if n["world"] == self.world]:
            print("niveau :", niveau)
            level_id = niveau["level"]
            print("level_id :", level_id)
            button_text = "Niveau " + str(level_id)

            if level_id <= highest_completed_level:
                button = MDRaisedButton(text=button_text)
                if level_id == highest_completed_level:
                    button.on_release = partial(self.start_level, niveau)
            elif level_id == highest_completed_level + 1:
                button = MDRaisedButton(text=button_text, on_release=partial(self.start_level, niveau))
            else:
                button = MDRaisedButton(text=button_text, disabled=True)  # Disable levels not yet unlocked

            layout.add_widget(button)

        # Back button
        back_button = MDRaisedButton(text="Retour", on_release=self.return_to_world_selection)
        layout.add_widget(back_button)

        self.add_widget(layout)


    # Nouvelle méthode pour retourner à l'écran de sélection de monde
    def return_to_world_selection(self, instance):
        self.manager.current = 'worlds'

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.niveau = None
        self.map_zone = None

    def start_game(self, niveau):
        #print("Début de start_game")  # Ajouté pour le débogage
        self.niveau = niveau
        self.main_layout = MainLayout(niveau)  # Initialise MainLayout avec le niveau choisi
        self.add_widget(self.main_layout)  # Assurez-vous d'ajouter MainLayout à GameScreen
        self.map_zone = self.main_layout.map_zone  # Accédez à MapZone à partir de MainLayout

        # Binding the events
        #print("map_zone avant liaison:", self.map_zone)  # Ajouté pour le débogage
        self.map_zone.bind(on_level_completed=self.return_to_menu)
        self.map_zone.bind(on_game_over=self.return_to_menu)

        self.manager.current = 'game'
        #print("Fin de start_game")   # Ajouté pour le débogage
        
    # Function to return to the main menu
    def return_to_menu(self, *args):
        self.manager.current = 'menu'

        self.niveau = self.niveau
        self.map_zone = MapZone(self.niveau)
        self.add_widget(self.map_zone)
        # TODO: Further logic to initialize and start the level

class MenuApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(WorldScreen(name='worlds'))
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(GameScreen(name='game'))

        self.scheduled_functions = []
        self.active_monsters = []

        self.game_over_popup_shown = False
        self.game_win_popup_shown = False
        return sm


if __name__ == '__main__':
    MenuApp().run()
