from ITCS_hw1.cycle_calculation_run import draw_error_bars, get_hash
from ITCS_hw1.mysim import MySim, k_base_to_decimal
import numpy as np


def run_repetition(repetition, r, base, rules, iteration_num):
    cycles_len_arrays = []
    transient_length_arrays = []
    entropy_arrays = []
    repetition_index = repetition

    while repetition_index:
        start_raw = list(np.random.choice([0, 1, 2], size=(50,)))
        result_map = {}
        cycle_len = []
        transient_length = []
        entr = []
        is_cycle_found = False
        print('repetition ' + str(repetition - repetition_index + 1) + ' / ' + str(repetition))
        counter = 0
        for current_rule in rules:
            my_sim = MySim(r, base, k_base_to_decimal(current_rule, base), start_raw)
            k = 0
            counter += 1
            while k < iteration_num and (not is_cycle_found):

                list_hash = get_hash(my_sim.current_raw)
                if list_hash not in result_map:
                    # if k % 10 == 0:
                    result_map[list_hash] = k
                    my_sim.step()
                else:
                    cycle_len.append(k - result_map[list_hash])
                    transient_length.append(result_map[list_hash])
                    print("entropy calculation...")
                    entr.append(my_sim.get_entropy(iteration_num))
                    print("entropy calculation finished")
                    is_cycle_found = True
                k += 1
            result_map = {}
            if not is_cycle_found:
                cycle_len.append(0)
                transient_length.append(0)
                print("no cycle found. entropy calculation...")
                entr.append(my_sim.get_entropy(iteration_num))
            is_cycle_found = False
            print(str(counter * 100 // (len(rules))) + '%')
        cycles_len_arrays.append(cycle_len)
        transient_length_arrays.append(transient_length)
        entropy_arrays.append(entr)
        repetition_index -= 1
    print("repetition finished")
    return [cycles_len_arrays, transient_length_arrays, entropy_arrays]


def run_calculation(cycles_len_arrays):
    print("start calculation max, min and avg values")
    j = 0
    average_cycle_len = []
    max_cycle_len = []
    min_cycle_len = []
    repetition_num = len(cycles_len_arrays)
    while j < len(cycles_len_arrays[0]):
        print(str(j * 100 // len(cycles_len_arrays[0])) + '%')
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
    print("finished calculation max, min and avg values")
    return [average_cycle_len, min_cycle_len, max_cycle_len]


BASE = 3
r = 2
rule = 30
init_raw = [0]*50

m = MySim(r, BASE, rule, init_raw)

l_param = 0
step = 0.05
rules = []
lyambdas = []
while l_param < 1 - 1 / m.k:
    m.rule = m.build_rule_by_lambda_randomly(l_param, 0, 10e3)
    rules.append(m.rule)
    lyambdas.append(round(l_param, 1))
    l_param += step
    print(str(l_param * 100 // (1 - 1 / m.k)) + "%")

repetition = 3
iteration_num = 10e4

res = run_repetition(repetition, r, BASE, rules, iteration_num)
print("AvgCycleLength drawing")
cycles_lengths = run_calculation(res[0])
draw_error_bars(cycles_lengths[0], lyambdas, cycles_lengths[1], cycles_lengths[2], "AvgCycleLength1", "CycleLength",
                "Langton’s λ-parameter")

print("TransientLength drawing")
trans_lengths = run_calculation(res[1])
draw_error_bars(trans_lengths[0], lyambdas, trans_lengths[1], trans_lengths[2], "TransientLength1", "CycleLength",
                "Langton’s λ-parameter")

print("Entropy drawing")
entropy = run_calculation(res[2])
draw_error_bars(entropy[0], lyambdas, entropy[1], entropy[2], "Shannon Information Entropy1", "Entropy",
                "Langton’s λ-parameter")

# r1 = m.build_rule_by_lambda_randomly(0.5, 0, 10e3)
# print(r1)
# r2 = m.build_rule_by_walk_through_method(0.5, 0, 10e3)
# print(r2)
# print(m.get_lyamda(r1, 0))
# print(m.get_lyamda(r2, 0))
# print(m.get_entropy(10e6))
