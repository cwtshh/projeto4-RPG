import random

def generate_map(width, height, wall_percentage):
    map = [[0 for _ in range(width)] for _ in range(height)]
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() < wall_percentage:
                map[y][x] = 395
    
    for y in range(height):
        map[y][0] = 395
        map[y][width - 1] = 395
    
    for x in range(width):
        map[0][x] = 395
        map[height - 1][x] = 395
    
    start_x = random.randint(2, width - 3)
    start_y = random.randint(2, height - 3)
    map[start_y][start_x] = "P"
    
    return map

def print_map(map):
    for row in map:
        print(' '.join(str(cell).rjust(3) if cell != "P" else " P " for cell in row))

width = 12
height = 12
wall_percentage = 0.1

game_map = generate_map(width, height, wall_percentage)
print_map(game_map)
