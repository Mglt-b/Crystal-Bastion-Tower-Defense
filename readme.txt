C'est un jeu de tower defense, developpé en python avec kivy/kivymd.
Il est destiné a un affichage vertical pour smartphone Android, sa taille doit etre adaptative.

Le jeu se lance via main.py : il permet de :
-Selectionner un monde 'world'.
    Chaque monde contient ses niveaux, définis dans "niveau.py" . A coté de chaque niveau, 3 étoiles grises qui deviennent de couleur
    "or" une fois certaines conditions de fin de niveau réussies, l'information est stockée dans "/db/stars.json".
-Acceder au shop de "tours".
    chaque tour dans reglages_tours.py est achetable et l'information est stockée dans "/db/tower_buy.json"
-Visualiser le compteur de cristaux "/db/cristaux.json"
-Visualiser le compteur d'étoiles "/db/stars.json"


Lors de la selection d'un niveau selectionné, jeu.py est appelé.

Une interface graphique s'affiche, MainLayout() composée de deux classes :
- MapZone() ou le chemmin et les monstres vont apparaitre, ainsi que le compteur de pièces, compteur des points de vie du joueur et compteur de monstres restant.
- TouSelectionZone() où l'utilisateur pourra selectionner des tours pour les Drag & Drop sur MapZone(). (uniquement les tours achetées stockées dans "/db/tower_buy.json")

Le chemin(path) pour les monstres ainsi que le nombre de monstres est géré dans niveau.py.
 - Il existe aussi dans ce fichier une fonction de generation de path qui n'est pas utilisée.
 - Le décor est egalement configuré ici

Les tours vont attaquer les montres.
- Le codage des tours (Classe, attaque...) est géré dans tours.py
- Les caractéristiques de chaque tours est défini dans reglages_tours.py
- le dossier tower_images contient les images des tours
- Chaque tour peut etre amméliorée, ce qui augmente ses statistiques et change leur image, c'est géré par ameliorations_tours.py

Les tours vont lancer des projectiles sur les monstres
- Le codage des projectiles (Classe, deplacement, image, ..) est géré dans projectiles.py

Le codage des montres (Classe, deplacement...) est géré dans monstres.py :
- Les caractéristiques de chaque monstre et leur images sont définis dans reglage_monstres.py
- le dossier "/montres_images/" contient les images des monstres
- Les conditions d'obtention d'étoiles en fin de niveau
- Le jeu se termine quand :
    - Gagné : le joueur a des points de vie >0 et tous les monstres montres
    - Perdu : le joueur n'a plus de point de vie <= 0



Les différentes tours :

#Chaque tour a son type élémentaire. Une tour attaquant un monstre de même élément n'inglige pas de dégats, sauf pour l'élément "normal".

    -Basique : Inflique uniquement des degats physiques.
               Dégats : moyen
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : 0

    -Magique : Inflique uniquement des degats magiques.
               Dégats : moyen
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : 0

    -Rapide : Inflique uniquement des degats phisiques.
               Dégats : moyen
               Target : monocible
               Portée : courte
               Cadence : rapide
               Effet : 0

    - Ice : Inflige des degats magiques, et ralentit la cible.
               Dégats : faible
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : snare

    - Fire : Inflige des degats magiques, et enflamme la cible.
               Dégats : faible
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : dot (degats magiques over time) 

    - Elec : Inflige des degats magiques, et immobilise la cible.
               Dégats : faible
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : root

    - Bomb : Pose une bombe sur la cible..
               Dégats : 0
               Target : monocible
               Portée : moyenne
               Cadence : moyenne
               Effet : explose après quelques secondes et inflige des degats a tous les enemis dans la zone.      