from kivy.metrics import dp
img_directory = "tower_images/"

tours = [
    {
        "nom": "Basique",
        "degats_physiques": 15,
        "degats_magiques": 0,
        "temps_entre_attaque": .7,  # en secondes
        "taille": (dp(50), dp(50)),  # Largeur x Hauteur
        "couleur": [1, 0.5, 0.5, 1],
        "range": dp(115),
        "projectile_color": [1, 0.5, 0.5, 1],
        'cost': 50,
        'cristal_cost':30,
        'extra_effect': ""
    },
    {
        "nom": "Magique",
        "degats_physiques": 0,
        "degats_magiques": 20,
        "temps_entre_attaque": 1,
        "taille": (dp(50), dp(50)),
        "couleur": [0, 0, 1, 1],  # Bleu
        "range": dp(100),
        "projectile_color": [0, 0, 1, 1],  # Bleu
        'cost': 50,
        'cristal_cost':50,
        'extra_effect': ""  
    },
    {
        "nom": "Rapide",
        "degats_physiques": 5,
        "degats_magiques": 0,
        "temps_entre_attaque": .5,
        "taille": (dp(50), dp(50)),
        "couleur": [0, 1, 0, 1],  # Vert
        "range": dp(100),
        "projectile_color": [0, 1, 0, 1],  # Vert
        'cost': 50,
        'cristal_cost':50,
        'extra_effect': ""   
    },
    {
        "nom": "Ice",
        "degats_physiques": 0,  # ou un autre nombre approprié
        "degats_magiques": 5,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':500,
        'extra_effect': "Snare"
    },
    ##############################################################
    {
        "nom": "Fire",
        "degats_physiques": 0,  # ou un autre nombre approprié
        "degats_magiques": 5,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1], 
        "range": dp(100),
        "projectile_color": [0.5, 0.5, 1, 1],
        'cost': 40,
        'cristal_cost':0,
        'extra_effect': "Burn dot"
    },
    {
        "nom": "Elec",
        "degats_physiques": 0,  # ou un autre nombre approprié
        "degats_magiques": 5,
        "temps_entre_attaque": 3,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 20,
        'cristal_cost':0,
        'extra_effect': "Roots"
    },
    {
        "nom": "Bomb",
        "degats_physiques": 0,  # ou un autre nombre approprié
        "degats_magiques": 0,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':0,
        'extra_effect': "Bomb"  
    },
    {
        "nom": "test2",
        "degats_physiques": 5,  # ou un autre nombre approprié
        "degats_magiques": 0,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':500,
        'extra_effect': ""  
    },
    {
        "nom": "test2",
        "degats_physiques": 5,  # ou un autre nombre approprié
        "degats_magiques": 0,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':500,
        'extra_effect': ""  
    },
    {
        "nom": "test2",
        "degats_physiques": 5,  # ou un autre nombre approprié
        "degats_magiques": 0,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':500,
        'extra_effect': ""  
    },
    {
        "nom": "test2",
        "degats_physiques": 5,  # ou un autre nombre approprié
        "degats_magiques": 0,
        "temps_entre_attaque": 1,  # ou un autre nombre approprié
        "taille": (dp(50), dp(50)),
        "couleur": [0.5, 0.5, 1, 1],  # Bleu clair
        "range": dp(100),  # ou un autre nombre approprié
        "projectile_color": [0.5, 0.5, 1, 1],  # Bleu clair
        'cost': 60,
        'cristal_cost':500,
        'extra_effect': ""  
    }
    # Ajoutez d'autres configurations de tours ici si nécessaire
]

# Créer un dictionnaire pour un accès facile par nom
tour_dict = {tour["nom"]: tour for tour in tours}
tours_info = {tour["nom"]: tour for tour in tours}
