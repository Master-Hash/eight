# 游戏规则：
# 1. 每个玩家有两个数字，数字范围是1-7
# 2. 双方轮流，每轮玩家可以将自己手上的一个数字的值变为该数字和对方手上某个数字的和
# 3. 如果超过7，则该数字的值变为1
# 4. 如果两个数字均为8，则该玩家赢

from functools import lru_cache
from json import dumps
from typing import Dict, Final, List, Set, Tuple, TypeAlias

OneHand: TypeAlias = Tuple[int | None, int | None]
Turn: TypeAlias = bool
StartIndex: TypeAlias = int
EndIndex: TypeAlias = int

COUNT_N: Final[int] = 8


@lru_cache(maxsize=None)
def sum_count_8(a1: int, a2: int) -> int | None:
    if a1 + a2 == COUNT_N:
        return None
    elif a1 + a2 > COUNT_N:
        return 1
    else:
        return a1 + a2


@lru_cache(maxsize=None)
def get_next_states(
    state: Tuple[OneHand, OneHand, Turn],
) -> List[Tuple[OneHand, OneHand, Turn]]:
    """
    >>> get_next_states(((1, 1), (1, 1), False))
    [((1, 2), (1, 1), True)]

    >>> get_next_states(((1, 2), (1, 1), True))
    [((1, 2), (1, 2), False), ((1, 2), (1, 3), False)]

    >>> get_next_states(((7, None), (5, None), True))
    [((7, None), (1, None), False)]

    如果某人两数字均为 None，轮到的一定是对方，而且函数返回值为空

    因此，返回空列表等于输
    """
    next_states: set[Tuple[OneHand, OneHand, Turn]] = set()
    current_turn_state: OneHand = state[state[2]]
    other_player_state: OneHand = state[not state[2]]
    # next_states = [
    #     (

    #         (sum_count_8(current_turn_state[i], other_player_state[j]), current_turn_state[1 - i]),
    #     )
    #     for i in range(2)
    #     for j in range(2)
    #     if current_turn_state[i] is not None
    #     if other_player_state[j] is not None
    # ]
    for i in range(2):
        for j in range(2):
            if current_turn_state[i] is not None and other_player_state[j] is not None:
                new_current_turn_state = list(current_turn_state)
                new_current_turn_state[i] = sum_count_8(
                    current_turn_state[i], other_player_state[j]
                )
                new_current_turn_state.sort(key=lambda x: COUNT_N if x is None else x)
                white, black = [tuple(new_current_turn_state), other_player_state][
                    :: 1 if not state[2] else -1
                ]
                next_states.add((white, black, not state[2]))
    for i in next_states:
        assert i in game_all_possible
    return list(next_states)


# 单个玩家的两个数字
one_player: List[OneHand] = [
    (i if i != COUNT_N else None, j if j != COUNT_N else None)
    for j in range(1, COUNT_N + 1)
    for i in range(1, j + 1)
]

game_all_possible: List[Tuple[OneHand, OneHand, Turn]] = [
    (i, j, k) for i in one_player for j in one_player for k in [False, True]
]

game_all_possible_reverse_dict: dict[Tuple[OneHand, OneHand, Turn], int] = {
    possibility: index for index, possibility in enumerate(game_all_possible)
}

# 键：局面元组
# 值：None（默认值）：未知，1：当前玩家胜，-1：当前玩家输
retrograde_dict: Dict[Tuple[OneHand, OneHand, Turn], int] = {}


graph: List[Tuple[StartIndex, EndIndex]] = []
traversed: Set[int] = set()
to_be_traversed: Set[int] = set()

# 广度优先遍历
# 起点为 game_all_possible[0]
to_be_traversed.add(0)
while to_be_traversed:
    current_index = to_be_traversed.pop()
    traversed.add(current_index)
    current_state = game_all_possible[current_index]
    for next_state in get_next_states(current_state):
        next_index = game_all_possible_reverse_dict[next_state]
        graph.append((current_index, next_index))
        if next_index not in traversed:
            to_be_traversed.add(next_index)


reversed_graph: Dict[EndIndex, List[StartIndex]] = {}
for start_index, end_index in graph:
    if end_index not in reversed_graph:
        reversed_graph[end_index] = []
    reversed_graph[end_index].append(start_index)

forward_graph: Dict[StartIndex, List[EndIndex]] = {}
for start_index, end_index in graph:
    if start_index not in forward_graph:
        forward_graph[start_index] = []
    forward_graph[start_index].append(end_index)

# 剔除没遍历到的节点
game_all_possible_traversible = [game_all_possible[i] for i in traversed]

print(len(game_all_possible_traversible))


# 标记终局
for state in game_all_possible_traversible:
    if len(get_next_states(state)) == 0:
        (a, b), (c, d), e = state
        if [a, b, c, d].count(None) == 2:
            retrograde_dict[state] = -2
        else:
            retrograde_dict[state] = -1

