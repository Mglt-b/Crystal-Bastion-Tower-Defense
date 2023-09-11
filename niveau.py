import random

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

path_level_1 = [(0.0, 0.6), (0.125, 0.6), (0.125, 0.725), (0.25, 0.725), (0.25, 0.6), (0.375, 0.6), 
                (0.375, 0.475), (0.5, 0.475), (0.5, 0.35), (0.475, 0.35), (0.25, 0.35), (0.25, 0.475), 
                (0.125, 0.475), (0.125, 0.21), (0.9, 0.21), (0.9, 0.5), (0.7, 0.5), (0.7, 0.6),
                (0.9, 0.6), (0.9, 0.9), (0, 0.9)]


path_level_2 = [(0.0, 0.6), (0.125, 0.6), (0, 0.9)]


niveaux = [
    {
        "path": path_level_1,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
        ]
    },
    {
        "path": path_level_2,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
        ]
    },
    {
        "path": path_level_2,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
        ]
    },
    {
        "path": path_level_2,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
        ]
    },
    {
        "path": path_level_2,
        "monsters": [
            {"type": "normal", "count": 10},
            {"type": "rapide", "count": 12}
        ]
    },
    # ... Ajoutez d'autres niveaux ici
]
