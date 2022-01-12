import sys
import re

SET_SIZE_STR = r'^set_size\s\d+$'
PUSH_STR = r'^push\s\S+$'

line = open(str(sys.argv[1]), 'r')
out = open(str(sys.argv[2]), 'w')
size_count, volume = 0, 0
tale, head = 0, 0
queue = []
size_of_queue = 0

for string in line:
    check = string.split()
    if len(check) == 0:
        pass
    else:
        if re.match(re.compile(SET_SIZE_STR), string):
            command = string.split()
            if command[0] == 'set_size':
                if len(command) == 2:
                    if size_count == 1:
                        out.write('error\n')
                    else:
                        size_of_queue = int(command[1])
                        queue = [None] * size_of_queue
                        size_count += 1
                else:
                    out.write('error\n')
        elif re.match(re.compile(r'^print$'), string):
            if size_count == 1:
                if volume == 0:
                    out.write('empty\n')
                else:
                    counter = 0
                    buff_str = ''
                    buff_elem = head
                    while counter < size_of_queue:
                        if queue[buff_elem] is not None:
                            buff_str += queue[buff_elem] + ' '
                        buff_elem = (buff_elem + 1) % size_of_queue
                        counter += 1
                    out.write(buff_str[:-1])
                    out.write('\n')
            else:
                out.write('error\n')
        elif re.match(re.compile(PUSH_STR), string):
            command = string.split()
            if size_count == 1:
                if volume < size_of_queue:
                    queue[tale] = command[1]
                    volume += 1
                    tale = (tale + 1) % size_of_queue
                else:
                    out.write('overflow\n')
            else:
                out.write('error\n')
        elif re.match(re.compile(r'^pop$'), string):
            if size_count == 1:
                if volume == 0:
                    out.write('underflow\n')
                else:
                    out.write(str(queue[head]) + '\n')
                    queue[head] = None
                    head = (head + 1) % size_of_queue
                    volume -= 1
            else:
                out.write('error\n')
        else:
            out.write('error\n')
line.close()
out.close()
