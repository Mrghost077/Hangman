import random

words = ("apple", "banana", "monkey", "cat")
hangman = {0: ("     ",
               "     ",
               "     "),
           1: ("  O  ",
               "     ",
               "     "),
           2: ("  O  ",
               "  |  ",
               "     "),
           3: ("  O  ",
               " /|  ",
               "     "),
           4: ("  O  ",
               " /|\\",
               "     "),
           5: ("  O  ",
               " /|\\",
               " /   "),
           6: ("  O  ",
               " /|\\",
               " / \\")}

def display_man(tries):
    pass

def display_hint(hint):
    pass

def display_word(word):
    pass

def main():
    pass



# this file runs when the file is executed directly and prevents this file from
#running when it is imported
if __name__ == "__main__":
    main()

