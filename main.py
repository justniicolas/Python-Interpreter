import sys
import operator

class InterpreterObject(object):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Keyword(InterpreterObject):
    ...


class String(InterpreterObject):
    ...


STRING_DELIMITER = "\""

def tokenize(s):
    result = []
    current_word = ""
    in_string = False

    for i, char in enumerate(s):
        if char == STRING_DELIMITER:
            if in_string is False: 
                in_string = True 
                current_word += char
            else :
                in_string = False
                current_word+=char
                result.append(current_word)
                current_word = ""

        elif in_string is True :
            current_word += char

        elif char in[' ','\n', '\t']:
            continue

        elif char in ["(", ")"]:
            result.append(char)
        else:
            current_word += char

            if i <len (s) and s[i+1] in ['(',')',' ','\n', '\t']:
                result.append(current_word)
                current_word = ""

    return(result)

def parse (tokens):
    tokens_iter = iter(tokens)
    token = next(tokens_iter)


    if token!= '(':
        print("Invalid program")
        sys.exit(1)

    return do_parse (tokens_iter)


def is_float(v):
    try: 
        float(v)
        return True 
    except Exception: 
        return False
def is_int(v):
    try: 
        int(v)
        return True 
    except Exception: 
        return False

def is_string(v):
    if v[0] == STRING_DELIMITER and v[-1]== STRING_DELIMITER:
        return True
    return False

def do_parse (tokens):
    result = []

    for token in tokens :
        if token == '(': 
            result.append(do_parse(tokens))
        elif token == ')': 
            return result
        elif is_int(token):
            result.append(int(token))
        elif is_float(token):
            result.append(float(token))
        elif is_string(token):
            result.append(String(token[1:][0:-1]))
        else:
            result.append(Keyword(token))


def eval (expr, context):
    if isinstance(expr, Keyword): 
        if expr.value not in context: 
            print("Cant find keyword ", expr)
            sys.exit(1)
        else : 
            return context[expr.value]
    elif isinstance (expr, list):
        fn = eval(expr[0], context)
        args = [eval(arg, context) for arg in expr[1:]]
        return apply(fn, args)
    elif isinstance (expr, String): 
        return expr.value 
    else: 
        return expr


def apply (fn, args):
    if callable (fn):
        return fn(*args)

context = {
    '+': operator.add,
    '-' : operator.sub, 
    'print' : print

}


with open("./test.lsp") as file:
    content = file.read()
    tokens = tokenize(content)
    parsed = parse(tokens)
    eval(parsed, context)