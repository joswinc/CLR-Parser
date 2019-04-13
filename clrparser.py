import pandas as pd
import lexer
import first_follow
from data import symb, keywords,keywords_def,special_char,list
import re
from parsertable import *
from prettytable import PrettyTable as pt

count=0
symbolss=re.compile(r'[();:=]')
STRING = lexer.lexer_analyser()
first_follow.printfirst()
print()
print()
def first(symbol):
    sub_list = []
    for item in list:
        if(symbol in special_char or symbol.islower()):
            final_set.add(symbol)
            return
    for item in list:
        if item[0] == symbol:
            a = item.split('->')
            if a[1][0].islower() or a[1][0] in special_char:
                final_set.add(a[1][0])
            elif a[1] == '#':
                final_set.add('#')
                return
            else:
                for i in a[1]:
                    result = False
                    y = symbol+'->'
                    for item1 in list:
                        if y in item1:
                            sub_list.append(item1)
                    for element in sub_list:
                        if (element != item):
                            split1, split2 = element.split('->')
                            result = True
                    z = i+'->#'
                    if i != symbol and (i.islower() or i in special_char):
                        final_set.add(i)
                        break
                    elif i == symbol and z not in list and result:
                        first(split2[0])
                        if '#' in final_set:
                            continue
                        break
                    elif i == symbol and z in list:
                        len_a1 = len(a[1])
                        x = a[1].index(i)
                        if x+1 < len_a1:
                            first(a[1][x+1])
                        break
                    elif i != symbol:
                        len_a1 = len(a[1])
                        x = a[1].index(i)
                        if x < len_a1:
                            first(a[1][x])
                            if '#' not in final_set:
                                break
        elif symbol.islower() or symbol in special_char:
            final_set.add(symbol)

    return final_set



final_set = set()
final_set2 = set()

def first_of_prod(sym):
    final_set2.clear()
    length_sym = len(sym)
    if sym == '#':
        final_set2.add('#')
    count = 0
    for item in sym:
        if item == '#':
            continue
        if item.islower() or item in special_char:
            final_set.clear()
            first(item)
            for finalelements in final_set:
                final_set2.add(finalelements)
            break
        else:
            if item == sym[length_sym-1] and count == length_sym-1:
                final_set.clear()
                first(item)
                for finalelements in final_set:
                    final_set2.add(finalelements)
            final_set.clear()
            first(item)
            if '#' in final_set:
                final_set.remove('#')
                for finalelements in final_set:
                    final_set2.add(finalelements)
                count = count + 1
                continue
            else:
                for finalelements in final_set:
                    final_set2.add(finalelements)
                break
    final_set.clear()
    return final_set2

def closure(elements):
    final_set2_new = set()
    for item in elements:
        lhs = item.split('->')
        lhs
        rhs = lhs[1].split(',')
        rhs
        length = len(rhs[0])
        part2 = ''
        if rhs[0].index('.') == length-1:
            pass
        elif rhs[0][rhs[0].index('.')+1].isupper() and rhs[0].index('.') < length:
            B = rhs[0][rhs[0].index('.')+1]+'->'
            B
            for i in range(rhs[0].index('.')+2, length):
                part2 += rhs[0][i]
            part2
            if part2 == '':
                part2 = '#'
            part2
            for item1 in list:
                if B in item1:

                    a = item1.split('->')
                    a1 = a[0]
                    b1 = a[1]
                    lookahead = part2+rhs[1]
                    final_set2_new = first_of_prod(lookahead)
                    for item2 in final_set2_new:
                        adding_element = B+"."+b1+","+item2
                        if adding_element not in elements:
                            elements.append(adding_element)
                    final_set2_new.clear()
    return elements

def goto(elements, X):
    J = []
    K = []


    for item1 in elements:
        find = '.'+X
        if find in item1:
            K.append(item1)
        else:
            pass

    for item2 in K:
        srr = ''


        index_of_dot = item2.index('.')


        for item3 in item2:
            if item3 != '.':
                srr = srr+item3
            else:

                srr = srr+item2[index_of_dot+1]+'.'+item2[index_of_dot+2:]


                break
        J.append(srr)

        J
    return closure(J)

def set_of_items(list):
    global count

    states = ['I0']
    state_number = 1
    items = {'I0': closure(['^->.S,$'])}
    for state in states:
        print("I",count)
        print("*****")
        count=count+1

        grammar_sym = []
        for item in items[state]:
            print("          ",end=" ")
            print(item)
            if '.,' in item:
                continue
            else:
                dot_index = item.index('.')
                if item[dot_index+1] not in grammar_sym:
                    grammar_sym.append(item[dot_index+1])
        print()
        print()
        for X in grammar_sym:

            goto_result = goto(items[state], X)

            if len(goto_result) > 0 and goto_result not in items.values():
                new_state = 'I'+str(state_number)
                states.append(new_state)
                items[new_state] = goto_result
                state_number += 1

    return items, state_number

def table_construction(list):
    terminals = set()
    non_terminals = set()
    for item in list:
        for item1 in item:
            if item1.islower() or item1 in special_char:
                terminals.add(item1)
            elif item1.isupper():
                non_terminals.add(item1)
    terminals.add('$')
    terminals
    non_terminals
    C, state_number = set_of_items(list)

    ACTION = pd.DataFrame(columns=terminals, index=range(state_number))
    GOTO = pd.DataFrame(columns=non_terminals, index=range(state_number))

    list_of_states = []
    for i in range(0, state_number):
        x = 'I'+str(i)
        list_of_states.append(x)
    test = 0
    for state in list_of_states:
        list_grammar_sym = []
        for item in C[state]:
            if '.,' in item:
                continue
            else:
                dot_index = item.index('.')
                if item[dot_index+1] not in list_grammar_sym:
                    list_grammar_sym.append(item[dot_index+1])
        for gramma_symbol in list_grammar_sym:
            number = 0
            goto_result_table = goto(C[state], gramma_symbol)
            i_states = 'I'+str(number)
            for i in range(state_number):
                if number < state_number:
                    if goto_result_table == C[i_states]:
                        if gramma_symbol in terminals:
                            row_index = int(state[1:])
                            ACTION.at[row_index, gramma_symbol] = "S "+str(i_states[1:])
                            break
                        elif gramma_symbol in non_terminals:
                            row_index = int(state[1:])
                            GOTO.at[row_index, gramma_symbol] = str(i_states[1:])
                            break
                    else:
                        number = number+1
                        i_states = 'I'+str(number)
        test= test+1
    for state in list_of_states:
        for item in C[state]:
            if '.,' in item:
                look_ahead = item.split('.,')
                print(look_ahead,end="---->")
                reduce_index = list.index(look_ahead[0])
                print(reduce_index)
                for element_reduce in look_ahead[1]:
                    ACTION.at[int(state[1:]), element_reduce] = "r "+str(reduce_index)
    ACTION.at[1, '$'] = "ACCEPT"
    ACTION.fillna("", inplace = True)
    GOTO.fillna("", inplace = True)
    PARSING_TABLE = pd.concat([ACTION, GOTO], axis=1)
    return PARSING_TABLE

PARSING_TABLE = table_construction(list)

PARSING_TABLE

PARSING_TABLE.to_csv('parsing_table.csv')


STRING  = STRING.replace(',', '|')
STRING_CONSIDERED = STRING+'$'

parsed_string_table(STRING_CONSIDERED,PARSING_TABLE,list)
