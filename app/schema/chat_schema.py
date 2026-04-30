from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id:str = Field(...,description="Unique id recieved per user session")
    message:str = Field(...,description="The chat message of the user")