from pathlib import Path
import heapq
import math
import sys


DEFAULT_INPUT = "3 13 7 8 9"


def parse_input(input_text):
    input_text = input_text.replace("\ufeff", "").strip()
    values = [int(value) for value in input_text.split()]
    if len(values) < 3:
        raise ValueError("Can nhap n, M va danh sach dung tich cac gao")
    n = values[0]
    target = values[1]
    capacities = values[2:]
    if len(capacities) != n:
        raise ValueError("So luong dung tich gao khong khop voi n")
    return n, target, capacities


def normalize_input_text(input_text):
    input_text = input_text.replace("\ufeff", "").strip()
    if not input_text:
        input_text = DEFAULT_INPUT
    return " ".join(input_text.split())


def has_possible_answer(target, capacities):
    return target % math.gcd(*capacities) == 0


def heuristic(state, target, capacities):
    _, tank_amount = state
    remaining = target - tank_amount
    if remaining <= 0:
        return 0
    return math.ceil(remaining / max(capacities))


def format_state(jug_amounts, tank_amount):
    jug_text = ", ".join(
        f"Gao {index + 1}: {amount} lit"
        for index, amount in enumerate(jug_amounts)
    )
    return f"({jug_text}, Be: {tank_amount} lit)"


def generate_neighbors(state, capacities, target):
    jug_amounts, tank_amount = state
    n = len(capacities)
    neighbors = []
    for i in range(n):
        if jug_amounts[i] < capacities[i]:
            new_jugs = list(jug_amounts)
            amount = capacities[i] - jug_amounts[i]
            new_jugs[i] = capacities[i]
            new_state = (tuple(new_jugs), tank_amount)
            action = (
                f"Chuyen/Muc {amount} lit nuoc tu bo song qua gao {i + 1} "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))
    for i in range(n):
        if jug_amounts[i] > 0 and tank_amount + jug_amounts[i] <= target:
            new_jugs = list(jug_amounts)
            amount = new_jugs[i]
            new_jugs[i] = 0
            new_tank = tank_amount + amount
            new_state = (tuple(new_jugs), new_tank)
            action = (
                f"Chuyen/Muc {amount} lit nuoc tu gao {i + 1} qua be "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if jug_amounts[i] > 0 and jug_amounts[j] < capacities[j]:
                amount = min(jug_amounts[i], capacities[j] - jug_amounts[j])
                new_jugs = list(jug_amounts)
                new_jugs[i] -= amount
                new_jugs[j] += amount
                new_state = (tuple(new_jugs), tank_amount)
                action = (
                    f"Chuyen/Muc {amount} lit nuoc tu gao {i + 1} qua gao {j + 1} "
                    f"{format_state(new_state[0], new_state[1])}"
                )
                neighbors.append((new_state, action))
    for i in range(n):
        if jug_amounts[i] > 0:
            new_jugs = list(jug_amounts)
            amount = new_jugs[i]
            new_jugs[i] = 0
            new_state = (tuple(new_jugs), tank_amount)
            action = (
                f"Vut bo toan bo {amount} lit nuoc cua gao {i + 1}. "
                f"{format_state(new_state[0], new_state[1])}"
            )
            neighbors.append((new_state, action))
    return neighbors


def reconstruct_actions(parent, goal_state):
    actions = []
    current = goal_state
    while parent[current][0] is not None:
        previous_state, action = parent[current]
        actions.append(action)
        current = previous_state
    actions.reverse()
    return actions


def format_solution(actions):
    if actions is None:
        return "Khong co dap an"
    lines = [f"So thao tac: {len(actions)}"]
    lines.extend(f"{index}. {action}" for index, action in enumerate(actions, start=1))
    return "\n".join(lines)


def greedy_water_jug(n, target, capacities):
    if n <= 0 or target <= 0 or any(capacity <= 0 for capacity in capacities):
        return None
    if not has_possible_answer(target, capacities):
        return None

    start_state = (tuple([0] * n), 0)
    frontier = []
    order = 0
    start_h = heuristic(start_state, target, capacities)
    heapq.heappush(frontier, (start_h, order, start_state))

    parent = {start_state: (None, None)}
    visited = set()

    while frontier:
        _, _, current_state = heapq.heappop(frontier)

        if current_state in visited:
            continue

        visited.add(current_state)
        _, tank_amount = current_state

        if tank_amount == target:
            return reconstruct_actions(parent, current_state), len(visited)

        for next_state, action in generate_neighbors(current_state, capacities, target):
            if next_state not in visited and next_state not in parent:
                parent[next_state] = (current_state, action)
                order += 1
                h = heuristic(next_state, target, capacities)
                heapq.heappush(frontier, (h, order, next_state))

    return None


def solve(input_text):
    n, target, capacities = parse_input(input_text)
    result = greedy_water_jug(n, target, capacities)

    if result is None:
        return "Khong co dap an"

    actions, visited_count = result
    return f"So trang thai da xet: {visited_count}\n{format_solution(actions)}"


def main():
    current_dir = Path(__file__).resolve().parent
    input_text = normalize_input_text(sys.stdin.read())
    output_text = solve(input_text)
    output_file = current_dir / "Greedy_out.txt"

    output_file.write_text(output_text, encoding="utf-8")
    print(f"Nhap: {input_text}")
    print(output_text)
    print(f"Da luu ket qua vao: {output_file}")


if __name__ == "__main__":
    main()
