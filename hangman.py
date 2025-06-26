import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.word_categories = {
            "Animals": ["elephant", "giraffe", "kangaroo", "penguin", "dolphin"],
            "Countries": ["canada", "brazil", "japan", "australia", "germany"],
            "Programming": ["python", "javascript", "algorithm", "function", "variable"]
        }
         
        self.word = ""
        self.guessed_letters = []
        self.attempts_left = 6
        self.score = 0
        self.high_score = 0
        self.hints_used = 0
        self.current_difficulty = "Medium"
        
        self.canvas = tk.Canvas(root, width=300, height=300, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        # Setup UI
        self.setup_ui()
        
        # Start new game
        self.choose_category_and_difficulty()
    
    def setup_ui(self):
        # Game info frame
        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        
        # Difficulty label
        self.difficulty_label = tk.Label(
            info_frame, 
            text=f"Difficulty: {self.current_difficulty}", 
            font=("Arial", 12, "bold"), 
            bg="#f0f0f0"
        )
        self.difficulty_label.pack(pady=5)
        
        # Attempts label
        self.attempts_label = tk.Label(
            info_frame, 
            text=f"Attempts left: {self.attempts_left}", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.attempts_label.pack(pady=5)
        
        # Score label
        self.score_label = tk.Label(
            info_frame, 
            text=f"Score: {self.score}", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.score_label.pack(pady=5)
        
        # High score label
        self.high_score_label = tk.Label(
            info_frame, 
            text=f"High Score: {self.high_score}", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.high_score_label.pack(pady=5)
        
        # Hints label
        self.hints_label = tk.Label(
            info_frame, 
            text=f"Hints used: {self.hints_used}/2", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.hints_label.pack(pady=5)
        
        # Word display
        self.word_display = tk.Label(
            self.root, 
            text="", 
            font=("Arial", 24), 
            bg="#f0f0f0"
        )
        self.word_display.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Guessed letters display
        self.guessed_label = tk.Label(
            self.root, 
            text="Guessed letters: ", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.guessed_label.grid(row=2, column=0, columnspan=2, pady=10)
         
        # Keyboard buttons
        self.setup_keyboard()
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(
            control_frame, 
            text="Hint", 
            command=self.give_hint, 
            font=("Arial", 12), 
            bg="#4CAF50", 
            fg="white"
        ).pack(side="left", padx=10)
        
        tk.Button(
            control_frame, 
            text="New Game", 
            command=self.new_game, 
            font=("Arial", 12), 
            bg="#0B3455", 
            fg="white"
        ).pack(side="left", padx=10)
        
        tk.Button(
            control_frame, 
            text="Quit", 
            command=self.root.quit, 
            font=("Arial", 12), 
            bg="#f44336", 
            fg="white"
        ).pack(side="left", padx=10)
    
    def setup_keyboard(self):
        keyboard_frame = tk.Frame(self.root, bg="#f0f0f0")
        keyboard_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # First row (A-M)
        first_row = tk.Frame(keyboard_frame, bg="#f0f0f0")
        first_row.pack()
        
        # Second row (N-Z)
        second_row = tk.Frame(keyboard_frame, bg="#f0f0f0")
        second_row.pack()
        
        # Create letter buttons
        self.letter_buttons = {}
        for letter in 'abcdefghijklm':
            btn = tk.Button(
                first_row, 
                text=letter.upper(), 
                width=3, 
                font=("Arial", 12), 
                command=lambda l=letter: self.guess_letter(l),
                bg="#e0e0e0"
            )
            btn.pack(side="left", padx=2, pady=2)
            self.letter_buttons[letter] = btn
        
        for letter in 'nopqrstuvwxyz':
            btn = tk.Button(
                second_row, 
                text=letter.upper(), 
                width=3, 
                font=("Arial", 12), 
                command=lambda l=letter: self.guess_letter(l),
                bg="#e0e0e0"
            )
            btn.pack(side="left", padx=2, pady=2)
            self.letter_buttons[letter] = btn
    
    def choose_category_and_difficulty(self):
        # Ask for category
        category = simpledialog.askstring(
            "Category", 
            "Choose category:\n(Animals, Countries, Programming)", 
            parent=self.root
        )
        
        if category and category.capitalize() in self.word_categories:
            category = category.capitalize()
        else:
            category = random.choice(list(self.word_categories.keys()))
            messagebox.showinfo("Info", f"Invalid choice. Selected '{category}' randomly.")
        
        # Ask for difficulty
        difficulty = simpledialog.askstring(
            "Difficulty", 
            "Choose difficulty:\n(Easy, Medium, Hard)", 
            parent=self.root
        )
        
        if difficulty and difficulty.capitalize() in ["Easy", "Medium", "Hard"]:
            self.current_difficulty = difficulty.capitalize()
        else:
            self.current_difficulty = "Medium"
            messagebox.showinfo("Info", "Invalid choice. Defaulting to Medium difficulty.")
        
        # Set attempts based on difficulty
        if self.current_difficulty == "Easy":
            self.attempts_left = 8
            word_pool = [w for w in self.word_categories[category] if len(w) <= 6]
        elif self.current_difficulty == "Hard":
            self.attempts_left = 4
            word_pool = [w for w in self.word_categories[category] if len(w) > 6]
        else:  # Medium
            self.attempts_left = 6
            word_pool = self.word_categories[category]
        
        # Select random word
        self.word = random.choice(word_pool).lower()
        self.guessed_letters = []
        self.hints_used = 0
        
        # Update UI
        self.update_word_display()
        self.update_attempts()
        self.update_score()
        self.update_guessed_letters()
        self.update_hints()
        self.difficulty_label.config(text=f"Difficulty: {self.current_difficulty}")
        self.reset_keyboard()
        self.draw_hangman(0)
    
    def update_word_display(self):
        display = []
        for letter in self.word:
            if letter in self.guessed_letters:
                display.append(letter.upper())
            else:
                display.append("_")
        self.word_display.config(text=" ".join(display))
    
    def update_attempts(self):
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
    
    def update_guessed_letters(self):
        self.guessed_label.config(
            text="Guessed letters: " + ", ".join(sorted(self.guessed_letters)).upper()
        )
    
    def update_hints(self):
        self.hints_label.config(text=f"Hints used: {self.hints_used}/2")
    
    def reset_keyboard(self):
        for letter, btn in self.letter_buttons.items():
            btn.config(state="normal", bg="#e0e0e0")
    
    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        
        self.guessed_letters.append(letter)
        self.letter_buttons[letter].config(state="disabled")
        
        if letter in self.word:
            # Correct guess
            self.letter_buttons[letter].config(bg="#a5d6a7")  # Light green
            self.score += 10
        else:
            # Incorrect guess
            self.letter_buttons[letter].config(bg="#ef9a9a")  # Light red
            self.attempts_left -= 1
            self.draw_hangman(6 - self.attempts_left)
        
        self.update_word_display()
        self.update_attempts()
        self.update_score()
        self.update_guessed_letters()
        
        # Check game status
        self.check_game_status()
    
    def give_hint(self):
        if self.hints_used >= 2:
            messagebox.showinfo("Hint", "You've used all your hints!")
            return
        
        unguessed = [letter for letter in self.word if letter not in self.guessed_letters]
        if unguessed:
            hint = random.choice(unguessed)
            self.hints_used += 1
            self.score -= 15  # Penalty for using hint
            messagebox.showinfo("Hint", f"Try the letter: {hint.upper()}")
            self.update_hints()
            self.update_score()
        else:
            messagebox.showinfo("Hint", "No hints needed - you've guessed all letters!")
    
    def check_game_status(self):
        # Check if won
        if all(letter in self.guessed_letters for letter in self.word):
            self.score += self.attempts_left * 20  # Bonus for remaining attempts
            self.update_score()
            self.update_high_score()
            messagebox.showinfo(
                "Congratulations!", 
                f"You won!\nThe word was: {self.word.upper()}\nYour score: {self.score}"
            )
            self.new_game()
            return
        
        # Check if lost
        if self.attempts_left <= 0:
            self.update_high_score()
            messagebox.showinfo(
                "Game Over", 
                f"You lost!\nThe word was: {self.word.upper()}\nYour score: {self.score}"
            )
            self.new_game()
            return
    
    def new_game(self):
        self.choose_category_and_difficulty()
    
    def draw_hangman(self, step):
        self.canvas.delete("all")
        
        # Gallows
        self.canvas.create_line(50, 250, 150, 250, width=3)  # Base
        self.canvas.create_line(100, 250, 100, 50, width=3)  # Pole
        self.canvas.create_line(100, 50, 200, 50, width=3)   # Top
        self.canvas.create_line(200, 50, 200, 80, width=3)   # Rope
        
        if step >= 1:  # Head
            self.canvas.create_oval(180, 80, 220, 120, width=2)
        
        if step >= 2:  # Body
            self.canvas.create_line(200, 120, 200, 180, width=2)
        
        if step >= 3:  # Left arm
            self.canvas.create_line(200, 140, 170, 130, width=2)
        
        if step >= 4:  # Right arm
            self.canvas.create_line(200, 140, 230, 130, width=2)
        
        if step >= 5:  # Left leg
            self.canvas.create_line(200, 180, 170, 210, width=2)
        
        if step >= 6:  # Right leg
            self.canvas.create_line(200, 180, 230, 210, width=2)
        
        # Sad face when game over
        if step >= 6:
            self.canvas.create_line(185, 95, 195, 105, width=2)  # Left eye
            self.canvas.create_line(205, 95, 215, 105, width=2)  # Right eye
            self.canvas.create_arc(185, 110, 215, 130, start=0, extent=-180, width=2)  # Frown

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()