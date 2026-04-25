from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class RegisterUser(BaseModel):
    name:str = Field(...,description="The name of the user using the chat assistance")
    email:Optional[EmailStr] = Field(description="The email of the user using the chat assistance",default="") 
    company:Optional[str] = Field(description="The name of the company where the user currently works in",default="")

