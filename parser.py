import lexical as lex


def main():

    global tokens, token_checked


    index = 0
    token_checked = 0

    while index < length:

        token_value = tokens[index][0]
        token_type = tokens[index][1]

        if token_type == 'IDENTIFIER':
            parsing_variable_initialization_or_arithmatic_operation(tokens[index:len(tokens)])

        elif token_type == 'DISPLAY_FUNCTION':
            display_argument_packing_and_parsing(tokens[index:len(tokens)])

        elif token_type in ['OPERATOR', 'PLUS_OPERATOR', 'MINUS_OPERATOR']:
            print('Error: you cannot use an operator in beginning.')
            quit()

        token_checked += 1
        index = token_checked





def parsing_variable_initialization_or_arithmatic_operation(token_stream):

    global tokens, token_checked
    for token in range(0, len(token_stream)):

        token_type = tokens[token_checked][1]
        token_value = tokens[token_checked][0]

        if token == 0:
            print('Variable Name: ' + token_value)

        elif token == 1 and token_type == 'OPERATOR':
            print('Assignment Operator: ' + token_value)

        elif token == 1 and token_type != 'OPERATOR':
            print('Error: Invalid operator')
            error.set('Error: Invalid operator')
            quit()

        elif token == 2 and token_type in ['INTEGER', 'IDENTIFIER']:
            print('Variable Value: ' + token_value)

        elif token == 2 and token_type not in ['INTEGER', 'IDENTIFIER']:
            print('Error: Invalid Assignment!')
            quit()

        elif token == 3 and token_type == 'END_LINE':
            break

        elif token == 3 and token_type != 'END_LINE':
            if token_type in ['PLUS_OPERATOR', 'MINUS_OPERATOR']:
                print(token_type + ':  ' + token_value)

            elif token_type not in ['PLUS_OPERATOR', 'MINUS_OPERATOR']:
                print('Error: EOL missing!')
                quit()

        elif token == 3 and token_type not in ['PLUS_OPERATOR', 'MINUS_OPERATOR']:
            print('Error: Are you missing an operator!')
            quit()


        elif token == 4 and token_type in ['INTEGER', 'IDENTIFIER']:
            print('Variable Value: ' + token_value)


        elif token == 4 and token_type not in ['INTEGER', 'IDENTIFIER']:
            print('Error: Invalid, are you missing a value!')
            quit()

        elif token == 5 and token_type == 'END_LINE':
            break

        elif token == 5 and token_type != 'END_LINE':
            print('Error: EOL missing!')
            quit()

        token_checked += 1


def display_argument_packing_and_parsing(token_stream):

    global token_checked
    global tokens

    display = tokens[token_checked][0]
    argument = tokens[token_checked + 1][0]

    displayArgument = ''

    for i in display:
        if i != '(':
            displayArgument += i

        else:
            displayArgument += i
            for j in argument:
                displayArgument += j

    for token in range(0, len(token_stream)):

        token_type = tokens[token_checked][1]
        token_value = displayArgument

        print('\n')

        if token == 0:
            print('Display and Argument: ' + token_value)

        elif token == 1 and token_type == 'IDENTIFIER':
            pass

        elif token == 2 and token_type == 'END_LINE':
            break

        elif token == 2 and token_type != 'END_LINE':
            print('\aError: EOL missing!')
            quit()

        token_checked += 1


