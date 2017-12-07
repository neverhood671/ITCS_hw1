import random

from ITCS_hw1 import Model
import numpy as np
import matplotlib.pyplot as plt


def k_base_to_decimal(val, base):
    res = 0
    index = len(val)
    for j in val:
        index -= 1
        res += j * (base ** index)
    return res


def decimal_to_k_base(val, base, digits_num):
    digits = []
    if val == 0:
        pass
    while val:
        digits.append(int(val % base))
        val //= base
        digits_num -= 1
    leading_zeroes = [0] * digits_num
    return leading_zeroes + digits[::-1]


class MySim(Model):
    def __init__(self, neighbors_num, base, rule_name, initial_raw):
        Model.__init__(self)
        self.k = base
        self.r = neighbors_num
        self.rule_name = rule_name
        self.rule = self.build_rule_set(rule_name, base)
        self.initial_raw = list(initial_raw)
        self.current_raw = list(initial_raw)
        rule_mas_dimension = 2 * neighbors_num + 1
        self.rule_mas = np.zeros(([base] * rule_mas_dimension), dtype=np.int)
        self.build_rule_mas(self.rule_mas, rule_mas_dimension, len(self.rule) - 1)
        self.current_time = 0

    def reset(self):
        self.current_raw = list(self.initial_raw)
        self.current_time = 0
        self.rule = self.build_rule_set(self.rule_name, self.k)
        rule_mas_dimension = 2 * self.r + 1
        self.rule_mas = np.zeros(([self.k] * rule_mas_dimension), dtype=np.int)
        self.build_rule_mas(self.rule_mas, rule_mas_dimension, len(self.rule) - 1)

    def step(self):
        start = 0
        end = start + 2 * self.r + 1
        length = len(self.current_raw)
        prev_state = list(self.current_raw)

        window_index = 0
        while window_index < self.r:
            prev_state.insert(0, self.current_raw[-window_index - 1])
            prev_state.append(self.current_raw[window_index])
            window_index += 1

        self.current_raw = []
        self.current_time += 1

        while start < length:
            sub_rule_mas = self.rule_mas[prev_state[start]]
            array_index = start + 1
            while array_index < end:
                sub_rule_mas = sub_rule_mas[prev_state[array_index % length]]
                array_index += 1
            self.current_raw.append(sub_rule_mas)
            start += 1
            end += 1

    def draw(self):
        return self.current_raw

    def build_rule_set(self, rule_name, base):
        length = pow(self.k, 2 * self.r + 1)
        digits = []
        if rule_name == 0:
            digits.append(0)
        while rule_name:
            digits.append(int(rule_name % base))
            rule_name //= base
            length -= 1
        leading_zeroes = [0] * length
        return leading_zeroes + digits[::-1]

    def check_rule(self, prev_state_with_neighbors):
        return self.rule[k_base_to_decimal(prev_state_with_neighbors, self.k)]

    def build_rule_mas(self, rule_mas, dimension, m):
        i = 0
        next_dimension = dimension - 1
        while i < self.k:
            if dimension > 1:
                m = self.build_rule_mas(rule_mas[i], next_dimension, m)
            else:
                rule_mas[i] = self.rule[m]
                m -= 1
            i += 1
        return m

    def build_rule_by_lambda_randomly(self, l, sq, iteration_num):
        rule = [0] * len(self.rule)
        while iteration_num:
            i = len(rule) - 1
            while i:
                g = random.uniform(0, 1)
                if g > l:
                    rule[i] = sq
                else:
                    while True:
                        rule[i] = random.randint(0, self.k - 1)
                        if rule[i] != sq:
                            break
                i -= 1
            iteration_num -= 1
        return rule

    def get_lyamda(self, rule, sq):
        N = 2 * self.r + 1
        n = rule.count(sq)
        return 1 - n / pow(self.k, N)

    def build_rule_by_walk_through_method(self, l, sq, iteration_num):
        rule = [sq] * len(self.rule)
        new_l = 0
        while iteration_num:
            if new_l < l:
                num_of_changing_cells = random.randint(1, len(self.rule) - 1)
                changing_indexes = random.sample(range(0, len(self.rule) - 1), num_of_changing_cells)
                for i in changing_indexes:
                    while True:
                        rule[i] = random.randint(0, self.k - 1)
                        if rule[i] != sq:
                            break
                new_l = self.get_lyamda(rule, sq)
            if new_l > l:
                num_of_rechanging_cells = random.randint(0, num_of_changing_cells - 1)
                cells_for_rechanging = np.random.choice(changing_indexes, size=num_of_rechanging_cells, replace=False)
                for i in cells_for_rechanging:
                    rule[i] = sq
                new_l = self.get_lyamda(rule, sq)
            iteration_num -= 1
        return rule

    def get_entropy(self, iteration_num):
        # self.reset()
        while self.current_time < iteration_num:
            self.step()
            iteration_num -= 1
        i = 0
        n = pow(self.k, 2 * self.r + 1)
        p = [0] * n
        raw = list(self.current_raw)
        raw.insert(0, self.current_raw[-1])
        raw.append(self.current_raw[1])

        print("calculation p")
        # while i < n:
        #     s = decimal_to_k_base(i, self.k, 2 * self.r + 1)
        #     p.append(sum(1 for j in range(len(raw)) if raw[j:j + len(s)] == s) / (len(raw) - 2))
        #     i += 1
        while i < len(raw) - 2:
            subraw = k_base_to_decimal(raw[i:i + 2 * self.r + 1], self.k)
            p[subraw] += 1
            i += 1

        div_const = len(raw) - 2
        result_p = [x / div_const for x in p]

        res = 0
        i = len(result_p) - 1
        print("calculation entropy sum ")
        while i >= 0:
            if result_p[i] != 0:
                a = result_p[i] * np.log2(result_p[i])
                res += a
            i -= 1
        return -res

    def draw_barchart(self, vals_to_plot, ylabel, xlabel):
        plt.rcdefaults()
        y = []
        x = []
        i = 0
        while i < len(vals_to_plot):
            y.append(str(i))
            i += 1
        y_pos = np.arange(len(y))

        plt.bar(y_pos, vals_to_plot, align='center', alpha=0.5)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()
