import random
from kivy.metrics import dp, sp

def generate_random_path(grid_size, path_length, min_turns):
    """Generate a random path on a grid of given size."""
    print("Generating random path...")
    
    # Start position
    x, y = 0, int(0.5 * grid_size)
    path = [(x, y)]

    # directions: right, up, left, down
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    last_direction = None

    for _ in range(path_length - 1):
        valid_moves = []
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Ensure we remain within the grid and not in the bottom 20%
            if (0.01 * grid_size <= new_x < 0.99 * grid_size and 
                0.2 * grid_size <= new_y < 0.99 * grid_size and 
                (new_x, new_y) not in path):
                valid_moves.append((dx, dy))

        if valid_moves:
            # If last direction is available in valid moves, remove it to increase chances of turns
            if last_direction in valid_moves and len(valid_moves) > 1:
                valid_moves.remove(last_direction)
            
            dx, dy = random.choice(valid_moves)
            x, y = x + dx, y + dy
            path.append((x, y))
            last_direction = (dx, dy)
        else:
            break

    # Adjust path to ensure minimum turns
    turns = sum(1 for i in range(1, len(path)) if path[i-1] != path[i])
    while turns < min_turns and len(path) >= 3:
        # Choose a random point in the path
        idx = random.randint(1, len(path) - 2)
        dx, dy = random.choice(directions)
        
        new_x, new_y = path[idx][0] + dx, path[idx][1] + dy
        
        if (0.1 * grid_size <= new_x < 0.9 * grid_size and 
            0.1 * grid_size <= new_y < 0.8 * grid_size and 
            (new_x, new_y) not in path):
            path[idx] = (new_x, new_y)
            turns += 1
    
    if len(path) < 3:
        print("Generated path is too short. Trying again...")
        return generate_random_path(grid_size, path_length, min_turns)



    # Normalization
    path = [(x/grid_size, y/grid_size) for x, y in path]


    print(f"Generated path: {path}")
    return path
#random generate : generate_random_path(8, 100000, 5)

def reverse_path(path):
    return path[::-1]

types_decor = {
    "arbre": {"image": "decors_images/arbre_image_1.png", "size": (dp(20), dp(20))},
    "rocher": {"image": "decors_images/rocher_image_1.png", "size": (dp(20), dp(20))},
    "cristal": {"image": "decors_images/cristal_image.png", "size": (dp(30), dp(30))},
    # ... Ajoutez d'autres types de décor ici
}


path_level_1 = [(0.0, 0.6), (1, 0.6)]


path_level_2 = [(0.0, 0.8), (0.125, 0.8), (0.3, 0.8),
                (0.5, 0.8), (0.5, 0.6), (0.2, 0.6),
                (0.1, 0.4),(0.8, 0.4),
                (0.8, 1),
                (0, 1)] #fin

path_level_3 = [(0.50, 0.69), (0.1, 0.22), (0.1, 1), (0.4, 1), (0.81, 0.68), (0.38, 0.31), (1.00, 0.38)]

path_level_4 = [(0.01, 0.20), 
                (0.48, 0.69), (0.03, 0.69), 
                (0.48, 1), 
                (0.97, 0.69), (0.52, 0.69), 
                (1.00, 0.20)]

path_level_5 =[(0.27875, 0.69833333333333335), (0.27875, 0.8016666666666667), (0.125, 0.8016666666666667), (0.125, 0.228333333333333332), 
               (0.84, 0.228333333333333332), (0.84, 0.44333333333333335), (0.615, 0.44333333333333335), (0.615, 0.815), (0.94625, 0.815), 
               (0.94625, 1), (0.47375, 1), (0.47375, 0.8133333333333333), (0.36, 0.8133333333333333), (0.36, 0.9233333333333334)]


path_level_6 =[(0, 1), (0.875, 0.3), (1.0, 0.3), (1.0, 0.425), (0.875, 0.425), (0.75, 0.425),
                (0.75, 0.3), (0.625, 0.3), (0.5, 0.3), (0.375, 0.3), (0.25, 0.3), (0.25, 0.525),
                  (0.25, 0.55), (0.125, 0.55), (0.125, 0.425), (0.125, 0.3), (0.0, 0.3), (0.0, 0.425), (0.0, 0.55), (0.0, 0.675), (0.0, 0.6)]
 
path_level_7 =reverse_path(path_level_3)

path_level_8 =reverse_path(path_level_2)


path_level_10 = [(0.0, 0.6), (0.125, 0.6), (0.125, 0.725), (0.25, 0.725), (0.25, 0.6), (0.375, 0.6), 
                (0.375, 0.475), (0.5, 0.475), (0.5, 0.35), (0.475, 0.35), (0.25, 0.35), (0.25, 0.475), 
                (0.125, 0.475), (0.125, 0.21), (0.9, 0.21), (0.9, 0.5), (0.7, 0.5), (0.7, 0.6),
                (0.9, 0.6), (0.9, 0.9), 
                (0, 0.9)] #fin

niveaux = [
    {
        "world": "World 1",
        "level": 1,
        "path": path_level_1,
        "monsters": [
            {"type": "tank", "count": 1},
            {"type": "normal", "count": 1},
            {"type": "rapide", "count": 2},
            {"type": "normal", "count": 10},
            {"type": "tank", "count": 1},
            {"type": "rapide", "count": 12},
                    ],
        "decor": [{"type": "cristal","position": (0.3,0.5)}],
        "sol": [{"type": "decors_images/sols/futuriste_1.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 2,
        "path": path_level_2,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_2.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 3,
        "path": path_level_3,
        "monsters": [
            {"type": "tank", "count": 1},
            {"type": "normal", "count": 2},
            {"type": "rapide", "count": 10},
            {"type": "tank", "count": 1},
            {"type": "normal", "count": 2},
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_3.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 4,
        "path": path_level_4,
        "monsters": [
            {"type": "ghost", "count": 5}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_4.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 5,
        "path": path_level_5,
        "monsters": [
            {"type": "fire", "count": 10}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_5.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 6,
        "path": path_level_6,
        "monsters": [
            {"type": "ice", "count": 10}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_6.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 7,
        "path": path_level_7,
        "monsters": [
            {"type": "stone", "count": 10},
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_7.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 1",
        "level": 8,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 1},
            {"type": "rapide", "count": 1},
            {"type": "meca", "count": 10},       
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/futuriste_8.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    # World 2
    {
        "world": "World 2",
        "level": 9,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/foret_1.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 2",
        "level": 10,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/foret_2.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 2",
        "level": 11,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/foret_3.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    # World 3
    {
        "world": "World 3",
        "level": 12,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_1.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 13,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_2.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 14,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_3.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 15,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_4.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 16,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_5.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 17,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_6.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 18,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_7.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 3",
        "level": 19,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_8.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
    {
        "world": "World 4",
        "level": 20,
        "path": path_level_8,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
                    ],
        "decor": [],
        "sol": [{"type": "decors_images/sols/lave_2.png",
                "size": 1}],
        "chemin": [{"type": "decors_images/futur_sol.png"}],
    },
]



