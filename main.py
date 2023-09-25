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
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from kivy.uix.checkbox import CheckBox
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton

from kivymd.uix.card import MDCard

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class TalentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_scroll0 = BoxLayout(orientation='vertical', size_hint=(1, .9), pos_hint= {'top': 1, 'top': 1})
        main_scroll = ScrollView(do_scroll_x=False)
        main_scroll0.add_widget(main_scroll)
        
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        main_scroll.add_widget(main_layout)
        
        # Afficher le compteur d'étoiles en haut
        self.star_count = self.get_stars_from_json()
        self.star_label = Label(text=f"Étoiles : {self.star_count}", font_size=dp(16), size_hint_y=None, height=dp(50), color="black")
        main_layout.add_widget(self.star_label)
        
        # Initialisez le dictionnaire pour stocker les labels des talents
        self.talent_labels = {}
        # Liste des talents
        self.talents = ["speed", "attack_phy", "attack_mag", "range", "extra ice effect", "extra fire damage", "extra bomb damage", "extra life points"]

        # Lire la valeur totale des étoiles
        self.star_count = self.get_stars_from_json()

        # Soustraire la somme des valeurs des talents
        for talent in self.talents:
            self.star_count -= self.get_talent_value(talent)

        # Mettre à jour le label du compteur d'étoiles
        self.star_label.text = f"Étoiles : {self.star_count} ({self.get_stars_from_json()})"


        
        for talent in self.talents:
            talent_card = MDCard(size_hint=(.9, None), height=dp(50), style="outlined", line_color=(0.2, 0.2, 0.2, 1), pos_hint= {'center_x': .5, 'center_y': .5},padding = [dp(5),dp(5),dp(5),dp(5)], spacing=dp(5), elevation=3)
            talent_layout = BoxLayout(size_hint=(1, 1),spacing=dp(5))
            
            talent_value = self.get_talent_value(talent)
            talent_label = MDLabel(text=f"{talent}: +{talent_value}%", size_hint_x=0.6, color="black")
            
            # Stocker une référence au label dans le dictionnaire
            self.talent_labels[talent] = talent_label
            
            add_button = MDRaisedButton(text="+", on_release=lambda x, t=talent: self.modify_talent(t, 1),size_hint=(.2, None))
            subtract_button = MDRaisedButton(text="-", on_release=lambda x, t=talent: self.modify_talent(t, -1))
            
            talent_layout.add_widget(talent_label)
            talent_layout.add_widget(add_button)
            talent_layout.add_widget(subtract_button)
            
            talent_card.add_widget(talent_layout)
            main_layout.add_widget(talent_card)
        
        # À la fin de la méthode __init__, définissez la hauteur de main_layout.
        main_layout.height = len(self.talents) * (dp(50) + dp(10)) + dp(50)  # hauteur de MDCard + espacement + hauteur du label d'étoile

        # Ajoutez main_scroll0 (qui contient le ScrollView) au screen
        self.add_widget(main_scroll0)

        # Create a horizontal layout for back
        back_layout = BoxLayout(orientation='horizontal', spacing=dp(10), height=dp(20))
        # Back button
        back_button = MDRaisedButton(text="Retour", on_release=self.return_to_world_selection)

        back_layout.add_widget(back_button)
        self.add_widget(back_layout)

    def get_stars_from_json(self):
        # Chargez le total des étoiles du fichier JSON
        store = JsonStore('db/stars.json')
        total_stars = sum([store.get(key)["stars"] for key in store.keys()])
        return total_stars
    
    def get_talent_value(self, talent_name):
        # Chargez la valeur du talent du fichier JSON
        store = JsonStore("db/talent.json")
        if not store.exists(talent_name):
            store.put(talent_name, value=0)
        return store.get(talent_name)["value"]
    
    def modify_talent(self, talent_name, value):
        current_value = self.get_talent_value(talent_name)
        new_value = current_value + value
        
        # Assurez-vous qu'il y a assez d'étoiles et que la valeur ne devient pas négative
        if (self.star_count - value >= 0) and (new_value >= 0) and (new_value <= 20):
            store = JsonStore("db/talent.json")
            store.put(talent_name, value=new_value)
            
            # Mettez à jour le compteur d'étoiles
            self.star_count -= value
            self.star_label.text = f"Étoiles : {self.star_count}"
            
            # Mettez à jour le label du talent
            self.talent_labels[talent_name].text = f"{talent_name}: +{new_value}%"

    def return_to_world_selection(self, instance):
        self.manager.current = 'worlds'

class DeckScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.worldscreen_widget = Widget()
        self.add_widget(self.worldscreen_widget)

        self.layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))
        self.add_widget(self.layout)

    def check_tower_selection(self, checkbox, value):
        # Limiter à 4 tours cochées
        if value and sum([cb.active for cb in self.checkboxes]) > 4:
            checkbox.active = False
    
    def save_deck(self, instance):
        # Enregistrez les tours sélectionnées dans tower_deck.json
        selected_towers = [tower for tower, checkbox in zip(self.bought_towers, self.checkboxes) if checkbox.active]
        deck_store = JsonStore(os.path.join('db', 'tower_deck.json'))
        deck_store.put('selected_towers', towers=selected_towers)
        self.return_to_world_selection(instance)

    def return_to_world_selection(self, instance):
        self.manager.current = 'worlds'

    def get_cristaux(self):
        store = JsonStore(os.path.join('db', 'cristaux.json'))
        if not store.exists('count'):
            store.put('count', value=0)
        return store.get('count')['value']

    def update_cristaux_label(self):
        cristal_count = self.get_cristaux()
        self.cristaux_label.text = str(cristal_count)

    def update_counters(self):
        # Update cristal count from JsonStore
        # (You might want to implement the logic for this if it's not already done)

        # Update stars count from JsonStore
        stars_store = JsonStore(os.path.join('db', 'stars.json'))
        total_stars = sum([stars_store.get(key)["stars"] for key in stars_store.keys()])

        self.stars_label.text = str(total_stars)

    def on_enter(self, *args):
        self.layout.clear_widgets()

        # Top bar for counters
        top_bar = MDBoxLayout(orientation='horizontal', size_hint=(.5, None), height=dp(50), spacing=dp(5))
        self.layout.add_widget(top_bar)  # Assurez-vous de l'ajouter en premier pour qu'il soit en haut
        
        # Cristaux counter
        crystal_icon = MDIconButton(icon="diamond-stone", font_size=dp(24), text_color="blue", theme_text_color="Custom")
        self.cristaux_label = Label(text='0', font_size=dp(16), color=(0, 0, 0, 1))
        crystal_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_x = .1)
        crystal_layout.add_widget(crystal_icon)
        crystal_layout.add_widget(self.cristaux_label)
        top_bar.add_widget(crystal_layout)

        # Stars counter
        star_icon = MDIconButton(icon="star", font_size=dp(24), text_color=(1, 0.84, 0, 1), theme_text_color="Custom")
        self.stars_label = Label(text='0', font_size=dp(16), color=(0, 0, 0, 1))
        star_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_x = .1)

        star_layout.add_widget(star_icon)
        star_layout.add_widget(self.stars_label)
        top_bar.add_widget(star_layout)


        self.update_cristaux_label()
        self.update_counters()


        # Liste des tours achetées
        bought_towers_store = JsonStore(os.path.join('db', 'tower_buy.json'))
        self.bought_towers = []

        self.bought_towers.append("Basique")
        self.bought_towers2 = [key for key in bought_towers_store.keys() if bought_towers_store.get(key).get("bought")]

        self.bought_towers = self.bought_towers + self.bought_towers2

        # Créer une liste pour stocker les cases à cocher
        self.checkboxes = []
        
        # Créer une section pour la sélection des tours
        self.tower_selection_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        for tower in self.bought_towers:
            tower_layout = BoxLayout(orientation='horizontal', spacing=dp(10))
            checkbox = CheckBox(size_hint_x=None, width=dp(50), color=[0, 0, 0, 1])
            checkbox.bind(active=self.check_tower_selection)
            tower_label = Label(text=tower, size_hint_x=0.8, color=(0, 0, 0, 1))  # Texte en noir
            # Cocher la case si la tour est déjà cochée dans le fichier JSON
            if self.is_tower_checked(tower):
                checkbox.active = True
                
            tower_layout.add_widget(checkbox)
            tower_layout.add_widget(tower_label)
            self.checkboxes.append(checkbox)
            self.tower_selection_layout.add_widget(tower_layout)
        self.layout.add_widget(self.tower_selection_layout)
        
        # Bouton pour sauvegarder la sélection
        save_button = MDRaisedButton(text="Sauvegarder", on_release=self.save_deck)
        self.layout.add_widget(save_button)

    def is_tower_checked(self, tower_name):
        """Return if the given tower is checked in the JSON."""
        deck_store = JsonStore(os.path.join('db', 'tower_deck.json'))
        if not deck_store.exists('selected_towers'):
            return False
        selected_towers = deck_store.get('selected_towers').get('towers', [])
        return tower_name in selected_towers

class WorldScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))
        self.add_widget(layout)

        # Top bar for counters
        top_bar = MDBoxLayout(orientation='horizontal', size_hint=(.5, None), height=dp(50), spacing=dp(10))
        top_bar2 = GridLayout(rows=1, cols=3,spacing=dp(5), padding=[dp(5),dp(0),dp(5),dp(0)])
        layout.add_widget(top_bar)  # Assurez-vous de l'ajouter en premier pour qu'il soit en haut
        layout.add_widget(top_bar2)  # Assurez-vous de l'ajouter en premier pour qu'il soit en haut
        
        # Cristaux counter
        crystal_icon = MDIconButton(icon="diamond-stone", font_size=dp(24), text_color="blue", theme_text_color="Custom")
        self.cristaux_label = Label(text='0', font_size=dp(16), color=(0, 0, 0, 1))
        crystal_layout = BoxLayout(orientation='horizontal',  size_hint_x = .1)
        crystal_layout.add_widget(crystal_icon)
        crystal_layout.add_widget(self.cristaux_label)
        top_bar.add_widget(crystal_layout)

        # Stars counter
        star_icon = MDIconButton(icon="star", font_size=dp(24), text_color=(1, 0.84, 0, 1), theme_text_color="Custom")
        self.stars_label = Label(text='0', font_size=dp(16), color=(0, 0, 0, 1))
        star_layout = BoxLayout(orientation='horizontal', size_hint_x = .1)

        star_layout.add_widget(star_icon)
        star_layout.add_widget(self.stars_label)
        top_bar.add_widget(star_layout)

        tour_shop = MDFlatButton(text="Shop", size_hint_x = 1, text_color= "black", line_color= "black", on_release=self.open_tower_shop)
        top_bar2.add_widget(tour_shop)

        deck_button = MDFlatButton(text="Deck", on_release=self.open_deck, size_hint_x = 1, text_color= "black", line_color= "black")
        top_bar2.add_widget(deck_button)

        talents_button = MDFlatButton(text="Talents", size_hint_x = 1, text_color= "black", line_color= "black", on_release=self.open_talent)
        top_bar2.add_widget(talents_button)



        self.update_counters()

        # Get unique worlds
        worlds = list(set([niveau["world"] for niveau in niveaux]))
        worlds.sort()
        pos_worlds = [(dp(20), dp(60)),
                      (Window.width -dp(110), dp(100)),
                      (dp(20), dp(140)),
                      (Window.width -dp(110), dp(180)),
                      (dp(20), dp(220)),
                      (Window.width -dp(110), dp(260))]
        p=0

        self.worldscreen_widget = Widget()
        layout.add_widget(self.worldscreen_widget)
        for world in worlds:
            button = MDRaisedButton(text=world, on_release=partial(self.select_world, world), pos=pos_worlds[p])
            self.worldscreen_widget.add_widget(button)
            p+=1

    def on_enter(self, *args):
        self.update_cristaux_label()
        self.update_counters()

    def open_deck(self,instance):
        self.manager.current = 'deck'

    def open_talent(self,instance):
        self.manager.current = 'talent'

    def open_tower_shop(self,instance):
        self.manager.current = 'tower_shop'

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
        self.cristaux_label.text = str(cristal_count)

    def update_counters(self):
        # Update cristal count from JsonStore
        # (You might want to implement the logic for this if it's not already done)

        # Update stars count from JsonStore
        stars_store = JsonStore(os.path.join('db', 'stars.json'))
        total_stars = sum([stars_store.get(key)["stars"] for key in stars_store.keys()])

        self.stars_label.text = str(total_stars)

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print('init menu')
        self.world = None  # Initialisez l'attribut world


    def start_level(self, niveau):
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
        layout = MDBoxLayout(orientation='vertical', padding=dp(20))
        
        # Load progress from JSON store
        progress_store = JsonStore(os.path.join('db', 'progress.json'))
        stars_store = JsonStore(os.path.join('db', 'stars.json'))  # Load stars from JSON store
        
        # Determine the highest completed level
        completed_levels = [int(key) for key, value in progress_store.find(completed=True)]
        highest_completed_level = max(completed_levels, default=0)

        for niveau in [n for n in niveaux if n["world"] == self.world]:
            level_id = niveau["level"]
            button_text = "Niveau " + str(level_id)
            
            # Create a horizontal layout for each level
            level_layout = BoxLayout(orientation='horizontal', spacing=dp(10), height=dp(20))

            if level_id <= highest_completed_level:
                button = MDRaisedButton(text=button_text)
                button.on_release = partial(self.start_level, niveau)
            elif level_id == highest_completed_level + 1:
                button = MDRaisedButton(text=button_text)
                button.on_release = partial(self.start_level, niveau)
            else:
                button = MDRaisedButton(text=button_text, disabled=True)  # Disable levels not yet unlocked
            
            level_layout.add_widget(button)

            # Determine how many stars were earned for this level
            stars_earned = 0
            if stars_store.exists(str(level_id)):
                stars_earned = stars_store.get(str(level_id))["stars"]
            
            # Add three stars to the level layout and color them based on stars_earned
            for i in range(3):
                if i < stars_earned:
                    star = MDIconButton(icon="star", font_size=dp(20), text_color=(1, 0.84, 0, 1), theme_text_color="Custom")  # Gold star
                else:
                    star = MDIconButton(icon="star", font_size=dp(20), theme_text_color="Secondary", opacity = .5)  # Grey star
                level_layout.add_widget(star)

            layout.add_widget(level_layout)

        # Create a horizontal layout for back
        back_layout = BoxLayout(orientation='horizontal', spacing=dp(10), height=dp(20))
        # Back button
        back_button = MDRaisedButton(text="Retour", on_release=self.return_to_world_selection)


        back_layout.add_widget(back_button)

        self.add_widget(layout)
        layout.add_widget(back_layout)



    # Nouvelle méthode pour retourner à l'écran de sélection de monde
    def return_to_world_selection(self, instance):
        self.manager.current = 'worlds'

class TowerShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        
        main_layout = BoxLayout(orientation='vertical')
        
        # Afficher le compteur de cristaux en haut
        self.cristaux_label = Label(text=self.get_cristaux_str(), font_size=dp(16), size_hint_y=None, height=dp(50),  color="black")
        main_layout.add_widget(self.cristaux_label)


        # Création du ScrollView et du GridLayout pour les tours
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        layout = GridLayout(cols=4, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        scroll_view.add_widget(layout)
        main_layout.add_widget(scroll_view)

        from reglages_tours import tours
        img_directory = "tower_images/"
        from kivy.uix.image import Image

        for tower in tours:
            tower_card = MDCard(size_hint=(.2, None), height=dp(150), style="outlined", line_color=(0.2, 0.2, 0.2, 1), padding = [dp(0),dp(5),dp(0),dp(5)], spacing=dp(5), elevation=3)
            tower_layout = BoxLayout(orientation='vertical')
            
            # Image de la tour
            tower_image_source = os.path.join(img_directory, f"tower_{tower['nom']}.png")
            tower_image = Image(source=tower_image_source, size_hint=(.85, .85),pos_hint= {'center_x': .5, 'center_y': .5})
            tower_layout.add_widget(tower_image)
            
            tower_info_layout = MDBoxLayout(orientation='vertical', pos_hint= {'center_x': .5, 'center_y': .5}, spacing=dp(2),adaptive_size=True)
            if tower["nom"] == "Basique":  # Si la tour n'a pas été achetée, on passe à la suivante
                continue
            tower_name = tower["nom"]
            tower_cost = tower["cristal_cost"]
            
            # Chaque tour aura trois éléments: nom, coût et bouton d'achat.
            tower_label = MDLabel(text=tower_name, valign='middle', halign='center', color="black", pos_hint= {'center_x': .5, 'center_y': .5},
                                font_size=sp(8))

            info_button = MDIconButton(icon="information-variant-circle-outline", icon_size= "18sp", on_release=partial(self.show_tower_info, tower), size_hint_y=None, height=dp(20), pos_hint= {'center_x': .5, 'center_y': .5})
            

            if self.is_tower_bought(tower_name):
                buy_button = MDLabel(text="")
            else:
                buy_button = MDFillRoundFlatIconButton(icon="diamond-stone", icon_size= "12sp", font_size= "12sp", text=str(tower_cost), on_release=partial(self.buy_tower, tower_name, tower_cost),height=dp(20), pos_hint= {'center_x': .5, 'center_y': .5})
                #buy_button = MDRaisedButton(text=str(tower_cost), on_release=partial(self.buy_tower, tower_name, tower_cost),height=dp(20), pos_hint= {'center_x': .5, 'center_y': .5})
                
            
            tower_layout.add_widget(tower_label)

            tower_info_layout.add_widget(info_button)
            tower_info_layout.add_widget(buy_button)

            tower_layout.add_widget(tower_info_layout)
            tower_card.add_widget(tower_layout)
            layout.add_widget(tower_card)

        

        self.add_widget(main_layout)

        # Bouton de retour
        back_button = MDRaisedButton(text="Retour", on_release=self.return_to_main_menu, size_hint_y=None, height=dp(50))
        main_layout.add_widget(back_button)

    def return_to_main_menu(self, instance):
        self.manager.current = 'worlds'  # Remplacez 'nom_de_l_ecran_principal' par le nom de votre écran principal

    def buy_tower(self, tower_name, tower_cost, instance):
        available_cristaux = self.get_cristaux()

        if available_cristaux >= tower_cost:
            # Mise à jour du compteur de cristaux
            new_cristaux_count = available_cristaux - tower_cost
            store_cristaux = JsonStore(os.path.join('db', 'cristaux.json'))
            store_cristaux.put('count', value=new_cristaux_count)
            self.update_cristaux_label()  # met à jour l'affichage du compteur

            # Enregistrement de la tour achetée
            store_towers = JsonStore(os.path.join('db', 'tower_buy.json'))
            store_towers.put(tower_name, bought=True)

            # (Optionnel) Affichage d'une notification à l'utilisateur
            popup = Popup(title='Succès', content=Label(text=f"Tour achetée : \n\n {tower_name}!"), size_hint=(0.6, 0.4), on_dismiss=partial(self.update_buy_button, tower_name, instance))
            popup.open()
        else:
            # Affichage d'une erreur si l'utilisateur n'a pas assez de cristaux
            popup = Popup(title='Erreur', content=Label(text="Vous n'avez pas assez de cristaux!"), size_hint=(0.9, 0.3))
            popup.open()

    def get_cristaux_str(self):
        # Supposons que vous ayez une fonction pour obtenir le nombre de cristaux actuels de l'utilisateur.
        # Je vais l'ajouter ici comme une simulation.
        store = JsonStore(os.path.join('db', 'cristaux.json'))
        if not store.exists('count'):
            store.put('count', value=0)
        cristal_count = store.get('count')['value']
        return f"Cristaux : {cristal_count}"
    
    def get_cristaux(self):
        store = JsonStore(os.path.join('db', 'cristaux.json'))
        if not store.exists('count'):
            store.put('count', value=0)
        return store.get('count')['value']

    def show_tower_info(self, tower, instance):
        # Création du contenu du popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"Nom : {tower['nom']}"))
        content.add_widget(Label(text=f"Coût en cristaux : {tower['cristal_cost']}"))
        content.add_widget(Label(text=f"Degats phisiques : {tower['degats_physiques']}"))
        content.add_widget(Label(text=f"Degats magiques : {tower['degats_magiques']}"))
        content.add_widget(Label(text=f"Temps_entre_attaque : {tower['temps_entre_attaque']}"))
        content.add_widget(Label(text=f"Range : {tower['range']}"))
        content.add_widget(Label(text=f"Cout pièces : {tower['cost']}"))

        # Bouton pour fermer le popup
        close_button = MDRaisedButton(text="Fermer", size_hint_y=None, height=dp(50))
        content.add_widget(close_button)

        popup = Popup(title="Informations sur la tour", content=content, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)  # fermer le popup lorsque le bouton est cliqué

        popup.open()

    def update_cristaux_label(self):
        cristal_count = self.get_cristaux()
        self.cristaux_label.text = f"Cristaux : {cristal_count}"

    def is_tower_bought(self, tower_name):
        store_towers = JsonStore(os.path.join('db', 'tower_buy.json'))
        return store_towers.exists(tower_name)

    def update_buy_button(self, tower_name, instance, *args):
        if self.is_tower_bought(tower_name):
            instance.parent.remove_widget(instance)

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
        sm.add_widget(TowerShopScreen(name='tower_shop'))
        sm.add_widget(DeckScreen(name='deck'))
        sm.add_widget(TalentScreen(name="talent"))

        self.scheduled_functions = []
        self.active_monsters = []

        self.game_over_popup_shown = False
        self.game_win_popup_shown = False
        return sm


if __name__ == '__main__':
    MenuApp().run()
