import sys
import re
from math import gcd


class BackpackResolver:
    def __init__(self, capacity_: int):
        self.__capacity = capacity_
        self.__result_weight = 0
        self.__result_value = 0
        self.__result_col = []
        self.__gcd_var = 0

    '''''
    Определяем методы, которые помогают решать задачу при больших числах
    '''''

    def __optimal_calc_weight(self, weight: list, capacity: int):
        buff_list = weight + [capacity]
        self.__gcd_var = int(max(buff_list))
        for i in range(1, len(buff_list) - 1):
            if self.__gcd_var > gcd(buff_list[i], buff_list[i + 1]):
                self.__gcd_var = gcd(buff_list[i], buff_list[i + 1])

    def __normalize_weight(self, weight: list):
        for i in range(len(weight)):
            weight[i] //= self.__gcd_var

    def __generate_table(self, weight: list, values: list):
        rows = len(weight)
        columns = self.__capacity // self.__gcd_var
        table = [[0] * (columns + 1) for _ in range(rows + 1)]
        for i in range(1, rows + 1):
            for j in range(0, columns + 1):
                if weight[i - 1] <= j:
                    table[i][j] = max(table[i - 1][j], values[i - 1] + table[i - 1][j - weight[i - 1]])
                else:
                    table[i][j] = table[i - 1][j]
        self.__result_value = table[rows][columns]
        self.__right_collection(table, weight, rows, columns)

    def __right_collection(self, table: list, weight: list, weight_size: int, capacity: int):
        if table[weight_size][capacity] == 0:
            return
        if table[weight_size - 1][capacity] == table[weight_size][capacity]:
            self.__right_collection(table, weight, weight_size - 1, capacity)
        else:
            self.__right_collection(table, weight, weight_size - 1,
                                    capacity - weight[weight_size - 1])
            self.__result_weight += weight[weight_size - 1] * self.__gcd_var
            self.__result_col.append(weight_size)

    def backpack_alg(self, weight, values):
        self.__optimal_calc_weight(weight, self.__capacity)
        self.__normalize_weight(weight)
        self.__generate_table(weight, values)

    def get_total_value(self):
        return self.__result_value

    def get_total_weight(self):
        return self.__result_weight

    def get_total_collection(self):
        return self.__result_col


def command_handler():
    out = sys.stdout
    my_backpack = None
    weights = []
    values = []
    flag = True
    for line in sys.stdin:
        if re.match(r'^\s+$', line):
            continue
        else:
            if flag:
                if re.match(re.compile(r'(^\d+$)'), line):
                    my_backpack = BackpackResolver(int(line))
                    flag = False
                else:
                    out.write('error\n')
            else:
                if re.match(re.compile(r'(^\d+\s\d+$)'), line):
                    buff_line = line.split()
                    weights.append(int(buff_line[0]))
                    values.append(int(buff_line[1]))
                else:
                    out.write('error\n')
    my_backpack.backpack_alg(weights, values)
    out.write(f'{my_backpack.get_total_weight()} {my_backpack.get_total_value()}\n')
    result_collection = my_backpack.get_total_collection()
    for item in result_collection:
        out.write(f'{item}\n')


if __name__ == '__main__':
    command_handler()
