from ITCS_hw1 import GUI
from ITCS_hw1.mysim import MySim

m = MySim(1, 2, 30, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
gui = GUI(m, 'someting')
gui.start()

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
