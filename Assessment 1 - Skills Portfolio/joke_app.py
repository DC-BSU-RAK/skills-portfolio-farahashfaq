import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
from PIL import Image, ImageTk

# jokes section
DEFAULT_JOKES = [
    "Why did the chicken cross the road?To get to the other side.",
    "What happens if you boil a clown?You get a laughing stock.",
    "Why did the car get a flat tire?Because there was a fork in the road!",
    "How did the hipster burn his mouth?He ate his pizza before it was cool.",
    "What did the janitor say when he jumped out of the closet?SUPPLIES!!!!",
    "Have you heard about the band 1023MB?It's probably because they haven't got a gig yet…",
    "Why does the golfer wear two pants?Because he's afraid he might get a Hole-in-one.",
    "Why should you wear glasses to maths class?Because it helps with division.",
    "Why does it take pirates so long to learn the alphabet?Because they could spend years at C.",
    "Why did the woman go on the date with a mushroom?Because he was a fun-ghi.",
    "Why do bananas never get lonely?Because they hang out in bunches.",
    "What did the buffalo say when his kid went to college?Bison.",
    "Why shouldn't you tell secrets in a cornfield?Too many ears.",
    "What do you call someone who doesn't like carbs?Lack-Toast Intolerant.",
    "Why did the can crusher quit his job?Because it was soda pressing.",
    "Why did the birthday boy wrap himself in paper?He wanted to live in the present.",
    "What does a house wear?A dress.",
    "Why couldn't the toilet paper cross the road?Because it got stuck in a crack.",
    "Why didn't the bike want to go anywhere?Because it was two-tired!",
    "Want to hear a pizza joke?Nahhh, it's too cheesy!",
    "Why are chemists great at solving problems?Because they have all of the solutions!",
    "Why is it impossible to starve in the desert?Because of all the sand which is there!",
    "What did the cheese say when it looked in the mirror?Halloumi!",
    "Why did the developer go broke?Because he used up all his cache.",
    "Did you know that ants are the only animals that don't get sick?It's true! It's because they have little antibodies.",
    "Why did the donut go to the dentist?To get a filling.",
    "What do you call a bear with no teeth?A gummy bear!",
    "What does a vegan zombie like to eat?Graaains.",
    "What do you call a dinosaur with only one eye?A Do-you-think-he-saw-us!",
    "Why should you never fall in love with a tennis player?Because to them... love means NOTHING!:",
    "What did the full glass say to the empty glass?You look drunk.",
    "What's a potato's favorite form of transportation?The gravy train",
    "What did one ocean say to the other?Nothing, they just waved.",
    "What did the right eye say to the left eye?Honestly, between you and me something smells.",
    "What do you call a dog that's been run over by a steamroller?Spot!",
    "What's the difference between a hippo and a zippo?One's pretty heavy and the other's a little lighter",
    "Why don't scientists trust Atoms?They make up everything."
]

# file info

def ensure_joke_file(filename="randomJokes.txt"):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            for line in DEFAULT_JOKES:
                f.write(line + "\n")

