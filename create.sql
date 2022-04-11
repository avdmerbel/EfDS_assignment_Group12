-- a text file with SQL code creating the database tables according to the schema in schema.pdf (.sql)

-- Students Table
CREATE TABLE IF NOT EXISTS Students (
   UniversityID INTEGER PRIMARY KEY,
   Name TEXT NOT NULL,
   Email TEXT NOT NULL UNIQUE
);

-- Question Table
CREATE TABLE IF NOT EXISTS Questions (
   QuestionID INTEGER PRIMARY KEY,
   Title TEXT NOT NULL UNIQUE,
   Text TEXT NOT NULL UNIQUE
);

-- Task Table
CREATE TABLE IF NOT EXISTS Tasks (
   TaskID INTEGER PRIMARY KEY,
   Title TEXT NOT NULL,
   Text TEXT NOT NULL
);

-- Evaluation Table
CREATE TABLE IF NOT EXISTS Evaluations (
   EvaluationID INTEGER PRIMARY KEY,
   EvaluationFinished BOOLEAN NOT NULL DEFAULT 0,
   SubmissionID INTEGER,
   FOREIGN KEY (SubmissionID)
      REFERENCES Submissions (SubmissionID)
);

-- QuestionTask Association Table
CREATE TABLE IF NOT EXISTS TaskQuestionLink (
   QuestionID INTEGER,
   TaskID INTEGER,
   PRIMARY KEY (QuestionID, TaskID),
   FOREIGN KEY (QuestionID) 
      REFERENCES Questions (QuestionID) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
   FOREIGN KEY (TaskID) 
      REFERENCES Tasks (TaskID) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);

-- Assignment Table
CREATE TABLE IF NOT EXISTS Assignments (
   AssignmentID INTEGER PRIMARY KEY,
   UniversityID INTEGER,
   TaskID INTEGER,
   FOREIGN KEY (UniversityID) 
      REFERENCES Students (UniversityID),
   FOREIGN KEY (TaskID) 
      REFERENCES Tasks (TaskID)
);  

-- Answer Table
CREATE TABLE IF NOT EXISTS Answers (
   AnswerID INTEGER PRIMARY KEY,
   Text TEXT NOT NULL,
   QuestionID INTEGER,
   SubmissionID INTEGER,
   FOREIGN KEY (QuestionID) 
      REFERENCES Questions (QuestionID),
   FOREIGN KEY (SubmissionID) 
      REFERENCES Submissions (SubmissionID)
); 

-- Submission Table
CREATE TABLE IF NOT EXISTS Submissions (
   SubmissionID INTEGER PRIMARY KEY,
   AssignmentID INTEGER,
   EvaluationRequest BOOLEAN NOT NULL DEFAULT 0,
   SubmissionTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (AssignmentID) 
      REFERENCES Assignments (AssignmentID)
);

-- Score Table
CREATE TABLE IF NOT EXISTS Scores (
   ScoreID INTEGER PRIMARY KEY,
   Value FLOAT,
   EvaluationID INTEGER,
   AnswerID INTEGER,
   FOREIGN KEY (EvaluationID) 
      REFERENCES Evaluations (EvaluationID),
   FOREIGN KEY (AnswerID) 
      REFERENCES Answers (AnswerID)
);