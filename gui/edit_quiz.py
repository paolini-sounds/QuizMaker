import tkinter as tk
# from tkinter import ttk
from qm_modules.objects import *
from qm_modules.functions import save_to_file, load_from_file, delete_file
from tkinter import INSERT
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame


"""
Edit Quiz:
Creates the page for editing quiz. Each string is pre-loaded into
an entry widget.
Currently able to edit quiz title, question, choices, and correct answer.

Features to Add:
Delete/Add Questions
Delete/Add Choices

"""



class EditChoice():
    def __init__(self, parent, letter, text, pframe, c_answer):
        #Create choices, radio buttons, and entries
        self.question = parent
        self.letter = letter
        self.frame = ttk.Frame(pframe)         
        self.label = ttk.Label(self.frame, text=f'{self.letter}. ')
        self.frame.grid()
        self.newText = ttk.StringVar
        self.rb = ttk.Radiobutton(self.frame, variable=c_answer, value=self.letter)
        self.rb.grid(row=0, column=0)
        self.label.grid(row=0, column=1)
        self.e = ttk.Entry(self.frame, textvariable=self.newText)
        self.e.insert(0, text)
        self.e.grid(row=0, column=2)

class EditQuestion(Question):
    def __init__(self, question, root):
        super().__init__(question.num, question.question, question.answer, question.choices)
        self.pframe = root 
        self.question = question.question #The only way I found to fix the broken entry problem
        self.qFrame = ttk.Frame(self.pframe)
        self.qHFrame = ttk.Frame(self.qFrame)
        #Variable to get answer from radio button
        self.newQ = ttk.StringVar()
        self.qFrame.grid(pady=10)
        self.qHFrame.columnconfigure(1, weight=1)
        self.qHFrame.grid()
        self.qFrame.columnconfigure(0, weight=1)
        self.qLabel = ttk.Label(self.qHFrame, text=f"Question {self.num}")
        self.qVar = ttk.StringVar()
        self.qEntry = ttk.Entry(self.qHFrame, textvariable=self.qVar)
        #Insert text from question
        self.qEntry.insert(0, self.question)
        self.qLabel.grid(row=0, column=0)
        self.qEntry.grid(row=0, column=1, pady=10)
        self.newAnswer = ttk.StringVar()
        self.newAnswer.set(question.answer)
        for l, c in self.choices.items():
            choice = EditChoice(self, l, c, self.qFrame, self.newAnswer)
        
        



class Edit_Quiz():
    def __init__(self, quiz, root, main_menu):
        self.main_menu = main_menu
        self.quiz = load_from_file(quiz)
        self.pframe = root
        self.frame = ttk.Frame(self.pframe)
        self.header = ttk.Label(self.frame, text=f'Edit Quiz', font=("helvetica", 20))
        self.scrFrame = ScrolledFrame(self.frame, 
                                      width = (self.pframe.winfo_width()* .80), 
                                      height = (self.pframe.winfo_height() * .60))
        self.frame.grid()
        self.frame.columnconfigure(1, weight=1)
        self.scrFrame.columnconfigure(0, weight=1)
        self.header.grid(row=0, column=0, pady=20)
        self.scrFrame.grid(row=1, column=0)
        self.scrFrame.columnconfigure(0, weight=1)
        self.tVar = ttk.StringVar()              
        self.tLabelFrame = ttk.LabelFrame(self.scrFrame, text="Title", bootstyle="primary")
        self.tEntry = ttk.Entry(self.tLabelFrame, textvariable=self.tVar)
        self.tLabelFrame.grid()
        self.tEntry.insert(0, self.quiz.title)
        self.tEntry.grid(padx=20, pady=3)
        self.questions = []
        for q in self.quiz.questions:
            newQuestion = EditQuestion(q, self.scrFrame)
            self.questions.append(newQuestion)
        self.saveButton = ttk.Button(self.scrFrame, text="Save Quiz", command = self.saveQuiz, bootstyle = "success")
        self.saveButton.grid(pady = 10)    

    def saveQuiz(self):
        newTitle = self.tVar.get()
        newQuestions = []
        for q in self.questions:
            newQ = q.qVar.get()
            choices = {}
            #If a new answer isn't chosen then use the old answer
            answer = q.newAnswer.get()
            for l, c in q.choices.items():
                choices[l] = c
            newQuestions.append(Question(q.num, newQ, answer, choices))
        newQuiz = Quiz(newTitle)
        newQuiz.questions = newQuestions
        delete_file(self.quiz.title)
        save_to_file(newQuiz)
        self.frame.destroy()
        mm = self.main_menu(self.pframe, "Helvetica")
        



