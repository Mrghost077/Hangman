import random
from wordList import words
from arts import hangman_ghost_art
from arts import hangman


def display_man(tries):
    print ("*********")
    for line in hangman[tries]:
        print(line)
    print ("*********")

def display_hint(hint):
    print(" ".join(hint))

def display_word(hidden_word):
    print(" ".join(hidden_word))

def main():
    print(hangman_ghost_art)
    hidden_word = random.choice(words)
    hint = ["_"] * len(hidden_word)
    tries = 0
    guessed_letters = set()
    run_status = True

    while run_status:
        display_man(tries)
        display_hint(hint)

        guess = input ("Guess a Letter : ").lower()
        

        if len(guess) != 1 :
            print("Invalid Input!! (Hint: You can only type one letter at a time)")
        elif not guess.isalpha():
            print("Invalid Input!! (Hint: You can only type a letter)")
            continue

        if guess in guessed_letters:
            print(f"You already guessed {guess} !")
            continue
            
        guessed_letters.add(guess)

        if guess in hidden_word:
            for i in range(len(hidden_word)):
                if hidden_word[i] == guess:
                    hint[i] = guess
        else:
            tries += 1

        if "_" not in hint:
            display_man(tries)
            print ("YOU WON !!!")
            run_status = False
        elif tries >= len(hangman) - 1:
            display_man(tries)
            display_word(hidden_word)
            print("YOU LOST !!!")
            run_status = False



# this file runs when the file is executed directly and prevents this file from
#running when it is imported
if __name__ == "__main__":
    main()

