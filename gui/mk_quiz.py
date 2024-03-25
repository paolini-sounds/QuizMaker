import tkinter as tk
# from tkinter import ttk
from qm_modules.objects import *
from qm_modules.functions import save_to_file
from gui.main_menu import Main_Menu
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

padding = (0, 30)



class Title_Page():
    def __init__(self, parent, pFrame, font):
        self.parent = parent
        pFrame = self.parent.frame
        self.font = font
        self.frame = ttk.Frame(pFrame, padding=padding)
        self.header = ttk.Label(self.frame, text="New Quiz", font=(font, 24), padding=(0, 20, 0, 30))
        self.instructions = ttk.Label(self.frame, text="Enter a title for your quiz")
        self.t_value = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.t_value)
        self.btn = ttk.Button(self.frame, text="Enter", default="active", command=parent.enterTitle)
        self.frame.grid(row=0)
        self.frame.rowconfigure(0, weight=1)
        self.header.grid(row=0, sticky="N")
        self.instructions.grid(sticky='N')
        self.entry.grid(row=2)
        self.btn.grid(row=3, pady=20)

class Question():
    def __init__(self, qNum, question, answer, choices):
        self.question = question
        self.num = qNum
        self.choices = choices
        self.answer = answer
        self.isCorrect = False
        

class Mk_Q_Page():
    def __init__(self, parent, pFrame, font, qnum):
        self.qNum = qnum
        #Parent Frame
        self.pFrame = pFrame
        self.font = font
        self.parent = parent
        #This frame belongs to the Make_Quiz Frame
        self.parent.curPage = self
        self.frame = ttk.Frame(self.pFrame)
        self.intructions = ttk.Label(self.frame, text=f'Enter question {self.qNum}:', padding=(padding))
        self.q_Value = tk.StringVar()
        self.entry = ttk.Entry(self.frame, width=35, textvariable=self.q_Value)
        self.entry.focus()
        self.intructions.grid(row=0)
        self.entry.grid(row=1)
        #Make the add choices button
        self.ansFrame = ttk.Frame(self.frame, padding=(0, 10))
        self.ansFrame.columnconfigure(0, weight=1)
        self.ansFrame.grid(row=2)
        self.choicesLabel = ttk.Label(self.ansFrame, text='Add answer choices and select correct answer.')
        self.choicesLabel.grid(sticky="ENSW", row=0, column=0)
        self.cBtnFrame = ttk.Frame(self.ansFrame)
        self.cBtnFrame.columnconfigure(1, weight=1)
        self.cBtnFrame.grid(row=1, pady=10)
        self.addButton = ttk.Button(self.cBtnFrame, width=2, text='+', command=self.addChoice, bootstyle=(PRIMARY, OUTLINE))
        self.minusButton = ttk.Button(self.cBtnFrame, width=2, text = '-', command=self.minusChoice, bootstyle=(PRIMARY, OUTLINE))
        self.minusButton.grid(sticky='E', row=0, padx=3, column=0)
        self.addButton.grid(sticky="E", row=0, column=1)
        self.letters = 'a'
        self.nChoiceRows = 0
        self.choices = []
        self.c_answer = tk.StringVar()

    def addChoice(self):
        newChoice = Choice(self.ansFrame, self.letters, self.nChoiceRows, self.c_answer)        
        #Increase row count and choice letters
        self.letters = chr(ord(self.letters) + 1)
        self.nChoiceRows += 1
        if self.parent.navPane == None:
            self.parent.initNavPane()
        self.choices.append(newChoice)
    
    def minusChoice(self):
        if len(self.choices) == 0:
            return
        lastChoice = self.choices.pop()
        lastChoice.frame.destroy()
        self.letters = chr(ord(self.letters) - 1)
        self.nChoiceRows -= 1

class Choice():
    def __init__(self, pframe, letter, rows, c_answer):
        self.pframe = pframe
        self.frame = ttk.Label(pframe)
        self.rb = tk.Radiobutton(self.frame, variable=c_answer, value=letter)
        self.frame.columnconfigure(1, weight=1)
        self.frame.grid(pady=2)
        self.eValue = tk.StringVar()
        self.e = ttk.Entry(self.frame, textvariable=self.eValue)
        self.e.focus()
        self.label = ttk.Label(self.frame, width=2, padding=(0), text=f'{letter}.')
        self.rb.grid(row=rows, column=0)
        self.label.grid(row=rows, column=1)
        self.e.grid(row=rows, column=2)
        self.letter = letter

