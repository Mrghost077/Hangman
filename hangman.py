import tkinter as tk
from tkinter import messagebox
import random
from wordList import words
from arts import hangman_ghost_art
from arts import hangman

incident_storyline = "Find the magic word to save your friend."

# Display hangman on the canvas
def display_man(canvas, tries):
    canvas.delete("all")
    y_offset = 50  
    x_offset = 150 
    for i, line in enumerate(hangman[tries[0]]):
        canvas.create_text(x_offset, y_offset + (i * 45), text=line, font=("Arial", 44), fill="white")  # Center align, increased font size, white color

    # Display storyline
    canvas.create_text(x_offset, 350, text=incident_storyline, font=("Arial", 12), fill="white", anchor="center")

# Update the word display
def update_word_display(hidden_word, guessed_letters, word_label):
    hint = [letter if letter in guessed_letters else "_" for letter in hidden_word]
    word_label.config(text=" ".join(hint), fg="red")  
    return hint

# Check the status of the game
def check_game_status(hidden_word, hint, tries, canvas, word_label, root):
    if "_" not in hint:
        display_man(canvas, tries)
        word_label.config(text=" ".join(hidden_word))
        messagebox.showinfo("Game Over", "YOU WON !!!\nThe ghost vanishes, and your friend is saved!")
        root.quit()
    elif tries[0] >= len(hangman) - 1:
        display_man(canvas, tries)
        word_label.config(text=" ".join(hidden_word))
        messagebox.showinfo("Game Over", "YOU LOST !!!\nYour friend hangs as the ghost laughs...")
        root.quit()

# Handle the letter guess
def guess_letter(letter, hidden_word, guessed_letters, tries, canvas, word_label, root):
    if letter in guessed_letters:
        messagebox.showinfo("Info", f"You have already guessed the letter '{letter}'!")
        return

    guessed_letters.add(letter)

    # Update hint based on guessed letter
    hint = update_word_display(hidden_word, guessed_letters, word_label)

    if letter in hidden_word:
       pass
    else:
        tries[0] += 1  
        display_man(canvas, tries)

    check_game_status(hidden_word, hint, tries, canvas, word_label, root)


# Remove the intro and start the game
def start_game(root, intro_frame, canvas, hidden_word, word_label, guessed_letters, tries):
    intro_frame.destroy()

    # Word display
    word_label.grid(row=2, column=0, columnspan=10)

    # Create buttons for each letter
    for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        tk.Button(root, text=letter, width=3, font=("Arial", 14),
                  command=lambda l=letter: guess_letter(l, hidden_word, guessed_letters, tries, canvas, word_label, root)).grid(row=3 + i // 10, column=i % 10)

    # Start the game
    display_man(canvas, tries)

# Create the Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Hangman Game")

    # Set dark background color
    root.configure(bg="black")

    # ASCII art intro frame
    intro_frame = tk.Frame(root, bg="black")
    intro_frame.grid(row=0, column=0, columnspan=10)
    intro_label = tk.Label(intro_frame, text=hangman_ghost_art, font=("Courier", 10), fg="white", bg="black") 
    intro_label.pack()

    # Canvas for Hangman
    canvas = tk.Canvas(root, width=300, height=400, bg="black") 
    canvas.grid(row=1, column=0, columnspan=10, padx=10, pady=10)

    # Word display (hidden initially)
    hidden_word = random.choice(words).upper()
    word_label = tk.Label(root, text=" ".join(["_"] * len(hidden_word)), font=("Arial", 24), fg="red", bg="black")
    word_label.grid(row=2, column=0, columnspan=10)

    # Set up a set of guessed letters
    guessed_letters = set()
    tries = [0]

    # Schedule the start of the game after 3 seconds
    root.after(3000, start_game, root, intro_frame, canvas, hidden_word, word_label, guessed_letters, tries)

    root.mainloop()

# Run the main game loop
def main():
    create_gui()

# this file runs when the file is executed directly and prevents this file from running when it is imported
if __name__ == "__main__":
    main()
