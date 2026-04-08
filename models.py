from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Priority = Literal["low", "medium", "high"]
Category = Literal["billing", "technical", "refund"]
Sentiment = Literal["calm", "frustrated", "angry"]

class Ticket(BaseModel):
    id: int
    text: str
    sentiment: Sentiment
    sla_deadline: int

    # agent-filled
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    responded: bool = False
    escalated: bool = False
    steps_taken: int = 0

class Observation(BaseModel):
    tickets: List[Ticket]
    remaining_steps: int

class Action(BaseModel):
    type: Literal["classify", "respond", "escalate"]
    ticket_id: int = Field(ge=0)
    value: Optional[str] = None

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict