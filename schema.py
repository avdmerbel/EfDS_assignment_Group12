# python file with SQLAlchemy description of the database tables (.py)

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Float, Table, Boolean, DateTime 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Student(Base):
  """
  Class to represent student

  ...

  Attributes
  ----------
  UniversityID : int
    University ID of student
  Name : str
    Student's full name
  Email: str
    Student's email address

  Methods
  -------
  __repr__:
    Creates clear layout for SQL query 
  """
  __tablename__ = "Students"
  
  UniversityID = Column(Integer, primary_key = True)
  Name = Column(String(160))
  Email = Column(String(200))
  
  def __repr__(self):
    return "Student(UniversityID='%s', Name='%s', Email='%s')" % (self.UniversityID, self.Name, self.Email)


TaskQuestionLink = Table('TaskQuestionLink', Base.metadata,
    Column('QuestionID', ForeignKey('Questions.QuestionID'), primary_key=True),
    Column('TaskID', ForeignKey('Tasks.TaskID'), primary_key=True)
)
""" Association table for Task and Question """

class Question(Base):
  """
  Class to represent Question

  ...

  Attributes
  ----------
  QuestionID : int
    Question ID of question
  Title : str
    Question title
  Text: str
    Question text
  
  Relationships
  --------------
  Answers -> QuestionID as foreign key
  Tasks -> related through association table TaskQuestionLink

  Methods
  -------
  __repr__:
    Creates clear layout for SQL query 
  """
  __tablename__ = "Questions"
  
  QuestionID = Column(Integer, primary_key = True)
  Title = Column(String(160))
  Text = Column(String(300))
  Answers = relationship("Answer", backref = "Question")
  Tasks = relationship("Task", secondary = TaskQuestionLink, back_populates = "Questions")

  def __repr__(self):
    return "Question(QuestionID='%s', Title='%s', Text='%s')" % (self.QuestionID, self.Title, self.Text)

class Task(Base):
  """
  Class to represent tasks

  ...

  Attributes
  ----------
  TaskID : int
    Tasks ID
  Title : str
    Task title
  Text: str
    Overview text

  Relationships
  -------------
  Assignments -> TaskID as foreign key
  Questions -> related through association table TaskQuestionLink

  Methods
  -------
  __repr__:
    Creates clear layout for SQL query 
  """
  __tablename__ = "Tasks"

  TaskID = Column(Integer, primary_key = True)
  Title = Column(String(200))
  Text = Column(String(400))
  Assignments = relationship( "Assignment", backref ='task')
  Questions = relationship("Question", secondary=TaskQuestionLink, back_populates = "Tasks") 

  def __repr__(self):
    return "Task(TaskID='%s', Title='%s', Text='%s')" % (self.TaskID, self.Title, self.Text) 

class Assignment(Base):
  """
  Class to represent Assignment

  ...

  Attributes
  ----------
  AssignmentID : int
    Assignment ID

  Relationships
  -------------
  Submissions -> primary key AssignmentID as foreign key to submissions
  Students -> UniversityID as foreign key
  TaskID -> TaskID as foreign key
  """
  __tablename__ = "Assignments"
  
  AssignmentID = Column(Integer, primary_key = True)
  UniversityID = Column(ForeignKey('Students.UniversityID'), nullable=False)
  TaskID = Column(ForeignKey('Tasks.TaskID'), nullable=False)
  Submissions = relationship("Submission", backref="Assignments")
  Students = relationship("Student", backref = "Assignemtns")

class Submission(Base):
  """
  Class to represent Submission

  ...

  Attributes
  ----------
  SubmisisonID : int
    Submission ID
  EvaluationRequest : boolean
    Whether an Evaluation was requested from teacher
  SubmissionTime : datetime
    Time of submission

  Relationships
  -------------
  AssignmentID -> AssignmentID as foreign key 
  Answers -> primary key SubmissionID as foreign key to Answers
  Evaluation -> primary key SubmissionID as foreign key to Evaluation
  """
  __tablename__ = "Submissions"
  
  SubmissionID = Column(Integer, primary_key = True)
  AssignmentID = Column(ForeignKey('Assignments.AssignmentID'), nullable=False)
  Answers = relationship("Answer", backref = "Submissions")
  EvaluationRequest = Column(Boolean)
  Evaluation = relationship("Evaluation", backref = "Assignment")
  SubmissionTime = Column(DateTime)
  
class Evaluation(Base):
  """
  Class to represent Evaluation

  ...

  Attributes
  ----------
  EvaluationID : int
    Evaluation ID
  EvaluationFinished : boolean
    Whether an Evaluation was finished by teacher

  Relationships
  -------------
  SubmissionID -> SubmissionID as foreign key 
  Scores -> primary key EvaluationID as foreign key to Scores
  """
  __tablename__ = "Evaluations"
  
  EvaluationID = Column(Integer, primary_key = True)
  SubmissionID = Column(ForeignKey('Submissions.SubmissionID'), nullable=False)
  Scores = relationship("Score", backref = "Evaluation")
  EvaluationFinished = Column(Boolean)
  
  def __repr__(self):
    return "Evaluation(EvaluationID='%s')" % (self.EvaluationID)


class Answer(Base):
  """
  Class to represent Answer

  ...

  Attributes
  ----------
  AnswerID : int
    Answer ID
  Text : str
    Text entered as answer

  Relationships
  -------------
  QuestionID -> QuestionID as foreign key 
  SubmissionID -> SubmissionID as foreign key
  """
  __tablename__ = "Answers"

  AnswerID = Column(Integer, primary_key=True)
  Text = Column(String(400))
  QuestionID = Column(ForeignKey("Questions.QuestionID"), nullable=False)
  SubmissionID = Column(Integer, ForeignKey("Submissions.SubmissionID"), nullable=False)

class Score(Base):
  """
  Class to represent Score

  ...

  Attributes
  ----------
  ScoreID : int
    Score ID
  Value : float
    Value given as score to answer 
    
  Relationships
  -------------
  EvaluationID -> EvaluationID as foreign key 
  AnswerID -> AnserID as foreign key
  """
  __tablename__ = "Scores"

  ScoreID = Column(Integer, primary_key=True)
  Value = Column(Float)
  EvaluationID = Column(ForeignKey("Evaluations.EvaluationID"), nullable = False)
  AnswerID = Column(ForeignKey("Answers.AnswerID"), nullable = False)
