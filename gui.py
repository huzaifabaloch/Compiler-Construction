from _lsprof import profiler_entry
from functools import partial
from itertools import chain
from textwrap import wrap
from tkinter import *
import tkinter.filedialog
import functions as f
import tkinter.messagebox
import re
import subprocess as sp


# Create Main Window and Widgets
root = Tk()
root.geometry("656x500+300+100")
root.title("tuna")
root.resizable(0,0)

error = StringVar()


def grammer():
    sp.call(['notepad.exe', 'grammer.txt'])


def browse():
    sourcefile = tkinter.filedialog.askopenfilename(title="Select Source File")
    with open(sourcefile, 'r') as fileOpen:
        code = fileOpen.read()
        fileOpen.close()
    codeArea.delete(0.0, END)
    codeArea.insert(0.0, code)


def update():
    if not codeArea.compare("end-1c", "==", "1.0"):
        tkinter.messagebox.showinfo('Code Updated', "Your Code has been Updated!")
        code = codeArea.get(1.0, END)
        return code

    else:
        tkinter.messagebox.showerror('Code', "Please Browse for a file or write your code here and click parse")


def lexer(code):

    try:
        # raw symbol table file, opening and splitting
        symbol = f.Symbol('symbolTable.txt')
        lexemes = f.SplitCode(code)

        # to store all tokens
        tokens = []

        iD = 'IDENTIFIER'
        flag = 0
        integer = 'INTEGER'

        for index in range(len(lexemes)):
            for smb in range(len(symbol)):

                if lexemes[index] == symbol[smb][0]:
                    tokens.append(symbol[smb])
                    flag = 1
                    break

            if re.match('[A-Z]', lexemes[index]) or re.match('[a-z]', lexemes[index]):
                if flag == 0 and not lexemes[index][:7] == 'display':
                    tk = []
                    tk.append(lexemes[index])
                    tk.append(iD)
                    tokens.append(tk)

            elif re.match('[0-9]', lexemes[index]):
                if flag == 0:
                    intK = []
                    intK.append(lexemes[index])
                    intK.append(integer)
                    tokens.append(intK)


            ''' CHECKING FOR DISPLAY FUNCTION WITH ARGUMENT '''
            if lexemes[index][:7] == 'display' and lexemes[index] != 'display()':
                dispAndArg = f.displaySlicing(lexemes[index])

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

        print(tokens)
        return tokens
    except:
        tkinter.messagebox.showerror('Error', 'the code is not valid!')
        quit()

def errorMessage():
    tkinter.messagebox.showerror('error', 'Error found in your code')

def main():

    error.set("")

    # getting code from the text widget and checking if it is not empty or None
    code = update()
    if code != None:

        ''' tokens where all tokens will be present and token checked used by many functions to stop repeating code
        # token_checked will keep on track whenever it parse a token, it counts so that parser wont check for same token 
        # again and again
        '''
        global tokens, token_checked

        # getting all the tokens from the lexer
        tokens = lexer(code)

        # to index through every token in the code, start from 0 -> first token
        index = 0

        # to check if a same token is not being checked again and again
        token_checked = 0

        # to count the number of tokens present in the tokens list
        length = len(tokens)

        # check tokens -> index = 0 is less than tokens --> length = N
        while index < length:

            # separating the token value and token type in a separate variable
            token_value = tokens[index][0]
            token_type = tokens[index][1]

            if token_type == 'DATA_TYPE_DEFINE':
                parseFlag = parsing_variable_initialization_or_arithmatic_operation(tokens[index:len(tokens)])
                if parseFlag != 1:
                    return

            elif token_type == 'DISPLAY_FUNCTION':
                displayFlag = display_argument_packing_and_parsing(tokens[index:len(tokens)])
                if displayFlag != 1:
                    return

            elif token_type == 'IF_STAT':
                ifFlag = parsing_IF_Statement(tokens[index:len(tokens)])
                if ifFlag != 1:
                    return

            elif token_type == 'WHILE_STAT':
                whileFlag = parsing_WHILE_Statement(tokens[index:len(tokens)])
                if whileFlag != 1:
                    return


            # -------------------------------------
            # FOR SOME INVALID LEXEMES IN START

            elif token_type in ['OPERATOR', 'PLUS_OPERATOR', 'MINUS_OPERATOR', 'MULTIPLY_OPERATOR', 'DIVISION_OPERATOR']:
                print('Error: you cannot use an operator in beginning.')
                error.set('you cannot use an operator in beginning.')
                errorMessage()
                return

            elif token_type == 'IDENTIFIER':
                error.set("Error: dtd -> data type definition is mandatory")
                errorMessage()
                return

            elif token_type == 'INTEGER':
                error.set('Error: invalid, value must be assign to a variable')
                errorMessage()
                return

            elif token_type == 'END_LINE':
                error.set('Error: invalid key el, endline must be used after a valid statement')
                errorMessage()
                return


            token_checked += 1
            index = token_checked

