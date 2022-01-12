import re
from collections import deque
import sys

sys.setrecursionlimit(10000000)


class SplayTree:
    class __Node:
        def __init__(self, key_=None, data_=None):
            self.key = key_
            self.data = data_
            self.parent = None
            self.left_child = None
            self.right_child = None

        def __repr__(self):
            if self.parent is not None:
                return f'[{self.key} {self.data} {self.parent.key}]'
            else:
                return f'[{self.key} {self.data}]'

    class __PrintNode:  # специальный класс для вывода косого дерева
        def __init__(self, node, index):
            self.print_node = node  # ссылка на вершину
            self.tree_index = index  # индекс, чтобы выводить по порядку

    def __init__(self, root=None):
        self.__root = root

    def __node_searcher(self, node=__Node(), key=None):
        if node is None:
            return node
        if node.key == key:
            return node
        elif node.key > key:
            if node.left_child is None:
                return node
            else:
                return self.__node_searcher(node.left_child, key)
        elif node.key < key:
            if node.right_child is None:
                return node
            else:
                return self.__node_searcher(node.right_child, key)

    def max_node(self):
        if self.__root is not None:
            buff_node = self.__root
            while buff_node.right_child is not None:
                buff_node = buff_node.right_child
            self.__splay(buff_node)
            return buff_node.key, buff_node.data
        else:
            raise Exception('error')

    def min_node(self):
        if self.__root is not None:
            buff_node = self.__root
            while buff_node.left_child is not None:
                buff_node = buff_node.left_child
            self.__splay(buff_node)
            return buff_node.key, buff_node.data
        else:
            raise Exception('error')

    def __left_rotation(self, v=__Node()):
        buff_parent = v.parent
        buff_right = v.right_child
        if buff_parent is not None:
            if buff_parent.left_child == v:
                buff_parent.left_child = buff_right
            else:
                buff_parent.right_child = buff_right
        else:
            self.__root = buff_right
        buff_right.parent = buff_parent
        v.right_child = buff_right.left_child
        if buff_right.left_child is not None:
            buff_right.left_child.parent = v
        buff_right.left_child = v
        v.parent = buff_right

    def __right_rotation(self, v=__Node()):
        buff_parent = v.parent
        buff_left = v.left_child
        if buff_parent is not None:
            if buff_parent.left_child == v:
                buff_parent.left_child = buff_left
            else:
                buff_parent.right_child = buff_left
        else:
            self.__root = buff_left
        buff_left.parent = buff_parent
        v.left_child = buff_left.right_child
        if buff_left.right_child is not None:
            buff_left.right_child.parent = v
        buff_left.right_child = v
        v.parent = buff_left

    def __splay(self, v=__Node()):
        if v is not None:
            while v.parent is not None:
                if v.parent == self.__root:
                    if v == v.parent.left_child:
                        self.__right_rotation(v.parent)
                    else:
                        self.__left_rotation(v.parent)
                else:
                    father = v.parent
                    grandpa = v.parent.parent
                    if father == grandpa.right_child and v == v.parent.right_child:
                        self.__left_rotation(grandpa)
                        self.__left_rotation(father)
                    elif father == grandpa.left_child and v == v.parent.left_child:
                        self.__right_rotation(grandpa)
                        self.__right_rotation(father)
                    elif father == grandpa.right_child and v == v.parent.left_child:
                        self.__right_rotation(father)
                        self.__left_rotation(grandpa)
                    elif father == grandpa.left_child and v == v.parent.right_child:
                        self.__left_rotation(father)
                        self.__right_rotation(grandpa)
        else:
            return

    def add_node(self, key, data):
        if key is not None and data is not None:
            if self.__root is None:
                self.__root = self.__Node(key, data)
                return

            tmp_node = self.__node_searcher(self.__root, key)

            if tmp_node.key == key:
                self.__splay(tmp_node)
                raise Exception('error')
            elif tmp_node.key < key:
                tmp_node.right_child = self.__Node(key, data)
                res_node = tmp_node.right_child
                res_node.parent = tmp_node
                self.__splay(res_node)
            else:
                tmp_node.left_child = self.__Node(key, data)
                res_node = tmp_node.left_child
                res_node.parent = tmp_node
                self.__splay(res_node)
        else:
            raise Exception('error')

    def set_node(self, key, data):
        if key is not None and data is not None:
            tmp_node = self.__node_searcher(self.__root, key)
            self.__splay(tmp_node)
            if tmp_node is None or tmp_node.key != key:
                raise Exception('error')
            else:
                tmp_node.data = data
                self.__splay(tmp_node)
        else:
            raise Exception('error')

    def search_node(self, key):
        if self.__root is None:
            return None, None
        else:
            tmp_node = self.__node_searcher(self.__root, key)
            self.__splay(tmp_node)
            return tmp_node.key, tmp_node.data

    def __height(self, v=__Node()):
        if v is None:
            return 0
        left = self.__height(v.left_child)
        right = self.__height(v.right_child)
        return max(left, right) + 1

    def __merge(self, node):
        tmp_node = node.left_child
        while tmp_node.right_child is not None:
            tmp_node = tmp_node.right_child
        self.__splay(tmp_node)
        tmp_node.right_child = node.right_child
        if tmp_node.right_child is not None:
            tmp_node.right_child.parent = tmp_node

    def delete_node(self, key):
        if key is not None:
            rm_node = self.__node_searcher(self.__root, key)
            if rm_node is None:
                raise Exception('error')
            if rm_node.key != key:
                self.__splay(rm_node)
                raise Exception('error')
            self.__splay(rm_node)
            if rm_node.right_child is None and rm_node.left_child is None:
                self.__root = None
            elif rm_node.right_child is None:
                self.__root = rm_node.left_child
                self.__root.parent = None
                del rm_node
            elif rm_node.left_child is None:
                self.__root = rm_node.right_child
                self.__root.parent = None
                del rm_node
            else:
                self.__merge(rm_node)
                del rm_node
        else:
            raise Exception('error')

    def print(self, output):
        if self.__root is None:
            output.write('_\n')
            return
        nodes_to_print = deque()
        if self.__root.left_child is not None:
            nodes_to_print.append(self.__PrintNode(self.__root.left_child, 1))
        if self.__root.right_child is not None:
            nodes_to_print.append(self.__PrintNode(self.__root.right_child, 2))
        output.write(str(self.__root))
        output.write('\n')
        layer = ''
        tree_level = 1
        tree_height = self.__height(self.__root)
        while tree_level < tree_height:
            tree_layer_elems_number = len(nodes_to_print)
            max_layer_elems_number = 2 ** tree_level
            printed_elems_number = 0
            number_of_underlinings = max_layer_elems_number
            i = 1
            while i <= max_layer_elems_number:
                if len(nodes_to_print) != 0:
                    if printed_elems_number < tree_layer_elems_number:
                        current_node = nodes_to_print.popleft()
                        if i != current_node.tree_index:
                            layer += '_ ' * (current_node.tree_index - i)
                            printed_elems_number += 1
                            number_of_underlinings -= current_node.tree_index - i
                            layer += str(current_node.print_node) + ' '
                            if current_node.print_node.left_child is not None:
                                nodes_to_print.append(
                                    self.__PrintNode(current_node.print_node.left_child,
                                                     (current_node.tree_index * 2) - 1))
                            if current_node.print_node.right_child is not None:
                                nodes_to_print.append(
                                    self.__PrintNode(current_node.print_node.right_child, current_node.tree_index * 2))
                            number_of_underlinings -= 1
                            i = current_node.tree_index + 1
                            continue
                        elif i == current_node.tree_index:
                            printed_elems_number += 1
                            number_of_underlinings -= 1
                            layer += str(current_node.print_node) + ' '
                            if current_node.print_node.left_child is not None:
                                nodes_to_print.append(self.__PrintNode(current_node.print_node.left_child, (i * 2) - 1))
                            if current_node.print_node.right_child is not None:
                                nodes_to_print.append(self.__PrintNode(current_node.print_node.right_child, i * 2))
                            i += 1
                            continue
                    else:
                        layer += '_ ' * number_of_underlinings
                        break
                else:
                    layer += '_ ' * number_of_underlinings
                    break
            output.write(layer.strip())
            output.write('\n')
            layer = ''
            tree_level += 1


