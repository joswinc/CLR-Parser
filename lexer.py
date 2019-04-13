from data import *
from parsertable import *
from prettytable import PrettyTable as pt
def lexer_analyser():
    with open('code.txt', 'r') as myfile:
        string = myfile.read().replace('\n', '')

    KEYWORDS = symb + keywords

    white_space = ' '
    lexeme = ''
    list = []
    string = string.replace('\t', '')
    tokens = {}
    for i, char in enumerate(string):
        if char != white_space:
            lexeme += char
        if (i+1 < len(string)):
            if string[i+1] == white_space or string[i+1] in KEYWORDS or lexeme in KEYWORDS:
                if lexeme != '':
                    list.append(lexeme.replace('\n', '<newline>'))
                    lexeme = ''
    list.append(lexeme.replace('\n', '<newline>'))
    s = ''
    for item in list:
        for i in keywords_def:
            if i[1] == item:
                tokens[item]=i[0]
                s = s+i[0]
        if item in symb:
            tokens[item]=item
            s = s+item
        if item.isdigit() or item not in KEYWORDS:
            tokens[item]='v'
            s = s+'v'
    print()
    print()
    a = pt(['Tokens',' '])
    for i in tokens:
        row = []
        row.append(i)
        row.append(" | ".join(tokens[i]))
        a.add_row(row)
    print("Tokens:")
    print(a)
    return s
