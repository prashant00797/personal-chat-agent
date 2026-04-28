from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message:str = Field(...,description="The chat message of the user")