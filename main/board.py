from .filemanager import File
import random
import os
import json

class DataManager:
    Data = []    
    def setup():
        p = os.path.abspath(os.path.dirname(__file__))
        f = File(p + "\\board.json")
        data = f.readJSON()["Categories"]
        keys = list(data.keys())
        cats = []
        for key in keys:
            cats.append(Category.fromJSON(key, data[key]))
        DataManager.Data = cats
        
        




class Question:
    def __init__(self, question : str, answer : str, points : int, done : bool = False):
        self.question : str = question
        self.answer : str = answer
        self.points : int = points
        self.done : bool = done
    @classmethod
    def split(cl, questions : list):
        q1 = [f for f in questions if f.points == 100]
        q2 = [f for f in questions if f.points == 200]
        q3 = [f for f in questions if f.points == 300]
        q4 = [f for f in questions if f.points == 400]
        q5 = [f for f in questions if f.points == 500]
        return (q1, q2, q3, q4, q5)
    @classmethod
    def fromJSON(cl, data : dict):
        q = data[0]
        a = data[1]
        p = data[2]
        d = False
        if len(data) > 3:
            d = data[3]
        return Question(q, a, p, done=d)
    @classmethod
    def toJSON(cl, question):
        return [question.question, question.answer, question.points, question.done]
    def __str__(self):
        return f"{self.question}:{self.answer}:{self.points}"

class Category:
    def __init__(self, name : str, questions : list[Question]):
        self.questions = questions
        self.name = name
        q = Question.split(questions)
        self.q1 = q[0]
        self.q2 = q[1]
        self.q3 = q[2]
        self.q4 = q[3]
        self.q5 = q[4]
        if len(self.questions) > 5:
            for i in range(1, 6):
                setattr(self, f"q{i}", random.choice(getattr(self, f"q{i}")))
            self.questions = [self.q1, self.q2, self.q3, self.q4, self.q5]
    @classmethod
    def fromJSON(cl, name : str, data : dict):
        quest = []
        for question in data:
            quest.append(Question.fromJSON(question))
        
        return Category(name, quest)
    @classmethod
    def toJSON(cl, category):
        quest = []
        for question in category.questions:
            quest.append(Question.toJSON(question))
        return {"name" : category.name, "questions" : quest}
    def randomCategories(n : int):
        already = []
        cats = []
        for i in range(0, n):
            r = random.randint(0, len(DataManager.Data)-1)
            while r in already:
                r = random.randint(0, len(DataManager.Data)-1)
            already.append(r)
            cats.append(DataManager.Data[r])
        return cats
            
    def __str__(self):
        s = self.name
        s += " | "
        for q in self.questions:
            s += str(q)
        return s
class Board:
    def __init__(self, categories : list[Category]):
        self.categories = categories
    
    def to_JSON(self):
        cats = []
        for cat in self.categories:
            cats.append(Category.toJSON(cat))
        d = {"Categories" : cats}
        return json.dumps(d)
    @classmethod
    def from_JSON(cl, data):
        if isinstance(data, str):
            data = json.loads(data)
        cats = []
        for cat in data["Categories"]:
            cats.append(Category.fromJSON(cat["name"], cat["questions"]))
        return Board(cats)
    def randomBoard():
        cats = Category.randomCategories(5)
        return Board(cats)    
    def __str__(self):
        s = "Board ("
        for cat in self.categories:
            s += str(cat)
        s += ")"
        return s
DataManager.setup()