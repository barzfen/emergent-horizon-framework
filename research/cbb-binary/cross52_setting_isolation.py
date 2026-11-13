"""Measure the shortest LR3 setting leak into the idle-branch readout."""

from collections import deque

from cross41_growth_and_return import LR3, read, rewrite, split_edge
from cross48_reversal_interference import support, swapped_positions
from cross49_route_recorder import ARRIVAL, P, Q, R
from cross50_cycle_apparatus import M, build_cube, four_cubes
from cross51_recorder_phase import check_phases


def grow_buffer(signs, edge, pairs):
    for _ in range(pairs):
        signs = split_edge(split_edge(signs, edge), edge + 1)
    return signs


def attempt(signs, start):
    replacement = LR3.get(read(signs, start, 4))
    return signs if replacement is None else rewrite(signs, start, replacement)


def update_relative_labels(relative, first, second, left_fires, right_fires):
    # relative[i] is the right-tour position of the label in left-tour position i.
    if not (left_fires or right_fires):
        return relative
    mapping = list(relative)
    if left_fires:
        mapping[first], mapping[second] = mapping[second], mapping[first]
    if right_fires:
        mapping = [second if i == first else first if i == second else i for i in mapping]
    return tuple(mapping)


def transition(state, start):
    left, right, relative = state
    new_left, new_right = attempt(left, start), attempt(right, start)
    first, second = swapped_positions(start, len(left))
    return new_left, new_right, update_relative_labels(
        relative, first, second, new_left != left, new_right != right
    )


def setup(pairs):
    _, seed, starts = next(four_cubes())
    seed = grow_buffer(grow_buffer(seed, 16, pairs), 10, pairs)
    size = len(seed)
    memory = starts[M] + 2 * pairs
    # The grown preparations retain the full carrier, recorder and memory cube.
    assert all(
        min(min((i - j) % size, (j - i) % size)
            for i in support(memory, size) for j in target) == 3 + 2 * pairs
        for target in (set(range(2, 10)), set(range(size - 4, size)))
    )
    # Both settings start with the recorder in the idle basis state r=0.
    written = attempt(seed, memory)
    assert written != seed
    first, second = swapped_positions(memory, size)
    relative = update_relative_labels(tuple(range(size)), first, second, False, True)
    sign_positions = tuple(range(2, 10)) + tuple(range(size - 4, size))
    label_positions = sign_positions + (10, 0)
    assert all(seed[i] == written[i] for i in sign_positions)
    assert all(i == relative[i] for i in label_positions)
    return (seed, written, relative), sign_positions, label_positions


def distinguishable(state, sign_positions, label_positions):
    left, right, relative = state
    return any(left[i] != right[i] for i in sign_positions) or any(
        relative[i] != i for i in label_positions
    )


def witness_path(predecessors, state):
    steps = []
    while predecessors[state] is not None:
        state, start, _ = predecessors[state]
        steps.append(start)
    return tuple(reversed(steps))


def first_leak(initial, signs, labels, cap):
    pending = deque([initial])
    predecessors = {initial: None}
    while pending:
        state = pending.popleft()
        link = predecessors[state]
        depth = 0 if link is None else link[2]
        if distinguishable(state, signs, labels):
            return witness_path(predecessors, state)
        if depth == cap:
            continue
        for start in range(len(state[0])):
            target = transition(state, start)
            if target not in predecessors:
                predecessors[target] = state, start, depth + 1
                pending.append(target)
    return None


def check_explicit_labels(initial, path, signs, labels):
    left, right, relative = initial
    left_labels = list(range(len(left)))
    right_labels = list(relative)  # The initial mapping is a single transposition.
    paired = initial
    for step, start in enumerate(path, 1):
        next_left, next_right = attempt(left, start), attempt(right, start)
        first, second = swapped_positions(start, len(left))
        if next_left != left:
            left_labels[first], left_labels[second] = left_labels[second], left_labels[first]
        if next_right != right:
            right_labels[first], right_labels[second] = right_labels[second], right_labels[first]
        left, right = next_left, next_right
        paired = transition(paired, start)
        assert all(left_labels[i] == right_labels[j] for i, j in enumerate(paired[2]))
        different = any(left[i] != right[i] for i in signs) or any(
            left_labels[i] != right_labels[i] for i in labels
        )
        assert different == (step == len(path))


def main():
    expected = (
        (9,),
        (8, 11, 8),
        (10, 13, 10, 8),
        (12, 15, 12, 10, 8),
        (14, 17, 14, 12, 10, 8),
        (16, 19, 16, 14, 12, 10, 8),
    )
    for pairs, witness in enumerate(expected):
        initial, signs, labels = setup(pairs)
        assert first_leak(initial, signs, labels, len(witness) - 1) is None
        check_explicit_labels(initial, witness, signs, labels)
        size = len(initial[0])
        starts = {P: 2, Q: size - 4, R: 6, M: 12 + 2 * pairs}
        plus, minus = check_phases(build_cube(initial[0], starts), starts)
        assert all(state & ARRIVAL == ARRIVAL for state in plus)
        assert all(state & ARRIVAL == 0 for state in minus)
        print(f"{len(initial[0])} vertices: first setting leak after {len(witness)} attempts via {witness}.")


if __name__ == "__main__":
    main()
