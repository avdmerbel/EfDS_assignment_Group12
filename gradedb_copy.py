# python file with definitions of the main project class GradeDB with access methods to the database. (.py)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Float, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # normally present once in a script!

## classes referring to tables needed:
# Student, Question, Task, Assignment, Submission, 
# Answer, EvaluationRequest, Evaluation, Score

class Student(Base):
  __tablename__ = "Students"
  
  UniversityID = Column(Integer, primary_key = True)
  Name = Column(String(160))
  Email = Column(String(200))
  #UniversityID = Column(Integer)
  
  def __repr__(self):
    return "Student(UniversityID='%s', Name='%s', Email='%s')" % (self.UniversityID, self.Name, self.Email)


TaskQuestionLink = Table('TaskQuestionLink', Base.metadata,
    Column('QuestionID', ForeignKey('Questions.QuestionID'), primary_key=True),
    Column('TaskID', ForeignKey('Tasks.TaskID'), primary_key=True)
)

class Question(Base):
  __tablename__ = "Questions"
  
  QuestionID = Column(Integer, primary_key = True)
  Title = Column(String(160))
  Text = Column(String(300))
  Answers = relationship("Answer", backref = "Question")
  Tasks = relationship("Task", secondary = TaskQuestionLink, back_populates = "Questions")

  def __repr__(self):
    return "Question(QuestionID='%s', Title='%s', Text='%s')" % (self.QuestionID, self.Title, self.Text)

class Task(Base):
  __tablename__ = "Tasks"

  TaskID = Column(Integer, primary_key = True)
  Title = Column(String(200))
  Text = Column(String(400))
  Assignments = relationship( "Assignment", backref ='task')
  Questions = relationship("Question", secondary=TaskQuestionLink, back_populates = "Tasks")  


# class TaskQuestionLink(Base):
#   __tablename__ = "taskquestionLink"

#   QuestionID = Column(Integer, ForeignKey("QuestionID"), primary_key=True)
#   TaskID = Column(Integer, ForeignKey("TaskID"), primary_key=True)

class Assignment(Base):
  __tablename__ = "Assignments"
  
  AssignmentID = Column(Integer, primary_key = True)
  UniversityID = Column(ForeignKey('Students.UniversityID'), nullable=False)
  TaskID = Column(ForeignKey('Tasks.TaskID'), nullable=False)
  Submissions = relationship("Submission", backref="Assignments")
  Students = relationship("Student", backref = "Assignemtns")

class Submission(Base):
  __tablename__ = "Submissions"
  
  SubmissionID = Column(Integer, primary_key = True)
  AssignmentID = Column(ForeignKey('Assignments.AssignmentID'), nullable=False)
  Answers = relationship("Answer", backref = "Submissions")
  
class Evaluation(Base):
  __tablename__ = "Evaluations"
  
  EvaluationID = Column(Integer, primary_key = True)
  AssignmentID = Column(ForeignKey('Assignments.AssignmentID'), nullable=False)
  Assignment = relationship("Assignment", backref = "Evaluation")
  Scores = relationship("Score", backref = "Evaluation")
  
  def __repr__(self):
    return "Evaluation(EvaluationID='%s')" % (self.EvaluationID)



class Answer(Base):
  __tablename__ = "Answers"

  AnswerID = Column(Integer, primary_key=True)
  Text = Column(String(400))
  QuestionID = Column(ForeignKey("Questions.QuestionID"), nullable=False)
  SubmissionID = Column(Integer, ForeignKey("Submissions.SubmissionID"), nullable=False)

class Score(Base):
  __tablename__ = "Scores"

  ScoreID = Column(Integer, primary_key=True)
  Value = Column(Float)
  EvaluationID = Column(ForeignKey("Evaluations.EvaluationID"), nullable = False)
  AnswerID = Column(ForeignKey("Answers.AnswerID"), nullable = False)

class GradeDB:
  def __init__(self, fileName):
    addr = "sqlite:///" + fileName
    self._engine = create_engine(addr,echo=False)
    self._sessionMaker = sessionmaker(bind=self._engine)
    
  def newSession(self):
    return self._sessionMaker()

  def addStudent(self, name, email, unid):
    if (not name or not (type(name) == str)):
      print('This is not a valid name.')
      return
    elif ( not email or not (type(email) == str)):
      print('This is not a valid email address.')
      return
    with self.newSession() as ses:
      stud = Student(Name = name, Email = email, UniversityID = unid)
      ses.add( stud )
      ses.commit()
      return 
  
  # def addQuestion(self, title, text):
  #   if (not title or not (type(title) == str)):
  #     print('This is not a valid title.')
  #     return
  #   #elif ( not text or not (type(text) == str)):
  #     #print('This is not a valid question.')
  #     #return
  #   with self.newSession() as ses:
  #     nq = Question(Title = title, Text = text)
  #     ses.add( nq )
  #     ses.commit()
  #     return

  # def addTask(self, title, text, questions):
  #   with self.newSession() as ses:
  #     nt = Task(Title = title, Text = text, Questions = questions)
  #     ses.add(nt)
  #     ses.commit()
  #     return 
    
  # def addAssignment(self, student, task):
  #   with self.newSession() as ses:
  #     assign = Assignment( )
  #     ses.add( assign )
  #     ses.commit()
  #     return
    
  # def newSubmission(self, assignment):
  #   with self.newSession() as ses:
  #     sub = Submission( Assignment = assignment )
  #     ses.add( sub )
  #     ses.commit()
  #     return

  # def addAnswer(self, answer):
  #   with self.newSession() as ses:
  #     ans = Answer(Answer = answer)
  #     ses.add(ans)
  #     ses.commit()
  #     return

  # def commitSubmission(self):
  #   with self.newSession() as ses:
  #     er = EvaluationRequest()
  #     ses.add(er)
  #     ses.commit()
  #     return

  # def newEvaluation(self, request ):
  #   with self.newSession() as ses:
  #     eva= Evaluation( EvaluationRequest = request )
  #     ses.add( eva )
  #     ses.commit()
  #     return

  # def addScore(self, score):
  #   with self.newSession() as ses:
  #     sc = Score(Score = score)
  #     ses.add(sc)
  #     ses.commit()
  #     return
