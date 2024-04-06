🏰 Tower Defense Game
This is a tower defense game developed in Python using the Kivy/KivyMD framework. It's specifically designed for vertical display on Android smartphones, with an adaptive layout for various screen sizes.

Table of Contents
Introduction
Getting Started
Gameplay Interface
Towers and Monsters
Game Outcome
Different Towers
Introduction
📱 Designed for Vertical Display on Android Smartphones: The game's layout adapts to different screen sizes for a seamless mobile gaming experience.

Getting Started
🚀 Launch the game by running main.py. Here's what you can do:

Select a World (world) 🌍:

Each world contains its levels, defined in niveau.py.
Next to each level, there are 3 gray stars that turn "gold" once certain level completion conditions are met. The information is stored in /db/stars.json.
Access the Tower Shop 🛒:

Each tower in reglages_tours.py can be purchased, with information stored in /db/tower_buy.json.
View the Crystal Counter /db/cristaux.json 💎.

View the Star Counter /db/stars.json ⭐.

Gameplay Interface
🎮 When a level is selected, jeu.py is called, presenting the graphical user interface, MainLayout(), which consists of two classes:

MapZone(): Displays the path and monsters, along with the coin counter, player's health points counter, and remaining monsters counter.
TouSelectionZone(): Allows the user to select towers to drag and drop onto MapZone() (only the towers purchased and stored in /db/tower_buy.json).
The path for monsters, as well as the number of monsters, are managed in niveau.py. The scenery is also configured here.

Towers and Monsters
🏹 Towers attack monsters:

The coding of towers (Class, attack...) is managed in tours.py.
The characteristics of each tower are defined in reglages_tours.py.
The tower_images folder contains images of the towers.
Each tower can be upgraded, enhancing its stats and changing its image, managed by ameliorations_tours.py.
Towers launch projectiles at monsters:

The coding of projectiles (Class, movement, image, etc.) is managed in projectiles.py.
The coding of monsters (Class, movement...) is managed in monstres.py:

The characteristics of each monster and their images are defined in reglage_monstres.py.
The /montres_images/ folder contains images of the monsters.
Game Outcome
🌟 The game ends when:

Won: The player has health points > 0 and all monsters are defeated.
Lost: The player's health points are <= 0.
Different Towers
🔥 Each tower has its elemental type. A tower attacking a monster of the same element inflicts no damage, except for the "normal" element.

Basic: Only inflicts physical damage.
Magic: Only inflicts magical damage.
Rapid: Only inflicts physical damage.
Ice: Inflicts magical damage and slows the target.
Fire: Inflicts magical damage and ignites the target.
Elec: Inflicts magical damage and immobilizes the target.
Bomb: Places a bomb on the target.