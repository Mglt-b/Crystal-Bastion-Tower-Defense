
# reglage_monstres.py
from kivy.metrics import dp, sp


monstre_configurations = {
    "normal": {
        "name": "Normal",
        "image": "monstre_normal.png",
        "size": (dp(35), dp(35)),
        "speed": 8,
        "health": 100,
        "armure": 20,
        "magique_resistance": 10, 
        "coin": 10,
        "rotation_behavior": "fixed",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "normal"  # nouvel attribut
    },
    "rapide": {
        "name": "Rapide",
        "image": "monstre_rapide.png",
        "size": (dp(25), dp(25)),
        "speed": 12,
        "health": 50,
        "armure": 5,
        "magique_resistance": 0, 
        "coin": 10,
        "rotation_behavior": "fixed",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "normal"  # nouvel attribut
    },
    "tank": {
        "name": "Tank",
        "image": "monstre_tank.png",
        "size": (dp(50), dp(50)),
        "speed": 4,
        "health": 500,
        "armure": 100,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "fixed",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "normal"  # nouvel attribut
    },
    "ghost": {
        "name": "Ghost",
        "image": "monstre_Ghost.png",
        "size": (dp(30), dp(30)),
        "speed": 10,
        "health": 200,
        "armure": 1000000000000000000000000,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "path_direction",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "dark"  # nouvel attribut
    },
    "fire": {
        "name": "Fire",
        "image": "monstre_Fire.png",
        "size": (dp(30), dp(30)),
        "speed": 10,
        "health": 100,
        "armure": 0,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "path_direction",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "fire"  # nouvel attribut
    },
    "ice": {
        "name": "Ice",
        "image": "monstre_Ice.png",
        "size": (dp(30), dp(30)),
        "speed": 10,
        "health": 200,
        "armure": 0,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "path_direction",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "ice"  # nouvel attribut
    },
    "stone": {
        "name": "Stone",
        "image": "monstre_Stone.png",
        "size": (dp(30), dp(30)),
        "speed": 4,
        "health": 500,
        "armure": 1000000000000000000,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "path_direction",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "normal"  # nouvel attribut
    },
    "meca": {
        "name": "Meca",
        "image": "monstre_Meca.png",
        "size": (dp(30), dp(30)),
        "speed": 10,
        "health": 50,
        "armure": 100,
        "magique_resistance": 0, 
        "coin": 50,
        "rotation_behavior": "path_direction",  # Nouveau champ (peut être "fixed", "path_direction", etc.)
        "element": "normal"  # nouvel attribut
    },
    # Ajoutez d'autres types de monstres ici...
}
