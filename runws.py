import re
import sys
import os

indent = 0

def parse(s:str):
    p = re.compile("(([a-zA-Z0-9]+\\s+(?=is))|((?<=of)(\\s+.+)+)|(\\s+[a-zA-Z]+(?!is)(?<!of).))")
    return [i.group().strip() for i in p.finditer(s)]

def compile(li:list[str]):  # sourcery skip: extract-method
    global indent
    if li[1] not in ['loop', 'end', 'break', 'if', 'elseif', 'else']:
        li.append('')
        if li[0] == 'it': li[0] = '_'
        verb = {'value', 'add', 'substract', 'multiply', 'divide', 'quotient', 'remainder', 'power',
                'print', 'printline', 'integer', 'float', 'string', 'boolean',
                'greater', 'less', 'equal', 'different', 'and', 'or', 'not', 'infinity', 'execute'}
        if li[1] in verb: li[1] = f"functions('{li[1]}')"
        li[2] = ','.join(li[2].split('and'))
        return f"{' '*indent*4}{li[0]} = {li[1]}({li[2]})"
    elif li[1] == 'loop':
        if li[0] == 'it': li[0] = '_'
        if li[2] == 'infinity': li[2] = str(functions('infinity')()) #type: ignore
        li[2] = ','.join(li[2].split('and'))
        indent += 1
        return f"{' '*(indent-1)*4}for {li[0]} in range({li[2]}):"
    elif li[1] == 'end':
        indent -= 1
        return ''
    elif li[1] == 'break': return f"{' '*indent*4}break"
    else:
        indent += 1
        if li[1] == 'elseif': li[1] = 'elif'
        return f"{' '*(indent-1)*4}{li[1]} {li[2]}:" if li[1] != 'else' else f"{' '*(indent-1)*4}else:"

def functions(s:str):
    match s:
        case 'value': return lambda x: x
        case 'add': return lambda a, b: a + b
        case 'substract': return lambda a, b: a - b
        case 'multiply': return lambda a, b: a * b
        case 'divide': return lambda a, b: a / b
        case 'quotient': return lambda a, b: a // b
        case 'remainder': return lambda a, b: a % b
        case 'power': return lambda a, b: a ** b
        case 'print': return lambda a: print(a, end='')
        case 'printline': return print
        case 'integer': return int
        case 'float': return float
        case 'string': return str
        case 'boolean': return bool
        case 'greater': return lambda a, b: a > b
        case 'less': return lambda a, b: a < b
        case 'equal': return lambda a, b: a == b
        case 'different': return lambda a, b: a != b
        case 'and': return lambda a, b: a and b
        case 'or': return lambda a, b: a or b
        case 'not': return lambda a: not a
        case 'infinity': return lambda: sys.maxsize
        case 'execute': return exec

def write():
    s = []
    while True:
        temp = input('>>> ')
        if temp == '' and len(s): break
        elif temp == '': continue
        else: s.append(temp + '\n')
    with open('temp.ws', 'w') as f:
        f.writelines(s)
    os.system('runws temp.ws')

def main():
    try:
        try:
            if sys.argv[1][sys.argv[1].index('.')+1:] != 'ws': raise RuntimeError('not a valid .ws file')
        except IndexError:
            while True:
                write()
                
        os.system(f'title {sys.argv[1]}')
        with open(sys.argv[1]) as f:
            src = '\n'.join(f.readlines())
        compiled = ''
        for i in src.split('\n'):
            i = i.strip()
            if i == '': continue
            compiled += compile(parse(i)) + '\n'
        exec(compiled)
    except Exception as e:
        print(e)
    input('\n-> exit')

main()