quizzes = []

class Question():
    def __init__(self, qNum, question, answer, choices):
        self.question = question
        self.num = qNum
        self.choices = choices
        self.answer = answer
        self.isCorrect = False

class Quiz():
    def __init__(self, title):
        self.title = title
        self.questions = []
        self.scores = []
        self.high_score = 0


            