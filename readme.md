# 🏰 Tower Defense Game

This tower defense game is developed in Python using the Kivy/KivyMD framework, designed specifically for vertical display on Android smartphones. 
The game's layout adapts to different screen sizes, ensuring a seamless mobile gaming experience.

Kivy : https://github.com/kivy/kivy
KivyMD : https://github.com/kivymd/KivyMD

## 📱 Designed for Vertical Display on Android Smartphones

The layout adapts to various screen sizes for a seamless gaming experience on mobile devices.

## 🚀 Getting Started

Launch the game by running `main.py`. Here's what you can do:

### Select a World (`world`) 🌍
- Each world contains its levels, defined in `niveau.py`.
- Next to each level, there are 3 gray stars that turn "gold" once certain level completion conditions are met. The information is stored in `/db/stars.json`.

### Access the Tower Shop 🛒
- Each tower in `reglages_tours.py` can be purchased, with information stored in `/db/tower_buy.json`.

### View the Crystal Counter 💎
- Crystals are displayed via `/db/cristaux.json`.

### View the Star Counter ⭐
- Stars are shown through `/db/stars.json`.

## 🎮 Gameplay Interface

When a level is selected, `jeu.py` is called, showcasing the graphical user interface, `MainLayout()`, which consists of two classes:

- **MapZone()**: Displays the path and monsters, alongside the coin counter, player's health points counter, and remaining monsters counter.
- **TouSelectionZone()**: Allows users to select and drag & drop towers onto `MapZone()` (only the towers purchased and stored in `/db/tower_buy.json`).

## 🏹 Towers and Monsters

Towers attack monsters, with their coding (Class, attack...) managed in `tours.py` and characteristics defined in `reglages_tours.py`. Each tower can be upgraded, enhancing its stats and changing its image, as managed by `ameliorations_tours.py`.

- The `tower_images` folder contains images of the towers.
- Projectiles' coding (Class, movement, image, etc.) is managed in `projectiles.py`.
- Monsters' coding (Class, movement...) is handled in `monstres.py`, with their characteristics and images defined in `reglage_monstres.py` and stored in the `/montres_images/` folder.

## 🌟 Game Outcome

- **Won**: The game ends successfully when the player has health points > 0 and all monsters are defeated.
- **Lost**: The game ends in a loss if the player's health points are <= 0.

## 🔥 Different Towers

Each tower has its elemental type. A tower attacking a monster of the same element inflicts no damage, except for the "normal" element. The towers include:

- **Basic**: Inflicts physical damage.
- **Magic**: Inflicts magical damage.
- **Rapid**: A faster tower that inflicts physical damage.
- **Ice**: Slows the target with magical damage.
- **Fire**: Ignites the target, causing damage over time.
- **Elec**: Immobilizes the target with magical damage.
- **Bomb**: Places a bomb on the target, exploding after a few seconds to damage all enemies in the area.

Each tower has detailed attributes such as Damage, Target, Range, Rate, and Effect.
