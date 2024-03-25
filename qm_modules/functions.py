import os
from qm_modules.objects import Quiz, Question, quizzes

"""
Functions:

Creates auxiliary functions for the app including
saving and loading quizzes, and file management.

"""



def delete_file(quiz):
    if os.path.exists(f'quizzes/{quiz}.txt'):
        os.remove(f'quizzes/{quiz}.txt')

def save_to_file(quiz):
    if not os.path.isdir('quizzes'):
        os.mkdir('quizzes')
    with open(f'quizzes/{quiz.title}.txt', 'w') as file:
        for i, q in enumerate(quiz.questions):
            file.write(f'{i} {q.question}\n')
            for l, c in q.choices.items():
                if l == q.answer:
                    file.write(f'{l} {c}*\n')
                else:
                    file.write(f'{l} {c}\n')
    print(f'Text file saved in "/quizzes" as "{quiz.title}.txt"')

def load_from_file(quiz_title):
    questions = []
    if os.path.exists(f'quizzes/{quiz_title}.txt'):
        with open (f'quizzes/{quiz_title}.txt', 'r') as file:
            lines = file.read().strip().split('\n')
            for line in lines:
                curr = len(questions) - 1
                if line[0].isnumeric():
                    question = line[2:]
                    questions.append({'question': question, 'choices': {}, 'answer': None, "qnum": int(line[0]) + 1})
                elif line[0].isalpha():
                    if line.endswith('*'):
                        questions[curr]['choices'][line[0]] = line[2:-1]
                        questions[curr]['answer'] = line[0]
                    else:
                        questions[curr]['choices'][line[0]] = line[2:]
    else:
        print("File not found.")
        print()
        return
    new_quiz = Quiz(quiz_title)
    for q in questions:
        new_question = Question(q["qnum"], q['question'], q['answer'], q['choices'])
        new_quiz.questions.append(new_question)
    print(f'Successfully loaded {new_quiz.title} from text file.')
    print()
    return(new_quiz)

def load_sample(quiz_title):
    questions = []
    if os.path.exists(f'quizzesSAMPLE/{quiz_title}.txt'):
        with open (f'quizzesSAMPLE/{quiz_title}.txt', 'r') as file:
            lines = file.read().strip().split('\n')
            for line in lines:
                curr = len(questions) - 1
                if line[0].isnumeric():
                    question = line[2:]
                    qnum = int(line[0]) + 1
                    questions.append({'qnum': qnum, 'question': question, 'answer': None, 'choices': {}, })
                elif line[0].isalpha():
                    if line.endswith('*'):
                        questions[curr]['choices'][line[0]] = line[2:-1]
                        questions[curr]['answer'] = line[0]
                    else:
                        questions[curr]['choices'][line[0]] = line[2:]
    else:
        print("File not found.")
        print()
        return
    new_quiz = Quiz(quiz_title)
    for q in questions:
        new_question = Question(q['qnum'], q['question'], q['choices'], q['answer'])
        new_quiz.questions.append(new_question)
    quizzes.append(new_quiz)
    print(f'Successfully loaded {new_quiz.title} from text file.')
    print()
    return(new_quiz)

def load_quiz(quiz_title):
    questions = []
    if os.path.exists(f'quizzes{quiz_title}.txt'):
        with open (f'quizzes/{quiz_title}.txt', 'r') as file:
            lines = file.read().strip().split('\n')
            for line in lines:
                curr = len(questions) - 1
                if line[0].isnumeric():
                    question = line[2:]
                    qnum = int(line[0]) + 1
                    questions.append({'qnum': qnum, 'question': question, 'answer': None, 'choices': {}, })
                elif line[0].isalpha():
                    if line.endswith('*'):
                        questions[curr]['choices'][line[0]] = line[2:-1]
                        questions[curr]['answer'] = line[0]
                    else:
                        questions[curr]['choices'][line[0]] = line[2:]
    else:
        print("File not found.")
        print()
        return
    new_quiz = Quiz(quiz_title)
    for q in questions:
        new_question = Question(q['qnum'], q['question'], q['choices'], q['answer'])
        new_quiz.questions.append(new_question)
    quizzes.append(new_quiz)
    print(f'Successfully loaded {new_quiz.title} from text file.')
    print()
    return(new_quiz)

def list_quiz_files():
    titles = []
    if os.path.isdir("quizzes"):
        for qfile in os.listdir("quizzes"):
            title = qfile[:-4]
            titles.append(title)
    return set(titles)


def list_sample_files():
    titles = []
    if os.path.isdir("quizzesSAMPLE"):
        for qfile in os.listdir("quizzesSAMPLE"):
            title = qfile[:-4]
            titles.append(title)
    return set(titles)


def init_test_quiz(name):
    quiz = Quiz(name)
    new_question = Question("Question1",
                             {'a': "choice1", 
                              'b': 'choice2',
                              'c': 'choice3',
                              'd': 'choice4'},
                              'a')
    quiz.questions.append(new_question)
    new_question2 = Question("Question2",
                             {'a': "choice1", 
                              'b': 'choice2',
                              'c': 'choice3',
                              'd': 'choice4'},
                              'a')
    quiz.questions.append(new_question2)
    new_question3 = Question("Question3",
                             {'a': "choice1", 
                              'b': 'choice2',
                              'c': 'choice3',
                              'd': 'choice4'},
                              'a')
    quiz.questions.append(new_question3)
    return quiz

if __name__ == "__main__":
    quiz1 = init_test_quiz("Quiz1")
    save_to_file(quiz1)
    quiz1 = load_from_file("Quiz1")
    quizzes["Quiz1"] = quiz1
    quiz2 = init_test_quiz("Quiz2")
    save_to_file(quiz2)
    quiz2 = load_from_file("Quiz2")
    quizzes["Quiz2"] = quiz2
    list_quiz_files()