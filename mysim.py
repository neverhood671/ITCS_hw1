from ITCS_hw1 import Model
import numpy as np


def k_base_to_decimal(val, base):
    res = 0
    index = len(val)
    for j in val:
        index -= 1
        res += j * (base ** index)
    return res


class MySim(Model):
    def __init__(self, neighbors_num, base, rule_name, initial_raw):
        Model.__init__(self)
        self.k = base
        self.r = neighbors_num
        self.rule_name = rule_name
        self.rule = self.build_rule_set(rule_name, base)
        self.initial_raw = initial_raw
        self.current_raw = initial_raw
        rule_mas_dimension = 2 * neighbors_num + 1
        self.rule_mas = np.zeros(([base] * rule_mas_dimension), dtype=np.int)
        self.build_rule_mas(self.rule_mas, rule_mas_dimension, len(self.rule) - 1)
        self.current_time = 0

    def reset(self):
        self.current_raw = self.initial_raw
        self.current_time = 0
        self.rule = self.build_rule_set(self.rule_name, self.k)
        rule_mas_dimension = 2 * self.r + 1
        self.rule_mas = np.zeros(([self.k] * rule_mas_dimension), dtype=np.int)
        self.build_rule_mas(self.rule_mas, rule_mas_dimension, len(self.rule) - 1)

    def step(self):
        start = 0
        end = start + 2 * self.r + 1
        length = len(self.current_raw)
        prev_state = self.current_raw
        self.current_raw = []
        prev_state.insert(0, prev_state[-1])
        prev_state.append(prev_state[1])
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
