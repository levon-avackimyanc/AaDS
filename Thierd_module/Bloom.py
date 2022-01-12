import sys
import re
import math

MERSENN_NUMBER = (2 ** 31) - 1


class BloomFilter:
    class __Bit_Array:
        def __init__(self, size):
            self.__bits_size = size
            self.__bit_array = bytearray(math.ceil(size / 8))

        def set_bit(self, index: int):
            position = 2 ** (index % 8)
            list_index = index // 8
            self.__bit_array[list_index] |= position

        def get_bit(self, index: int):
            position = 2 ** (index % 8)
            list_index = index // 8
            if self.__bit_array[list_index] & position > 0:
                return True
            else:
                return False

        def print(self, out_):
            for i in range(self.__bits_size):
                if self.get_bit(i) is True:
                    out_.write('1')
                else:
                    out_.write('0')

    def __init__(self, n: int, p: float):
        self.__size = self.__calculate_size(n, p)
        self.__bit_array = self.__Bit_Array(self.__size)
        self.__hash_number = self.__calculate_hashes(p)
        self.__prime_numbers = self.__calculate_prime_numbers(self.__hash_number)

    @staticmethod
    def __calculate_size(n: int, p: float):
        return int(round(-n * math.log2(p) / math.log(2)))

    @staticmethod
    def __calculate_hashes(p: float):
        hashes = int(round(-math.log2(p)))
        if hashes == 0:
            raise Exception('error')
        else:
            return hashes

    @staticmethod
    def __calculate_prime_numbers(hash_number: int):
        result = [0 for _ in range(hash_number)]
        result[0] = 2
        base_counter = 1
        prime_counter = 2
        while base_counter != hash_number:
            for i in range(base_counter):
                if prime_counter % result[i] == 0:
                    prime_counter += 1
                    break
            else:
                result[base_counter] = prime_counter
                base_counter += 1
        return result

    def __hash(self, index: int, x):
        return int((((index + 1) * x + self.__prime_numbers[index]) % MERSENN_NUMBER) % self.__size)

    def get_size(self):
        return self.__size

    def get_num_of_hashes(self):
        return self.__hash_number

    def add(self, x: int):
        for i in range(self.__hash_number):
            buff_hash = self.__hash(i, x)
            self.__bit_array.set_bit(buff_hash)

    def search_elem(self, x: int):
        buff_bits = self.__Bit_Array(self.__size)
        for i in range(self.__hash_number):
            index = self.__hash(i, x)
            buff_bits.set_bit(index)
            if buff_bits.get_bit(index) != self.__bit_array.get_bit(index):
                return False
        return True

    def print(self, out_):
        self.__bit_array.print(out_)


def command_handler():
    out = sys.stdout
    my_bf = None
    for line in sys.stdin:
        if re.match(re.compile(r'^\s+$'), line):
            continue
        if my_bf is None:
            if re.match(re.compile(r'^set\s\d+\s\d.\d+$'), line):
                try:
                    buff = line[4:-1].split()
                    if int(buff[0]) > 0 and 0 < float(buff[1]) < 1:
                        my_bf = BloomFilter(int(buff[0]), float(buff[1]))
                        out.write(f'{my_bf.get_size()} {my_bf.get_num_of_hashes()}\n')
                    else:
                        out.write('error\n')
                except Exception as msg:
                    out.write(str(msg) + '\n')
            else:
                out.write('error\n')
        else:
            if re.match(re.compile(r'^add\s\d+$'), line):
                buff = line[4:]
                my_bf.add(int(buff))
            elif re.match(re.compile(r'^search\s\d+$'), line):
                buff = line[7:]
                if my_bf.search_elem(int(buff)) is True:
                    out.write('1\n')
                else:
                    out.write('0\n')
            elif re.match(re.compile(r'^print$'), line):
                my_bf.print(out)
                out.write('\n')
            else:
                out.write('error\n')


if __name__ == '__main__':
    command_handler()
