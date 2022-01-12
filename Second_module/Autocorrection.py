import sys
import re

regular_expression = r'^\s+$'


class TreeNode:
    def __init__(self):
        self.children = dict()
        self.word = None


class PrefixTree:
    """""
    В данной структуре префиксного дерева вершины хранятся в ребрах
    у каждой вершины есть словарь, которое хранит название выходящего из нее ребра (то есть буква)
    и ссылку на следующую вершину. Доходя до последней вершины, в неё записывается само словаершине хранится слово, 
    которое собирается в результате обхода предшествующих ребёр.    
    """""

    def __init__(self):
        self.__root = TreeNode()

    """""
    Вставка:
     Алгоритм действует следующим образом: спускаемся из корня дерева на нижние уровни, каждый раз переходя в узел, 
     чья метка совпадает с очередным символом слова. 
     После того как обработаны все символы ключа, узел, в котором остановился алгоритм и будет узлом, 
     которому должно быть присвоено значение word.
     Если в процессе спуска отсутствует узел с меткой, соответствующей очередному символу ключа, 
     то нужно создать новый промежуточный узел с нужной меткой и назначить его потомком текущего.

    Временная сложность добавления ключа — О(|word|). |word| - длина добавляемого слова
    Сложность по памяти — О(|word|). |word| - длина добавляемого слова
    """""

    def add_node(self, word):
        vertex = self.__root
        word = word.lower()
        for char in word:
            if char not in vertex.children:
                vertex.children[char] = TreeNode()
            vertex = vertex.children[char]
        vertex.word = word

    """""
    Поиск слова:
    Алгоритм поиска слова очень похож на алгоритм добавления ключа, 
    за тем исключением, что если в процессе спуска отсутствует узел с меткой, соответствующей очередному символу ключа, 
    мы не создаём никаких промежуточных узлов, а выводим булевое значение False, что означает, 
    что в дереве данного слова нет.
    Временная сложность алгоритма поиска слова - O(|word|). |word| - длина добавляемого слова
    Сложность по памяти - O(1), т. к. создаем 1 переменную, хранящую ссылку на текущий узел.
    """""

    def search_in_tree(self, word):
        if word is None:
            return False
        refactor = self.__root
        for char in word:
            if char not in refactor.children:
                return False
            refactor = refactor.children[char]
        if refactor.word == word:
            return True
        else:
            return False

    """""
    Алгоритм расстояния Дамерау-Левенштайна:
    Расстояние Дамерау-Левенштайна - это мера разницы двух строк символов, 
    определяемая как минимальное количество операций вставки, 
    удаления, замены и транспозиции, необходимых для перевода одной строки в другую.
    На вход подается слово, далее это слово сравнивается с каждым словом хранящимся внутри префиксного дерева, то есть
    создается таблица MxN, где M и N - длины сравниваемых слов. 
    Алгоритм Автокоррекции:
    Сложность по времени:
        Для подаваемого на вход слова, по очереди проверяется символ из ветви дерева. 
        То есть для каждого узла (или символа) в префиксном дереве создаем одну строку в таблице.
        В каждой строке данной таблицы length + 1 элементов, 
        потому что в алгоритме Дамерау-Левенштайна нумерация символов начинается с единицы.
        В итоге сложность по времени займёт O(quantity*length),
        где quantity - число узлов в дереве, length - длина максимального слова.
    Сложность по памяти:
        Для обработки каждого узла в данной реализации используется 
        рекурсивный вызов алгоритма Дамерау-Левенштайна, из-за рекурсии
        заполняется стек вызовов. Поэтому по памяти это займёт O(quantity) вызовов функции, где quantity - число узлов, 
        ведь в худшем случае мы обойдем все узлы в дереве. Внутри алгоритма Дамерау-Левенштайна, для проверки узла
        требуется 3 строки матрицы (текущая, предыдущая и предпредыдущая), в итоге для каждого узла создаётся и 
        заполняется строка в матрице. Длина такой строки равна length+1, потому что нумерация символов начинается
        с единицы. length - длина проверяемого слова.
        Следовательно по памяти это составляет O(length) для каждого вызова функции.
        В итоге, сложность по памяти займёт O(number*length)
    """""

    @staticmethod
    # стоимость трансопзиции
    def __get_transposition_cost(prev_char, index, word, char, pre_prev_row):
        if prev_char is not None and index > 1 and word[index - 1] != char \
                and prev_char == word[index - 1] and char == word[index - 2]:
            return pre_prev_row[index - 2] + 1
        else:
            return None

    def __get_cost(self, index, curr_row, prev_row, pre_prev_row, word, char, prev_char):
        # Вычисляем стоимость удаления, вставки и замены слова
        delete_cost = curr_row[index - 1] + 1
        insert_cost = prev_row[index] + 1
        if word[index - 1] == char:
            replace_cost = prev_row[index - 1]
        else:
            replace_cost = prev_row[index - 1] + 1
        transposition_cost = self.__get_transposition_cost(prev_char, index, word, char, pre_prev_row)
        if transposition_cost is not None:
            curr_row.append(min(delete_cost, insert_cost, replace_cost, transposition_cost))
        else:
            curr_row.append(min(delete_cost, insert_cost, replace_cost))

    def __damerau_levenshtein(self, vertex, char, word, prev_row, pre_prev_row, prev_char, results, size_of_word):
        if vertex is not None:
            columns = size_of_word
            curr_row = [prev_row[0] + 1]
            # Строим одну строку для символа с столбцами для каждого символа из нашего слова
            for i in range(1, columns):
                self.__get_cost(i, curr_row, prev_row, pre_prev_row, word, char, prev_char)
            # если последняя запись в строке, указывающая оптимальную стоимость, меньше или равна единице
            # и в этой вершине есть слово, то добавляем в результат
            if vertex.word is not None and curr_row[-1] <= 1:
                results.append(vertex.word)
            # если какие-либо позиции в строке меньше либо равно единице, то рекурсивно перебираем все ветви дерева
            if min(curr_row) <= 1:
                prev_char = char
                for symbol in vertex.children:
                    self.__damerau_levenshtein(vertex.children[symbol], symbol, word, curr_row, prev_row, prev_char,
                                               results, size_of_word)
        else:
            return

    def autocorrection(self, word):
        node = self.__root
        # строим первый ряд
        curr_row = list()
        for i in range(len(word) + 1):
            curr_row.append(i)
        results = list()
        # рекурсивно перебираем каждую ветвь префиксного дерева
        for char in node.children:
            self.__damerau_levenshtein(node.children[char], char, word, curr_row, None, None,
                                       results, len(word) + 1)
        return results


def print_answer(out, tree, word):
    if tree.search_in_tree(word.lower()):
        out.write(f'{word} - ok')
    else:
        result = tree.autocorrection(word.lower())
        if len(result) == 0:
            out.write(f'{word} -?')
        else:
            out.write(f'{word} -> ')
            out.write(', '.join((sorted(result))))


def initialization(tree):
    sequence = range(int(input()))
    for _ in sequence:
        tree.add_node(input())


if __name__ == '__main__':
    prefix_tree = PrefixTree()
    output = sys.stdout
    initialization(prefix_tree)
    flag = True
    for line in sys.stdin:
        if re.match(re.compile(regular_expression), line):
            continue
        else:
            # делаем перевод на новую строчку только когда вводим команду
            if flag:
                flag = False
            else:
                output.write('\n')
            target_word = line.strip('\n')
            print_answer(output, prefix_tree, target_word)
