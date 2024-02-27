class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def read_expressions(file):
    with open(file, 'r') as f:
        number_of_expressions = int(f.readline())
        expression_list = []
        for _ in range(number_of_expressions):
            expression_list.append(f.readline().strip())
        return expression_list


def clean_expression(expression_string) -> str:
    expression_string = expression_string.replace(' ', '')
    new_expression = ''
    for i in range(len(expression_string)):
        if expression_string[i] in ['+', '-', '*', '/']:
            new_expression += ' ' + expression_string[i] + ' '
        else:
            new_expression += expression_string[i]
    return new_expression.replace('(', ' ( ').replace(')', ' ) ')


def build_tree(expression_string):
    tokens = expression_string.split()
    index = 0

    def parse_factor():
        nonlocal index
        token = tokens[index]
        index += 1

        if token.isdigit():
            return Node(int(token))
        elif token == '(':
            node = parse_expression()
            index += 1
            return node
        else:
            raise ValueError(f"Chybny token: {token}")

    def parse_term():
        nonlocal index
        node = parse_factor()

        while index < len(tokens) and tokens[index] in {'*', '/'}:
            operator = tokens[index]
            index += 1
            right = parse_factor()
            node = Node(operator, node, right)

        return node

    def parse_expression():
        nonlocal index
        node = parse_term()

        while index < len(tokens) and tokens[index] in {'+', '-'}:
            operator = tokens[index]
            index += 1
            right = parse_term()
            node = Node(operator, node, right)

        return node

    return parse_expression()


def solve_tree(tree):
    if tree.value in {'+', '-', '*', '/'}:
        left = solve_tree(tree.left)
        right = solve_tree(tree.right)
        if tree.value == '+':
            return left + right
        elif tree.value == '-':
            return left - right
        elif tree.value == '*':
            return left * right
        elif tree.value == '/':
            return left / right
    else:
        return tree.value


if __name__ == '__main__':
    expressions = read_expressions('expressions.txt')
    for expression in expressions:
        try:
            expression_tree = build_tree(clean_expression(expression))
            print(solve_tree(expression_tree))
        except ValueError:
            print('ERROR')

