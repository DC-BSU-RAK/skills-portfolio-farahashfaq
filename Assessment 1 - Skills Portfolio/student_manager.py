import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from PIL import Image, ImageTk

FILENAME = "studentMarks.txt"

def load_students():
    if not os.path.exists(FILENAME):
        messagebox.showerror("Error", f"{FILENAME} not found")
        return []

    with open(FILENAME, "r") as f:
        lines = f.read().strip().split("\n")

    if not lines:
        return []

    count = int(lines[0])
    students = []

    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) < 6:
            continue
        code = parts[0]
        name = parts[1]
        c1, c2, c3 = map(int, parts[2:5])
        exam = int(parts[5])
        students.append({
            "code": code,
            "name": name,
            "cmarks": [c1, c2, c3],
            "exam": exam
        })

    return students

def save_students(students):
    with open(FILENAME, "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            line = (
                f"{s['code']},{s['name']},"
                f"{s['cmarks'][0]},{s['cmarks'][1]},{s['cmarks'][2]},"
                f"{s['exam']}\n"
            )
            f.write(line)

# Calculations 

def total_coursework(c):
    return sum(c)

def total_percentage(c, exam):
    return ((sum(c) + exam) / 160) * 100

def get_grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("900x600")
        self.root.config(bg="#1a1a1a")

        self.students = load_students()

        # panel
        self.panel = tk.Frame(root, bg="#71aadf", bd=2, relief="ridge")
        self.panel.place(x=20, y=20, width=860, height=560)

        # background image 
        img = Image.open("gridpg.jpeg").convert("RGBA")  
        img = img.resize((860, 560))

        # Semi-transparent overlay 
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 120)) 
        blended = Image.alpha_composite(img, overlay)

        self.bg_img = ImageTk.PhotoImage(blended)
        self.bg_label = tk.Label(self.panel, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Buttons on left
        button_frame = tk.Frame(self.panel, bg="#28365E")
        button_frame.place(x=20, y=20)

        style = ttk.Style()
        style.configure("TButton",
                        font=("Segoe UI", 11),
                        padding=6)

        btns = [
            ("1. View All Students", self.view_all),
            ("2. View Individual Student", self.view_individual),
            ("3. Highest Score", self.show_highest),
            ("4. Lowest Score", self.show_lowest),
            ("5. Sort Students", self.sort_students),
            ("6. Add Student", self.add_student),
            ("7. Delete Student", self.delete_student),
            ("8. Update Student", self.update_student),
        ]

        for text, cmd in btns:
            ttk.Button(button_frame, text=text, command=cmd, width=25)\
                .pack(pady=5)

        # Output box
        self.output = tk.Text(self.panel, width=60, height=26, font=("Consolas", 11))
        self.output.place(x=300, y=20)

    def show_student(self, s):
        cw = total_coursework(s["cmarks"])
        p = total_percentage(s["cmarks"], s["exam"])
        grade = get_grade(p)

        return (
            f"Name: {s['name']}\n"
            f"Code: {s['code']}\n"
            f"Coursework Total: {cw}/60\n"
            f"Exam Mark: {s['exam']}/100\n"
            f"Percentage: {p:.2f}%\n"
            f"Grade: {grade}\n"
            f"{'-'*40}\n"
        )

    def clear(self):
        self.output.delete("1.0", tk.END)

    def view_all(self):
        self.clear()
        total = 0

        for s in self.students:
            self.output.insert(tk.END, self.show_student(s))
            total += total_percentage(s["cmarks"], s["exam"])

        avg = total / len(self.students) if self.students else 0
        self.output.insert(tk.END, f"\nTotal Students: {len(self.students)}\n")
        self.output.insert(tk.END, f"Average Percentage: {avg:.2f}%")

    def view_individual(self):
        code = simpledialog.askstring("Search", "Enter Student Code:")
        if not code: return

        for s in self.students:
            if s["code"] == code:
                self.clear()
                self.output.insert(tk.END, self.show_student(s))
                return

        messagebox.showerror("Error", "Student not found")

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students found")
            return
        best = max(self.students, key=lambda s: total_percentage(s["cmarks"], s["exam"]))
        self.clear()
        self.output.insert(tk.END, self.show_student(best))

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students found")
            return
        worst = min(self.students, key=lambda s: total_percentage(s["cmarks"], s["exam"]))
        self.clear()
        self.output.insert(tk.END, self.show_student(worst))

    def sort_students(self):
        if not self.students:
            messagebox.showinfo("Info", "No students to sort")
            return
        asc = messagebox.askyesno("Sort", "Sort ascending? (Yes=Asc, No=Desc)")
        self.students.sort(
            key=lambda s: total_percentage(s["cmarks"], s["exam"]),
            reverse=not asc
        )
        self.view_all()

    def add_student(self):
        code = simpledialog.askstring("Add", "Enter student code:")
        name = simpledialog.askstring("Add", "Enter name:")
        c1 = int(simpledialog.askstring("Add", "Coursework 1:"))
        c2 = int(simpledialog.askstring("Add", "Coursework 2:"))
        c3 = int(simpledialog.askstring("Add", "Coursework 3:"))
        exam = int(simpledialog.askstring("Add", "Exam:"))

        self.students.append({
            "code": code,
            "name": name,
            "cmarks": [c1, c2, c3],
            "exam": exam
        })

        save_students(self.students)
        messagebox.showinfo("Student added")

    def delete_student(self):
        code = simpledialog.askstring("Delete", "Enter student code:")
        for s in self.students:
            if s["code"] == code:
                self.students.remove(s)
                save_students(self.students)
                messagebox.showinfo("Student deleted")
                return
        messagebox.showerror("Error", "Student not found")

    def update_student(self):
        code = simpledialog.askstring("Update", "Enter student code:")
        for s in self.students:
            if s["code"] == code:
                new_exam = simpledialog.askstring("Exam", f"New exam mark ({s['exam']}):")
                new_c1 = simpledialog.askstring("CW1", f"New CW1 ({s['cmarks'][0]}):")
                new_c2 = simpledialog.askstring("CW2", f"New CW2 ({s['cmarks'][1]}):")
                new_c3 = simpledialog.askstring("CW3", f"New CW3 ({s['cmarks'][2]}):")

                if new_exam: s["exam"] = int(new_exam)
                if new_c1: s["cmarks"][0] = int(new_c1)
                if new_c2: s["cmarks"][1] = int(new_c2)
                if new_c3: s["cmarks"][2] = int(new_c3)

                save_students(self.students)
                messagebox.showinfo("Record updated")
                return

        messagebox.showerror("Student not found")

root = tk.Tk()
app = StudentManager(root)
root.mainloop()
