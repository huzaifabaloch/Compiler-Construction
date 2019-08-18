import functions as m
import re


def lexer():

    ''' TO STORE ALL THE TOKENS'''
    tokens = []
    iD = 'IDENTIFIER'
    flag = 0
    integer = 'INTEGER'

    symbol = m.Symbol('symboltable.txt')

    code = m.Input('code.lang.txt')

    for index in range(len(code)):
        for smb in range(len(symbol)):

            if code[index] == symbol[smb][0]:
                tokens.append(symbol[smb])
                flag = 1
                break

        if re.match('[A-Z]', code[index]) or re.match('[a-z]', code[index]):
            if flag == 0 and not code[index][:7] == 'display':
                tk = []
                tk.append(code[index])
                tk.append(iD)
                tokens.append(tk)

        elif re.match('[0-9]', code[index]):
            if flag == 0:
                intK = []
                intK.append(code[index])
                intK.append(integer)
                tokens.append(intK)

        ''' CHECKING FOR DISPLAY FUNCTION WITH ARGUMENT '''
        if code[index][:7] == 'display' and code[index] != 'display()':
            dispAndArg = m.displaySlicing(code[index])
            for i in dispAndArg:
                if i == 'display()':
                    dk = []
                    dk.append(i)
                    dk.append('DISPLAY_FUNCTION')
                    tokens.append(dk)

                else:
                    idk = []
                    idk.append(i)
                    idk.append(iD)
                    tokens.append(idk)
        flag = 0

    return tokens
