from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id:str = Field(...,description="The thread id of the current user")
    message:str = Field(...,description="The chat message of the user")