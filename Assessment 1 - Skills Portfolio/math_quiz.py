import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance

            #questions and points
TOTAL_QUESTIONS = 10
POINTS_FIRST_TRY = 10
POINTS_SECOND_TRY = 5
            #levels
DIFFICULTIES = {
    "Easy (single-digit)": (1, 9),
    "Moderate (two-digit)": (10, 99),
    "Advanced (four-digit)": (1000, 9999)
}


class MathQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maths Quiz")
        self.geometry("800x500")
        self.resizable(True, True)
        self.minsize(540, 340)

            #Background Image
        self.original_bg = Image.open("bg.jpeg")  # Replace with your file name
        self.bg_photo = ImageTk.PhotoImage(self.original_bg)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<Configure>", self.resize_background)


        self.difficulty_name = None
        self.low = self.high = None
        self.score = 0
        self.q_index = 0
        self.answer = None
        self.attempt = 1

            #colors and fonts
        self.bg_color = "#ffe4ec"   # pastel pink
        self.btn_color = "#ffb6c1"  # button pink
        self.text_color = "#6a1b9a" # cute purple
        self.font_main = ("Comic Sans MS", 12, "bold")
        self.font_title = ("Comic Sans MS", 18, "bold")

        self.menu_frame = tk.Frame(self, padx=20, pady=20, bg=self.bg_color, bd=4, relief="ridge")
        self.quiz_frame = tk.Frame(self, padx=20, pady=20, bg=self.bg_color, bd=4, relief="ridge")

        self.build_menu()
        self.build_quiz()
        self.show_menu()

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height
        resized = self.original_bg.resize((new_width, new_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.bg_label.configure(image=self.bg_photo)
        self.bg_label.image = self.bg_photo

            #Main Menu 
    def build_menu(self):
        tk.Label(
            self.menu_frame, text="🐱 Choose Your Level!", font=self.font_title,
            bg=self.bg_color, fg=self.text_color
        ).pack(pady=10)

        for name in DIFFICULTIES.keys():
            btn = tk.Button(
                self.menu_frame,
                text=name,
                width=28,
                font=self.font_main,
                bg=self.btn_color,
                fg="white",
                activebackground="#ff99cc",
                relief="raised",
                bd=3,
                command=lambda n=name: self.start_quiz(n)
            )
            btn.pack(pady=6)

        tk.Label(
            self.menu_frame,
            text="✨ Good Luck ✨",
            font=("Comic Sans MS", 10, "italic"),
            bg=self.bg_color,
            fg="#a82d73"
        ).pack(pady=10)

    def show_menu(self):
        self.quiz_frame.pack_forget()
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

            #quiz UI
    def build_quiz(self):
        top = tk.Frame(self.quiz_frame, bg=self.bg_color)
        top.pack(fill="x")

        self.score_var = tk.StringVar(value="Score: 0 / 100    |    Q: 0 / 10")
        tk.Label(top, textvariable=self.score_var, font=self.font_main,
                    bg=self.bg_color, fg=self.text_color).pack(anchor="w")

        self.diff_var = tk.StringVar(value="")
        tk.Label(top, textvariable=self.diff_var, font=("Comic Sans MS", 10),
                    bg=self.bg_color, fg=self.text_color).pack(anchor="w", pady=(2, 10))

        qwrap = tk.Frame(self.quiz_frame, bg=self.bg_color)
        qwrap.pack(pady=10, fill="x")

        self.question_var = tk.StringVar(value="")
        tk.Label(qwrap, textvariable=self.question_var, font=("Comic Sans MS", 22, "bold"),
                    bg=self.bg_color, fg="#ff4081").pack()

        inrow = tk.Frame(self.quiz_frame, bg=self.bg_color)
        inrow.pack(pady=8)

        tk.Label(inrow, text=" Your answer:", font=self.font_main,
                    bg=self.bg_color, fg=self.text_color).pack(side="left")
        self.entry = tk.Entry(inrow, width=12, font=("Comic Sans MS", 16),
                                justify="center", bd=3, relief="sunken")
        self.entry.pack(side="left", padx=8)
        self.entry.bind("<Return>", lambda e: self.check_answer())

        self.submit_btn = tk.Button(self.quiz_frame, text=" Submit ", font=self.font_main,
                                    command=self.check_answer, bg="#ffb6c1",
                                    fg="white", activebackground="#ff99cc",
                                    bd=3, relief="ridge")
        self.submit_btn.pack(pady=6)

        self.feedback_var = tk.StringVar(value="")
        tk.Label(self.quiz_frame, textvariable=self.feedback_var, font=("Comic Sans MS", 12, "italic"),
                    bg=self.bg_color, fg="#7b1fa2").pack(pady=6)

        self.next_btn = tk.Button(self.quiz_frame, text="Next ➡️", state="disabled",
                                    command=self.next_question, bg="#f8bbd0",
                                    fg="#6a1b9a", font=self.font_main, bd=3, relief="ridge")
        self.next_btn.pack(pady=6)

        self.result_label = tk.Label(self.quiz_frame, text="", font=("Comic Sans MS", 14, "bold"),
                                        bg=self.bg_color, fg="#d81b60")
        self.result_label.pack(pady=8)

        self.quit_btn = tk.Button(self.quiz_frame, text="❌ Quit Game", command=self.on_quit,
                                    bg="#ffcdd2", fg="#c2185b", font=self.font_main,
                                    bd=3, relief="ridge")
        self.quit_btn.pack(pady=(12, 0))

    def start_quiz(self, diff_name):
        self.menu_frame.place_forget()
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.difficulty_name = diff_name
        self.low, self.high = DIFFICULTIES[diff_name]
        self.diff_var.set(f"Difficulty: {self.difficulty_name}")

        self.score = 0
        self.q_index = 0
        self.attempt = 1
        self.result_label.config(text="")
        self.update_scorebar()

        self.feedback_var.set("")
        self.next_btn.config(state="disabled")
        self.submit_btn.config(state="normal")

        self.generate_question()
        self.entry.focus_set()

    def generate_question(self):
        a = random.randint(self.low, self.high)
        b = random.randint(self.low, self.high)
        self.answer = a + b
        self.q_index += 1
        self.attempt = 1
        self.question_var.set(f"Q{self.q_index}:  {a} + {b} = ? ")
        self.entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.update_scorebar()

    def update_scorebar(self):
        self.score_var.set(f" Score: {self.score} / {TOTAL_QUESTIONS * POINTS_FIRST_TRY} | Q: {self.q_index} / {TOTAL_QUESTIONS}")

    def check_answer(self):
        text = self.entry.get().strip()
        if not text.isdigit() and not (text.startswith("-") and text[1:].isdigit()):
            self.feedback_var.set(" Please enter a number, cutie!")
            return

        user = int(text)
        if user == self.answer:
            if self.attempt == 1:
                self.score += POINTS_FIRST_TRY
                self.feedback_var.set("🎉 Yay! You got it right! (+10)")
            else:
                self.score += POINTS_SECOND_TRY
                self.feedback_var.set(" Correct on your 2nd try! (+5)")
            self.finish_current_question()
        else:
            if self.attempt == 1:
                self.attempt = 2
                self.feedback_var.set(" Oops! Try again, sweetie")
                self.entry.delete(0, tk.END)
                self.entry.focus_set()
            else:
                self.feedback_var.set(f"💔 The correct answer was {self.answer}.")
                self.finish_current_question()

        self.update_scorebar()

    def finish_current_question(self):
        self.submit_btn.config(state="disabled")
        self.next_btn.config(state="normal")

        if self.q_index >= TOTAL_QUESTIONS:
            self.show_results()

    def next_question(self):
        if self.q_index < TOTAL_QUESTIONS:
            self.submit_btn.config(state="normal")
            self.next_btn.config(state="disabled")
            self.generate_question()
            self.entry.focus_set()

    def show_results(self):
        total = self.score
        max_score = TOTAL_QUESTIONS * POINTS_FIRST_TRY
        percentage = round((total / max_score) * 100, 2)
        grade = self.get_grade(percentage)

        msg = f"💫 Score: {total}/{max_score}  |  {percentage}%  ({grade})"
        self.result_label.config(text=msg)

        self.submit_btn.config(state="disabled")
        self.next_btn.config(state="disabled")

        self.feedback_var.set(" Quiz complete! Great job, cutie! ")

            #score
    @staticmethod
    def get_grade(pct):
        if pct >= 90:
            return "A+ 🌟"
        if pct >= 80:
            return "A 💖"
        if pct >= 70:
            return "B 🌸"
        if pct >= 60:
            return "C "
        return "F "

            #quit😖
    def on_quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to leave, sweetie? 💔"):
            self.destroy()


if __name__ == "__main__":
    app = MathQuizApp()
    app.mainloop()