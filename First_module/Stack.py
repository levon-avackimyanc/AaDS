import sys
import re

size_command = 0
stack = []
last_elem = -1
capasity = 0
size = 0
for line in sys.stdin:
    b = line.split()
    if (len(b) != 0):
        if (re.match(r'^set_size\s\d+$', line)):
            a = line.split()
            if (len(a) != 0):
                if a[0] == 'set_size':
                    if (len(a) == 2):
                        if (size_command < 1):
                            size = int(a[1])
                            stack = [None] * size
                            size_command += 1
                        else:
                            print('error')
                    else:
                        print('error')
        elif (re.match(r'^push\s\S+$', line)):
            a = line.split()
            if size_command == 1:
                if capasity < size:
                    last_elem += 1
                    stack[last_elem] = a[1]
                    capasity += 1
                else:
                    print('overflow')
            else:
                print('error')
        elif (re.match(r'^pop$', line)):
            a = line.split()
            if size_command == 1:
                if last_elem >= 0:
                    print(stack[last_elem])
                    stack[last_elem] = [None]
                    last_elem -= 1
                    capasity -= 1
                else:
                    print('underflow')
            else:
                print('error')
        elif (re.match(r'^print$', line)):
            if size_command:
                if capasity != 0:
                    print(' '.join(stack[0:last_elem + 1]))
                else:
                    print('empty')
            else:
                print('error')
        else:
            print('error')
    else:
        pass
