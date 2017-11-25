from ITCS_hw1 import Model
import numpy as np
import scipy.misc as smp


def k_base_to_decimal(val, base):
    res = 0
    index = 0
    for j in val:
        res += j * pow(base, index)
        index += 1
    return res


class MySim(Model):
    def __init__(self, neighbors_num, base, rule_name, initial_raw):
        Model.__init__(self)
        self.k = base
        self.r = neighbors_num
        self.rule = self.build_rule_set(rule_name, base)
        self.initial_raw = initial_raw
        self.current_raw = initial_raw

    def reset(self):
        pass

    def step(self):
        start = 0
        end = start + 2 * self.r + 1
        length = len(self.current_raw)
        rule_length = len(self.rule)
        prev_state = self.current_raw
        self.current_raw = []
        prev_state.insert(0, prev_state[-1])
        prev_state.append(prev_state[1])
        while start < length:
            current_val = prev_state[start:end:1]
            self.current_raw.append(self.rule[rule_length - k_base_to_decimal(current_val, self.k) - 1])
            start += 1
            end += 1
        print(self.current_raw)

    def draw(self):
        return self.current_raw

    def build_rule_set(self, rule_name, base):
        length = pow(self.k, 2 * self.r + 1)
        if rule_name == 0:
            return [0]
        digits = []
        while rule_name:
            digits.append(int(rule_name % base))
            rule_name //= base
            length -= 1
        leading_zeroes = [0] * length
        return leading_zeroes + digits[::-1]

    def check_rule(self, prev_state_with_neighbors):
        return self.rule[k_base_to_decimal(prev_state_with_neighbors, self.k)]
