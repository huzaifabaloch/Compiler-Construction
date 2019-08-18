



def displaySlicing(lexeme):

    start = 0
    end = 0
    disp = ''
    a = 0
    arg = ''

    ''' RETRIEVING START AND END BRACE INDEX OF DISPLAY FUNCTION '''
    for i in range(len(lexeme)):
        if lexeme[i] == '(':
            start = i
        elif lexeme[i] == ')':
            end = i

    print(lexeme)

    if end != 8:
        ''' SLICING THE DISPLAY FUNCTION WITHOUT ARGUMENT '''
        while a != start:
            disp += lexeme[a]
            a += 1

        disp += lexeme[a]
        a += 1

        while a != end:
            arg += lexeme[a]
            a += 1

        disp += lexeme[a]

        displayAndArgument = (disp, arg)

        return displayAndArgument

# ------------ END OF FUNCTION ----------------







def Input(inputFile):

    ''' OPENING AND SPLITING INPUT FILE AKA SOURCE CODE '''
    with open(inputFile, 'r') as fileOpen:
        lexemes = fileOpen.read()
        fileOpen.close()

    lexemesSplit = lexemes.split()

    return lexemesSplit


def SplitCode(code):

    lexeme = code.split()

    # GOAL TO RAISE SYNTAX ERROR IF A DISPLAY FUNCTION HAS ONE SPACE IN IT

    for i in range(len(lexeme)):


        '''
        checking for the occurence of display token, then checking for the closing
        bracket ) of it in the next token because of splitation by whitespace
        and concatenating them together
        the second check is checking if display is not equal to the last lexeme
        and ) bracket in the next token to merge them
        if it is last lexeme, it means user has input one paramter in the display
        function

        '''

        if lexeme[i][:7] == 'display':
             if lexeme[i] != lexeme[-1] and ')' in lexeme[i+1]:
                lexeme[i] += lexeme[i+1]


    return lexeme

# ------------ END OF FUNCTION ----------------






def Symbol(symbolFile):

    ''' HOLD TYPE AND VALUE OF A LEXEME FROM THE SYMBOL TABLE AFTER SPLITING '''
    symbolT = []

    ''' OPENING AND SPLITING SYMBOL TABLE FILE '''
    with open(symbolFile, 'r') as fileOpen:
        symbols = fileOpen.read()
        fileOpen.close()

    symbolsSplit = symbols.split()

    for i in symbolsSplit:
        symbol = i.split('|')
        symbolT.append(symbol)

    return symbolT

# ------------ END OF FUNCTION ----------------





























