from collections import deque
import time

# Możliwe ruchy pustego pola
DIRECTIONS = {
    'L': -1,
    'R': 1,
    'U': None,  # wartość zostanie ustawiona dynamicznie
    'D': None
}


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


def solve_puzzle_bfs(initial_state, goal_state, width, height, move_order):
    DIRECTIONS['U'] = -width  # Ustawienie dynamiczne dla dowolnej szerokości
    DIRECTIONS['D'] = width

    start_time = time.time()
    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(initial_state)
    states_processed = 0
    max_depth = 0

    while queue:
        state, path = queue.popleft()
        states_processed += 1
        max_depth = max(max_depth, len(path))

        if states_processed % 1000 == 0:
            print(f"Przetworzono {states_processed} stanów...")

        if state == goal_state:
            duration = time.time() - start_time
            return path, len(visited), states_processed, max_depth, duration

        zero_index = state.index(0)

        for move in move_order:
            if is_valid_move(zero_index, move, width, height):
                new_state = make_move(state, zero_index, move, width, height)
                if new_state not in visited:
                    print(f"Test: dodano nowy stan {new_state}")
                    visited.add(new_state)
                    queue.append((new_state, path + [move]))

    return None, len(visited), states_processed, max_depth, time.time() - start_time


# Przykładowe użycie
initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 15, 13, 14)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
width, height = 4, 4
move_order = "RDUL"

solution, visited_count, processed_count, max_depth, duration = solve_puzzle_bfs(initial_state, goal_state, width,
                                                                                 height, move_order)
print("Solution:", solution)
print("Length of solution:", len(solution) if solution else 0)
print("Visited states:", visited_count)
print("Processed states:", processed_count)
print("Max depth:", max_depth)
print("Execution time (s):", duration)
