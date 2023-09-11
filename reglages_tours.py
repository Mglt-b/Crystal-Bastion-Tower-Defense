from kivy.metrics import dp
img_directory = "tower_images/"
from kivy.metrics import dp

tours = [
    {
        "nom": "Basique2",
        "degats_physiques": 10,
        "degats_magiques": 0,
        "temps_entre_attaque": 1.5,  # en secondes
        "taille": (dp(50), dp(50)),  # Largeur x Hauteur
        "couleur": [1, 0.5, 0.5, 1],
        "range": 100,
        "projectile_color": [1, 0.5, 0.5, 1],
        'cost': 50
    },
    {
        "nom": "Magique2",
        "degats_physiques": 5,
        "degats_magiques": 20,
        "temps_entre_attaque": 2,
        "taille": (dp(50), dp(50)),
        "couleur": [0, 0, 1, 1],  # Bleu
        "range": 50,
        "projectile_color": [0, 0, 1, 1],  # Bleu
        'cost': 50
    },
    {
        "nom": "Rapide",
        "degats_physiques": 5,
        "degats_magiques": 0,
        "temps_entre_attaque": 1,
        "taille": (dp(25), dp(25)),
        "couleur": [0, 1, 0, 1],  # Vert
        "range": 70,
        "projectile_color": [0, 1, 0, 1],  # Vert
        'cost': 50
    }
    # Ajoutez d'autres configurations de tours ici si nécessaire
]

# Créer un dictionnaire pour un accès facile par nom
tour_dict = {tour["nom"]: tour for tour in tours}
tours_info = {tour["nom"]: tour for tour in tours}
