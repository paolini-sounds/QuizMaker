import tkinter as tk
from qm_modules.functions import *
from qm_modules.objects import *
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.mk_quiz import Question
import gui.main_menu as mm
from ttkbootstrap.scrolled import ScrolledFrame

"""
Take Quiz:
Loads all questions and creates a page for each of them
Displays one question per page
Next button destroys current frame and loads new one
Displays detailed results page

To add:
Back Button
High Scores
"""




#Create the progress bar
class ProgFrame():
    def __init__(self, parent):
        self.pFrame = parent.root
        self.parent = parent
        self.min = 0
        self.max = len(parent.quiz.questions)        
        self.progBar = ttk.Progressbar(bootstyle="striped-info", maximum=self.max, value=self.min, length=200)
        self.progFrame = ttk.Label(self.pFrame, text=f"Question {self.min + 1} of {self.max}")
        self.progFrame.grid()
        self.progBar.grid()
    #Updates progress bar with each new question
    def updateProg(self):
        if self.min < self.max:
            self.progBar.step()
            self.min += 1
            self.progFrame.configure(text=f"Question {self.min + 1} of {self.max}")

    def destroy(self):
        self.progBar.destroy()
        self.progFrame.destroy()


class Choice():
    def __init__(self, choice, pframe, letter, rows, user_answer):
        self.pframe = pframe
        self.frame = ttk.LabelFrame(pframe, width=250, bootstyle=LIGHT)
        #Radio button
        self.rb = tk.Radiobutton(self.frame, variable=user_answer, value=letter)
        self.frame.columnconfigure(2, weight=1)
        self.frame.grid(pady=4)
        self.text = ttk.Label(self.frame, text=choice)
        self.label = ttk.Label(self.frame, width=2, padding=(0), text=f'{letter}.')
        self.rb.grid(row=rows, column=0)
        self.label.grid(row=rows, column=1)
        self.text.grid(row=rows, column=2, padx=(10, 100))
        self.letter = letter

class QPage():
    def __init__(self, parent, index):
        self.pFrame = parent.qFrame
        self.quiz = parent.quiz
        self.qObject = self.quiz.questions[index]
        self.answer = self.qObject.answer
        self.choices = self.qObject.choices
        self.qFrame = ttk.Label(self.pFrame)
        self.qLabel = ttk.Label(self.qFrame, text=f"{self.qObject.question}", font=("helvetica", 16), padding=(0, 20))
        self.userAnswer = tk.StringVar()
        self.choiceUI = []

    #Displays question page when next button is clicked
    def packPage(self):   
        self.rows = 0 
        self.qFrame.columnconfigure(0, weight=1)
        self.qFrame.grid(ipadx=100)
        self.qLabel.grid(row=0, column=0)
        for letter, choice in self.choices.items():
            self.choiceUI.append(Choice(choice, self.qFrame, letter, self.rows, self.userAnswer))
            self.rows +=1

    #Displays the question on results page
    def resPage(self, pFrame):
        lblFrame = ttk.LabelFrame(pFrame, 
                                  text=f'Question {self.qObject.num}',
                                  bootstyle ='success' if self.qObject.isCorrect else 'danger')
        lblFrame.grid(pady=20)
        qLbl = ttk.Label(lblFrame, text=self.qObject.question)
        qLbl.grid(pady=10)
        #Shows correct answer in green vs. user answer in red (if different)
        for l, c in self.choices.items():
            color = "#F8F5F0"
            if l == self.userAnswer and l != self.answer:
                color = "#d9534f"
            elif l == self.answer:
                color = "#93c54b"
            chLbl = ttk.Label(lblFrame, background=color, text=f'{l}. {c}', width=30)
            chLbl.grid(pady=3)

#The main class which controls the Take Quiz portion of the app
class TakeQuiz():
    def __init__(self, quiz, root):
        self.root = root
        self.quiz = quiz
        self.questions = quiz.questions
        self.header = ttk.Label(self.root, text=f"Attempt #{len(self.quiz.scores) + 1} of Quiz: {self.quiz.title}", font=("helvetica", 22))
        self.header.grid(pady=15)
        #Instantiate the progress bar and Label
        self.progFrame = ProgFrame(self)
        self.qFrame = ttk.Frame(self.root)
        self.qFrame.grid()
        self.qPages = {}
        self.makeQPages()
        self.curPage = 1
        self.qPages[self.curPage].packPage()
        self.nextBtn = ttk.Button(self.root, text="Next", command=self.nextPage)
        self.quitBtn = ttk.Button(self.root, text="Quit", command=self.mMenu, bootstyle=DANGER)
        self.userAnswers = []
        self.nextBtn.grid(row=10, pady=20)
        self.quitBtn.grid(row=11, )

    #Go back to main menu
    def mMenu(self):
        self.header.destroy()
        self.progFrame.destroy()
        self.qPages[self.curPage].qFrame.destroy()
        mm.Main_Menu(self.root, "Helvetica")
        self.quitBtn.destroy()
        self.nextBtn.destroy()
        self.qFrame.destroy()
        if self.resFrameParent:
            self.resFrameParent.destroy()

    #Load results page
    def loadResults(self):
        color = "success"
        if self.score < 70:
            color = "danger"
        elif self.score < 85:
            color = "warning"
        self.progFrame.destroy()
        self.qFrame.destroy()
        self.nextBtn.destroy()
        self.quitBtn.grid_forget()
        self.header.configure(text="Results:", padding= (0, 50, 0, 10))
        self.resFrameParent = ttk.Frame(self.root)
        self.resFrameParent.grid()
        self.resFrame = ScrolledFrame(self.resFrameParent, 
                                      width = (self.root.winfo_width()* .80), 
                                      height = (self.root.winfo_height() * .60))
        self.resFrame.columnconfigure(0, weight=1)
        self.resFrame.grid()
        #Create the meter widget
        meter = ttk.Meter(self.resFrame,
                          metertype="full",
                           metersize=180, 
                           padding=5, 
                           amountused=self.score,
                           textright="%",
                           bootstyle=color
                           )
        meter.grid()
        self.subHeader = ttk.Label(self.resFrame, text=f'You answered {self.points} out of {len(self.questions)} questions correctly.')
        self.subHeader.grid(sticky="S")
        for i, q in self.qPages.items():
            q.resPage(self.resFrame)
        self.quitBtn.configure(text="Main Menu", bootstyle="primary")
        self.quitBtn.grid(pady=30)
    
    #Calculates the score after quiz is complete
    def calcScore(self):
        self.points = 0
        for q in self.questions:
            if q.isCorrect:
                self.points += 1
        maxPoints = len(self.questions)
        self.score = round((self.points / maxPoints) * 100, 1)
                
    #Destroys current page, saves answers, and loads new page
    def nextPage(self):
        #Set question to correct if answer matches
        pg = self.qPages[self.curPage]
        usrAns = pg.userAnswer.get()
        if usrAns == '':
            return
        pg.userAnswer = usrAns      
        self.userAnswers.append(usrAns) 
        if usrAns == self.qPages[self.curPage].answer:
                self.questions[self.curPage - 1].isCorrect = True
        #Go to next page if quiz is not done
        if self.curPage < len(self.qPages):
            pg.qFrame.destroy()
            self.curPage += 1
            self.progFrame.updateProg()
            self.qPages[self.curPage].packPage()
        #If quiz is done, calculate score and load results page
        else:
            self.calcScore()
            self.loadResults()

    def makeQPages(self):
        for i, question in enumerate(self.quiz.questions):
            #init a new page for each question
            self.qPages[question.num] = QPage(self, i)
