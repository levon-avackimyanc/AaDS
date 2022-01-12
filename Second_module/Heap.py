import sys
import math
import re


class BinaryHeap:
    class __HeapElem:
        def __init__(self, key_=None, data_=None):
            self.key = key_
            self.data = data_

    def __init__(self):
        self.__nodes_list = []
        self.__heap_indexes = dict()  # модификация кучи, позволяющая обращаться к её элементам в среднем за О(1)

    def __heap_size(self):
        return len(self.__nodes_list)

    def __bubble_up(self, key, index):
        i = index
        parent = (i - 1) // 2
        self.__heap_indexes[key] = i
        while i > 0 and self.__nodes_list[parent].key > self.__nodes_list[i].key:
            buff = self.__nodes_list[i]
            self.__heap_indexes[self.__nodes_list[parent].key] = i
            self.__nodes_list[i] = self.__nodes_list[parent]
            self.__nodes_list[parent] = buff
            i = parent
            self.__heap_indexes[key] = i
            parent = (i - 1) // 2

    def add_element(self, key=None, value=None):
        if key is None or value is None or key in self.__heap_indexes:
            raise Exception('error')
        self.__nodes_list.append(self.__HeapElem(key, value))
        self.__bubble_up(key, self.__heap_size() - 1)

    def set(self, key=None, value=None):
        if key is None or value is None or key not in self.__heap_indexes:
            raise Exception('error')
        i = self.__heap_indexes[key]
        self.__nodes_list[i].data = value

    def search(self, key):
        if key is None:
            raise Exception('error')
        if key not in self.__heap_indexes:
            return None, None
        index = self.__heap_indexes[key]
        return index, self.__nodes_list[index].data

    def min_elem(self):
        if self.__nodes_list:
            return self.__nodes_list[0].key, self.__nodes_list[0].data
        else:
            raise Exception('error')

    def max_elem(self):
        if self.__nodes_list:
            max_elem = self.__nodes_list[0]
            max_index = 0
            number_of_elems = self.__heap_size()
            for i in range(number_of_elems // 2, number_of_elems):
                if self.__nodes_list[i].key > max_elem.key:
                    max_elem = self.__nodes_list[i]
                    max_index = i
            return max_elem.key, max_index, max_elem.data
        else:
            raise Exception('error')

    def __heapify(self, index):
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            min_child = index
            if left_child < self.__heap_size() and self.__nodes_list[left_child].key < \
                    self.__nodes_list[min_child].key:
                min_child = left_child
            if right_child < self.__heap_size() and self.__nodes_list[right_child].key < \
                    self.__nodes_list[min_child].key:
                min_child = right_child
            if min_child == index:
                break
            buff = self.__nodes_list[index]
            self.__heap_indexes[self.__nodes_list[index].key] = min_child
            self.__heap_indexes[self.__nodes_list[min_child].key] = index
            self.__nodes_list[index] = self.__nodes_list[min_child]
            self.__nodes_list[min_child] = buff
            index = min_child

    def extract(self):
        if self.__nodes_list:
            yield self.__nodes_list[0].key
            yield self.__nodes_list[0].data
            index = self.__heap_size() - 1
            key = self.__nodes_list[0].key
            self.__nodes_list[0] = self.__nodes_list[index]
            self.__nodes_list.pop()
            del self.__heap_indexes[key]
            self.__heapify(0)
        else:
            raise Exception('error')

    def delete(self, key=None):
        if key is None or key not in self.__heap_indexes:
            raise Exception('error')
        index_to_rm = self.__heap_indexes[key]
        size_of_list = self.__heap_size()
        if index_to_rm == 0 and size_of_list > 1:
            index = size_of_list - 1
            self.__heap_indexes[self.__nodes_list[index].key] = 0
            self.__nodes_list[0] = self.__nodes_list[index]
            self.__nodes_list.pop()
            del self.__heap_indexes[key]
            self.__heapify(0)
            return
        elif index_to_rm == size_of_list - 1:
            del self.__heap_indexes[key]
            self.__nodes_list.pop()
            return
        elif 0 < index_to_rm < size_of_list - 1 and size_of_list > 1:
            del self.__heap_indexes[key]
            self.__nodes_list[index_to_rm] = self.__nodes_list[size_of_list - 1]
            self.__heap_indexes[self.__nodes_list[size_of_list - 1].key] = index_to_rm
            self.__nodes_list.pop()
            parent = (index_to_rm - 1) // 2
            if self.__nodes_list[index_to_rm].key > self.__nodes_list[parent].key:
                self.__heapify(index_to_rm)
            else:
                self.__bubble_up(self.__nodes_list[index_to_rm].key, index_to_rm)

    def print(self, output):
        if self.__heap_size() == 0:
            output.write('_\n')
            return
        else:
            output.write(f'[{self.__nodes_list[0].key} {self.__nodes_list[0].data}]\n')
            size = self.__heap_size()
            heap_height = int(math.log(size, 2))
            current_index = 1
            i = 1
            max_elem_number = 2
            while i <= heap_height:
                if i < heap_height:
                    for j in range(1, max_elem_number):
                        output.write(f'[{self.__nodes_list[current_index].key} {self.__nodes_list[current_index].data}'
                                     f' {self.__nodes_list[(current_index - 1) // 2].key}] ')
                        current_index += 1
                    output.write(f'[{self.__nodes_list[current_index].key} {self.__nodes_list[current_index].data}'
                                 f' {self.__nodes_list[(current_index - 1) // 2].key}]\n')
                    current_index += 1
                    i += 1
                    max_elem_number *= 2
                elif i == heap_height:
                    number_of_elems_on_last_level = size - current_index
                    number_of_underscores = max_elem_number - number_of_elems_on_last_level
                    if number_of_underscores != 0:
                        for j in range(current_index, size):
                            output.write(f'[{self.__nodes_list[j].key} {self.__nodes_list[j].data}'
                                         f' {self.__nodes_list[(j - 1) // 2].key}] ')
                        output.write('_ ' * (number_of_underscores - 1))
                        output.write('_\n')
                        break
                    else:
                        for j in range(current_index, size):
                            if j == size - 1:
                                output.write(f'[{self.__nodes_list[j].key} {self.__nodes_list[j].data}'
                                             f' {self.__nodes_list[(j - 1) // 2].key}]\n')
                                i += 1
                                break
                            output.write(f'[{self.__nodes_list[j].key} {self.__nodes_list[j].data}'
                                         f' {self.__nodes_list[(j - 1) // 2].key}] ')


def command_handler():
    heap = BinaryHeap()
    out = sys.stdout
    for line in sys.stdin:
        if line == '\n':
            continue
        line = line[:-1]
        try:
            if re.match(re.compile(r'(min|max|print|extract)$'), line):
                if line == 'min':
                    min_key, min_data = heap.min_elem()
                    out.write(f'{min_key} 0 {min_data}\n')
                elif line == 'max':
                    min_key, index, min_data = heap.max_elem()
                    out.write(f'{min_key} {index} {min_data}\n')
                elif line == 'extract':
                    target_key, target_data = heap.extract()
                    out.write(f'{target_key} {target_data}\n')
                else:
                    heap.print(out)
            elif re.match(re.compile(r'(add\s-?\d+\s\S+$)'), line):
                buff_line = line.split()
                heap.add_element(int(buff_line[1]), buff_line[2])
            elif re.match(re.compile(r'(set\s-?\d+\s\S+$)'), line):
                buff_line = line.split()
                heap.set(int(buff_line[1]), buff_line[2])
            elif re.match(re.compile(r'(delete\s-?\d+$)'), line):
                buff_line = line.split()
                heap.delete(int(buff_line[1]))
            elif re.match(re.compile(r'(search\s-?\d+$)'), line):
                buff_line = line.split()
                key_ = int(buff_line[1])
                index, target_data = heap.search(key_)
                if index is None:
                    out.write('0\n')
                else:
                    out.write(f'1 {index} {target_data}\n')
            else:
                out.write('error\n')
        except Exception as exc:
            out.write(str(exc) + '\n')


if __name__ == '__main__':
    command_handler()
