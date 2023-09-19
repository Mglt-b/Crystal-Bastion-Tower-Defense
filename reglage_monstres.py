
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
        "coin": 20
    },
    "rapide": {
        "name": "Rapide",
        "image": "monstre_rapide.png",
        "size": (dp(25), dp(25)),
        "speed": 12,
        "health": 50,
        "armure": 5,
        "magique_resistance": 0, 
        "coin": 25
    },
    "tank": {
        "name": "Tank",
        "image": "monstre_tank.png",
        "size": (dp(50), dp(50)),
        "speed": 4,
        "health": 500,
        "armure": 50,
        "magique_resistance": 50, 
        "coin": 100
    },
    # Ajoutez d'autres types de monstres ici...
}