def load_jokes(filename="randomJokes.txt"):
    jokes = []
    ensure_joke_file(filename)
    with open(filename, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line:
                continue
            if "?" not in line:
                print(f"Skipping line {lineno}: no '?' found")
                continue
            setup, punchline = line.split("?", 1)
            setup = setup.strip()
            punchline = punchline.strip()
            if not punchline:
                print(f"Skipping line {lineno}: no punchline")
                continue
            if not setup.endswith("?"):
                setup += "?"
            jokes.append((setup, punchline))
    return jokes

def add_new_joke(setup, punchline, filename="randomJokes.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{setup}?{punchline}\n")



# themes
THEMES = {
    "Light Pink": {"bg": "#ffb6e6", "accent": "#ff69b4", "panel": "#fffafa"},
    "Deep Pink": {"bg": "#ff5ca8", "accent": "#ff2f92", "panel": "#f71e8e"},
    "Black": {"bg": "#241d20", "accent": "#585858", "panel": "#8d8d8d"},
    "Red": {"bg": "#e62222", "accent": "#da3434", "panel": "#992a09"},
}



# main setup for app
class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Machine")
        self.theme = "Light Pink"

        self.jokes = load_jokes()
        self.current_joke = None

        self.apply_theme()

        # frame 
        self.main_frame = tk.Frame(root, bg=self.panel)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # GIF
        try:
            self.gif = Image.open("200.webp")
            self.gif_frames = []
            for frame in range(self.gif.n_frames):
                self.gif.seek(frame)
                self.gif_frames.append(ImageTk.PhotoImage(self.gif.copy().resize((120, 120))))
            self.gif_index = 0
            self.gif_label = tk.Label(self.main_frame, bg=self.panel)
            self.gif_label.pack(pady=5)
            self.animate_gif()
        except:
            pass

        # top text
        self.title_label = tk.Label(
            self.main_frame, text="Joke Machine",
            font=("Comic Sans MS", 22, "bold"),
            fg=self.accent, bg=self.panel)
        self.title_label.pack(pady=12)

        # setup
        self.setup_label = tk.Label(
            self.main_frame, text="Press Alexa tell me a joke",
            font=("Comic Sans MS", 15),
            fg="#ff6d6d", bg=self.panel, wraplength=580, justify="center")
        self.setup_label.pack(pady=10)

        # punchline
        self.punchline_label = tk.Label(
            self.main_frame, text="",
            font=("Comic Sans MS", 14, "italic"),
            fg=self.accent, bg=self.panel, wraplength=580, justify="center")
        self.punchline_label.pack(pady=6)

        # button and content
        btn_frame = tk.Frame(self.main_frame, bg=self.panel)
        btn_frame.pack(pady=14)

        self.alexa_btn = self.rounded_button(btn_frame, "Alexa tell me a Joke", self.new_joke)
        self.alexa_btn.grid(row=0, column=0, padx=10)

        self.show_btn = self.rounded_button(btn_frame, "Show Punchline", self.show_punchline, state="disabled")
        self.show_btn.grid(row=0, column=1, padx=10)

        self.next_btn = self.rounded_button(btn_frame, "Next ➜", self.new_joke)
        self.next_btn.grid(row=0, column=2, padx=10)

        # theme switch
        self.theme_menu = ttk.Combobox(self.main_frame, values=list(THEMES.keys()))
        self.theme_menu.set("Light Pink")
        self.theme_menu.bind("<<ComboboxSelected>>", self.switch_theme)
        self.theme_menu.pack(pady=5)

        # extra addition jokes section
        self.add_section()

    # style of button
    def rounded_button(self, frame, text, cmd, state="normal"):
        return tk.Button(
            frame, text=text, command=cmd, state=state,
            font=("Comic Sans MS", 11, "bold"), bg=self.accent, fg="white",
            relief="flat", bd=0, padx=16, pady=8
        )

    # theme system
    def apply_theme(self):
        t = THEMES[self.theme]
        self.bg = t["bg"]
        self.accent = t["accent"]
        self.panel = t["panel"]
        self.root.config(bg=self.bg)

    def switch_theme(self, event):
        self.theme = self.theme_menu.get()
        self.apply_theme()
        self.main_frame.config(bg=self.panel)

    # GIF animation
    def animate_gif(self):
        try:
            self.gif_label.config(image=self.gif_frames[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.root.after(120, self.animate_gif)
        except:
            pass

    # new joke
    def new_joke(self):
        if not self.jokes:
            messagebox.showwarning("No jokes", "No jokes to show!")
            return
        choice = random.choice(self.jokes)
        while choice == self.current_joke and len(self.jokes) > 1:
            choice = random.choice(self.jokes)
        self.current_joke = choice
        self.setup_label.config(text=choice[0])
        self.punchline_label.config(text="")
        self.show_btn.config(state="normal")

    # display punchline
    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
            self.show_btn.config(state="disabled")

    # add joke section
    def add_section(self):
        section = tk.LabelFrame(
            self.main_frame, text="Add Your Own Joke",
            bg=self.panel, fg=self.accent,
            font=("Comic Sans MS", 12, "bold")
        )
        section.pack(pady=14)

        tk.Label(section, text="Setup (question):", bg=self.panel, fg="#7d2caf").grid(row=0, column=0)
        tk.Label(section, text="Punchline:", bg=self.panel, fg="#7d2caf").grid(row=1, column=0)

        self.new_setup = tk.Entry(section, width=40)
        self.new_setup.grid(row=0, column=1, pady=5)

        self.new_punch = tk.Entry(section, width=40)
        self.new_punch.grid(row=1, column=1, pady=5)

        save_btn = self.rounded_button(section, "Add Joke", self.save_new_joke)
        save_btn.grid(row=2, column=0, columnspan=2, pady=6)

    def save_new_joke(self):
        s = self.new_setup.get().strip()
        p = self.new_punch.get().strip()
        if not s or not p:
            messagebox.showerror("Missing info", "Please fill BOTH fields.")
            return
        add_new_joke(s, p)
        self.jokes = load_jokes()
        messagebox.showinfo("Saved", "Your joke was added!")
        self.new_setup.delete(0, "end")
        self.new_punch.delete(0, "end")

# app run 
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