def command_handler():
    splay_tree = SplayTree()
    out = sys.stdout
    for line in sys.stdin:
        if line == '\n':
            continue
        try:
            line = line[:-1]
            if re.match(re.compile(r'(min|max|print)$'), line):
                if line == 'min':
                    min_key, min_data = splay_tree.min_node()
                    out.write(f'{min_key} {min_data}')
                    out.write('\n')
                elif line == 'max':
                    max_key, max_data = splay_tree.max_node()
                    out.write(f'{max_key} {max_data}')
                    out.write('\n')
                else:
                    splay_tree.print(out)
            elif re.match(re.compile(r'(add\s-?\d+\s\S+$)'), line):
                buff_line = line.split()
                splay_tree.add_node(int(buff_line[1]), buff_line[2])
            elif re.match(re.compile(r'(set\s-?\d+\s\S+$)'), line):
                buff_line = line.split()
                splay_tree.set_node(int(buff_line[1]), buff_line[2])
            elif re.match(re.compile(r'(delete\s-?\d+$)'), line):
                buff_line = line.split()
                splay_tree.delete_node(int(buff_line[1]))
            elif re.match(re.compile(r'(search\s-?\d+$)'), line):
                buff_line = line.split()
                key_ = int(buff_line[1])
                target_key, target_data = splay_tree.search_node(key_)
                if target_key != key_ or target_key is None:
                    out.write('0\n')
                else:
                    out.write(f'1 {target_data}\n')
            else:
                out.write('error\n')
        except Exception as ex:
            out.write(str(ex) + '\n')


if __name__ == '__main__':
    command_handler()
