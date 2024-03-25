import tkinter as tk
import gui.mk_quiz as mk_quiz
from gui.show_quizzes import QuizMenu
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

"""
Main Menu

Creates and displays the main menu of the app.

"""


class Main_Menu():
    def __init__(self, root, font):
        self.root = root
        self.font = font
        self.frame = ttk.Frame(self.root, padding=(0, 20))
        self.frame.grid(row=1)
        self.header = ttk.Label(self.frame, text="Main Menu", font=(font, 24), bootstyle='primary')
        self.header.grid(row=0, sticky='N')
        #Make Buttons and place on grid
        self.btnFrame = ttk.Frame(self.frame)
        self.btnFrame.grid(pady=100)
        self.mkQuizBtn = ttk.Button(self.btnFrame, text = "Create Quiz", command=self.showMkQuiz)
        self.showQuizzesBtn = ttk.Button(self.btnFrame, text = "My Quizzes", command=self.showQuizzes)
        self.mkQuizBtn.grid(row=1, column=0, padx=5)
        self.showQuizzesBtn.grid(row=1, column=1, padx=5)
        self.quitButton = ttk.Button(self.frame, text="Quit", bootstyle=DANGER, command=self.root.destroy)
        self.quitButton.grid(sticky="S")

    def showMkQuiz(self):
        self.frame.destroy()
        mk_quiz.Make_Quiz(self.root, self.font)
    
    def showQuizzes(self):
        self.frame.grid_forget()
        quizList = QuizMenu(self.root, self.font, self)