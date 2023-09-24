from kivy.metrics import dp
ameliorations = {

    "Magique": [
        {   
            "niveau": "1",
            "cout_amelioration": 50,
            "temps_entre_attaque": .8,
            "degats_physiques": 0,
            "range": dp(120),
            "color": [0.5, 0.5, 0.5, 1],
            "degats_magiques": 30,
        },
        {   
            "niveau": "2",
            "cout_amelioration": 100,
            "temps_entre_attaque": .6,
            "degats_physiques": 0,
            "range": dp(140),
            "color": [0.7, 0.5, 0.5, 1],
            "degats_magiques": 40,
        },
        # ... Plus de niveaux d'amélioration
    ],
    "Basique": [
        {   
            "niveau": "1",
            "cout_amelioration": 50,
            "temps_entre_attaque": .6,
            "degats_physiques": 20,
            "range": dp(125),
            "color": [0.5, 0.5, 0.5, 1],
            "degats_magiques": 0,
        },
        {   
            "niveau": "2",
            "cout_amelioration": 100,
            "temps_entre_attaque": 0.5,
            "degats_physiques": 30,
            "range": dp(135),
            "color": [0.7, 0.5, 0.5, 1],
            "degats_magiques": 0,
        },
        # ... Plus de niveaux d'amélioration
    ],
}
