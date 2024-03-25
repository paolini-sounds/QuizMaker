import tkinter as tk
# from tkinter import ttk
from qm_modules.objects import Question, Quiz, quizzes
from qm_modules.functions import load_from_file, load_sample, list_quiz_files, list_sample_files, delete_file
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import gui.main_menu as menu
from gui.take_quiz import TakeQuiz
from ttkbootstrap.scrolled import ScrolledFrame
from gui.edit_quiz import Edit_Quiz

"""
Show Quizzes:

Creates the page which lists quizzes
Each quiz is listed with option to take quiz, edit quiz, and delete


"""



class Q_title():
    def __init__(self, pframe, title, parent):
        self.title = title
        #keep track of parent to destroy later
        self.parent = parent
        #frame for quiz title and buttons
        self.rect = ttk.Frame(pframe,  width=75, bootstyle='light')
        self.rect.columnconfigure(0, weight=1)
        self.label = ttk.Label(self.rect, width=20, text=title, background="#F8F5F0", font=("helvetica", 18))
        self.rect.grid(sticky="W", pady=5, ipadx=30)
        self.label.grid(row=0, column=0, sticky="W")
        self.takeBtn = ttk.Button(self.rect, text = "Take Quiz", bootstyle="info", command=self.takeQuiz)
        self.takeBtn.grid(row=0, column=1, sticky="E")
        self.editBtn = ttk.Button(self.rect, text="✏️", bootstyle='outline', command=self.editQuiz)
        self.delBtn = ttk.Button(self.rect, text="❌", bootstyle='outline-danger', command=self.deleteQuiz)
        self.editBtn.grid(row=0, column=2)
        self.delBtn.grid(row=0, column=3)

    #destroy current page, load new page with chosen quiz
    def takeQuiz(self):
        curQuiz = load_from_file(self.title)
        self.parent.frame.destroy()
        self.parent.menuBtn.destroy()
        TakeQuiz(curQuiz, self.parent.pframe)

    def editQuiz(self):
        self.parent.menuBtn.destroy()
        self.parent.frame.destroy()
        Edit_Quiz(self.title, self.parent.pframe, menu.Main_Menu)

    def deleteQuiz(self):
        def remove():
            self.rect.destroy()
        def delete():
            delete_file(self.title)
            self.rect.destroy()
        self.msg = ttk.Label(self.rect, background="#F8F5F0", text="Delete the source file, or remove from app?")
        self.removeBtn = ttk.Button(self.rect, text="Remove", command=remove, bootstyle='outline-warning')
        self.delFileBtn = ttk.Button(self.rect, text="Delete File", command=delete, bootstyle='outline-danger')
        self.msg.grid(row=1)
        self.removeBtn.grid(row=2, column=0, sticky="N")
        self.delFileBtn.grid(row=2, column=1, sticky="N")
        
class QuizMenu():
    def __init__(self, root, font, mainMenu):
        self.mainMenu = self
        self.quizzes = list(list_quiz_files())
        self.pframe = root
        self.frame = ttk.Frame(self.pframe, padding=(0, 20))
        self.frame.grid()
        self.font = font
        #Header for quiz list page
        self.header = ttk.Label(self.frame, text="Your available quizzes:", font=(font, 24))
        self.header.grid(row=0, sticky="NW", pady=(10, 20))
        #Frame to keep all the quiz title objects
        self.qListFrame = ScrolledFrame(self.frame, width = (root.winfo_width()* .80), height = (root.winfo_height() * .60))
        #self.qListFrame = ttk.Frame(self.frame, padding=(0, 20))
        self.qListFrame.columnconfigure(0, weight=1)
        self.qListFrame.grid(sticky="EW")
        self.list_quizzes()
        #Initiate empty quiz list (only load the titles)      
        self.menuBtn = ttk.Button(self.pframe, bootstyle=PRIMARY, text="Main Menu", command=self.b_mainMenu)
        self.menuBtn.grid(sticky="S", pady=30)
    
    #Make a new quiz title object for each quiz
    def list_quizzes(self):
        for quiz in self.quizzes:
            qTitle = Q_title(self.qListFrame, quiz, self)

    #Back to main menue    
    def b_mainMenu(self):
        self.frame.destroy()
        self.menuBtn.destroy()
        menu.Main_Menu(self.pframe, self.font)
        


