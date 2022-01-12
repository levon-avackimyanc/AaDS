import sys
import re
from collections import deque


def BFS(graf, start):
    checks = set()
    checks.add(start)
    print(start)
    deq = deque([start])
    while len(deq) != 0:
        buff_vert = deq.popleft()
        for i in graf[buff_vert]:
            if i not in checks:
                checks.add(i)
                print(i)
                deq.append(i)


def DFS(graf, start):
    checks = set()
    checks.add(start)
    print(start)
    deq = deque(graf[start])
    while len(deq) != 0:
        buff_vert = deq.popleft()
        if buff_vert not in checks:
            checks.add(buff_vert)
            print(buff_vert)
            for j in graf[buff_vert][::-1]:
                deq.appendleft(j)


graf = dict()
graf_type = ''
start_vertex = ''
search_type = ''
for line in sys.stdin:
    if (re.match('^[u|d]\s\S+\s[b|d]$', line)):
        string = line.split()
        graf_type = string[0]
        start_vertex = string[1]
        search_type = string[2]
    else:
        string = line.split()
        if (len(string) != 0):
            if string[0] not in graf:
                graf[string[0]] = []
            if string[1] not in graf:
                graf[string[1]] = []
            if (graf_type == 'u'):
                if (string[1] not in graf[string[0]]):
                    graf[string[0]].append(string[1])
                if (string[0] not in graf[string[1]]):
                    graf[string[1]].append(string[0])
            elif (graf_type == 'd'):
                if (string[1] not in graf[string[0]]):
                    graf[string[0]].append(string[1])
for key in graf.keys():
    graf[key].sort()
if (search_type == 'b'):
    BFS(graf, start_vertex)
if (search_type == 'd'):
    DFS(graf, start_vertex)
