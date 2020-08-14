from __future__ import print_function   
def descifrar(message, key):
    message    = message.upper()
    translated = ""
    LETTERS    = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)   
            num = num - key
            if num >= len(LETTERS):
                num -= len(LETTERS)
            elif num < 0:
                num += len(LETTERS)
            translated += LETTERS[num]
        else:
            translated += symbol
    return print(translated)
