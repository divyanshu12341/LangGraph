# so now we are creating a graph 
# the first thing you create is a state 
import os 
# first way
# 1) typed dict 
from typing import TypedDict
# 1 
class State(TypedDict):
    topic:str
    summary:str 
    score:str

# 2) pydantic approach 
# GOOD AT DATA VALIDATION AT TYPE-CHECKING 
from pydantic import BaseModel,Field,field_validator
class State(BaseModel):
    topic:str
    score:int 
    summary:str = ""
    @field_validator
    def score_positive(cls,v):
        if v<0:
            raise ValueError("Score must be positive")

# python dataclasses
# standard python dataclass but it is used very rarely
from dataclasses import dataclass,field
@dataclass
class State:
    topic:str  = ""
    summary:str = ""
    messages:list = field(default_factory=list)

# 4) using langgraph only 
from langgraph.graph import MessagesState
class State(MessagesState):
    user_name:str
