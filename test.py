from ITCS_hw1 import GUI
from ITCS_hw1.mysim import MySim
import matplotlib.pyplot as plt
import numpy as np
import time


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


def draw_error_bars(average_lens, min_lens, max_lens):
    x = list(range(0, len(average_lens)))
    y = average_lens
    plt.figure()
    plt.errorbar(x, y, yerr=[min_lens, max_lens], fmt='o')
    plt.title("Average Cycle Length")
    plt.ylabel("Cycle Length")
    plt.xlabel("Rule Number")
    plt.show()


def sort_by_classes(arr):
    classes_dict = {}
    with open("wolfram_classes.txt") as f:
        for line in f:
            (key, val) = line.split()
            classes_dict[int(key)] = val
    for i in range(len(arr)):
        for j in range(len(arr) - 1, i, -1):
            if classes_dict[arr[j]] < classes_dict[arr[j - 1]]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
    return arr


repetition = 10

cycle_len_array = []
start_time = time.time()
repetition_index = repetition

while repetition_index:
    init_raw = list(np.random.choice([0, 1], size=(25,)))
    result_map = {}
    r = 0
    cycle_len = []
    is_cycle_found = False
    print('repetition ' + str(repetition - repetition_index) + ' / ' + str(repetition))
    while r < 256:

        m = MySim(1, 2, r, init_raw)
        k = 0
        while k < 10e4 and (not is_cycle_found):
            list_hash = tuple(m.current_raw)
            if list_hash not in result_map:
                if k % 100 == 0:
                    result_map[list_hash] = k
            else:
                cycle_len.append(k - result_map[list_hash])
                is_cycle_found = True
            k += 1
            m.step()
        result_map = {}
        if not is_cycle_found:
            cycle_len.append(0)
        r += 1
        is_cycle_found = False
        print(str(r * 100 // 256) + '%')
    cycle_len_array.append(cycle_len)
    repetition_index -= 1

end_time = time.time()
print(end_time - start_time)

j = 0
average_cycle_len = []
max_cycle_len = []
min_cycle_len = []
while j < len(cycle_len):
    repetition_index = repetition
    average_val = 0
    max_len = -1
    min_len = 10e4
    while repetition_index:
        repetition_index -= 1
        if cycle_len_array[repetition_index][j] > max_len:
            max_len = cycle_len_array[repetition_index][j]
        if cycle_len_array[repetition_index][j] < min_len:
            min_len = cycle_len_array[repetition_index][j]
        average_val += cycle_len_array[repetition_index][j]
    average_cycle_len.append(average_val // repetition)
    if max_len > -1:
        max_cycle_len.append(abs(max_len - (average_val // repetition)))
    else:
        max_cycle_len.append(0)
    if min_len < 10e4:
        min_cycle_len.append(abs(min_len - (average_val // repetition)))
    else:
        min_cycle_len.append(0)
    j += 1

draw_error_bars(average_cycle_len, min_cycle_len, max_cycle_len)

with open("avarege_cycle_ten.txt", 'w') as file_handler:
    for item in average_cycle_len:
        file_handler.write("{}\n".format(item))



        # init_raw = [
        #     # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #     # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # ]
        # m = MySim(1, 2, 2, init_raw)
        # gui = GUI(m, 'someting')
        # gui.start()





        # with open("result.txt", 'w') as file_handler:
        #     for item in cycle_len:
        #         file_handler.write("{}\n".format(item))
        #
        # draw_rules_cycle_len(average_cycle_len)

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
