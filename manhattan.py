from collections import deque
import heapq
import time

# Możliwe ruchy pustego pola
DIRECTIONS = {
    'L': -1,
    'R': 1,
    'U': None,  # wartość zostanie ustawiona dynamicznie
    'D': None
}

# Obliczanie metryki Manhattana
def manhattan_distance(state, goal_state, width):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:  # Pomijamy pustą kratkę
            goal_index = goal_state.index(state[i])
            # Obliczamy współrzędne w układzie 2D
            current_x, current_y = divmod(i, width)
            goal_x, goal_y = divmod(goal_index, width)
            distance += abs(current_x - goal_x) + abs(current_y - goal_y)
    return distance

def is_valid_move(index, move, width, height):
    if move == 'L' and index % width == 0:
        return False
    if move == 'R' and index % width == width - 1:
        return False
    if move == 'U' and index < width:
        return False
    if move == 'D' and index >= width * (height - 1):
        return False
    return True

def make_move(state, index, move, width, height):
    move_offset = DIRECTIONS[move]
    new_index = index + move_offset
    new_state = list(state)
    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
    return tuple(new_state)

def solve_puzzle_a_star(initial_state, goal_state, width, height, move_order):
    # Ustawienie dynamiczne dla dowolnej szerokości
    DIRECTIONS['U'] = -width
    DIRECTIONS['D'] = width

    start_time = time.time()
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(initial_state, goal_state, width), 0, initial_state, []))  # (f(n), g(n), stan, ścieżka)
    visited = set()
    visited.add(initial_state)
    states_processed = 0
    max_depth = 0

    while open_list:
        f, g, state, path = heapq.heappop(open_list)
        states_processed += 1
        max_depth = max(max_depth, len(path))

        # Co 1000 stanów wypisz postęp
        if states_processed % 1000 == 0:
            print(f"Przetworzono {states_processed} stanów...")

        # Sprawdzenie, czy dotarliśmy do rozwiązania
        if state == goal_state:
            duration = time.time() - start_time
            return path, len(visited), states_processed, max_depth, duration

        zero_index = state.index(0)

        # Sprawdzenie wszystkich możliwych ruchów
        for move in move_order:
            if is_valid_move(zero_index, move, width, height):
                new_state = make_move(state, zero_index, move, width, height)
                if new_state not in visited:
                    visited.add(new_state)
                    f_cost = g + 1 + manhattan_distance(new_state, goal_state, width)  # f(n) = g(n) + h(n)
                    heapq.heappush(open_list, (f_cost, g + 1, new_state, path + [move]))

    return None, len(visited), states_processed, max_depth, time.time() - start_time

# Przykładowe użycie
initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 15, 13, 14)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
width, height = 4, 4
move_order = "RDUL"  # Można dostosować kolejność ruchów

# Uruchomienie algorytmu A* z metryką Manhattana
solution, visited_count, processed_count, max_depth, duration = solve_puzzle_a_star(initial_state, goal_state, width,
                                                                                   height, move_order)

# Wyniki
print("Solution:", solution)
print("Length of solution:", len(solution) if solution else 0)
print("Visited states:", visited_count)
print("Processed states:", processed_count)
print("Max depth:", max_depth)
print("Execution time (s):", duration)
