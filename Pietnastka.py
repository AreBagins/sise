import heapq
import sys
from collections import deque
import time

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

def make_move(state, index, move):
    move_offset = DIRECTIONS[move]
    new_index = index + move_offset
    new_state = list(state)
    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
    return tuple(new_state)

def dfs(state, goal_state, width, height, move_order, depth_limit, path, visited, current_depth, counters):
    # Update the maximum recursion depth reached
    if current_depth > counters["max_depth"]:
        counters["max_depth"] = current_depth

    # Count this state as processed
    counters["states_processed"] += 1

    if state == goal_state:
        return path
    if depth_limit == 0:
        return 0
    for move in move_order:
        if is_valid_move(state.index(0), move, width, height):
            new_state = make_move(state, state.index(0), move)
            if new_state not in visited:
                visited.add(new_state)
                result = dfs(new_state, goal_state, width, height, move_order,
                             depth_limit - 1, path + [move], visited,
                             current_depth + 1, counters)
                if result != 0:
                    return result
                visited.remove(new_state)
    return 0

def solve_puzzle_bfs(initial_state, goal_state, width, height, move_order):
    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(initial_state)
    states_processed = 0
    max_depth = 0

    while queue:
        state, path = queue.popleft()
        states_processed += 1
        max_depth = max(max_depth, len(path))

        # if states_processed % 1000 == 0:
            # print(f"Przetworzono {states_processed} stanów...")

        if state == goal_state:
            return path, len(visited), states_processed, max_depth

        zero_index = state.index(0)

        for move in move_order:
            if is_valid_move(zero_index, move, width, height):
                new_state = make_move(state, zero_index, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [move]))

    return None, len(visited), states_processed, max_depth

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

def solve_puzzle_a_star(initial_state, goal_state, width, height, move_order, strategy):
    open_list = []
    if strategy == "hamm":
        heapq.heappush(open_list, (hamming_distance(initial_state, goal_state), 0, initial_state, []))
    elif strategy == "manh":
        heapq.heappush(open_list, (manhattan_distance(initial_state, goal_state, width), 0, initial_state, []))
                                            # (f(n), g(n), stan, ścieżka)
    visited = set()
    visited.add(tuple(initial_state))
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
            return path, len(visited), states_processed, max_depth

        zero_index = state.index(0)

        # Sprawdzenie wszystkich możliwych ruchów
        for move in move_order:
            if is_valid_move(zero_index, move, width, height):
                new_state = make_move(state, zero_index, move)
                if new_state not in visited:
                    visited.add(new_state)
                    if strategy == "hamm":
                        f_cost = g + 1 + hamming_distance(new_state, goal_state)  # f(n) = g(n) + h(n)
                    else:
                        f_cost = g + 1 + manhattan_distance(new_state, goal_state, width)
                    heapq.heappush(open_list, (f_cost, g + 1, new_state, path + [move]))

    return None, len(visited), states_processed, max_depth

def hamming_distance(state, goal_state):
    return sum(1 for i in range(len(state)) if state[i] != goal_state[i] and state[i] != 0)

def start_bfs(option, input_data, width, height, goal_state):
    start_time = time.time()
    solution, visited_count, processed_count, max_depth = solve_puzzle_bfs(tuple(input_data), goal_state, width, height, option)
    duration = time.time() - start_time
    return solution, visited_count, processed_count, max_depth, duration

def start_dfs(option, input_data, width, height, goal_state):
    counters = {"max_depth": 0, "states_processed": 0}
    visited = set()
    visited.add(tuple(input_data))
    start_time = time.time()
    sol = dfs(input_data, goal_state, width, height, option, 20, [], visited, 1, counters)
    duration = time.time() - start_time
    return sol, counters["states_processed"], counters["states_processed"], counters["max_depth"], duration

def start_astr(option, inputData, width, height, goal_state):

    if option != "manh" and option != "hamm":
        print(f"error, {option} is not an option for aStar")
        return
    start_time = time.time()
    solution, visited_count, processed_count, max_depth = solve_puzzle_a_star(inputData,goal_state,width,height, "LURD", option)
    duration = time.time() - start_time
    return solution, visited_count, processed_count, max_depth, duration

def main():
    strategy = sys.argv[1]
    option = sys.argv[2]
    inputFile = sys.argv[3]
    solutionFile = sys.argv[4]
    statsFile = sys.argv[5]

    with open(inputFile) as f:
        width, height = [int(x) for x in next(f).split()]
        inputData = []
        for line in f:
            for c in line.split():
                inputData.append(int(c))
    DIRECTIONS['U'] = -width
    DIRECTIONS['D'] = width
    goal_state = tuple(range(1, width*height)) + (0,)
    match strategy:
        case "bfs":
            sol, vc, pc, md, dr = start_bfs(option, inputData, width, height, goal_state)
        case "dfs":
            sol, vc, pc, md, dr = start_dfs(option, inputData, width, height, goal_state)
            if sol == 0: sol = None
        case "astr":
            sol, vc, pc, md, dr = start_astr(option, inputData, width, height, goal_state)
    if sol is not None:
        solution_length = len(sol)
    else:
        solution_length = -1

    with open(solutionFile, 'w') as s:
        s.write(str(solution_length))
        if solution_length != -1:
            s.write("\n")
            for i in sol:
                s.write(i)

    with open(statsFile, 'w') as s:
        s.write(str(solution_length))
        s.write("\n")
        s.write(str(vc))
        s.write("\n")
        s.write(str(pc))
        s.write("\n")
        s.write(str(md))
        s.write("\n")
        s.write(str(dr))

DIRECTIONS = {'L': -1, 'R': 1, 'U': None, 'D': None}
main()