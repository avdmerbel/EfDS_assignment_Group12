# python file with definitions of the main project class GradeDB with access methods to the database. (.py)
from schema import *
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

class GradeDB:
  def __init__(self, fileName):
    """ initializes the class """
    addr = "sqlite:///" + fileName
    self._engine = create_engine(addr,echo=False)
    self._sessionMaker = sessionmaker(bind=self._engine)
    
  def newSession(self):
    return self._sessionMaker()

  def addStudent(self, name, email, unid):
    """
    Adds student to Students Table

      Parameters:
        name (str): string with name of student
        email (str): string with email of student
        unid (int): integer with student UniID

    """
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
    """
    Adds question to Questions Table

      Parameters:
        title (str): string title for question
        text (str): string question text

      constraints:
        title has to be string object
        text has to be string object
    """
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


  def addTask(self, title, text, questions):
    """
    Adds task to Task Table

      Parameters:
        title (str): string with Task title
        text (str): string with overview text
        questions: questions from Questions Table belonging to the task

    """
    with self.newSession() as ses:
      qs = ses.query(Question).filter(Question.Title.in_(questions)).all()
      nt = Task(Title = title, Text = text)
      for i in range(len(qs)):
        nt.Questions.append(qs[i])
      ses.add(nt)
      ses.commit()
      return 
    
  def addAssignment(self, student, task):
    """
    Adds an assignment to Assignments Table

      Parameters:
        student (int): integer UniversityID belonging to 1 student
        task: task from Tasks table  

    Notifies student that a new assignment has ben assigned to them
    """
    with self.newSession() as ses:
      ts = ses.query(Task).filter(Task.Title == task).one()
      stud = ses.query(Student).filter(Student.UniversityID == student).one()
      assign = Assignment(UniversityID = student, TaskID = ts.TaskID)
      assign.Task = ts
      ses.add( assign )
      print("Notification of new Assignment has been sent to: " + str(stud.Email))
      ses.commit()
      return
    
  def newSubmission(self, student):
    """
    Adds submission of assignment to Submission Table

      Parameters:
        student (int): integer UniversityID belonging to 1 student
    """
    with self.newSession() as ses:
      sm = ses.query(Assignment).filter(Assignment.UniversityID == student).one()
      sub = Submission( AssignmentID = sm.AssignmentID, EvaluationRequest = False, SubmissionTime = datetime.now())
      sub.Student = student
      ses.add( sub )
      ses.commit()
      return

  def addAnswer(self, student, answer, question):
    """
    Adds answer to questions in assignment to Answer table

      Parameters:
        student (int): integer UniversityId of 1 student
        answer (str): string answer to question
        question: question from Question Table to be answered
    
    If evaluation was already requested for this answer a new one can not be added 
    """
    with self.newSession() as ses:
      asm = ses.query(Assignment).filter(Assignment.UniversityID == student).one()
      sbm = ses.query(Submission).filter(Submission.AssignmentID == asm.AssignmentID).one()
      if(sbm.EvaluationRequest == 1):
        print("This submission already has an Evaluation Request associated with it.")
        return  
      else: 
        ans = Answer(Text = answer, SubmissionID = sbm.SubmissionID, QuestionID = question)
        ses.add(ans)
        ses.commit()
        return

  def commitSubmission(self, SubmissionID):
    """
    Student commits submission for evaluation

      Parameters:
        SubmissionID (int): integer ID of submission
      
      Evaluation is requested and notification is sent to teacher 
    """
    with self.newSession() as ses:
      ses.query(Submission).filter(Submission.SubmissionID == SubmissionID).update({'EvaluationRequest': 1})
      print( "An email will now be sent to the teacher who has to grade submission" + str(SubmissionID))
      ses.commit()
      return

  def newEvaluation(self, submission ):
    """
    Adds new evaluation to Evaluation Table

      Parameters: 
        submission (int): integer submission ID

      If submission has no Evaluation request pending, new Evaluation not possible
    """
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
    """
    Adds score to Scores table

      Parameters:
        value (float): float value of score
        answer (int): integer answerID of answer that is scored
        evaluation (int): integer evaluationID of evaluation belonging to score
    
    if an assignment was already given a score it cannot be scored again
    """
  
    with self.newSession() as ses:
      req = ses.query(Evaluation).filter(Evaluation.EvaluationID == evaluation).one()
      if (req.EvaluationFinished == 1):
        print("This evaluation is already finished and sent to the student.")
        return
      else:
        sc = Score(Value = value, AnswerID = answer, EvaluationID = evaluation)
        ses.add(sc)
        ses.commit()
        return

  def commitEvaluation( self, evaluation ):
    """
    commits Evaluation

      Parameters:
        evaluation (int): integer evaluationID

      If Evaluation was already committed, new evaluation cannot be committed

      Sends notification to student that assignment was evaluated along with average score
    """
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