def parsing_WHILE_Statement(token_stream):

    flag = 0
    global tokens, token_checked

    for token in range(0, len(token_stream)):

        token_type = tokens[token_checked][1]
        token_value = tokens[token_checked][0]

        if token == 0:
            print('While Key: ' + token_value)

        elif token == 1 and token_type in ['IDENTIFIER', 'INTEGER']:
            print('Identifier or Integer: ' + token_value)

        elif token == 1 and token_type not in ['IDENTIFIER', 'INTEGER']:
            error.set('Error: the while condition must have valid values to to check')
            errorMessage()
            return

        elif token == 2 and token_type in ['GREATER_THAN', 'LESS_THAN', 'EQUAL_TO', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL']:
            print('Relational operator: ' + token_value)

        elif token == 2 and token_type not in ['GREATER_THAN', 'LESS_THAN', 'EQUAL_TO', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL']:
            error.set("Error: the conditional operator does not match in the following situation"
                      "\nAre you missing something? try -> gt, lt eq, gte, lte, ne")
            errorMessage()
            return

        elif token == 3 and token_type in ['IDENTIFIER', 'INTEGER']:
            print('Identifier or Integer: ' + token_value)

        elif token == 3 and token_type not in ['IDENTIFIER', 'INTEGER']:
            error.set('Error: the while condition must have valid values to to check')
            errorMessage()
            return


        elif token == 4 and token_type == 'WHILE_START':
            print('While Body Start: ' + token_value)

        elif token == 4 and token_type != 'WHILE_START':
            error.set("Error: while must have start body. Start Key missing\nKeyError missing")
            errorMessage()
            return

        elif token == 5 and token_type == 'DISPLAY_FUNCTION':
            print('Display: ' + token_value)


        elif token == 5 and token_type != 'DISPLAY_FUNCTION':
            error.set("Error: Atleast one statment is required\nthe function display is not valid, try display(argument)")
            return

        elif token == 6 and token_type == 'IDENTIFIER':
            pass


        elif token == 6 and token_type != 'IDENTIFIER':
            error.set('Error: variable name expected in display(?)\ndiplsay() takes 1 argument but 0 was given, try display(variablename)')
            return


        elif token == 7 and token_type == 'END_LINE':
             print('End Line: ' + token_value)


        elif token == 7 and token_type != 'END_LINE':
            if token_type == 'IDENTIFIER':
                error.set("Error: Invalid Syntax! display has some invalid parameter\ndisplay must have only one name in it")
                errorMessage()
                return
            else:
                print('\aError: EOL missing!')
                error.set('Error: EOL missing')
                errorMessage()
                return


        elif token == 8 and token_type == 'WHILE_END':
            print('While Body End : ' + token_value)
            error.set('No error found!')
            flag = 1
            break

        elif token == 8 and token_type != 'WHILE_END':
            if token_type in ['DATA_TYPE_DEFINE', 'IDENTIFIER', 'IF_STAT', 'WHILE_STAT', 'DISPLAY_FUNCTION']:
                error.set("Error: Atleast one statment is required inside while body, you have used multiple\nor are you missing to end the --> while")
                errorMessage()
                return
            else:
                error.set('Error: the while body must end before a statement\nyou have not closed the body. end_while missing')
                errorMessage()
                return


        token_checked += 1

    return flag


def parsing_IF_Statement(token_stream):

    flag = 0
    global tokens, token_checked

    for token in range(0, len(token_stream)):

        token_type = tokens[token_checked][1]
        token_value = tokens[token_checked][0]

        if token == 0:
            print('IF START: ' + token_value)

        elif token == 1 and token_type in ['IDENTIFIER', 'INTEGER']:
            print('Identifier or Integer: ' + token_value)

        elif token == 1 and token_type not in ['IDENTIFIER', 'INTEGER']:
            error.set('Error: the if condition must have valid values to to check')
            errorMessage()
            return

        elif token == 2 and token_type in ['GREATER_THAN', 'LESS_THAN', 'EQUAL_TO', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL']:
            print('Relational operator: ' + token_value)

        elif token == 2 and token_type not in ['GREATER_THAN', 'LESS_THAN', 'EQUAL_TO', 'GREATER_EQUAL', 'LESS_EQUAL', 'NOT_EQUAL']:
            error.set("Error: the conditional operator does not match in the following situation"
                      "\nAre you missing something? try -> gt, lt eq, gte, lte, ne")
            errorMessage()
            return

        elif token == 3 and token_type in ['IDENTIFIER', 'INTEGER']:
            print('Identifier or Integer: ' + token_value)

        elif token == 3 and token_type not in ['IDENTIFIER', 'INTEGER']:
            error.set('Error: the if condition must have valid values to to check')
            errorMessage()
            return

        elif token == 4 and token_type == 'IF_STAT_START':
            print('If Body Start: ' + token_value)

        elif token == 4 and token_type != 'IF_STAT_START':
            error.set('Error: the if body must have a start, are you missing something there\nstart_if missing')
            errorMessage()
            return

        elif token == 5 and token_type == 'DISPLAY_FUNCTION':
            print('Display: ' + token_value)


        elif token == 5 and token_type != 'DISPLAY_FUNCTION':
            error.set("Error: Atleast one statment is required\nthe function display is not valid, try display(argument)")
            return

        elif token == 6 and token_type == 'IDENTIFIER':
            pass


        elif token == 6 and token_type != 'IDENTIFIER':
            error.set('Error: variable name expected in display(?)\ndiplsay() takes 1 argument but 0 was given, try display(variablename)')
            return


        elif token == 7 and token_type == 'END_LINE':
             print('End Line: ' + token_value)



        elif token == 7 and token_type != 'END_LINE':
            if token_type == 'IDENTIFIER':
                error.set("Error: Invalid Syntax! display has some invalid parameter\ndisplay must have only one name in it")
                errorMessage()
                return
            else:
                print('\aError: EOL missing!')
                error.set('Error: EOL missing')
                errorMessage()
                return


        elif token == 8 and token_type == 'IF_STAT_END':
            print('If Body End : ' + token_value)
            error.set('No error found!')
            flag = 1
            break

        elif token == 8 and token_type != 'IF_STAT_END':
            if token_type in ['DATA_TYPE_DEFINE', 'IDENTIFIER', 'IF_STAT', 'WHILE_STAT', 'DISPLAY_FUNCTION ']:
                error.set("Error: Atleast one statment is required inside if body, you have used multiple\nor are you missing to end the --> if")
                errorMessage()
                return
            else:
                error.set('Error: the if body must end before a statement\nyou have not closed the body. end_if missing')
                errorMessage()
                return


        token_checked += 1

    return flag


def parsing_variable_initialization_or_arithmatic_operation(token_stream):

    global tokens, token_checked
    flag = 0

    for token in range(0, len(token_stream)):

        token_type = tokens[token_checked][1]
        token_value = tokens[token_checked][0]

        if token == 0:
            print('Data Type Define: ' + token_value)

        elif token == 1 and token_type == 'IDENTIFIER':
            print('Variable Name: ' + token_value)

        elif token == 1 and token_type != 'IDENTIFIER':
            print('Error: Invalid Name defined!')
            error.set('Invalid Name defined!')
            errorMessage()
            return

        elif token == 2 and token_type == 'OPERATOR':
            print('Assignment Operator: ' + token_value)

        elif token == 2 and token_type != 'OPERATOR':
            if token_type == 'END_LINE':
                print('End Line: ' + token_value)
                error.set("No error found!")
                return
            else:
                print('Error: Invalid! operator = required')
                error.set('Error: Invalid! operator = required')
                errorMessage()
                return


        elif token == 3 and token_type in ['INTEGER', 'IDENTIFIER']:
            print('Variable Value: ' + token_value)

        elif token == 3 and token_type not in ['INTEGER', 'IDENTIFIER']:
            print('Error: Invalid Assignment!')
            error.set('Error: Invalid Assignment!')
            errorMessage()
            return


        elif token == 4 and token_type == 'END_LINE':
            error.set("No error found!")
            flag = 1
            break

        elif token == 4 and token_type != 'END_LINE':

            if token_type in ['PLUS_OPERATOR', 'MINUS_OPERATOR', 'MULTIPLY_OPERATOR', 'DIVISION_OPERATOR']:
                print(token_type + ':  ' + token_value)

            elif token_type in ['INTEGER', 'IDENTIFIER']:
                error.set("Error: are you missing an operation between them")
                errorMessage()
                return
            else:
                error.set("Error: EOL missing!")
                errorMessage()
                return


        elif token == 5 and token_type in ['INTEGER', 'IDENTIFIER']:
            print(token_type + ': ' + token_value)


        elif token == 5 and token_type not in ['INTEGER', 'IDENTIFIER']:
            error.set("Error: two values required for the operation!")
            errorMessage()
            return


        elif token == 6 and token_type == 'END_LINE':
            error.set("No error found!")
            flag = 1
            break

        elif token == 6 and token_type != 'END_LINE':
            print('Error: EOL missing!')
            error.set("Error: EOL missing!")
            errorMessage()

        token_checked += 1

    return flag



def display_argument_packing_and_parsing(token_stream):

    global token_checked
    global tokens

    flag = 0

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


        if token == 0:
            print('Display and Argument: ' + token_value)


        elif token == 1 and token_type == 'IDENTIFIER':
            pass

        elif token == 1 and token_type != 'IDENTIFIER':
            error.set('Error: variable name expected in display(?)\ndiplsay() takes 1 argument but 0 was given, try display(variablename)')
            return


        elif token == 2 and token_type == 'END_LINE':
            flag = 1
            break

        elif token == 2 and token_type != 'END_LINE':
            if token_type == 'IDENTIFIER':
                error.set("Error: Invalid Syntax! display has some invalid parameter\ndisplay must have only one name in it")
                errorMessage()
                return
            else:
                print('\aError: EOL missing!')
                error.set('Error: EOL missing')
                errorMessage()
                return

        token_checked += 1

    return flag




# ---------------------------------------------------------------------------

lblHeader = Label(root, text="Write your code here or click on browse for a file", fg='blue', relief="solid", font="Arial 11 bold", pady=5, padx=155)
lblHeader.grid(row=0, column=0, sticky=W)


# Text Widget to add Code Part
codeArea = Text(root, width=80, height=15, wrap=WORD, bd=5, padx=3, pady=3, bg='grey', fg="white", font="Consolos 11 bold")
codeArea.grid(row=1, column=0, sticky=W)

# Button Widget to Browse for a file
btnBrowse = Button(root, text="Browse File", command=browse)
btnBrowse.grid(row=2, column=0, sticky=S)


# Button Widget to Parse the Entire code in the text area and find out errors
btnParse = Button(root, text="Parse Code", command=main)
btnParse.grid(row=3, column=0)


# Label Widget to detect error while parsing
lblError = Label(root, textvariable=error, fg="red", font="Arial 11 bold")
lblError.grid(row=5, column=0, sticky=W)

lblDash = Label(root, text="Error Window", font="Calibri 12 bold")
lblDash.grid(row=4, column=0, sticky=W)

grammerbtn = Button(root, text='Need Help regarding language\nClick Here', fg='red', command=grammer)
grammerbtn.grid(row=2,column=0, sticky=E)

root.mainloop()
