# python file with definitions of the main project class GradeDB with access methods to the database. (.py)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # normally present once in a script!

class GradeDB:
  def __init__(self, fileName):
    addr = "sqlite:///" + fileName
    self._engine = create_engine(addr,echo=False)
    self._sessionMaker = sessionmaker(bind=self._engine)
    
  def newSession(self):
    return self._sessionMaker()
  
  def addQuestion(self, title, text):
    if (not title or not (type(title) == str)):
      print('This is not a valid name.')
      return
    elif ( not text or not (type(text) == str)):
      print('This is not a valid question.')
      return
    with self.newSession() as ses:
      nq = Question(Title = title, Text = text)
      ses.add( nq )
      ses.commit()
      return
    
  def newSubmission(self, assignment):
    with self.newSession() as ses:
      sub = Submission( Assignment = assignment )
      ses.add( sub )
      ses.commit()
      return
    
  def newEvaluation(self, request ):
    with self.newSession() as ses:
      eva= Evaluation( EvaluationRequest = request )
      ses.add( eva )
      ses.commit()
      return

# test