from collections import deque
PARENTESIS = ('(', ')')
OPERATORS = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}


def main():
    variables_dict = dict()
    while True:
        msg = None
        inp = input().strip()
        if inp.startswith("/"):
            msg = commands(inp)
        else:
            expr = normalize(inp)
            if None in expr:
                msg = "Invalid identifier"
            elif len(expr) == 1:
                value, msg = get_value(expr[0], variables_dict)
                if not msg:
                    print(value)
            elif len(expr) > 1 and type(expr[0]) is str and expr[1] == '=':
                value, msg = calcolate(expr[2:], variables_dict)
                if not msg:
                    variables_dict[expr[0]] = value
            elif inp:
                value, msg = calcolate(expr, variables_dict)
                if not msg:
                    print(value)
        if msg:
            print(msg)


def commands(cmd):
    if cmd == "/help":
        return "The program calculate expressions with sums and subtractions like these: 4 + 6 - 8, 2 - 3 - 4"
    elif cmd == '/exit':
        print("Bye!")
        exit()
    else:
        return "Unknown command"


def get_value(elem, variables_dict):
    value, msg = None, None
    if type(elem) is str:
        if elem in variables_dict.keys():
            value = variables_dict[elem]
        else:
            msg = "Unknown variable"
    else:
        value = elem

    if not msg and int(value) == value:
        value = int(value)
    return value, msg


def normalize(inp):
    inp_norm = ''
    for i, ch in enumerate(" ".join(inp.split())):
        if ch == ' ' or ch.isdigit() or ch.isalpha():
            inp_norm += ch
        elif ch == '=' or ch in PARENTESIS:
            inp_norm += f' {ch} '
        elif ch == '-' and inp[i+1].isdigit():
            if len(inp_norm) > 0 and (inp_norm[-1].isdigit() or inp_norm[-1].isalpha()):
                inp_norm += f' {ch} '
            elif len(inp_norm) > 1 and (inp_norm[-2].isdigit() or inp_norm[-2].isalpha()):
                inp_norm += f' {ch} '
            else:
                inp_norm += ch
        elif ch in OPERATORS and inp[i+1] in OPERATORS:
            inp_norm += ch
        elif ch in OPERATORS:
            if len(inp_norm) > 0 and inp_norm[-1] in OPERATORS:
                inp_norm += ch
            else:
                inp_norm += f' {ch} '
        else:
            inp_norm += ch

    out = []
    for element in inp_norm.split():
        if element.isdigit():
            out.append(int(element))
        elif element.isalpha() or element in ('=', '(', ')', '*', '/', '^'):
            out.append(element)
        elif set(list(element)).issubset({'+', '-'}):
            operations = {'+': 1, '-': -1}
            x = 1
            for c in element:
                if c in operations.keys():
                    x *= operations[c]
            out.append('+' if x > 0 else '-')
        else:
            try:
                out.append(float(element))
            except ValueError:
                out.append(None)
    return out


def calcolate(expr, variables_dict):
    value, msg = None, None
    if '=' in expr:
        msg = "Invalid assignment"
    else:
        rpn_expr, msg = to_postfix(expr)
        if not msg:
            tmp_stack = deque()
            for elem in rpn_expr:
                if elem in OPERATORS:
                    b = tmp_stack.pop()
                    a = tmp_stack.pop()
                    if elem == '+':
                        tmp_stack.append(a+b)
                    elif elem == '-':
                        tmp_stack.append(a-b)
                    elif elem == '*':
                        tmp_stack.append(a*b)
                    elif elem == '/':
                        tmp_stack.append(a/b)
                    elif elem == '^':
                        tmp_stack.append(a ** b)
                else:
                    x, msg = get_value(elem, variables_dict)
                    if msg:
                        return None, msg
                    tmp_stack.append(x)
            if int(tmp_stack[-1]) == tmp_stack[-1]:
                value = int(tmp_stack[-1])
            else:
                value = tmp_stack[-1]
    return value, msg


def to_postfix(expr):
    rpn_expr = []
    tmp_stack = deque()
    for el in expr:
        if el not in OPERATORS and el not in PARENTESIS:
            rpn_expr.append(el)
        elif el == '(':
            tmp_stack.append(el)
        elif len(tmp_stack) == 0 or tmp_stack[-1] == '(':
            tmp_stack.append(el)
        elif el == ')':
            while len(tmp_stack) > 0 and tmp_stack[-1] != '(':
                rpn_expr.append(tmp_stack.pop())
            if len(tmp_stack) == 0:
                return None, "Invalid expression"
            elif tmp_stack[-1] == '(':
                tmp_stack.pop()
        elif OPERATORS[el] > OPERATORS[tmp_stack[-1]]:
            tmp_stack.append(el)
        else:
            while len(tmp_stack) > 0 and OPERATORS[el] <= OPERATORS[tmp_stack[-1]] and tmp_stack[-1] != '(':
                rpn_expr.append(tmp_stack.pop())
            tmp_stack.append(el)
    while len(tmp_stack) > 0:
        if tmp_stack[-1] in PARENTESIS:
            return None, "Invalid expression"
        else:
            rpn_expr.append(tmp_stack.pop())
    return rpn_expr, None


if __name__ == "__main__":
    main()
