from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    attempts: List["QuizAttempt"] = Relationship(back_populates="user")


# This class defines both a Python Object AND a Database Table
class QuizAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topics.id")
    topic_name: str = Field(foreign_key="topics.name")
    score: int
    feedback: str  # Linked to Mistake Analysis
    user_id: int = Field(foreign_key="users.id")
    user: Users = Relationship(back_populates="attempts")   

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    topics: List["Topics"] = Relationship(back_populates="subject")

class Topics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    subject_id: int = Field(foreign_key="subject.id")
    subject: Subject = Relationship(back_populates="topics")
    materials: List["Materials"] = Relationship(back_populates="topics")

class Materials(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    file_path: str
    topic_id: int = Field(foreign_key="topics.id")
    topic: Topics = Relationship(back_populates="materials")