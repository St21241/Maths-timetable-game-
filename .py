import random
import tkinter as tk
import ctypes

class AgeVerification:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Verification")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}")  # Set window size to cover the whole screen
        self.set_bg_color("#38b6ff")  # Set background color
        
        self.age_label = tk.Label(root, text="Enter your age:", font=("Anton", 40))
        self.age_label.pack(pady=20)
        
        self.age_entry = tk.Entry(root, font=("Anton", 30))
        self.age_entry.pack(pady=10)
        
        self.verify_btn = tk.Button(root, text="Verify", font=("Anton", 40), command=self.verify_age)
        self.verify_btn.pack()

    def set_bg_color(self, color):
        self.root.configure(bg=color)
        for widget in self.root.winfo_children():
            widget.configure(bg=color)

    def verify_age(self):
        try:
            age = int(self.age_entry.get())
            if 7 <= age <= 18:
                self.root.destroy()  # Close age verification window
                self.open_level_selection()
            else:
                self.show_age_error()
        except ValueError:
            self.show_age_error()

    def show_age_error(self):
        error_label = tk.Label(self.root, text="You must be between 7 and 18 years old to play.", fg="red", font=("Anton", 30))
        error_label.pack(pady=10)

    def open_level_selection(self):
        root = tk.Tk()
        game_gui = TimesTableGameGUI(root)
        root.mainloop()

class TimesTableGame:
    def __init__(self, level):
        self.level = level
        self.current_question = 0
        self.score = 0
        self.questions = 5
        self.questions_list = []
        self.user_answers = []

        self.generate_questions()

    def generate_questions(self):
        max_multiplier = 0
        if self.level == 1:
            max_multiplier = 5
        elif self.level == 3:
            max_multiplier = 9
        elif self.level == 5:
            max_multiplier = 12

        for _ in range(self.questions):
            num1 = random.randint(2, max_multiplier)
            num2 = random.randint(2, max_multiplier)
            self.questions_list.append((num1, num2))

    def check_answer(self, user_answer):
        correct_answer = self.questions_list[self.current_question][0] * self.questions_list[self.current_question][1]
        if user_answer == correct_answer:
            self.score += 1
        self.user_answers.append((self.questions_list[self.current_question], user_answer, correct_answer))
        self.current_question += 1

    def get_current_question(self):
        return self.questions_list[self.current_question]

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.current_question == self.questions

    def get_user_answers(self):
        return self.user_answers

    def get_options(self):
        num1, num2 = self.questions_list[self.current_question]
        options = [num1 * num2]

        while len(options) < 4:
            wrong_answer = random.randint(2, 144)
            if wrong_answer != num1 * num2 and wrong_answer not in options:
                options.append(wrong_answer)

        random.shuffle(options)

        options_with_letters = [f"{chr(65 + i)}. {option}" for i, option in enumerate(options)]
        return options_with_letters

class TimesTableGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiplication Game")
        self.set_bg_color("#38b6ff")
        self.game_title_label = tk.Label(root, text="Multiplication Game", font=("Anton", 100, "bold"))
        self.game_title_label.pack(pady=20)
        self.level_frame = tk.Frame(root)
        self.level_frame.pack(pady=20)
        self.level1_btn = tk.Button(self.level_frame, text="Level 1", font=("Anton", 40), command=lambda: self.start_game(1))
        self.level2_btn = tk.Button(self.level_frame, text="Level 2", font=("Anton", 40), command=lambda: self.start_game(2))
        self.level3_btn = tk.Button(self.level_frame, text="Level 3", font=("Anton", 40), command=lambda: self.start_game(3))
        self.level1_btn.pack(side=tk.LEFT, padx=10)
        self.level2_btn.pack(side=tk.LEFT, padx=10)
        self.level3_btn.pack(side=tk.LEFT, padx=10)
        self.exit_btn = tk.Button(root, text="Exit", font=("Anton", 50), command=root.quit)
        self.exit_btn.pack(pady=75,padx=75)
        self.result_label = tk.Label(root, text="")
        self.score_label = tk.Label(root, text="")
        self.play_again_btn = tk.Button(root, text="Play Again", font=("Anton", 20), command=self.restart_game)
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=20)
        self.game = None

        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        self.root.geometry(f"{screen_width}x{screen_height}")

    def set_bg_color(self, color):
        self.root.configure(bg=color)
        for widget in self.root.winfo_children():
            widget.configure(bg=color)

    def start_game(self, level):
        self.game_title_label.pack_forget()
        self.exit_btn.pack_forget()
        self.level_frame.pack_forget()
        self.game = TimesTableGame(level)
        self.game.generate_questions()
        self.question_label = tk.Label(self.grid_frame, text="", font=("Anton", 40))
        self.question_label.grid(row=0, column=0, columnspan=3, pady=5)
        self.option_buttons = []
        self.ask_question()

    def ask_question(self):
        if not self.game.is_game_over():
            current_question = self.game.get_current_question()
            options = self.game.get_options()
            self.question_label.config(text=f"What is {current_question[0]} x {current_question[1]}?", font=("Anton", 65))
            for button in self.option_buttons:
                button.grid_forget()
            self.option_buttons = []
            for i, option in enumerate(options):
                row, col = divmod(i, 2)
                btn = tk.Button(self.grid_frame, text=str(option), font=("Anton", 100), command=lambda ans=option: self.submit_answer(ans))
                btn.grid(row=row + 1, column=col, padx=15, pady=15, sticky="w")
                if i == 0:
                    btn.config(bg="#38b6ff")
                elif i == 1:
                    btn.config(bg="#ff3838")
                elif i == 2:
                    btn.config(bg="#38ff58")
                elif i == 3:
                    btn.config(bg="#ff38af")
                self.option_buttons.append(btn)
        else:
            self.show_results()

    def submit_answer(self, user_answer):
        self.game.check_answer(user_answer)
        for button in self.option_buttons:
            button.grid_forget()
        self.ask_question()

    def show_results(self):
        self.question_label.grid_forget()
        self.result_label.config(text="Game Over!", font=("Anton", 40))
        self.score_label.config(text=f"Your score: {self.game.get_score()} / {self.game.questions}", font=("Anton", 20))
        self.view_answers_btn = tk.Button(self.grid_frame, text="View Answers", font=("Anton", 16), command=self.show_answers)
        self.view_answers_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def show_answers(self):
        self.view_answers_btn.grid_forget()
        self.score_label.grid_forget()
        self.result_label.config(text="Your Answers:", font=("Anton", 20))

        # Destroy the previous answers_frame if it exists
        if hasattr(self, 'answers_frame'):
            self.answers_frame.destroy()

        self.answers_frame = tk.Frame(self.root)
        self.answers_frame.pack(pady=10)
        self.back_btn = tk.Button(self.answers_frame, text="Back", font=("Anton", 0), command=self.show_main_interface)
        self.back_btn.pack(anchor=tk.N, padx=10, pady=10)
        self.current_question = 0
        self.show_next_answer()

    def show_next_answer(self):
        if self.current_question < self.game.questions:
            current_question, user_answer, correct_answer = self.game.get_user_answers()[self.current_question]
            question_text = f"{current_question[0]} x {current_question[1]} = "
            user_answer_text = f"Your Answer: {user_answer}"
            correct_answer_text = f"Correct Answer: {correct_answer}"
            tk.Label(self.answers_frame, text=f"Question {self.current_question + 1}: {question_text}", font=("Anton", 12)).pack(anchor=tk.W)
            tk.Label(self.answers_frame, text=user_answer_text, font=("Anton", 12)).pack(anchor=tk.W)
            tk.Label(self.answers_frame, text=correct_answer_text, font=("Anton", 12)).pack(anchor=tk.W)
            self.current_question += 1
            self.next_btn = tk.Button(self.answers_frame, text="Next", font=("Anton", 16), command=self.show_next_answer)
            self.next_btn.pack(pady=10)
        else:
            self.show_play_again_interface()

    def show_play_again_interface(self):
        self.answers_frame.pack_forget()
        self.back_btn.pack_forget()
        self.play_again_frame = tk.Frame(self.root)
        self.play_again_frame.pack(pady=10)
        play_again_btn = tk.Button(self.play_again_frame, text="Play Again", font=("Anton", 16), command=self.restart_game)
        play_again_btn.pack(pady=10)

        well_played_label = tk.Label(self.play_again_frame, text="Well Played!", font=("Anton", 30))
        well_played_label.pack(pady=10)

        self.game_title_label.pack()
        self.exit_btn.pack()

    def restart_game(self):
        self.play_again_frame.pack_forget()
        self.level_frame.pack(pady=10)
        self.exit_btn.pack(pady=5)

    def show_main_interface(self):
        self.answers_frame.pack_forget()
        self.back_btn.pack_forget()
        self.game_title_label.pack()
        self.level_frame.pack(pady=10)
        self.exit_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    age_verification = AgeVerification(root)
    root.mainloop()
