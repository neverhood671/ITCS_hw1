from ITCS_hw1 import GUI
from ITCS_hw1.mysim import MySim
import matplotlib.pyplot as plt
import numpy as np
import pickle
import hashlib


def get_hash(ra):
    p = pickle.dumps(ra, -1)
    return hashlib.md5(p).hexdigest()


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
    # plt.bar(x, y, yerr=[min_lens, max_lens])
    plt.errorbar(x, y, yerr=[min_lens, max_lens], fmt='o')
    plt.title("Average Cycle Length")
    plt.ylabel("Cycle Length")
    plt.yscale('log')
    plt.xlabel("Rule Number")
    plt.show()


def run_repetition(repetition, base, neighbors_num, iteration_num):
    cycles_len_arrays = []
    repetition_index = repetition

    while repetition_index:
        init_raw = list(np.random.choice([0, 1], size=(25,)))
        result_map = {}
        r = 0
        cycle_len = []
        is_cycle_found = False
        print('repetition ' + str(repetition - repetition_index) + ' / ' + str(repetition))
        while r < 256:
            m = MySim(neighbors_num, base, r, init_raw)
            k = 0
            while k < iteration_num and (not is_cycle_found):
                list_hash = get_hash(m.current_raw)
                if list_hash not in result_map:
                    # if k % 100 == 0:
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
        cycles_len_arrays.append(cycle_len)
        repetition_index -= 1
    return cycles_len_arrays


def get_average_max_and_min_cycle_len(cycles_len_arrays):
    j = 0
    average_cycle_len = []
    max_cycle_len = []
    min_cycle_len = []
    repetition_num = len(cycles_len_arrays)
    while j < len(cycles_len_arrays[0]):
        repetition_index = len(cycles_len_arrays)
        average_val = 0
        max_len = -1
        min_len = 10e4
        while repetition_index:
            repetition_index -= 1
            if cycles_len_arrays[repetition_index][j] > max_len:
                max_len = cycles_len_arrays[repetition_index][j]
            if cycles_len_arrays[repetition_index][j] < min_len:
                min_len = cycles_len_arrays[repetition_index][j]
            average_val += cycles_len_arrays[repetition_index][j]
        average_cycle_len.append(average_val // repetition_num)
        if max_len > -1:
            max_cycle_len.append(abs(max_len - (average_val // repetition_num)))
        else:
            max_cycle_len.append(0)
        if min_len < 10e4:
            min_cycle_len.append(abs(min_len - (average_val // repetition_num)))
        else:
            min_cycle_len.append(0)
        j += 1

    draw_error_bars(average_cycle_len, min_cycle_len, max_cycle_len)

    with open("avarege_cycle_ten.txt", 'w') as file_handler:
        for item in average_cycle_len:
            file_handler.write("{}\n".format(item))


def run_gui(initial_raw, k, r, rule):
    m = MySim(r, k, rule, initial_raw)
    gui = GUI(m, 'Running Rule №' + str(rule))
    gui.start()


repetition = 3
base = 2
neighbors_num = 1
iteration_num = 100
get_average_max_and_min_cycle_len(run_repetition(repetition, base, neighbors_num, iteration_num))


# init_raw = [
#     # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#     # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
# ]
#
# run_gui(init_raw, 2, 1, 30)
