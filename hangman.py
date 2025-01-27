import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
from wordList import words
from arts import hangman_ghost_art
from arts import hangman

class HangmanGame:
    incident_storyline = "Find the magic word to save your friend."
    scores_file = 'leaderboard.json'

    def __init__(self, root):
        self.root = root
        self.hidden_word = random.choice(words).upper()
        self.guessed_letters = set()
        self.tries = [0]
        self.setup_gui()

    def setup_gui(self):
        # Set up the root window
        self.root.title("Hangman Game")
        self.root.configure(bg="#2C2C2C")

        # ASCII art intro frame
        self.intro_frame = tk.Frame(self.root, bg="black")
        self.intro_frame.grid(row=0, column=0, columnspan=10, pady=10)
        intro_label = tk.Label(self.intro_frame, text=hangman_ghost_art, font=("Courier", 12), fg="white", bg="black")
        intro_label.pack()

        # Canvas for Hangman
        self.canvas = tk.Canvas(self.root, width=300, height=400, bg="#2C2C2C")

        # Word display (hidden initially)
        self.word_label = tk.Label(self.root, text=" ".join(["_"] * len(self.hidden_word)), font=("Arial", 24), fg="red", bg="#2C2C2C")

        # Schedule the start of the game after 3 seconds
        self.root.after(3000, self.start_game)

    def display_man(self):
        self.canvas.delete("all")
        y_offset = 50
        x_offset = 150
        for i, line in enumerate(hangman[self.tries[0]]):
            self.canvas.create_text(x_offset, y_offset + (i * 45), text=line, font=("Arial", 44), fill="white")
        self.canvas.create_text(x_offset, 350, text=self.incident_storyline, font=("Arial", 12), fill="white", anchor="center")

    def update_word_display(self):
        hint = [letter if letter in self.guessed_letters else "_" for letter in self.hidden_word]
        self.word_label.config(text=" ".join(hint), fg="red")
        return hint

    def calculate_score(self):
        max_tries = len(hangman) - 1
        score = ((max_tries - self.tries[0]) * 100) // max_tries 
        return score

    def save_score(self, player_name, score):
        try:
            with open(self.scores_file, 'r') as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []

        leaderboard.append({'player_name': player_name, 'score': score})
        leaderboard.sort(key=lambda x: x['score'], reverse=True)

        with open(self.scores_file, 'w') as file:
            json.dump(leaderboard, file)

    def display_leaderboard(self):
        try:
            with open(self.scores_file, 'r') as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []

        leaderboard_window = tk.Tk()  # Create a separate Tk instance for the leaderboard
        leaderboard_window.title("Leaderboard")
        leaderboard_window.configure(bg="#2C2C2C")

        tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 18), fg="white", bg="#2C2C2C").pack(pady=10)
        for idx, entry in enumerate(leaderboard[:10]):
            tk.Label(leaderboard_window, text=f"{idx + 1}. {entry['player_name']} - {entry['score']}",
                     font=("Arial", 14), fg="white", bg="#2C2C2C").pack(pady=2)

        def close_leaderboard():
            leaderboard_window.destroy()

        # Schedule the leaderboard window to close after 5 seconds
        leaderboard_window.after(5000, close_leaderboard)

        # Start the main loop for the leaderboard window
        leaderboard_window.mainloop()

    def check_game_status(self, hint):
        if "_" not in hint:
            self.display_man()
            self.word_label.config(text=" ".join(self.hidden_word))
            score = self.calculate_score()
            player_name = simpledialog.askstring("Congratulations!", "You won! Enter your name:")
            if player_name:
                self.save_score(player_name, score)
            if messagebox.askyesno("Game Over", f"YOU WON !!!\nScore: {score}\nThe ghost vanishes, and your friend is saved!\nDo you want to play again?"):
                self.root.destroy()
                main()
            else:
                self.root.destroy()  # Close the game window
                self.display_leaderboard()
        elif self.tries[0] >= len(hangman) - 1:
            self.display_man()
            self.word_label.config(text=" ".join(self.hidden_word))
            score = self.calculate_score()
            if messagebox.askyesno("Game Over", f"YOU LOST !!!\nScore: {score}\nYour friend hangs as the ghost laughs...\nDo you want to play again?"):
                self.root.destroy()
                main()
            else:
                self.root.destroy()  # Close the game window
                self.display_leaderboard()

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            messagebox.showinfo("Info", f"You have already guessed the letter '{letter}'!")
            return

        self.guessed_letters.add(letter)

        # Update hint based on guessed letter
        hint = self.update_word_display()

        if letter not in self.hidden_word:
            self.tries[0] += 1
            self.display_man()
            self.word_label.config(fg="red")
            self.canvas.config(bg="red")
        else:
            self.word_label.config(fg="green")
            self.canvas.config(bg="green")

        self.check_game_status(hint)

    def start_game(self):
        self.intro_frame.destroy()
        
        # Display the canvas for Hangman
        self.canvas.grid(row=1, column=0, columnspan=10, padx=10, pady=10)
        
        self.word_label.grid(row=2, column=0, columnspan=10)

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            tk.Button(self.root, text=letter, width=3, font=("Arial", 14),
                      command=lambda l=letter: self.guess_letter(l),
                      bg="white", fg="black", activebackground="#D32F2F", activeforeground="white").grid(row=3 + i // 10, column=i % 10, padx=5, pady=5)

        self.display_man()

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