class Make_Quiz():
    def __init__(self, root, font):
        self.questions = []
        self.root = root
        self.font = font
        self.frame = ttk.Frame(root, padding=padding)
        self.frame.grid(row=1, sticky="N")
        #Create Title Entry Page
        self.titlePage = Title_Page(self, self.frame, font)
        self.pg_index = 0
        self.titlePage.frame.grid(row=2)
        self.navPane = None
        self.msg = None
        #Create Prev and Next Navigation buttons
    
    def initNavPane(self):
        self.navPane = ttk.Frame(self.root, padding=padding)
        self.doneBtn = ttk.Button(self.navPane, text="Finish and Save", command=self.saveQuiz, bootstyle=SUCCESS)
        self.nextBtn = ttk.Button(self.navPane, text="Add Next Question", command=self.nextPage)
        self.navPane.grid(row=2)
        self.nextBtn.grid(row=1)
        self.doneBtn.grid(row=2, pady=30)
    
    def enterTitle(self):
        self.title = self.titlePage.t_value.get()
        if self.title == '':
            self.msg = validate(self.msg, self.titlePage.frame, "Please enter a title.")
            self.msg.grid()
            return
        self.titlePage.frame.grid_forget()
        # self.titleLabel = ttk.Label(self.frame, text=f'Creating Quiz "{self.title}"', font=(self.font, 18))
        # self.titleLabel.grid(row=0)
        self.initQPage(self, self.root, self.font)
        

    def initQPage(self, parent, root, font):
        newQuestionPage = Mk_Q_Page(parent, root, font, len(self.questions) + 1)
        newQuestionPage.frame.grid(row=1)
        #Set current page to newest page
        self.curPage = newQuestionPage

    def saveQuestion(self):
        question = self.curPage.q_Value.get()
        #Save the data on current screen as new question
        qnum = self.curPage.qNum
        choices = self.curPage.choices
        _choices = {}
        c_answer = self.curPage.c_answer.get()
        for c in choices:
            _choices[c.letter] = c.e.get()
        newQuestion = Question(qnum, question, c_answer, _choices)
        self.questions.append(newQuestion)
        print(self.questions)

    def nextPage(self):
        #Question text from entry
        question = self.curPage.q_Value.get()
        #Don't allow blank question
        if question == '':
            self.msg = validate(self.msg, self.navPane, "Question cannot be blank.")
            self.msg.grid(row=0, pady=3)
            return
        #Require answer choice
        if self.curPage.c_answer.get() == '':
            self.msg = validate(self.msg, self.navPane, "Choose an answer first.")
            self.msg.grid(row=0, pady=3)
            return
        #Don't allow blank answers
        for c in self.curPage.choices:
            if c.e.get() == "":
                self.msg = validate(self.msg, self.navPane, "Answers cannot be blank.")
                self.msg.grid(row=0, pady=3)
                return
        #Save Question
        if self.curPage.c_answer.get() is not None:
            self.saveQuestion()
            self.curPage.frame.grid_forget()
            if self.msg:
                self.msg.destroy()
            newQPage = self.initQPage(self, self.frame, self.font)
            



    def saveQuiz(self):
        print(self.curPage.qNum)
        #Get question text from entry
        question = self.curPage.q_Value.get()
        #If question is not blank, validate choices
        if question != "":
            choices = self.curPage.choices
            for c in choices:
                #If question isn't blank, answers can't be blank
                if c.e.get() == '':
                    self.msg = validate(self.msg, self.navPane, "Answers cannot be blank if there is a question.")
                    self.msg.grid(row=0, pady=3)
                    return
            #Must choose an answer
            if self.curPage.c_answer.get() is None:
                self.msg = validate(self.msg, self.navPane, "Choose an answer first.")
                self.msg.grid(row=0, pady=3)
                return
            self.saveQuestion()
        #If question is blank and it is the first question, don't allow finish
        elif question == '' and self.curPage.qNum == 1:
            self.msg = validate(self.msg, self.navPane, "Question cannot be blank.")
            self.msg.grid(row=0, pady=3)
            return
        quizzes.append(self)
        save_to_file(self)
        self.frame.destroy()
        self.navPane.destroy()
        self.curPage.frame.destroy()
        Main_Menu(self.root, self.font)

def validate(msg, root, text):
    if msg:
        msg.destroy()
    return ttk.Label(root, text=text, foreground="red")




        


        
