from ITCS_hw1 import GUI
from ITCS_hw1.mysim import MySim
import matplotlib.pyplot as plt
import numpy as np


def draw_rules_cycle_len(len_values):
    plt.rcdefaults()
    objects = []
    i = 0
    while i < len(len_values):
        objects.append(str(i))
        i += 1
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, len_values, align='center', alpha=0.5)
    plt.ylabel('Usage')
    plt.title('Rules Cycles Length')
    plt.show()


init_raw = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            ]
# m = MySim(1, 2, 0, init_raw)
# gui = GUI(m, 'someting')
# gui.start()

r = 0
result_map = dict()
cycle_len = []
is_cycle_found = False
while r < 256:
    m = MySim(1, 2, r, init_raw)
    k = 0
    while k < 10e6:
        list_hash = tuple(m.current_raw)
        if list_hash not in result_map:
            result_map[list_hash] = k
        else:
            cycle_len.append(k - result_map[list_hash])
            is_cycle_found = True
            break
        k += 1
        m.step()
    result_map.clear()
    if not is_cycle_found:
        cycle_len.append(-1)
    r += 1
    is_cycle_found = False
    print(str(int(r*100/256)) + '%')

with open("result.txt", 'w') as file_handler:
    for item in cycle_len:
        file_handler.write("{}\n".format(item))

draw_rules_cycle_len(cycle_len)


# k = 3
# r = 1




# def decimal_to_base_k(val, base):
#     length = pow(k, 2 * r + 1)
#     if val == 0:
#         return [0]
#     digits = []
#     while val:
#         digits.append(int(val % base))
#         val //= base
#         length -= 1
#     leading_zeroes = [0] * length
#     return leading_zeroes + digits[::-1]



# def k_base_to_decimal(val, base):
#     res = 0
#     index = 0
#     for j in val:
#         res += j * pow(base, index)
#         index += 1
#     return res
#
#
# def check_rule(prev_state, rule):
#     start = 0
#     stop = start + 2 * r + 1
#     length = len(prev_state)
#     rule_length = len(rule)
#     prev_state.insert(0, prev_state[-1])
#     prev_state.append(prev_state[1])
#     new_state = []
#     while start < length:
#         current_val = prev_state[start:stop:1]
#         new_state.append(rule[rule_length - k_base_to_decimal(current_val, k) - 1])
#         start += 1
#         stop += 1
#     return new_state
#
#
# # print(decimal_to_base_k(30, 2))
# current_rule = decimal_to_base_k(30, 2)
# start_state = [0, 0, 1, 2, 0]
# print(check_rule(start_state, current_rule))
