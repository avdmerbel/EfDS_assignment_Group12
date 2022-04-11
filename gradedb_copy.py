# python file with definitions of the main project class GradeDB with access methods to the database. (.py)
from audioop import avg
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Float, Table, Boolean, update, DateTime 
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

  def __repr__(self):
    return "Task(TaskID='%s', Title='%s', Text='%s')" % (self.TaskID, self.Title, self.Text) 


#class TaskQuestionLink(Base):
 #  __tablename__ = "TaskQuestionLinks"
#
#  QuestionID = Column(Integer, ForeignKey("QuestionID"), primary_key=True, nullable = False)
#  TaskID = Column(Integer, ForeignKey("TaskID"), primary_key=True, nullable = False)

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
  EvaluationRequest = Column(Boolean)
  Evaluation = relationship("Evaluation", backref = "Assignment")
  SubmissionTime = Column(DateTime)
  
class Evaluation(Base):
  __tablename__ = "Evaluations"
  
  EvaluationID = Column(Integer, primary_key = True)
  SubmissionID = Column(ForeignKey('Submissions.SubmissionID'), nullable=False)
  Scores = relationship("Score", backref = "Evaluation")
  EvaluationFinished = Column(Boolean)
  
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
  
  def addQuestion(self, title, text):
    if (not title or not (type(title) == str)):
      print('This is not a valid title.')
      return
    elif ( not text or not (type(text) == str)):
      print('This is not a valid question.')
      return
    with self.newSession() as ses:
      nq = Question(Title = title, Text = text)
      ses.add( nq )
      ses.commit()
      return

#  def addLink( self, Tid, Qid ):
#    with self.newSession() as sess:
#      link = TaskQuestionLink( TaskID = Tid, QuestionID = Qid )
#      sess.add( link )
#      sess.commit()
#      return

  def addTask(self, title, text, questions):
    with self.newSession() as ses:
      qs = ses.query(Question).filter(Question.Title.in_(questions)).all()
      nt = Task(Title = title, Text = text)
      for i in range(len(qs)):
        nt.Questions.append(qs[i])
      ses.add(nt)
      ses.commit()
      return 
    
  def addAssignment(self, student, task):
    with self.newSession() as ses:
      ts = ses.query(Task).filter(Task.Title == task).one()
      assign = Assignment(UniversityID = student, TaskID = ts.TaskID)
      assign.Task = ts
      ses.add( assign )
      ses.commit()
      return
    
  def newSubmission(self, student):
    with self.newSession() as ses:
      sm = ses.query(Assignment).filter(Assignment.UniversityID == student).one()
      sub = Submission( AssignmentID = sm.AssignmentID, EvaluationRequest = False, SubmissionTime = datetime.now())
      sub.Student = student
      ses.add( sub )
      ses.commit()
      return

  def addAnswer(self, student, answer, question):
    with self.newSession() as ses:
      asm = ses.query(Assignment).filter(Assignment.UniversityID == student).one()
      sbm = ses.query(Submission).filter(Submission.AssignmentID == asm.AssignmentID).one()
      ans = Answer(Text = answer, SubmissionID = sbm.SubmissionID, QuestionID = question)
      ses.add(ans)
      ses.commit()
      return

  def commitSubmission(self, SubmissionID):
    with self.newSession() as ses:
      ses.query(Submission).filter(Submission.SubmissionID == SubmissionID).update({'EvaluationRequest': 1})
      print( "An email will now be sent to the teacher who has to grade submission" + str(SubmissionID))
      ses.commit()
      return

  def newEvaluation(self, submission ):
    with self.newSession() as ses:
      sub = ses.query(Submission).filter(Submission.SubmissionID == submission).one()
      if( sub.EvaluationRequest == 0):
        print("This submission does not have a request for evaluation.")
        return
      eva= Evaluation( SubmissionID = submission, EvaluationFinished = False )
      ses.add( eva )
      ses.commit()
      return

  def addScore(self, value, answer, evaluation):
    with self.newSession() as ses:
      sc = Score(Value = value, AnswerID = answer, EvaluationID = evaluation)
      ses.add(sc)
      ses.commit()
      return

  def commitEvaluation( self, evaluation ):
    with self.newSession() as ses:
      eval = ses.query(Evaluation).filter(Evaluation.EvaluationID == evaluation).one()
      if (eval.EvaluationFinished == 1):
        print("This evaluation is already finished and sent to the student.")
        return
      else:
        ses.query(Evaluation).filter(Evaluation.EvaluationID == evaluation).update({'EvaluationFinished': 1})
        ses.query(Submission).filter(Submission.SubmissionID == eval.SubmissionID).update({'EvaluationRequest': 0})
        sub = ses.query(Submission).filter(Submission.SubmissionID == eval.SubmissionID).one()
        ass = ses.query(Assignment).filter(Assignment.AssignmentID == sub.AssignmentID).one()
        stud = ses.query(Student).filter(Student.UniversityID == ass.UniversityID).one()
        scr = ses.query(Score.Value).filter(Score.EvaluationID == evaluation).all()
        avg_scr = round((sum([sum(i) for i in scr])/len([sum(i) for i in scr])),1)
        print("Sent an email to address: " + str(stud.Email) + ". The average grade of the assignment was: " + str(avg_scr))
        ses.commit()
        return
