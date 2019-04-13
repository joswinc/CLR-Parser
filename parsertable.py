import pandas as pd

def parsed_string_table( STRING_CONSIDERED,PARSING_TABLE,list):


    def parsing_string():
        PARSING_STRING.at[0, 'STACK'] = '$0'
        PARSING_STRING.at[0, 'INPUT'] = STRING_CONSIDERED
        i = 0
        ip = 0
        flag = 0
        stack = ['$', '0']
        while True:
            S = int(stack[-1])
            a = STRING_CONSIDERED[ip]
            entity = PARSING_TABLE.loc[S, a]
            if 'S' in PARSING_TABLE.loc[S, a]:
                state = PARSING_TABLE.loc[S, a].split(' ')
                number = state[1]
                x = PARSING_STRING.iloc[i, 0]
                x = x + a + number
                stack.append(a)
                stack.append(number)
                PARSING_STRING.at[i+1, 'STACK'] = x
                ip = ip+1
                PARSING_STRING.at[i+1, 'INPUT'] = PARSING_STRING.at[0, 'INPUT'][ip:]
                PARSING_STRING.at[i, 'COMMENT'] = PARSING_TABLE.loc[S, a]
            elif 'r' in PARSING_TABLE.loc[S, a]:
                grammar_rule_number = PARSING_TABLE.loc[S, a].split(' ')
                item = list[int(grammar_rule_number[1])]
                item_split = item.split('->')
                beta_len = len(item_split[1]) * 2
                length = len(stack)
                diff = length-beta_len
                stack = stack[0: diff]
                reduced_form = PARSING_STRING.iloc[i, 0][0: diff]
                reduced_form = reduced_form + item_split[0]
                stack.append(item_split[0])
                goto_state = PARSING_TABLE.loc[int(stack[-2]), stack[-1]]
                stack_content = reduced_form + goto_state
                stack.append(goto_state)
                PARSING_STRING.at[i+1, 'STACK'] = stack_content
                PARSING_STRING.at[i+1, 'INPUT'] = PARSING_STRING.iloc[i, 1]
                PARSING_STRING.at[i, 'COMMENT'] = PARSING_TABLE.loc[S, a]
            elif 'ACCEPT' in PARSING_TABLE.loc[S, a]:
                PARSING_STRING.at[i, 'COMMENT'] = PARSING_TABLE.loc[S, a]
                flag = 1
                break
            else:
                flag = 0
                break
            i = i+1
        return flag


    PARSING_STRING = pd.DataFrame(columns=['STACK', 'INPUT', 'COMMENT'], index=range(1))
    CLR_FLAG = parsing_string()
    PARSING_STRING.fillna("INVALID", inplace = True)

    PARSING_STRING
    PARSING_STRING.to_csv('parsed_string_table.csv')

    if(CLR_FLAG == 1):
        print("THE SOURCE CODE IS ACCEPTED BY THE GRAMMAR!")
    else:
        print("THE SOURCE CODE IS INVALID!")

    return
