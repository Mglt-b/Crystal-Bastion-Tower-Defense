C'est un jeu de tower defense, developpé en python avec kivy/kivymd.
Il est destiné a un affichage vertical pour smartphone Android, sa taille doit etre adaptative.

Le jeu se lance via main.py : il permet de selectionner un niveau

Une fois le niveau selectionné, jeu.py est appelé.

Une interface graphique s'affiche, MainLayout() composée de deux classes :
- MapZone() ou le chemmin et les monstres vont apparaitre, ainsi que le compteur de pièces et les points de vie du joueur.
- TouSelectionZone() ou l'utilisateur pourra selectionner des tours pour les Drag & Drop sur MapZone().

Le chemin(path) pour les monstres ainsi que le nombre de monstres est géré dans niveau.py.
 - Il existe aussi dans ce fichier une fonction de generation de path qui n'est pas utilisée.
 - Le décor est egalement configuré ici

Les tours vont attaquer les montres.
- Le codage des tours (Classe, attaque...) est géré dans tours.py
- Les caractéristiques de chaque tours est défini dans reglages_tours.py
- le dossier tower_images contient les images des tours
- Chaque tour peut etre amméliorée, ce qui augmente ses statistiques, c'est géré par ameliorations_tours.py

Les tours vont lancer des projectiles sur les monstres
- Le codage des projectiles (Classe, deplacement...) est géré dans projectiles.py

Le codage des montres (Classe, deplacement...) est géré dans monstres.py
- Les caractéristiques de chaque monstre est défini dans reglage_monstres.py
- le dossier montres_images contient les images des monstres

Le jeu se termine quand :
    - Gagné : le joueur a des points de vie >0 et tous les monstres montres
    - Perdu : le joueur n'a plus de point de vie <= 0


Quelques prompts generation images tours :

"Schéma d'une tour de défense magique avec des runes, vue du dessus, sans contour"


##### CHATGPT Tu peux commencer cette section pour ajouter des notes que je te renverrais a chaque fois
..
..
..
FIN DE SECTION #########


TO DO:
 - 