# 必赢或者必输的父节点
while True:
    print(len(retrograde_dict))

    not_changed = True
    for state in game_all_possible_traversible:
        state_index = game_all_possible_reverse_dict[state]
        if (
            retrograde_dict.get(state, None) in [-2, -1, 1, 2]
            # 有些游戏的开局是确定的！
            # and state_index in reversed_graph
            and state_index != 0
        ):
            parents_indexes = reversed_graph[state_index]
            for parent_index in parents_indexes:
                parent_state = game_all_possible[parent_index]
                # 如果已经算过此 parent，则跳过
                if retrograde_dict.get(parent_state, None) is not None:
                    continue
                childs_indexes = forward_graph[parent_index]
                # 如果 parent 的所有子节点均为大赢，则 parent 大输
                if all(
                    retrograde_dict.get(game_all_possible[child_index], None) == 2
                    for child_index in childs_indexes
                ):
                    retrograde_dict[parent_state] = -2
                    not_changed = False
                # 如果 parent 的所有子节点均为赢，则 parent 输
                elif all(
                    retrograde_dict.get(game_all_possible[child_index], None) in [1, 2]
                    for child_index in childs_indexes
                ):
                    retrograde_dict[parent_state] = -1
                    not_changed = False
                # 如果存在子节点为大输，则 parent 大赢
                elif any(
                    retrograde_dict.get(game_all_possible[child_index], None) == -2
                    for child_index in childs_indexes
                ):
                    retrograde_dict[parent_state] = 2
                    not_changed = False
                # 如果存在子节点为输，则 parent 赢
                elif any(
                    retrograde_dict.get(game_all_possible[child_index], None)
                    in [-1, -2]
                    for child_index in childs_indexes
                ):
                    retrograde_dict[parent_state] = 1
                    not_changed = False
    if not_changed:
        break

game_all_possible_not_determined = [
    game_all_possible[i]
    for i in traversed
    if retrograde_dict.get(game_all_possible[i], None) is None
]


def what_to_do_next(state: Tuple[OneHand, OneHand, Turn]) -> None:
    if state not in game_all_possible_traversible:
        print("局面不在可遍历的局面中")
        return
    current_win_or_lose = retrograde_dict.get(state, None)
    next_states = get_next_states(state)
    next_win_or_loses = [
        retrograde_dict.get(next_state, None) for next_state in next_states
    ]
    if current_win_or_lose in [-1, -2]:
        print(f"{'大' if current_win_or_lose == -2 else ''}输")
        print(f"因为自己的选择 {next_states} 的结果分别为 {next_win_or_loses}")
        print("对方都能赢")
    elif current_win_or_lose in [1, 2]:
        print(f"{'大' if current_win_or_lose == 2 else ''}赢")
        print(f"因为自己的选择 {next_states} 的结果分别为 {next_win_or_loses}")
        print("选择让对方输的局面就能赢")
    else:
        print("未知")
        print(f"因为自己的选择 {next_states} 的结果分别为 {next_win_or_loses}")
        print("不选让对方赢，局面就能循环下去")


cytoscape_nodes = [
    {
        "data": {
            "id": f"node{game_all_possible_reverse_dict[node]}",
            "label": f"{node[0]}{' <' if not node[2] else '  '}\n{node[1]}{' <' if node[2] else '  '}",
        },
        "classes": f"{'white' if not node[2] else 'black'}{
            ' win'
            if retrograde_dict.get(node, None) == 1
            else ' lose'
            if retrograde_dict.get(node, None) == -1
            else ' winwin'
            if retrograde_dict.get(node, None) == 2
            else ' loselose'
            if retrograde_dict.get(node, None) == -2
            else ''
        }",
    }
    for node in game_all_possible_traversible
    # ###
    # for node in game_all_possible_not_determined
]
cytoscape_edges = [
    {
        "data": {
            "id": f"edge{index}",
            "source": f"node{start_index}",
            "target": f"node{end_index}",
        }
    }
    for index, (start_index, end_index) in enumerate(graph)
    # ###
    # if retrograde_dict.get(game_all_possible[start_index], None) is None
    # and retrograde_dict.get(game_all_possible[end_index], None) is None
]

# print(len(traversed))  # 1934
# print(game_all_possible_traversible)
# print(graph)
# for index, state in enumerate(game_all_possible):
#     if index not in traversed:
#         print(state)
# print(dumps(cytoscape_nodes + cytoscape_edges, indent=2, ensure_ascii=False))

# print(get_next_states(((None, None), (3, 4), True)))
# what_to_do_next(((1, None), (7, None), False))

# for i in game_all_possible_traversible:
#     print(retrograde_dict.get(i, None))
