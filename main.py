import tkinter as tks
from gui.mk_quiz import Make_Quiz
from gui.main_menu import Main_Menu
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

"""
QuizMaker

Features:
    - Create your own multiple choice quizzes.

    - Save them to a text file which can be loaded later.

    - Load pre-existing quizzes from text files.

    - Edit quizzes
"""



bg_color = "#054bb4"
font = 'Helvetica'

root = ttk.Window()
style = ttk.Style("sandstone")
root.geometry("600x600")
root.title("QuizMaker")

root.columnconfigure(0, weight=1)

navbar = ttk.Label(root, background='black')
header = ttk.Label(navbar, text="QuizMaker", background="black",
              font=(font, 36),
              foreground="white"
              )
navbar.grid(sticky="EW")
header.grid()

Main_Menu(root, font)
root.mainloop()