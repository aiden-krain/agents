from pydantic import BaseModel, Field
from agents import Agent


INSTRUCTIONS = """You are a helpful research assistant. Given a user's query, your job is to ask exactly 3 clarifying questions that will help better understand what the user is looking for and improve the quality of the research.

Your questions should:
- Help narrow down the scope of the research
- Clarify any ambiguous terms or concepts
- Understand the specific context or use case the user has in mind
- Be open-ended to encourage detailed responses

Focus on the most important aspects that would significantly impact how the research should be conducted."""


class ClarifyingQuestion(BaseModel):
    reasoning: str = Field(description="Why this question is important for improving the research")
    question: str = Field(description="A clarifying question to ask the user")

class ClarifyingQuestions(BaseModel):
    questions: list[ClarifyingQuestion] = Field(
        description="Exactly 3 clarifying questions to ask the user",
        min_items=3,
        max_items=3
    )


clarifying_agent = Agent(
    name="ClarifyingAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)
